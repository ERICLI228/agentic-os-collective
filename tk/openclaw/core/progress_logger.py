#!/usr/bin/env python3
"""
进度日志写入器 - 支持分项目追加
"""
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
PROGRESS_LOG = WORKSPACE / "tasks/progress.txt"

def log_progress(project_id: str, task_id: str, action: str, result: str = "", notes: str = ""):
    """追加一条进度记录"""
    PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{project_id.upper()}] [{task_id}] {action}"
    if result:
        entry += f" | 结果: {result}"
    if notes:
        entry += f" | 备注: {notes}"
    entry += "\n"
    
    with open(PROGRESS_LOG, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(f"✅ 进度已记录: {entry.strip()}")

if __name__ == "__main__":
    log_progress("drama", "DRAMA-20260410-001", "完成剧本筛选", "3个候选剧本", "人工审核中")