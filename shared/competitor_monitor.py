"""
竞品监控 — 价格+销量采集 → competitor_report.json → 飞书告警(降价>15%)
"""
import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "reports"
REPORT_PATH = DATA_DIR / "competitor_report.json"
BASELINE_PATH = DATA_DIR / "competitor_baseline.json"


def scrape_competitors(shop_id="8371977", product_ids=None, max_retries=2):
    """
    从妙手API采集竞品价格+销量。
    无API可用时使用上次基准对比。
    """
    items = []

    if BASELINE_PATH.exists():
        with open(BASELINE_PATH) as f:
            baseline = json.load(f)
    else:
        baseline = {"items": [], "timestamp": None}

    # 尝试从API采集
    try:
        import requests
        api_url = f"http://localhost:5001/api/tasks"
        resp = requests.get(api_url, timeout=5)
        if resp.status_code == 200:
            api_data = resp.json()
    except Exception:
        baseline_only = True
    else:
        baseline_only = True

    if baseline_only:
        items = baseline.get("items", [])
        source = "baseline"
    else:
        source = "live"
        items = api_data.get("competitors", [])

    report = {
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "shop_id": shop_id,
        "items": items,
        "alerts": [],
        "summary": {"total_tracked": len(items), "price_drops": 0, "high_risk": 0}
    }

    old_map = {p["id"]: p for p in baseline.get("items", [])}

    for item in items:
        pid = item.get("id", "")
        current_price = item.get("price", 0)
        old = old_map.get(pid)
        if old and old.get("price") and current_price > 0:
            old_price = old["price"]
            drop_pct = (old_price - current_price) / old_price * 100
            if drop_pct >= 15:
                alert = {
                    "product_id": pid,
                    "product_name": item.get("title", pid),
                    "old_price": old_price,
                    "new_price": current_price,
                    "drop_pct": round(drop_pct, 1),
                    "severity": "high" if drop_pct >= 25 else "medium"
                }
                report["alerts"].append(alert)
                if drop_pct >= 25:
                    report["summary"]["high_risk"] += 1

    report["summary"]["price_drops"] = len(report["alerts"])

    # 保存基准
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    if report["alerts"]:
        _send_feishu_alert(report["alerts"])

    return report


def _send_feishu_alert(alerts):
    try:
        notifier = PROJECT_ROOT / "shared" / "feishu_decision_notifier.py"
        if notifier.exists():
            msg = f"⚠️ 竞品降价告警 — {len(alerts)} 个商品降价>15%\n"
            for a in alerts[:5]:
                msg += f"• {a['product_name']}: {a['old_price']}→{a['new_price']} (↓{a['drop_pct']}%)\n"
            if len(alerts) > 5:
                msg += f"... 共{len(alerts)}项，详见 competitor_report.json\n"
            os.system(f"python3 {notifier} '{msg}' &")
    except Exception:
        pass


def update_baseline(items):
    baseline = {
        "items": items,
        "timestamp": datetime.now().isoformat()
    }
    with open(BASELINE_PATH, "w") as f:
        json.dump(baseline, f, ensure_ascii=False, indent=2)
    return baseline


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--shop", default="8371977")
    p.add_argument("--no-alert", action="store_true")
    p.add_argument("--update-baseline", action="store_true")
    args = p.parse_args()

    if args.update_baseline:
        baseline = update_baseline([])
        print(json.dumps(baseline, ensure_ascii=False, indent=2))
        return

    report = scrape_competitors(shop_id=args.shop)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
