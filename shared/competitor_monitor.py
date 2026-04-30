#!/usr/bin/env python3
"""
Competitor Monitor — 竞品监控告警

从采集数据中提取竞品信息，检测价格变动、新品上架、销量异常。

输入:
  - ~/.agentic-os/miaoshou_products.json (妙手采集数据)
  - ~/.agentic-os/competitors/history.json (历史竞品快照)

输出:
  - ~/.agentic-os/competitors/alerts.json (告警列表)
  - ~/.agentic-os/competitors/history.json (更新快照)

用法:
  python3 shared/competitor_monitor.py          # 运行监控
  python3 shared/competitor_monitor.py --test    # Mock 测试
  python3 shared/competitor_monitor.py --push    # 运行 + 飞书推送
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

tz = timezone(timedelta(hours=8))
DATA_DIR = Path.home() / ".agentic-os" / "competitors"
PRODUCTS_FILE = Path.home() / ".agentic-os" / "miaoshou_products.json"
HISTORY_FILE = DATA_DIR / "history.json"
ALERTS_FILE = DATA_DIR / "alerts.json"

# 告警阈值
PRICE_DROP_PCT = 10       # 降价 ≥10% 触发告警
NEW_PRODUCT_THRESHOLD = 3 # 同竞品新增 ≥3 品触发告警
MIN_PRICE = 1.0           # 低于此价格标记异常

DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_competitor_data():
    """加载妙手采集的竞品数据"""
    if not PRODUCTS_FILE.exists():
        return []

    with open(PRODUCTS_FILE) as f:
        data = json.load(f)

    products = data.get("products", [])
    # 按店铺/品牌分组
    competitors = defaultdict(list)
    for p in products:
        key = p.get("shop_name", "unknown")
        competitors[key].append(p)

    return dict(competitors)


def load_history():
    """加载历史竞品快照"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {"snapshots": {}, "last_update": None}


def detect_alerts(current, history):
    """检测告警: 价格变动、新品、异常"""
    alerts = []
    snapshots = history.get("snapshots", {})

    for shop_name, products in current.items():
        old_products = snapshots.get(shop_name, [])
        old_ids = {p.get("product_id") for p in old_products}
        old_price_map = {p.get("product_id"): float(p.get("price", 0)) for p in old_products}

        # 1. 新品检测
        new_products = [p for p in products if p.get("product_id") not in old_ids]
        if len(new_products) >= NEW_PRODUCT_THRESHOLD:
            alerts.append({
                "type": "new_products",
                "severity": "warning",
                "shop": shop_name,
                "message": f"{shop_name} 新增 {len(new_products)} 个商品",
                "details": [p.get("title", "")[:30] for p in new_products[:5]],
                "timestamp": datetime.now(tz).isoformat()
            })

        # 2. 价格变动检测
        for p in products:
            pid = p.get("product_id")
            new_price = float(p.get("price", 0))
            old_price = old_price_map.get(pid)

            if old_price and old_price > 0 and new_price > 0:
                pct_change = (new_price - old_price) / old_price * 100
                if pct_change <= -PRICE_DROP_PCT:
                    alerts.append({
                        "type": "price_drop",
                        "severity": "high",
                        "shop": shop_name,
                        "product": p.get("title", "")[:40],
                        "message": f"{p.get('title','')[:30]} 降价 {abs(pct_change):.1f}% (${old_price:.2f}→${new_price:.2f})",
                        "timestamp": datetime.now(tz).isoformat()
                    })

        # 3. 低价异常
        low_price = [p for p in products if 0 < float(p.get("price", 0)) < MIN_PRICE]
        if low_price:
            alerts.append({
                "type": "price_anomaly",
                "severity": "info",
                "shop": shop_name,
                "message": f"{shop_name} 有 {len(low_price)} 个商品价格异常 (<${MIN_PRICE})",
                "timestamp": datetime.now(tz).isoformat()
            })

    return alerts


def save_snapshot(current):
    """保存当前竞品快照"""
    history = load_history()
    history["snapshots"] = {
        shop: [{"product_id": p.get("product_id"), "price": p.get("price"), "title": p.get("title")}
               for p in products]
        for shop, products in current.items()
    }
    history["last_update"] = datetime.now(tz).isoformat()
    history["total_competitors"] = len(current)
    history["total_products"] = sum(len(p) for p in current.values())

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return history


