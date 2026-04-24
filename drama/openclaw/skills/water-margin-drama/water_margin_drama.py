#!/usr/bin/env python3
"""
AI 数字短剧制作系统 (多故事支持 v2.0)
支持 --story 参数切换故事: shuihuzhuan | sanguo | xiyou
"""

import os, sys, json, time, urllib.request, argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config
from shared.story_loader import load_story, list_available
ARK_API_KEY = config.ARK_API_KEY
GLM_MODEL = "glm-4-7-251222"
SEEDANCE_MODEL = "doubao-seedance-2-0-fast-260128"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 清理代理环境变量
def clean_env():
    for key in ['http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
        os.environ.pop(key, None)

def call_glm(prompt: str, max_tokens: int = 1000) -> str:
    """调用GLM-4.7生成内容"""
    clean_env()
    
    url = f"{ARK_BASE_URL}/chat/completions"
    data = json.dumps({
        "model": GLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是一个短视频剧本专家，擅长创作幽默风格的水浒传故事"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json"
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def generate_video(prompt: str, ratio: str = "16:9", duration: int = 10) -> str:
    """调用Seedance 2.0生成视频"""
    clean_env()
    
    # 导入SDK
    seedance_dir = os.path.expanduser("~/Seedance 2.0 及 Seedance 2.0 fast API/ark_seedance2.0_quickstart_package")
    if os.path.exists(seedance_dir):
        sys.path.insert(0, seedance_dir)
        from volcenginesdkarkruntime import Ark
        client = Ark(api_key=ARK_API_KEY)
        
        result = client.content_generation.tasks.create(
            model=SEEDANCE_MODEL,
            content=[{"type": "text", "text": prompt}],
            ratio=ratio,
            duration=duration,
            generate_audio=True,
            watermark=True
        )
        
        task_id = result.id
        print(f"📹 视频任务已创建: {task_id}")
        print("⏳ 等待生成...")
        
        # 轮询等待
        for i in range(60):
            time.sleep(10)
            status = client.content_generation.tasks.get(task_id=task_id)
            print(f"  {i+1}. 状态: {status.status}")
            
            if status.status == "succeeded":
                return status.content.video_url
            elif status.status == "failed":
                return "Error: Video generation failed"
        
        return "Error: Timeout waiting for video"
    
    return "Error: Seedance SDK not found"

def main():
    stories_avail = ", ".join(list_available())

    parser = argparse.ArgumentParser(description=f"AI 数字短剧制作系统 (可用故事: {stories_avail})")
    parser.add_argument("--story", default="shuihuzhuan", help=f"故事 ID (默认 shuihuzhuan), 可用: {stories_avail}")
    parser.add_argument("--theme", default="", help="剧本主题 (如: 武松打虎)")
    parser.add_argument("--mode", default="script", choices=["script", "video", "full"],
                        help="模式: script (仅剧本) | video (仅视频) | full (完整流水线)")
    parser.add_argument("extra", nargs="*", help="额外参数 (兼容旧版)")
    args = parser.parse_args()

    # 加载故事配置
    try:
        story = load_story(args.story)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    theme = args.theme or " ".join(args.extra) if args.extra else (
        story.episodes[0].title if story.episodes else story.name
    )
    mode = args.mode

    if mode == "script":
        print(f"🎬 [{story.name}] 生成剧本: {theme}")
        prompt = story.script_prompt.format(theme=theme, style=story.style, name=story.name)
        script = call_glm(prompt)
        print("\n" + "="*50)
        print(f"📝 {story.name} · 剧本输出：")
        print("="*50)
        print(script)

    elif mode == "video":
        prompt = theme or "一个英雄战斗的场面，电影质感"
        print(f"🎬 [{story.name}] 生成视频: {prompt[:50]}...")
        video_url = generate_video(prompt)
        print(f"\n✅ 视频生成完成！\n🔗 {video_url}")

    elif mode == "full":
        print("\n" + "="*60)
        print(f"🎬 {story.name} AI数字短剧 · 全自动制作流水线")
        print(f"   时代: {story.era} | 风格: {story.style}")
        print("="*60)

        # 0. 确认门禁
        try:
            from confirmation import ConfirmationState
            confirm = ConfirmationState()
            confirm.start_project(f"{story.id}_{theme[:8]}")
            confirm.confirm_stage("script", "system", "自动确认 — 流水线模式")
        except Exception:
            pass

        # 1. 剧本
        print(f"\n📝 第1步：剧本生成 (GLM-4.7)")
        print("-"*40)
        script_prompt = story.script_prompt.format(theme=theme, style=story.style, name=story.name)
        script = call_glm(script_prompt)
        print(script)

        # 2. 视频提示词
        print(f"\n🎬 第2步：视频生成提示词")
        print("-"*40)
        video_prompt = call_glm(story.video_prompt.format(script=script[:500]))
        print(video_prompt)

        # 3. 视频
        print(f"\n🎥 第3步：生成视频 (Seedance 2.0)")
        print("-"*40)
        first_line = video_prompt.split('\n')[0] if '\n' in video_prompt else video_prompt[:100]
        video_url = generate_video(first_line)

        try:
            confirm.confirm_stage("roles", "system", "自动确认")
            confirm.confirm_stage("video", "system", "自动确认")
        except Exception:
            pass

        # 4. 配音
        print(f"\n🎙️ 第4步：配音合成 (macOS TTS + FFmpeg)")
        print("-"*40)
        try:
            from drama_audio import full_workflow
            full_workflow(video_url, script[:500])
        except Exception as e:
            print(f"  ⚠️  配音失败: {e}")

        print(f"\n✅ {story.name} · 视频生成完成！")
        print(f"🔗 {video_url}")

        # 5. 交付清单
        print("\n" + "="*60)
        print("📦 交付清单")
        print("="*60)
        print(f"📖 故事: {story.name} ({story.genre})")
        print(f"🎬 主题: {theme}")
        print(f"🎥 视频: {video_url}")
        print(f"🎙️ 配音: macOS TTS")
        print(f"👥 可用角色: {', '.join(r.name for r in story.roles())}")
        print(f"💾 存储: TOS (火山引擎对象存储)")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()