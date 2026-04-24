#!/usr/bin/env python3
"""
AI 质量自评模块 (FR-DR-005) — QA 角色: 陈小兰
功能: 调用 GLM 对短剧剧本+分镜进行结构化评分，低分自动回流

评分维度:
  1. 故事张力 (1-10) — 剧情吸引力、节奏感
  2. 角色一致性 (1-10) — 角色行为是否符合设定
  3. 冲突强度 (1-10) — 矛盾是否尖锐、有看点
  4. 对话自然度 (1-10) — 台词是否口语化、符合角色

回流规则:
  - 综合分 < 阈值 (默认6.5) → 回到 MS-1 重新生成
  - 单维度 < 3.0 → 直接回流
  - 最多回流 3 次，超过则终止并告警

用法:
  python3 quality_assessor.py --script script.json --shots shots.json
  python3 quality_assessor.py --task DRAMA-20260424-001
"""
import json, os, sys, urllib.request, argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config

ARK_API_KEY = config.ARK_API_KEY
API_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
GLM_MODEL = "glm-4-7-251222"

# 可配置阈值 — 运行时可通过 --threshold 覆盖
_QA_THRESHOLD = float(os.environ.get("QA_THRESHOLD", "6.5"))
MAX_RETRIES = int(os.environ.get("QA_MAX_RETRIES", "3"))

DIMENSIONS = {
    "story_tension":      {"name": "故事张力",   "weight": 0.30},
    "character_consistency": {"name": "角色一致性", "weight": 0.25},
    "conflict_intensity": {"name": "冲突强度",   "weight": 0.25},
    "dialogue_naturalness": {"name": "对话自然度", "weight": 0.20},
}

SCORE_PROMPT = """你是一位资深短剧质量评审专家。请对以下短剧剧本进行结构化评分。

评分标准 (1-10分):
1. 故事张力: 剧情是否有吸引力和悬念？节奏是否紧凑？
2. 角色一致性: 角色行为是否符合其设定？前后是否矛盾？
3. 冲突强度: 矛盾是否尖锐？冲突是否有看点和高潮？
4. 对话自然度: 台词是否口语化？是否符合角色性格？

请以 JSON 格式返回评分结果，格式如下:
{{
  "story_tension": 分数,
  "character_consistency": 分数,
  "conflict_intensity": 分数,
  "dialogue_naturalness": 分数,
  "overall_comment": "总体评价 (100字以内)",
  "suggestions": ["改进建议1", "改进建议2", ...],
  "verdict": "pass" 或 "retry" 或 "reject"
}}

剧本内容:
{script}"""


