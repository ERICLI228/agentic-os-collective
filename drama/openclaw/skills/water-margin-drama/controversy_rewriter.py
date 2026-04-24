#!/usr/bin/env python3
"""
争议剧情改写系统 (多故事支持 v2.0)
基于广电总局AI魔改治理标准，自动改写争议内容
从 story 配置加载争议规则
"""
import os, sys, json, urllib.request, argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config
from shared.story_loader import load_story, list_available

ARK_API_KEY = config.ARK_API_KEY
GLM_MODEL = "glm-4-7-251222"

STORY = None  # 由 main() 设置

# 改写Prompt模板 (由 story 配置决定)
def story_rewrite_prompt():
    return STORY.rewrite_prompt if hasattr(STORY, 'rewrite_prompt') else f"""
你是一位资深编剧，熟悉现代观众审美和广电总局AI魔改治理要求。

请将以下{STORY.name}章节进行改编，要求：
1. **保留核心冲突和人物性格**
2. **删除或弱化原著中以下争议内容**：
   - 滥杀无辜、歧视女性、愚忠愚孝的情节
   - 过度血腥暴力的描写
3. **强化正面价值观**：
   - 反抗压迫、兄弟情义、替天行道
4. **对话口语化**，符合短视频节奏
5. **控制篇幅**：30-60秒短剧脚本

**原章节**: {chapter_title}
**主角**: {character}
**争议点**: {controversy}

请输出：
1. 改编后的30秒剧本（分镜表格格式）
2. 改编说明（改了什么、为什么）

输出格式：
```
【分镜表】
| 序号 | 景别 | 画面描述 | 台词/旁白 | 时长 |

【改编说明】
- 删除了...
- 新增了...
- 价值观调整为...
```
"""

