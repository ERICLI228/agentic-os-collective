#!/usr/bin/env python3
"""
自动同步脚本 — 将代码同步到 GitHub
安全修复: shell=True → shell=False + shlex.split
"""
import os, sys, shlex, subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path.home() / "agentic-os-collective"

ALLOWED_COMMANDS = {
    "git", "python3", "npm", "ruff", "pytest",
}

def run(cmd: str) -> tuple:
    """安全执行命令 (shell=False)"""
    parts = shlex.split(cmd)
    if not parts:
        return -1, "", "empty command"
    exe = Path(parts[0]).name
    if exe not in ALLOWED_COMMANDS:
        return -1, "", f"blocked: {exe}"

    result = subprocess.run(parts, shell=False, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def sync():
    print(f"\n{'='*50}")
    print(f"🔄 自动同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    os.chdir(REPO_DIR)

    code, out, err = run("git status --porcelain")
    if not out.strip():
        print("✅ 没有新改动")
        return

    print(f"📝 发现 {len(out.splitlines())} 个改动")

    for cmd in ["git add -A", f'git commit -m "Auto sync {datetime.now().strftime("%Y-%m-%d %H:%M")}"', "git push"]:
        code, out, err = run(cmd)
        if code != 0:
            print(f"❌ {cmd.split()[0]} 失败: {err}")
            return
        print(f"✅ {cmd.split()[0]} 完成")

    print("✅ 已同步到 GitHub")

if __name__ == "__main__":
    sync()
