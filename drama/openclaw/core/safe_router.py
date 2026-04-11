#!/usr/bin/env python3
"""
Safe Mode 模型路由器 - 第一批次简化版
功能：读取项目配置返回模型名，配置缺失时自动降级到安全模型
"""
import os
import yaml
from pathlib import Path

PROJECTS_DIR = Path.home() / ".openclaw/projects"
SAFE_MODEL = "ollama/llama3.2"  # 最保守的本地模型

def load_config(project_id: str) -> dict:
    """加载项目配置"""
    config_path = PROJECTS_DIR / project_id / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_model_for_project(project_id: str, role: str = "default") -> str:
    """
    获取指定项目指定角色的模型名
    如果配置缺失或损坏，返回 SAFE_MODEL
    """
    try:
        config = load_config(project_id)
        role_config = config.get('roles', {}).get(role, {})
        return role_config.get('model', SAFE_MODEL)
    except Exception as e:
        print(f"⚠️ [SafeRouter] 配置读取失败，使用安全模型: {e}")
        return SAFE_MODEL

def get_budget_ratio(project_id: str) -> float:
    """获取项目预算占比"""
    try:
        config = load_config(project_id)
        return config.get('project', {}).get('budget_ratio', 0.5)
    except Exception:
        return 0.5  # 均分

# 简单测试
if __name__ == "__main__":
    print("drama default model:", get_model_for_project("drama"))
    print("tk default model:", get_model_for_project("tk"))
    print("drama budget ratio:", get_budget_ratio("drama"))