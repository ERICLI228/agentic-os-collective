#!/usr/bin/env python3
"""
完播率追踪器 — v3.5 Sprint 4.2 (FR-DR-010)

追踪 AI 短剧每集完播率数据:
  1. 记录每集发布后的播放数据
  2. 计算完播率 (完成率 = 完整播放次数 / 总播放次数)
  3. 识别流失节点 (用户在哪个时间点退出最多)
  4. 生成趋势报告和优化建议

输入:
  - playback_logs.json (播放日志)
  - 或从 TK Seller Center API 拉取

输出:
  - completion_report.json

用法:
  python3 shared/core/completion_tracker.py --test
  python3 shared/core/completion_tracker.py --input playback_logs.json
"""

import json, sys
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

OUTPUT_DIR = Path.home() / ".agentic-os" / "completion_tracking"


@dataclass
class EpisodeCompletion:
    """单集完播数据"""
    episode_id: str
    episode_title: str
    duration_seconds: int
    total_plays: int
    full_completions: int
    completion_rate: float       # 完播率 %
    avg_watch_time: float        # 平均观看时长 (秒)
    drop_off_points: List[Dict]  # 流失节点 [{time: x, users: y}]
    trend: str                   # "上升"/"下降"/"持平"
    benchmark: str               # "优秀(>60%)" / "达标(40-60%)" / "偏低(<40%)"


@dataclass
class CompletionReport:
    """完播率总报告"""
    generated_at: str
    series_name: str
    total_episodes: int
    avg_completion_rate: float
    best_episode: str
    worst_episode: str
    episodes: List[EpisodeCompletion]
    recommendations: List[str]


def calculate_completion_rate(full_completions: int, total_plays: int) -> float:
    """计算完播率"""
    if total_plays == 0:
        return 0.0
    return round((full_completions / total_plays) * 100, 1)


def classify_benchmark(rate: float) -> str:
    """完播率评级"""
    if rate >= 60:
        return "优秀(>60%)"
    elif rate >= 40:
        return "达标(40-60%)"
    else:
        return "偏低(<40%)"


def analyze_drop_off(playback_data: List[Dict], duration: int) -> List[Dict]:
    """分析流失节点"""
    if not playback_data:
        return []

    # 按 25% 间隔分段
    segments = [0, 0.25, 0.5, 0.75, 1.0]
    drop_offs = []
    for i in range(len(segments) - 1):
        start = segments[i] * duration
        end = segments[i + 1] * duration
        exits = sum(1 for p in playback_data if start <= p.get("exit_time", 0) < end)
        drop_offs.append({
            "segment": f"{int(segments[i]*100)}-{int(segments[i+1]*100)}%",
            "exits": exits,
            "percentage": round(exits / len(playback_data) * 100, 1) if playback_data else 0,
        })
    return drop_offs


def track_episode(episode: dict) -> EpisodeCompletion:
    """追踪单集完播数据"""
    total_plays = episode.get("total_plays", 0)
    full_completions = episode.get("full_completions", 0)
    duration = episode.get("duration_seconds", 60)
    playback = episode.get("playback_logs", [])

    rate = calculate_completion_rate(full_completions, total_plays)
    avg_watch = episode.get("avg_watch_time", duration * rate / 100)
    drop_offs = analyze_drop_off(playback, duration)

    return EpisodeCompletion(
        episode_id=episode.get("id", ""),
        episode_title=episode.get("title", ""),
        duration_seconds=duration,
        total_plays=total_plays,
        full_completions=full_completions,
        completion_rate=rate,
        avg_watch_time=round(avg_watch, 1),
        drop_off_points=drop_offs,
        trend=episode.get("trend", "持平"),
        benchmark=classify_benchmark(rate),
    )


