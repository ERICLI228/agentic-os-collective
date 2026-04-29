#!/usr/bin/env python3
"""
定价计算器 — v3.5.1 MS-2.4

公式: 售价 = (1688进价 + 头程运费) ÷ (1 - 佣金率 - 广告率 - 退货率 - 利润率)

各国参数:
  菲律宾(PHP): 佣金6% + 广告10% + 退货5% + 利润目标25%
  泰国(THB):   佣金6% + 广告10% + 退货3% + 利润目标20%
  越南(VND):   佣金6% + 广告8%  + 退货3% + 利润目标20%
  马来西亚(MYR): 佣金6% + 广告10% + 退货5% + 利润目标22%
  新加坡(SGD):  佣金6% + 广告8%  + 退货2% + 利润目标18%

用法:
  python3 shared/core/pricing_calculator.py --cost 17 --weight 0.1
"""

import json, sys
from pathlib import Path
from datetime import datetime

# 各国定价参数
PRICING_PARAMS = {
    "PH": {"commission": 0.06, "ad_rate": 0.10, "return_rate": 0.05, "profit_margin": 0.25,
           "currency": "PHP", "exchange": 7.8},     # 1 CNY ≈ 7.8 PHP
    "TH": {"commission": 0.06, "ad_rate": 0.10, "return_rate": 0.03, "profit_margin": 0.20,
           "currency": "THB", "exchange": 5.0},     # 1 CNY ≈ 5.0 THB
    "VN": {"commission": 0.06, "ad_rate": 0.08, "return_rate": 0.03, "profit_margin": 0.20,
           "currency": "VND", "exchange": 3500},    # 1 CNY ≈ 3500 VND
    "MY": {"commission": 0.06, "ad_rate": 0.10, "return_rate": 0.05, "profit_margin": 0.22,
           "currency": "MYR", "exchange": 0.64},    # 1 CNY ≈ 0.64 MYR
    "SG": {"commission": 0.06, "ad_rate": 0.08, "return_rate": 0.02, "profit_margin": 0.18,
           "currency": "SGD", "exchange": 0.19},    # 1 CNY ≈ 0.19 SGD
}

# 头程运费估算 (每kg, CNY)
SHIPPING_RATE = {
    "PH": 25,  # 菲律宾头程 ~25¥/kg
    "TH": 22,
    "VN": 18,
    "MY": 20,
    "SG": 28,
}


def calculate_price(cost_cny: float, weight_kg: float = 0.2, country: str = "PH") -> dict:
    """
    输入: 1688采购价(CNY) + 重量(kg)
    输出: 各国建议售价 + 利润表
    """
    params = PRICING_PARAMS.get(country, PRICING_PARAMS["PH"])
    shipping_cost = SHIPPING_RATE.get(country, 25) * weight_kg
    total_cost = cost_cny + shipping_cost

    denominator = 1 - params["commission"] - params["ad_rate"] - params["return_rate"] - params["profit_margin"]
    price_local = total_cost / denominator * params["exchange"]

    result = {
        "cost_cny": cost_cny,
        "weight_kg": weight_kg,
        "shipping_cny": round(shipping_cost, 2),
        "total_cost_cny": round(total_cost, 2),
        "price_local": round(price_local, 2),
        "currency": params["currency"],
        "breakdown": {
            "commission": f"{params['commission']*100:.0f}%",
            "ad_cost": f"{params['ad_rate']*100:.0f}%",
            "return_loss": f"{params['return_rate']*100:.0f}%",
            "profit_margin": f"{params['profit_margin']*100:.0f}%",
        },
        "exchange_rate": params["exchange"],
    }
    return result


def calculate_all_countries(cost_cny: float, weight_kg: float = 0.2) -> dict:
    """计算所有5国定价"""
    results = {}
    for country in PRICING_PARAMS:
        results[country] = calculate_price(cost_cny, weight_kg, country)
    return results


def main():
    cost = 17.0
    weight = 0.1
    for i, arg in enumerate(sys.argv):
        if arg == "--cost" and i + 1 < len(sys.argv):
            cost = float(sys.argv[i + 1])
        elif arg == "--weight" and i + 1 < len(sys.argv):
            weight = float(sys.argv[i + 1])

    results = calculate_all_countries(cost, weight)
    print(f"1688进价: ¥{cost} | 重量: {weight}kg\n")
    for country, r in results.items():
        symbol = {"PHP": "₱", "THB": "฿", "VND": "₫", "MYR": "RM", "SGD": "S$"}.get(r["currency"], "")
        print(f"  {country} ({r['currency']}): {symbol}{r['price_local']:.0f}  |  成本¥{r['total_cost_cny']:.2f} + 利润{r['breakdown']['profit_margin']}")


if __name__ == "__main__":
    main()