def call_glm(prompt: str) -> Optional[dict]:
    """调用 GLM API 获取评分"""
    data = {
        "model": GLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是一个严格但公正的短剧质量评审。请返回有效的 JSON。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    try:
        req = urllib.request.Request(
            API_ENDPOINT,
            data=json.dumps(data).encode('utf-8'),
            headers={"Authorization": f"Bearer {ARK_API_KEY}", "Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=120)
        body = json.loads(resp.read().decode('utf-8'))
        content = body.get('choices', [{}])[0].get('message', {}).get('content', '')
        # 尝试解析 JSON
        content = content.strip()
        if content.startswith('```'):
            content = content.split('\n', 1)[1].rsplit('\n```', 1)[0]
        return json.loads(content)
    except Exception as e:
        print(f"⚠️  GLM API 调用失败: {e}")
        return None


def rule_based_scoring(script_text: str) -> dict:
    """规则引擎降级评分 (当 API 不可用时)"""
    lines = script_text.strip().split('\n') if script_text else []
    char_count = len(script_text) if script_text else 0

    # 简单规则评分
    dialogue_lines = sum(1 for l in lines if '：' in l or ':' in l)
    scene_breaks = sum(1 for l in lines if l.startswith('#') or '场景' in l or '幕' in l)

    scores = {
        "story_tension": min(round(4 + scene_breaks * 0.5, 1), 10),
        "character_consistency": min(round(5 + dialogue_lines * 0.1, 1), 10),
        "conflict_intensity": min(round(3 + dialogue_lines * 0.15, 1), 10),
        "dialogue_naturalness": min(round(4 + dialogue_lines * 0.1, 1), 10),
        "overall_comment": "【规则引擎降级评分】API 不可用时的近似评估",
        "suggestions": ["建议接入 GLM API 以获取精确评分"],
        "verdict": "pass",
        "_mode": "rule_based"
    }
    return scores


def compute_composite(scores: dict) -> float:
    """加权计算综合分"""
    total = 0
    for key, dim in DIMENSIONS.items():
        val = scores.get(key, 5)
        total += val * dim["weight"]
    return round(total, 1)


def assess_quality(script_text: str, retry_count: int = 0, threshold: float = None, silent: bool = False) -> dict:
    """
    评估剧本质量，返回评分报告
    """
    if threshold is None:
        threshold = _QA_THRESHOLD

    if not silent:
        print(f"🔍 [QA] 质量自评开始 (回流次数: {retry_count}/{MAX_RETRIES})")

    # API 评分
    prompt = SCORE_PROMPT.format(script=script_text[:4000])
    api_scores = call_glm(prompt)

    if api_scores and all(k in api_scores for k in DIMENSIONS):
        scores = api_scores
        mode = "api"
    else:
        if not silent:
            print("⚠️  API 评分失败，降级到规则引擎")
        scores = rule_based_scoring(script_text)
        mode = "rule_based"

    composite = compute_composite(scores)

    # 判定逻辑
    verdict = "pass"
    if composite < threshold:
        verdict = "retry"
    # 单维度低于 3.0 直接回流
    if any(scores.get(k, 5) < 3.0 for k in DIMENSIONS):
        verdict = "retry"
    # 超过最大重试次数则 reject
    if retry_count >= MAX_RETRIES and verdict == "retry":
        verdict = "reject"

    report = {
        "dimensions": {k: scores.get(k, 5) for k in DIMENSIONS},
        "dimension_labels": {k: v["name"] for k, v in DIMENSIONS.items()},
        "composite": composite,
        "threshold": threshold,
        "verdict": verdict,
        "suggestions": scores.get("suggestions", []),
        "overall_comment": scores.get("overall_comment", ""),
        "retry_count": retry_count,
        "max_retries": MAX_RETRIES,
        "assessed_at": datetime.now().isoformat(),
        "mode": mode,
    }

    # 打印报告
    if not silent:
        print(f"\n{'='*50}")
        print(f"📊 AI 质量评分报告")
        print(f"{'='*50}")
        for k, v in report["dimensions"].items():
            label = DIMENSIONS[k]["name"]
            bar = "█" * int(v) + "░" * (10 - int(v))
            print(f"  {label:8s}: {bar} {v}/10")
        print(f"  {'─'*40}")
        print(f"  综合分: {composite}/10 (阈值: {threshold})")
        print(f"  判定: {'✅ 通过' if verdict == 'pass' else '🔄 需回流' if verdict == 'retry' else '❌ 驳回'}")
        if report["suggestions"]:
            print(f"  💡 建议: {', '.join(report['suggestions'][:3])}")
        print(f"  ⏱️  模式: {mode.upper()} | 回流: {retry_count}/{MAX_RETRIES}")
        print()

    return report


def evaluate_and_flow(script_text: str, task_id: str = None, threshold: float = None, silent: bool = False) -> dict:
    """
    评估并执行回流逻辑:
    - pass → 继续 MS-5 (人工审核)
    - retry → 回到 MS-1，retry_count+1
    - reject → 终止任务，飞书告警
    """
    # 读取当前回流次数
    retry_count = 0
    if task_id:
        task_file = Path.home() / f".openclaw/workspace/tasks/active/{task_id}.json"
        if task_file.exists():
            task = json.loads(task_file.read_text())
            retry_count = task.get("qa_retry_count", 0)

    report = assess_quality(script_text, retry_count, threshold, silent)

    # 更新任务状态
    if task_id:
        task_file = Path.home() / f".openclaw/workspace/tasks/active/{task_id}.json"
        if task_file.exists():
            task = json.loads(task_file.read_text())
            task["qa_report"] = report
            task["qa_retry_count"] = retry_count + 1 if report["verdict"] == "retry" else retry_count
            task_file.write_text(json.dumps(task, ensure_ascii=False, indent=2))

    return report


def main():
    parser = argparse.ArgumentParser(description="AI 质量自评 (FR-DR-005)")
    parser.add_argument("--script", help="剧本文件路径 (.json 或 .txt)")
    parser.add_argument("--text", help="直接传入剧本文本")
    parser.add_argument("--task", help="任务 ID (用于回流计数)")
    parser.add_argument("--threshold", type=float, default=_QA_THRESHOLD, help=f"评分阈值 (默认 {_QA_THRESHOLD})")
    parser.add_argument("--json-only", action="store_true", help="仅输出 JSON")
    args = parser.parse_args()

    # 读取剧本
    script_text = ""
    if args.script:
        sp = Path(args.script)
        if sp.suffix == '.json':
            data = json.loads(sp.read_text())
            script_text = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            script_text = sp.read_text()
    elif args.text:
        script_text = args.text
    else:
        # 示例剧本
        script_text = """
场景一：景阳冈山脚
武松：(背行李上) 这店家说冈上有虎，我看不过是吓唬人罢了。
酒保：客官留步！冈上真有猛虎，天色已晚，不如明日再走。
武松：(拍刀) 区区大虫，何足道哉！
(武松大步上山，酒保摇头叹气)

场景二：景阳冈山腰
(风声呼啸，虎啸隐约)
武松：(警觉) 什么声音？
(突然一只猛虎从林中扑出)
猛虎：(怒吼) 吼——
武松：(拔刀) 来得好！
(武松与猛虎搏斗，拳拳到肉)

场景三：景阳冈山顶
(武松骑在虎身上，挥拳猛击)
武松：今日便为民除害！
(猛虎挣扎渐弱，最终倒地)
武松：(喘气) 这大虫果然凶猛...好在此番除了它。
"""
        print("⚠️  未提供剧本，使用示例文本")

    report = evaluate_and_flow(script_text, args.task, args.threshold, args.json_only)

    if args.json_only:
        import json as _json
        print(_json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
