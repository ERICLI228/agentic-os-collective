#!/usr/bin/env python3
"""共享工具函数"""
import shutil
from pathlib import Path


def _find_binary(name: str) -> str:
    """
    动态查找二进制路径，避免 brew 升级后硬编码失效。
    查找顺序: PATH → /opt/homebrew/bin → /usr/local/bin → brew Cellar 最新版本
    """
    candidates = [
        shutil.which(name),
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
    ]
    cellar = Path(f"/opt/homebrew/Cellar/{name.replace('ffprobe', 'ffmpeg')}")
    if cellar.exists():
        for d in sorted(cellar.iterdir(), reverse=True):
            f = d / "bin" / name
            if f.exists():
                candidates.append(str(f))
                break
    for p in candidates:
        if p and Path(p).exists():
            return p
    return name  # fallback: 让系统 PATH 决定


def _find_ffmpeg() -> str:
    return _find_binary("ffmpeg")


def _find_ffprobe() -> str:
    return _find_binary("ffprobe")
