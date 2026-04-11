#!/usr/bin/env python3
"""
自动同步脚本 - 将代码同步到 GitHub
"""
import os
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path.home() / "agentic-os-collective"

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def sync():
    print(f"\n{'='*50}")
    print(f"🔄 自动同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    os.chdir(REPO_DIR)
    
    # 检查是否有改动
    code, out, err = run("git status --porcelain")
    if not out.strip():
        print("✅ 没有新改动")
        return
    
    print(f"📝 发现 {len(out.splitlines())} 个改动")
    
    # 添加所有改动
    code, out, err = run("git add -A")
    if code != 0:
        print(f"❌ git add 失败: {err}")
        return
    
    # 提交
    commit_msg = f"Auto sync {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    code, out, err = run(f'git commit -m "{commit_msg}"')
    if code != 0:
        print(f"❌ git commit 失败: {err}")
        return
    
    print(f"✅ 已提交")
    
    # 推送
    code, out, err = run("git push")
    if code != 0:
        print(f"❌ git push 失败: {err}")
        return
    
    print(f"✅ 已推送到 GitHub")

if __name__ == "__main__":
    sync()