#!/usr/bin/env python3
"""
短剧角色设计器 — Sprint 3.1

调用 AutoGLM / SiliconFlow 生成角色三视图（正面/侧面/背面），
输出 character_designs.json。

流程:
  1. 从 stories/*.yaml 读取角色列表
  2. 为每个角色生成 prompt
  3. 调用 AutoGLM image generation 生成三视图
  4. 保存 character_designs.json

用法:
  python3 drama/openclaw/core/role_designer.py                  # 全部角色
  python3 drama/openclaw/core/role_designer.py --characters 武松,鲁智深  # 指定角色
  python3 drama/openclaw/core/role_designer.py --mock            # Mock 模式
  python3 drama/openclaw/core/role_designer.py --story shuihuzhuan
"""

import json
import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ── 路径 ──
STORIES_DIR = Path(__file__).resolve().parents[3] / "stories"
OUTPUT_DIR = Path.home() / ".agentic-os" / "character_designs"
OUTPUT_FILE = OUTPUT_DIR / "character_designs.json"

# ── 角色风格预设 ──
CHARACTER_PROFILES = {
    "水浒传": {
        "era": "Song Dynasty China",
        "style": "wuxia, realistic digital art, dramatic lighting",
        "clothing": "traditional Chinese martial arts clothing",
        "characters": {
            "武松": {
                "description": "tall muscular man, heroic expression, tiger-skill warrior",
                "props": "carries a staff, tiger-killing hero",
                "face": "strong jaw, determined eyes, masculine",
            },
            "鲁智深": {
                "description": "burly bald monk with tattoos, fierce but kind-hearted",
                "props": "Buddhist prayer beads, monk robe, iron staff",
                "face": "round face, thick eyebrows, wild beard",
            },
            "林冲": {
                "description": "elegant swordsman, refined but deadly warrior",
                "props": "long sword, panther-head spear",
                "face": "handsome, calm expression, scholar-warrior",
            },
            "宋江": {
                "description": "charismatic leader, middle-aged, authoritative",
                "props": "leadership robes, command flag",
                "face": "square face, kind but firm eyes",
            },
            "李逵": {
                "description": "fierce wild warrior, dark skin, axe-wielding berserker",
                "props": "twin axes, rough clothing",
                "face": "dark skin, wild hair, fierce expression",
            },
            "吴用": {
                "description": "strategic advisor, scholar appearance, cunning",
                "props": "feather fan, scroll, scholar robes",
                "face": "thin face, sharp eyes, goatee",
            },
        },
    },
}


def load_story_characters(story_name: str = "shuihuzhuan") -> List[Dict]:
    """从 YAML 故事文件读取角色列表"""
    import yaml
    story_file = STORIES_DIR / f"{story_name}.yaml"
    if not story_file.exists():
        print(f"⚠️ 故事文件不存在: {story_file}")
        return []

    with open(story_file) as f:
        data = yaml.safe_load(f)

    # 提取去重角色
    characters = set()
    for ep in data.get("episodes", []):
        if ep.get("character"):
            characters.add(ep["character"])

    return sorted(characters)


def build_three_view_prompt(name: str, profile: Dict, era: str, style: str) -> str:
    """构建三视图生成 prompt"""
    return (
        f"Character three-view design sheet: {name}. "
        f"Three poses side by side: front view, side view, back view. "
        f"Setting: {era}. Style: {style}. "
        f"Appearance: {profile['description']}. "
        f"Props: {profile['props']}. "
        f"Face: {profile['face']}. "
        f"White background, clean character design reference sheet, "
        f"consistent proportions across all three views, professional concept art."
    )


