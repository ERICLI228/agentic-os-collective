#!/usr/bin/env python3
"""v3.9c: AI 回流重写后台执行器 — 子进程独立运行 + auto-retry质量门 + version_history"""
import sys, os, json, time
from pathlib import Path

SELF_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SELF_DIR))
sys.path.insert(0, str(SELF_DIR / "core"))

try:
    from dotenv import load_dotenv
    load_dotenv(SELF_DIR.parent / ".env")
except ImportError:
    pass

from script_manager import (
    get_episode_detail_rich, build_rewrite_prompt,
    parse_ai_storyboard, rewrite_episode_to_json, compute_dialogue_stats
)


def add_version_history(ep_title, sb_before, sb_after, feedback_type, feedback_desc):
    """v3.9c: 在 episode_templates.json 的 _version_history 中记录变更"""
    ep_data_path = SELF_DIR / "episode_templates.json"
    templates = {}
    if ep_data_path.exists():
        templates = json.loads(ep_data_path.read_text(encoding="utf-8"))
    history = templates.get("_version_history", [])
    entry = {
        "episode": ep_title,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "feedback_type": feedback_type,
        "feedback_desc": feedback_desc,
        "shots_before": len(sb_before),
        "shots_after": len(sb_after),
        "changes": {
            "shots_delta": len(sb_after) - len(sb_before),
            "before_stats": compute_dialogue_stats(sb_before),
            "after_stats": compute_dialogue_stats(sb_after)
        }
    }
    history.append(entry)
    if len(history) > 50:
        history = history[-50:]
    templates["_version_history"] = history
    ep_data_path.write_text(json.dumps(templates, ensure_ascii=False, indent=2), encoding="utf-8")


def quality_check(storyboard, original_sb):
    """v3.9c: 质量门槛 — 检查镜数、对白密度、字段完整性"""
    issues = []
    if len(storyboard) < len(original_sb) + 1:
        issues.append("镜数未增加(原" + str(len(original_sb)) + "→" + str(len(storyboard)) + ")")
    for shot in storyboard:
        dia = shot.get("dialogue", [])
        if not dia:
            issues.append(shot.get("shot_label", "?") + " 无对白")
        for d in dia:
            if not d.get("voice_dir"):
                issues.append(shot.get("shot_label", "?") + " " + d.get("speaker", "") + " 缺voice_dir")
            if not d.get("emotion_mark"):
                issues.append(shot.get("shot_label", "?") + " " + d.get("speaker", "") + " 缺emotion_mark")
        if not shot.get("camera_script") or len(shot.get("camera_script", "")) < 10:
            issues.append(shot.get("shot_label", "?") + " camera_script过短")
    classical = sum(1 for s in storyboard for d in s.get("dialogue", []) if d.get("style") == "classical")
    if classical < 2:
        issues.append("classical对白不足2条(当前" + str(classical) + ")")
    return issues


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

        # Write running status
        task_data = {"task_id": task_id, "status": "running",
            "episode_current": ep_title,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with open(task_file, "w") as f:
            json.dump(task_data, f, ensure_ascii=False)

        # ===== AI call with auto-retry (max 2 retries) =====
        max_retries = 2
        final_sb = None
        final_error = None

        for attempt in range(max_retries + 1):
            if attempt > 0:
                time.sleep(3)

            prompt = build_rewrite_prompt(original_sb, ep_title, feedback_type,
                (feedback_desc or "") + (" [自动重试第" + str(attempt) + "次]" if attempt > 0 else ""))

            ai_result = None
            ai_error = None
            try:
                from adversarial_review import LLMClient
                client = LLMClient("coding/qwen3.6-plus")
                ai_response = client.call(prompt["system"], prompt["user"], temperature=0.7, max_tokens=8192)
                ai_result = parse_ai_storyboard(ai_response)
            except RuntimeError as e:
                ai_error = "AI Key未配置: " + str(e)
                break  # No point retrying without key
            except Exception as e:
                ai_error = "AI调用失败: " + str(e)[:150]
                if attempt < max_retries:
                    continue  # Retry on connection errors
                break

            if ai_result and ai_result.get("storyboard") and not ai_result.get("errors"):
                new_sb = ai_result["storyboard"]
                issues = quality_check(new_sb, original_sb)

                if not issues or attempt >= max_retries:
                    final_sb = new_sb
                    break
                else:
                    # Retry with specific issues
                    feedback_desc = (feedback_desc or "") + " [质量检查不通过:" + ",".join(issues[:3]) + "]"
                    if attempt < max_retries:
                        continue
            else:
                if attempt < max_retries:
                    continue
                final_error = ai_error

        final_error = ai_error or ""

        # ===== Save result =====
        if final_sb:
            shot_count = rewrite_episode_to_json(ep_title, final_sb)
            new_stats = compute_dialogue_stats(final_sb)
            add_version_history(ep_title, original_sb, final_sb, feedback_type, feedback_desc)

            changes = []
            if len(final_sb) != len(original_sb):
                changes.append(f"镜数: {len(original_sb)} -> {len(final_sb)}")
            if new_stats["classical_pct"] != original_stats["classical_pct"]:
                changes.append(f"古典比: {original_stats['classical_pct']}% -> {new_stats['classical_pct']}%")
            if new_stats["total_chars"] != original_stats["total_chars"]:
                changes.append(f"总字数: {original_stats['total_chars']} -> {new_stats['total_chars']}")

            results.append(dict(episode=ep_str, title=ep_title, status="done",
                shots=shot_count, original_shots=len(original_sb),
                classical_pct=new_stats["classical_pct"], modern_pct=new_stats["modern_pct"],
                original_classical_pct=original_stats["classical_pct"],
                original_modern_pct=original_stats["modern_pct"],
                total_chars=new_stats["total_chars"], changes=changes,
                ai_error=None, retries_used=min(max_retries, attempt)))
            done_count += 1
        else:
            results.append(dict(episode=ep_str, title=ep_title, status="mock",
                error=final_error, mock=True,
                note="AI不可用(已尝试" + str(max_retries + 1) + "次)，请检查网络和API Key"))
            fail_count += 1

    task_data = {
        "task_id": task_id, "episodes": episodes,
        "feedback_type": feedback_type, "feedback_desc": feedback_desc,
        "status": "completed", "results": results,
        "total": len(results), "done": done_count, "failed": fail_count,
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
