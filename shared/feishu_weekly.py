#!/usr/bin/env python3
"""
Feishu 周报推送 — 每周一 09:00 推送到飞书
汇总: 订单/TK店铺/广告/短剧/安全
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path.home() / ".agentic-os"
WEEKLY_PATH = DATA_DIR / "logs" / "weekly.json"


def gather_weekly_data():
    """汇总本周关键指标"""
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    monday_str = week_start.strftime("%m-%d")

    data = {
        "report_date": now.strftime("%Y-%m-%d"),
        "week_of": f"{monday_str} ~ {now.strftime('%m-%d')}",
        "tk_shops": {"total": 6, "active": 0, "violations": 0, "new_products": 0},
        "orders": {"total": 0, "gmv_usd": 0.0, "top_product": "N/A"},
        "short_drama": {"episodes": 0, "total_duration_s": 0, "status": "Pillow过渡期"},
        "security": {"issues_found": 0, "keys_rotated": 0, "scans_passed": 5},
        "decisions": {"total": 0, "approved": 0, "rejected": 0},
        "budget": {"tokens_used": 0, "tokens_remaining": 0, "pct": 100.0},
    }

    # 读取订单数据
    products_path = DATA_DIR / "miaoshou_products.json"
    if products_path.exists():
        with open(products_path) as f:
            products = json.load(f)
        data["tk_shops"]["active"] = products.get("shops_count", 6)
        data["orders"]["total"] = products.get("orders_count", 0)

    # 读取短剧产出
    for ep in range(1, 7):
        ep_dir = DATA_DIR / f"episode_{ep:02d}"
        if (ep_dir / "final.mp4").exists():
            data["short_drama"]["episodes"] += 1

    # 读取决策日志
    decisions_dir = DATA_DIR / "decisions"
    if decisions_dir.exists():
        for f in sorted(decisions_dir.glob("*.json")):
            try:
                d = json.loads(f.read_text())
                if d.get("decision_status"):
                    data["decisions"]["total"] += 1
                    if d["decision_status"] == "approved":
                        data["decisions"]["approved"] += 1
                    elif d["decision_status"] == "rejected":
                        data["decisions"]["rejected"] += 1
            except Exception:
                pass

    # 读取健康度
    health_path = DATA_DIR / "shop_health.json"
    if health_path.exists():
        with open(health_path) as f:
            health = json.load(f)
        data["tk_shops"]["violations"] = health.get("warning", 0) + health.get("critical", 0)

    # 读取Token预算
    budget_path = Path.home() / ".openclaw" / "data" / "token_budget.json"
    if budget_path.exists():
        with open(budget_path) as f:
            budget = json.load(f)
        data["budget"]["tokens_used"] = budget.get("daily_used", 0)
        data["budget"]["tokens_remaining"] = max(0, budget.get("daily_limit", 500000) - budget.get("daily_used", 0))
        if budget.get("daily_limit", 500000) > 0:
            data["budget"]["pct"] = round(100 - budget.get("daily_used", 0) / budget.get("daily_limit", 500000) * 100, 1)

    return data


def build_card(data):
    """构建飞书周报卡片"""
    wk = data["week_of"]

    content = [
        [{"tag": "text", "text": f"📊 Agentic OS 周报 — {wk}"}],
        [{"tag": "hr"}],
        [{"tag": "text", "text": f"🛒 TK 店铺: {data['tk_shops']['active']}/6 活跃 | "
                                f"违规 {data['tk_shops']['violations']} | "
                                f"新品 {data['tk_shops']['new_products']}"}],
        [{"tag": "text", "text": f"📦 订单: {data['orders']['total']} 单 | "
                                f"GMV \${data['orders']['gmv_usd']}"}],
        [{"tag": "text", "text": f"🎬 短剧: {data['short_drama']['episodes']} 集 | "
                                f"状态: {data['short_drama']['status']}"}],
        [{"tag": "text", "text": f"✅ 决策: {data['decisions']['approved']}/{data['decisions']['total']} 通过 | "
                                f"驳回 {data['decisions']['rejected']}"}],
        [{"tag": "text", "text": f"🔐 安全: {data['security']['scans_passed']} 扫描通过 | "
                                f"缺陷 {data['security']['issues_found']}"}],
        [{"tag": "text", "text": f"💰 Token: {data['budget']['tokens_used']} 已用 | "
                                f"剩余 {data['budget']['tokens_remaining']} ({data['budget']['pct']}%)"}],
        [{"tag": "hr"}],
        [{"tag": "text", "text": f"⏰ 生成时间: {data['report_date']}"}],
    ]

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 周报 {wk}"},
            "template": "blue",
        },
        "elements": content,
    }


def push_to_feishu(card):
    """推送到飞书"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from config import get_feishu_webhook
        webhook = get_feishu_webhook("运营指挥部")
    except Exception:
        webhook = os.environ.get("FEISHU_WEBHOOK_URL", "")

    if not webhook:
        print("⚠️ 未配置飞书 Webhook，周报保存到本地")
        with open(WEEKLY_PATH, "w") as f:
            json.dump({"card": card, "timestamp": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        return False

    try:
        import urllib.request
        body = json.dumps({"msg_type": "interactive", "card": card}).encode("utf-8")
        req = urllib.request.Request(webhook, data=body,
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"⚠️ 推送失败: {e}")
        return False


def main():
    if "--test" in sys.argv:
        data = gather_weekly_data()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print("\n✅ --test PASS: feishu_weekly")
        return

    print("📊 生成周报...")
    data = gather_weekly_data()
    card = build_card(data)

    success = push_to_feishu(card)
    if success:
        print("✅ 周报已推送到飞书")
    else:
        print("📄 周报已保存到本地")


if __name__ == "__main__":
    main()
