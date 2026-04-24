#!/usr/bin/env python3
"""
TK 发布与追踪 (FR-TK-008/010/015) — MS-4
功能: 模拟发布流程，追踪视频表现数据
状态: ⚠️ 模拟模式 — 真实发布需 TikTok API 接入
"""
import json, sys, os, random
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_DIR = Path.home() / ".openclaw/workspace/artifacts/tk"
TASK_ID = sys.argv[1] if len(sys.argv) > 1 else "TK-PUBLISH-001"
MILESTONE_ID = "MS-4"

import sys
_SCRIPT_DIR = Path(__file__).resolve().parent
_CORE_DIR = _SCRIPT_DIR.parent.parent / "core"
sys.path.insert(0, str(_CORE_DIR))
from task_updater import update_milestone


def load_content_scripts():
    """加载 MS-3 生成的脚本"""
    if not OUTPUT_DIR.exists():
        return []
    files = sorted(OUTPUT_DIR.glob("scripts_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if files:
        return json.loads(files[0].read_text())
    return []


def simulate_publish(scripts):
    """模拟发布 (真实发布需 TikTok API + 店小秘)"""
    results = []
    for script in scripts[:3]:
        statuses = ["published", "scheduled", "draft"]
        result = {
            "product": script.get("product", "Unknown"),
            "target_country": script.get("target_country", "SEA"),
            "publish_time": (datetime.now() + timedelta(hours=random.randint(1, 6))).isoformat(),
            "status": random.choice(statuses),
            "tiktok_video_id": f"vid_{random.randint(1000000, 9999999)}",
            "note": "⚠️ 模拟发布 — 真实发布需配置 TikTok API 密钥",
        }
        results.append(result)
    return results


def generate_performance_data(publish_results, hours_back=24):
    """生成 (模拟) 视频表现数据"""
    data = []
    for r in publish_results:
        base_views = random.randint(5000, 500000)
        base_likes = int(base_views * random.uniform(0.03, 0.08))
        base_comments = int(base_views * random.uniform(0.005, 0.02))

        for h in range(0, hours_back, 4):
            growth = 1 + h * random.uniform(0.1, 0.5)
            data.append({
                "video_id": r["tiktok_video_id"],
                "product": r["product"],
                "timestamp": (datetime.now() - timedelta(hours=h)).isoformat(),
                "views": int(base_views * growth),
                "likes": int(base_likes * growth),
                "comments": int(base_comments * growth),
                "shares": int(base_views * growth * 0.01),
                "engagement_rate": round(random.uniform(3, 8), 2),
                "note": "⚠️ 模拟数据 — 真实数据需 TikTok Analytics API",
            })

    return sorted(data, key=lambda x: x["timestamp"])


def detect_burst_candidates(performance):
    """检测早期爆款候选 (FR-TK-015)"""
    candidates = []
    by_video = {}
    for p in performance:
        vid = p["video_id"]
        if vid not in by_video:
            by_video[vid] = []
        by_video[vid].append(p)

    for vid, entries in by_video.items():
        if len(entries) < 2:
            continue
        first = entries[-1]
        last = entries[0]
        hours_span = (datetime.fromisoformat(last["timestamp"]) - datetime.fromisoformat(first["timestamp"])).total_seconds() / 3600
        if hours_span < 1:
            continue
        view_growth = (last["views"] - first["views"]) / max(first["views"], 1) * 100
        if view_growth > 200:
            candidates.append({
                "video_id": vid,
                "product": first["product"],
                "growth_rate": round(view_growth, 1),
                "prediction": "🔥 可能成为爆款" if view_growth > 500 else "📈 有增长潜力",
                "confidence": min(round(view_growth / 500 * 100), 95),
            })

    return candidates


def main():
    print(f"🚀 [MS-4] 发布与追踪开始 — {datetime.now().isoformat()} (模拟模式)")

    scripts = load_content_scripts()
    if not scripts:
        print("⚠️  无脚本数据，使用默认产品")
        scripts = [{"product": "防水手机袋", "target_country": "TH"}]

    publish_results = simulate_publish(scripts)
    performance = generate_performance_data(publish_results)
    burst_candidates = detect_burst_candidates(performance)

    output = {
        "task_id": TASK_ID, "milestone": MILESTONE_ID,
        "publish_status": publish_results,
        "performance_data": performance,
        "burst_candidates": burst_candidates,
        "mode": "simulated",
        "generated_at": datetime.now().isoformat(),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pub_path = OUTPUT_DIR / f"publish_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    perf_path = OUTPUT_DIR / f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    pub_path.write_text(json.dumps(output["publish_status"], ensure_ascii=False, indent=2))
    perf_path.write_text(json.dumps(output["performance_data"], ensure_ascii=False, indent=2))

    update_milestone(TASK_ID, MILESTONE_ID, "completed")

    print(f"✅ 发布完成: {len(publish_results)} 个视频 (模拟)")
    print(f"📊 数据: {len(performance)} 条表现记录")
    if burst_candidates:
        print(f"🔥 爆款候选: {len(burst_candidates)} 个")
        for b in burst_candidates:
            print(f"   {b['product']}: {b['prediction']} (置信度 {b['confidence']}%)")


if __name__ == "__main__":
    main()
