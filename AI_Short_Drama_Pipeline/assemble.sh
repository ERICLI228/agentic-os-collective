#!/bin/bash
# AI短剧剪辑合成 (FR-DR-008) — FFmpeg-based assembly
# 用法: ./assemble.sh <scene_dir> <audio_dir> <output.mp4>
# 功能: 将分镜视频按序拼接 + 合成配音 + 加片头片尾

set -e

SCENE_DIR="${1:-assets/videos}"
AUDIO_DIR="${2:-assets/audio}"
OUTPUT="${3:-output/final_$(date +%Y%m%d_%H%M%S).mp4}"
TEMP_DIR="/tmp/drama_merge_$$"

mkdir -p "$TEMP_DIR" "$(dirname "$OUTPUT")"

echo "🎬 FR-DR-008: AI短剧剪辑合成"
echo "  分镜目录: $SCENE_DIR"
echo "  音频目录: $AUDIO_DIR"
echo "  输出: $OUTPUT"

# 1. 拼接分镜视频
scene_files=($(ls "$SCENE_DIR"/*.mp4 2>/dev/null | sort))
if [ ${#scene_files[@]} -eq 0 ]; then
    echo "⚠️  无分镜视频，生成占位黑场..."
    ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=3 -c:v libx264 -pix_fmt yuv420p "$TEMP_DIR/placeholder.mp4" -loglevel error
    scene_files=("$TEMP_DIR/placeholder.mp4")
fi

# 生成 concat 列表
concat_list="$TEMP_DIR/concat.txt"
> "$concat_list"
for f in "${scene_files[@]}"; do
    echo "file '$f'" >> "$concat_list"
done

echo "  📐 拼接 ${#scene_files[@]} 个分镜..."
ffmpeg -y -f concat -safe 0 -i "$concat_list" -c copy "$TEMP_DIR/merged_video.mp4" -loglevel error

# 2. 合成配音 (如有)
if [ -d "$AUDIO_DIR" ] && [ "$(ls "$AUDIO_DIR"/*.m4a 2>/dev/null)" ]; then
    echo "  🎙️  合成配音..."
    audio_concat="$TEMP_DIR/audio_concat.txt"
    > "$audio_concat"
    for f in "$AUDIO_DIR"/*.m4a; do
        echo "file '$f'" >> "$audio_concat"
    done
    ffmpeg -y -f concat -safe 0 -i "$audio_concat" -c copy "$TEMP_DIR/full_audio.m4a" -loglevel error
    ffmpeg -y -i "$TEMP_DIR/merged_video.mp4" -i "$TEMP_DIR/full_audio.m4a" \
        -c:v copy -c:a aac -shortest -map 0:v:0 -map 1:a:0 "$OUTPUT" -loglevel error
else
    echo "  ⚠️  无配音文件，仅输出视频"
    cp "$TEMP_DIR/merged_video.mp4" "$OUTPUT"
fi

# 3. 清理
rm -rf "$TEMP_DIR"

echo "✅ 合成完成: $OUTPUT"
echo "  大小: $(du -sh "$OUTPUT" | cut -f1)"
