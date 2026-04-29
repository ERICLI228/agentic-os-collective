#!/usr/bin/env python3
"""
早期爆款预测器 — v3.5 Sprint 4.1 (FR-TK-015)

综合信号:
  1. 1688供应链趋势 (价格变动/上新频率/供应商响应)
  2. TK市场数据 (tk_ad_review转化评分/历史订单)
  3. 季节性和竞争密度

输入:
  - miaoshou_products.json (采集箱)
  - localized_product.json (本地化listing)
  - tk_ad_review 评分

输出:
  - TOP10 爆款预测排行 (trend_predictions.json)

用法:
  python3 shared/core/trend_predictor.py --input miaoshou_products.json --top 10
  python3 shared/core/trend_predictor.py --test
"""

import json, sys, random
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional

OUTPUT_DIR = Path.home() / ".agentic-os" / "predictions"
DATA_PATH = Path.home() / ".agentic-os" / "miaoshou_products.json"


# ── 品类季节权重 ──
SEASONAL_WEIGHTS = {
    "phone_case": {"Q1": 0.8, "Q2": 0.9, "Q3": 1.0, "Q4": 1.2},
    "charger": {"Q1": 0.7, "Q2": 0.8, "Q3": 0.8, "Q4": 1.3},  # 旺季在年底
    "cable": {"Q1": 0.9, "Q2": 0.9, "Q3": 1.0, "Q4": 1.1},
    "power_bank": {"Q1": 1.0, "Q2": 1.1, "Q3": 1.2, "Q4": 0.8},
    "earphone": {"Q1": 0.9, "Q2": 1.0, "Q3": 1.1, "Q4": 1.3},
    "hub": {"Q1": 1.2, "Q2": 0.9, "Q3": 0.8, "Q4": 1.0},  # 开学季
    "lamp": {"Q1": 0.7, "Q2": 0.8, "Q3": 0.9, "Q4": 1.4},  # 年底节日
    "speaker": {"Q1": 0.8, "Q2": 1.2, "Q3": 1.3, "Q4": 1.0},
}

# ── 1688品类关键词映射 ──
CATEGORY_KEYWORDS = {
    "phone_case": ["手机壳", "phone case", "手机套"],
    "charger": ["充电器", "charger", "快充"],
    "cable": ["数据线", "cable", "充电线"],
    "power_bank": ["充电宝", "power bank", "移动电源"],
    "earphone": ["耳机", "earphone", "earbuds"],
    "hub": ["扩展坞", "hub", "转换器"],
    "lamp": ["灯", "lamp", "led"],
    "speaker": ["音箱", "speaker", "蓝牙音箱"],
}


@dataclass
class TrendPrediction:
    """单品预测结果"""
    rank: int
    product_id: str
    title: str
    category: str
    trend_score: float          # 0-100 爆款潜力分
    signals: Dict               # 各维度得分
    recommendation: str         # "立即上架" / "观察" / "暂缓"
    reasoning: str


def detect_category(title: str) -> str:
    """根据标题检测品类"""
    title_lower = title.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            return cat
    return "other"


def calculate_supply_signal(product: dict) -> dict:
    """供应链趋势信号"""
    price = product.get("price", 0) or 0
    min_order = product.get("min_order", 1)
    supplier_days = product.get("supplier_response_days", 3)

    # 低价 + 低起订 = 更容易起量
    price_score = max(0, 100 - price * 5)
    moq_score = max(0, 100 - min_order * 2)
    response_score = max(0, 100 - supplier_days * 15)

    return {
        "price_competitiveness": round(price_score, 1),
        "moq_flexibility": round(moq_score, 1),
        "supplier_responsiveness": round(response_score, 1),
    }


def calculate_market_signal(product: dict) -> dict:
    """市场热度信号"""
    sales = product.get("monthly_sales", 0)
    reviews = product.get("review_count", 0)
    rating = product.get("rating", 4.0)

    # 销量增长信号
    sales_score = min(100, sales / 10)
    # 评论活跃度
    review_score = min(100, reviews / 5)
    # 好评率
    rating_score = rating * 10

    return {
        "sales_volume": round(sales_score, 1),
        "review_activity": round(review_score, 1),
        "rating_quality": round(rating_score, 1),
    }


def calculate_competition_signal(category: str, product: dict) -> dict:
    """竞争密度信号"""
    competitor_count = product.get("competitor_count", 50)

    # 竞争越少越容易突围
    density_score = max(0, 100 - competitor_count * 0.5)

    # 差异化空间（基于title长度，越短越需要差异化）
    title_len = len(product.get("title", ""))
    diff_score = min(100, title_len * 2)

    return {
        "competition_density": round(density_score, 1),
        "differentiation_space": round(diff_score, 1),
    }


