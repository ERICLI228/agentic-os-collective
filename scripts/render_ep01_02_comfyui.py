#!/usr/bin/env python3
"""Generate EP01/EP02 ComfyUI renders for 鲁智深 using video_prompts."""
import json, sys, time, uuid, urllib.request
from pathlib import Path

COMFYUI_URL = "http://127.0.0.1:8188"
RENDER_DIR = Path.home() / ".agentic-os/character_designs/renders/鲁智深"
BIBLE_PATH = Path.home() / ".agentic-os/character_designs/visual_bible.json"

QUALITY_SUFFIX = ", cinematic lighting, photorealistic, 8K, sharp focus, highly detailed, professional photography, 35mm film grain, warm color grade"
NEG_PROMPT = "low quality, blurry, distorted, deformed, bad anatomy, ugly, watermark, text, signature, extra limbs, cartoon, anime, 3D render"

def load_prompts():
    with open(BIBLE_PATH) as f:
        data = json.load(f)
    chars = data.get("characters", {})
    luzhi = chars.get("luzhishen", {})
    vp = luzhi.get("video_prompts", {})
    prompts = []
    for key in ["方案一", "方案二", "方案三"]:
        entry = vp.get(key, {})
        if isinstance(entry, dict):
            prompts.append(entry.get("prompt", entry.get("简练版", "")))
        elif isinstance(entry, str):
            prompts.append(entry)
    return [p for p in prompts if p]

def queue_prompt(prompt_text):
    workflow = {
        "3": {"class_type": "KSampler", "inputs": {"seed": 42, "steps": 25, "cfg": 7.5,
                "sampler_name": "euler_ancestral", "scheduler": "normal",
                "denoise": 1, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0],
                "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 768, "height": 1024, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt_text + QUALITY_SUFFIX, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG_PROMPT, "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "luzhishen_ep", "images": ["8", 0]}},
    }
    payload = {"prompt": workflow, "client_id": f"eprender-{uuid.uuid4().hex[:8]}"}
    req = urllib.request.Request(f"{COMFYUI_URL}/prompt", data=json.dumps(payload).encode())
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def get_result(prompt_id, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req) as resp:
                history = json.loads(resp.read())
            if prompt_id in history:
                for node_id, node_output in history[prompt_id]["outputs"].items():
                    if "images" in node_output:
                        return node_output["images"]
        except: pass
        time.sleep(3)
    return None

def download_image(filename, subfolder=""):
    params = f"filename={filename}&subfolder={subfolder}&type=output"
    with urllib.request.urlopen(f"{COMFYUI_URL}/view?{params}") as resp:
        return resp.read()

def render_episode(ep_num, prompts):
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    for i, prompt in enumerate(prompts):
        shot_id = i + 1
        out_path = RENDER_DIR / f"ep{ep_num}_shot_{shot_id:02d}.png"
        if out_path.exists():
            print(f"  ⏭ ep{ep_num}_shot_{shot_id:02d} 已存在 ({out_path.stat().st_size//1024}KB)")
            continue
        print(f"  🎨 EP{ep_num} shot_{shot_id:02d}: {prompt[:50]}...", end=" ", flush=True)
        try:
            result = queue_prompt(prompt)
            images = get_result(result["prompt_id"])
            if not images:
                print("⏰ 超时")
                continue
            img_data = download_image(images[0]["filename"], images[0].get("subfolder", ""))
            with open(out_path, "wb") as f:
                f.write(img_data)
            print(f"✅ {len(img_data)//1024}KB")
        except Exception as e:
            print(f"❌ {e}")

if __name__ == "__main__":
    prompts = load_prompts()
    if not prompts:
        print("❌ 鲁智深 video_prompts 为空, 无法渲染")
        sys.exit(1)
    print(f"鲁智深 prompts: {len(prompts)}")
    for ep in ["01", "02"]:
        print(f"\n=== EP{ep} ===")
        render_episode(ep, prompts)
    print("\n✅ 完成")
