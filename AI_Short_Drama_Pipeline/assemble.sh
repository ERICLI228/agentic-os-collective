#!/bin/bash

VIDEO_DIR="assets/videos"
AUDIO_DIR="assets/audio"
OUTPUT="wusong_episode01_final.mp4"

echo "Starting final assembly..."

# Fix for empty/invalid files: Skip missing or empty clips
VALID_CLIPS=0
rm -f inputs.txt
for f in $VIDEO_DIR/clip_*.mp4; do
    if [ -s "$f" ]; then
        echo "file '$f'" >> inputs.txt
        ((VALID_CLIPS++))
    fi
done

if [ $VALID_CLIPS -eq 0 ]; then
    echo "Error: No valid video clips found. Please ensure fetch_assets.py downloaded real mp4 files."
    exit 1
fi

echo "Concatenating $VALID_CLIPS video clips..."
ffmpeg -y -f concat -safe 0 -i inputs.txt -c copy temp_video.mp4

# Audio processing: Convert all to wav first to avoid "Invalid data" errors
echo "Processing audio tracks..."
rm -f audio_list.txt
for f in $AUDIO_DIR/vo_*.mp3; do
    if [ -s "$f" ]; then
        # Convert mp3 to wav for stable concatenation
        filename=$(basename "$f")
        ffmpeg -y -i "$f" "assets/audio/${filename%.mp3}.wav"
        echo "file 'assets/audio/${filename%.mp3}.wav'" >> audio_list.txt
    fi
done

if [ ! -f audio_list.txt ]; then
    echo "Error: No valid audio files found."
    exit 1
fi

ffmpeg -y -f concat -safe 0 -i audio_list.txt -c copy temp_audio.wav

echo "Applying final merge and color grading..."
ffmpeg -y -i temp_video.mp4 -i temp_audio.wav \
    -vf "eq=contrast=1.1:saturation=1.2" \
    -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest \
    $OUTPUT

echo "Assembly complete! Final video: $OUTPUT"
rm -f inputs.txt audio_list.txt temp_video.mp4 temp_audio.wav
