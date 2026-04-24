#!/usr/bin/env python3
"""
每日业务摘要生成器 (v1.0) — 对应 FR-TK-012: 运营简报生成

功能:
  1. 聚合 TK 运营数据（任务状态、里程碑进度、预算消耗、系统告警）
  2. 生成 Markdown 格式日报 + 飞书交互式卡片
  3. 支持手动执行和 Cron 定时任务

用法:
  python3 daily_business_summary.py              # 生成并推送日报
  python3 daily_business_summary.py --dry-run    # 仅生成不推送
  python3 daily_business_summary.py --json-only  # 仅输出 JSON 不推送
  python3 daily_business_summary.py --date 2026-04-24  # 指定日期

Cron 配置 (每日 01:00 北京时间 / 10:00 PDT):
  0 10 * * * cd ~/agentic-os-collective && python3 tk/openclaw/core/daily_business_summary.py

数据来源:
  - ~/.openclaw/workspace/tasks/active/*.json   → 活跃任务
  - ~/.openclaw/workspace/tasks/completed/*.json → 已完成任务
  - ~/.openclaw/data/token_budget.json          → 预算消耗
  - ~/.openclaw/workspace/tasks/progress.txt    → 进度日志
  - tk/openclaw/skills/feishu-tk-notifier/      → 飞书推送通道
"""

import json, os, sys, time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# ── 路径解析 ───────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WORKSPACE   = Path.home() / ".openclaw/workspace"
ACTIVE_DIR  = WORKSPACE / "tasks/active"
COMPLETED_DIR = WORKSPACE / "tasks/completed"
PROGRESS_LOG = WORKSPACE / "tasks/progress.txt"
BUDGET_FILE  = Path.home() / ".openclaw/data/token_budget.json"
FEISHU_NOTIFIER_PATH = (
    PROJECT_ROOT / "tk/openclaw/skills/feishu-tk-notifier/feishu_notifier.py"
)

sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════
# 数据采集层
# ═══════════════════════════════════════════════════════════════

