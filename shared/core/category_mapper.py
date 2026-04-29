#!/usr/bin/env python3
"""
类目映射 + 属性填充器 — v3.5.1 MS-2.2

1688商品信息 → TK类目树映射 + 必填属性自动填充

TK 3C品类常见类目树(东南亚):
  - Electronics > Audio > Headphones & Earphones
  - Electronics > Chargers & Cables > USB Cables
  - Electronics > Power Banks
  - Home & Living > Lighting > Night Lights
  - Electronics > Computer Accessories > USB Hubs

必填属性(按类目):
  - 电池产品: Battery In Product, Battery Quantity, Battery Capacity(mAh)
  - 电子: Volts/Watts/Hertz, Input Voltage, Plug Type
  - 所有: Brand, Product Condition, Warranty Type

用法:
  python3 shared/core/category_mapper.py --input miaoshou_products.json
"""

import json, sys
from pathlib import Path

# 1688→TK类目映射 (基于关键词)
CATEGORY_MAP = {
    "灯": {
        "tk_path": "Home & Living > Lighting > Night Lights & Ambient Lighting",
        "tk_id": "500258",
        "attributes": {
            "battery_in_product": "Yes",
            "battery_quantity": "1",
            "power_consumption": "5W",
            "input_voltage": "5V",
            "with_magnet": "No",
            "warranty_type": "1 Year",
            "product_condition": "100% Brand New",
        }
    },
    "充电宝|移动电源": {
        "tk_path": "Electronics > Chargers & Power Accessories > Power Banks",
        "tk_id": "500612",
        "attributes": {
            "battery_in_product": "Yes",
            "battery_capacity": "10000mAh",
            "input_voltage": "5V",
            "power_plug_type": "USB Type-C",
            "warranty_type": "1 Year",
            "product_condition": "100% Brand New",
        }
    },
    "扩展坞|拓展坞|hub": {
        "tk_path": "Electronics > Computer Accessories > USB Hubs & Docking Stations",
        "tk_id": "500238",
        "attributes": {
            "input_connectivity": "USB Type-C",
            "warranty_type": "1 Year",
            "product_condition": "100% Brand New",
        }
    },
    "投屏|同屏|hdmi": {
        "tk_path": "Electronics > Video Accessories > Screen Mirroring & Streaming Devices",
        "tk_id": "500623",
        "attributes": {
            "input_connectivity": "HDMI, USB",
            "resolution": "1080P HD",
            "warranty_type": "1 Year",
            "product_condition": "100% Brand New",
        }
    },
    "充电器|充电头": {
        "tk_path": "Electronics > Chargers & Power Accessories > Wall Chargers",
        "tk_id": "500611",
        "attributes": {
            "input_voltage": "100-240V",
            "power_plug_type": "USB-A, USB Type-C",
            "power_consumption": "20W",
            "warranty_type": "1 Year",
            "product_condition": "100% Brand New",
        }
    },
    "数据线|充电线|cable": {
        "tk_path": "Electronics > Chargers & Power Accessories > Charging Cables",
        "tk_id": "500613",
        "attributes": {
            "warranty_type": "1 Year",
            "product_condition": "100% Brand New",
        }
    },
}

DEFAULT_3C_ATTRIBUTES = {
    "product_condition": "100% Brand New",
    "warranty_type": "1 Year Manufacturer Warranty",
    "brand": "MagicPockets",
}


def map_category(product_title: str) -> dict:
    """根据产品标题关键词匹配TK类目"""
    title = product_title.lower()
    for keywords, cat in CATEGORY_MAP.items():
        for kw in keywords.split("|"):
            if kw in title:
                return cat.copy()
    # 默认 3C
    return {
        "tk_path": "Electronics > Other Electronics",
        "tk_id": "500200",
        "attributes": DEFAULT_3C_ATTRIBUTES.copy()
    }


def fill_attributes(category: dict) -> dict:
    """填充TK必填属性(合并默认值)"""
    attrs = DEFAULT_3C_ATTRIBUTES.copy()
    attrs.update(category.get("attributes", {}))
    return attrs


def main():
    miaoshou = None
    for i, arg in enumerate(sys.argv):
        if arg == "--input" and i + 1 < len(sys.argv):
            miaoshou = Path(sys.argv[i + 1])

    if miaoshou and miaoshou.exists():
        with open(miaoshou) as f:
            products = json.load(f).get("products", [])[:5]
        for p in products:
            title = p.get("title", "")
            cat = map_category(title)
            attrs = fill_attributes(cat)
            print(f'{title[:50]:50s} → {cat["tk_path"][:40]:40s} ({len(attrs)} attrs)')
    else:
        print("用法: python3 shared/core/category_mapper.py --input miaoshou_products.json")
        print()
        for cat_name, cat_info in CATEGORY_MAP.items():
            print(f"  {cat_name:20s} → {cat_info['tk_path']}")


if __name__ == "__main__":
    main()
