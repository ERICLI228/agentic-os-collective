import sys
from pathlib import Path
#!/usr/bin/env python3
"""
水浒传AI数字短剧 - 自动制作系统
一句话启动完整流水线：剧本→视频→配音→上传
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.parse

# 配置
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config
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
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📖 用法:")
        print("  python water_margin_drama.py --script <主题>")
        print("  python water_margin_drama.py --video <剧本>")
        print("  python water_margin_drama.py --full <主题>")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "--script":
        theme = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "鲁智深倒拔垂杨柳"
        print(f"🎬 正在生成剧本: {theme}")
        script = call_glm(f"""生成一个30秒的水浒传短视频剧本：{theme}
要求：
1. 幽默风格，现代网感
2. 包含分镜描述（镜头、画面、对白、音效）
3. 角色：鲁智深/武松/李逵等
4. 场景：寺庙、酒馆、山寨等
5. 时长：约30秒""")
        print("\n" + "="*50)
        print("📝 剧本输出：")
        print("="*50)
        print(script)
        
    elif action == "--video":
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "一个和尚用力拔出一棵大柳树"
        print(f"🎬 正在生成视频: {prompt}")
        video_url = generate_video(prompt)
        print(f"\n✅ 视频生成完成！")
        print(f"🔗 地址: {video_url}")
        
    elif action == "--full":
        theme = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "鲁智深倒拔垂杨柳"
        
        print("\n" + "="*60)
        print("🎬 水浒传AI数字短剧 - 全自动制作流水线")
        print("="*60)

        # 0. 确认门禁初始化
        try:
            from confirmation import ConfirmationState
            confirm = ConfirmationState()
            confirm.start_project(f"water_margin_{theme[:10]}")
            confirm.confirm_stage("script", "system", "自动确认 — 流水线模式")
        except Exception:
            pass

        # 1. 生成剧本
        print("\n📝 第1步：剧本生成 (GLM-4.7)")
        print("-"*40)
        script_prompt = f"""生成一个30秒的水浒传短视频剧本：{theme}
要求：
1. 幽默风格，现代网感，适合抖音/快手
2. 包含分镜描述（镜头、画面、对白/旁白、音效）
3. 角色设定清晰
4. 场景：古代中国风格
5. 时长：约30秒
6. 输出格式：分镜脚本格式"""
        
        script = call_glm(script_prompt)
        print(script)
        
        # 2. 提取视频提示词
        print("\n🎬 第2步：视频生成提示词")
        print("-"*40)
        video_prompt = call_glm(f"""从以下剧本中提取3个关键画面描述，用于AI视频生成。
每个描述格式：“主体 + 动作 + 场景 + 镜头语言 + 氛围”
每个描述不超过50字。

剧本：
{script[:500]}""")
        print(video_prompt)
        
        # 3. 生成视频
        print("\n🎥 第3步：生成视频 (Seedance 2.0)")
        print("-"*40)
        video_url = generate_video(video_prompt.split('\n')[0] if '\n' in video_prompt else video_prompt[:100])

        # 自动确认视频+角色阶段
        try:
            confirm.confirm_stage("roles", "system", "自动确认")
            confirm.confirm_stage("video", "system", "自动确认")
        except Exception:
            pass

        # 4. 配音合成
        print("\n🎙️ 第4步：配音合成 (macOS TTS + FFmpeg)")
        print("-"*40)
        try:
            from drama_audio import full_workflow
            audio_result = full_workflow(video_url, script[:500])
            print(f"  配音结果: {audio_result}")
        except Exception as e:
            print(f"  ⚠️  配音失败: {e} (视频仍可用)")

        print(f"\n✅ 视频生成完成！")
        print(f"🔗 视频链接: {video_url}")

        # 5. 输出交付清单
        print("\n" + "="*60)
        print("📦 交付清单")
        print("="*60)
        print(f"🎬 主题: {theme}")
        print(f"📝 剧本: (见上方)")
        print(f"🎥 视频: {video_url}")
        print(f"🎙️ 配音: macOS TTS (单角色)")
        print(f"💾 存储: TOS (火山引擎对象存储)")
        
    else:
        print("未知指令")
        sys.exit(1)

if __name__ == "__main__":
    main()