def generate_report(episodes: List[dict], series_name: str = "水浒传") -> CompletionReport:
    """生成完播率报告"""
    tracked = [track_episode(ep) for ep in episodes]
    rates = [e.completion_rate for e in tracked]
    avg_rate = sum(rates) / len(rates) if rates else 0

    best = max(tracked, key=lambda e: e.completion_rate) if tracked else None
    worst = min(tracked, key=lambda e: e.completion_rate) if tracked else None

    # 生成建议
    recommendations = []
    if avg_rate < 40:
        recommendations.append("整体完播率偏低，建议缩短单集时长至 60-90 秒")
    if best:
        recommendations.append(f"标杆集 #{best.episode_id} ({best.episode_title}) 完播率 {best.completion_rate}%，分析其节奏特征")
    if worst:
        recommendations.append(f"问题集 #{worst.episode_id} ({worst.episode_title}) 完播率 {worst.completion_rate}%，检查流失节点")

    # 检查前 25% 流失
    high_early_drop = [e for e in tracked if e.drop_off_points and
                       e.drop_off_points[0].get("percentage", 0) > 30]
    if high_early_drop:
        recommendations.append(f"发现 {len(high_early_drop)} 集在开头 25% 流失率>30%，需优化开场钩子")

    return CompletionReport(
        generated_at=datetime.now().isoformat(),
        series_name=series_name,
        total_episodes=len(tracked),
        avg_completion_rate=round(avg_rate, 1),
        best_episode=f"{best.episode_title} ({best.completion_rate}%)" if best else "N/A",
        worst_episode=f"{worst.episode_title} ({worst.completion_rate}%)" if worst else "N/A",
        episodes=tracked,
        recommendations=recommendations,
    )


def save_report(report: CompletionReport) -> Path:
    """保存报告"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    data = asdict(report)
    # 转换 dataclass 为 dict
    data["episodes"] = [asdict(e) for e in report.episodes]
    with open(output_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_file


def main():
    if "--test" in sys.argv:
        print("=" * 60)
        print("  完播率追踪器 — Mock 测试")
        print("=" * 60)

        mock_episodes = [
            {
                "id": "EP01", "title": "武松打虎", "duration_seconds": 90,
                "total_plays": 5000, "full_completions": 3200,
                "avg_watch_time": 68,
                "playback_logs": [
                    {"exit_time": 10, "user_id": "u1"}, {"exit_time": 15, "user_id": "u2"},
                    {"exit_time": 30, "user_id": "u3"}, {"exit_time": 85, "user_id": "u4"},
                    {"exit_time": 90, "user_id": "u5"},
                ],
                "trend": "上升",
            },
            {
                "id": "EP02", "title": "鲁智深倒拔垂杨柳", "duration_seconds": 85,
                "total_plays": 4200, "full_completions": 2100,
                "avg_watch_time": 52,
                "playback_logs": [
                    {"exit_time": 8, "user_id": "u1"}, {"exit_time": 12, "user_id": "u2"},
                    {"exit_time": 20, "user_id": "u3"}, {"exit_time": 80, "user_id": "u4"},
                ],
                "trend": "持平",
            },
            {
                "id": "EP03", "title": "林冲雪夜上梁山", "duration_seconds": 95,
                "total_plays": 3800, "full_completions": 1200,
                "avg_watch_time": 38,
                "playback_logs": [
                    {"exit_time": 5, "user_id": "u1"}, {"exit_time": 8, "user_id": "u2"},
                    {"exit_time": 15, "user_id": "u3"}, {"exit_time": 25, "user_id": "u4"},
                ],
                "trend": "下降",
            },
        ]

        report = generate_report(mock_episodes, series_name="水浒传")

        print(f"\n📊 《{report.series_name}》完播率报告:\n")
        print(f"  总集数: {report.total_episodes}")
        print(f"  平均完播率: {report.avg_completion_rate}%")
        print(f"  最佳: {report.best_episode}")
        print(f"  最差: {report.worst_episode}")
        print()

        for ep in report.episodes:
            icon = {"优秀(>60%)": "🌟", "达标(40-60%)": "✅", "偏低(<40%)": "⚠️"}[ep.benchmark]
            print(f"  {icon} EP{ep.episode_id}: {ep.episode_title}")
            print(f"     完播率: {ep.completion_rate}% | 平均观看: {ep.avg_watch_time}s/{ep.duration_seconds}s")
            drop_info = ', '.join(f"{d['segment']}({d['percentage']}%)" for d in ep.drop_off_points)
            print(f"     流失节点: {drop_info}")
            print()

        if report.recommendations:
            print("  💡 优化建议:")
            for r in report.recommendations:
                print(f"    - {r}")

        output_file = save_report(report)
        print(f"\n✅ 报告: {output_file}")
        return

    # 正常模式
    data_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--input" and i + 1 < len(sys.argv):
            data_path = Path(sys.argv[i + 1])

    if not data_path or not data_path.exists():
        print(f"⚠️ 数据文件不存在: {data_path}")
        print("使用 --test 运行 Mock 测试")
        sys.exit(1)

    with open(data_path) as f:
        data = json.load(f)

    episodes = data.get("episodes", data)
    series = data.get("series_name", "水浒传")
    report = generate_report(episodes, series_name=series)
    output_file = save_report(report)
    print(f"✅ Report saved: {output_file}")


if __name__ == "__main__":
    main()
