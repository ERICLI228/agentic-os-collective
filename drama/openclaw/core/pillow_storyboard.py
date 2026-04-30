#!/usr/bin/env python3
"""Pillow v2: 渐变背景 + 情绪配色 + 角色名叠加 → final_pillow.mp4"""
import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SCRIPT = Path.home() / ".agentic-os" / "episode_01" / "script" / "script_ep01.json"
IMG_DIR = Path.home() / ".agentic-os" / "episode_01" / "pillow_v2"
IMG_DIR.mkdir(parents=True, exist_ok=True)
import shutil

def _find_ffmpeg():
    """动态查找 ffmpeg，避免 brew 升级后路径失效"""
    candidates = [
        shutil.which("ffmpeg"),
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
    ]
    cellar = Path("/opt/homebrew/Cellar/ffmpeg")
    if cellar.exists():
        for d in sorted(cellar.iterdir(), reverse=True):
            f = d / "bin" / "ffmpeg"
            if f.exists():
                candidates.append(str(f))
                break
    for p in candidates:
        if p and Path(p).exists():
            return p
    return "ffmpeg"

FFMPEG = _find_ffmpeg()
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
W, H = 1280, 720

shots = json.loads(SCRIPT.read_text())["shots"]

# 情绪配色方案: (bg_top, bg_bottom, accent, mood_label)
PALETTES = [
    ("#2d1b00", "#1a0f00", "#ff8c42", "肃穆"),   # shot_01 夕阳山林 → 棕橙渐变
    ("#1a2a0a", "#0a1500", "#66bb6a", "紧张"),   # shot_02 上山 → 暗绿渐变
    ("#3a0a0a", "#1a0000", "#ff4444", "惊险"),   # shot_03 猛虎 → 暗红渐变
    ("#2a1a00", "#150d00", "#ffd700", "激昂"),   # shot_04 打虎 → 暗金渐变
    ("#0a1a2a", "#000d15", "#4fc3f7", "豪迈"),   # shot_05 英雄 → 深蓝渐变
]

TYPE_MAP = {"establishing": "远景", "action": "动作", "climax": "高潮", "resolution": "结果", "closing": "结尾"}
DURATIONS = [5, 7, 8, 7, 3]

def make_gradient(top_color, bottom_color, w, h):
    """创建垂直渐变背景"""
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r1, g1, b1 = int(top_color[1:3], 16), int(top_color[3:5], 16), int(top_color[5:7], 16)
        r2, g2, b2 = int(bottom_color[1:3], 16), int(bottom_color[3:5], 16), int(bottom_color[5:7], 16)
        ratio = y / h
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def try_font(size):
    for path in [FONT_PATH, "/System/Library/Fonts/STHeiti Light.ttc"]:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

fonts = {
    "xs": try_font(16), "sm": try_font(20), "md": try_font(26),
    "lg": try_font(36), "xl": try_font(52), "tag": try_font(18)
}

print(f"\n🎨 Pillow v2 生成 {len(shots)} 张分镜图 (渐变背景)\n")

img_files = []
for i, shot in enumerate(shots):
    bg_top, bg_bot, accent, mood = PALETTES[i]

    img = make_gradient(bg_top, bg_bot, W, H)
    draw = ImageDraw.Draw(img)

    # 顶部标题区
    draw.text((60, 40), f"水浒传 · EP01  {'武松打虎'}", fill=accent, font=fonts["md"])
    draw.line([(60, 90), (W - 60, 90)], fill=accent, width=1)

    # 分镜标签
    shot_label = f"分镜 {shot['id'].replace('shot_', '')} / {len(shots)}"
    draw.text((60, 110), shot_label, fill="#666666", font=fonts["sm"])

    # 角色名 (大字居中)
    cx, cy = W // 2, 240
    char_name = "武松" if i < 4 else "武松 & 猛虎"
    tw = fonts["xl"].getlength(char_name)
    draw.text((cx - tw // 2, cy - 30), char_name, fill="#ffffff", font=fonts["xl"])

    # 场景情绪标签
    tag_text = f"{TYPE_MAP[shot['type']]} | {mood}"
    tw = fonts["tag"].getlength(tag_text)
    # 标签背景框
    tag_x, tag_y = cx - tw // 2 - 15, cy + 40
    tag_w, tag_h = tw + 30, 36
    draw.rounded_rectangle([(tag_x, tag_y), (tag_x + tag_w, tag_y + tag_h)], radius=8, fill=accent)
    draw.text((tag_x + 15, tag_y + 6), tag_text, fill=bg_bot, font=fonts["tag"])

    # 画面描述
    desc_y = cy + 100
    draw.text((60, desc_y), "📖 画面", fill="#888888", font=fonts["sm"])
    # 文字换行
    visual = shot["visual"]
    y = desc_y + 30
    chars_per_line = 30
    for line_idx in range(0, len(visual), chars_per_line):
        line = visual[line_idx:line_idx + chars_per_line]
        draw.text((80, y), line, fill="#d0d0d0", font=fonts["md"])
        y += 36

    # 底部信息栏
    draw.line([(60, H - 80), (W - 60, H - 80)], fill="#333333", width=1)
    draw.text((60, H - 60), f"景阳冈 · {shot['time_range']}", fill="#555555", font=fonts["xs"])
    draw.text((W - 140, H - 60), f"⏱ {DURATIONS[i]}s", fill=accent, font=fonts["md"])

    out = IMG_DIR / f"{shot['id']}.png"
    img.save(str(out), "PNG", quality=95)
    size = out.stat().st_size
    print(f"  ✅ {shot['id']}: {size:,} bytes | {char_name} | {mood}")
    img_files.append(str(out))

# ffmpeg 合成
print("\n🎬 合成 final_pillow.mp4...")
concat = IMG_DIR / "_concat.txt"
with open(concat, "w") as f:
    for img_path, dur in zip(img_files, DURATIONS):
        f.write(f"file '{img_path}'\nduration {dur}\n")

output = Path.home() / ".agentic-os" / "episode_01" / "final_pillow.mp4"
cmd = [
    FFMPEG, "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat),
    "-vf", "format=yuv420p,fps=25",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-preset", "medium", "-crf", "18",
    str(output)
]
result = subprocess.run(cmd, capture_output=True, text=True)

if output.exists() and output.stat().st_size > 1000:
    size = output.stat().st_size
    dur_cmd = subprocess.run(
        [f"{FFMPEG.replace('ffmpeg', 'ffprobe')}", "-v", "error",
         "-show_entries", "format=duration,size", "-of", "csv=p=0", str(output)],
        capture_output=True, text=True
    ).stdout.strip().split(",")
    print(f"\n{'='*60}")
    print(f"  ✅ final_pillow.mp4 生成成功!")
    print(f"  📄 {output}")
    print(f"  📏 {int(size):,} bytes  |  ⏱ {dur_cmd[0]}s  |  h264 无声")
    print(f"{'='*60}\n")
else:
    print(f"❌ 合成失败: {result.stderr[-300:]}")
    sys.exit(1)
