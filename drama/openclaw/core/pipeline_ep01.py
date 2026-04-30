#!/usr/bin/env python3
"""
短剧第一集端到端管线 - Sprint 1.5

管线: 剧本 → 角色设计 → 配音 → 视频 → 合成

用法:
  python3 pipeline_ep01.py                  # 跑完整管线 (macOS say)
  python3 pipeline_ep01.py --voice nls      # 阿里云 NLS 真人配音
  python3 pipeline_ep01.py --silent         # 纯视频(无声)
  python3 pipeline_ep01.py --sfx            # + 环境音效混音 (freesound)
  python3 pipeline_ep01.py --dry-run        # 只打印计划
  python3 pipeline_ep01.py --test           # 验证依赖
"""

import argparse
import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# ── 路径 ──
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Episode 映射 (按 shuihuzhuan.yaml 索引)
EPISODE_MAP = {
    "01": {"idx": 0, "title": "鲁提辖拳打镇关西", "character": "鲁智深",
            "dir": "episode_01", "scene_key": "渭州"},
    "02": {"idx": 1, "title": "鲁智深倒拔垂杨柳", "character": "鲁智深",
            "dir": "episode_02", "scene_key": "大相国寺菜园"},
    "03": {"idx": 6, "title": "林冲风雪山神庙", "character": "林冲",
            "dir": "episode_03", "scene_key": "风雪山神庙"},
    "04": {"idx": 10, "title": "宋江杀阎婆惜", "character": "宋江",
            "dir": "episode_04", "scene_key": "梁山聚义厅"},
    "05": {"idx": 9, "title": "李逵沂岭杀四虎", "character": "李逵",
            "dir": "episode_05", "scene_key": "梁山"},
    "06": {"idx": 8, "title": "智取生辰纲", "character": "吴用",
            "dir": "episode_06", "scene_key": "景阳冈"},
}

# ── ffmpeg 路径 (Mac brew 不在默认 PATH) ──
from shared.core.utils import _find_ffmpeg

FFMPEG = _find_ffmpeg()
FFPROBE = str(Path(FFMPEG).parent / "ffprobe") if Path(FFMPEG).parent.name == "bin" else (FFMPEG.replace("ffmpeg", "ffprobe") if "ffmpeg" in FFMPEG else "ffprobe")
os.environ["PATH"] = f"{Path(FFMPEG).parent}:{os.environ.get('PATH', '')}"


