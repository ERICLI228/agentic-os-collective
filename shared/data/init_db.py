#!/usr/bin/env python3
"""
SQLite数据库初始化脚本 (v1.2)
彻底修复状态值不匹配问题：使用更宽松的映射逻辑
"""
import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / "agentic-os-collective/shared/data/agentic.db"

# 状态值映射表
STATUS_MAP = {
    "in_progress": "running",
    "running": "running",
    "pending": "pending",
    "created": "pending",
    "completed": "completed",
    "done": "completed",
    "failed": "failed",
    "error": "failed",
    "cancelled": "cancelled",
    "stopped": "cancelled"
}

def normalize_status(status):
    if not status:
        return "pending"
    s = str(status).lower().strip()
    return STATUS_MAP.get(s, "pending")

def init_db():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 彻底重建任务表以确保约束生效
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("""
        CREATE TABLE tasks (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            project TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            metadata TEXT,
            CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled'))
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY,
            task_id TEXT,
            question TEXT NOT NULL,
            options TEXT,
            status TEXT DEFAULT 'pending',
            chosen_option TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            decided_at TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dramas (
            id TEXT PRIMARY KEY,
            title TEXT,
            script TEXT,
            characters TEXT,
            scenes TEXT,
            video_path TEXT,
            audio_path TEXT,
            status TEXT DEFAULT 'scripting',
            project TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT,
            CHECK (status IN ('scripting', 'audio', 'video', 'rendering', 'completed', 'failed'))
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT UNIQUE NOT NULL,
            webhook_url TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            action TEXT,
            details TEXT,
            status TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ 数据库表结构重建完成: {DB_PATH}")

def migrate_json_to_sqlite():
    workspace = Path.home() / ".openclaw/workspace"
    tasks_dir = workspace / "tasks/active"
    completed_dir = workspace / "tasks/completed"
    
    if not tasks_dir.exists():
        print("⚠️  无JSON任务数据可迁移")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    migrated = 0
    all_files = list(tasks_dir.glob("*.json")) + list(completed_dir.glob("*.json"))
    
    for task_file in all_files:
        try:
            with open(task_file) as f:
                task = json.load(f)
            
            # 强制标准化
            raw_status = task.get('status', 'pending')
            norm_status = normalize_status(raw_status)
            
            cursor.execute("""
                INSERT OR REPLACE INTO tasks (id, title, description, project, status, priority, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.get('id', task_file.stem),
                task.get('title', ''),
                task.get('description', ''),
                task.get('project', 'unknown'),
                norm_status,
                task.get('priority', 'medium'),
                task.get('created_at', datetime.now().isoformat()),
                json.dumps(task)
            ))
            
            # 迁移决策点
            for dp in task.get('decision_points', []):
                cursor.execute("""
                    INSERT OR REPLACE INTO decisions (id, task_id, question, options, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    dp.get('id', f"{task['id']}-{dp.get('id','N/A')}"),
                    task['id'],
                    dp.get('question', ''),
                    json.dumps(dp.get('options', [])),
                    dp.get('status', 'pending'),
                    dp.get('created_at', datetime.now().isoformat())
                ))
            
            migrated += 1
        except Exception as e:
            print(f"⚠️  迁移失败 {task_file.name}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ 迁移完成: {migrated}/{len(all_files)} 个任务成功进入数据库")

if __name__ == "__main__":
    init_db()
    migrate_json_to_sqlite()
    print("\n🎉 数据库重建与全量迁移完成！")
