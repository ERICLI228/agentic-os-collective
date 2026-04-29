"""
水浒传AI数字短剧 — 音视频合成系统 (NLS-only TTS)
Aliyun NLS TTS (资源包 NLSTTSBAG-xxx) + FFmpeg 合成
"""
import os, sys, subprocess, uuid, shutil
from pathlib import Path
from aliyun_nls import synthesize

TEMP_DIR = os.path.expanduser("~/.openclaw/skills/water-margin-drama/temp")
OUTPUT_DIR = os.path.expanduser("~/.openclaw/skills/water-margin-drama/output")
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def cleanup():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)


def text_to_speech(text: str, voice: str = "zhiming", output_path: str = None) -> str:
    return synthesize(text, voice, output_path)


def merge_video_audio(video_path: str, audio_path: str, output_path: str = None) -> str:
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}"); return None
    if not os.path.exists(audio_path):
        print(f"❌ 音频文件不存在: {audio_path}"); return None
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"final_{uuid.uuid4().hex[:8]}.mp4")
    cmd = ['ffmpeg', '-y', '-i', video_path, '-i', audio_path,
           '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
           '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 合成完成: {output_path}"); return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg错误: {e.stderr}"); return None


def add_background_music(video_path: str, music_path: str = None, output_path: str = None,
                        volume: float = 0.3, ducking: bool = True) -> str:
    if not os.path.exists(video_path):
        print(f"❌ 视频不存在: {video_path}"); return None
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"final_bgm_{uuid.uuid4().hex[:8]}.mp4")
    if not music_path or not os.path.exists(music_path):
        print("⚠️ 未指定背景音乐，仅处理音视频合并")
        shutil.copy(video_path, output_path); return output_path
    vol = ducking and f'[1:a]volume={volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first:weights=1 {volume}[aout]' or \
          f'[1:a]volume={volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]'
    cmd = ['ffmpeg', '-y', '-i', video_path, '-i', music_path,
           '-filter_complex', vol, '-map', '0:v', '-map', '[aout]',
           '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ BGM混音完成: {output_path}"); return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 混音失败: {e.stderr}"); return None


def generate_dubbing(script: str, video_duration: int = 8) -> str:
    char_count = len(script)
    estimated_time = char_count / 150 * 60
    if estimated_time > video_duration:
        ratio = video_duration / estimated_time
        target_chars = int(char_count * ratio * 0.8)
        script = script[:target_chars] + "..."
        print(f"⚠️ 文字已压缩: {char_count} -> {len(script)} 字符")
    return text_to_speech(script)


def full_workflow(video_url: str, script: str, output_name: str = None) -> str:
    print("🎬 音视频合成流水线 (NLS-only)");
    print("=" * 50)
    video_path = os.path.join(TEMP_DIR, f"source_{uuid.uuid4().hex[:8]}.mp4")
    cmd = ['curl', '-L', '-o', video_path, video_url]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 视频下载: {video_path}")
    except:
        print("❌ 视频下载失败，使用本地路径")
        video_path = video_url
    audio_path = generate_dubbing(script)
    if not audio_path:
        return None
    if output_name:
        output_path = os.path.join(OUTPUT_DIR, f"{output_name}.mp4")
    else:
        output_path = os.path.join(OUTPUT_DIR, f"drama_{uuid.uuid4().hex[:8]}.mp4")
    final_path = merge_video_audio(video_path, audio_path, output_path)
    cleanup()
    return final_path


def mix_with_voice_and_bgm(video_path, voice_path, music_path=None,
                           voice_volume=1.0, bgm_volume=0.2, output_path=None):
    if not os.path.exists(video_path) or not os.path.exists(voice_path):
        print("❌ 视频或配音不存在"); return None
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"final_mix_{uuid.uuid4().hex[:8]}.mp4")
    if music_path and os.path.exists(music_path):
        cmd = ['ffmpeg', '-y', '-i', video_path, '-i', voice_path, '-i', music_path,
               '-filter_complex',
               f'[1:a]volume={voice_volume}[voice];[2:a]volume={bgm_volume}[bgm];[voice][bgm]amix=inputs=2:duration=first[aout]',
               '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path]
    else:
        cmd = ['ffmpeg', '-y', '-i', video_path, '-i', voice_path,
               '-filter_complex', f'[1:a]volume={voice_volume}[voice]',
               '-map', '0:v', '-map', '[voice]', '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 混音完成: {output_path}"); return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 混音失败: {e.stderr}"); return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法:")
        print("  python drama_audio.py --tts \"文字\"")
        print("  python drama_audio.py --merge video.mp4 audio.mp3")
        print("  python drama_audio.py --full video_url \"脚本\" output_name")
        sys.exit(1)
    action = sys.argv[1]
    if action == "--tts":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "你好，我是水浒传AI数字短剧系统"
        text_to_speech(text)
    elif action == "--merge":
        if len(sys.argv) >= 4:
            merge_video_audio(sys.argv[2], sys.argv[3])
    elif action == "--bgm":
        video = sys.argv[2]; music = sys.argv[3] if len(sys.argv) > 3 else None
        vol = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
        add_background_music(video, music, volume=vol)
    elif action == "--mix":
        if len(sys.argv) >= 4:
            mix_with_voice_and_bgm(sys.argv[2], sys.argv[3],
                                   sys.argv[4] if len(sys.argv) > 4 else None,
                                   float(sys.argv[5]) if len(sys.argv) > 5 else 1.0,
                                   float(sys.argv[6]) if len(sys.argv) > 6 else 0.2)
    elif action == "--full":
        if len(sys.argv) >= 4:
            full_workflow(sys.argv[2], sys.argv[3],
                          sys.argv[4] if len(sys.argv) > 4 else None)


if __name__ == "__main__":
    main()