def load_json(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def collect_active_tasks() -> List[dict]:
    """扫描活跃任务目录，返回所有 TK 相关任务"""
    tasks = []
    if not ACTIVE_DIR.exists():
        return tasks
    for f in sorted(ACTIVE_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        t = load_json(f)
        if not t:
            continue
        project = t.get("project_id", "")
        title   = t.get("title", f.name)
        # 匹配 TK 相关任务 (project_id == "tk" 或 title 含关键词)
        if project == "tk" or any(kw in title.lower() for kw in ("tk", "运营", "日报", "飞书", "店小秘", "达人")):
            tasks.append({
                "id": t.get("id", f.stem),
                "title": t.get("title", f.stem),
                "status": t.get("status", "unknown"),
                "progress": t.get("progress", {}),
                "milestones": t.get("milestones", []),
                "metrics": t.get("metrics", {}),
                "groups": t.get("groups", []),
                "created_at": t.get("created_at", ""),
                "updated_at": t.get("updated_at", ""),
            })
    return tasks


def collect_completed_tasks(since_days: int = 7) -> List[dict]:
    """扫描已完成任务目录 (最近 N 天)"""
    tasks = []
    if not COMPLETED_DIR.exists():
        return tasks
    cutoff = time.time() - since_days * 86400
    for f in sorted(COMPLETED_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        if f.stat().st_mtime < cutoff:
            continue
        t = load_json(f)
        if not t:
            continue
        project = t.get("project_id", "")
        if project == "tk":
            tasks.append({
                "id": t.get("id", f.stem),
                "title": t.get("title", f.stem),
                "completed_at": t.get("completed_at", ""),
                "progress": t.get("progress", {}),
            })
    return tasks


def collect_budget() -> dict:
    """采集 Token 预算数据"""
    data = load_json(BUDGET_FILE)
    tk = data.get("tk", {})
    drama = data.get("drama", {})
    return {
        "tk_used": tk.get("used", 0),
        "tk_limit": tk.get("limit", 600000),
        "tk_pct": round(tk.get("used", 0) / max(tk.get("limit", 1), 1) * 100, 1),
        "drama_used": drama.get("used", 0),
        "drama_limit": drama.get("limit", 400000),
        "drama_pct": round(drama.get("used", 0) / max(drama.get("limit", 1), 1) * 100, 1),
    }


def collect_progress_events(since_hours: int = 24) -> List[str]:
    """采集最近 N 小时的进度日志条目"""
    events = []
    if not PROGRESS_LOG.exists():
        return events
    cutoff = datetime.now() - timedelta(hours=since_hours)
    try:
        with open(PROGRESS_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ts_str = line[:19]
                    event_ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                    if event_ts >= cutoff:
                        events.append(line)
                except ValueError:
                    if line:
                        events.append(line)
    except Exception:
        pass
    return events


def collect_artifacts() -> List[dict]:
    """扫描 artifact 目录，收集产出物"""
    artifacts = []
    artifact_base = WORKSPACE / "artifacts"
    if not artifact_base.exists():
        return artifacts
    for f in sorted(artifact_base.rglob("*"), key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True):
        if f.is_file() and not f.name.startswith("."):
            artifacts.append({
                "path": str(f.relative_to(artifact_base)),
                "size": f.stat().st_size,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    return artifacts[:50]


# ═══════════════════════════════════════════════════════════════
# 分析计算层
# ═══════════════════════════════════════════════════════════════

def compute_summary(active_tasks: List[dict], completed_tasks: List[dict],
                    budget: dict, events: List[str]) -> dict:
    """汇总所有数据，生成核心指标"""

    # ── 任务统计 ──
    task_running   = [t for t in active_tasks if t.get("status") == "running"]
    task_pending   = [t for t in active_tasks if t.get("status") == "pending"]
    task_failed    = [t for t in active_tasks if t.get("status") in ("failed", "blocked")]

    # ── 里程碑进度 ──
    total_milestones = 0
    completed_milestones = 0
    pending_milestones = 0
    for t in active_tasks:
        for m in t.get("milestones", []):
            total_milestones += 1
            if m.get("status") == "completed":
                completed_milestones += 1
            if m.get("status") == "pending":
                pending_milestones += 1

    # ── 告警检测 ──
    alerts = []
    if budget.get("tk_pct", 0) > 80:
        alerts.append(f"⚠️ TK Token 预算已使用 {budget['tk_pct']}%，接近上限")
    if task_failed:
        for tf in task_failed:
            alerts.append(f"❌ 任务失败: {tf['title']}")

    # ── 飞书群状态 (从 daily-report task 读取) ──
    feishu_groups = []
    for t in active_tasks:
        for g in t.get("groups", []):
            feishu_groups.append(g)

    # ── 构建汇总 ──
    summary = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now().isoformat(),
        "tasks": {
            "running": len(task_running),
            "pending": len(task_pending),
            "failed": len(task_failed),
            "completed_today": len(completed_tasks),
            "total_active": len(active_tasks),
        },
        "milestones": {
            "total": total_milestones,
            "completed": completed_milestones,
            "pending": pending_milestones,
            "progress_pct": round(completed_milestones / max(total_milestones, 1) * 100, 1),
        },
        "budget": budget,
        "alerts": alerts,
        "feishu_groups": feishu_groups,
        "recent_events": events[-10:],
        "task_details": [
            {
                "title": t["title"],
                "status": t["status"],
                "progress": t.get("progress", {}).get("percent", 0),
                "milestones_done": sum(1 for m in t.get("milestones", []) if m.get("status") == "completed"),
                "milestones_total": len(t.get("milestones", [])),
            }
            for t in active_tasks
        ],
    }

    # ── 数据完整性标记 ──
    # 标记哪些数据源为真实数据，哪些为占位
    summary["_data_sources"] = {
        "tasks": {"available": len(active_tasks) > 0, "real": True},
        "budget": {"available": budget.get("tk_used", 0) > 0, "real": True},
        "events": {"available": PROGRESS_LOG.exists(), "real": True,
                   "note": f"最近24h有{len(events)}条事件" if events else "最近24h无新事件"},
        "gmv": {"available": False, "real": False,
                "note": "GMV/订单/库存数据需店小秘 API 接入 (FR-TK-007, P1)"},
        "products": {"available": False, "real": False,
                     "note": "品类数据需 TikTok API 接入 (FR-TK-001, P0)"},
        "creators": {"available": False, "real": False,
                     "note": "达人数据需 TikTok 达人联盟 API 接入 (FR-TK-010, P0)"},
    }

    return summary


# ═══════════════════════════════════════════════════════════════
# 输出生成层
# ═══════════════════════════════════════════════════════════════

def format_markdown(summary: dict) -> str:
    """生成 Markdown 格式日报"""
    b = summary["budget"]
    t = summary["tasks"]
    m = summary["milestones"]

    lines = [
        f"# 📊 TK 运营日报 {summary['date']}",
        "",
        f"> 生成时间: {summary['generated_at']}",
        "",
        "---",
        "",
        "## 📈 核心指标",
        "",
        f"| 指标 | 数值 | 状态 |",
        f"|------|------|------|",
        f"| 活跃任务 | {t['running']} | {'✅' if t['running'] > 0 else '⚠️ 无活跃任务'} |",
        f"| 待处理 | {t['pending']} | {'⚠️' if t['pending'] > 0 else '✅'} |",
        f"| 失败 | {t['failed']} | {'❌' if t['failed'] > 0 else '✅'} |",
        f"| 今日完成 | {t['completed_today']} | |",
        f"| 里程碑进度 | {m['completed']}/{m['total']} ({m['progress_pct']}%) | {'✅' if m['progress_pct'] > 70 else '⚠️' if m['progress_pct'] > 30 else '❌'} |",
        f"| TK Token 消耗 | {b['tk_used']:,} / {b['tk_limit']:,} ({b['tk_pct']}%) | {'⚠️' if b['tk_pct'] > 80 else '✅'} |",
        f"| Drama Token 消耗 | {b['drama_used']:,} / {b['drama_limit']:,} ({b['drama_pct']}%) | {'⚠️' if b['drama_pct'] > 80 else '✅'} |",
        "",
        "---",
        "",
        "## 📋 任务详情",
        "",
        "| 任务 | 状态 | 进度 | 里程碑 |",
        "|------|------|------|--------|",
    ]

    status_icon = {"running": "🟢", "pending": "🟡", "completed": "✅", "failed": "❌", "blocked": "⛔"}
    for td in summary.get("task_details", []):
        icon = status_icon.get(td["status"], "❓")
        lines.append(
            f"| {td['title']} | {icon} {td['status']} | {td['progress']}% | "
            f"{td['milestones_done']}/{td['milestones_total']} |"
        )

    # 告警
    if summary.get("alerts"):
        lines.extend(["", "---", "", "## ⚠️ 告警", ""])
        for a in summary["alerts"]:
            lines.append(f"- {a}")

    # 近期事件
    if summary.get("recent_events"):
        lines.extend(["", "---", "", "## 📝 最近 24 小时事件", ""])
        for e in summary["recent_events"][-8:]:
            lines.append(f"- {e}")

    # 数据完整性说明
    ds = summary.get("_data_sources", {})
    missing = {k: v for k, v in ds.items() if not v.get("available")}
    if missing:
        lines.extend(["", "---", "", "## ⚠️ 数据完整性说明", ""])
        lines.append("以下数据源尚未接入，相关指标为占位数据：")
        lines.append("")
        for k, v in missing.items():
            lines.append(f"- **{k}**: {v.get('note', '未接入')}")
        lines.append("")
        lines.append("")
        lines.append(f"*报告由 Agentic OS v3.3 自动生成 | 下次推送: {datetime.now().strftime('%Y-%m-%d')} 10:00 PDT*")

    return "\n".join(lines)


def build_feishu_card(summary: dict) -> dict:
    """构建飞书交互式卡片 (对应 PRD 6.3 线框图)"""
    b = summary["budget"]
    t = summary["tasks"]
    m = summary["milestones"]

    # 构建核心指标 Markdown
    metrics_md = (
        f"🟢 活跃任务: **{t['running']}** 　 "
        f"✅ 今日完成: **{t['completed_today']}**\n"
        f"📊 里程碑: **{m['progress_pct']}%** ({m['completed']}/{m['total']}) 　 "
        f"💰 Token: **{b['tk_pct']}%** ({b['tk_used']:,}/{b['tk_limit']:,})"
    )

    # 任务列表
    status_icon = {"running": "🟢", "pending": "🟡", "completed": "✅", "failed": "❌"}
    task_lines = []
    for td in summary.get("task_details", [])[:10]:
        icon = status_icon.get(td["status"], "❓")
        task_lines.append(
            f"{icon} {td['title']} — {td['milestones_done']}/{td['milestones_total']} 里程碑"
        )

    task_md = "\n".join(task_lines) if task_lines else "暂无活跃任务"

    # 告警
    alert_md = ""
    if summary.get("alerts"):
        alert_md = "\n".join(f"• {a}" for a in summary["alerts"])

    # 数据完整性说明
    ds = summary.get("_data_sources", {})
    missing_data_keys = [k for k, v in ds.items() if not v.get("available") and k not in ("gmv", "products", "creators")]
    note_text = ""
    if missing_data_keys:
        note_text = "⚠️ " + ", ".join(missing_data_keys) + " 数据源未接入"

    # ── 组装飞书卡片 ──
    elements = [
        {
            "tag": "markdown",
            "content": metrics_md,
        },
        {"tag": "hr"},
        {
            "tag": "markdown",
            "content": f"**📋 任务详情**\n{task_md}",
        },
    ]

    if alert_md:
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "markdown",
            "content": f"**⚠️ 告警**\n{alert_md}",
        })

    if summary.get("recent_events"):
        recent = "\n".join(f"• {e}" for e in summary["recent_events"][-5:])
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "markdown",
            "content": f"**📝 最近事件**\n{recent}",
        })

    elements.append({"tag": "hr"})
    elements.append({
        "tag": "note",
        "elements": [
            {"tag": "plain_text", "content": f"⏰ {summary['generated_at']} | Agentic OS v3.3"}
        ],
    })

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📊 TK 运营日报 {summary['date']}",
                },
                "template": "blue",
            },
            "elements": elements,
        },
    }

    return card