def save_alerts(alerts):
    """保存告警列表"""
    existing = []
    if ALERTS_FILE.exists():
        with open(ALERTS_FILE) as f:
            existing = json.load(f)

    # 保留最近 100 条
    combined = alerts + existing
    combined = combined[:100]

    with open(ALERTS_FILE, "w") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return combined


def run_monitor():
    """运行竞品监控"""
    current = load_competitor_data()
    if not current:
        print("⚠️ 无竞品数据，跳过监控")
        return {"alerts": [], "status": "no_data"}

    history = load_history()
    alerts = detect_alerts(current, history)

    save_snapshot(current)
    save_alerts(alerts)

    return {"alerts": alerts, "status": "ok", "competitors": len(current)}


def print_report(result):
    """打印监控报告"""
    print(f"\n{'='*50}")
    print(f"  🔍 竞品监控报告 | {datetime.now(tz).strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")

    if result["status"] == "no_data":
        print("  ⚠️ 无竞品数据")
        print(f"{'='*50}\n")
        return

    print(f"  📊 监控竞品: {result.get('competitors', 0)} 个店铺")

    alerts = result.get("alerts", [])
    if not alerts:
        print("  ✅ 无新告警")
    else:
        severity_order = {"high": 0, "warning": 1, "info": 2}
        alerts.sort(key=lambda a: severity_order.get(a.get("severity", "info"), 3))

        high = sum(1 for a in alerts if a.get("severity") == "high")
        warn = sum(1 for a in alerts if a.get("severity") == "warning")
        info = sum(1 for a in alerts if a.get("severity") == "info")

        print(f"  🚨 告警: {high} 高 / {warn} 中 / {info} 低")
        for a in alerts[:10]:
            icon = {"high": "🔴", "warning": "🟡", "info": "🔵"}.get(a.get("severity"), "⚪")
            print(f"    {icon} [{a['type']}] {a['message']}")

    print(f"{'='*50}\n")


# ── CLI ──

if __name__ == "__main__":
    if "--test" in sys.argv:
        print("\n🔍 Competitor Monitor Mock 测试\n")

        # Mock 数据
        mock_current = {
            "SG店": [
                {"product_id": "P1", "title": "蓝牙耳机 Pro", "price": 12.99, "shop_name": "SG店"},
                {"product_id": "P2", "title": "智能手表 X1", "price": 29.99, "shop_name": "SG店"},
                {"product_id": "P3", "title": "充电宝 20000mAh", "price": 8.99, "shop_name": "SG店"},
                {"product_id": "P4", "title": "USB-C 快充线", "price": 3.99, "shop_name": "SG店"},
            ],
            "MY店": [
                {"product_id": "M1", "title": "无线鼠标", "price": 5.99, "shop_name": "MY店"},
                {"product_id": "M2", "title": "键盘套装", "price": 15.99, "shop_name": "MY店"},
                {"product_id": "M3", "title": "手机支架", "price": 0.50, "shop_name": "MY店"},
            ]
        }

        mock_history = {
            "snapshots": {
                "SG店": [
                    {"product_id": "P1", "price": 15.99, "title": "蓝牙耳机 Pro"},
                    {"product_id": "P2", "price": 29.99, "title": "智能手表 X1"},
                ],
                "MY店": [
                    {"product_id": "M1", "price": 5.99, "title": "无线鼠标"},
                ]
            }
        }

        alerts = detect_alerts(mock_current, mock_history)
        print(f"检测到 {len(alerts)} 条告警:")
        for a in alerts:
            icon = {"high": "🔴", "warning": "🟡", "info": "🔵"}.get(a["severity"], "⚪")
            print(f"  {icon} [{a['type']}] {a['message']}")

        # 预期:
        # P1 降价 18.8% → price_drop (high)
        # SG店 新增 P3,P4 (2个 < 3) → 不触发
        # MY店 新增 M2,M3 (2个 < 3) → 不触发
        # M3 价格 0.50 < 1.0 → price_anomaly (info)

        assert any(a["type"] == "price_drop" for a in alerts), "应检测到降价"
        assert any(a["type"] == "price_anomaly" for a in alerts), "应检测到低价异常"
        print("\n✅ Mock 测试通过")

    else:
        result = run_monitor()
        print_report(result)
