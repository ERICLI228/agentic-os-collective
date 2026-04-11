#!/usr/bin/env python3
"""
水浒传AI数字短剧 - 音视频合成系统
TTS配音 + FFmpeg合成
"""

import os
import sys
import subprocess
import uuid
import shutil

# 配置
TEMP_DIR = os.path.expanduser("~/.openclaw/skills/water-margin-drama/temp")
OUTPUT_DIR = os.path.expanduser("~/.openclaw/skills/water-margin-drama/output")

# 确保目录存在
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def cleanup():
    """清理临时文件"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)

def text_to_speech_mac(text: str, voice: str = "Ting-Ting", output_path: str = None) -> str:
    """
    使用macOS say命令生成语音
    免费方案，支持中文
    """
    if output_path is None:
        output_path = os.path.join(TEMP_DIR, f"audio_{uuid.uuid4().hex[:8]}.m4a")
    
    # 清理旧文件
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # 使用say命令生成语音
    # -v: voice, -o: output file, -f: input text file
    text_file = os.path.join(TEMP_DIR, f"text_{uuid.uuid4().hex[:8]}.txt")
    
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # 生成m4a格式
    cmd = ['say', '-v', voice, '-f', text_file, '-o', output_path.replace('.m4a', ''), '--file-format=m4af']
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # 修正扩展名
        actual_file = output_path.replace('.m4a', '.m4a')
        if not os.path.exists(actual_file):
            # 尝试其他扩展名
            for ext in ['.m4a', '.aiff', '.wav']:
                alt_file = output_path.replace('.m4a', ext)
                if os.path.exists(alt_file):
                    shutil.move(alt_file, output_path)
                    break
        
        os.remove(text_file)
        print(f"✅ 语音生成: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 语音生成失败: {e}")
        return None

def text_to_speech_elevenlabs(text: str, voice_id: str = "rachel", api_key: str = None) -> str:
    """
    使用ElevenLabs生成语音 (付费方案)
    需要API key
    """
    if not api_key:
        print("⚠️ 需要ElevenLabs API key")
        return None
    
    output_path = os.path.join(TEMP_DIR, f"audio_{uuid.uuid4().hex[:8]}.mp3")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    import urllib.request
    import json
    
    data = json.dumps({
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    })
    
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        with open(output_path, 'wb') as f:
            f.write(resp.read())
        print(f"✅ ElevenLabs语音: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ ElevenLabs错误: {e}")
        return None

def merge_video_audio(video_path: str, audio_path: str, output_path: str = None) -> str:
    """
    使用FFmpeg合并视频和音频
    """
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        return None
    
    if not os.path.exists(audio_path):
        print(f"❌ 音频文件不存在: {audio_path}")
        return None
    
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"final_{uuid.uuid4().hex[:8]}.mp4")
    
    # FFmpeg命令：替换音频轨道
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 合成完成: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg错误: {e.stderr}")
        return None

def add_background_music(video_path: str, music_path: str = None, output_path: str = None, 
                        volume: float = 0.3, ducking: bool = True) -> str:
    """
    添加背景音乐 (混音)
    
    Args:
        video_path: 视频文件路径
        music_path: 背景音乐路径 (可选，为None时使用内置音乐)
        output_path: 输出路径
        volume: BGM音量 (0.0-1.0), 默认0.3
        ducking: 是否启用音频闪避 (人声出现时降低BGM)
    """
    if not os.path.exists(video_path):
        print(f"❌ 视频不存在: {video_path}")
        return None
    
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"final_bgm_{uuid.uuid4().hex[:8]}.mp4")
    
    # 如果没有指定背景音乐，使用默认静音处理
    if not music_path or not os.path.exists(music_path):
        print("⚠️ 未指定背景音乐，仅处理音视频合并")
        shutil.copy(video_path, output_path)
        return output_path
    
    print(f"🎵 添加背景音乐: {os.path.basename(music_path)}")
    print(f"   音量: {int(volume*100)}%")
    print(f"   闪避: {'启用' if ducking else '禁用'}")
    
    if ducking:
        # 使用音频闪避: 人声时降低BGM
        # 简单实现: 降低BGM音量
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', music_path,
            '-filter_complex',
            f'[1:a]volume={volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first:weights=1 {volume}[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]
    else:
        # 简单混音
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', music_path,
            '-filter_complex',
            f'[1:a]volume={volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ BGM混音完成: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 混音失败: {e.stderr}")
        return None


def mix_with_voice_and_bgm(video_path: str, voice_path: str, music_path: str = None,
                           voice_volume: float = 1.0, bgm_volume: float = 0.2,
                           output_path: str = None) -> str:
    """
    完整混音: 视频 + 人声配音 + 背景音乐
    
    Args:
        video_path: 视频文件
        voice_path: 人声配音文件
        music_path: 背景音乐 (可选)
        voice_volume: 人声音量 (0.0-1.0)
        bgm_volume: BGM音量 (0.0-1.0)
        output_path: 输出路径
    """
    if not os.path.exists(video_path):
        print(f"❌ 视频不存在: {video_path}")
        return None
    if not os.path.exists(voice_path):
        print(f"❌ 配音不存在: {voice_path}")
        return None
    
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"final_mix_{uuid.uuid4().hex[:8]}.mp4")
    
    print("🎛️ 完整混音: 视频 + 配音 + BGM")
    print(f"   视频: {os.path.basename(video_path)}")
    print(f"   配音: {os.path.basename(voice_path)}")
    print(f"   人声音量: {int(voice_volume*100)}%")
    print(f"   BGM音量: {int(bgm_volume*100)}%")
    
    if music_path and os.path.exists(music_path):
        # 三路混音: 视频 + 人声 + BGM
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', voice_path,
            '-i', music_path,
            '-filter_complex',
            f'[1:a]volume={voice_volume}[voice];[2:a]volume={bgm_volume}[bgm];[voice][bgm]amix=inputs=2:duration=first[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]
    else:
        # 两路混音: 视频 + 人声
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', voice_path,
            '-filter_complex',
            f'[1:a]volume={voice_volume}[voice]',
            '-map', '0:v',
            '-map', '[voice]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 混音完成: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 混音失败: {e.stderr}")
        return None


def create_test_bgm(output_path: str = None) -> str:
    """
    创建测试用背景音乐 (使用系统音频生成简单旋律)
    由于无法直接生成音乐，返回提示信息
    """
    print("⚠️ 建议使用以下免费BGM资源:")
    print("   - https://pixabay.com/zh/music/ (免费商用)")
    print("   - https://mixkit.co/free-music/ (免费商用)")
    print("   - YouTube音频库 (免费)")
    print("   或下载背景音乐后指定路径")
    return None

def generate_dubbing(script: str, video_duration: int = 8) -> str:
    """
    生成配音：根据视频时长调整语速
    """
    # 估算文字朗读时间 (中文约150字/分钟)
    char_count = len(script)
    estimated_time = char_count / 150 * 60  # 秒
    
    # 如果文字太长，需要调整语速
    if estimated_time > video_duration:
        # 压缩文字
        ratio = video_duration / estimated_time
        target_chars = int(char_count * ratio * 0.8)  # 留20%余量
        script = script[:target_chars] + "..."
        print(f"⚠️ 文字已压缩: {char_count} -> {len(script)} 字符")
    
    # 生成语音
    audio_path = text_to_speech_mac(script, voice="Ting-Ting")
    return audio_path

def full_workflow(video_url: str, script: str, output_name: str = None) -> str:
    """
    完整工作流：下载视频 → 生成配音 → 合成 → 输出
    """
    print("🎬 音视频合成流水线")
    print("="*50)
    
    # 1. 下载视频
    print("\n📥 第1步: 下载视频...")
    video_path = os.path.join(TEMP_DIR, f"source_{uuid.uuid4().hex[:8]}.mp4")
    
    # 使用curl下载
    cmd = ['curl', '-L', '-o', video_path, video_url]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 视频下载: {video_path}")
    except:
        print("❌ 视频下载失败，使用本地路径")
        video_path = video_url  # 可能是本地文件
    
    # 2. 生成配音
    print("\n🎤 第2步: 生成配音...")
    audio_path = generate_dubbing(script)
    if not audio_path:
        return None
    
    # 3. 合成
    print("\n🎵 第3步: 音视频合成...")
    if output_name:
        output_path = os.path.join(OUTPUT_DIR, f"{output_name}.mp4")
    else:
        output_path = os.path.join(OUTPUT_DIR, f"drama_{uuid.uuid4().hex[:8]}.mp4")
    
    final_path = merge_video_audio(video_path, audio_path, output_path)
    
    # 4. 清理
    print("\n🧹 清理临时文件...")
    cleanup()
    
    print("\n" + "="*50)
    print(f"🎉 完成！最终文件: {final_path}")
    
    return final_path

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📖 用法:")
        print("  python drama_audio.py --tts \"需要配音的文字\"")
        print("  python drama_audio.py --merge video.mp4 audio.m4a")
        print("  python drama_audio.py --full video_url \"配音脚本\" output_name")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "--tts":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "你好，我是水浒传AI数字短剧系统"
        text_to_speech_mac(text)
        
    elif action == "--merge":
        if len(sys.argv) >= 4:
            video = sys.argv[2]
            audio = sys.argv[3]
            merge_video_audio(video, audio)
        else:
            print("用法: --merge video.mp4 audio.m4a")
            
    elif action == "--bgm":
        # 添加背景音乐
        if len(sys.argv) >= 3:
            video = sys.argv[2]
            music = sys.argv[3] if len(sys.argv) > 3 else None
            volume = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
            add_background_music(video, music, volume=volume)
        else:
            print("用法: --bgm video.mp4 [music.mp3] [volume=0.3]")
            print("示例: --bgm output.mp3 bgm.mp3 0.2")
            
    elif action == "--mix":
        # 完整混音: 视频 + 配音 + BGM
        if len(sys.argv) >= 4:
            video = sys.argv[2]
            voice = sys.argv[3]
            music = sys.argv[4] if len(sys.argv) > 4 else None
            voice_vol = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
            bgm_vol = float(sys.argv[6]) if len(sys.argv) > 6 else 0.2
            mix_with_voice_and_bgm(video, voice, music, voice_vol, bgm_vol)
        else:
            print("用法: --mix video.mp4 voice.m4a [music.mp3] [voice_vol] [bgm_vol]")
            print("示例: --mix video.mp4 voice.m4a bgm.mp3 1.0 0.2")
            
    elif action == "--full":
        if len(sys.argv) >= 4:
            video_url = sys.argv[2]
            script = sys.argv[3]
            output_name = sys.argv[4] if len(sys.argv) > 4 else None
            full_workflow(video_url, script, output_name)
        else:
            print("用法: --full video_url script output_name")

if __name__ == "__main__":
    main()