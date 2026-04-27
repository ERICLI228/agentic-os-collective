#!/usr/bin/env bash
# 设置 wiki Lint 每周定时巡检
# 每周一 9:00 自动运行

CRON_JOB="0 9 * * 1 cd $HOME/agentic-os-collective && python3 shared/scripts/wiki-lint.py >> shared/knowledge/wiki/outputs/lint-cron.log 2>&1"

(crontab -l 2>/dev/null | grep -v "wiki-lint"; echo "$CRON_JOB") | crontab -
echo "✓ Lint cron installed (weekly Mon 9am)"
echo "  Job: $CRON_JOB"
