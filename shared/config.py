#!/usr/bin/env python3
"""
统一配置管理模块 (v1.0)
─────────────────────────────────────────────────────────────────
所有模块通过此文件获取配置，禁止在业务代码中直接读取 os.environ。
优先级：系统环境变量 > .env 文件 > 代码默认值
─────────────────────────────────────────────────────────────────
"""
import os
from pathlib import Path

# ── 自动查找 .env（从本文件向上两级）──────────────────────────────────
_root = Path(__file__).parent.parent           # → agentic-os-collective/
_env_file = _root / ".env"

try:
    from dotenv import load_dotenv
    load_dotenv(_env_file, override=False)      # 系统变量优先，不覆盖
    _dotenv_loaded = _env_file.exists()
except ImportError:
    _dotenv_loaded = False
    print("⚠️  python-dotenv 未安装，仅使用系统环境变量和默认值")
    print("   运行: pip install python-dotenv")


class Config:
    """
    项目全局配置。
    读取顺序：环境变量 → .env 文件 → 下方默认值
    """

    # ── 路径 ──────────────────────────────────────────────────────────
    WORKSPACE_DIR: Path = Path(
        os.getenv("WORKSPACE_DIR", str(Path.home() / "agentic-os-collective"))
    )
    DB_PATH: Path = Path(
        os.getenv("DB_PATH", str(WORKSPACE_DIR / "shared/data/agentic.db"))
    )

    # ── 内部服务 ───────────────────────────────────────────────────────
    API_BASE:  str = os.getenv("API_BASE",  "http://localhost:5001")
    API_HOST:  str = os.getenv("API_HOST",  "127.0.0.1")   # ⚠️ 默认禁止公网
    API_PORT:  int = int(os.getenv("API_PORT", "5001"))

    # ── 外部 API 密钥（严禁硬编码真实值）──────────────────────────────
    FEISHU_WEBHOOK_URL:  str = os.getenv("FEISHU_WEBHOOK_URL",  "")
    MINIMAX_API_KEY:     str = os.getenv("MINIMAX_API_KEY",     "")
    SEEDANCE_API_KEY:    str = os.getenv("SEEDANCE_API_KEY",    "")
    REPLICATE_API_TOKEN: str = os.getenv("REPLICATE_API_TOKEN", "")
    OPENAI_API_KEY:      str = os.getenv("OPENAI_API_KEY",      "")
    GLM_API_KEY:         str = os.getenv("GLM_API_KEY",         "")
    ARK_API_KEY:         str = os.getenv("ARK_API_KEY",
                            "f25a15bc-b109-40d4-976b-e2bb71cf9bf3")  # 火山引擎 ARK 网关

    # ── 飞书 Webhook ID（8 个群，从 send-feishu-v3.py 配置）──────────
    FEISHU_WEBHOOK_BASE: str = "https://open.feishu.cn/open-apis/bot/v2/hook"
    FEISHU_WEBHOOK_IDS: dict = {
        "选品作战室": "74a5a7e3-d88f-44a0-a012-07b56dc5cd4c",
        "数据看板":   "8f3fde4b-ce19-41c7-b37d-e09a992d1473",
        "达人运营":   "32c6f1d0-af10-4340-876b-9cd54a589289",
        "订单中心":   "cc17bf78-7112-4c38-84ea-f5be40afb9a5",
        "广告指挥室": "fd52600b-b626-4cf3-898c-dac2ecd77d58",
        "内容工坊":   "c851d4b8-5a63-47c7-bb71-5c474f6c99ad",
        "客服中心":   "fcf21b55-8b43-4719-a2b2-51854fdf9aef",
        "技术研发":   "148cb666-4573-4ef6-a03e-a9008b0c972b",
    }

    @classmethod
    def get_feishu_webhook(cls, channel: str) -> str:
        """获取指定频道的完整 Webhook URL"""
        wid = cls.FEISHU_WEBHOOK_IDS.get(channel, "")
        return f"{cls.FEISHU_WEBHOOK_BASE}/{wid}" if wid else ""

    # ── 运营参数 ───────────────────────────────────────────────────────
    TK_TRENDING_THRESHOLD: int = int(os.getenv("TK_TRENDING_THRESHOLD", "3000000"))
    TK_UPDATE_INTERVAL:    int = int(os.getenv("TK_UPDATE_INTERVAL",    "7200"))

    # ── 日志参数 ───────────────────────────────────────────────────────
    LOG_MAX_SIZE:      int = int(os.getenv("LOG_MAX_SIZE_MB",    "10"))  * 1024 * 1024
    LOG_ROTATION_DAYS: int = int(os.getenv("LOG_ROTATION_DAYS", "30"))

    @classmethod
    def validate_required(cls, keys: list) -> None:
        """
        启动时校验必填项，缺失则抛出异常而非静默失败。
        用法：Config.validate_required(["FEISHU_WEBHOOK_URL", "MINIMAX_API_KEY"])
        """
        missing = [k for k in keys if not getattr(cls, k, None)]
        if missing:
            raise EnvironmentError(
                f"❌ 缺少必要配置，请检查 .env 文件:\n"
                + "\n".join(f"   - {k}" for k in missing)
            )

    @classmethod
    def debug_print(cls) -> None:
        """打印当前配置（隐藏密钥），用于排查问题"""
        def mask(v):
            if not v:
                return "（未设置）"
            return v[:4] + "****" + v[-2:] if len(v) > 8 else "****"

        print(f"""
╔══════════════════════════════════════════════╗
║          当前配置（密钥已脱敏）               ║
╠══════════════════════════════════════════════╣
║ WORKSPACE_DIR  : {cls.WORKSPACE_DIR}
║ DB_PATH        : {cls.DB_PATH}
║ API_BASE       : {cls.API_BASE}
║ API_HOST:PORT  : {cls.API_HOST}:{cls.API_PORT}
║ .env 已加载    : {_dotenv_loaded}
╠── 外部服务 ───────────────────────────────────
║ FEISHU_WEBHOOK : {mask(cls.FEISHU_WEBHOOK_URL)}
║ MINIMAX_KEY    : {mask(cls.MINIMAX_API_KEY)}
║ SEEDANCE_KEY   : {mask(cls.SEEDANCE_API_KEY)}
║ REPLICATE_TOKEN: {mask(cls.REPLICATE_API_TOKEN)}
║ GLM_API_KEY    : {mask(cls.GLM_API_KEY)}
╠── 运营参数 ───────────────────────────────────
║ TK爆款阈值    : {cls.TK_TRENDING_THRESHOLD:,} 播放
║ TK更新间隔    : {cls.TK_UPDATE_INTERVAL}s
╚══════════════════════════════════════════════╝
""")


# 模块级单例
config = Config()


if __name__ == "__main__":
    config.debug_print()
