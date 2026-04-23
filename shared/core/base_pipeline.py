#!/usr/bin/env python3
"""
流水线抽象基类 (v1.0)
drama / tk / yt 等所有业务线均继承此类，消除重复的任务加载/保存/里程碑更新逻辑。
"""
import json
import fcntl
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

ACTIVE_DIR = Path.home() / ".openclaw/workspace/tasks/active"


class BasePipeline(ABC):
    """所有业务线流水线的公共基类"""

    def __init__(self, task_id: str):
        self.task_id   = task_id
        self.task_data = self._load_task()
        if not self.validate_task():
            raise ValueError(
                f"任务 {task_id!r} 不属于 {self.__class__.__name__} 业务线，"
                f"期望前缀: {self.task_prefix()}"
            )

    # ── 子类必须实现 ────────────────────────────────────────────────────

    @abstractmethod
    def task_prefix(self) -> str:
        """返回本业务线任务ID前缀，如 'TK-', 'DS-', 'YT-'"""
        ...

    @abstractmethod
    def get_skill_dir(self) -> Path:
        """返回本业务线 skill 脚本目录"""
        ...

    # ── 公共方法（drama / tk / yt 共用）───────────────────────────────

    def validate_task(self) -> bool:
        """校验任务ID是否属于本业务线"""
        return self.task_id.upper().startswith(self.task_prefix().upper())

    def update_milestone(
        self,
        milestone_id: str,
        status: str,
        content: Optional[dict] = None,
        decision_required: bool = False,
        decision_options: Optional[list] = None,
    ) -> bool:
        """更新里程碑状态（线程安全，使用文件锁）"""
        task_file = ACTIVE_DIR / f"{self.task_id}.json"
        if not task_file.exists():
            logger.error(f"任务文件不存在: {task_file}")
            return False

        with open(task_file, "r+", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                task = json.load(f)
                for m in task.get("milestones", []):
                    if m.get("id") == milestone_id:
                        m["status"]     = status
                        m["updated_at"] = datetime.now().isoformat()
                        if content:
                            m.setdefault("execution_details", {}).update(content)
                        if decision_required:
                            m["decision_required"] = True
                            m["decision_options"]  = decision_options or []
                        break
                f.seek(0)
                json.dump(task, f, ensure_ascii=False, indent=2)
                f.truncate()
                self.task_data = task   # 刷新内存缓存
                logger.info(f"[{self.task_id}] 里程碑 {milestone_id} → {status}")
                return True
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def get_milestone(self, milestone_id: str) -> Optional[dict]:
        """获取指定里程碑数据"""
        for m in self.task_data.get("milestones", []):
            if m.get("id") == milestone_id:
                return m
        return None

    def log_error(self, milestone_id: str, error: str) -> None:
        self.update_milestone(milestone_id, "failed", {"error": error})
        logger.error(f"[{self.task_id}/{milestone_id}] {error}")

    # ── 私有方法 ─────────────────────────────────────────────────────────

    def _load_task(self) -> dict:
        task_file = ACTIVE_DIR / f"{self.task_id}.json"
        if not task_file.exists():
            raise FileNotFoundError(f"任务文件不存在: {task_file}")
        with open(task_file, encoding="utf-8") as f:
            return json.load(f)
