#!/usr/bin/env python3
"""
SQLite数据库初始化脚本 (v1.3 — 安全加固版)
修复：增强输入校验，防止恶意JSON数据绕过数据库约束
"""
import sqlite3
import json
import re
import os
from pathlib import Path
from datetime import datetime

# ── 从统一配置加载（如 .env 不存在则用默认值）
try:
    from shared.config import config
    DB_PATH = config.DB_PATH
except ImportError:
    DB_PATH = Path.home() / "agentic-os-collective/shared/data/agentic.db"

# ── 合法枚举值白名单
STATUS_MAP = {
    "in_progress": "running",  "running":   "running",
    "pending":     "pending",  "created":   "pending",
    "completed":   "completed","done":      "completed",
    "failed":      "failed",   "error":     "failed",
    "cancelled":   "cancelled","stopped":   "cancelled",
}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
VALID_PROJECTS   = {"drama", "tk", "yt", "unknown"}
TASK_ID_RE       = re.compile(r'^[A-Za-z0-9\-]{1,64}$')


def normalize_status(status) -> str:
    if not status:
        return "pending"
    return STATUS_MAP.get(str(status).lower().strip(), "pending")


def _safe_str(value, max_len: int = 500, default: str = "") -> str:
    if value is None:
        return default
    return str(value)[:max_len]


def validate_task_data(task: dict, fallback_id: str) -> dict:
    """严格校验和清洗从 JSON 文件读取的任务数据"""
    raw_id = task.get("id", fallback_id)
    if not TASK_ID_RE.match(str(raw_id)):
        raise ValueError(f"非法任务ID格式: {raw_id!r}")

    priority = task.get("priority", "medium")
    if priority not in VALID_PRIORITIES:
        priority = "medium"

    project = task.get("project", "unknown")
    if project not in VALID_PROJECTS:
        project = "unknown"

    created_at = task.get("created_at", "")
    try:
        datetime.fromisoformat(str(created_at))
    except (ValueError, TypeError):
        created_at = datetime.now().isoformat()

    return {
        "id":          str(raw_id),
        "title":       _safe_str(task.get("title", ""), max_len=200),
        "description": _safe_str(task.get("description", ""), max_len=2000),
        "project":     project,
        "status":      normalize_status(task.get("status", "pending")),
        "priority":    priority,
        "created_at":  str(created_at),
    }


def init_db():
    """建表 — 全部静态DDL，无任何用户输入拼接"""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn   = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("""
        CREATE TABLE tasks (
            id           TEXT PRIMARY KEY,
            title        TEXT,
            description  TEXT,
            project      TEXT,
            status       TEXT DEFAULT 'pending',
            priority     TEXT DEFAULT 'medium',
            created_at   TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at   TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            metadata     TEXT,
            CHECK (status   IN ('pending','running','completed','failed','cancelled')),
            CHECK (priority IN ('low','medium','high','critical'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id            TEXT PRIMARY KEY,
            task_id       TEXT,
            question      TEXT NOT NULL,
            options       TEXT,
            status        TEXT DEFAULT 'pending',
            chosen_option TEXT,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            decided_at    TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dramas (
            id         TEXT PRIMARY KEY,
            title      TEXT,
            script     TEXT,
            characters TEXT,
            scenes     TEXT,
            video_path TEXT,
            audio_path TEXT,
            status     TEXT DEFAULT 'scripting',
            project    TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            metadata   TEXT,
            CHECK (status IN ('scripting','audio','video','rendering','completed','failed'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhooks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name  TEXT UNIQUE NOT NULL,
            webhook_url TEXT NOT NULL,
            enabled     INTEGER DEFAULT 1,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_logs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id    TEXT,
            action     TEXT,
            details    TEXT,
            status     TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ 数据库表结构重建完成: {DB_PATH}")


def migrate_json_to_sqlite():
    """迁移 — 参数化查询 + 输入校验"""
    workspace = Path.home() / ".openclaw/workspace"
    tasks_dir = workspace / "tasks/active"
    done_dir  = workspace / "tasks/completed"

    if not tasks_dir.exists():
        print("⚠️  无JSON任务数据可迁移")
        return

    conn   = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    migrated, skipped = 0, 0
    all_files = list(tasks_dir.glob("*.json")) + list(done_dir.glob("*.json"))

    for task_file in all_files:
        try:
            with open(task_file, encoding="utf-8") as f:
                task = json.load(f)

            v = validate_task_data(task, task_file.stem)          # 严格校验

            cursor.execute("""                                     -- 全参数化，无拼接
                INSERT OR REPLACE INTO tasks
                    (id, title, description, project, status, priority, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (v["id"], v["title"], v["description"], v["project"],
                  v["status"], v["priority"], v["created_at"], json.dumps(task)))

            for dp in task.get("decision_points", []):
                cursor.execute("""
                    INSERT OR REPLACE INTO decisions
                        (id, task_id, question, options, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    _safe_str(dp.get("id", f"{v['id']}-dp"), max_len=64),
                    v["id"],
                    _safe_str(dp.get("question", ""), max_len=500),
                    json.dumps(dp.get("options", [])),
                    normalize_status(dp.get("status", "pending")),
                    str(dp.get("created_at", datetime.now().isoformat())),
                ))
            migrated += 1

        except ValueError as e:
            print(f"⚠️  校验失败，跳过 {task_file.name}: {e}")
            skipped += 1
        except Exception as e:
            print(f"⚠️  迁移失败 {task_file.name}: {e}")
            skipped += 1

    conn.commit()
    conn.close()
    print(f"✅ 迁移完成: {migrated} 成功 / {skipped} 跳过 / {len(all_files)} 总计")


if __name__ == "__main__":
    init_db()
    migrate_json_to_sqlite()
    print("\n🎉 数据库重建与全量迁移完成！")
