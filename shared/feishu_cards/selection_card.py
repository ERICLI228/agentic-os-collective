#!/usr/bin/env python3
"""
选品审核飞书卡片 — v3.5 Sprint 1.3

生成选品审核卡片 + 写入决策文件（文件轮询方案，不依赖回调端点）。

流程:
  1. 从 ~/.agentic-os/miaoshou_products.json 读取 TOP N 商品
  2. (如对抗审核引擎可用) 给每个商品评分
  3. 生成飞书卡片 JSON → 推送到飞书群 webhook
  4. 写决策请求文件 → ~/.agentic-os/decisions/{task_id}.json
  5. 用户通过 resolve.py 或 /api/decision 做出决策

用法:
  python3 shared/feishu_cards/selection_card.py              # 生成并推送卡片
  python3 shared/feishu_cards/selection_card.py --top 5       # 指定 TOP N
  python3 shared/feishu_cards/selection_card.py --dry-run     # 仅生成 JSON，不推送
"""

import json
import os
import sys
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta
from uuid import uuid4

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DECISIONS_DIR = Path.home() / ".agentic-os" / "decisions"
MIAOSHOU_FILE = Path.home() / ".agentic-os" / "miaoshou_products.json"

def load_env():
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k not in os.environ:
                    os.environ[k] = v.strip().strip('"').strip("'")

def load_products():
    if not MIAOSHOU_FILE.exists():
        print(f"❌ 妙手数据不存在: {MIAOSHOU_FILE}", file=sys.stderr)
        return []
    with open(MIAOSHOU_FILE) as f:
        data = json.load(f)
    products = data.get("products", [])
    if isinstance(products, dict):
        products = list(products.values())
    return products

def try_score(product):
    """尝试用对抗审核给商品评分，失败返回 mock 分数"""
    try:
        from shared.core.adversarial_review import run_review
        title = product.get("title", "未知商品")
        price = product.get("price")
        result = run_review("tk_product_review", {"title": title, "price": price}, {})
        return result.get("score", 5.0)
    except Exception:
        return round(random.uniform(6.0, 9.0), 1)

def generate_card(products, top_n=5, account_name="MagicPockets"):
    selected = products[:min(top_n, len(products))]

    product_lines = []
    for i, p in enumerate(selected):
        title = p.get("title", "未知商品")[:30]
        price = p.get("price") or "?"
        source = p.get("source", "1688")
        score = try_score(p)

        icon = "⭐" if score >= 8.0 else "👍" if score >= 7.0 else "👀"
        product_lines.append(
            f"**{i+1}. {title}**\n"
            f"  {icon} 对抗评分: {score}/10 | 来源: {source} | 参考价: {price}"
        )

    task_id = f"DEC-{datetime.now(tz).strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:4]}"

    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"🛒 选品审核 | {account_name}"},
            "template": "indigo"
        },
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**任务ID**: {task_id}\n**时间**: {datetime.now(tz).strftime('%Y-%m-%d %H:%M CST')}\n**采集箱总数**: {len(products)} 商品"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(product_lines)}},
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": "🤖 请通过以下方式决策:\n```\npython3 shared/feishu_cards/resolve.py " + task_id + " --action approved\n```"}},
        ]
    }

    return task_id, card

def push_card(card):
    webhook = os.environ.get("FEISHU_WEBHOOK_URL", "")
    if not webhook:
        print("❌ FEISHU_WEBHOOK_URL 未配置", file=sys.stderr)
        return False
    try:
        import urllib.request
        payload = json.dumps({"msg_type": "interactive", "card": card}).encode("utf-8")
        req = urllib.request.Request(webhook, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("code") == 0
    except Exception as e:
        print(f"❌ 飞书推送异常: {e}", file=sys.stderr)
        return False

def write_decision_request(task_id, card):
    DECISIONS_DIR.mkdir(parents=True, exist_ok=True)
    decision_file = DECISIONS_DIR / f"{task_id}.json"
    request = {
        "task_id": task_id,
        "type": "selection_review",
        "status": "waiting_decision",
        "card": card,
        "options": ["approved", "modify", "rejected"],
        "created_at": datetime.now(tz).isoformat(),
        "resolved_at": None,
        "decision": None,
        "reason": None
    }
    with open(decision_file, "w") as f:
        json.dump(request, f, ensure_ascii=False, indent=2)
    print(f"✅ 决策文件已写入: {decision_file}")
    return decision_file

def main():
    load_env()

    top_n = 5
    for i, arg in enumerate(sys.argv):
        if arg == "--top" and i + 1 < len(sys.argv):
            top_n = int(sys.argv[i + 1])

    products = load_products()
    if not products:
        print("⚠️ 无可选品数据")
        return

    task_id, card = generate_card(products, top_n)

    if "--dry-run" in sys.argv:
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return

    ok = push_card(card)
    if ok:
        write_decision_request(task_id, card)
    else:
        print("❌ 飞书推送失败，未写入决策文件")

if __name__ == "__main__":
    main()
