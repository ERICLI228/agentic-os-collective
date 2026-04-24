#!/usr/bin/env python3
"""
Token Governor v1 → 已迁移至 shared/core/token_governor_v1.py
此文件为兼容性重导出 shim，请直接 import shared.core.token_governor_v1
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.core.token_governor_v1 import *  # noqa: F401, F403
