#!/usr/bin/env python3
"""
物流重量体积测算器 — v3.5.1 MS-2.5

输入: 商品重量+体积 → 输出: 头程/尾程运费估算 + 物流模板

头程(中国→东南亚):
  - 燕文经济小包: ~15-30¥/kg
  - 云途专线: ~20-35¥/kg  
  - 4PX: ~18-32¥/kg

尾程(到达国国内配送):
  - TK平台物流(TikTok Shipping): 按重量阶梯计价
  - 第三方: J&T / NinjaVan / Flash Express

用法:
  python3 shared/core/logistics_calculator.py --weight 0.1 --l 10 --w 8 --h 5
"""

import sys

# 头程费率 (CNY/kg, 首重0.5kg起)
FIRST_LEG = {
    "PH": {"yawen": 28, "yuntu": 32, "4px": 30},
    "TH": {"yawen": 25, "yuntu": 28, "4px": 26},
    "VN": {"yawen": 20, "yuntu": 22, "4px": 21},
    "MY": {"yawen": 22, "yuntu": 25, "4px": 23},
    "SG": {"yawen": 30, "yuntu": 35, "4px": 32},
}

# 尾程费率 (当地货币/kg)
LAST_MILE = {
    "PH": {"tk_shipping": 55, "jnt": 45, "ninjavan": 50},    # PHP/kg
    "TH": {"tk_shipping": 35, "jnt": 30, "flash": 32},       # THB/kg
    "VN": {"tk_shipping": 18000, "jnt": 15000, "ninjavan": 16000},  # VND/kg
    "MY": {"tk_shipping": 8, "jnt": 7, "ninjavan": 7.5},     # MYR/kg
    "SG": {"tk_shipping": 2.5, "jnt": 2, "ninjavan": 2.2},   # SGD/kg
}


def calculate_volumetric_weight(l_cm: float, w_cm: float, h_cm: float) -> float:
    """体积重 = 长×宽×高 / 6000 (行业标准)"""
    return (l_cm * w_cm * h_cm) / 6000


def calculate_logistics(weight_kg: float, l_cm: float = 10, w_cm: float = 8, h_cm: float = 5):
    """计算各物流方案"""
    vol_weight = calculate_volumetric_weight(l_cm, w_cm, h_cm)
    billable_weight = max(weight_kg, vol_weight)

    print(f"实际重: {weight_kg}kg | 体积重: {vol_weight:.3f}kg | 计费重: {billable_weight:.3f}kg")
    print()
    print(f"{'国家':6s} {'头程(燕文)':>10s} {'头程(云途)':>10s} {'尾程(TK)':>10s} {'总运费':>10s}")
    print("-" * 52)

    for country in FIRST_LEG:
        fl = FIRST_LEG[country]
        ll = LAST_MILE[country]
        first_cost = fl["yawen"] * billable_weight
        last_cost = ll["tk_shipping"] * billable_weight
        total = first_cost + last_cost
        print(f"{country:6s} ¥{first_cost:8.2f} ¥{fl['yuntu']*billable_weight:8.2f} {last_cost:8.2f} ¥{total:8.2f}")


def main():
    weight = 0.1
    lcm, wcm, hcm = 10, 8, 5
    for i, arg in enumerate(sys.argv):
        if arg == "--weight" and i + 1 < len(sys.argv):
            weight = float(sys.argv[i + 1])
        elif arg == "--l" and i + 1 < len(sys.argv):
            lcm = float(sys.argv[i + 1])
        elif arg == "--w" and i + 1 < len(sys.argv):
            wcm = float(sys.argv[i + 1])
        elif arg == "--h" and i + 1 < len(sys.argv):
            hcm = float(sys.argv[i + 1])

    calculate_logistics(weight, lcm, wcm, hcm)


if __name__ == "__main__":
    main()
