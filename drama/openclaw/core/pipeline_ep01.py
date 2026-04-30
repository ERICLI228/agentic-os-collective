#!/usr/bin/env python3
"""
短剧第一集端到端管线 - Sprint 1.5

管线: 剧本 → 角色设计 → 配音 → 视频 → 合成

用法:
  python3 pipeline_ep01.py                  # 跑完整管线 (macOS say)
  python3 pipeline_ep01.py --voice nls      # 阿里云 NLS 真人配音
  python3 pipeline_ep01.py --silent         # 纯视频(无声)
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

# Episode 映射 (按 shuihuzhuan.yaml 顺序)
EPISODE_MAP = {
    "01": {"idx": 0, "dir": "episode_01"},
    "02": {"idx": 1, "dir": "episode_02"},
    "03": {"idx": 2, "dir": "episode_03", "scene_key": "景阳冈"},
    "04": {"idx": 3, "dir": "episode_04"},
    "05": {"idx": 4, "dir": "episode_05"},
    "06": {"idx": 5, "dir": "episode_06"},
}

# ── ffmpeg 路径 (Mac brew 不在默认 PATH) ──
FFMPEG_BIN = "/opt/homebrew/Cellar/ffmpeg/8.1_1/bin/ffmpeg"
FFPROBE_BIN = "/opt/homebrew/Cellar/ffmpeg/8.1_1/bin/ffprobe"
os.environ["PATH"] = f"{Path(FFMPEG_BIN).parent}:{os.environ.get('PATH', '')}"
FFMPEG = FFMPEG_BIN if Path(FFMPEG_BIN).exists() else "ffmpeg"
FFPROBE = FFPROBE_BIN if Path(FFPROBE_BIN).exists() else "ffprobe"


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


def generate_script(ep_id="03", script_dir=None):
    """Step 1: 生成剧本 JSON"""
    import yaml

    story_file = PROJECT_ROOT / "stories" / "shuihuzhuan.yaml"
    with open(story_file) as f:
        story = yaml.safe_load(f)

    ep_cfg = EPISODE_MAP.get(ep_id, EPISODE_MAP["03"])
    ep = story["episodes"][ep_cfg["idx"]]
    scene_key = ep_cfg.get("scene_key")
    scene = story["scenes"].get(scene_key, "") if scene_key else ep.get("title", "")

    # 分镜脚本
    character = ep.get("character", "武松")
    script = {
        "episode_id": ep["id"],
        "title": ep["title"],
        "character": character,
        "scene": scene_key or ep.get("title", ""),
        "scene_description": scene,
        "duration_seconds": 30,
        "generated_at": datetime.now().isoformat(),
        "shots": [
            {
                "id": "shot_01",
                "time_range": "0-5s",
                "type": "establishing",
                "visual": "景阳冈山路,夕阳西下,古松参天,远处酒旗飘扬",
                "narration": "话说武松来到景阳冈前,见一酒旗迎风飘扬,上书'三碗不过冈'五个大字。",
                "mood": "肃穆"
            },
            {
                "id": "shot_02",
                "time_range": "5-12s",
                "type": "action",
                "visual": "武松手提哨棒大步上山,肌肉紧绷,目光如电",
                "narration": "武松喝了十八碗酒,趁着酒兴,一步步走上景阳冈来。",
                "mood": "紧张"
            },
            {
                "id": "shot_03",
                "time_range": "12-20s",
                "type": "climax",
                "visual": "猛虎从乱草丛中猛然跃出,狂风大作,武松翻身闪避",
                "narration": "忽听一阵狂风,乱草丛中跳出一只吊睛白额大虫,直往武松扑来!",
                "mood": "惊险"
            },
            {
                "id": "shot_04",
                "time_range": "20-27s",
                "type": "resolution",
                "visual": "武松骑在虎背上,双拳如雨,老虎挣扎无力",
                "narration": "武松奋起平生之力,按住虎头,提起铁锤般大小的拳头,尽平生之力只顾打。",
                "mood": "激昂"
            },
            {
                "id": "shot_05",
                "time_range": "27-30s",
                "type": "closing",
                "visual": "武松站在被打死的老虎旁,夕阳余晖,英雄气概",
                "narration": "这一打,打出了一位打虎英雄,威名远扬。",
                "mood": "豪迈"
            }
        ]
    }

    output_file = script_dir / f"script_ep{ep_id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    print(f"  ✅ Step 1: 剧本生成 ({ep_id}) → {output_file}")
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


def generate_video(script, video_dir=None):
    """Step 3: 生成视频片段 (ffmpeg 静态帧+文字叠加)"""
    if video_dir is None:
        video_dir = VIDEO_DIR
    video_files = []
    colors = ["0x1a1a2e", "0x16213e", "0x0f3460", "0x533483", "0x2c3e50"]

    for i, shot in enumerate(script["shots"]):
        video_file = video_dir / f"{shot['id']}.mp4"
        duration = 5 if i < 4 else 3  # 前4个各5s,最后一个3s
        bg_color = colors[i % len(colors)]

        # 用 ffmpeg 生成纯色视频片段 (drawtext 需要 libfreetype, 用简单颜色过渡代替)
        cmd = [
            FFMPEG, "-y",
            "-f", "lavfi", "-i", f"color=c={bg_color}:s=1280x720:d={duration},format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            str(video_file)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            if video_file.exists() and video_file.stat().st_size > 1000:
                video_files.append(str(video_file))
                print(f"  ✅ 片段 {shot['id']}: {video_file.name} ({video_file.stat().st_size} bytes, {duration}s)")
            else:
                print(f"  ⚠️ 片段 {shot['id']} 生成失败")
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ 片段 {shot['id']} 超时")
        except Exception as e:
            print(f"  ❌ 片段 {shot['id']} 错误: {e}")

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
    parser.add_argument("--silent", action="store_true")
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
        print("  Step 3: 用 ffmpeg 生成视频片段 (5段)")
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

    # Step 3
    print("\n🎥 Step 3: 生成视频片段...")
    video_files = generate_video(script, video_dir=video_dir)

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
