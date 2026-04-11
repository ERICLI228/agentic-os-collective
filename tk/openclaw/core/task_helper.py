#!/usr/bin/env python3
"""
任务管理工具 - 支持创建任务、添加决策点
"""
from pathlib import Path
from datetime import datetime
import json
import sys
import argparse

TASKS_DIR = Path.home() / ".openclaw/workspace/tasks/active"
MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"

def create_task(project_id: str, title: str, description: str, priority: str = "P1"):
    """创建新任务"""
    task_id = f"{project_id.upper()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    task = {
        "id": task_id,
        "project_id": project_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "stage": "剧本筛选",
        "milestones": [],
        "decision_points": [],
        "created_at": datetime.now().isoformat()
    }
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    task_file = TASKS_DIR / f"{task_id}.json"
    with open(task_file, 'w') as f:
        json.dump(task, f, indent=2)
    return task_id

def add_decision(task_id: str, question: str, options: list, context: str = ""):
    """为任务添加决策点"""
    task_file = TASKS_DIR / f"{task_id}.json"
    if not task_file.exists():
        raise ValueError(f"Task {task_id} not found")
    
    with open(task_file, 'r+') as f:
        task = json.load(f)
        decision = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "question": question,
            "options": options,
            "context": context,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        task["decision_points"].append(decision)
        f.seek(0)
        json.dump(task, f, indent=2)
        f.truncate()
    return decision

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="任务管理工具")
    parser.add_argument("command", choices=["create", "list", "add_decision"])
    parser.add_argument("project_id", help="项目ID（drama/tk）")
    parser.add_argument("title", nargs="?", help="任务标题")
    parser.add_argument("description", nargs="?", help="任务描述")
    parser.add_argument("priority", nargs="?", default="P1", help="优先级")
    parser.add_argument("--task-id", help="任务ID（用于添加决策点）")
    
    args = parser.parse_args()
    
    if args.command == "create":
        if not args.title:
            print("错误：需要指定任务标题")
            sys.exit(1)
        task_id = create_task(args.project_id, args.title, args.description or "", args.priority)
        print(f"✅ 任务已创建：{task_id}")
    elif args.command == "add_decision":
        if not args.task_id or not args.title:
            print("错误：需要指定 --task-id 和问题标题")
            sys.exit(1)
        options = args.description.split(",") if args.description else ["通过", "修改", "驳回"]
        decision = add_decision(args.task_id, args.title, options)
        print(f"✅ 决策点已添加：{decision['id']}")


def get_active_task(project_id: str, status: str = "running"):
    """获取当前活跃的任务（按创建时间排序，返回最新的）"""
    TASKS_DIR = Path.home() / ".openclaw/workspace/tasks/active"
    tasks = []
    
    for f in TASKS_DIR.glob("*.json"):
        try:
            with open(f, 'r') as fp:
                task = json.load(fp)
                if task.get('project_id') == project_id and task.get('status') == status:
                    tasks.append(task)
        except Exception:
            continue
    
    # 按创建时间排序，返回最新的
    if tasks:
        return max(tasks, key=lambda t: t.get('created_at', ''))
    return None


def get_pending_decision_tasks(project_id: str):
    """获取有待决策事项的任务"""
    TASKS_DIR = Path.home() / ".openclaw/workspace/tasks/active"
    tasks = []
    
    for f in TASKS_DIR.glob("*.json"):
        try:
            with open(f, 'r') as fp:
                task = json.load(fp)
                if task.get('project_id') == project_id:
                    decisions = [d for d in task.get('decision_points', []) if d.get('status') == 'pending']
                    if decisions:
                        task['pending_decisions'] = len(decisions)
                        tasks.append(task)
        except Exception:
            continue
    
    return tasks