def predict_trend(products: List[dict], top_n: int = 10) -> List[TrendPrediction]:
    """
    预测爆款趋势

    Args:
        products: 商品列表 (来自 miaoshou_products.json)
        top_n: 返回前N名

    Returns:
        TrendPrediction 列表 (按 trend_score 降序)
    """
    predictions = []

    for p in products:
        category = detect_category(p.get("title", ""))
        seasonal = SEASONAL_WEIGHTS.get(category, {}).get(get_seasonal_quarter(), 1.0)

        supply = calculate_supply_signal(p)
        market = calculate_market_signal(p)
        competition = calculate_competition_signal(category, p)

        # 综合评分 (权重可调整)
        weights = {
            "supply": 0.25,
            "market": 0.35,
            "competition": 0.25,
            "seasonal": 0.15,
        }

        supply_avg = sum(supply.values()) / len(supply) if supply else 50
        market_avg = sum(market.values()) / len(market) if market else 50
        comp_avg = sum(competition.values()) / len(competition) if competition else 50

        trend_score = (
            supply_avg * weights["supply"] +
            market_avg * weights["market"] +
            comp_avg * weights["competition"] +
            seasonal * 100 * weights["seasonal"]
        )
        trend_score = min(100, max(0, trend_score))

        # 推荐
        if trend_score >= 75:
            rec = "立即上架"
        elif trend_score >= 60:
            rec = "观察"
        else:
            rec = "暂缓"

        reasoning = (
            f"供应链{supply_avg:.0f}分 + 市场{market_avg:.0f}分 + 竞争{comp_avg:.0f}分, "
            f"季节系数{seasonal:.1f}"
        )

        predictions.append(TrendPrediction(
            rank=0,
            product_id=p.get("id", p.get("product_id", "")),
            title=p.get("title", "Unknown"),
            category=category,
            trend_score=round(trend_score, 1),
            signals={**supply, **market, **competition},
            recommendation=rec,
            reasoning=reasoning,
        ))

    # 排序
    predictions.sort(key=lambda x: x.trend_score, reverse=True)
    for i, pred in enumerate(predictions):
        pred.rank = i + 1

    return predictions[:top_n]


def get_seasonal_quarter() -> str:
    """获取当前季度"""
    month = datetime.now().month
    return f"Q{(month - 1) // 3 + 1}"


def save_predictions(predictions: List[TrendPrediction]) -> Path:
    """保存预测结果"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"trend_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    data = {
        "generated_at": datetime.now().isoformat(),
        "quarter": get_seasonal_quarter(),
        "total_products": len(predictions),
        "predictions": [asdict(p) for p in predictions],
    }
    with open(output_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_file


def main():
    if "--test" in sys.argv:
        print("=" * 60)
        print("  早期爆款预测器 — Mock 测试")
        print("=" * 60)

        mock_products = [
            {"id": "P001", "title": "透明手机壳 防摔 iPhone 15 Pro", "price": 3.5, "min_order": 10,
             "monthly_sales": 500, "review_count": 120, "rating": 4.8, "competitor_count": 80,
             "supplier_response_days": 1},
            {"id": "P002", "title": "65W GaN 快充充电器 USB-C PD", "price": 12.0, "min_order": 50,
             "monthly_sales": 300, "review_count": 85, "rating": 4.6, "competitor_count": 45,
             "supplier_response_days": 2},
            {"id": "P003", "title": "磁吸充电宝 10000mAh 无线充电", "price": 8.5, "min_order": 20,
             "monthly_sales": 800, "review_count": 200, "rating": 4.9, "competitor_count": 30,
             "supplier_response_days": 1},
            {"id": "P004", "title": "蓝牙5.3 降噪耳机 TWS", "price": 15.0, "min_order": 100,
             "monthly_sales": 150, "review_count": 40, "rating": 4.2, "competitor_count": 120,
             "supplier_response_days": 3},
            {"id": "P005", "title": "Type-C 扩展坞 7合1 HDMI", "price": 10.0, "min_order": 30,
             "monthly_sales": 200, "review_count": 60, "rating": 4.5, "competitor_count": 55,
             "supplier_response_days": 2},
        ]

        preds = predict_trend(mock_products, top_n=5)
        print(f"\n📊 TOP {len(preds)} 爆款预测:\n")
        for p in preds:
            icon = {"立即上架": "🔥", "观察": "👁️", "暂缓": "⏸️"}[p.recommendation]
            print(f"  #{p.rank} {icon} {p.trend_score}分 | {p.title[:40]}")
            print(f"     品类: {p.category} | 推荐: {p.recommendation}")
            print(f"     信号: {p.reasoning}")
            print()

        output_file = save_predictions(preds)
        print(f"✅ 预测结果: {output_file}")
        return

    # 正常模式
    data_path = DATA_PATH
    top_n = 10
    for i, arg in enumerate(sys.argv):
        if arg == "--input" and i + 1 < len(sys.argv):
            data_path = Path(sys.argv[i + 1])
        elif arg == "--top" and i + 1 < len(sys.argv):
            top_n = int(sys.argv[i + 1])

    if not data_path.exists():
        print(f"⚠️ 数据文件不存在: {data_path}")
        print("使用 --test 运行 Mock 测试")
        sys.exit(1)

    with open(data_path) as f:
        raw = json.load(f)

    products = raw.get("products", raw) if isinstance(raw, dict) else raw
    preds = predict_trend(products, top_n=top_n)

    output_file = save_predictions(preds)
    print(f"✅ {len(preds)} predictions → {output_file}")
    for p in preds[:5]:
        icon = {"立即上架": "🔥", "观察": "👁️", "暂缓": "⏸️"}[p.recommendation]
        print(f"  #{p.rank} {icon} {p.trend_score}分 | {p.title[:40]}")


if __name__ == "__main__":
    main()
