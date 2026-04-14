#!/usr/bin/env python3
"""
MCP Task Server - 连接 OpenCode 与 Agentic OS API
"""
import json
import sys
import requests
from typing import Dict, Any

API_BASE = "http://localhost:5001"

def get_tasks() -> Dict[str, Any]:
    """获取任务列表"""
    resp = requests.get(f"{API_BASE}/api/tasks", timeout=5)
    return resp.json()

def get_task_detail(task_id: str) -> Dict[str, Any]:
    """获取任务详情"""
    resp = requests.get(f"{API_BASE}/api/task/{task_id}", timeout=5)
    return resp.json()

def update_milestone(task_id: str, milestone_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """更新里程碑"""
    resp = requests.patch(
        f"{API_BASE}/api/task/{task_id}/milestone/{milestone_id}",
        json=data,
        timeout=5
    )
    return resp.json()

def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """处理MCP请求"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "list_tools":
        return {
            "tools": [
                {"name": "get_tasks", "description": "获取所有任务列表"},
                {"name": "get_task_detail", "description": "获取任务详情"},
                {"name": "update_milestone", "description": "更新里程碑状态"}
            ]
        }
    elif method == "get_tasks":
        return get_tasks()
    elif method == "get_task_detail":
        return get_task_detail(params.get("task_id"))
    elif method == "update_milestone":
        return update_milestone(
            params.get("task_id"),
            params.get("milestone_id"),
            params.get("data", {})
        )
    else:
        return {"error": f"Unknown method: {method}"}

def main():
    """MCP Server主循环（stdio模式）"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()