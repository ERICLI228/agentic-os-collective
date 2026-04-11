#!/usr/bin/env python3
"""
产出物记录工具
"""
import json
import fcntl
import sys
from pathlib import Path
from datetime import datetime

ACTIVE_DIR = Path.home() / ".openclaw/workspace/tasks/active"

def add_artifact(task_id: str, artifact_type: str, name: str, path: str, url: str = None):
    """为任务添加产出物记录"""
    task_file = ACTIVE_DIR / f"{task_id}.json"
    if not task_file.exists():
        print(f"❌ 任务 {task_id} 不存在")
        return False
    
    with open(task_file, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        task = json.load(f)
        
        artifact = {
            "type": artifact_type,
            "name": name,
            "path": path,
            "url": url or f"file://{path}",
            "created_at": datetime.now().isoformat()
        }
        task.setdefault('artifacts', []).append(artifact)
        
        f.seek(0)
        json.dump(task, f, ensure_ascii=False, indent=2)
        f.truncate()
        fcntl.flock(f, fcntl.LOCK_UN)
        
        print(f"✅ 产出物已记录: {name}")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: artifact_recorder.py <task_id> <type> <name> <path> [url]")
        print("示例: artifact_recorder.py DRAMA-20260410-001 video 武松打虎第1集.mp4 /data/drama/output/episode_01.mp4")
        sys.exit(1)
    add_artifact(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)