# ═══════════════════════════════════════════════════════════════
# 推送层 — 使用 shared/config.py 中的 Webhook ID 拼装 URL
# ═══════════════════════════════════════════════════════════════

def get_feishu_webhooks() -> dict:
    """获取所有已配置的飞书 Webhook URL (频道名 → 完整URL)"""
    try:
        from shared.config import config
        base = config.FEISHU_WEBHOOK_BASE
        return {ch: f"{base}/{wid}" for ch, wid in config.FEISHU_WEBHOOK_IDS.items()}
    except Exception:
        return {}


def push_to_feishu(card: dict, webhook_url: str, channel_name: str = "") -> bool:
    """推送飞书交互式卡片到单个频道"""
    if not webhook_url:
        print("⚠️  Webhook URL 为空，跳过推送")
        return False
    try:
        import requests
        resp = requests.post(webhook_url, json=card, timeout=15)
        if resp.status_code == 200:
            body = resp.json()
            if body.get("code") == 0:
                label = f" → {channel_name}" if channel_name else ""
                print(f"✅ 飞书日报推送成功{label}")
                return True
            else:
                print(f"⚠️  飞书返回错误 ({channel_name}): {body}")
                return False
        else:
            print(f"❌ 飞书推送失败 ({channel_name}): HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ 飞书推送异常 ({channel_name}): {e}")
        return False


