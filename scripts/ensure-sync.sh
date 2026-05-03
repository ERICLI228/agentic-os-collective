#!/bin/bash
# ensure-sync.sh — 三环境同步状态检查
# check DEV↔TEST↔PROD 所有关键文件是否一致
# 用法: bash scripts/ensure-sync.sh [--dev|--test|--prod|--all]

set -e

DEV=/tmp/agentic-os-dev
TEST=/tmp/agentic-os-test
PROD=~/agentic-os-collective

FILES=(
  dashboard/task_board.html
  shared/task_wizard.py
  CLAUDE.md
  SAFETY_RULES.md
  reports/PRD-v3.7.21.md
  shared/knowledge/wiki/log.md
  shared/knowledge/wiki/index.md
)

check_pair() {
  local A="$1" B="$2" label="$3" drift=0
  for f in "${FILES[@]}"; do
    local af="$A/$f" bf="$B/$f"
    if [ ! -f "$af" ]; then echo "  ⚠️  MISSING $label-A: $f"; drift=1; continue; fi
    if [ ! -f "$bf" ]; then echo "  ⚠️  MISSING $label-B: $f"; drift=1; continue; fi
    local a_md5=$(md5 -q "$af" 2>/dev/null)
    local b_md5=$(md5 -q "$bf" 2>/dev/null)
    if [ "$a_md5" != "$b_md5" ]; then
      echo "  ❌ DRIFT: $f"
      drift=1
    else
      echo "  ✅ $f"
    fi
  done
  return $drift
}

# Default: check test↔prod
PAIR="${1:---prod}"
case "$PAIR" in
  --dev)
    echo "🔧 DEV ↔ TEST 同步状态"
    check_pair "$DEV" "$TEST" "DEV↔TEST" && echo "  ✅ 同步" || echo "  ❌ 不同步"
    ;;
  --test|--prod)
    echo "🧪 TEST ↔ 🚀 PROD 同步状态"
    check_pair "$TEST" "$PROD" "TEST↔PROD" && echo "  ✅ 同步" || echo "  ❌ 不同步"
    ;;
  --all)
    echo "🔧 DEV ↔ TEST 同步状态"
    check_pair "$DEV" "$TEST" "DEV↔TEST" && echo "  ✅ 同步" || echo "  ❌ 不同步"
    echo ""
    echo "🧪 TEST ↔ 🚀 PROD 同步状态"
    check_pair "$TEST" "$PROD" "TEST↔PROD" && echo "  ✅ 同步" || echo "  ❌ 不同步"
    ;;
  *)
    echo "用法: ensure-sync.sh [--dev|--test|--prod|--all]"
    echo "  --dev  检查 DEV ↔ TEST"
    echo "  --test 检查 TEST ↔ PROD (默认)"
    echo "  --all  检查全链路 DEV↔TEST↔PROD"
    ;;
esac
