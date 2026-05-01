#!/usr/bin/env python3
"""
Generate 4 multi-angle portraits for all 109 characters via ComfyUI SDXL.
v3.7 — Enhanced: Song dynasty period accuracy, character consistency, aged/mature faces.
"""
import sys, os, time, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.comfyui_renderer import COMFYUI_URL, build_sdxl_workflow, queue_prompt, get_history, get_image

RENDERS = os.path.expanduser("~/.agentic-os/character_designs/renders")
LOG = os.path.expanduser("~/.agentic-os/logs/bulk_portraits_v3.log")

# ── Core negative prompt — reject Korean/anime/young/beauty standards ──
NEG = (
    "low quality, blurry, distorted, deformed, bad anatomy, ugly, watermark, text, "
    "cartoon, anime, 3D render, digital art, illustration, painting, "
    "Asian drama, Korean drama, K-drama, k-pop, idol, makeup, lipstick, eyeliner, "
    "smooth plastic skin, glossy skin, porcelain doll, glass skin, dewy skin, "
    "bishounen, flower boy, effeminate, feminine, babyface, young girl, teenage, "
    "20s, youth, young adult, western classical, renaissance, "
    "sunglasses, modern clothes, t-shirt, jeans, sneakers, "
    "white skin, pale skin, fair skin, flawless"
)

# ── Quality positive prompt ──
QUAL = (
    ", cinematic lighting, photorealistic, 8K, sharp focus, highly detailed, "
    "35mm film grain, warm color grade, "
    "1998 Chinese TV drama aesthetic, CCTV Water Margin look, "
    "aged face, wrinkles, weathered skin, sun-beaten skin, coarse textured skin, "
    "Song dynasty accurate historical clothing, ancient Chinese period costume, "
    "middle aged male, 35 to 50 year old, rough hands, calloused, "
    "natural aging, realistic pores, gray hair strands, "
    "no makeup, natural appearance, historical authenticity"
)

# ── 4 angles with consistent character reference ──
def make_prompt(cname, angle_idx):
    """Build prompt with consistent character identity across angles."""
    angles = [
        "Front-facing portrait, looking directly at camera. Full face visible, both shoulders squared. Neutral dignified expression. Even lighting.",
        "Three-quarter profile facing camera right. Head turned slightly, eyes looking into the distance. Dramatic side lighting casting half the face in shadow. One ear visible.",
        "Profile view facing left. Complete side profile showing the jawline, nose bridge, and period headwear. Background softly blurred. Rim lighting on the edge of the face.",
        "Low angle shot looking slightly upward at the face. Heroic posture, chin raised slightly. Background shows ancient Chinese architecture (wooden pillars, tiled roof). Natural daylight flooding in from one side."
    ]
    p = f"{cname} from the 1998 CCTV TV series Water Margin. {angles[angle_idx]}. Traditional Song dynasty historical clothing, traditional Chinese male/female attire from the 12th century. No modern elements of any kind.{QUAL}"
    return p


# ── Main generation loop ──
def log(msg):
    ts = time.strftime("%H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"{ts} {msg}\n")
    print(msg)

# First, read visual_bible to get all characters with their consistent metadata
VB_PATH = os.path.expanduser("~/.agentic-os/character_designs/visual_bible.json")
with open(VB_PATH) as f:
    vb = json.load(f)

# Build character list (ordered by star_rank)
chars_data = []
for fid, ch in vb["characters"].items():
    name = ch.get("name", fid)
    rank = ch.get("star_rank", 999)
    chars_data.append((rank, name, fid))
chars_data.sort()

log(f"Starting bulk portrait generation for {len(chars_data)} characters")
log(f"4 angles each, ~30s/image, estimated {len(chars_data)*4*30/60:.0f} min total")
log("=" * 60)

total_new = 0
for rank, cname, fid in chars_data:
    d = os.path.join(RENDERS, cname)
    existing = sorted([f for f in os.listdir(d) if f.endswith(".png") and f.startswith("portrait_")])
    existing_names = set(existing)
    
    need = 4 - len(existing)
    if need <= 0:
        log(f"[{rank:>3}] {cname}: already {len(existing)} portraits, skip")
        continue

    log(f"[{rank:>3}] {cname}: {len(existing)} existing, generating {need} more")
    for ai in range(4):
        fname = f"portrait_{ai}.png"
        if fname in existing_names:
            continue
        
        # Use consistent seed per character for facial consistency
        seed = abs(hash("shuihu_" + fid)) % 100000 + ai * 100
        prompt = make_prompt(cname, ai)
        
        try:
            wf = build_sdxl_workflow(prompt, NEG, seed=seed, width=768, height=1024)
            resp = queue_prompt(wf)
            pid = resp.get("prompt_id", "")

            for attempt in range(90):
                time.sleep(2)
                hist = get_history(pid)
                if pid in hist:
                    outs = hist[pid].get("outputs", {})
                    for nid, no in outs.items():
                        for img in no.get("images", []):
                            fn = img["filename"]
                            sf = img.get("subfolder", "")
                            b = get_image(fn, sf, "output")
                            out_path = os.path.join(d, fname)
                            with open(out_path, "wb") as f:
                                f.write(b)
                            log(f"  ✅ {cname} portrait_{ai}: {len(b)//1024}KB (seed={seed})")
                            total_new += 1
                            existing_names.add(fname)
                            break
                    break
            else:
                log(f"  ⚠️ {cname} portrait_{ai}: timeout")
        except Exception as e:
            log(f"  ❌ {cname} portrait_{ai}: {e}")
    
    # Small delay every 10 characters
    if (rank) % 10 == 0:
        time.sleep(3)
        log(f"  --- checkpoint: {rank}/{len(chars_data)} chars, {total_new} new images ---")

log("=" * 60)
log(f"COMPLETE: {total_new} new portrait images generated for {len(chars_data)} characters")
log("=" * 60)
