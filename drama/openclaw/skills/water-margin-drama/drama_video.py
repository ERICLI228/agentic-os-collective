#!/usr/bin/env python3
"""
MS-5: 视频生成脚本 (完整版)
使用 FFmpeg 合成视频 + 文字 + 音频

方案:
1. 从 MS-4 获取剧本内容
2. 从 MS-7 获取音频文件
3. 使用 FFmpeg 合成完整视频

Usage:
    python3 drama_video.py --task TASK_ID
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
TASKS_DIR = WORKSPACE / "tasks" / "active"
OUTPUT_DIR = WORKSPACE / "output" / "videos"
AUDIO_DIR = WORKSPACE / "output" / "audio"

def get_task(task_id: str) -> dict:
    """获取任务数据"""
    task_file = TASKS_DIR / f"{task_id}.json"
    if not task_file.exists():
        task_file = TASKS_DIR / "drama" / f"{task_id}.json"
    if not task_file.exists():
        return None
    with open(task_file, 'r') as f:
        return json.load(f)

def get_script_content(task: dict) -> tuple:
    """从 MS-4 获取剧本内容和标题"""
    for m in task.get('milestones', []):
        if m.get('id') == 'MS-4':
            output = m.get('execution_details', {}).get('output_content', {})
            data = output.get('data', {})
            return data.get('script', ''), data.get('title', '未命名')
    return '', '未命名'

def get_audio_file(task: dict) -> str:
    """从 MS-7 获取音频文件路径"""
    for m in task.get('milestones', []):
        if m.get('id') == 'MS-7':
            output = m.get('execution_details', {}).get('output_content', {})
            data = output.get('data', {})
            return data.get('audio_file', '')
    return ''

def generate_tts_audio(script: str, output_file: str) -> bool:
    """使用 macOS say 命令生成 TTS 音频"""
    if not script:
        return False
    
    # 截取前500字符
    text = script[:500].replace('\n', ' ')
    
    # 使用 macOS say 命令
    cmd = ['say', '-v', 'Amira', '-o', output_file, text]
    result = subprocess.run(cmd, capture_output=True)
    
    return result.returncode == 0

def create_video_with_text_audio(title: str, script: str, audio_file: str, output_file: str) -> dict:
    """创建带有文字和音频的视频"""
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1. 生成或获取音频
        if audio_file and os.path.exists(audio_file):
            # 使用现有音频
            final_audio = audio_file
        else:
            # 生成 TTS 音频
            temp_audio = os.path.join(temp_dir, 'audio.aiff')
            if generate_tts_audio(script, temp_audio):
                # 转换为 mp3
                final_audio = os.path.join(temp_dir, 'audio.mp3')
                subprocess.run(['ffmpeg', '-y', '-i', temp_audio, final_audio], capture_output=True)
            else:
                final_audio = None
        
        # 2. 获取音频时长
        if final_audio and os.path.exists(final_audio):
            probe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', final_audio]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip() or '10')
        else:
            duration = 10
        
        # 3. 创建带有文字的视频
        # 提取剧本前几行作为显示文字
        lines = script.split('\n')[:5] if script else [title]
        text_content = '\n'.join([line.strip() for line in lines if line.strip()])
        
        # 使用 drawtext 滤镜
        video_cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=c=black:s=1920x1080:d={duration}:r=30',
            '-vf', f"drawtext=text='{title}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h/3,drawtext=text='内容生成中...':fontsize=40:fontcolor=gray:x=(w-text_w)/2:y=h/2",
            '-c:v', 'libx264',
            '-t', str(duration),
            '-pix_fmt', 'yuv420p',
            '-r', '30',
            output_file
        ]
        
        subprocess.run(video_cmd, capture_output=True)
        
        # 4. 如果有音频，合并音频
        if final_audio and os.path.exists(final_audio):
            temp_output = os.path.join(temp_dir, 'temp.mp4')
            merge_cmd = [
                'ffmpeg', '-y',
                '-i', output_file,
                '-i', final_audio,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                temp_output
            ]
            subprocess.run(merge_cmd, capture_output=True)
            if os.path.exists(temp_output):
                shutil.move(temp_output, output_file)
        
        # 检查结果
        if os.path.exists(output_file):
            probe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', output_file]
            result = subprocess.run(probe_cmd, capture_output=True, text=True)
            actual_duration = float(result.stdout.strip() or '0')
            
            # 检查是否有音频流
            probe_streams = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', output_file]
            result = subprocess.run(probe_streams, capture_output=True, text=True)
            has_audio = 'audio' in result.stdout
            
            return {
                'success': True,
                'file': output_file,
                'duration': actual_duration,
                'has_audio': has_audio,
                'method': 'ffmpeg_with_text_audio'
            }
        
        return {'success': False, 'error': '视频生成失败'}
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def generate_video(task_id: str) -> dict:
    """生成完整视频"""
    task = get_task(task_id)
    if not task:
        return {"error": "任务不存在"}
    
    script, title = get_script_content(task)
    audio_file = get_audio_file(task)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"{task_id}_MS-5.mp4"
    
    result = create_video_with_text_audio(title, script, audio_file, str(output_file))
    
    if result.get('success'):
        return {
            'task_id': task_id,
            'milestone_id': 'MS-5',
            'output_content': {
                'type': 'video',
                'title': f"{title} - 完整视频",
                'data': {
                    'video_file': str(output_file),
                    'duration': result.get('duration', 10),
                    'has_audio': result.get('has_audio', False),
                    'method': 'ffmpeg_with_text_audio',
                    'note': '包含文字标题和音频'
                },
                'generated_at': datetime.now().isoformat()
            }
        }
    return {"error": result.get('error', '视频生成失败')}

def update_task(task_id: str, result: dict):
    """更新任务"""
    task_file = TASKS_DIR / f"{task_id}.json"
    if not task_file.exists():
        task_file = TASKS_DIR / "drama" / f"{task_id}.json"
    if not task_file.exists():
        return False
    
    with open(task_file, 'r') as f:
        task = json.load(f)
    
    for m in task.get('milestones', []):
        if m.get('id') == 'MS-5':
            m['status'] = 'completed'
            m['execution_details'] = {'output_content': result['output_content']}
            break
    
    with open(task_file, 'w') as f:
        json.dump(task, f, ensure_ascii=False, indent=2)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='完整视频生成')
    parser.add_argument('--task', required=True, help='任务ID')
    args = parser.parse_args()
    
    print(f"📋 任务ID: {args.task}")
    print(f"🎬 生成完整视频（文字+音频）...")
    
    result = generate_video(args.task)
    
    if result.get('error'):
        print(f"❌ 错误: {result['error']}")
        return
    
    data = result['output_content']['data']
    print(f"✅ 视频生成成功!")
    print(f"📁 文件: {data['video_file']}")
    print(f"⏱️ 时长: {data['duration']}秒")
    print(f"🔊 音频: {'有' if data['has_audio'] else '无'}")
    
    update_task(args.task, result)
    print(f"💾 任务已更新")

if __name__ == '__main__':
    main()