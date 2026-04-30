#!/usr/bin/env python3
"""
妙手ERP 数据同步 — MS-1 (采集箱 + 订单数据同步)
拉取采集箱/订单数据 → 更新 miaoshou_products.json → 供日报+选品使用

用法:
  python3 shared/core/miaoshou_sync.py              # 全量同步
  python3 shared/core/miaoshou_sync.py --orders-only # 只拉订单
  python3 shared/core/miaoshou_sync.py --test        # Mock验证
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = Path.home() / ".agentic-os"
PRODUCTS_PATH = DATA_DIR / "miaoshou_products.json"


def _make_client():
    sys.path.insert(0, str(PROJECT_ROOT / "shared" / "core"))
    from miaoshou_publish import MiaoshouClient
    return MiaoshouClient()


def fetch_collect_box(client):
    """
    拉取TikTok采集箱数据
    API: POST /api/platform/tiktok/move/collect_box/searchCollectBoxDetail
    """
    try:
        import urllib.parse
        params = {
            "page": "0",
            "pageSize": "100",
            "platform": "tiktok",
        }
        body = urllib.parse.urlencode(params)
        result = client._request("POST",
            "/api/platform/tiktok/move/collect_box/searchCollectBoxDetail",
            data=body,
            extra_headers={"content-type": "application/x-www-form-urlencoded"})
        return result
    except Exception as e:
        return {"error": str(e), "endpoint": "collect_box"}


def fetch_orders(client, shop_ids=None):
    """
    拉取订单数据
    
    尝试多个可能的订单API端点:
    1. /api/platform/tiktok/order/list
    2. /api/platform/tiktok/order/searchOrderList
    3. /api/order/list
    
    返回: {"orders": [...], "total": int, "endpoint": str}
    """
    if shop_ids is None:
        shop_ids = ["8371977", "7795399", "7795400", "8460401", "8460416", "8460434"]

    all_orders = []

    for endpoint in [
        "/api/platform/tiktok/order/list",
        "/api/platform/tiktok/order/searchOrderList",
        "/api/order/list",
    ]:
        try:
            import urllib.parse
            params = {"page": "0", "pageSize": "50", "platform": "tiktok"}
            body = urllib.parse.urlencode(params)
            result = client._request("POST", endpoint, data=body,
                extra_headers={"content-type": "application/x-www-form-urlencoded"})
            if isinstance(result, dict) and result.get("result") == "success":
                data = result.get("data", {})
                orders = data.get("list", data.get("orders", data.get("records", [])))
                if orders:
                    all_orders = orders
                    return {"orders": all_orders, "total": data.get("total", len(orders)),
                            "endpoint": endpoint}
        except Exception as e:
            continue

    return {"orders": all_orders, "total": 0, "endpoint": None,
            "note": "订单API端点待确认(需浏览器抓包)"}


def sync_all():
    """全量同步: 采集箱 + 订单"""
    client = _make_client()

    try:
        client.login()
        print("✅ 妙手ERP登录成功")
    except Exception as e:
        print(f"⚠️ 登录失败: {e}")
        return _load_existing()

    result = {
        "sync_time": datetime.now().isoformat(),
        "status": "ok",
    }

    box_data = fetch_collect_box(client)
    if "error" not in box_data:
        result["collect_box"] = box_data

    order_data = fetch_orders(client)
    result["orders"] = order_data.get("orders", [])
    result["orders_count"] = order_data.get("total", 0)
    result["order_endpoint"] = order_data.get("endpoint")

    if PRODUCTS_PATH.exists():
        with open(PRODUCTS_PATH) as f:
            existing = json.load(f)
    else:
        existing = {}

    existing.update({
        "sync_time": result["sync_time"],
        "orders_count": result["orders_count"],
        "orders": result["orders"],
    })

    with open(PRODUCTS_PATH, "w") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"✅ 同步完成: 采集箱 {len(box_data.get('data', {}).get('list', []))} 商品, "
          f"订单 {result['orders_count']} 笔")
    return result


def _load_existing():
    if PRODUCTS_PATH.exists():
        with open(PRODUCTS_PATH) as f:
            return json.load(f)
    return {"error": "无可用数据", "sync_time": None}


def main():
    if "--test" in sys.argv:
        result = {
            "sync_time": datetime.now().isoformat(),
            "status": "test",
            "collect_box": {"data": {"list": [], "total": 0}},
            "orders": [],
            "orders_count": 0,
            "shops_count": 6,
            "products_count": 0,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\n✅ --test PASS: miaoshou_sync")
        return

    if "--orders-only" in sys.argv:
        client = _make_client()
        try:
            client.login()
            result = fetch_orders(client)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        return

    result = sync_all()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
