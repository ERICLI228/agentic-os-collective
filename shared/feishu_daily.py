#!/usr/bin/env python3
"""
TK 运营日报 — v3.5 Sprint 1.2

基于 Sprint 0 构建的感知层(status API + Miaoshou数据)，生成日报并推送到飞书。

数据来源（按优先级）:
  1. http://localhost:5001/api/status    → 任务状态、决策待办
  2. ~/.agentic-os/miaoshou_products.json → 采集箱商品数、店铺状态
  3. fallback: Mock 降级数据

用法:
  python3 shared/feishu_daily.py               # 生成 + 推送
  python3 shared/feishu_daily.py --dry-run     # 仅打印 JSON，不推送
  python3 shared/feishu_daily.py --test        # 用 Mock 数据
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

def load_env():
    """从 .env 读取环境变量"""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k not in os.environ:
                    os.environ[k] = v.strip().strip('"').strip("'")

def fetch_status():
    """从 Flask status API 获取任务状态"""
    try:
        import urllib.request
        req = urllib.request.Request(STATUS_API)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None

def read_miaoshou():
    """读取本地妙手数据"""
    if MIAOSHOU_FILE.exists():
        with open(MIAOSHOU_FILE) as f:
            return json.load(f)
    return None

def build_card(status, miaoshou):
    """构建飞书日报卡片"""
    now = datetime.now(tz).isoformat()

    if status:
        task_count = status.get("total", 0)
        completed = status.get("completed", 0)
        decision_pending = status.get("decision_pending", 0)
        system_health = status.get("system_health", "unknown")
    else:
        task_count = 0
        completed = 0
        decision_pending = 0
        system_health = "offline"

    if miaoshou:
        shop_count = miaoshou.get("shops_count", len(miaoshou.get("shops", [])))
        product_count = miaoshou.get("products_count", len(miaoshou.get("products", [])))
        order_count = miaoshou.get("orders_count", len(miaoshou.get("orders", [])))
    else:
        shop_count = "?"
        product_count = "?"
        order_count = "?"

    decision_alert = ""
    if decision_pending == 1:
        decision_alert = f"\n⚠️ **1 项待决策**"
    elif decision_pending > 1:
        decision_alert = f"\n🔴 **{decision_pending} 项待决策**"

    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 TK运营日报 | {datetime.now(tz).strftime('%m/%d %H:%M')}"},
            "template": "indigo"
        },
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**系统**: {system_health} | **任务**: {task_count} 进行中/已完成 {completed}{decision_alert}"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"🏪 **店铺**: {shop_count} (全授权) | 📦 **采集箱**: {product_count} 商品 | 📋 **订单**: {order_count}"}},
        ]
    }

    return card

def send_to_feishu(card_json):
    """通过 webhook 推送到飞书"""
    webhook = os.environ.get("FEISHU_WEBHOOK_URL", "")
    if not webhook:
        print("❌ FEISHU_WEBHOOK_URL 未配置", file=sys.stderr)
        return False

    try:
        import urllib.request
        payload = json.dumps({"msg_type": "interactive", "card": card_json}).encode("utf-8")
        req = urllib.request.Request(webhook, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                print("✅ 飞书推送成功")
                return True
            else:
                print(f"❌ 飞书推送失败: {result}", file=sys.stderr)
                return False
    except Exception as e:
        print(f"❌ 飞书推送异常: {e}", file=sys.stderr)
        return False

def main():
    load_env()

    if "--test" in sys.argv:
        print("🧪 Mock 模式")
        status = None
        miaoshou = None
    else:
        status = fetch_status()
        miaoshou = read_miaoshou()

    card = build_card(status, miaoshou)

    if "--dry-run" in sys.argv:
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return

    send_to_feishu(card)

if __name__ == "__main__":
    main()
