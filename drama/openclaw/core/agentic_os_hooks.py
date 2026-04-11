#!/usr/bin/env python3
"""
Agentic OS 脚本对接钩子 - 所有业务脚本应统一使用此接口
"""
from pathlib import Path
from datetime import datetime
import sys
import json

# 添加 core 目录到路径
sys.path.insert(0, str(Path.home() / ".openclaw/core"))

from task_helper import get_active_task, add_decision, create_task
from progress_logger import log_progress

class ScriptHooks:
    """脚本执行钩子，统一任务追踪接口"""
    
    @staticmethod
    def get_current_task(project_id: str):
        """获取当前活跃任务"""
        return get_active_task(project_id, "running")
    
    @staticmethod
    def log_start(project_id: str, task_id: str, stage: str, context: str):
        """记录任务开始"""
        log_progress(project_id, task_id, f"开始{stage}", f"上下文：{context}", "进行中")
    
    @staticmethod
    def log_end(project_id: str, task_id: str, stage: str, output: str, next_stage: str):
        """记录任务完成"""
        log_progress(project_id, task_id, f"完成{stage}", f"输出：{output}", next_stage)
    
    @staticmethod
    def add_decision_point(task_id: str, question: str, options: list):
        """为当前任务添加决策点"""
        add_decision(task_id, question, options)
    
    @staticmethod
    def create_task(project_id: str, title: str, description: str, priority: str = "P1"):
        """创建新任务"""
        return create_task(project_id, title, description, priority)

if __name__ == "__main__":
    print("✅ ScriptHooks 模块加载成功")