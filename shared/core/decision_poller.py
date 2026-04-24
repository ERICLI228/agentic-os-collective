#!/usr/bin/env python3
"""
决策轮询服务 - 后台运行，持续监听决策事件
"""
from pathlib import Path
import time
import sys
import os

# 添加 core 目录到路径
sys.path.insert(0, str(Path.home() / ".openclaw/core"))
os.chdir(str(Path.home() / ".openclaw/core"))

from decision_listener import check_and_trigger

POLL_INTERVAL = 30  # 秒

def run_poller():
    """后台轮询服务"""
    print(f"🚀 决策轮询服务已启动，每 {POLL_INTERVAL} 秒检查一次")
    while True:
        try:
            check_and_trigger()
        except Exception as e:
            print(f"⚠️ 轮询错误：{e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    run_poller()