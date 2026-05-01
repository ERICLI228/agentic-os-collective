#!/usr/bin/env python3
"""
Generate 6 verification portraits with actor-locked 1998-style prompts
for visual comparison against previous generation.
"""
import sys, os, json, time, uuid, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.comfyui_renderer import (
    COMFYUI_URL, OUTPUT_DIR, build_sdxl_workflow,
    queue_prompt, get_history, get_image
)

# 6 sample characters with strengthened 1998 CCTV actor-locked prompts
VERIFICATION_CHARS = [
    ("wusong", "武松", 
     "Wu Song (1998 CCTV Water Margin). Thick ink-black eyebrows slanting up to temples like drawn sabers. Sharp phoenix eyes gleaming with intensity. A stern square-jawed face that inspires fear without anger. The iconic iron fillet headband binding his forehead. Grey simple headband monk's robe. Close-up headshot, stern expression.",
     "Headshot portrait, Wu Song from 1998 Water Margin TV series. Thick black eyebrows, sharp phoenix eyes, stern square-jawed face, iron fillet headband, grey monk robe."),
    ("luzhishen", "鲁智深",
     "Lu Zhishen (1998 CCTV Water Margin). Extremely burly and stout monk with a wide face and large ears. Fierce intimidating face covered in a full bristling beard. Eyes that are clear, wise, and serene. Nine incense scars on forehead. Coarse grey monk's robe, massive Buddhist beads around neck. Photorealistic portrait.",
     "Lu Zhishen portrait. Burly monk, wide face, full black beard, nine scars on forehead, wise eyes, grey robe, heavy Buddhist beads."),
    ("likui", "李逵",
     "Li Kui (1998 CCTV Water Margin). Dark iron-tower-like build with bulging muscles. Pitch-black skin covered in ferocious facial flesh. Bristling hair and beard like a wild beast. Round bulging eyes that switch between murderous rage and childlike innocence. Rough dark vest, bare muscular arms, massive axes at waist.",
     "Li Kui portrait. Dark skin, iron-tower build, bulging muscles, bristling beard, round fierce eyes, simple dark vest, wild look."),
    ("linchong", "林冲",
     "Lin Chong (1998 CCTV Water Margin). Refined scholarly face with proper features and a thin mustache. Eyes carrying deep grief and suppressed fury. Perpetually furrowed brows of a wronged hero. Faded blue-grey cloth robe, worn felt hat with wide brim, frayed cuffs hinting at past dignity. Tragic and restrained.",
     "Lin Chong portrait. Refined scholarly face, thin mustache, sorrowful eyes, faded blue cloth robe, felt hat, tragic expression."),
    ("husanniang", "扈三娘",
     "Hu Sanniang (1998 CCTV Water Margin). Striking pale jade-skin face with a high heroic brow over sharp almond-shaped eyes. Cold aloof beauty, a woman of steel in a soldier's guise. Floral headdress over golden chainmail, flowing red cape. Twin crescent sabers crossed at her back. Proud defiant expression.",
     "Hu Sanniang portrait. Beautiful heroic woman, cold almond eyes, floral headdress, golden chainmail, red cape, defiant look."),
    ("shiqian", "时迁",
     "Shi Qian (1998 CCTV Water Margin). Small thin wiry frame with a pointed monkey-like face. Small quick-shifting eyes always alert. Master thief's expression, cunning and nimble. Dark black stealth outfit, tools hidden in sleeves. Hunched cautious posture.",
     "Shi Qian portrait. Small thin man, monkey-like pointed face, quick shifting eyes, dark thief outfit, nimble crouched posture."),
]

# Use the negative suffix from the existing pipeline
NEGATIVE_PROMPT = "low quality, blurry, distorted, deformed, bad anatomy, ugly, watermark, text, signature, extra limbs, cartoon, anime, 3D render, Asian drama, Korean drama, k-pop, idol, makeup, lipstick, eyeliner, smooth plastic skin, glossy skin, porcelain doll, bishounen, flower boy, effeminate, young girl, teenage, babyface, western classical, renaissance"

def generate_portrait(char_id, char_name, prompt_main, prompt_short, seed=42):
    """Generate one portrait via ComfyUI SDXL."""
    quality = ", cinematic lighting, photorealistic, 8K, sharp focus, highly detailed, professional photography, 35mm film grain, warm color grade, 1998 Chinese TV drama aesthetic, CCTV dramatic lighting, coarse textured skin"
    
    prompt = prompt_main + quality
    negative = NEGATIVE_PROMPT
    
    print(f"📸 Generating {char_name} ({char_id})...")
    workflow = build_sdxl_workflow(prompt, negative, seed=seed, width=768, height=1024)
    
    try:
        resp = queue_prompt(workflow)
        prompt_id = resp.get("prompt_id", "")
        print(f"   Queued: {prompt_id}")
        
        # Wait for completion
        for attempt in range(60):
            time.sleep(2)
            history = get_history(prompt_id)
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, node_output in outputs.items():
                    for img_data in node_output.get("images", []):
                        fn = img_data.get("filename", "")
                        sf = img_data.get("subfolder", "")
                        img_bytes = get_image(fn, sf, "output")
                        
                        # Save
                        out_dir = OUTPUT_DIR / char_name
                        out_dir.mkdir(parents=True, exist_ok=True)
                        out_path = out_dir / "verification_portrait.png"
                        with open(out_path, "wb") as f:
                            f.write(img_bytes)
                        print(f"   ✅ Saved: {out_path} ({len(img_bytes)/1024:.0f} KB)")
                        return True
                print(f"   ⚠️ No images in output")
                return False
        print(f"   ⚠️ Timeout after 120s")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("="*60)
    print("  水浒传 6角色96版定妆照验证生成")
    print(f"  Time: {time.strftime('%H:%M:%S')}")
    print("="*60)
    
    base_seed = int(time.time()) % 100000
    results = []
    
    for i, (cid, name, pm, ps) in enumerate(VERIFICATION_CHARS):
        seed = base_seed + i * 1000
        ok = generate_portrait(cid, name, pm, ps, seed=seed)
        results.append((name, "✅" if ok else "❌"))
        print()
    
    print("="*60)
    print("  生成结果:")
    for name, status in results:
        print(f"    {status} {name}")
    print("="*60)
    print(f"  输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
