#!/usr/bin/env python3
"""
决策事件监听器 - 监听决策结果并触发后续脚本执行
"""
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys

EVENT_FILE = Path.home() / ".openclaw/workspace/events/decision_received.json"
CONSUMED_FLAG = Path.home() / ".openclaw/workspace/events/.decision_consumed"

def check_and_trigger():
    """检查是否有新决策事件并触发后续脚本"""
    if not EVENT_FILE.exists():
        return None
    
    try:
        with open(EVENT_FILE, 'r') as f:
            event = json.load(f)
        
        task_id = event.get('task_id')
        choice = event.get('choice')
        decision_id = event.get('decision_id')
        
        print(f"📋 处理决策事件：{task_id} - {choice}")
        
        # 触发对应的后续脚本
        if task_id and task_id.startswith("DRAMA"):
            # 触发短剧流水线下一阶段的脚本
            script_path = Path.home() / ".openclaw/scripts/drama/next_stage.py"
            if script_path.exists():
                subprocess.run([sys.executable, str(script_path), task_id, choice])
            else:
                print(f"⚠️ 未找到后续脚本：{script_path}")
        elif task_id and task_id.startswith("TK"):
            # TK 运营的后续脚本
            script_path = Path.home() / ".openclaw/scripts/tk/next_stage.py"
            if script_path.exists():
                subprocess.run([sys.executable, str(script_path), task_id, choice])
            else:
                print(f"⚠️ 未找到后续脚本：{script_path}")
        
        # 标记事件已消费
        CONSUMED_FLAG.touch()
        EVENT_FILE.unlink(missing_ok=True)
        
        return event
    
    except Exception as e:
        print(f"❌ 处理决策事件失败：{e}")
        return None

if __name__ == "__main__":
    check_and_trigger()