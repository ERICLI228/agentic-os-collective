#!/usr/bin/env python3
"""
命令执行器基类 (v1.0)
修复原 execution_logger.py 的命令注入漏洞：
  - 禁用 shell=True
  - 使用 shlex.split() 解析命令
  - 严格白名单校验可执行文件和脚本路径
"""
import shlex
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# ── 白名单：允许的可执行文件 ────────────────────────────────────────────
ALLOWED_EXECUTABLES = {"python3", "bash"}

# ── 白名单：脚本必须位于以下目录之一 ────────────────────────────────────
ALLOWED_PATH_PREFIXES = [
    str(Path.home() / ".openclaw/skills/"),
    str(Path.home() / ".agents/skills/"),
    str(Path.home() / "agentic-os-collective/"),
]

# ── 黑名单：拒绝包含以下字符的命令 ──────────────────────────────────────
DANGEROUS_CHARS = {"|", ";", "&", "`", "$(", "${", ">", "<", "\n", "\r"}


def validate_command(command: str) -> tuple:
    """
    安全校验命令。
    返回 (True, "OK") 或 (False, 错误原因)
    """
    # 1. 危险字符检查
    for ch in DANGEROUS_CHARS:
        if ch in command:
            return False, f"命令包含危险字符: {ch!r}"

    # 2. 解析命令（不经过 shell）
    try:
        parts = shlex.split(command)
    except ValueError as e:
        return False, f"命令解析失败: {e}"

    if not parts:
        return False, "空命令"

    # 3. 可执行文件白名单
    executable = Path(parts[0]).name   # 取文件名，防止绝对路径绕过
    if executable not in ALLOWED_EXECUTABLES:
        return False, f"不允许的可执行文件: {executable!r}"

    # 4. 脚本路径白名单
    if len(parts) > 1:
        script_path = parts[1]
        if not any(script_path.startswith(p) for p in ALLOWED_PATH_PREFIXES):
            return False, f"脚本路径不在白名单: {script_path!r}"

    return True, "OK"


def run_command(
    command: str,
    timeout: int = 3600,
    cwd: Optional[Path] = None,
) -> dict:
    """
    安全执行命令并返回结果。
    使用 shlex.split + shell=False，彻底避免 shell 注入。
    """
    is_valid, reason = validate_command(command)
    if not is_valid:
        logger.error(f"命令校验失败: {reason}")
        return {"status": "error", "error": reason, "duration": 0.0}

    start = datetime.now()
    try:
        result = subprocess.run(
            shlex.split(command),      # ✅ 列表形式，不经过 shell
            shell=False,               # ✅ 关键：禁用 shell=True
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
        duration = (datetime.now() - start).total_seconds()
        return {
            "status":      "completed" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "duration":    round(duration, 2),
            "stdout":      result.stdout[:5000],
            "stderr":      result.stderr[:2000],
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "duration": (datetime.now() - start).total_seconds()}
    except Exception as e:
        return {"status": "error", "error": str(e), "duration": (datetime.now() - start).total_seconds()}
