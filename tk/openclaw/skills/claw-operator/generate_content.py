#!/usr/bin/env python3
"""
TK 内容制作 (FR-TK-005) — MS-3
功能: 基于选品建议生成短视频脚本和发布日历
"""
import json, sys, os
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_DIR = Path.home() / ".openclaw/workspace/artifacts/tk"
TASK_ID = sys.argv[1] if len(sys.argv) > 1 else "TK-CONTENT-001"
MILESTONE_ID = "MS-3"

import sys
_SCRIPT_DIR = Path(__file__).resolve().parent
_CORE_DIR = _SCRIPT_DIR.parent.parent / "core"
sys.path.insert(0, str(_CORE_DIR))
from task_updater import update_milestone

HOOK_TEMPLATES = [
    "还在花大价钱买{m}？这个{c}只要{price}！",
    "{m}的{c}爆卖{d}单，关键在这一点...",
    "测评{d}款{c}，终于找到{m}最好的{m}！",
    "打开{c}的正确方式，{m}都在这样用...",
    "🇹🇭🇻🇳🇮🇩🇲🇾🇵🇭 东南亚爆款{c}实测",
]

COUNTRY_MAP = {"TH": "泰国", "VN": "越南", "ID": "印尼", "MY": "马来西亚", "PH": "菲律宾"}


def load_analysis():
    """加载 MS-2 分析结果"""
    if not OUTPUT_DIR.exists():
        return None
    files = sorted(OUTPUT_DIR.glob("analysis_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if files:
        return json.loads(files[0].read_text())
    return None


def generate_scripts(recommendations):
    """为每个推荐产品生成短视频脚本"""
    scripts = []
    for i, rec in enumerate(recommendations[:3]):
        product = rec.get("product", f"产品{i+1}")
        country = list(COUNTRY_MAP.keys())[i % 5]

        # 构建 hook
        hook = HOOK_TEMPLATES[i % len(HOOK_TEMPLATES)].format(
            m=COUNTRY_MAP.get(country, "东南亚"), c=product[:10], price=f"${5+i*3}.99", d=(i+1)*100
        )

        script = {
            "product": product,
            "target_country": country,
            "target_market": COUNTRY_MAP.get(country, "东南亚"),
            "hook": hook,
            "scenes": [
                {"time": "0-3s", "action": "开箱特写+价格字幕弹出", "text": hook},
                {"time": "3-10s", "action": "产品实拍+功能演示", "text": f"✅ {product}核心卖点展示"},
                {"time": "10-18s", "action": "使用场景+对比效果", "text": f"用之前 vs 用之后 / 对比竞品"},
                {"time": "18-25s", "action": "用户好评+购买引导", "text": "点击下方链接购买 ↘️"},
            ],
            "duration": 25,
            "hashtags": ["#TikTokMadeMeBuyIt", f"#{product.replace(' ', '')}", "#3C", "#测评"],
            "voiceover": "AI配音" if i % 2 == 0 else "真人配音",
        }
        scripts.append(script)

    return scripts


def generate_calendar(scripts):
    """生成7天内容发布日历"""
    today = datetime.now()
    calendar = []
    for i in range(7):
        day = today + timedelta(days=i)
        if i < len(scripts):
            calendar.append({
                "date": day.strftime("%Y-%m-%d"),
                "time": f"{10+i*2:02d}:00",
                "script": scripts[i]["product"],
                "country": scripts[i]["target_country"],
                "status": "scheduled",
            })
        else:
            calendar.append({
                "date": day.strftime("%Y-%m-%d"),
                "time": "10:00",
                "script": "待生成",
                "country": list(COUNTRY_MAP.keys())[i % 5],
                "status": "pending",
            })
    return calendar


def main():
    print(f"📝 [MS-3] 内容制作开始 — {datetime.now().isoformat()}")

    analysis_data = load_analysis()
    recommendations = (analysis_data or {}).get("recommendations", [{
        "product": "防水手机袋", "reason": "样本数据", "action": "推广测试", "priority": "high"
    }])

    scripts = generate_scripts(recommendations)
    calendar = generate_calendar(scripts)

    output = {
        "task_id": TASK_ID, "milestone": MILESTONE_ID,
        "scripts": scripts, "calendar": calendar,
        "generated_at": datetime.now().isoformat(),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    script_path = OUTPUT_DIR / f"scripts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    cal_path = OUTPUT_DIR / f"calendar_{datetime.now().strftime('%Y%m%d')}.json"

    script_path.write_text(json.dumps(scripts, ensure_ascii=False, indent=2))
    cal_path.write_text(json.dumps(calendar, ensure_ascii=False, indent=2))

    update_milestone(TASK_ID, MILESTONE_ID, "completed")

    print(f"✅ 已生成 {len(scripts)} 个脚本, {len(calendar)} 天发布日历")
    print(f"📄 脚本: {script_path}")
    print(f"📄 日历: {cal_path}")


if __name__ == "__main__":
    main()
