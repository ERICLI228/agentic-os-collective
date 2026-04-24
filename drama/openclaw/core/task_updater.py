#!/usr/bin/env python3
"""已迁移至 shared/core/ —— 此文件为兼容性重导出 shim"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.core.task_updater import *  # noqa: F401, F403

