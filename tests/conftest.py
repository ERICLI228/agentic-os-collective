"""
Pytest 共享受件配置
"""
import json
import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def task_dir():
    """返回任务目录"""
    return Path.home() / ".openclaw/workspace/tasks/active"

@pytest.fixture
def sample_drama_task(task_dir):
    """返回短剧示例任务"""
    for task_file in task_dir.glob("DRAMA-*.json"):
        with open(task_file) as f:
            task = json.load(f)
        if "武松" in task.get('title', ''):
            return task
    return None

@pytest.fixture
def sample_tk_task(task_dir):
    """返回TK示例任务"""
    for task_file in task_dir.glob("TK-*.json"):
        with open(task_file) as f:
            task = json.load(f)
        return task
    return None

@pytest.fixture
def test_config():
    """返回测试配置"""
    return {
        "min_script_length": 1000,
        "min_data_completeness": 0.95,
        "test_timeout": 300
    }