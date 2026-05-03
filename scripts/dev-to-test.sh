#!/bin/bash
# dev-to-test.sh — DEV → TEST 同步（AI 可执行，合并到 test 分支前验证用）
# 用法: bash scripts/dev-to-test.sh
set -e

DEV=/tmp/agentic-os-dev
TEST=/tmp/agentic-os-test

FILES=(
  dashboard/task_board.html
  shared/task_wizard.py
  CLAUDE.md
  SAFETY_RULES.md
  reports/PRD-v3.7.21.md
  shared/knowledge/wiki/log.md
  shared/knowledge/wiki/index.md
)

echo "🔧 DEV → 🧪 TEST 同步中..."
for f in "${FILES[@]}"; do
  cp "$DEV/$f" "$TEST/$f" 2>/dev/null && echo "  📋 $f" || echo "  ⚠️  SKIP $f"
done

# Restart test Flask
kill $(lsof -ti :5002) 2>/dev/null
sleep 1
cd "$TEST/shared"
PYTHONPATH="$TEST/shared" API_PORT=5002 nohup python3 task_wizard.py > /tmp/test-flask-5002.log 2>&1 &
sleep 2
curl -s http://localhost:5002/api/status > /dev/null 2>&1 && echo "  ✅ Test Flask :5002 已重启" || echo "  ⚠️  Test Flask 启动可能失败"

echo ""
echo "✅ DEV → TEST 同步完成"
echo "⏭  下一步: 在 :5002 验证 → 人工审核 → sync-test-to-prod.sh"
