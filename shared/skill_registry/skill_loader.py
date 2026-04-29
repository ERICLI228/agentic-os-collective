#!/usr/bin/env python3
"""
Skill 加载器 (v1.0)
在执行 pipeline 前调用 validate_task_skill()，
防止 TK 任务被路由到 drama 脚本（已发现的生产 Bug）。
"""
import fnmatch
import yaml
from pathlib import Path
from typing import Optional, Tuple

_REGISTRY_FILE = Path(__file__).parent / "registry.yaml"


def _load_registry() -> dict:
    with open(_REGISTRY_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_skill_for_task(task_id: str) -> Optional[str]:
    """根据任务ID匹配对应的 skill 名称"""
    registry = _load_registry()
    for skill_name, skill_cfg in registry.get("skills", {}).items():
        for pattern in skill_cfg.get("compatible_tasks", []):
            if fnmatch.fnmatch(task_id.upper(), pattern.upper()):
                return skill_name
    return None


def validate_task_skill(task_id: str, skill_name: str) -> Tuple[bool, str]:
    """
    校验 task_id 与 skill_name 是否匹配。
    返回 (True, "OK") 或 (False, 错误原因)
    在每次 pipeline 调度前调用此方法。

    用法示例：
        ok, reason = validate_task_skill("TK-20260423-001", "claw-operator")
        if not ok:
            raise RuntimeError(reason)
    """
    matched = get_skill_for_task(task_id)
    if matched is None:
        return False, f"任务 {task_id!r} 未匹配到任何 skill"
    if matched != skill_name:
        return False, (
            f"任务 {task_id!r} 应使用 skill {matched!r}，"
            f"但调度到了 {skill_name!r}（跨业务线路由错误）"
        )
    return True, "OK"


def get_stage_script(skill_name: str, stage_id: str) -> Optional[str]:
    """获取指定 skill + 阶段的脚本文件名"""
    registry = _load_registry()
    skill    = registry.get("skills", {}).get(skill_name, {})
    skill_path = skill.get("path", "")
    for stage in skill.get("stages", []):
        if stage.get("id") == stage_id:
            return f"{skill_path}/{stage['script']}"
    return None


if __name__ == "__main__":
    # 快速测试
    tests = [
        ("TK-20260423-001", "claw-operator"),
        ("TK-20260423-001", "water-margin-drama"),   # 应报错
        ("DS-20260423-001", "water-margin-drama"),
        ("DRAMA-20260410-002", "water-margin-drama"),
    ]
    for tid, skill in tests:
        ok, msg = validate_task_skill(tid, skill)
        icon = "✅" if ok else "❌"
        print(f"{icon} validate_task_skill({tid!r}, {skill!r}) → {msg}")
