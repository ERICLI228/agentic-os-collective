#!/usr/bin/env python3
"""
短剧视频合成器 — v3.5 Sprint 1.4

合并视频片段 + 配音轨 + 字幕 → 输出最终 MP4。

特点:
  - 文件不存在时优雅退出（不抛 traceback）
  - ffmpeg 不可用时给出明确提示
  - 支持分步检查和合并

用法:
  python3 drama/openclaw/core/drama_merge.py \
    --video "scene1.mp4 scene2.mp4" \
    --audio "narration.mp3" \
    --output "episode_1.mp4"

  python3 drama/openclaw/core/drama_merge.py --help
  python3 drama/openclaw/core/drama_merge.py --check  # 检查 ffmpeg 可用性
"""

import sys
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# ffmpeg 路径
FFMPEG_PATH = "/opt/homebrew/Cellar/ffmpeg/8.1_1/bin/ffmpeg"
import os
os.environ["PATH"] = f"{Path(FFMPEG_PATH).parent}:{os.environ.get('PATH', '')}"


def check_ffmpeg():
    """检查 ffmpeg 是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_files(files_str):
    """检查所有输入文件是否存在"""
    files = [f.strip() for f in files_str.split() if f.strip()]
    missing = []
    for f in files:
        p = Path(f)
        if not p.is_absolute():
            p = PROJECT_ROOT / f
        if not p.exists():
            missing.append(str(p))
    return missing


def merge_video_audio(video_files, audio_file, output_file, subtitle_file=None):
    """合并视频+音频 → 最终 MP4"""
    video_list = [f.strip() for f in video_files.split() if f.strip()]
    subprocess.run(["ffmpeg", "-version"], capture_output=True)
    
    # 如果有多个视频片段，先拼接
    if len(video_list) > 1:
        concat_file = Path(output_file).parent / "_concat_list.txt"
        with open(concat_file, "w") as f:
            for v in video_list:
                f.write(f"file '{v}'\n")
        
        temp_video = str(Path(output_file).parent / "_temp_concat.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file), "-c", "copy", temp_video
        ], check=True)
        
        concat_file.unlink(missing_ok=True)
        video_input = temp_video
    else:
        video_input = video_list[0]

    # 合并视频+音频
    cmd = [
        "ffmpeg", "-y",
        "-i", video_input,
        "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest"
    ]

    if subtitle_file:
        cmd += ["-vf", f"subtitles={subtitle_file}"]

    cmd.append(output_file)
    subprocess.run(cmd, check=True)

    # 清理临时文件
    if len(video_list) > 1:
        Path(video_input).unlink(missing_ok=True)

    return True


def run_full_pipeline(episode_id="wusong_dahu"):
    """
    --run 模式: 调用 pipeline_ep01.py 跑通完整管线
    剧本 → 角色设计 → 配音 → 视频 → 合成 → final.mp4
    """
    pipeline_script = Path(__file__).parent / "pipeline_ep01.py"
    if not pipeline_script.exists():
        print(f"❌ 管线脚本不存在: {pipeline_script}")
        sys.exit(1)
    
    # 直接执行管线
    result = subprocess.run(
        [sys.executable, str(pipeline_script)],
        cwd=str(PROJECT_ROOT),
        timeout=300
    )
    
    # 验证输出
    output_file = Path.home() / ".agentic-os" / "episode_01" / "final.mp4"
    if output_file.exists() and output_file.stat().st_size > 0:
        print(f"\n✅ 验证通过: {output_file} ({output_file.stat().st_size:,} bytes)")
        return True
    else:
        print("\n❌ final.mp4 未生成或为空")
        return False


def main():
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
        print(__doc__)
        return

    if "--run" in sys.argv:
        if not check_ffmpeg():
            print("❌ ffmpeg 不可用，请安装: brew install ffmpeg")
            sys.exit(1)
        print("\n🚀 Sprint 1.5: 短剧第一集端到端管线")
        print("   剧本 → 角色设计 → 配音 → 视频 → 合成\n")
        success = run_full_pipeline()
        sys.exit(0 if success else 1)

    if "--check" in sys.argv:
        ok = check_ffmpeg()
        print(f"ffmpeg: {'✅ 可用' if ok else '❌ 不可用 (brew install ffmpeg)'}")
        return

    if not check_ffmpeg():
        print("❌ ffmpeg 不可用，请安装: brew install ffmpeg")
        sys.exit(1)

    video_files = None
    audio_file = None
    subtitle_file = None
    output_file = "final.mp4"

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--video" and i + 1 < len(sys.argv):
            video_files = sys.argv[i + 1]; i += 2
        elif arg == "--audio" and i + 1 < len(sys.argv):
            audio_file = sys.argv[i + 1]; i += 2
        elif arg == "--subtitle" and i + 1 < len(sys.argv):
            subtitle_file = sys.argv[i + 1]; i += 2
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]; i += 2
        else:
            i += 1

    if not video_files:
        print("❌ 需要 --video 参数")
        sys.exit(1)

    if not audio_file:
        print("❌ 需要 --audio 参数")
        sys.exit(1)

    # 文件检查
    all_files = f"{video_files} {audio_file}"
    if subtitle_file:
        all_files += f" {subtitle_file}"

    missing = check_files(all_files)
    if missing:
        print(f"❌ 以下文件不存在，无法合成:")
        for f in missing:
            print(f"   {f}")
        print("\n跳过合成，请先确保所有素材就绪。")
        sys.exit(1)

    try:
        merge_video_audio(video_files, audio_file, output_file, subtitle_file)
        print(f"✅ 合成完成: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ ffmpeg 合成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
