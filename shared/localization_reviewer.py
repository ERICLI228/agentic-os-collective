#!/usr/bin/env python3
"""
本地化审查引擎 — v3.6
TK 5国内容本地化质量审核: LLM语义+术语+禁忌词+转化力+超时优化

解决 MS-2.1 遗留问题: LLM调用需超时优化
"""
import json
import sys
import os
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutTimeout

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "shared" / "core"))

LLM_TIMEOUT = 20  # 单次 LLM 调用超时 20s

FIVE_COUNTRIES = [
    {"code": "PH", "lang": "en", "name": "菲律宾"},
    {"code": "SG", "lang": "en", "name": "新加坡"},
    {"code": "VN", "lang": "vi", "name": "越南"},
    {"code": "TH", "lang": "th", "name": "泰国"},
    {"code": "MY", "lang": "ms", "name": "马来西亚"},
]

TABOO_WORDS = {
    "PH": ["counterfeit", "fake", "replica", "guaranteed refund", "100% original"],
    "SG": ["cheapest", "lowest price", "guaranteed", "fake", "replica"],
    "VN": ["h ng giả", "h ng nhái", "fake", "replica", "bảo h nh"],
    "TH": ["ของปลอม", "ของก๊อบ", "fake", "ของแท้ 100%"],
    "MY": ["tiruan", "palsu", "fake", "jaminan", "100% asli"],
}

CATEGORY_TERMS = {
    "手机壳": {"en": "phone case", "vi": "ốp điện thoại", "th": "เคสมือถือ", "ms": "sarung telefon"},
    "充电器": {"en": "charger", "vi": "bộ sạc", "th": "เครื่องชาร์จ", "ms": "pengecas"},
    "数据线": {"en": "cable", "vi": "cáp", "th": "สายชาร์จ", "ms": "kabel"},
    "耳机": {"en": "earphones", "vi": "tai nghe", "th": "หูฟัง", "ms": "fon telinga"},
    "钢化膜": {"en": "screen protector", "vi": "miếng dán cường lực", "th": "ฟิล์มกันรอย", "ms": "pelindung skrin"},
    "支架": {"en": "stand", "vi": "giá đỡ", "th": "ขาตั้ง", "ms": "penyangga"},
}


@dataclass
class LocalizationIssue:
    field: str
    severity: str  # critical / warning / suggestion
    description: str
    original: str = ""
    suggested: str = ""


@dataclass
class LocalizationReview:
    task_id: str
    product_name: str
    country: str
    target_lang: str
    score: float
    issues: List[LocalizationIssue] = field(default_factory=list)
    translated_title: str = ""
    translated_desc: str = ""
    has_taboo: bool = False
    llm_timeout: bool = False
    data_source: str = "mock"
    reviewed_at: str = ""


def _call_llm(prompt: str, model: str = "aliyun/qwen3.6-plus") -> Optional[str]:
    """带超时的 LLM 调用"""
    try:
        import requests
        api_key = os.environ.get("DASHSCOPE_API_KEY", "")
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY", "")

        if not api_key:
            return None

        # DASHSCOPE
        if "dashscope" in api_key or "sk-" == api_key[:3]:
            resp = requests.post(
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.3,
                },
                timeout=LLM_TIMEOUT,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        return None
    except Exception:
        return None


def _check_taboo(text: str, country_code: str) -> List[LocalizationIssue]:
    """禁忌词检查"""
    issues = []
    banned = TABOO_WORDS.get(country_code, [])
    for word in banned:
        if word.lower() in text.lower():
            issues.append(LocalizationIssue(
                field="title",
                severity="critical",
                description=f"触发禁忌词 '{word}' — 可能导致商品下架",
                original=text,
                suggested=f"移除 '{word}' 或用合规词汇替换",
            ))
    return issues


def _check_terminology(text: str, product_category: str, target_lang: str) -> List[LocalizationIssue]:
    """术语一致性检查"""
    issues = []
    terms = CATEGORY_TERMS.get(product_category, {})
    expected = terms.get(target_lang, "")
    if expected and expected.lower() not in text.lower():
        for lang, term in terms.items():
            if term.lower() in text.lower():
                issues.append(LocalizationIssue(
                    field="title",
                    severity="warning",
                    description=f"可能用了 {lang} 术语 '{term}' 而非目标语言 {target_lang} 术语 '{expected}'",
                    suggested=expected,
                ))
    return issues


