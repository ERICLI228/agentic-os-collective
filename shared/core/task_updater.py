#!/usr/bin/env python3
"""
任务状态更新工具 - 供业务脚本调用
"""
import json
import fcntl
import sys
from pathlib import Path
from datetime import datetime

ACTIVE_DIR = Path.home() / ".openclaw/workspace/tasks/active"

def update_milestone(task_id: str, milestone_id: str, status: str = "completed"):
    """更新指定任务的里程碑状态"""
    task_file = ACTIVE_DIR / f"{task_id}.json"
    if not task_file.exists():
        print(f"❌ 任务 {task_id} 不存在")
        return False
    
    with open(task_file, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        task = json.load(f)
        
        updated = False
        for m in task.get('milestones', []):
            if m.get('id') == milestone_id:
                m['status'] = status
                if status == 'completed':
                    m['completed_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            # 检查是否所有里程碑完成
            all_done = all(m.get('status') == 'completed' for m in task.get('milestones', []))
            if all_done:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
            
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
        
        fcntl.flock(f, fcntl.LOCK_UN)
        
        if updated:
            print(f"✅ 里程碑 {milestone_id} 已更新为 {status}")
        return updated

def add_decision(task_id: str, question: str, options: list, context: str = ""):
    """为任务添加决策点"""
    task_file = ACTIVE_DIR / f"{task_id}.json"
    if not task_file.exists():
        print(f"❌ 任务 {task_id} 不存在")
        return None
    
    with open(task_file, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        task = json.load(f)
        
        decision = {
            "id": f"DEC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "question": question,
            "options": options,
            "context": context,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        task.setdefault('decision_points', []).append(decision)
        
        f.seek(0)
        json.dump(task, f, ensure_ascii=False, indent=2)
        f.truncate()
        fcntl.flock(f, fcntl.LOCK_UN)
        
        print(f"✅ 决策点已添加: {question[:30]}...")
        return decision['id']

def update_task_status(task_id: str, status: str):
    """更新任务状态"""
    task_file = ACTIVE_DIR / f"{task_id}.json"
    if not task_file.exists():
        print(f"❌ 任务 {task_id} 不存在")
        return False
    
    with open(task_file, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        task = json.load(f)
        task['status'] = status
        if status == 'completed':
            task['completed_at'] = datetime.now().isoformat()
        
        f.seek(0)
        json.dump(task, f, ensure_ascii=False, indent=2)
        f.truncate()
        fcntl.flock(f, fcntl.LOCK_UN)
        
        print(f"✅ 任务状态已更新为 {status}")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法:")
        print("  python3 task_updater.py update <task_id> <milestone_id> [status]")
        print("  python3 task_updater.py decision <task_id> <question> <options>")
        print("  python3 task_updater.py status <task_id> <status>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "update" and len(sys.argv) >= 4:
        task_id = sys.argv[2]
        milestone_id = sys.argv[3]
        status = sys.argv[4] if len(sys.argv) > 4 else "completed"
        update_milestone(task_id, milestone_id, status)
    
    elif cmd == "decision" and len(sys.argv) >= 5:
        task_id = sys.argv[2]
        question = sys.argv[3]
        options = sys.argv[4].split(",")
        add_decision(task_id, question, options)
    
    elif cmd == "status" and len(sys.argv) >= 4:
        task_id = sys.argv[2]
        status = sys.argv[3]
        update_task_status(task_id, status)
    
    else:
        print("无效命令")
        sys.exit(1)