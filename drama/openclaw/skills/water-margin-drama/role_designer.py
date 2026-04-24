import sys
from pathlib import Path
#!/usr/bin/env python3
"""
角色设计系统 (多故事支持 v2.0)
从 story 配置加载角色库，生成定妆照提示词与视频提示词
"""
import os, sys, json, base64, argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config
from shared.story_loader import load_story, list_available

ARK_API_KEY = config.ARK_API_KEY
SEEDANCE_MODEL = "doubao-seedance-2-0-fast-260128"
SEEDANCE_IMAGE_API = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

STORY = None  # 由 main() 设置

def generate_role_prompt(role_name: str, scene: str = None, action: str = None) -> str:
    """
    生成完整的角色提示词
    """
    role = STORY.role(role_name)
    if not role:
        return None
    
    base = role["description"]
    
    if scene:
        scene_desc = STORY.scenes.get(scene, scene)
        base = f"{base}，场景：{scene_desc}"
    
    if action:
        base = f"{base}，动作：{action}"
    
    # 添加负面提示词避免问题
    negative = "distorted, messy, low quality, blurred, deformed face, extra limbs, watermark, text"
    
    return {
        "positive": base,
        "negative": negative,
        "role": role_name,
        "traits": role["traits"]
    }

def save_role_library(output_path: str = None):
    """
    保存角色库到JSON文件
    """
    if output_path is None:
        output_path = os.path.expanduser("~/.openclaw/skills/water-margin-drama/role_library.json")
    
    library = {
        "version": "v1.0",
        "roles": ROLES,
        "scenes": SCENES,
        "usage": {
            "generate_prompt": "generate_role_prompt(role_name, scene, action)",
            "ensure_consistency": "每次使用相同角色时，复用相同描述"
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(library, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 角色库保存: {output_path}")
    return output_path

def list_roles():
    """列出所有可用角色"""
    print(f"🎭 {STORY.name}角色库:")
    print("=" * 50)
    for r in STORY.roles():
        print(f"\n📌 {r.name}")
        print(f"   特征: {', '.join(r.traits)}")
        print(f"   描述: {r.description[:50]}...")
        print(f"   默认场景: {r.default_scene}")

    print("\n" + "=" * 50)
    print("📍 可用场景:")
    for name, desc in STORY.scenes.items():
        print(f"   - {name}: {desc[:30]}...")

def generate_character_image_prompt(role_name: str) -> str:
    """
    生成角色定妆照提示词（用于图像生成）
    """
    role = STORY.role(role_name)
    if not role:
        print(f"❌ 角色 '{role_name}' 不存在")
        return None
    
    prompt = f"""
请生成一张{role_name}的定妆照，用于后续AI视频生成的角色一致性参考。

角色描述：{role.description}

要求：
1. 正面照，表情自然
2. 服装和特征清晰可见
3. 电影质感，写实风格
4. 中景构图（能看到上半身和部分背景）
5. 场景：{role.default_scene}

负面提示词：distorted, messy, low quality, blurred, deformed face, extra limbs
"""
    return prompt.strip()

def batch_generate_prompts(output_dir: str = None):
    """
    批量生成所有角色的定妆照提示词
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/.openclaw/skills/water-margin-drama/character_prompts")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎭 批量生成角色定妆照提示词...")
    print("=" * 50)
    
    for role_name in [r.name for r in STORY.roles()]:
        prompt = generate_character_image_prompt(role_name)
        filepath = os.path.join(output_dir, f"{role_name}_定妆照.txt")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"✅ {role_name}: {filepath}")
    
    print("=" * 50)
    print(f"🎉 完成，共 {len(STORY.roles())} 个角色")

def get_video_prompt(role_name: str, scene: str, action: str) -> str:
    """
    生成视频提示词（用于Seedance）
    """
    prompt_data = generate_role_prompt(role_name, scene, action)
    if not prompt_data:
        return None
    
    video_prompt = f"""
{prompt_data['positive']}

电影质感，流畅动作，24帧，8秒视频。
负面：{prompt_data['negative']}
"""
    return video_prompt.strip()

def generate_image(role_name: str, output_dir: str = None) -> str:
    """
    调用 Seedance/ARK API 生成角色定妆照 (FR-DR-003)
    返回图片路径，失败返回空字符串
    """
    role = STORY.role(role_name)
    if not role:
        print(f"❌ 角色 '{role_name}' 不存在")
        return ""

    prompt = generate_character_image_prompt(role_name)
    if not prompt:
        return ""

    print(f"🖼️  生成 {role_name} 定妆照...")

    try:
        import urllib.request
        data = json.dumps({
            "model": SEEDANCE_MODEL,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }).encode('utf-8')
        req = urllib.request.Request(
            SEEDANCE_IMAGE_API,
            data=data,
            headers={"Authorization": f"Bearer {ARK_API_KEY}", "Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=120)
        body = json.loads(resp.read().decode('utf-8'))

        # 提取 base64 图片
        b64 = body.get("data", [{}])[0].get("b64_json", "")
        if not b64:
            print(f"⚠️  API 返回无图片数据")
            return ""

        if output_dir is None:
            output_dir = str(Path(__file__).parent / "output" / "characters")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = f"{output_dir}/{role_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        import base64
        Path(output_path).write_bytes(base64.b64decode(b64))
        print(f"✅ {role_name}: {output_path}")
        return output_path

    except Exception as e:
        print(f"⚠️  图像生成失败: {e}")
        return ""


def batch_generate_images(output_dir: str = None) -> dict:
    """批量生成所有角色的定妆照"""
    results = {}
    for role_name in [r.name for r in STORY.roles()]:
        path = generate_image(role_name, output_dir)
        results[role_name] = path
    return results


def main():
    stories_avail = ", ".join(list_available())
    parser = argparse.ArgumentParser(description=f"角色设计系统 (可用: {stories_avail})")
    parser.add_argument("--story", default="shuihuzhuan", help=f"故事 ID")
    parser.add_argument("action", nargs="?", choices=["list", "prompt", "image", "batch", "batch-img", "save"])
    parser.add_argument("extra", nargs="*", help="角色名等")
    args = parser.parse_args()

    global STORY
    STORY = load_story(args.story)

    if not args.action:
        parser.print_help()
        sys.exit(1)

    action = args.action

    if action == "list":
        list_roles()
    elif action == "prompt":
        role = args.extra[0] if args.extra else None
        if role:
            print(generate_character_image_prompt(role))
        else:
            print("用法: prompt 角色名")
    elif action == "batch":
        batch_generate_prompts()
    elif action == "batch-img":
        batch_generate_images()
    elif action == "image":
        role = args.extra[0] if args.extra else None
        if role:
            generate_image(role)
        else:
            print("用法: image 角色名")
    elif action == "save":
        save_role_library()

if __name__ == "__main__":
    main()