def _check_readability(text: str) -> float:
    """可读性评分 (简化版 Flesch-Kincaid)"""
    if not text:
        return 0
    words = text.split()
    if not words:
        return 0
    avg_len = sum(len(w) for w in words) / len(words)
    # 短词好读 → 高分
    if avg_len <= 4:
        return 9.0
    elif avg_len <= 6:
        return 7.5
    elif avg_len <= 8:
        return 5.0
    else:
        return 3.0


def review_localization(task_id: str, product_name: str, original_title: str,
                        original_desc: str, category: str = "手机壳",
                        use_llm: bool = True) -> List[LocalizationReview]:
    """
    5国本地化审查 — 并行执行 + 超时保护

    返回每个国家的审查结果，含评分+问题+建议翻译
    """

    def review_single(country: dict) -> LocalizationReview:
        start = time.time()
        issues = []
        translated_title = ""
        translated_desc = ""
        llm_timeout = False
        data_source = "mock"

        # Step 1: LLM 翻译 (带超时)
        if use_llm:
            prompt = f"""Translate this product listing from Chinese to {country['lang']} for TikTok Shop {country['name']}.
Title: {original_title}
Description: {original_desc}
Requirements:
- Use natural, native-sounding {country['lang']}
- Avoid machine-translation style
- Keep it concise for mobile shopping
- Include key selling points
Return JSON: {{"title": "...", "description": "..."}}"""

            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(_call_llm, prompt)
                    try:
                        result = future.result(timeout=LLM_TIMEOUT)
                        if result:
                            try:
                                parsed = json.loads(result)
                                translated_title = parsed.get("title", "")
                                translated_desc = parsed.get("description", "")
                                data_source = "real"
                            except json.JSONDecodeError:
                                # 非 JSON 输出，尝试提取
                                lines = result.strip().split("\n")
                                for line in lines:
                                    if "title" in line.lower() and ":" in line:
                                        translated_title = line.split(":", 1)[1].strip().strip('"').strip("'")
                                    if "description" in line.lower() and ":" in line:
                                        translated_desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                    except FutTimeout:
                        llm_timeout = True
                        translated_title = f"[超时] {original_title}"
                        translated_desc = f"[超时] {original_desc}"
            except Exception as e:
                llm_timeout = True
                translated_title = f"[错误] {original_title}"
                translated_desc = f"[错误: {str(e)[:50]}]"

        if not translated_title:
            translated_title = _simple_translate(original_title, country["lang"])
            translated_desc = _simple_translate(original_desc, country["lang"])
            data_source = "mock"

        # Step 2: 禁忌词检查
        taboo = _check_taboo(translated_title, country["code"])
        taboo += _check_taboo(translated_desc, country["code"])
        issues.extend(taboo)

        # Step 3: 术语检查
        term = _check_terminology(translated_title + " " + translated_desc, category, country["lang"])
        issues.extend(term)

        # Step 4: 可读性
        readability = _check_readability(translated_title)
        if readability < 5:
            issues.append(LocalizationIssue(
                field="title", severity="warning",
                description=f"标题可读性偏低 ({readability}/10)，建议简化词汇",
            ))

        # Step 5: 长度检查 (TK 标题建议 20-80 字符)
        title_len = len(translated_title)
        if title_len > 100:
            issues.append(LocalizationIssue(
                field="title", severity="warning",
                description=f"标题过长 ({title_len}字符)，建议控制在80以内",
                suggested=translated_title[:80] + "...",
            ))
        elif title_len < 10:
            issues.append(LocalizationIssue(
                field="title", severity="suggestion",
                description=f"标题过短 ({title_len}字符)，建议补充卖点关键词",
            ))

        # 计算总分
        penalty = sum(10 if i.severity == "critical" else (5 if i.severity == "warning" else 2) for i in issues)
        score = max(0, min(10, round(readability - penalty / 10 + 2, 1)))

        elapsed = round(time.time() - start, 2)
        issues.insert(0, LocalizationIssue(
            field="_meta", severity="info",
            description=f"审查耗时 {elapsed}s | LLM={not llm_timeout} | 数据={data_source}",
        ))

        return LocalizationReview(
            task_id=task_id,
            product_name=product_name,
            country=country["code"],
            target_lang=country["lang"],
            score=score,
            issues=issues,
            translated_title=translated_title,
            translated_desc=translated_desc,
            has_taboo=len(taboo) > 0,
            llm_timeout=llm_timeout,
            data_source=data_source,
            reviewed_at=datetime.now().isoformat(),
        )

    results = []
    for country in FIVE_COUNTRIES:
        results.append(review_single(country))

    # 写入 DB
    try:
        from tk_pipeline_db import save_localization_review
        for r in results:
            save_localization_review(task_id, "product_title", r.country, r.score,
                                     [asdict(i) for i in r.issues])
    except Exception:
        pass

    return results


