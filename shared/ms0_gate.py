"""
MS-0 采集数据门禁
校验采集箱数据质量 → 未通过则飞书告警 + 暂停Pipeline
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "reports"


def load_collect_box():
    box_path = DATA_DIR / "collect_box.json"
    if not box_path.exists():
        return {"status": "error", "reason": "collect_box.json 不存在", "items": []}
    with open(box_path) as f:
        return json.load(f)


def validate_item(item):
    errors = []
    if not item.get("title", "").strip():
        errors.append("title为空")
    price = item.get("price")
    if price is None:
        errors.append("price缺失")
    elif not isinstance(price, (int, float)) or price <= 0:
        errors.append(f"price无效({price})")
    sku = item.get("sku", "").strip()
    if not sku:
        errors.append("SKU为空")
    cats = item.get("categories")
    if not cats or (isinstance(cats, list) and len(cats) == 0):
        errors.append("分类缺失")
    return errors


def run_gate(alert_feishu=True):
    data = load_collect_box()
    if data["status"] == "error":
        result = {"passed": False, "gate": "MS-0", "reason": data["reason"],
                  "total": 0, "passed_count": 0, "failed_count": 0,
                  "failures": [], "timestamp": datetime.now().isoformat()}
        if alert_feishu:
            _alert_feishu(result)
        return result

    items = data.get("items", [])
    failures = []
    for item in items:
        errs = validate_item(item)
        if errs:
            failures.append({"id": item.get("id", "?"), "title": item.get("title", "?"), "errors": errs})

    passed_count = len(items) - len(failures)
    total = len(items)
    ok = len(failures) == 0 and total > 0

    result = {
        "passed": ok,
        "gate": "MS-0",
        "total": total,
        "passed_count": passed_count,
        "failed_count": len(failures),
        "failures": failures,
        "timestamp": datetime.now().isoformat()
    }

    if not ok:
        result["reason"] = f"{len(failures)}/{total} 商品未通过质量校验"
        if alert_feishu:
            _alert_feishu(result)

    return result


def _alert_feishu(result):
    try:
        notifier = PROJECT_ROOT / "shared" / "feishu_decision_notifier.py"
        if notifier.exists():
            msg = f"🛑 MS-0 门禁告警\n{result['failed_count']}/{result['total']} 商品数据不合格\n"
            for f in result.get("failures", [])[:5]:
                msg += f"• {f['title']}: {', '.join(f['errors'])}\n"
            os.system(f"python3 {notifier} '{msg}' &")
    except Exception:
        pass


def main():
    alert = "--no-alert" not in sys.argv
    result = run_gate(alert_feishu=alert)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
