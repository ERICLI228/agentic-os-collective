# Agentic OS v3.5 — Agent Quick Reference

> 最后更新: 2026-04-29 | 完成度 ~55% | `~/agentic-os-collective/`

## 路径速查

```bash
ROOT=~/agentic-os-collective
DRAMA=$ROOT/drama/openclaw/skills/water-margin-drama
TK=$ROOT/tk/openclaw
SHARED=$ROOT/shared/core              # ← 14个模块唯一源，drama/tk core 已是 shim
STORIES=$ROOT/stories                 # 3个YAML: shuihuzhuan/sanguo/xiyou
FEISHU_V3=~/.openclaw/workspace/scripts/send-feishu-v3.py
```

## 端口

| 端口 | 服务 | 文件 |
|:--:|------|------|
| 5001 | Flask 任务管理 API | `shared/task_wizard.py` (v3.5 新增 /api/status + /api/decision) |
| 5004 | FastAPI v3 主API | `api/v3/dashboard_api_v3.py` |
| 8081 | NGINX 网关 | `gateway/nginx.conf` |

## 常用命令

```bash
# 故事切换 (三个故事不改代码)
python3 $DRAMA/water_margin_drama.py --story sanguo --theme "桃园结义" --mode script
python3 $DRAMA/script_selector.py --story xiyou select

# 任务
python3 $DRAMA/quality_assessor.py --json-only          # AI评分
python3 $TK/core/daily_business_summary.py --dry-run    # 日报预览
python3 $TK/core/daily_business_summary.py --all-channels

# 开发
python3 -m py_compile <file>          # 写后验证
ruff check --select E,F,W,B,S --ignore S101 $ROOT/drama $ROOT/tk $ROOT/shared
pytest $ROOT/tests/ -v

# 运维
pm2 start $ROOT/ecosystem.config.js
pm2 logs agentic-api-v3
```

## 代码架构

```
shared/core/  ← 14模块唯一源 (drama/core + tk/core 已去重为shim)
├── base_executor.py       # run_command(shell=False, shlex.split) — 所有命令走这里
├── task_helper.py         # create_task(project_id)
├── task_updater.py        # update_milestone(task_id, milestone_id, status)
├── safe_router.py         # 模型路由
├── adversarial_review.py  # v3.5 通用对抗审核框架 (从 AI_Short_Drama_Pipeline 搬迁)
├── *_server.py            # HTTP服务 (端口已去冲突)
└── __init__.py            # 导出 validate_command, run_command, BasePipeline

shared/ (根级, v3.5 新增)
├── feishu_status_push.py  # 飞书状态推送 (Sprint 0.2)
├── publish_gate.py        # 发布审批硬约束 (Sprint 0.4, 双条件检查)
└── config.py              # 统一配置 (.env + 8 Webhook ID + ARK_API_KEY)

water-margin-drama/
├── water_margin_drama.py   # 主入口 --story --theme --mode
├── script_selector.py      # 从story.episodes评分排序 (去硬编码CHAPTERS)
├── role_designer.py        # 从story.roles()加载角色 (去硬编码ROLES/SCENES)
├── controversy_rewriter.py # 从story.controversies加载规则 (去硬编码CONTROVERSY_RULES)
├── quality_assessor.py     # FR-DR-005 AI评分 (GLM 4维 + 规则引擎降级)
├── audio_generator.py      # FR-DR-007 多角色TTS
├── auto_publisher.py       # --dev模式可用
└── confirmation.py         # 3阶段确认门禁

TK pipeline (MS-1~MS-5):
├── tk/.../proactive-operator/  # MS-1 Shell脚本 (+data/+logs)
├── tk/.../claw-operator/       # MS-2/3/4 Python脚本
└── tk/core/daily_business_summary.py  # MS-5 日报

shared/extras:
├── story_loader.py        # 多故事加载: load_story("sanguo")
├── execution_logger.py    # 已委托base_executor.run_command()
└── mcp_task_server.py     # MCP桥接

妙手数据:
└── ~/.agentic-os/miaoshou_products.json  # 100商品 (2026-04-28)
```

## v3.5 新增决策接口

### GET /api/status (5001)
返回任务列表 + 决策状态 + 系统健康检查
```bash
curl http://localhost:5001/api/status
```

### POST /api/decision (5001)
人工审批任务，支持 approved/rejected/modify
```bash
curl -X POST http://localhost:5001/api/decision \
  -H 'Content-Type: application/json' \
  -d '{"task_id":"TK-xxx","action":"approved","reason":"通过"}'
```

### 发布审批 (publish_gate.py)
```bash
MIAOSHOW_PUBLISH_ENABLED=true python3 shared/publish_gate.py <task_id>
# 双条件: env=true AND human_approved=true
```

## 已闭合的安全边界

- **命令执行**: `base_executor.run_command()` — shell=False + shlex.split + 双白名单
- **API密钥**: `config.py` 统一管理, .env 覆盖, 代码0硬编码
- **跨业务路由**: `skill_loader.py` + `registry.yaml` + fnmatch

## TTS 策略 (NLS-only, 2026-04-27)

所有 TTS 只能走阿里云 NLS 资源包 `NLSTTSBAG-xxx` (余额 29817/30000)。
严禁使用 ElevenLabs、macOS `say`、DashScope CosyVoice、OpenAI TTS 等可能产生额外扣费的方案。

| 项目 | 文件 | 凭证 |
|------|------|------|
| Clicky (macOS App) | `AliyunNLSClient.swift` + `ElevenLabsTTSClient.swift` | `~/.clicky/config.json` |
| water-margin-drama | `aliyun_nls.py` + `audio_generator.py` + `drama_audio.py` | 环境变量 `ALIYUN_*` |
| openclaw-video | `.env` | `ALIYUN_ACCESS_KEY_ID/ SECRET/ APP_KEY` |
| TK video-generation | `tts.py` + `local-tts.py` | 环境变量 |

凭证: RAM用户 `tts-service-user` (LTAI5t92pPDVgFvSWEWKuWZS), AppKey EO3zZigsTGKIUL1y
可用男声: zhiming/zhiyuan/zhihao/zhilin | 女声: xiaoyun/zhiqi | (zhifeng 不通 NLS 网关)

## 飞书 Webhook (8频道, 无需环境变量)

```python
from shared.config import config
url = config.get_feishu_webhook("数据看板")
# 频道: 选品作战室/数据看板/达人运营/订单中心/广告指挥室/内容工坊/客服中心/运营指挥部/技术研发
```

## 硬编码已消除

| 原位置 | 原问题 | 现状态 |
|--------|--------|:--:|
| 4个py + make-drama.sh | ARK_API_KEY 硬编码 | config.py 默认值 (.env覆盖) |
| dashboard_api_v2.py | FEISHU_WEBHOOK_URL | config.py Webhook ID字典 |
| 4个drama模块 | 水浒传专有数据 | stories/*.yaml 配置驱动 |
| execution_logger/auto_sync | shell=True | base_executor.run_command() |
