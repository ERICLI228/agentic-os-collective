#!/bin/bash
# notify.sh - 通知脚本 (飞书/邮件/Slack等)

title="$1"
message="$2"

# 飞书 Webhook (替换为你自己的)
FEISHU_WEBHOOK=""

if [ -n "$FEISHU_WEBHOHOOK" ]; then
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{
            \"msg_type\": \"text\",
            \"content\": {\"text\": \"$title\n$message\"}
        }" 2>/dev/null
    echo "✅ 飞书通知已发送"
fi

# 打印到控制台 (调试用)
echo "📢 通知: $title"
echo "   $message"

# 保存通知日志
NOTIFY_LOG="$HOME/.agents/skills/proactive-operator/logs/notifications.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] $title | $message" >> "$NOTIFY_LOG"