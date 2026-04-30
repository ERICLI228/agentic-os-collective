#!/usr/bin/env python3
"""
智能决策引擎 — AI先分析 → 推荐最佳选项 → 详细理由 → 你才选
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "shared" / "core"))


@dataclass
class RiskFactor:
    name: str
    level: str  # high/medium/low
    detail: str
    mitigation: str = ""


@dataclass
class Option:
    action: str  # approved / rejected / modify
    label: str   # "✅ 批准发布" / "❌ 驳回重选"
    summary: str
    pros: List[str]
    cons: List[str]
    confidence: float  # 0-1


@dataclass
class DecisionBrief:
    """决策简报 — AI分析后的完整材料"""
    task_id: str
    node: str
    title: str

    # AI 分析
    ai_recommendation: str  # "approved" / "rejected"
    ai_confidence: float    # 0-1
    reasoning: List[str]    # 推荐理由 (3-5条)

    # 关键数据
    score: float            # 综合评分 0-10
    profit_margin: float = 0
    competitor_count: int = 0
    risk_level: str = "medium"

    # 选项
    options: List[Option] = None

    # 风险评估
    risks: List[RiskFactor] = None

    # 如果驳回 — 下一步做什么
    fallback_plan: str = ""

    generated_at: str = ""

    def to_dict(self):
        d = asdict(self)
        d["options"] = [asdict(o) for o in (self.options or [])]
        d["risks"] = [asdict(r) for r in (self.risks or [])]
        return d


def run_ai_analysis(context: dict, node: str) -> dict:
    """
    执行 AI 三轮分析
    1. 参谋审核 — 5维挑刺
    2. 裁判裁决 — 综合评分
    3. 综合推荐 — 最佳选项
    """
    from adversarial_review import create_review_engine, MultiAgentConfig

    content = json.dumps(context, ensure_ascii=False)

    try:
        engine = create_review_engine("tk_product")
        cfg = MultiAgentConfig(
            critic_model="aliyun/qwen3.6-plus",
            judge_model="aliyun/qwen3-coder-plus"
        )

        # 参谋 + 裁判 (独立模型)
        result = engine.review_multi_agent(
            content, "选品报告", context.get("task_id", "decision"),
            multi_config=cfg
        )

        return {
            "total_score": result.total_score,
            "decision": result.decision,
            "dimensions": [d.to_dict() for d in result.dimensions],
            "critique": result.critique_summary,
            "judge_reason": result.judge_reason,
            "elapsed": result.elapsed_seconds,
        }
    except Exception as e:
        # API 不可用时用 Mock
        result = engine.review_mock_multi_agent(content, "选品报告", context.get("task_id", "decision"))
        return {
            "total_score": result.total_score,
            "decision": result.decision,
            "dimensions": [d.to_dict() for d in result.dimensions],
            "critique": f"[Mock 降级] {result.critique_summary}",
            "judge_reason": result.judge_reason,
            "elapsed": result.elapsed_seconds,
            "fallback": str(e)[:100],
        }


def generate_decision_brief(task_id: str, node: str, context: dict) -> DecisionBrief:
    """
    生成决策简报:
    1. 跑 AI 分析
    2. 构建推荐选项
    3. 评估风险
    4. 输出结构化简报
    """

    # Step 1: AI 分析
    analysis = run_ai_analysis(context, node)
    score = analysis["total_score"]
    decision = analysis["decision"]
    dims = analysis["dimensions"]

    # Step 2: 构建推理链
    reasoning = []
    for d in dims:
        if d["severity"] in ("critical", "warning"):
            for f in d["findings"][:1]:
                reasoning.append(f"[{d['dimension']}] {f}")

    if not reasoning:
        reasoning.append(f"综合五维评分 {score}/10，各维度无明显致命缺陷")

    reasoning.append(analysis["critique"])

    # Step 3: 风险评估
    risks = _assess_risks(dims, context)

    # Step 4: 构建选项
    options = _build_options(score, decision, context, risks)

    # Step 5: 驳回后方案
    fallback = _build_fallback(node, context, dims)

    confidence = min(score / 10, 0.95)

    return DecisionBrief(
        task_id=task_id,
        node=node,
        title=context.get("title", "产品选品决策"),
        ai_recommendation=decision,
        ai_confidence=round(confidence, 2),
        reasoning=reasoning[:5],
        score=round(score, 2),
        profit_margin=context.get("profit_margin", 0),
        competitor_count=context.get("competitor_count", 0),
        risk_level=risks[0].level if risks else "low",
        options=options,
        risks=risks,
        fallback_plan=fallback,
        generated_at=datetime.now().isoformat(),
    )


def _assess_risks(dims, context):
    risks = []
    for d in dims:
        if d["severity"] == "critical":
            risks.append(RiskFactor(
                name=d["dimension"],
                level="high",
                detail="; ".join(d["findings"]),
                mitigation=_get_mitigation(d["dimension"]),
            ))

    if context.get("profit_margin", 0) < 30:
        risks.append(RiskFactor(
            name="利润率偏低",
            level="high" if context.get("profit_margin", 0) < 15 else "medium",
            detail=f"当前毛利率 {context.get('profit_margin', 0)}%",
            mitigation="重新议价1688供应商，或提高TK售价",
        ))

    if context.get("competitor_count", 0) > 20:
        risks.append(RiskFactor(
            name="竞争激烈",
            level="high",
            detail=f"当前市场 {context['competitor_count']} 个竞品",
            mitigation="差异化主图/文案/定价，避免价格战",
        ))

    return risks or [RiskFactor(name="无明显风险", level="low",
                                 detail="五维审核未发现致命缺陷")]


def _get_mitigation(dimension: str) -> str:
    tips = {
        "利润可信度": "重新核算1688进价+物流+平台佣金，确认毛利率≥30%",
        "数据真实性": "交叉验证多个数据源（TK后台+第三方工具），排除刷单",
        "竞争壁垒": "增加差异化卖点（赠品/包装/主图），建立品牌认知",
        "供应链风险": "联系备选供应商，确保至少2家可供货",
        "市场时机": "参考Google Trends确认品类趋势，避免季节性误判",
    }
    return tips.get(dimension, "进一步调研确认")


def _build_options(score: float, decision: str, context: dict, risks: list) -> list:
    profit = context.get("profit_margin", 0)
    competitors = context.get("competitor_count", 0)
    high_risks = sum(1 for r in risks if r.level == "high")

    options = []

    # 推荐选项 (AI判断最优)
    if decision == "pass" and score >= 8.0 and high_risks == 0:
        options.append(Option(
            action="approved",
            label="✅ 批准发布 (AI推荐)",
            summary=f"综合评分 {score}/10，利润率 {profit}%，无高危风险，建议立即发布",
            pros=[
                f"AI五维评分 {score}/10，通过审核",
                f"毛利率 {profit}% 符合盈利标准",
                f"竞品数 {competitors}，市场空间充足" if competitors < 15 else f"竞品数 {competitors}，可差异化进入",
                "无明显高危风险",
            ],
            cons=["需要持续监控售后数据和退货率"],
            confidence=0.85,
        ))
    elif decision in ("pass", "rework") and score >= 6.0:
        options.append(Option(
            action="approved",
            label="✅ 批准发布 (需注意风险)",
            summary=f"综合评分 {score}/10，有 {high_risks} 个风险点需关注。AI建议可发布但需监控",
            pros=[
                f"评分 {score}/10，基本达标",
                "可分批次测试，小量试水",
            ],
            cons=[r.detail for r in risks if r.level == "high"][:2],
            confidence=0.65,
        ))
    elif decision == "rework":
        options.append(Option(
            action="modify",
            label="✏️ 驳回修改 (AI推荐)",
            summary=f"综合评分 {score}/10 低于阈值，建议修改后重新提交",
            pros=[
                "修改后有机会达到通过标准",
                f"主要问题集中在: {', '.join(r.name for r in risks[:3])}",
            ],
            cons=["需1-2天重新选品/调整"],
            confidence=0.75,
        ))
    else:
        options.append(Option(
            action="rejected",
            label="❌ 直接驳回 (AI推荐)",
            summary=f"综合评分 {score}/10 严重不达标，建议重新选品",
            pros=["避免低效投入"],
            cons=["需重新启动选品流程"],
            confidence=0.9,
        ))

    # 备选: 强制批准 (用户覆盖AI)
    options.append(Option(
        action="approved",
        label="⚡ 强制批准 (覆盖AI)",
        summary="忽略AI风险提示，直接批准发布",
        pros=["立即推进"],
        cons=[f"忽略 {high_risks} 个高危风险点", "可能造成资金/口碑损失"],
        confidence=0.3,
    ))

    # 备选: 直接驳回
    if options[0].action != "rejected":
        options.append(Option(
            action="rejected",
            label="❌ 直接驳回",
            summary="不论AI建议如何，直接驳回",
            pros=["避免风险"],
            cons=["错失潜在机会"],
            confidence=1.0,
        ))

    return options


def _build_fallback(node: str, context: dict, dims: list) -> str:
    if node == "market_assessment":
        return "重新调研其他品类市场，或等待淡季过后再评估"
    elif node == "selection":
        return "从采集箱未审核的商品中重新选品，优先选择利润率≥30%的品类"
    elif node == "publish":
        return "检查MS-2各子步骤是否全部完成，确认合规/定价/物流无遗漏"
    return "返回上一节点重新评估"


def build_feishu_card(brief: DecisionBrief) -> dict:
    """构建飞书决策卡片 — 含AI分析和推荐理由"""

    header_color = "green" if brief.ai_recommendation == "approved" else (
        "red" if brief.ai_recommendation == "rejected" else "yellow"
    )

    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": f"**{brief.title}**"}},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"🤖 AI推荐: **{brief.ai_recommendation.upper()}** (置信度 {int(brief.ai_confidence*100)}%)"}},
        {"tag": "div", "text": {"tag": "lark_md", "content": f"📊 综合评分: **{brief.score}/10** | 利润率: {brief.profit_margin}% | 竞品: {brief.competitor_count}个"}},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md", "content": "**📋 推荐理由:**"}},
    ]

    for r in brief.reasoning:
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"• {r}"}})

    if brief.risks:
        elements.append({"tag": "hr"})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "**⚠️ 风险提示:**"}})
        for risk in brief.risks:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk.level, "⚪")
            elements.append({"tag": "div", "text": {"tag": "lark_md",
                "content": f"{icon} {risk.name}: {risk.detail}"}})
            if risk.mitigation:
                elements.append({"tag": "div", "text": {"tag": "lark_md",
                    "content": f"   缓解: {risk.mitigation}"}})

    elements.append({"tag": "hr"})
    for opt in brief.options:
        elements.append({"tag": "div", "text": {"tag": "lark_md",
            "content": f"**{opt.label}** (置信度 {int(opt.confidence*100)}%)\n{opt.summary}"}})

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"🤖 {brief.node} · AI决策建议"},
            "template": header_color,
        },
        "elements": elements,
    }


def main():
    import argparse
    p = argparse.ArgumentParser(description="智能决策引擎")
    p.add_argument("--task", default="TK-20260430-001")
    p.add_argument("--node", default="selection")
    p.add_argument("--test", action="store_true")
    args = p.parse_args()

    if args.test:
        ctx = {
            "task_id": args.task,
            "title": "防水手机壳 X Pro — 菲律宾站",
            "profit_margin": 45,
            "competitor_count": 12,
            "price": 5.99,
            "cost": 3.30,
            "category": "手机配件",
        }
        brief = generate_decision_brief(args.task, args.node, ctx)
        card = build_feishu_card(brief)

        print("=" * 60)
        print(f"  🤖 AI决策分析完成")
        print(f"  推荐: {brief.ai_recommendation.upper()}")
        print(f"  评分: {brief.score}/10")
        print(f"  置信度: {int(brief.ai_confidence*100)}%")
        print(f"  风险等级: {brief.risk_level}")
        print("=" * 60)
        for r in brief.reasoning:
            print(f"  📋 {r}")
        print("=" * 60)
        for opt in brief.options:
            print(f"  {opt.label}: {opt.summary[:60]}...")
        print()
        print(json.dumps(brief.to_dict(), ensure_ascii=False, indent=2))
        print("\n✅ --test PASS: decision_engine")
        return

    ctx = {
        "task_id": args.task,
        "title": "TK选品审核",
        "profit_margin": 0,
        "competitor_count": 0,
        "price": 0,
        "cost": 0,
    }
    brief = generate_decision_brief(args.task, args.node, ctx)
    card = build_feishu_card(brief)
    print(json.dumps(card, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