def push_to_channels(summary: dict, channels: list = None) -> dict:
    """推送到指定飞书频道列表，返回结果统计"""
    webhooks = get_feishu_webhooks()
    if not webhooks:
        print("⚠️  无可用飞书 Webhook 配置")
        return {"success": 0, "failed": 0, "total": 0}

    if channels is None:
        channels = ["数据看板"]

    card = build_feishu_card(summary)
    results = {"success": [], "failed": []}

    print(f"\n📤 推送飞书日报到 {len(channels)} 个频道...")
    for ch in channels:
        url = webhooks.get(ch, "")
        if not url:
            print(f"  ⚠️  频道 {ch}: Webhook 未配置")
            results["failed"].append(ch)
            continue
        if push_to_feishu(card, url, ch):
            results["success"].append(ch)
        else:
            results["failed"].append(ch)

    return {
        "success": len(results["success"]),
        "failed": len(results["failed"]),
        "total": len(channels),
        "channels": results,
    }


def save_report(summary: dict, md_content: str, report_dir: Path = None):
    """保存日报到文件"""
    if report_dir is None:
        report_dir = WORKSPACE / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    date_str = summary["date"]
    json_path = report_dir / f"daily_summary_{date_str}.json"
    md_path   = report_dir / f"daily_summary_{date_str}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"📄 JSON 已保存: {json_path}")
    print(f"📄 Markdown 已保存: {md_path}")


