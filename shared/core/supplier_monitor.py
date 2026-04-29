#!/usr/bin/env python3
"""
1688供应商监控守护进程 — v3.5.1 DAEMON-1

每小时检查1688采集商品的价格+库存变化，超阈值飞书告警。

告警触发:
  - 1688价格变动>10% → "⚠️ 供应商调价"
  - 库存跌破50 → "⚠️ 库存告急"
  - 库存归零 → "🚨 库存清空，立即下架"

用法:
  python3 shared/core/supplier_monitor.py --check           # 单次检查
  python3 shared/core/supplier_monitor.py --daemon          # 守护模式(每60分钟)
  python3 shared/core/supplier_monitor.py --alert-test      # 测试飞书告警
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
STATE_FILE = Path.home() / ".agentic-os" / "supplier_state.json"
MIAOSHOU_FILE = Path.home() / ".agentic-os" / "miaoshou_products.json"

ALERT_THRESHOLDS = {
    "price_change_pct": 10,      # 价格变动超10%告警
    "stock_low": 50,             # 库存低于50告警
    "stock_zero": True,          # 0库存告警
}


def load_current_state():
    """加载当前最新妙手数据"""
    if not MIAOSHOU_FILE.exists():
        return {}
    with open(MIAOSHOU_FILE) as f:
        data = json.load(f)
    products = data.get("products", [])
    return {str(p.get("sourceItemId", "")): p for p in products}


def load_previous_state():
    """加载上次快照"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    """保存当前快照"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def compare_states(current, previous):
    """对比两个快照，返回告警列表"""
    alerts = []

    for item_id, product in current.items():
        prev = previous.get(item_id, {})
        title = product.get("title", item_id)[:40]

        # 价格检查
        cur_price = float(product.get("price") or 0)
        prev_price = float(prev.get("price") or cur_price)
        if prev_price > 0 and cur_price != prev_price:
            change_pct = (cur_price - prev_price) / prev_price * 100
            if abs(change_pct) > ALERT_THRESHOLDS["price_change_pct"]:
                direction = "↑" if change_pct > 0 else "↓"
                alerts.append({
                    "type": "price_change",
                    "severity": "warning",
                    "title": title,
                    "message": f"{direction} {abs(change_pct):.1f}% | ¥{prev_price}→¥{cur_price}",
                })

        # 库存检查
        cur_stock = int(product.get("stock") or 0)
        prev_stock = int(prev.get("stock") or cur_stock)
        if cur_stock == 0 and ALERT_THRESHOLDS["stock_zero"]:
            alerts.append({
                "type": "stock_zero",
                "severity": "critical",
                "title": title,
                "message": f"🚨 库存归零 (曾 {prev_stock})",
            })
        elif cur_stock < ALERT_THRESHOLDS["stock_low"]:
            alerts.append({
                "type": "stock_low",
                "severity": "warning",
                "title": title,
                "message": f"⚠️ 库存仅 {cur_stock}",
            })

    return alerts


def send_feishu_alert(alerts):
    """飞书推送告警"""
    webhook = os.environ.get("FEISHU_WEBHOOK_URL", "")
    if not webhook or not alerts:
        return

    lines = [f"## 📦 供应商监控 | {datetime.now(tz).strftime('%m/%d %H:%M')}\n"]
    for a in alerts:
        lines.append(f"- {a['message']} | {a['title']}")

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": f"📦 供应商监控 ({len(alerts)}项)"}},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}}]
        }
    }

    try:
        import urllib.request
        payload = json.dumps(card).encode("utf-8")
        req = urllib.request.Request(webhook, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                print(f"✅ 飞书推送 {len(alerts)} 条告警")
            else:
                print(f"❌ 飞书推送失败: {result}")
    except Exception as e:
        print(f"❌ 飞书推送异常: {e}")


def main():
    if "--alert-test" in sys.argv:
        send_feishu_alert([{
            "type": "test", "severity": "info",
            "title": "测试告警", "message": "供应商监控系统正常"
        }])
        return

    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] 检查1688供应商数据...")

    current = load_current_state()
    if not current:
        print("  ⚠️ 妙手数据文件不存在")
        return

    previous = load_previous_state()
    alerts = compare_states(current, previous)

    if alerts:
        print(f"  🔴 {len(alerts)} 项告警:")
        for a in alerts:
            print(f"    {a['severity']:8s} {a['type']:15s} {a['message']}")
        send_feishu_alert(alerts)
    else:
        print("  ✅ 无异常")

    save_state(current)

    if "--daemon" in sys.argv:
        print(f"  守护模式: 每60分钟检查一次 (Ctrl+C 退出)")
        try:
            while True:
                time.sleep(3600)
                current = load_current_state()
                alerts = compare_states(current, previous)
                prev = load_previous_state()
                if alerts:
                    send_feishu_alert(alerts)
                save_state(current)
        except KeyboardInterrupt:
            print("\n  守护进程已停止")


if __name__ == "__main__":
    main()
