#!/usr/bin/env python3
"""
发布审批硬约束 — v3.5 Sprint 0.4

所有发布动作必须先通过 check_approval(task_id)，不通过则抛出 PublishBlockedError。
触发条件（双条件检查）：
  1. 环境变量 MIAOSHOW_PUBLISH_ENABLED == "true"
  2. 任务 JSON 中 human_approved == true

用法:
  from shared.publish_gate import check_approval
  check_approval("TK-20260429-001")  # 不通过则抛异常

  # 或者直接调用
  python3 shared/publish_gate.py TK-20260429-001  # 检查单个任务
  MIAOSHOW_PUBLISH_ENABLED=true python3 shared/publish_gate.py TK-20260429-001
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime


class PublishBlockedError(Exception):
    """发布被阻止异常 — 任何发布代码捕获此异常应立即停止"""
    pass


# 任务存储目录（与 task_wizard.py 共享）
ACTIVE_DIR = Path.home() / ".openclaw" / "workspace" / "tasks" / "active"


def _find_task_file(task_id: str) -> Path:
    """按 task_id 查找任务文件（文件名可能与 id 不同）"""
    # 精确匹配
    exact = ACTIVE_DIR / f"{task_id}.json"
    if exact.exists():
        return exact
    # 模糊匹配：遍历所有 JSON 找 id 字段
    for f in ACTIVE_DIR.glob('*.json'):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
                if data.get('id') == task_id:
                    return f
        except Exception:
            pass
    raise FileNotFoundError(f"任务文件不存在: {task_id}")


def _load_task(task_id: str) -> dict:
    """加载任务 JSON"""
    task_file = _find_task_file(task_id)
    with open(task_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_approval(task_id: str) -> bool:
    """
    发布前双条件检查。任一条件不满足则抛出 PublishBlockedError。

    条件 1: MIAOSHOW_PUBLISH_ENABLED 环境变量必须为 "true"
    条件 2: 任务必须有 human_approved: true

    Returns:
        True — 审批通过，允许发布

    Raises:
        PublishBlockedError — 审批未通过，禁止发布
    """
    # 条件 1: 环境变量
    env_val = os.environ.get("MIAOSHOW_PUBLISH_ENABLED", "false")
    if env_val.lower() != "true":
        raise PublishBlockedError(
            f"🚫 发布被阻止: MIAOSHOW_PUBLISH_ENABLED={env_val}（需要 'true'）\n"
            f"   这是硬性安全约束，禁止自动发布。\n"
            f"   如需发布，请设置: MIAOSHOW_PUBLISH_ENABLED=true"
        )

    # 条件 2: 人工审批
    task = _load_task(task_id)
    if not task.get("human_approved", False):
        decision_status = task.get("decision_status", "not_requested")
        raise PublishBlockedError(
            f"🚫 发布被阻止: 任务 {task_id} 未获得人工审批\n"
            f"   当前决策状态: {decision_status}\n"
            f"   请通过飞书卡片或驾驶舱界面完成审批后再发布"
        )

    # 通过
    approved_at = task.get("decision_at", "unknown")
    approved_by = task.get("decision_by", "unknown")
    print(f"✅ 发布审批通过: {task_id} (审批人: {approved_by}, 时间: {approved_at})")
    return True


def log_publish_attempt(task_id: str, success: bool, error: str = ""):
    """记录发布尝试（审计日志）"""
    log_dir = Path.home() / ".agentic-os" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "publish_audit.log"
    entry = {
        "task_id": task_id,
        "timestamp": datetime.now().isoformat(),
        "approved": success,
        "error": error if not success else ""
    }
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("用法: python3 publish_gate.py <task_id>")
        print("  MIAOSHOW_PUBLISH_ENABLED=true python3 publish_gate.py TK-20260429-001")
        sys.exit(1)

    task_id = sys.argv[1]

    try:
        check_approval(task_id)
        log_publish_attempt(task_id, success=True)
    except PublishBlockedError as e:
        log_publish_attempt(task_id, success=False, error=str(e))
        print(str(e))
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