# ═══════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="TK 运营日报生成器 — 对应 FR-TK-012 P0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 daily_business_summary.py                    # 生成 + 推送
  python3 daily_business_summary.py --dry-run          # 仅预览，不推送
  python3 daily_business_summary.py --json-only        # 仅输出 JSON
  python3 daily_business_summary.py --date 2026-04-24  # 指定日期
  python3 daily_business_summary.py --no-feishu        # 生成但不推送飞书
        """,
    )
    parser.add_argument("--dry-run", action="store_true", help="仅生成并打印，不推送不保存")
    parser.add_argument("--json-only", action="store_true", help="仅输出 JSON 到 stdout")
    parser.add_argument("--no-feishu", action="store_true", help="跳过飞书推送")
    parser.add_argument("--date", default=None, help="指定报告日期 (YYYY-MM-DD)")
    parser.add_argument("--channel", default=None, help="目标飞书频道 (默认: 数据看板)")
    parser.add_argument("--all-channels", action="store_true", help="推送到全部 8 个飞书频道")
    args = parser.parse_args()

    # ── 1. 采集数据 ──
    if not args.json_only:
        print("📡 采集数据中...")
    active_tasks    = collect_active_tasks()
    completed_tasks = collect_completed_tasks()
    budget_data     = collect_budget()
    recent_events   = collect_progress_events()
    artifacts       = collect_artifacts()

    # ── 2. 分析汇总 ──
    summary = compute_summary(active_tasks, completed_tasks, budget_data, recent_events)
    if args.date:
        summary["date"] = args.date

    # ── 3. 生成报告 ──
    md_content = format_markdown(summary)

    if args.json_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    if args.dry_run:
        print("\n" + "=" * 60)
        print(md_content)
        print("=" * 60)
        print("\n[DRY RUN] 未保存文件，未推送飞书")
        return

    # ── 4. 保存报告 ──
    save_report(summary, md_content)

    # ── 5. 推送飞书 ──
    if not args.no_feishu:
        if args.all_channels:
            channels = list(get_feishu_webhooks().keys())
        elif args.channel:
            channels = [args.channel]
        else:
            channels = ["数据看板"]

        result = push_to_channels(summary, channels)
        print(f"📊 推送结果: {result['success']}/{result['total']} 成功" +
              (f", {result['failed']} 失败" if result['failed'] else ""))

    print(f"\n✅ 日报生成完成: {summary['date']}")


if __name__ == "__main__":
    main()