def init_episode_dirs(ep_id="03"):
    """初始化 episode 输出目录，返回 (output_dir, script_dir, audio_dir, video_dir, ep_cfg)"""
    ep_cfg = EPISODE_MAP.get(ep_id, EPISODE_MAP["03"])
    output_dir = Path.home() / ".agentic-os" / ep_cfg["dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    script_dir = output_dir / "script"
    audio_dir = output_dir / "audio"
    video_dir = output_dir / "video"
    for d in [script_dir, audio_dir, video_dir]:
        d.mkdir(exist_ok=True)
    return output_dir, script_dir, audio_dir, video_dir, ep_cfg


def check_dependencies():
    """验证管线依赖"""
    results = {}

    # yaml
    try:
        import yaml
        results["pyyaml"] = True
    except ImportError:
        results["pyyaml"] = False

    # ffmpeg
    try:
        subprocess.run([FFMPEG, "-version"], capture_output=True, timeout=5)
        results["ffmpeg"] = True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        results["ffmpeg"] = False

    # macOS say (TTS fallback)
    say_path = shutil.which("say")
    results["say_tts"] = say_path is not None

    # story YAML
    story_file = PROJECT_ROOT / "stories" / "shuihuzhuan.yaml"
    results["story_yaml"] = story_file.exists()

    return results


def _import_script_manager():
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from shared.script_manager import _build_storyboard, CURRENT_EPISODES
    return _build_storyboard, CURRENT_EPISODES


ACT_TYPE_MAP = {
    "开场": "establishing",
    "发展": "action",
    "冲突": "conflict",
    "高潮": "climax",
    "结局": "closing",
}


def generate_script(ep_id="03", script_dir=None):
    """Step 1: 生成剧本 JSON (动态从 script_manager 加载分镜)"""
    import yaml
    _build_storyboard, CURRENT_EPISODES = _import_script_manager()

    ep_cfg = EPISODE_MAP.get(ep_id, EPISODE_MAP["03"])
    story_file = PROJECT_ROOT / "stories" / "shuihuzhuan.yaml"
    with open(story_file) as f:
        story = yaml.safe_load(f)

    ep = story["episodes"][ep_cfg["idx"]]
    character = ep_cfg.get("character", ep.get("character", ""))
    title = ep_cfg.get("title", ep.get("title", ""))

    storyboard = _build_storyboard(title, ep_cfg.get("idx", 0), character)

    shots = []
    time_offset = 0
    for sb in storyboard:
        dur_sec = int(sb.get("duration", "10秒").replace("秒", ""))
        shot = {
            "id": f"shot_{sb['seq']:02d}",
            "time_range": f"{time_offset}-{time_offset + dur_sec}s",
            "type": ACT_TYPE_MAP.get(sb.get("act", ""), "action"),
            "visual": sb.get("description", ""),
            "narration": sb.get("dialogue", sb.get("description", "")),
            "mood": sb.get("emotion", ""),
            "scene": sb.get("scene", ""),
            "act": sb.get("act", ""),
            "duration_sec": dur_sec,
        }
        shots.append(shot)
        time_offset += dur_sec

    total_duration = sum(s["duration_sec"] for s in shots)
    scene_key = ep_cfg.get("scene_key")
    scene_desc = story.get("scenes", {}).get(scene_key, "") if scene_key else ""

    script = {
        "episode_id": f"ep{ep_id}",
        "title": title,
        "character": character,
        "scene": scene_key or title,
        "scene_description": scene_desc,
        "duration_seconds": total_duration,
        "generated_at": datetime.now().isoformat(),
        "shots": shots,
    }

    if script_dir is None:
        from pathlib import Path
        script_dir = Path.home() / ".agentic-os" / f"episode_{ep_id}" / "script"
        script_dir.mkdir(parents=True, exist_ok=True)

    output_file = script_dir / f"script_ep{ep_id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    print(f"  ✅ Step 1: 剧本生成 ({ep_id}) → {output_file} ({len(shots)}镜/{total_duration}秒)")
    return script


def generate_audio(script, voice_mode="say", audio_dir=None):
    """Step 2: 生成旁白音频 (say/nls)"""
    if audio_dir is None:
        audio_dir = AUDIO_DIR
    narration_files = []

    for i, shot in enumerate(script["shots"]):
        text = shot["narration"]
        audio_file = audio_dir / f"narration_{shot['id']}.aiff" if voice_mode != "nls" else audio_dir / f"narration_{shot['id']}.mp3"

        if voice_mode == "nls":
            _generate_nls(text, audio_file, voice="zhiqi")
        else:
            _generate_say(text, audio_file)

        if audio_file.exists() and audio_file.stat().st_size > 0:
            narration_files.append(str(audio_file))
            print(f"  ✅ 旁白 {shot['id']}: {audio_file.name} ({audio_file.stat().st_size} bytes)")
        else:
            print(f"  ⚠️ 旁白 {shot['id']} 生成失败")

    if not narration_files:
        print("  ⚠️ 无旁白音频,使用静音替代")
        silence_file = audio_dir / "silence.aiff"
        subprocess.run([FFMPEG, "-f", "lavfi", "-i", "anullsrc=duration=3", "-y", str(silence_file)], capture_output=True)
        narration_files.append(str(silence_file))

    print(f"  ✅ Step 2: 音频生成 → {len(narration_files)} 段旁白")
    return narration_files


def _generate_say(text, audio_file):
    """macOS say TTS"""
    subprocess.run(
        ["say", "-v", "Tingting", "-o", str(audio_file), text],
        capture_output=True, timeout=30
    )


def _generate_nls(text, audio_file, voice="zhiqi"):
    """阿里云 NLS TTS"""
    try:
        import importlib.util
        nls_path = PROJECT_ROOT / "drama/openclaw/skills/water-margin-drama/aliyun_nls.py"
        spec = importlib.util.spec_from_file_location("aliyun_nls", str(nls_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod.synthesize(text, voice=voice, output_path=str(audio_file))
        if not result:
            print(f"  ⚠️ NLS 返回空，降级到 macOS say")
            _generate_say(text, audio_file)
    except Exception as e:
        print(f"  ⚠️ NLS 异常: {e}, 降级到 macOS say")
        _generate_say(text, audio_file)


def generate_video(script, video_dir=None, render_mode="pillow", ep_id="03"):
    """Step 3: 生成视频片段 (Pillow 字幕帧 或 ComfyUI AI渲染图 → ffmpeg)"""
    if video_dir is None:
        video_dir = VIDEO_DIR
    video_files = []
    episode = script.get("episode", "")

    from PIL import Image, ImageDraw, ImageFont

    w, h = 1280, 720
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 48)
        font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
        font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
    except Exception:
        font_title = font_sub = font_small = ImageFont.load_default()

    chars = script.get("characters") or [script.get("character", "")] * len(script["shots"])
    character_palettes = {
        "武松": ("#1a1a2e", "#8b0000"),
        "鲁智深": ("#4a3728", "#c4a35a"),
        "林冲": ("#1c1c2a", "#8b0000"),
        "宋江": ("#1a3a1a", "#ffd700"),
        "李逵": ("#2a1a0a", "#cc4400"),
        "吴用": ("#1a2a3a", "#66ccff"),
    }

    # ComfyUI render path config
    RENDER_CHAR_MAP = {"01": "luzhishen", "02": "luzhishen", "03": "linchong",
                       "04": "songjiang", "05": "likui", "06": "wuyong"}
    RENDER_BASE = Path.home() / ".agentic-os" / "character_designs" / "renders"

    # Render mapping
    use_comfyui = (render_mode == "comfyui")
    ep_num = ep_id
    char_id = RENDER_CHAR_MAP.get(ep_num, "linchong")

    for i, shot in enumerate(script["shots"]):
        video_file = video_dir / f"{shot['id']}.mp4"
        duration = 5 if i < 4 else 3

        char_name = chars[i] if i < len(chars) else ""
        colors = character_palettes.get(char_name, ("#1a1a2e", "#e0e0e0"))
        bg_color = colors[0]
        accent_color = colors[1]

        narration = shot.get("narration", "")
        scene_label = shot.get("scene", "")

        # ── ComfyUI mode: load AI render image ──
        if use_comfyui:
            # Cycle through available renders (3 renders → 5 shots: 0,1,2,0,1)
            render_idx = (i % 3) + 1
            render_file = RENDER_BASE / char_id / f"ep{ep_num}_shot_{render_idx:02d}.png"
            if render_file.exists():
                try:
                    img = Image.open(render_file).convert("RGB")
                    img = img.resize((w, h), Image.LANCZOS)
                    draw = ImageDraw.Draw(img)
                    print(f"    📷 ComfyUI: {render_file.name} ({render_file.stat().st_size//1024}KB)")
                except Exception as e:
                    print(f"    ⚠️ ComfyUI加载失败: {e}, 降级Pillow")
                    img = Image.new("RGB", (w, h), bg_color)
                    draw = ImageDraw.Draw(img)
            else:
                print(f"    ⚠️ ComfyUI渲染图不存在: {render_file}, 降级Pillow")
                img = Image.new("RGB", (w, h), bg_color)
                draw = ImageDraw.Draw(img)
        else:
            img = Image.new("RGB", (w, h), bg_color)
            draw = ImageDraw.Draw(img)

        # Top: Episode + Shot info
        draw.text((40, 30), f"{episode}  {shot['id']}", fill="#888888", font=font_small)

        # Center: Character name (only in pillow mode — comfyui has it in the image)
        if not use_comfyui and char_name:
            bbox = draw.textbbox((0, 0), char_name, font=font_title)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((w - tw) // 2, 200), char_name, fill=accent_color, font=font_title)

        # Bottom: Scene description
        if scene_label:
            scene_font = font_sub
            lines = [scene_label[i:i+30] for i in range(0, len(scene_label), 30)]
            for j, line in enumerate(lines[:2]):
                bbox = draw.textbbox((0, 0), line, font=scene_font)
                lw = bbox[2] - bbox[0]
                draw.text(((w - lw) // 2, 520 + j * 36), line, fill="#cccccc", font=scene_font)

        # Bottom: Narration subtitle
        if narration:
            sub_lines = [narration[i:i+45] for i in range(0, len(narration), 45)]
            for j, line in enumerate(sub_lines[:2]):
                bbox = draw.textbbox((0, 0), line, font=font_small)
                lw = bbox[2] - bbox[0]
                draw.text(((w - lw) // 2, 620 + j * 26), line, fill="#999999", font=font_small)

        frame_path = video_dir / f"_frame_{shot['id']}.png"
        img.save(str(frame_path))

        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", str(frame_path),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-t", str(duration),
            "-preset", "ultrafast",
            str(video_file)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            if video_file.exists() and video_file.stat().st_size > 1000:
                video_files.append(str(video_file))
                print(f"  ✅ 片段 {shot['id']}: {video_file.name} ({video_file.stat().st_size} bytes, {duration}s) [{char_name}]")
            else:
                print(f"  ⚠️ 片段 {shot['id']} 生成失败")
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ 片段 {shot['id']} 超时")
        except Exception as e:
            print(f"  ❌ 片段 {shot['id']} 错误: {e}")
        finally:
            frame_path.unlink(missing_ok=True)

    print(f"  ✅ Step 3: 视频生成 → {len(video_files)} 个片段")
    return video_files


def merge_to_silent(video_files, output_dir):
    """Step 4 (silent): 仅拼接视频，无音频 → final_silent.mp4"""
    output_file = output_dir / "final_silent.mp4"

    concat_file = output_dir / "_concat_list.txt"
    with open(concat_file, "w") as f:
        for v in video_files:
            f.write(f"file '{os.path.abspath(v)}'\n")

    concat_cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output_file)
    ]
    subprocess.run(concat_cmd, capture_output=True, check=True)
    concat_file.unlink(missing_ok=True)

    return output_file


def merge_to_final(video_files, audio_files, output_dir):
    """Step 4: 合并视频+音频 → final.mp4"""
    output_file = output_dir / "final.mp4"

    # Step 4a: 拼接所有视频片段
    concat_file = output_dir / "_concat_list.txt"
    with open(concat_file, "w") as f:
        for v in video_files:
            f.write(f"file '{os.path.abspath(v)}'\n")

    temp_video = output_dir / "_temp_video.mp4"
    concat_cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(temp_video)
    ]
    subprocess.run(concat_cmd, capture_output=True, check=True)

    # Step 4b: 拼接所有音频
    if len(audio_files) > 1:
        concat_audio_file = output_dir / "_audio_concat.txt"
        with open(concat_audio_file, "w") as f:
            for a in audio_files:
                f.write(f"file '{os.path.abspath(a)}'\n")
        concat_audio_cmd = [
            FFMPEG, "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_audio_file),
            "-c:a", "aac",
            str(output_dir / "_temp_audio.aac")
        ]
        subprocess.run(concat_audio_cmd, capture_output=True, check=True)
        audio_input = str(output_dir / "_temp_audio.aac")
    else:
        audio_input = audio_files[0]

    # Step 4c: 视频+音频合并
    merge_cmd = [
        FFMPEG, "-y",
        "-i", str(temp_video),
        "-i", audio_input,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest",
        str(output_file)
    ]
    subprocess.run(merge_cmd, capture_output=True, check=True)

    # 清理临时文件
    concat_file.unlink(missing_ok=True)
    temp_video.unlink(missing_ok=True)
    (output_dir / "_temp_audio.aac").unlink(missing_ok=True)
    (output_dir / "_audio_concat.txt").unlink(missing_ok=True)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="短剧端到端管线")
    parser.add_argument("--voice", choices=["say", "nls"], default="say")
    parser.add_argument("--episode", default="03", help="集数编号 (01-06)")
    parser.add_argument("--render", choices=["pillow", "comfyui"], default="pillow", help="视频渲染引擎: pillow=字帧(2/10) comfyui=AI渲染图(5/10)")
    parser.add_argument("--silent", action="store_true")
    parser.add_argument("--sfx", action="store_true", help="启用环境音效混音 (freesound)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    silent_mode = args.silent
    voice_mode = args.voice
    ep_id = args.episode

    # 初始化输出目录
    output_dir, script_dir, audio_dir, video_dir, ep_cfg = init_episode_dirs(ep_id)

    # 加载 .env (NLS keys)
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

    if args.test:
        deps = check_dependencies()
        print("\n🔍 依赖检查:")
        for name, ok in deps.items():
            status = "✅" if ok else "❌"
            print(f"  {status} {name}")
        if all(deps.values()):
            print("\n✅ 所有依赖就绪")
        else:
            missing = [k for k, v in deps.items() if not v]
            print(f"\n⚠️ 缺失依赖: {', '.join(missing)}")
        return

    if args.dry_run:
        print(f"\n📋 Sprint 1.5 管线计划 [EP{ep_id}]:")
        print(f"  Step 1: 从 shuihuzhuan.yaml 生成 EP{ep_id} 剧本 JSON")
        if silent_mode:
            print("  Step 2: [SILENT] 跳过音频生成")
        elif voice_mode == "nls":
            print("  Step 2: 用 NLS TTS 生成旁白音频 (旁白: zhiqi 女声, 5段)")
        else:
            print("  Step 2: 用 macOS say TTS 生成旁白音频 (5段)")
        if args.sfx:
            print("  Step 2.5: 混入环境音效 (freesound)")
        print("  Step 3: 用 ffmpeg 生成视频片段 (5段)")
        if args.render == "comfyui":
            print("          渲染引擎: ComfyUI AI静态图")
        else:
            print("          渲染引擎: Pillow 字幕帧")
        if silent_mode:
            print("  Step 4: 拼接视频 → final_silent.mp4 (无声)")
        else:
            print("  Step 4: 拼接视频+音频 → final.mp4")
        print(f"\n  输出目录: {output_dir}")
        return

    # 获取剧集标题
    import yaml
    with open(PROJECT_ROOT / "stories" / "shuihuzhuan.yaml") as f:
        _story = yaml.safe_load(f)
    ep_title = _story["episodes"][ep_cfg["idx"]]["title"]

    mode_parts = []
    if voice_mode == "nls":
        mode_parts.append("NLS 真人")
    elif silent_mode:
        mode_parts.append("SILENT (无声)")
    else:
        mode_parts.append("有声")
    if args.render == "comfyui":
        mode_parts.append("ComfyUI渲染")
    else:
        mode_parts.append("Pillow字帧")
    if args.sfx:
        mode_parts.append("SFX音效")
    mode_label = "+".join(mode_parts)
    print(f"\n{'='*60}")
    print(f"  🎬 Sprint 1.5: 水浒传 EP{ep_id} 端到端管线 [{mode_label}]")
    print(f"  📖 {ep_title} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    # Step 1
    print("📝 Step 1: 生成剧本...")
    script = generate_script(ep_id, script_dir)

    # Step 2
    if silent_mode:
        print("\n⏭️ Step 2: [SILENT] 跳过音频")
        audio_files = []
    else:
        print(f"\n🎙️ Step 2: 生成旁白音频 [voice={voice_mode}]...")
        audio_files = generate_audio(script, voice_mode=voice_mode, audio_dir=audio_dir)

    # Step 2.5: SFX 混音
    if args.sfx and not silent_mode:
        print("\n🎵 Step 2.5: 环境音效混音 (freesound)...")
        try:
            import sys
            sys.path.insert(0, str(PROJECT_ROOT / "shared"))
            from core.sfx_engine import SFXEngine
            sfx_engine = SFXEngine()
            sfx_output = sfx_engine.process_episode(ep_id, audio_dir, output_dir)
            if sfx_output:
                print(f"  ✅ SFX 混音完成 → {sfx_output.name}")
            else:
                print("  ℹ️ 无SFX处理 (可能缺少API Key或缓存)")
        except Exception as e:
            print(f"  ⚠️ SFX 引擎异常: {e}")

    # Step 3
    print("\n🎥 Step 3: 生成视频片段...")
    video_files = generate_video(script, video_dir=video_dir, render_mode=args.render, ep_id=ep_id)

    # Step 4
    if silent_mode:
        print("\n🔗 Step 4: 拼接为 final_silent.mp4 (无声)...")
        final_file = merge_to_silent(video_files, output_dir)
    else:
        print("\n🔗 Step 4: 合并为 final.mp4...")
        final_file = merge_to_final(video_files, audio_files, output_dir)

    # 验证
    size = final_file.stat().st_size
    duration_cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final_file)]
    try:
        dur = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except:
        dur = "?"

    print(f"\n{'='*60}")
    print(f"  ✅ final.mp4 生成成功!")
    print(f"  📄 路径: {final_file}")
    print(f"  📏 大小: {size:,} bytes")
    print(f"  ⏱️ 时长: {dur}s")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
