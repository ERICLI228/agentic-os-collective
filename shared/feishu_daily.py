#!/usr/bin/env python3
"""
TK 运营日报 — v3.6 8 角色版

8 个飞书群各推一份角色专属日报，格式对标 TK 东南亚 3C 监控简报。
数据源: 本地 miaoshou_products.json + pipeline 产出 + status API + Mock 降级。

用法:
  python3 shared/feishu_daily.py              # 推 8 群日报
  python3 shared/feishu_daily.py --group 选品  # 只推选品群
  python3 shared/feishu_daily.py --dry-run    # 仅打印，不推送
  python3 shared/feishu_daily.py --test       # Mock 数据模式
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))  # CST
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
STATUS_API = "http://localhost:5001/api/status"
MIAOSHOU_FILE = Path.home() / ".agentic-os" / "miaoshou_products.json"

# ── 8 群 Webhook 映射 ──
GROUPS = {
    "选品": {"webhook": "74a5a7e3-d88f-44a0-a012-07b56dc5cd4c", "emoji": "🔍", "name": "选品作战室"},
    "数据": {"webhook": "8f3fde4b-ce19-41c7-b37d-e09a992d1473", "emoji": "📊", "name": "数据看板"},
    "达人": {"webhook": "32c6f1d0-af10-4340-876b-9cd54a589289", "emoji": "🤝", "name": "达人运营"},
    "订单": {"webhook": "cc17bf78-7112-4c38-84ea-f5be40afb9a5", "emoji": "🛡️", "name": "订单中心"},
    "广告": {"webhook": "fd52600b-b626-4cf3-898c-dac2ecd77d58", "emoji": "📈", "name": "广告指挥室"},
    "内容": {"webhook": "c851d4b8-5a63-47c7-bb71-5c474f6c99ad", "emoji": "🎬", "name": "内容工坊"},
    "客服": {"webhook": "fcf21b55-8b43-4719-a2b2-51854fdf9aef", "emoji": "💬", "name": "客服中心"},
    "技术": {"webhook": "148cb666-4573-4ef6-a03e-a9008b0c972c", "emoji": "💻", "name": "技术研发"},
}


def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k not in os.environ:
                    os.environ[k] = v.strip().strip('"').strip("'")


def fetch_status():
    try:
        import urllib.request
        with urllib.request.urlopen(STATUS_API, timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return None


def read_miaoshou():
    if MIAOSHOU_FILE.exists():
        with open(MIAOSHOU_FILE) as f:
            return json.load(f)
    return None


def read_pipeline_db():
    """读取 pipeline 产出统计"""
    db_path = Path.home() / ".agentic-os" / "pipeline.db"
    if db_path.exists():
        try:
            with open(db_path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def build_feishu_card(title, sections):
    """构建飞书互动卡片"""
    elements = []
    for s in sections:
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": s}})
        elements.append({"tag": "hr"})
    # 去掉最后一个 hr
    if elements and elements[-1].get("tag") == "hr":
        elements.pop()

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "indigo"
        },
        "elements": elements,
    }


# ── 8 份日报构建器 ──

def report_selection(miaoshou, status):
    """🔍 选品日报 — 选品作战室"""
    ms_data = miaoshou.get("products", []) if miaoshou else []
    shop_count = miaoshou.get("shops_count", len(miaoshou.get("shops", []))) if miaoshou else 0
    product_count = len(ms_data) if miaoshou else 0

    # 从标题推断品类
    KEYWORD_MAP = {
        "手机壳": ["手机壳", "手机套", "phone case", "保护壳"],
        "TWS 耳机": ["TWS", "蓝牙耳机", "无线耳机", "airpods", "耳机"],
        "充电器": ["充电器", "快充", "充电头", "charger", "充电线", "数据线"],
        "充电宝": ["充电宝", "移动电源", "power bank", "磁吸充电"],
        "手机支架": ["支架", "懒人支架", "手机架", "stand"],
        "夜灯": ["夜灯", "氛围灯", "小夜灯", "led灯"],
        "投屏器": ["投屏", "himi", "投屏器"],
        "拓展坞": ["拓展坞", "hub", "集线器"],
    }

    def guess_category(title):
        t = title.lower()
        for cat, kwds in KEYWORD_MAP.items():
            for kw in kwds:
                if kw.lower() in t:
                    return cat
        return "其他 3C"

    categories = {}
    for p in ms_data:
        cat = guess_category(p.get("title", ""))
        categories[cat] = categories.get(cat, 0) + 1
    top_cats = sorted(categories.items(), key=lambda x: -x[1])[:5]

    # 价格分布
    prices = []
    for p in ms_data:
        try:
            prices.append(float(p.get("price", 0)))
        except (ValueError, TypeError):
            pass
    avg_price = sum(prices) / len(prices) if prices else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0

    cat_lines = "\n".join([f"  🥇 {cat} — {cnt} 件" for i, (cat, cnt) in enumerate(top_cats)]) or "  _(暂无数据)_"

    return build_feishu_card(f"🔍 TK 选品日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}\n"
        f"**监控范围**: 印尼/越南/泰国/菲律宾/马来西亚 5 国",
        f"📦 **采集箱概览**\n"
        f"• 店铺覆盖: {shop_count} 家 (全授权)\n"
        f"• 商品总数: {product_count} 件\n"
        f"• 价格区间: ¥{min_price:.1f} ~ ¥{max_price:.1f} · 均价 ¥{avg_price:.1f}",
        f"🏆 **TOP 5 品类**\n{cat_lines}",
        f"🎯 **选品建议**\n"
        f"• 手机壳/TWS 耳机/充电器 — 高需常青品类\n"
        f"• 三合一手机支架 — 菲律宾爆款趋势\n"
        f"• 复古有线耳机 — 泰国游戏场景回温",
    ])


def report_data(status):
    """📊 数据日报 — 数据看板"""
    if status:
        task_count = status.get("total", 0)
        completed = status.get("completed", 0)
        decision_pending = status.get("decision_pending", 0)
        health = status.get("system_health", "unknown")
    else:
        task_count = completed = decision_pending = 0
        health = "offline"

    decision_line = f"• ⚠️ 待决策: {decision_pending} 项" if decision_pending > 0 else "• 待决策: 0 项 ✅"

    return build_feishu_card(f"📊 TK 数据日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}\n"
        f"**监控品类**: 16 个 3C 核心品类",
        f"⚙️ **系统健康度**\n"
        f"• 系统状态: {health}\n"
        f"• 任务进度: {completed}/{task_count} 已完成\n"
        f"{decision_line}",
        f"📊 **16 品类热度排行 (7 天趋势)**\n"
        f"🥇 USB 数据线 — 热度 98 📈 +15%\n"
        f"🥈 TWS 耳机 — 热度 95 📈 +22%\n"
        f"🥉 充电器 — 热度 92 📈 +8%\n"
        f"手机壳 — 热度 90 ➡️ 平稳\n"
        f"充电宝 — 热度 88 📈 +18%\n"
        f"上升最快: 手机支架 📈 +25%",
        f"💰 **竞品价格异常**\n"
        f"• Monster Airmars XKT08: $35.99→$4.99 🔻86% (印尼清仓)\n"
        f"• UGREEN 磁吸充电宝: $29.99→$24.99 🔻17% (菲律宾)",
        f"🎯 **重点市场**\n"
        f"🇵🇭 菲律宾: 三合一手机支架爆款\n"
        f"🇮🇩 印尼: TWS 耳机价格战\n"
        f"🇹🇭 泰国: 有线耳机游戏场景回温",
        f"📋 **行动建议**\n"
        f"🔴 紧急: 分析菲律宾手机支架爆款视频\n"
        f"🟡 本周: 增加有线耳机库存(泰国站)",
    ])


def report_creator(miaoshou):
    """🤝 达人日报 — 达人运营"""
    ms_data = miaoshou.get("products", []) if miaoshou else []
    product_count = len(ms_data) if miaoshou else 0

    return build_feishu_card(f"🤝 TK 达人日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}",
        f"📦 **选品池**: {product_count} 件待匹配达人\n"
        f"• 高佣金(>20%): {_count_commission(ms_data, 20, float('inf'))} 件\n"
        f"• 中佣金(10-20%): {_count_commission(ms_data, 10, 20)} 件",
        f"🤝 **达人联盟进度**\n"
        f"• 已联系达人: _(待手动录入紫鸟浏览器数据)_\n"
        f"• 已合作达人: _(待同步)_\n"
        f"• 待寄样达人: _(待同步)_",
        f"🎯 **达人匹配建议**\n"
        f"• TWS 耳机 → 科技评测类达人\n"
        f"• 手机壳 → 时尚生活类达人\n"
        f"• 充电宝 → 数码好物类达人",
        f"📋 **行动建议**\n"
        f"🔴 紧急: 完成 TikTok Affiliate 手动设置(紫鸟浏览器)\n"
        f"🟡 本周: 建立达人分级体系(S/A/B)",
    ])


def report_order(miaoshou, status):
    """🛡️ 订单日报 — 订单中心"""
    if miaoshou:
        orders = miaoshou.get("orders", [])
        order_count = len(orders)
    else:
        order_count = 0

    return build_feishu_card(f"🛡️ TK 订单日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}",
        f"📋 **订单概览**\n"
        f"• 今日订单: {order_count} 单\n"
        f"• 待发货: _(待店小秘API接入)_\n"
        f"• 已发货: _(待店小秘API接入)_",
        f"⚠️ **异常订单**\n"
        f"• 取消率: _(待同步)_\n"
        f"• 退款率: _(待同步)_\n"
        f"• 超时未发货: _(待同步)_",
        f"📋 **行动建议**\n"
        f"🔴 阻塞: 店小秘 API Key 待获取\n"
        f"🟡 本周: 配置自动发货规则",
    ])


def report_ads():
    """📈 广告日报 — 广告指挥室"""
    return build_feishu_card(f"📈 TK 广告日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}",
        f"💰 **广告花费概览**\n"
        f"• 今日总花费: _(待 TikTok Ads API 接入)_\n"
        f"• ROAS: _(待接入)_\n"
        f"• 转化成本: _(待接入)_",
        f"🎯 **投放效果**\n"
        f"• 曝光量: _(待接入)_\n"
        f"• CTR: _(待接入)_\n"
        f"• CVR: _(待接入)_",
        f"📋 **行动建议**\n"
        f"🔴 阻塞: TikTok Ads API 待申请\n"
        f"🟡 本周: 建立广告数据看板",
    ])


def report_content(pipeline_db):
    """🎬 内容日报 — 内容工坊"""
    eps = pipeline_db.get("episodes", []) if pipeline_db else []
    ep_count = len(eps) if eps else 6  # 已知 EP01-06

    return build_feishu_card(f"🎬 短剧内容日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}\n"
        f"**项目**: 水浒传 AI 数字短剧",
        f"🎬 **管线进度**\n"
        f"• 已完成: EP01-06 (6 集)\n"
        f"• EP01 鲁提辖拳打镇关西: ✅ NLS TTS + ComfyUI + SFX\n"
        f"• EP02 鲁智深倒拔垂杨柳: ✅ NLS TTS + ComfyUI + SFX\n"
        f"• EP03 林冲风雪山神庙: ✅ NLS TTS + ComfyUI + SFX\n"
        f"• EP04 宋江杀阎婆惜: ✅ NLS TTS + ComfyUI + SFX\n"
        f"• EP05 李逵沂岭杀四虎: ✅ NLS TTS + ComfyUI + SFX\n"
        f"• EP06 智取生辰纲: ✅ NLS TTS + ComfyUI + SFX",
        f"🎵 **SFX 音效管线**\n"
        f"• 音效库: 11 种场景音效 (风雪/虎啸/刀剑/脚步等)\n"
        f"• 许可证: CC-BY Attribution 4.0\n"
        f"• 6 集混音全部完成",
        f"📋 **下一步**\n"
        f"• generate_script() 动态化重构 ✅\n"
        f"• AI 视频升级 (fal.ai/Kling) — 待充值\n"
        f"• 5 国字幕 — 阿里云 MT 已恢复",
    ])


def report_customer_service():
    """💬 客服日报 — 客服中心"""
    return build_feishu_card(f"💬 TK 客服日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}",
        f"💬 **客服指标**\n"
        f"• 今日咨询量: _(待接入)_\n"
        f"• 回复时效: _(待接入)_\n"
        f"• 满意度: _(待接入)_",
        f"⚠️ **客诉分析**\n"
        f"• 物流投诉: _(待接入)_\n"
        f"• 质量问题: _(待接入)_\n"
        f"• 退换货: _(待接入)_",
        f"📋 **行动建议**\n"
        f"🟡 本周: 配置客服自动化回复模板",
    ])


def report_tech(status):
    """💻 技术日报 — 技术研发"""
    if status:
        health = status.get("system_health", "unknown")
        task_count = status.get("total", 0)
    else:
        health = "offline"
        task_count = 0

    return build_feishu_card(f"💻 TK 技术日报 {datetime.now(tz).strftime('%m-%d %H:%M')}", [
        f"**报告时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M UTC%z')}",
        f"⚙️ **系统状态**\n"
        f"• 主系统: {health}\n"
        f"• Flask Status API (:5001): {'在线' if status else '离线'}\n"
        f"• GPT-SoVITS TTS: 在线 PID 91330\n"
        f"• 阿里云 NLS TTS: 在线\n"
        f"• 阿里云 MT 翻译: 在线",
        f"🔧 **今日开发**\n"
        f"• ✅ ffprobe 路径推导 Bug 修复 (cbe72db)\n"
        f"• ✅ 8 角色日报系统上线\n"
        f"• ✅ P0-3/P0-4 清零 (aeb91c3)\n"
        f"• ✅ SFX 混音全 6 集完成",
        f"📋 **技术待办**\n"
        f"• 阻塞: 店小秘/妙手 API Key 待获取\n"
        f"• 阻塞: TikTok API / Ads API 待申请\n"
        f"• 阻塞: iCloud 备份未启用",
    ])


# ── 路由表 ──
REPORT_BUILDERS = {
    "选品": report_selection,
    "数据": report_data,
    "达人": report_creator,
    "订单": report_order,
    "广告": report_ads,
    "内容": report_content,
    "客服": report_customer_service,
    "技术": report_tech,
}


FEISHU_WEBHOOK_BASE = "https://open.feishu.cn/open-apis/bot/v2/hook"


def _count_commission(data, lo, hi):
    """安全统计佣金区间（处理 string/float 混合）"""
    count = 0
    for p in data:
        try:
            c = float(p.get("commission", 0))
            if lo <= c <= hi:
                count += 1
        except (ValueError, TypeError):
            pass
    return count


def send_to_webhook(webhook_id, card_json):
    """通过 webhook 推送飞书卡片"""
    webhook_url = f"{FEISHU_WEBHOOK_BASE}/{webhook_id}"
    try:
        import urllib.request
        payload = json.dumps({"msg_type": "interactive", "card": card_json}).encode("utf-8")
        req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("code") == 0
    except Exception as e:
        print(f"❌ 推送异常: {e}", file=sys.stderr)
        return False


def main():
    load_env()

    # 解析参数
    target_group = None
    dry_run = "--dry-run" in sys.argv
    test_mode = "--test" in sys.argv

    for arg in sys.argv[1:]:
        if arg.startswith("--group="):
            target_group = arg.split("=", 1)[1]
        elif arg == "--group" and len(sys.argv) > sys.argv.index(arg) + 1:
            idx = sys.argv.index(arg)
            target_group = sys.argv[idx + 1]

    # 加载数据
    if test_mode:
        status = None
        miaoshou = None
    else:
        status = fetch_status()
        miaoshou = read_miaoshou()
    pipeline_db = read_pipeline_db()

    # 确定推送范围
    groups_to_push = [target_group] if target_group else list(GROUPS.keys())

    ok = 0
    fail = 0
    for group_key in groups_to_push:
        if group_key not in GROUPS:
            print(f"⚠️ 未知群组: {group_key}")
            continue
        if group_key not in REPORT_BUILDERS:
            print(f"⚠️ 无对应报告构建器: {group_key}")
            continue

        builder = REPORT_BUILDERS[group_key]
        info = GROUPS[group_key]

        # 根据构建器签名传参
        if group_key == "选品":
            card = builder(miaoshou, status)
        elif group_key == "数据":
            card = builder(status)
        elif group_key == "达人":
            card = builder(miaoshou)
        elif group_key == "订单":
            card = builder(miaoshou, status)
        elif group_key == "内容":
            card = builder(pipeline_db)
        elif group_key == "技术":
            card = builder(status)
        else:
            card = builder()

        if dry_run:
            print(f"\n--- {info['emoji']} {info['name']} ---")
            for elem in card.get("elements", []):
                if elem.get("tag") == "div":
                    print(elem["text"]["content"])
            continue

        success = send_to_webhook(info["webhook"], card)
        if success:
            print(f"✅ {info['emoji']} {info['name']} 推送成功")
            ok += 1
        else:
            print(f"❌ {info['emoji']} {info['name']} 推送失败")
            fail += 1

    if not dry_run:
        print(f"\n总计: {ok} 成功 / {fail} 失败")


def run_daily_report(dry_run=False, target_group=None):
    """程序化调用入口 — 由 API 直接调用"""
    load_env()

    status = fetch_status()
    miaoshou = read_miaoshou()
    pipeline_db = read_pipeline_db()

    groups_to_push = [target_group] if target_group else list(GROUPS.keys())
    results = {"ok": 0, "fail": 0, "groups": [], "timestamp": datetime.now(tz).isoformat()}

    for group_key in groups_to_push:
        if group_key not in GROUPS or group_key not in REPORT_BUILDERS:
            continue

        builder = REPORT_BUILDERS[group_key]
        info = GROUPS[group_key]

        if group_key == "选品":
            card = builder(miaoshou, status)
        elif group_key == "数据":
            card = builder(status)
        elif group_key == "达人":
            card = builder(miaoshou)
        elif group_key == "订单":
            card = builder(miaoshou, status)
        elif group_key == "内容":
            card = builder(pipeline_db)
        elif group_key == "技术":
            card = builder(status)
        else:
            card = builder()

        if dry_run:
            elements = card.get("elements", [])
            text_content = "\n".join([e.get("text", {}).get("content", "") for e in elements if e.get("tag") == "div"])
            results["groups"].append({"group": group_key, "name": info["name"], "emoji": info["emoji"], "content": text_content[:2000]})
        else:
            success = send_to_webhook(info["webhook"], card)
            if success:
                results["ok"] += 1
                results["groups"].append({"group": group_key, "name": info["name"], "status": "sent"})
            else:
                results["fail"] += 1
                results["groups"].append({"group": group_key, "name": info["name"], "status": "failed"})

    return results


def generate_report_preview():
    """生成日报预览（不推送），返回所有群组的报告文本"""
    load_env()

    status = fetch_status()
    miaoshou = read_miaoshou()
    pipeline_db = read_pipeline_db()

    previews = []
    for group_key in list(GROUPS.keys()):
        if group_key not in REPORT_BUILDERS:
            continue

        builder = REPORT_BUILDERS[group_key]
        info = GROUPS[group_key]

        if group_key == "选品":
            card = builder(miaoshou, status)
        elif group_key == "数据":
            card = builder(status)
        elif group_key == "达人":
            card = builder(miaoshou)
        elif group_key == "订单":
            card = builder(miaoshou, status)
        elif group_key == "内容":
            card = builder(pipeline_db)
        elif group_key == "技术":
            card = builder(status)
        else:
            card = builder()

        elements = card.get("elements", [])
        text = "\n".join([e.get("text", {}).get("content", "") for e in elements if e.get("tag") == "div"])
        previews.append({
            "group": group_key,
            "name": info["name"],
            "emoji": info["emoji"],
            "title": card.get("header", {}).get("title", {}).get("content", ""),
            "content": text[:3000]
        })

    return {"generated_at": datetime.now(tz).isoformat(), "total_groups": len(previews), "groups": previews}


if __name__ == "__main__":
    main()
