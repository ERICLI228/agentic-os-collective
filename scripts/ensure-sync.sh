#!/bin/bash
# ensure-sync.sh — 双向环境同步校验
# 检查 /tmp/agentic-os-test 与 ~/agentic-os-collective 的关键文件是否一致
# 用法: bash scripts/ensure-sync.sh

PROD=~/agentic-os-collective
TEST=/tmp/agentic-os-test
DRIFT=0

FILES=(
  dashboard/task_board.html
  shared/task_wizard.py
  CLAUDE.md
  SAFETY_RULES.md
  reports/PRD-v3.7.21.md
  shared/knowledge/wiki/log.md
  shared/knowledge/wiki/index.md
)

for f in "${FILES[@]}"; do
  p="$PROD/$f"
  t="$TEST/$f"
  if [ ! -f "$p" ]; then echo "  ⚠️  PROD missing: $f"; DRIFT=1; continue; fi
  if [ ! -f "$t" ]; then echo "  ⚠️  TEST missing: $f"; DRIFT=1; continue; fi
  p_md5=$(md5 -q "$p" 2>/dev/null)
  t_md5=$(md5 -q "$t" 2>/dev/null)
  if [ "$p_md5" != "$t_md5" ]; then
    echo "  ❌ DRIFT: $f"
    DRIFT=1
  else
    echo "  ✅ $f"
  fi
done

if [ $DRIFT -eq 0 ]; then
  echo ""
  echo "✅ 全部 ${#FILES[@]} 个文件已同步"
else
  echo ""
  echo "❌ 存在不同步文件，请运行: cp ~/agentic-os-collective/<file> /tmp/agentic-os-test/<file>"
  exit 1
fi
