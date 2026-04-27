#!/bin/bash
# 会话归档 - 由 CLAUDE.md 规则在会话结束时自动调用
# 提取关键决策 → wiki/log.md + wiki/outputs/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/.."

python3 "$PROJECT_DIR/shared/scripts/session-archiver.py"
echo "  → 归档完成: $(date '+%Y-%m-%d %H:%M')"
