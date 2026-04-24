#!/bin/bash
# 水浒传AI数字短剧 - 一键生成脚本
# 用法: ./make-drama.sh "剧集名称" [比例] [时长]

THEME="${1:-鲁智深倒拔垂杨柳}"
RATIO="${2:-16:9}"
DURATION="${3:-8}"

echo "🎬 水浒传AI数字短剧 - 制作流水线"
echo "================================"
echo "📖 主题: $THEME"
echo "📐 比例: $RATIO"
echo "⏱️ 时长: ${DURATION}秒"
echo ""

# 环境准备
SEEDANCE_DIR=$(ls -d ~/Seedance*/*/ 2>/dev/null | head -1)
# ARK_API_KEY 从 .env 或环境变量读取
if [ -f "$HOME/agentic-os-collective/.env" ]; then
    export $(grep -v '^#' "$HOME/agentic-os-collective/.env" | grep ARK_API_KEY | xargs)
fi
ARK_API_KEY="${ARK_API_KEY:-}"

echo "📝 第1步: 生成剧本 (GLM-4.7)"
echo "----------------------------"
SCRIPT_PROMPT="生成一个30秒的水浒传短视频剧本：$THEME
要求：
1. 幽默风格，现代网感
2. 包含分镜描述（镜头、画面、对白/旁白、音效）
3. 角色：鲁智深、武松、李逵、林冲等
4. 场景：古代中国风格
5. 输出：分镜脚本格式"

# 这里简单输出提示词，实际使用可调用GLM API
echo "$SCRIPT_PROMPT"
echo ""

echo "🎬 第2步: 生成视频 (Seedance 2.0)"
echo "--------------------------------"

cd "$SEEDANCE_DIR" 2>/dev/null && source .venv/bin/activate

python3 << EOF
import os
import time

# 清理代理
for k in ['http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

from volcenginesdkarkruntime import Ark
client = Ark(api_key="$ARK_API_KEY")

prompt = "一位古代中国${THEME}场景，穿古装的人物，古代建筑背景，电影质感，写实风格"

result = client.content_generation.tasks.create(
    model='doubao-seedance-2-0-fast-260128',
    content=[{"type": "text", "text": prompt}],
    ratio='$RATIO',
    duration=$DURATION,
    generate_audio=True,
    watermark=True
)

task_id = result.id
print(f"Task: {task_id}")
print("⏳ 等待生成...")

for i in range(60):
    time.sleep(10)
    status = client.content_generation.tasks.get(task_id=task_id)
    print(f"  {i+1}. {status.status}")
    
    if status.status == 'succeeded':
        print(f"\n✅ 视频生成完成！")
        print(f"🔗 {status.content.video_url}")
        break
    elif status.status == 'failed':
        print("❌ 生成失败")
        break
EOF

echo ""
echo "📦 第3步: 上传TOS (可选)"
echo "-----------------------"
echo "视频已保存在TOS，24小时内有效"
echo ""
echo "================================"
echo "🎉 制作完成！"