def rewrite_chapter(chapter_title: str, character: str, controversy: str) -> str:
    """
    调用GLM改写争议章节
    """
    prompt = REWRITE_PROMPT_TEMPLATE.format(
        chapter_title=chapter_title,
        character=character,
        controversy=controversy
    )
    
    print(f"🔄 改写章节: {chapter_title}")
    print(f"   主角: {character}")
    print(f"   争议点: {controversy}")
    print("-" * 50)

    data = {
        "model": GLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深编剧，熟悉现代观众审美和监管要求。请基于指导改写剧本。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    api_endpoint = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    try:
        req = urllib.request.Request(
            api_endpoint,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {ARK_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        resp = urllib.request.urlopen(req, timeout=60)
        body = json.loads(resp.read().decode('utf-8'))
        content = body.get('choices', [{}])[0].get('message', {}).get('content', '')
        if content:
            return content.strip()
        else:
            print("⚠️ API 返回空内容，使用手动改写模板")
            return generate_manual_rewrite(chapter_title, character, controversy)
    except Exception as e:
        print(f"⚠️ API 调用失败: {e}")
        return generate_manual_rewrite(chapter_title, character, controversy)
    except Exception as e:
        print(f"⚠️ 错误: {e}")
        return generate_manual_rewrite(chapter_title, character, controversy)

def generate_manual_rewrite(chapter_title: str, character: str, controversy: str) -> str:
    """
    手动生成改写模板（当API不可用时）
    """
    rule = CONTROVERSY_RULES.get(controversy, {})
    
    template = f"""
【分镜表】
| 序号 | 景别 | 画面描述 | 台词/旁白 | 时长 |
|------|------|----------|----------|------|
| 1 | 远景 | {character}出场 | 旁白：话说{character}... | 3秒 |
| 2 | 中景 | 面临困境 | {character}：这... | 5秒 |
| 3 | 近景 | 关键动作 | 动作场面 | 10秒 |
| 4 | 特写 | 情感升华 | {character}：为了兄弟！ | 5秒 |
| 5 | 全景 | 结局收尾 | 旁白：从此... | 5秒 |

【改编说明】
- 删除了：{rule.get('问题', '原争议内容')}
- 新增了：{rule.get('改写方向', '正面价值观')}
- 价值观调整：强调反抗压迫、兄弟情义

⚠️ 此为手动模板，建议审核后使用
"""
    return template

def batch_rewrite(chapters: list) -> dict:
    """
    批量改写争议章节
    """
    results = {
        "rewritten": [],
        "failed": []
    }
    
    for ch in chapters:
        if ch.get("needs_rewrite"):
            controversy = identify_controversy(ch["title"])
            rewritten = rewrite_chapter(ch["title"], ch["character"], controversy)
            
            if rewritten:
                results["rewritten"].append({
                    "chapter": ch["chapter"],
                    "title": ch["title"],
                    "rewritten_script": rewritten,
                    "status": "done"
                })
            else:
                results["failed"].append(ch)
    
    return results

def identify_controversy(title: str) -> str:
    """根据标题识别争议类型"""
    if "宋江" in title and ("招安" in title or "杀" in title):
        return "宋江招安"
    if "李逵" in title and ("杀" in title or "虎" in title):
        return "李逵滥杀"
    if "潘金莲" in title or "西门庆" in title:
        return "潘金莲"
    if "血溅" in title or "杀" in title:
        return "血腥暴力"
    return "封建糟粕"

def save_rewritten_scripts(output_dir: str = None):
    """保存改写后的剧本"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.openclaw/skills/water-margin-drama/scripts")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 需改写的章节列表
    need_rewrite = [
        {"chapter": 31, "title": "血溅鸳鸯楼", "character": "武松"},
        {"chapter": 43, "title": "李逵沂岭杀四虎", "character": "李逵"},
        {"chapter": 22, "title": "宋江杀阎婆惜", "character": "宋江"},
    ]
    
    print("🔄 批量改写争议章节...")
    print("=" * 50)
    
    for ch in need_rewrite:
        controversy = identify_controversy(ch["title"])
        rewritten = rewrite_chapter(ch["title"], ch["character"], controversy)
        
        filename = f"{ch['chapter']}_{ch['title']}_改编版.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {ch['title']} 改编版\n\n")
            f.write(f"**主角**: {ch['character']}\n\n")
            f.write(rewritten)
        
        print(f"✅ 保存: {filepath}")
    
    print("=" * 50)
    print(f"🎉 改写完成，共 {len(need_rewrite)} 个章节")

def main():
    stories_avail = ", ".join(list_available())
    parser = argparse.ArgumentParser(description=f"争议改写系统 (可用: {stories_avail})")
    parser.add_argument("--story", default="shuihuzhuan", help=f"故事 ID")
    parser.add_argument("action", nargs="?", choices=["list", "rewrite", "batch", "rules"])
    parser.add_argument("extra", nargs="*")
    args = parser.parse_args()

    global STORY
    STORY = load_story(args.story)

    if not args.action:
        parser.print_help()
        return

    action = args.action

    if action == "list":
        print(f"⚖️ [{STORY.name}] 争议规则:")
        print("=" * 50)
        for c in STORY.controversies:
            print(f"\n📌 {c.pattern} (严重度: {c.severity})")
            print(f"   问题: {c.problem}")
            print(f"   改写: {c.rewrite}")
            print(f"   保留: {c.keep}")

    elif action == "rules":
        print(f"⚖️ [{STORY.name}] 争议剧情改写规则:")
        for c in STORY.controversies:
            print(f"\n📌 {c.pattern} (严重度: {c.severity}): {c.problem}")

    elif action == "rewrite":
        title = args.extra[0] if args.extra else "武松打虎"
        character = args.extra[1] if len(args.extra) > 1 else "武松"
        controversy = identify_controversy(title)
        result = rewrite_chapter(title, character, controversy)
        print(result)

    elif action == "batch":
        save_rewritten_scripts()


if __name__ == "__main__":
    main()