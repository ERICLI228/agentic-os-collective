#!/usr/bin/env python3
"""
Safe Mode 模型路由器 → 已迁移至 shared/core/safe_router.py
此文件为兼容性重导出 shim，请直接 import shared.core.safe_router
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.core.safe_router import *  # noqa: F401, F403