def generate_image(prompt: str, output_path: str, mock: bool = False) -> Dict:
    """
    调用图像生成 API 生成角色三视图

    支持:
      1. SiliconFlow (wanx2.1-t2i-turbo / stable-diffusion)
      2. AutoGLM image endpoint
      3. Mock 模式 (生成占位符)
    """
    if mock:
        # Mock 模式: 生成占位记录
        return {
            "status": "mock",
            "prompt": prompt,
            "output_path": output_path,
            "image_url": None,
            "generated_at": datetime.now().isoformat(),
            "note": "Mock mode - no actual image generated",
        }

    api_key = os.environ.get("SILICONFLOW_API_KEY", os.environ.get("CODING_API_KEY", ""))
    if not api_key:
        return {
            "status": "error",
            "error": "Missing SILICONFLOW_API_KEY or CODING_API_KEY in environment",
        }

    # SiliconFlow 文本生成图像 API
    try:
        import requests

        url = "https://api.siliconflow.cn/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": prompt,
            "image_size": "1024x768",
            "num_images": 1,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        # 保存图像
        img_data = data.get("data", [])
        if img_data:
            img_url = img_data[0].get("url")
            if img_url:
                # 下载保存
                img_resp = requests.get(img_url, timeout=30)
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                return {
                    "status": "success",
                    "prompt": prompt,
                    "output_path": output_path,
                    "image_url": img_url,
                    "generated_at": datetime.now().isoformat(),
                }
            else:
                # base64 格式
                b64 = img_data[0].get("b64_json")
                if b64:
                    import base64
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(base64.b64decode(b64))
                    return {
                        "status": "success",
                        "prompt": prompt,
                        "output_path": output_path,
                        "image_url": None,
                        "generated_at": datetime.now().isoformat(),
                    }

        return {
            "status": "failed",
            "error": "No image data returned",
            "response": str(data),
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "prompt": prompt,
        }


def design_character(
    name: str,
    story: str = "水浒传",
    mock: bool = False,
) -> Dict:
    """为单个角色生成三视图设计"""
    story_data = CHARACTER_PROFILES.get(story, {})
    era = story_data.get("era", "ancient China")
    style = story_data.get("style", "wuxia digital art")
    profile = story_data.get("characters", {}).get(name, {})

    if not profile:
        return {
            "name": name,
            "status": "error",
            "error": f"No profile for {name} in {story}",
        }

    prompt = build_three_view_prompt(name, profile, era, style)
    output_path = str(OUTPUT_DIR / f"{name}_three_view.png")

    print(f"  🎨 生成 {name} 三视图...")
    result = generate_image(prompt, output_path, mock=mock)

    return {
        "name": name,
        "story": story,
        "profile": profile,
        "prompt": prompt,
        "generation": result,
        "created_at": datetime.now().isoformat(),
    }


def main():
    mock = "--mock" in sys.argv
    story = "shuihuzhuan"
    characters = None

    # 解析参数
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--mock":
            mock = True
            i += 1
        elif sys.argv[i] == "--story" and i + 1 < len(sys.argv):
            story = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--characters" and i + 1 < len(sys.argv):
            characters = sys.argv[i + 1].split(",")
            i += 2
        else:
            i += 1

    story_title = story.replace("shuihuzhuan", "水浒传").replace("sanguo", "三国").replace("xiyou", "西游")

    print(f"\n{'='*60}")
    print(f"  角色设计器 | {story_title} | {'Mock' if mock else 'Real'}")
    print(f"{'='*60}\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 加载角色
    if characters:
        char_list = characters
    else:
        char_list = load_story_characters(story)
        if not char_list:
            char_list = list(CHARACTER_PROFILES.get(story_title, {}).get("characters", {}).keys())

    if not char_list:
        print("❌ 无角色数据")
        return

    print(f"📋 待设计角色: {len(char_list)}")
    for c in char_list:
        print(f"  - {c}")
    print()

    # 逐个生成
    designs = []
    for name in char_list:
        result = design_character(name, story=story_title, mock=mock)
        designs.append(result)

        status = result.get("generation", {}).get("status", "unknown")
        if status == "success":
            path = result["generation"].get("output_path", "?")
            print(f"  ✅ {name} → {path}")
        elif status == "mock":
            print(f"  🧪 {name} → Mock (跳过实际生成)")
        else:
            error = result.get("generation", {}).get("error", "unknown")
            print(f"  ❌ {name} → {error}")

    # 输出 JSON
    output = {
        "project": story_title,
        "generated_at": datetime.now().isoformat(),
        "mode": "mock" if mock else "real",
        "total": len(designs),
        "characters": designs,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n📄 设计文件: {OUTPUT_FILE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
