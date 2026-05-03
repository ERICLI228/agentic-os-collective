#!/bin/bash
# sync-test-to-prod.sh — 将测试环境通过验收的代码同步到生产
set -e

TEST_DIR="/tmp/agentic-os-test"
PROD_DIR="$HOME/agentic-os-collective"

echo "⚠️ 即将把 $TEST_DIR 中的代码同步到 $PROD_DIR"
read -p "确认测试环境已通过全部回归测试？(yes/no) " confirm
if [ "$confirm" != "yes" ]; then
 echo "❌ 取消同步"
 exit 1
fi

# 只同步源码（dashboard/ shared/ scripts/），不同步 .env / 数据库
rsync -av --progress \
 --exclude='.env' \
 --exclude='*.db' \
 --exclude='__pycache__' \
 "$TEST_DIR/dashboard/" "$PROD_DIR/dashboard/"
rsync -av --progress \
 --exclude='__pycache__' \
 "$TEST_DIR/shared/" "$PROD_DIR/shared/"
rsync -av --progress \
 --exclude='__pycache__' \
 "$TEST_DIR/scripts/" "$PROD_DIR/scripts/"

echo "✅ 生产代码已更新。请手动重启生产服务 (Flask :5001 / Vite :5173)"
