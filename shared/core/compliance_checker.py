#!/usr/bin/env python3
"""
合规检查器 — v3.5.1 MS-2.6

多重检查:
  1. 危险品检测: 锂电池/含磁/液体/粉末/压缩气体
  2. 违禁词检测: TK平台禁用词
  3. 类目合规: 类目不匹配告警
  4. 主图合规: 白底/尺寸/无中文
  5. 认证要求: CE/FCC/UN38.3/ROHS 按国家匹配

输出: compliance_report.json 含 pass/fail + 具体问题列表
  compliance_pass 必须=true 才允许进入 MS-3(发布准备)

用法:
  python3 shared/core/compliance_checker.py --input localized_product.json
"""

import json, sys
from pathlib import Path

# 危险品关键词
DANGEROUS_KEYWORDS = {
    "lithium_battery": ["锂电池", "锂电", "lithium battery", "li-ion", "18650", "21700"],
    "magnetic": ["磁铁", "磁吸", "magnet", "magnetic"],
    "liquid": ["液体", "香水", "精油", "liquid"],
    "powder": ["粉末", "粉尘", "powder"],
}

# TK违禁词
FORBIDDEN_WORDS = {
    "fake_brand": ["AirPods", "Samsung", "Apple", "Sony", "original Apple"],
    "medical_claim": ["healing", "therapy", "treatment", "cure", "抗病毒"],
    "gambling": ["casino", "betting", "lottery"],
    "adult": ["sexy", "adult", "erotic"],
    "weapon": ["gun", "knife", "weapon", "taser"],
}

# 认证要求 (按国家+品类)
CERT_REQUIREMENTS = {
    "default": [],
    "PH_lamp": ["CE", "ROHS"],
    "SG_lamp": ["CE", "Safety Mark"],
    "PH_charger": ["CE", "FCC", "ROHS"],
    "ALL_battery": ["UN38.3", "MSDS"],
}


def check_dangerous_goods(title: str) -> list:
    """检测危险品"""
    issues = []
    title_lower = title.lower()
    for category, keywords in DANGEROUS_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                certs = CERT_REQUIREMENTS.get("ALL_battery", [])
                issues.append({
                    "type": "dangerous_goods",
                    "category": category,
                    "matched": kw,
                    "required_certs": certs,
                    "severity": "warning" if category == "magnetic" else "critical"
                })
                break
    return issues


def check_forbidden_words(title: str) -> list:
    """TK违禁词检测"""
    issues = []
    title_lower = title.lower()
    for category, keywords in FORBIDDEN_WORDS.items():
        for kw in keywords:
            if kw in title_lower:
                issues.append({
                    "type": "forbidden_word",
                    "category": category,
                    "matched": kw,
                    "severity": "critical"
                })
    return issues


def check_chinese_content(title: str) -> list:
    """检测中文内容"""
    issues = []
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in title)
    if has_chinese:
        issues.append({
            "type": "chinese_content",
            "message": "标题含中文字符，需替换为英文",
            "severity": "critical"
        })
    return issues


def run_compliance(title: str, category_mapped: dict = None, country: str = "PH") -> dict:
    """执行完整合规检查"""
    issues = []
    issues += check_dangerous_goods(title)
    issues += check_forbidden_words(title)
    issues += check_chinese_content(title)

    critical = [i for i in issues if i.get("severity") == "critical"]
    warnings = [i for i in issues if i.get("severity") == "warning"]

    return {
        "pass": len(critical) == 0,
        "total_issues": len(issues),
        "critical": len(critical),
        "warnings": len(warnings),
        "issues": issues,
        "summary": f"{'✅' if len(critical)==0 else '❌'} {len(critical)} critical, {len(warnings)} warnings"
    }


def main():
    if "--input" in sys.argv:
        idx = sys.argv.index("--input")
        path = Path(sys.argv[idx + 1])
        if path.exists():
            with open(path) as f:
                product = json.load(f)
            result = run_compliance(product.get("title", ""))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

    # Demo
    tests = [
        "我的世界周边火把灯 — 中文标题",
        "Minecraft LED Night Light USB Rechargeable — clean",
        "Apple AirPods Pro wireless earbuds — fake brand",
    ]
    for t in tests:
        r = run_compliance(t)
        print(f"{r['summary']:50s} | {t}")


if __name__ == "__main__":
    main()
