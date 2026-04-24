#!/usr/bin/env python3
"""
剧本筛选与精华提取系统 (多故事支持 v2.0)
基于 story 配置的 episodes 进行智能筛选
"""
import os, sys, json, urllib.request, argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config
from shared.story_loader import load_story, list_available

ARK_API_KEY = config.ARK_API_KEY
GLM_MODEL = "glm-4-7-251222"
API_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

def call_glm(prompt: str) -> str:
    """调用 GLM-4.7 API (直连，无代理)"""
    data = {
        "model": GLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深编剧，熟悉水浒传原著和现代观众审美。请基于以下标准进行剧本筛选和改编。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        req = urllib.request.Request(
            API_ENDPOINT,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {ARK_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        resp = urllib.request.urlopen(req, timeout=60)
        body = json.loads(resp.read().decode('utf-8'))
        return body.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"GLM API 调用失败: {e}")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

STORY = None  # 由 main() 设置

def select_best_chapters(story, top_n: int = 10) -> list:
    """剧本筛选：基于 story 配置的 episodes 评分排序"""
    print(f"📊 [{story.name}] 剧本筛选...")
    print("=" * 50)

    scored = []
    for ep in story.episodes:
        ch = {"title": ep.title, "chapter": ep.chapter, "character": ep.character,
              "tags": ep.tags, "score": ep.score * 10}
        ch["needs_rewrite"] = "需改编" in ep.tags
        scored.append(ch)

    scored.sort(key=lambda x: x["score"], reverse=True)
    for i, ch in enumerate(scored[:top_n], 1):
        status = "⚠️需改编" if ch["needs_rewrite"] else "✅可用"
        print(f"{i}. 第{ch['chapter']}回 {ch['title']} [{ch['character']}] 评分:{ch['score']:.0f} {status}")
    return scored[:top_n]


def generate_episode_list(story) -> dict:
    best = select_best_chapters(story, 10)
    return {
        "story": story.id,
        "version": "v2.0",
        "selection_criteria": story.selection_criteria,
        "episodes": [
            {"episode_number": i, "title": ch["title"], "chapter": ch["chapter"],
             "main_character": ch["character"], "score": ch["score"],
             "needs_rewrite": ch["needs_rewrite"],
             "status": "pending" if ch["needs_rewrite"] else "ready"}
            for i, ch in enumerate(best, 1)
        ]
    }


def save_episode_list(story, output_path: str = None):
    if output_path is None:
        output_path = str(Path.home() / f".openclaw/skills/water-margin-drama/episode_list_{story.id}.json")
    data = generate_episode_list(story)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ [{story.name}] 剧集列表已保存: {output_path}")
    return output_path


def main():
    stories_avail = ", ".join(list_available())
    parser = argparse.ArgumentParser(description=f"剧本筛选系统 (可用: {stories_avail})")
    parser.add_argument("--story", default="shuihuzhuan", help=f"故事 ID (默认 shuihuzhuan)")
    parser.add_argument("action", nargs="?", choices=["select", "list", "analyze"],
                        help="select (评分排序) | list (生成JSON) | analyze (GLM深度分析)")
    args = parser.parse_args()

    story = load_story(args.story)
    action = args.action or "select"

    if action == "select":
        select_best_chapters(story)
    elif action == "list":
        save_episode_list(story)
    elif action == "analyze":
        criteria_text = "\n".join(f"{k}: {v}" for k, v in story.selection_criteria.items())
        prompt = f"请分析{story.name}原著，基于以下标准提取最适合制作AI短剧的20个章节：\n{criteria_text}\n请按优先级排序，输出JSON列表。"
        print(f"🤖 [{story.name}] 调用 GLM 深度分析...")
        result = call_glm(prompt)
        if result:
            print(result)


if __name__ == "__main__":
    main()