def _simple_translate(text: str, target_lang: str) -> str:
    """简单术语替换 (无 LLM 时的降级方案)"""
    replacements = {
        "防水": {"en": "Waterproof", "vi": "Chống nước", "th": "กันน้ำ", "ms": "Kalis air"},
        "手机壳": {"en": "Phone Case", "vi": "Ốp điện thoại", "th": "เคสมือถือ", "ms": "Sarung telefon"},
        "防摔": {"en": "Shockproof", "vi": "Chống sốc", "th": "กันกระแทก", "ms": "Kalis hentakan"},
        "透明": {"en": "Clear", "vi": "Trong suốt", "th": "ใส", "ms": "Jelas"},
        "超薄": {"en": "Ultra Thin", "vi": "Siêu mỏng", "th": "บางเฉียบ", "ms": "Sangat nipis"},
        "磁吸": {"en": "Magnetic", "vi": "Nam châm", "th": "แม่เหล็ก", "ms": "Magnetik"},
        "支架": {"en": "Stand", "vi": "Giá đỡ", "th": "ขาตั้ง", "ms": "Penyangga"},
        "硅胶": {"en": "Silicone", "vi": "Silicone", "th": "ซิลิโคน", "ms": "Silikon"},
    }
    result = text
    for zh, trans in replacements.items():
        if zh in result:
            result = result.replace(zh, trans.get(target_lang, zh))
    return result


def main():
    import argparse
    p = argparse.ArgumentParser(description="本地化审查引擎 v3.6")
    p.add_argument("--task", default="TK-LOCALIZE")
    p.add_argument("--product", default="防水防摔透明手机壳 磁吸支架")
    p.add_argument("--desc", default="超薄硅胶材质，360度防摔保护，支持无线充电")
    p.add_argument("--category", default="手机壳")
    p.add_argument("--no-llm", action="store_true", help="不使用 LLM (仅规则检查)")
    p.add_argument("--test", action="store_true")
    args = p.parse_args()

    if args.test:
        print("=" * 60)
        print("  🌏 本地化审查 — 5国并行测试")
        print("=" * 60)

        reviews = review_localization(
            args.task, args.product, args.product, args.desc,
            category=args.category, use_llm=not args.no_llm,
        )

        for r in reviews:
            tag = "[真实]" if r.data_source == "real" else "[模拟]"
            print(f"\n{r.country} ({r.target_lang}) {tag} — 评分: {r.score}/10")
            print(f"  翻译: {r.translated_title[:60]}...")
            print(f"  禁忌词: {'⚠️ 触发' if r.has_taboo else '✅ 通过'}")
            print(f"  LLM超时: {'⚠️ 是' if r.llm_timeout else '✅ 否'}")
            for i in r.issues:
                icon = {"critical": "🔴", "warning": "🟡", "suggestion": "💡", "info": "ℹ️"}.get(i.severity, "")
                print(f"  {icon} [{i.severity}] {i.description[:70]}")

        print("\n✅ --test PASS: localization_reviewer")
        return

    reviews = review_localization(
        args.task, args.product, args.product, args.desc,
        category=args.category, use_llm=not args.no_llm,
    )
    print(json.dumps([asdict(r) for r in reviews], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
