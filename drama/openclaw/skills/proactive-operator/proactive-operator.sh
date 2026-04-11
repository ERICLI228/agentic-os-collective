#!/bin/bash
# proactive-operator.sh - TK东南亚5国 3C运营 Agent (简化版)

set -e

SCRIPT_DIR="$HOME/.agents/skills/proactive-operator"
DATA_DIR="$SCRIPT_DIR/data"
LOG_DIR="$SCRIPT_DIR/logs"
CONFIG_FILE="$SCRIPT_DIR/config.json"

mkdir -p "$DATA_DIR" "$LOG_DIR"
LOG_FILE="$LOG_DIR/operator_$(date +%Y%m%d).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 3C品类
CATEGORIES="laptop phone case earbuds charger smart watch cable usb power bank keyboard mouse speaker"

# 检查TikTok
check_tiktok() {
    log "🎯 TK东南亚3C热门检查..."
    
    for cat in $CATEGORIES; do
        log "  搜索: $cat"
        
        result=$(opencli tiktok search "$cat" --limit 10 -f json 2>/dev/null || echo "[]")
        
        if [ "$result" != "[]" ] && [ -n "$result" ]; then
            echo "$result" > "$DATA_DIR/tiktok_${cat}_$(date +%Y%m%d_%H%M%S).json"
            
            # 检测爆款 (播放>3M)
            echo "$result" | python3 -c "
import json,sys
data = json.load(sys.stdin)
for item in data:
    try:
        p = str(item.get('plays','0')).replace('M','000000').replace('K','000')
        if int(p) > 3000000:
            print(f'HOT:{item.get(\"author\")}:{item.get(\"plays\")}:{item.get(\"desc\",\"\")[:50]}')
    except: pass
" 2>/dev/null | while read -r line; do
                log "  🔥 $line"
            done
        fi
        
        sleep 1
    done
}

# 生成报告
generate_report() {
    report="# TK东南亚3C运营日报 $(date '+%Y-%m-%d')
"
    
    for f in $DATA_DIR/tiktok_*_$(date +%Y%m%d)*.json; do
        [ -f "$f" ] || continue
        cat=$(basename "$f" | sed 's/tiktok_//' | sed 's/_[0-9]*\.json//')
        report+="### $cat\n"
        report+=$(python3 -c "
import json
d=json.load(open('$f'))
for i in d[:3]:
    print(f'- {i.get(\"desc\",\"\")[:50]}: {i.get(\"plays\")}')" 2>/dev/null)
        report+="\n\n"
    done
    
    echo -e "$report" > "$DATA_DIR/report_$(date +%Y%m%d).md"
    log "✅ 报告: $DATA_DIR/report_$(date +%Y%m%d).md"
}

# 主函数
log "========== TK东南亚3C运营 Agent =========="
check_tiktok
generate_report
log "========== 完成 =========="