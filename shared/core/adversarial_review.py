#!/usr/bin/env python3
"""
通用对抗审核框架 (FR-BS-011)
笔杆子(生成) → 参谋(挑刺) → 裁判(裁决)

支持场景:
- 选品审核 (FR-TK-016): 五维挑刺 + 8 分阈值
- 广告审核 (FR-TK-017): 四维审核
- 剧本审核 (FR-DR-011): 前置审核
- 视频审核 (FR-DR-005): 对抗式质量审核

PRD 设计完成度: 100%
代码实现进度: 0% → 开发中

@author: 阿牛
@date: 2026-04-28
"""

import json
import time
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field


# ============================================================
# 数据模型
# ============================================================

@dataclass
class DimensionCritique:
    """单个维度的挑刺意见"""
    dimension: str           # 维度名称 (如"利润可信度")
    score: float             # 该维度得分 (0-10)
    findings: List[str]      # 发现的问题列表
    severity: str            # "critical" | "warning" | "ok"

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ReviewResult:
    """一次对抗审核的完整结果"""
    scenario: str                    # 场景名称 (如"选品审核")
    content_id: str                  # 被审核内容的 ID
    total_score: float               # 综合得分
    dimensions: List[DimensionCritique]  # 各维度得分
    decision: str                    # "pass" | "rework" | "reject"
    rework_count: int                # 当前回流次数
    max_rework: int                  # 最大回流次数
    critique_summary: str            # 参谋挑刺总结
    judge_reason: str                # 裁判裁决理由
    timestamp: str                   # 审核时间
    elapsed_seconds: float           # 耗时

    def to_dict(self) -> Dict:
        return {
            "scenario": self.scenario,
            "content_id": self.content_id,
            "total_score": self.total_score,
            "dimensions": [d.to_dict() for d in self.dimensions],
            "decision": self.decision,
            "rework_count": self.rework_count,
            "max_rework": self.max_rework,
            "critique_summary": self.critique_summary,
            "judge_reason": self.judge_reason,
            "timestamp": self.timestamp,
            "elapsed_seconds": round(self.elapsed_seconds, 1),
        }


@dataclass
class AdversarialReviewConfig:
    """对抗审核配置"""
    scenario: str                          # 场景名称
    dimensions: List[str]                  # 审核维度列表 (3-5 个)
    threshold: float = 8.0                 # 通过阈值 (默认 8.0)
    rework_threshold: float = 6.0          # 回流阈值下限 (默认 6.0)
    max_rework_cycles: int = 3             # 最大回流次数
    model: str = "coding/qwen3.6-plus"     # 使用的 LLM 模型
    timeout_seconds: int = 300             # 单次 LLM 调用超时

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# 预定义场景配置
# ============================================================

