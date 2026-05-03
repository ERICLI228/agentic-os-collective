#!/usr/bin/env python3
"""v3.9: AI 回流重写后台执行器 — 子进程独立运行，不受 Flask 阻塞"""
import sys, os, json, time
from pathlib import Path

SELF_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SELF_DIR))
sys.path.insert(0, str(SELF_DIR / "core"))

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(SELF_DIR.parent / ".env")
except ImportError:
    pass

from script_manager import (
    get_episode_detail_rich, build_rewrite_prompt,
    parse_ai_storyboard, rewrite_episode_to_json, compute_dialogue_stats
)


def run_rewrite(task_id, episodes, feedback_type, feedback_desc):
    task_file = Path.home() / ".agentic-os" / "rewrite_tasks" / f"{task_id}.json"
    results = []
    done_count = 0
    fail_count = 0

    for ep_num in episodes:
        ep_str = str(ep_num).zfill(2)
        detail = get_episode_detail_rich(ep_str)
        if not detail:
            results.append({"episode": ep_str, "status": "error", "error": "Episode not found"})
            fail_count += 1
            continue

        original_sb = detail.get("storyboard", [])
        original_stats = compute_dialogue_stats(original_sb)
        ep_title = detail.get("title", "EP" + ep_str)

        prompt = build_rewrite_prompt(original_sb, ep_title, feedback_type, feedback_desc)

        ai_result = None
        ai_error = None
        try:
            from adversarial_review import LLMClient
            client = LLMClient("coding/qwen3.6-plus")
            ai_response = client.call(prompt["system"], prompt["user"], temperature=0.7, max_tokens=8192)
            ai_result = parse_ai_storyboard(ai_response)
        except RuntimeError as e:
            ai_error = "AI Key未配置: " + str(e)
        except Exception as e:
            ai_error = "AI调用失败: " + str(e)[:200]

        if ai_result and ai_result.get("storyboard") and not ai_result.get("errors"):
            new_sb = ai_result["storyboard"]
            shot_count = rewrite_episode_to_json(ep_title, new_sb)
            new_stats = compute_dialogue_stats(new_sb)
            changes = []
            if len(new_sb) != len(original_sb):
                changes.append(f"镜数: {len(original_sb)} -> {len(new_sb)}")
            if new_stats["classical_pct"] != original_stats["classical_pct"]:
                changes.append(f"古典比: {original_stats['classical_pct']}% -> {new_stats['classical_pct']}%")
            if new_stats["total_chars"] != original_stats["total_chars"]:
                changes.append(f"总字数: {original_stats['total_chars']} -> {new_stats['total_chars']}")
            results.append(dict(episode=ep_str, title=ep_title, status="done",
                shots=shot_count, original_shots=len(original_sb),
                classical_pct=new_stats["classical_pct"], modern_pct=new_stats["modern_pct"],
                original_classical_pct=original_stats["classical_pct"],
                original_modern_pct=original_stats["modern_pct"],
                total_chars=new_stats["total_chars"], changes=changes, ai_error=None))
            done_count += 1
        else:
            results.append(dict(episode=ep_str, title=ep_title, status="mock",
                error=ai_error, mock=True,
                note="AI调用失败，请检查CODING_API_KEY环境变量或网络连接"))
            fail_count += 1

    task_data = {
        "task_id": task_id,
        "episodes": episodes,
        "feedback_type": feedback_type,
        "feedback_desc": feedback_desc,
        "status": "completed",
        "results": results,
        "total": len(results),
        "done": done_count,
        "failed": fail_count,
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    with open(task_file, "w") as f:
        json.dump(task_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--task-id", required=True)
    p.add_argument("--episodes", required=True)
    p.add_argument("--feedback-type", default="其他")
    p.add_argument("--feedback-desc", default="")
    args = p.parse_args()

    episodes = [int(x) for x in args.episodes.split(",") if x.strip()]
    run_rewrite(args.task_id, episodes, args.feedback_type, args.feedback_desc)
