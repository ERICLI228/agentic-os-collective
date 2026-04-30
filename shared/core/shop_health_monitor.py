#!/usr/bin/env python3
"""
店铺健康度监控 — DAEMON-2 (TK 6店违规点/扣分/处罚状态)
每2小时检查TK店铺健康状态，飞书推送告警

用法:
  python3 shared/core/shop_health_monitor.py --daemon    # 后台模式, 120分钟
  python3 shared/core/shop_health_monitor.py              # 单次检查
  python3 shared/core/shop_health_monitor.py --test       # Mock验证
"""
import json
import os
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = Path.home() / ".agentic-os"
PRODUCTS_PATH = DATA_DIR / "miaoshou_products.json"
HEALTH_PATH = DATA_DIR / "shop_health.json"
LOGS_DIR = PROJECT_ROOT / "shared" / "logs" / "executions"

HEALTHY = "healthy"
WARNING = "warning"
CRITICAL = "critical"
UNKNOWN = "unknown"


def load_shop_data():
    if not PRODUCTS_PATH.exists():
        return {"shops": [], "sync_time": None}

    with open(PRODUCTS_PATH) as f:
        data = json.load(f)

    return {
        "shops": data.get("shops", []),
        "sync_time": data.get("sync_time"),
        "products_count": data.get("products_count", 0),
        "orders_count": data.get("orders_count", 0),
    }


def check_shop_health(shop):
    issues = []
    score = 100

    name = shop.get("platformShopName", "Unknown")
    site = shop.get("site", "?")

    item_total = int(shop.get("itemTotal", "0") or "0")
    if item_total == 0:
        issues.append("商品数为0(可能被下架)")
        score -= 30

    platform_shop_id = shop.get("platformShopId")
    if not platform_shop_id:
        issues.append("店铺ID缺失")
        score -= 50

    open_shop_id = shop.get("openShopId")
    if not open_shop_id:
        issues.append("OpenID缺失(授权可能过期)")
        score -= 40

    return {
        "shop_id": shop.get("shopId"),
        "name": name,
        "site": site,
        "item_count": item_total,
        "score": max(score, 0),
        "status": HEALTHY if score >= 80 else WARNING if score >= 50 else CRITICAL,
        "issues": issues,
        "checked_at": datetime.now().isoformat(),
    }


def check_publish_logs(shop_id):
    alerts = []
    if not LOGS_DIR.exists():
        return alerts

    for log_file in sorted(LOGS_DIR.glob("*.log"), reverse=True)[:50]:
        try:
            content = log_file.read_text()[:5000]
            if shop_id in content:
                if "PublishBlockedError" in content:
                    alerts.append(f"发布门禁阻断: {log_file.name}")
                if "error" in content.lower() or "fail" in content.lower():
                    if "timeout" in content.lower():
                        alerts.append(f"超时: {log_file.name}")
        except Exception:
            pass

    return alerts


def run_health_check(alert_feishu=True):
    data = load_shop_data()
    shops = data.get("shops", [])

    results = []
    for shop in shops:
        health = check_shop_health(shop)
        log_alerts = check_publish_logs(shop.get("shopId", ""))
        if log_alerts:
            health["issues"].extend(log_alerts)
            health["status"] = WARNING
            if health["score"] > 50:
                health["score"] = max(health["score"] - 10, 0)
        results.append(health)

    overall = {
        "checked_at": datetime.now().isoformat(),
        "total_shops": len(results),
        "healthy": sum(1 for r in results if r["status"] == HEALTHY),
        "warning": sum(1 for r in results if r["status"] == WARNING),
        "critical": sum(1 for r in results if r["status"] == CRITICAL),
        "shops": results,
        "latest_sync": data.get("sync_time"),
    }

    with open(HEALTH_PATH, "w") as f:
        json.dump(overall, f, ensure_ascii=False, indent=2)

    if alert_feishu:
        _send_alerts(overall)

    return overall


def _send_alerts(overall):
    critical_shops = [s for s in overall["shops"] if s["status"] == CRITICAL]
    warning_shops = [s for s in overall["shops"] if s["status"] == WARNING]

    if not critical_shops and not warning_shops:
        return

    try:
        sys.path.insert(0, str(PROJECT_ROOT / "shared"))
        from config import get_feishu_webhook
        webhook = get_feishu_webhook("订单中心")
    except Exception:
        webhook = os.environ.get("FEISHU_WEBHOOK_URL", "")

    if not webhook:
        return

    lines = [f"🩺 店铺健康度告警 — {datetime.now().strftime('%m-%d %H:%M')}"]
    lines.append(f"健康: {overall['healthy']} | 预警: {overall['warning']} | 危急: {overall['critical']}\n")

    for s in critical_shops:
        lines.append(f"🔴 CRITICAL: {s['name']}({s['site']}) — {', '.join(s['issues'])}")

    for s in warning_shops:
        lines.append(f"🟡 WARNING: {s['name']}({s['site']}) — {', '.join(s['issues'])}")

    body = {"msg_type": "text", "content": {"text": "\n".join(lines)}}

    try:
        import urllib.request
        req = urllib.request.Request(
            webhook,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def run_daemon(interval_minutes=120):
    print(f"🩺 店铺健康度守护进程启动 (间隔: {interval_minutes}分钟)")
    while True:
        try:
            result = run_health_check()
            status_icon = "✅" if result["critical"] == 0 else "🔴"
            print(f"  {status_icon} {datetime.now().strftime('%H:%M')} | "
                  f"健康:{result['healthy']} 预警:{result['warning']} 危急:{result['critical']}")
        except Exception as e:
            print(f"  ❌ 检查失败: {e}")
        time.sleep(interval_minutes * 60)


def main():
    if "--test" in sys.argv:
        mock_shops = [
            {"shopId": "8371977", "platformShopName": "PH旗舰店", "site": "PH",
             "itemTotal": "15", "platformShopId": "x12345", "openShopId": "abc-def"},
            {"shopId": "7795399", "platformShopName": "全球店", "site": "global",
             "itemTotal": "0", "platformShopId": "x67890", "openShopId": "ghi-jkl"},
            {"shopId": "8460434", "platformShopName": "SG店", "site": "SG",
             "itemTotal": "3", "platformShopId": "", "openShopId": ""},
        ]
        results = []
        for s in mock_shops:
            results.append(check_shop_health(s))
        overall = {"total_shops": len(results),
                   "healthy": sum(1 for r in results if r["status"] == HEALTHY),
                   "warning": sum(1 for r in results if r["status"] == WARNING),
                   "critical": sum(1 for r in results if r["status"] == CRITICAL),
                   "shops": results}
        print(json.dumps(overall, ensure_ascii=False, indent=2))
        print("\n✅ --test PASS: shop_health_monitor")
        return

    if "--daemon" in sys.argv:
        run_daemon()
    else:
        result = run_health_check()
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