SCENARIO_PRESETS = {
    "market_assessment": {
        "name": "TK 市场判断 (MS-1.5)",
        "dimensions": [
            "竞品饱和度",       # 头部卖家占比？新品进入门槛？广告竞争？
            "利润空间",         # 1688进价vsTK售价？毛利率？退货成本？
            "供应链",           # 货源稳定性？头程时效？库存风险？
            "季节性",           # 品类是否受季节影响？Q1-Q4 波动？
            "达人潜力",         # 该品类达人丰富度？佣金接受度？
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
    "tk_product": {
        "name": "TK 选品对抗审核",
        "dimensions": [
            "利润可信度",     # 成本计算是否漏项？毛利率是否虚高？
            "数据真实性",     # 销量数据是否刷单？评论是否水军？
            "竞争壁垒",       # 头部卖家是否垄断？新品进入门槛？
            "供应链风险",     # 1688 货源稳定性？物流时效？退货率？
            "市场时机",       # 品类处于上升期还是衰退期？季节性风险？
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
    "tk_ad": {
        "name": "TK 广告文案对抗审核",
        "dimensions": [
            "创意吸引力",     # 标题是否抓眼球？CTA 是否有力？
            "ROI 预估",       # 投放成本与预期转化是否匹配？
            "合规风险",       # 是否违反 TK 广告政策？敏感词？
            "竞品差异化",     # 与竞品广告相比有何独特卖点？
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
    # Sprint 3.2: TK 广告全维度审核（合规/转化/本地化/品牌）
    "tk_ad_review": {
        "name": "TK 广告全维度对抗审核",
        "dimensions": [
            "合规",           # TK 广告政策/禁投品类/敏感词/版权
            "转化",           # CTA力度/价值主张/紧迫感/落地页一致性
            "本地化",         # 目标国语言/文化禁忌/本地支付习惯/节日适配
            "品牌",           # 品牌一致性/视觉规范/调性匹配/长期价值
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
    "drama_script": {
        "name": "短剧剧本对抗审核",
        "dimensions": [
            "编剧规则合规",    # 是否符合编剧规则引擎？
            "场景完整性",     # 场景数量/对话长度是否达标？
            "剧情节奏",       # 节奏是否合理？有无拖沓？
            "逻辑一致性",     # 是否有逻辑漏洞？
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
    # Sprint 3.3: 剧本生成后即时预审（生成→视频前拦截）
    "drama_script_review": {
        "name": "短剧剧本即时预审",
        "dimensions": [
            "角色一致性",     # 角色行为/台词是否符合人设？
            "剧情张力",       # 冲突是否尖锐？钩子是否有效？
            "台词自然度",     # 是否AI味重？符合角色身份？
            "时长适配",       # 预估时长是否符合单集要求（60-90s）？
            "合规",           # 无违规内容（血腥/暴力/敏感话题）？
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
    "drama_video": {
        "name": "短剧视频对抗式质量审核",
        "dimensions": [
            "故事张力",       # 节奏是否拖沓？高潮是否到位？
            "角色一致性",     # 外貌/性格/语气是否前后一致？
            "冲突强度",       # 矛盾是否尖锐？转折是否合理？
            "对话自然度",     # 是否符合角色身份？有无 AI 痕迹？
            "商业化潜力",     # 完播率预估？传播力？带货适配性？
        ],
        "threshold": 8.0,
        "rework_threshold": 6.0,
        "max_rework_cycles": 3,
    },
}


# ============================================================
# LLM 调用层
# ============================================================

class LLMClient:
    """
    轻量级 LLM 客户端
    支持 CODING 计划 / 阿里云 DashScope
    简单优先，不做过度抽象
    """

    PROVIDERS = {
        "coding": {
            "url": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
            "key_env": "CODING_API_KEY",
        },
        "aliyun": {
            "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            "key_env": "DASHSCOPE_API_KEY",
        },
    }

    def __init__(self, model: str = "coding/qwen3.6-plus"):
        self.model = model
        self.provider, self.model_name = self._parse_model(model)

    @staticmethod
    def _parse_model(model: str) -> tuple:
        """解析模型名，如 'aliyun/qwen3.6-plus' → ('aliyun', 'qwen3.6-plus')"""
        if "/" in model:
            parts = model.split("/", 1)
            return parts[0], parts[1]
        return "aliyun", model

    def _get_api_key(self) -> str:
        """获取 API Key — 从环境变量读取"""
        env_key = self.PROVIDERS.get(self.provider, {}).get("key_env", "")
        key = os.environ.get(env_key, "")
        if key:
            return key
        raise RuntimeError(
            f"未配置 {self.provider} API Key，请在 .env 设置 {env_key}"
        )

    def _get_url(self) -> str:
        return self.PROVIDERS.get(self.provider, {}).get(
            "url", "https://api.siliconflow.cn/v1/chat/completions"
        )

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        """调用 LLM，返回文本"""
        import requests

        url = self._get_url()
        headers = {
            "Authorization": f"Bearer {self._get_api_key()}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def call_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
    ) -> Dict:
        """调用 LLM 并解析 JSON 输出"""
        text = self.call(system_prompt, user_prompt, temperature)
        # 清理 markdown 代码块
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)


# ============================================================
# 对抗审核引擎
# ============================================================

class AdversarialReviewEngine:
    """
    通用对抗审核引擎

    工作流程:
    1. [参谋] 按维度逐条挑刺 → 输出结构化批评
    2. [裁判] 综合参谋意见打分 → 返回 通过/回流/驳回
    """

    def __init__(self, config: AdversarialReviewConfig):
        self.config = config
        self.client = LLMClient(config.model)

    def _build_critic_prompt(self, content: str, content_type: str) -> tuple:
        """构建参谋挑刺 prompt"""
        dims = ", ".join(self.config.dimensions)
        system_prompt = f"""你是一个专业的审核参谋（批判角色）。你的职责是对{content_type}内容进行严格的对抗性审核。

审核维度：{dims}

你必须从每个维度出发，找出内容中的问题、漏洞和风险。
评分标准：0-10 分，10 分为完美。

请严格按以下 JSON 格式输出：
{{
  "dimension_scores": {{
    "维度1": 分数,
    "维度2": 分数,
    ...
  }},
  "dimension_critiques": {{
    "维度1": {{
      "findings": ["问题1", "问题2"],
      "severity": "critical|warning|ok"
    }},
    ...
  }},
  "summary": "一句话总结主要问题"
}}"""

        user_prompt = f"""请审核以下{content_type}内容：

---
{content}
---

请从以下维度进行严格挑刺：{dims}

注意：
1. 每个维度必须给出具体发现的问题，不能只说"还行"
2. 评分要客观，不要因为礼貌而给高分
3. severity 标准：critical=致命问题，warning=需关注，ok=无明显问题
4. 只输出 JSON，不要其他文字"""

        return system_prompt, user_prompt

    def _build_judge_prompt(
        self,
        content_summary: str,
        critic_result: Dict,
        rework_count: int,
    ) -> tuple:
        """构建裁判裁决 prompt"""
        dims = ", ".join(self.config.dimensions)
        system_prompt = f"""你是一个严格的审核裁判（裁决角色）。你收到一份参谋的审核意见。

你的职责：
1. 综合参谋意见，给出 0-10 的综合评分
2. 做出裁决：
   - 综合分 >= {self.config.threshold}：通过 (pass)
   - 综合分 {self.config.rework_threshold}-{self.config.threshold}：回流修改 (rework)
   - 综合分 < {self.config.rework_threshold}：驳回 (reject)
3. 说明裁决理由

审核维度：{dims}
当前回流次数：{rework_count}/{self.config.max_rework_cycles}

请严格按以下 JSON 格式输出：
{{
  "total_score": 综合评分(0-10的浮点数),
  "decision": "pass|rework|reject",
  "reason": "裁决理由，说明为什么做这个决定"
}}"""

        # 格式化参谋意见
        critique_lines = []
        for dim in self.config.dimensions:
            score = critic_result.get("dimension_scores", {}).get(dim, 0)
            crit = critic_result.get("dimension_critiques", {}).get(dim, {})
            findings = crit.get("findings", [])
            findings_text = "; ".join(findings) if findings else "无明显问题"
            severity = crit.get("severity", "ok")
            critique_lines.append(f"- {dim}: {score}/10 [{severity}] {findings_text}")

        critique_text = "\n".join(critique_lines)

        user_prompt = f"""审核内容摘要：
{content_summary}

参谋审核意见：
{critique_text}

参谋总结：{critic_result.get("summary", "")}

请综合以上信息，给出你的裁决。"""

        return system_prompt, user_prompt

    def _get_content_summary(self, content: str, max_len: int = 500) -> str:
        """截取内容摘要"""
        if len(content) <= max_len:
            return content
        return content[:max_len] + "..."

    def review(
        self,
        content: str,
        content_type: str = "内容",
        content_id: str = "",
        rework_count: int = 0,
    ) -> ReviewResult:
        """
        执行一次对抗审核

        Args:
            content: 被审核的内容
            content_type: 内容类型描述 (如"选品报告"/"广告文案"/"剧本")
            content_id: 内容 ID（用于追踪）
            rework_count: 当前已回流次数

        Returns:
            ReviewResult: 审核结果
        """
        start_time = time.time()
        content_id = content_id or f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Step 1: 参谋挑刺
        print(f"  🔍 [参谋] 开始审核 {content_type}...")
        critic_sys, critic_usr = self._build_critic_prompt(content, content_type)
        critic_result = self.client.call_json(critic_sys, critic_usr)

        # 构建维度结果
        dimensions = []
        for dim in self.config.dimensions:
            score = critic_result.get("dimension_scores", {}).get(dim, 0)
            crit = critic_result.get("dimension_critiques", {}).get(dim, {})
            findings = crit.get("findings", [])
            severity = crit.get("severity", "ok")

            # 根据分数自动判定 severity
            if score < self.config.rework_threshold:
                severity = "critical"
            elif score < self.config.threshold:
                severity = "warning" if not severity or severity == "ok" else severity

            dimensions.append(DimensionCritique(
                dimension=dim,
                score=float(score),
                findings=findings,
                severity=severity,
            ))

        # Step 2: 裁判裁决
        print(f"  ⚖️  [裁判] 综合裁决...")
        content_summary = self._get_content_summary(content)
        judge_sys, judge_usr = self._build_judge_prompt(
            content_summary, critic_result, rework_count
        )
        judge_result = self.client.call_json(judge_sys, judge_usr)

        total_score = float(judge_result.get("total_score", 0))
        decision = judge_result.get("decision", "reject")
        judge_reason = judge_result.get("reason", "")

        # 验证裁决逻辑
        if total_score >= self.config.threshold:
            expected = "pass"
        elif total_score >= self.config.rework_threshold:
            expected = "rework"
        else:
            expected = "reject"

        # 如果裁判决策与分数不匹配，以分数为准
        if decision != expected:
            print(f"  ⚠️  裁判决策({decision})与分数({total_score})不匹配，修正为 {expected}")
            decision = expected

        # 超过最大回流次数自动转为驳回
        if decision == "rework" and rework_count >= self.config.max_rework_cycles:
            decision = "reject"
            judge_reason = f"已达到最大回流次数({self.config.max_rework_cycles})，自动驳回"

        elapsed = time.time() - start_time

        result = ReviewResult(
            scenario=self.config.scenario,
            content_id=content_id,
            total_score=round(total_score, 2),
            dimensions=dimensions,
            decision=decision,
            rework_count=rework_count,
            max_rework=self.config.max_rework_cycles,
            critique_summary=critic_result.get("summary", ""),
            judge_reason=judge_reason,
            timestamp=datetime.now().isoformat(),
            elapsed_seconds=elapsed,
        )

        return result

    # ============================================================
    # Mock 模式 (无 API Key 时用于测试)
    # ============================================================

    def review_mock(
        self,
        content: Any,
        content_type: str = "内容",
        content_id: str = "",
        rework_count: int = 0,
    ) -> ReviewResult:
        """Mock 审核 — 模拟 3-Agent 对抗审核流程，用于无 API Key 时的功能测试"""
        start_time = time.time()
        content_id = content_id or f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 模拟参谋挑刺
        import hashlib
        raw = json.dumps(content, ensure_ascii=False) if isinstance(content, dict) else str(content)
        seed = int(hashlib.md5((raw + content_type).encode()).hexdigest()[:8], 16)

        dimensions = []
        for i, dim in enumerate(self.config.dimensions):
            score = 5.0 + (seed % 50) / 10.0  # 5.0-9.9
            seed = (seed * 1103515245 + 12345) % (2**31)
            findings = []
            if score < self.config.rework_threshold:
                findings = [f"{dim}存在严重问题，需立即修正"]
                severity = "critical"
            elif score < self.config.threshold:
                findings = [f"{dim}有改进空间，建议优化"]
                severity = "warning"
            else:
                findings = [f"{dim}表现良好"]
                severity = "ok"
            dimensions.append(DimensionCritique(
                dimension=dim, score=round(score, 1), findings=findings, severity=severity
            ))

        total_score = round(sum(d.score for d in dimensions) / len(dimensions), 2)

        if total_score >= self.config.threshold:
            decision = "pass"
            reason = "各项指标均达标，审核通过"
        elif total_score >= self.config.rework_threshold:
            decision = "rework"
            reason = "部分指标未达标，需要回流修改"
        else:
            decision = "reject"
            reason = "多项指标不达标，予以驳回"

        if decision == "rework" and rework_count >= self.config.max_rework_cycles:
            decision = "reject"
            reason = f"已达到最大回流次数({self.config.max_rework_cycles})，自动驳回"

        elapsed = time.time() - start_time

        return ReviewResult(
            scenario=self.config.scenario,
            content_id=content_id,
            total_score=total_score,
            dimensions=dimensions,
            decision=decision,
            rework_count=rework_count,
            max_rework=self.config.max_rework_cycles,
            critique_summary="Mock 模式: 模拟审核完成",
            judge_reason=reason,
            timestamp=datetime.now().isoformat(),
            elapsed_seconds=elapsed,
        )

    def review_with_rework(
        self,
        content: str,
        content_type: str = "内容",
        content_id: str = "",
        max_retries: Optional[int] = None,
        use_mock: bool = False,
    ) -> List[ReviewResult]:
        """
        执行对抗审核，自动回流

        Args:
            content: 被审核的内容
            content_type: 内容类型描述
            content_id: 内容 ID
            max_retries: 最大回流次数 (默认使用配置值)
            use_mock: 是否使用 Mock 模式

        Returns:
            审核结果列表（包含每次回流的结果）
        """
        if max_retries is None:
            max_retries = self.config.max_rework_cycles

        results = []
        current_content = content

        for i in range(max_retries + 1):
            if use_mock:
                result = self.review_mock(current_content, content_type, content_id, rework_count=i)
            else:
                result = self.review(current_content, content_type, content_id, rework_count=i)
            results.append(result)

            print(f"  📊 第 {i + 1} 轮审核: {result.total_score} 分 → {result.decision}")
            for dim in result.dimensions:
                icon = {"critical": "🔴", "warning": "🟡", "ok": "🟢"}.get(dim.severity, "⚪")
                print(f"    {icon} {dim.dimension}: {dim.score}/10")

            if result.decision == "pass":
                print(f"  ✅ 审核通过！")
                break
            elif result.decision == "reject":
                print(f"  ❌ 审核驳回: {result.judge_reason}")
                break
            else:
                print(f"  🔄 需要回流修改 (第 {i + 1}/{max_retries} 次)")
                # 在真实场景中，这里会调用 Agent 进行修改
                # 当前版本只记录结果，不自动修改（需要 Agent 层配合）
                break

        return results


# ============================================================
# 便捷函数
# ============================================================

def create_review_engine(
    scenario: str,
    custom_config: Optional[Dict] = None,
) -> AdversarialReviewEngine:
    """
    快速创建对抗审核引擎

    Args:
        scenario: 预定义场景名 ("tk_product" / "tk_ad" / "drama_script" / "drama_video")
        custom_config: 自定义配置覆盖 (可选)

    Returns:
        AdversarialReviewEngine 实例
    """
    preset = SCENARIO_PRESETS.get(scenario)
    if not preset:
        raise ValueError(f"未知场景: {scenario}，可用场景: {list(SCENARIO_PRESETS.keys())}")

    config = AdversarialReviewConfig(
        scenario=preset["name"],
        dimensions=preset["dimensions"],
        threshold=preset.get("threshold", 8.0),
        rework_threshold=preset.get("rework_threshold", 6.0),
        max_rework_cycles=preset.get("max_rework_cycles", 3),
    )

    # 应用自定义覆盖
    if custom_config:
        for key, value in custom_config.items():
            if hasattr(config, key):
                setattr(config, key, value)

    return AdversarialReviewEngine(config)


def quick_review(
    content: str,
    scenario: str,
    content_type: str = "内容",
) -> ReviewResult:
    """
    一键对抗审核（最简接口）

    Args:
        content: 被审核内容
        scenario: 场景名
        content_type: 内容类型描述

    Returns:
        ReviewResult 审核结果
    """
    engine = create_review_engine(scenario)
    return engine.review(content, content_type)


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("  通用对抗审核框架 (FR-BS-011)")
    print("  Agentic OS v3.4")
    print("=" * 60)
    print()

    use_mock = "--mock" in sys.argv
    if use_mock:
        sys.argv.remove("--mock")

    # 如果没有参数，运行演示
    if len(sys.argv) < 2:
        print("用法:")
        print("  python adversarial_review.py <scenario> [content_file] [--mock]")
        print()
        print("可用场景:")
        for key, preset in SCENARIO_PRESETS.items():
            dims = ", ".join(preset["dimensions"])
            print(f"  {key}: {preset['name']}")
            print(f"    维度: {dims}")
            print()

        if use_mock:
            print("📝 演示模式 (Mock): 模拟审核一份选品报告...")
        else:
            print("📝 演示模式 (LLM): 使用 LLM 审核一份选品报告...")
        print()

        demo_content = """
选品报告: 防水手机壳 X Pro
- 品类: 手机配件/手机壳
- 目标市场: 印尼
- 采购成本: 8 元 (1688)
- 建议售价: $5.99 (~42 元)
- 毛利率: 81%
- 竞品分析: TikTok 印尼月销 5000+ 单
- 供应商: 深圳 XX 电子 (1688 金牌供应商)
- 物流: 海运 15 天，$0.5/件
- 日销预估: 50 单/天
"""

        engine = create_review_engine("tk_product")

        if use_mock:
            result = engine.review_mock(demo_content.strip(), "选品报告", "demo_product_001")
        else:
            try:
                result = engine.review(demo_content.strip(), "选品报告", "demo_product_001")
            except Exception as e:
                print(f"⚠️  LLM 调用失败: {e}")
                print("使用 Mock 模式继续演示...")
                print()
                result = engine.review_mock(demo_content.strip(), "选品报告", "demo_product_001")

        print()
        print("=" * 60)
        print("  审核结果")
        print("=" * 60)
        print(f"  场景: {result.scenario}")
        print(f"  综合评分: {result.total_score}/10")
        print(f"  裁决: {result.decision}")
        print(f"  耗时: {result.elapsed_seconds:.1f} 秒")
        print()
        for dim in result.dimensions:
            icon = {"critical": "🔴", "warning": "🟡", "ok": "🟢"}.get(dim.severity, "⚪")
            print(f"  {icon} {dim.dimension}: {dim.score}/10 [{dim.severity}]")
            for f in dim.findings:
                print(f"     - {f}")
        print()
        print(f"  裁判理由: {result.judge_reason}")
        print()
    else:
        scenario = sys.argv[1]
        content_file = sys.argv[2] if len(sys.argv) > 2 else None

        if content_file:
            with open(content_file) as f:
                content = f.read()
        else:
            content = sys.stdin.read()

        engine = create_review_engine(scenario)

        if use_mock:
            result = engine.review_mock(content.strip(), "审核内容")
        else:
            result = engine.review(content.strip(), "审核内容")

        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
