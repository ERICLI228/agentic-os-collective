#!/usr/bin/env python3
"""
ComfyUI 静态图渲染器 — v3.6
连接本地 ComfyUI → 生成 6角色×3分镜=18张角色图 → 升级Pillow字幕帧

用法:
  python3 shared/comfyui_renderer.py --character wusong     # 单个角色
  python3 shared/comfyui_renderer.py --episode 01            # 单集3镜
  python3 shared/comfyui_renderer.py --all                   # 全部18镜
  python3 shared/comfyui_renderer.py --test                  # 测试: 1张小图

输出: ~/.agentic-os/character_designs/renders/{character}/shot_{01-03}.png
"""
import json
import sys
import os
import time
import uuid
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path.home() / ".agentic-os" / "character_designs" / "renders"
VISUAL_BIBLE = Path.home() / ".agentic-os" / "character_designs" / "visual_bible.json"

# SDXL 9:16 竖屏 (TikTok/Reels 规格)
DEFAULT_WIDTH = 768
DEFAULT_HEIGHT = 1344
DEFAULT_STEPS = 25
DEFAULT_CFG = 7.5
DEFAULT_SEED = 42

QUALITY_SUFFIX = ", cinematic lighting, photorealistic, 8K, sharp focus, highly detailed, professional photography, 35mm film grain, warm color grade"


def load_visual_bible():
    if not VISUAL_BIBLE.exists():
        print(f"❌ 视觉圣经不存在: {VISUAL_BIBLE}")
        return None
    with open(VISUAL_BIBLE) as f:
        return json.load(f)


def queue_prompt(prompt_workflow):
    """提交 workflow 到 ComfyUI"""
    import urllib.request
    p = {"prompt": prompt_workflow, "client_id": f"agentic-os-{uuid.uuid4().hex[:8]}"}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request(f"{COMFYUI_URL}/prompt", data=data)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_history(prompt_id):
    """获取生成历史"""
    import urllib.request
    with urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}") as resp:
        return json.loads(resp.read())


def get_image(filename, subfolder="", folder_type="output"):
    """下载生成的图片"""
    import urllib.request
    params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    query = "&".join(f"{k}={v}" for k, v in params.items())
    with urllib.request.urlopen(f"{COMFYUI_URL}/view?{query}") as resp:
        return resp.read()


