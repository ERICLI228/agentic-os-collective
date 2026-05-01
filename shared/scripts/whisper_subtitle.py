#!/usr/bin/env python3
"""
Whisper Subtitle Generator — S3-2

Generates SRT subtitle files from audio/video using OpenAI Whisper.
Fallback to mock mode when whisper is not available.

Usage:
    python3 shared/scripts/whisper_subtitle.py --input audio.wav --output subtitle.srt
    python3 shared/scripts/whisper_subtitle.py --input episode_07.mp4 --output sub.srt --model small
"""

import argparse
import sys
import os
import subprocess
from pathlib import Path
from datetime import timedelta


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)
    hours = total_ms // 3600000
    minutes = (total_ms % 3600000) // 60000
    secs = (total_ms % 60000) // 1000
    ms = total_ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def get_audio_duration(input_path: str) -> float:
    """Get audio/video duration via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", input_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            import json
            dur = json.loads(result.stdout).get("format", {}).get("duration")
            if dur:
                return float(dur)
    except Exception:
        pass
    return 0.0


def extract_audio(input_path: str, output_path: str) -> bool:
    """Extract audio from video using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-vn", "-acodec", "pcm_s16le",
             "-ar", "16000", "-ac", "1", output_path],
            capture_output=True, text=True, timeout=120
        )
        return Path(output_path).exists()
    except Exception:
        return False


def generate_with_whisper(audio_path: str, model_name: str = "small", language: str = "zh") -> list:
    """Generate subtitle segments using OpenAI Whisper."""
    import whisper

    print(f"Loading whisper model '{model_name}'...", file=sys.stderr)
    model = whisper.load_model(model_name)

    print(f"Transcribing audio: {audio_path}", file=sys.stderr)
    result = model.transcribe(audio_path, language=language, word_timestamps=False)

    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })

    return segments


def generate_mock_subtitle(audio_path: str, segment_duration: float = 5.0) -> list:
    """Generate placeholder SRT when whisper is unavailable."""
    duration = get_audio_duration(audio_path)
    if duration <= 0:
        # Fallback: assume 60 seconds
        duration = 60.0

    print(f"⚠️  whisper not available, generating mock subtitle ({duration:.1f}s)", file=sys.stderr)

    segments = []
    idx = 0
    current = 0.0
    while current < duration:
        end = min(current + segment_duration, duration)
        segments.append({
            "start": current,
            "end": end,
            "text": f"[字幕片段 {idx + 1} - whisper 未安装]"
        })
        idx += 1
        current = end

    return segments


def write_srt(segments: list, output_path: str):
    """Write segments to SRT file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            f.write(f"{i + 1}\n")
            f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")

    print(f"SRT written to: {output_path} ({len(segments)} segments)", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Generate SRT subtitle from audio/video using Whisper")
    parser.add_argument("--input", "-i", required=True, help="Input audio or video file path")
    parser.add_argument("--output", "-o", required=True, help="Output SRT file path")
    parser.add_argument("--model", "-m", default="small", help="Whisper model size (tiny/base/small/medium/large)")
    parser.add_argument("--language", "-l", default="zh", help="Language code (default: zh)")
    parser.add_argument("--mock-duration", type=float, default=5.0,
                        help="Mock segment duration in seconds (default: 5.0)")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    # Validate input
    if not Path(input_path).exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Determine audio path (extract if video)
    audio_path = input_path
    is_video = Path(input_path).suffix.lower() in ('.mp4', '.mov', '.avi', '.mkv', '.webm')

    if is_video:
        # Check if input has audio track
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "a",
                 "-show_entries", "stream=index", "-of", "csv=p=0", input_path],
                capture_output=True, text=True, timeout=10
            )
            if not result.stdout.strip():
                # No audio track, create mock subtitle based on video duration
                print(f"⚠️  Video has no audio track, generating mock subtitle", file=sys.stderr)
                duration = get_audio_duration(input_path)
                segments = []
                idx = 0
                current = 0.0
                while current < duration:
                    end = min(current + args.mock_duration, duration)
                    segments.append({
                        "start": current,
                        "end": end,
                        "text": f"[字幕片段 {idx + 1}]"
                    })
                    idx += 1
                    current = end
                write_srt(segments, output_path)
                sys.exit(0)
        except Exception:
            pass

        # Extract audio for whisper
        temp_audio = str(Path(output_path).with_suffix(".wav"))
        if extract_audio(input_path, temp_audio):
            audio_path = temp_audio

    # Try whisper first, fallback to mock
    segments = []
    whisper_available = False

    try:
        import whisper
        whisper_available = True
    except ImportError:
        pass

    if whisper_available:
        try:
            segments = generate_with_whisper(audio_path, args.model, args.language)
        except Exception as e:
            print(f"⚠️  Whisper transcription failed: {e}", file=sys.stderr)
            whisper_available = False

    if not whisper_available:
        segments = generate_mock_subtitle(audio_path, args.mock_duration)

    # Write SRT
    write_srt(segments, output_path)

    # Cleanup temp audio
    if audio_path != input_path and Path(audio_path).exists():
        try:
            Path(audio_path).unlink()
        except Exception:
            pass

    # Print SRT content to stdout for API response
    with open(output_path, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
