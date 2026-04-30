#!/usr/bin/env python3
"""
MS-0 Gate — 采集数据质量门禁

校验 ~/.agentic-os/miaoshou_products.json 的数据质量，确保下游 Pipeline 可用。

规则:
  1. 文件存在且可解析为 JSON
  2. products 字段 ≥ 10 条
  3. 每个商品必须有: product_id, title, price, shop_name
  4. 至少覆盖 2 个店铺
  5. price 字段为有效数值 (非 0, 非负)

用法:
  python3 shared/ms0_gate.py              # 运行门禁检查
  python3 shared/ms0_gate.py --test       # 用 mock 数据验证

输出:
  通过 → 返回 gate_report (pass), 写入 milestones MS-0 = approved
  失败 → 返回 gate_report (fail + 原因), 写入 milestones MS-0 = rejected
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
DATA_FILE = Path.home() / ".agentic-os" / "miaoshou_products.json"
MILESTONE_FILE = Path.home() / ".agentic-os" / "milestones.json"

# 妙手实际字段名
REQUIRED_FIELDS = ["title", "price"]  # 最小必填
OPTIONAL_ID_FIELDS = ["product_id", "sourceItemId", "commonCollectBoxDetailId"]  # ID 至少有一个
MIN_PRODUCTS = 10
MIN_SHOPS = 2


def validate_data(data):
    """校验采集数据质量，返回 (passed, errors, stats)"""
    errors = []
    stats = {}

    # 检查 products 字段
    products = data.get("products", [])
    if not isinstance(products, list):
        errors.append("products 字段不存在或不是数组")
        return False, errors, stats

    stats["total_products"] = len(products)

    if len(products) < MIN_PRODUCTS:
        errors.append(f"商品数不足: {len(products)} < {MIN_PRODUCTS}")

    # 检查必填字段 (最小: title + price)
    missing_fields = {}
    invalid_prices = 0
    shops = set()
    id_found = False

    for i, p in enumerate(products):
        if not isinstance(p, dict):
            errors.append(f"商品 #{i} 不是字典对象")
            continue

        # 检查最小必填
        for field in REQUIRED_FIELDS:
            if field not in p or not str(p[field]).strip():
                missing_fields.setdefault(field, []).append(i)

        # 检查是否有 ID 字段 (至少一个)
        for id_field in OPTIONAL_ID_FIELDS:
            if id_field in p and str(p[id_field]).strip():
                id_found = True
                break

        # 价格校验
        try:
            price = float(p.get("price", 0))
            if price <= 0:
                invalid_prices += 1
        except (ValueError, TypeError):
            invalid_prices += 1

        # 店铺来源 (优先 shop_name, 降级 source, 再降级 platformList)
        shop = p.get("shop_name", "") or p.get("source", "") or str(p.get("platformList", ""))
        shop = shop.strip()
        if shop and shop not in ("None", "[]", ""):
            shops.add(shop)

    stats["shops"] = list(shops)
    stats["shop_count"] = len(shops)
    stats["invalid_prices"] = invalid_prices

    if missing_fields:
        for field, indices in missing_fields.items():
            errors.append(f"字段 '{field}' 缺失于 {len(indices)} 个商品")

    if invalid_prices > 0:
        errors.append(f"{invalid_prices} 个商品价格无效 (≤0 或非法格式)")

    if not id_found:
        errors.append("所有商品均无有效 ID 字段")

    if len(shops) < MIN_SHOPS and not id_found:
        errors.append(f"店铺覆盖不足: {len(shops)} < {MIN_SHOPS} 且无 ID 字段")

    # 检查 shops/orders 字段 (可选但加分)
    if "shops" in data:
        stats["shop_records"] = len(data["shops"])
    if "orders" in data:
        stats["order_records"] = len(data["orders"])

    passed = len(errors) == 0
    return passed, errors, stats


def run_gate(data_path=None):
    """运行 MS-0 门禁"""
    path = Path(data_path) if data_path else DATA_FILE
    report = {
        "gate": "MS-0",
        "timestamp": datetime.now(tz).isoformat(),
        "data_file": str(path),
    }

    # 文件存在性
    if not path.exists():
        report["status"] = "fail"
        report["errors"] = [f"数据文件不存在: {path}"]
        _update_milestone("rejected", report)
        return report

    # JSON 解析
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        report["status"] = "fail"
        report["errors"] = [f"JSON 解析失败: {e}"]
        _update_milestone("rejected", report)
        return report

    # 质量校验
    passed, errors, stats = validate_data(data)

    report["stats"] = stats
    report["status"] = "pass" if passed else "fail"
    if errors:
        report["errors"] = errors

    status = "approved" if passed else "rejected"
    _update_milestone(status, report)
    return report


def _update_milestone(status, report):
    """更新 MS-0 里程碑状态"""
    if not MILESTONE_FILE.exists():
        return

    with open(MILESTONE_FILE) as f:
        ms_data = json.load(f)

    ms_data["milestones"]["MS-0"] = {
        "id": "MS-0",
        "name": "采集门禁",
        "status": status,
        "decision_point": True,
        "decision": "auto_gate",
        "decision_at": datetime.now(tz).isoformat(),
        "decision_by": "ms0_gate",
        "decision_reason": json.dumps(report, ensure_ascii=False),
        "updated_at": datetime.now(tz).isoformat(),
        "log": [f"{datetime.now(tz).isoformat()} MS-0 门禁: {status}"]
    }
    ms_data["updated_at"] = datetime.now(tz).isoformat()

    with open(MILESTONE_FILE, "w") as f:
        json.dump(ms_data, f, ensure_ascii=False, indent=2)


# ── CLI ──

if __name__ == "__main__":
    if "--test" in sys.argv:
        print("\n🔍 MS-0 Gate Mock 测试\n")

        # Mock 通过
        mock_pass = {
            "products": [
                {"product_id": f"P{i}", "title": f"测试商品 {i}", "price": 9.9 + i, "shop_name": ["SG店", "MY店"][i % 2]}
                for i in range(20)
            ],
            "shops": [{"name": "SG店"}, {"name": "MY店"}],
            "orders": [{"order_id": "O1"}]
        }
        passed, errors, stats = validate_data(mock_pass)
        print(f"Mock 通过: {'✅' if passed else '❌'}")
        print(f"  商品数: {stats.get('total_products')}, 店铺: {stats.get('shop_count')}")

        # Mock 失败 (商品数不足)
        mock_fail = {
            "products": [
                {"product_id": "P1", "title": "测试", "price": 5.0, "shop_name": "SG店"}
            ]
        }
        passed, errors, stats = validate_data(mock_fail)
        print(f"Mock 失败: {'❌' if not passed and errors else '⚠️ 误判'}")
        print(f"  错误: {errors}")

        # Mock 失败 (缺字段)
        mock_missing = {
            "products": [
                {"product_id": "P1", "price": 5.0}
                for _ in range(15)
            ]
        }
        passed, errors, stats = validate_data(mock_missing)
        print(f"Mock 缺字段: {'❌' if not passed and errors else '⚠️ 误判'}")
        print(f"  错误: {errors}")

        print("\n✅ MS-0 Gate Mock 测试完成")

    else:
        report = run_gate()
        icon = "✅" if report["status"] == "pass" else "❌"
        print(f"\n{'='*50}")
        print(f"  {icon} MS-0 采集门禁: {report['status'].upper()}")
        print(f"  📄 数据文件: {report.get('data_file', 'N/A')}")
        if "stats" in report:
            s = report["stats"]
            print(f"  📊 商品: {s.get('total_products', 0)} | 店铺: {s.get('shop_count', 0)} | 无效价格: {s.get('invalid_prices', 0)}")
        if "errors" in report:
            for e in report["errors"]:
                print(f"  ⚠️ {e}")
        print(f"{'='*50}\n")