def build_sdxl_workflow(positive_prompt, negative_prompt="", seed=None, width=None, height=None, steps=None, cfg=None):
    """构建 SDXL 生成 workflow"""
    w = width or DEFAULT_WIDTH
    h = height or DEFAULT_HEIGHT
    s = seed if seed is not None else DEFAULT_SEED
    st = steps or DEFAULT_STEPS
    cf = cfg or DEFAULT_CFG

    pos = positive_prompt + QUALITY_SUFFIX
    neg = negative_prompt or "low quality, blurry, distorted, deformed, bad anatomy, ugly, watermark, text, signature, extra limbs, cartoon, anime, 3D render"

    return {
        "3": {"class_type": "KSampler", "inputs": {"seed": s, "steps": st, "cfg": cf,
                "sampler_name": "euler_ancestral", "scheduler": "normal",
                "denoise": 1, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0],
                "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "agentic_os", "images": ["8", 0]}},
    }


def wait_for_completion(prompt_id, timeout=600):
    """等待生成完成"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            history = get_history(prompt_id)
            if prompt_id in history:
                outputs = history[prompt_id]["outputs"]
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        return node_output["images"]
        except Exception:
            pass
        time.sleep(2)
    return None


def render_shot(character_id, shot_key, prompt, negative_prompt="", shot_name="", opts=None):
    """渲染单个分镜"""
    out_dir = OUTPUT_DIR / character_id
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{shot_key}.png"
    if out_path.exists():
        print(f"  ⏭  {shot_name} 已存在: {out_path}")
        return str(out_path)

    print(f"  🎨 生成: {shot_name}...", end=" ", flush=True)
    try:
        o = opts or {}
        workflow = build_sdxl_workflow(prompt, negative_prompt,
                                       width=o.get("width"), height=o.get("height"),
                                       steps=o.get("steps"), seed=o.get("seed"))
        result = queue_prompt(workflow)
        prompt_id = result["prompt_id"]

        images = wait_for_completion(prompt_id)
        if not images:
            print("⏰ 超时")
            return None

        img_data = get_image(images[0]["filename"], images[0].get("subfolder", ""))
        with open(out_path, "wb") as f:
            f.write(img_data)

        size_kb = len(img_data) // 1024
        elapsed = images[0].get("_elapsed", "?")
        print(f"✅ {size_kb}KB")
        return str(out_path)
    except Exception as e:
        print(f"❌ {str(e)[:60]}")
        return None


def render_character(bible, char_id, opts=None, episode=None):
    """渲染单个角色的3个分镜。episode: 集数前缀(如'ep01')，用于同角色不同集"""
    chars = bible.get("characters", {})
    char = chars.get(char_id)
    if not char:
        print(f"❌ 角色不存在: {char_id}")
        return

    prefix = f"{episode}_" if episode else ""
    cname = char.get("character", char_id)
    print(f"\n{'='*50}\n  {cname} · {len(char.get('scenes',[]))} 镜\n{'='*50}")

    results = []
    for scene in char.get("scenes", []):
        shot = scene.get("shot", "unknown")
        desc = scene.get("description", shot)
        prompt = scene.get("prompt", "")
        neg = scene.get("negative_prompt", "")
        shot_file = f"{prefix}{shot}"
        path = render_shot(char_id, shot_file, prompt, neg, f"{shot}: {desc}", opts)
        results.append({"shot": shot_file, "path": path, "success": path is not None})

    return results


def render_episode(bible, episode_id, opts=None):
    """渲染单集所有分镜——对齐pipeline EPISODE_MAP"""
    # EPISODE_MAP aligned with pipeline_ep01.py v3.6
    ep_map = {
        "01": "luzhishen",  # 鲁提辖拳打镇关西
        "02": "luzhishen",  # 鲁智深倒拔垂杨柳 (同角色不同集)
        "03": "linchong",   # 林冲风雪山神庙
        "04": "songjiang",  # 宋江杀阎婆惜
        "05": "likui",      # 李逵沂岭杀四虎
        "06": "wuyong",     # 智取生辰纲
    }
    ep_num = str(episode_id).zfill(2)
    char_id = ep_map.get(ep_num)
    if not char_id:
        print(f"❌ 未知集数: {episode_id}")
        return
    ep_tag = f"ep{ep_num}"
    return render_character(bible, char_id, opts, episode=ep_tag)


def main():
    import argparse
    p = argparse.ArgumentParser(description="ComfyUI 静态图渲染器 v3.6")
    p.add_argument("--character", help="角色ID: wusong/luzhishen/linchong/songjiang/likui/wuyong")
    p.add_argument("--episode", help="集数: 01-06")
    p.add_argument("--all", action="store_true", help="渲染全部18镜")
    p.add_argument("--test", action="store_true", help="快速测试: 生成1张512x912小图")
    p.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    p.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    p.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = p.parse_args()

    opts = {"width": args.width, "height": args.height, "steps": args.steps, "seed": args.seed}

    bible = load_visual_bible()
    if not bible:
        return

    if args.test:
        print("🧪 快速测试: 1张小图 (512×912 · 10步)")
        test_opts = {"width": 512, "height": 912, "steps": 10, "seed": args.seed}
        chars = bible.get("characters", {})
        ws = chars.get("wusong", {})
        scenes = ws.get("scenes", [])
        if scenes:
            s = scenes[0]
            path = render_shot("wusong", "shot_01_test", s.get("prompt", ""), s.get("negative_prompt", ""), "武松镜01(测试)", test_opts)
            if path:
                print(f"\n✅ 测试通过: {path}")
                print(f"   文件大小: {Path(path).stat().st_size // 1024}KB")
        return

    if args.character:
        render_character(bible, args.character, opts)
    elif args.episode:
        render_episode(bible, args.episode, opts)
    elif args.all:
        results = {}
        # Pipeline-aligned: 6 episodes → 6 character renders (with ep prefixes for same-char episodes)
        pipeline_eps = {"01": "luzhishen", "02": "luzhishen", "03": "linchong",
                        "04": "songjiang", "05": "likui", "06": "wuyong"}
        for ep, char_id in pipeline_eps.items():
            ep_tag = f"ep{ep}"
            results[ep_tag] = render_character(bible, char_id, opts, episode=ep_tag)

        total = sum(len(r) for r in results.values() if r)
        ok = sum(1 for r in results.values() if r for s in r if s.get("success"))
        print(f"\n{'='*50}")
        print(f"  全部完成: {ok}/{total} 镜成功")
        print(f"  输出: {OUTPUT_DIR}")
        print(f"{'='*50}")
    else:
        print("用法: --character wusong | --episode 01 | --all | --test")
        chars = bible.get("characters", {})
        print(f"\n可用角色: {', '.join(chars.keys())}")
        for cid, cdata in chars.items():
            sc = len(cdata.get("scenes", []))
            print(f"  {cid:12s} → {cdata.get('character','?')} ({sc}镜)")


if __name__ == "__main__":
    main()
