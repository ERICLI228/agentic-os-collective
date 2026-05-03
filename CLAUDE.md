# Agentic OS v3.7 — Agent Quick Reference

> 最后更新: 2026-05-01 | 完成度 基础设施97% / 核心功能85% | `~/agentic-os-collective/`

---

## ⛔ 铁则 #0.5: 安全作业铁则（环境隔离 + 精准代码编辑）

> **任何任务开始前，必须读取并遵守 `~/agentic-os-collective/SAFETY_RULES.md`**
> 此规则优先级高于一切任务描述，不可被绕过。

- 测试环境优先：所有修改必须在 `/tmp/agentic-os-test` 中进行，禁止写入生产 `~/agentic-os-collective/`
- 代码编辑三层防护：`// @@FUNC:` 锚点 + `grep -cF` 唯一性校验 + `node --check` 语法校验
- 同步仅限人工：`scripts/sync-test-to-prod.sh` 仅人工可执行，AI 禁止调用
- 违反此规则 = 立即中止任务

---

## ⛔ 铁则 #0: 任务完成强制闭环 (TASK COMPLETION LOCK)

> **任何任务完成后，必须按以下顺序执行全部 4 步，遗漏任一步 = 任务未完成。不得跳过。**

```
任务完成 → [1] 标注 PRD → [2] git commit+push → [3] Obsidian 同步 → [4] wiki/index/log 更新
                                                                              ↓
                                                                    任务才算真正完成
```

| 步骤 | 命令/操作 | 验证 |
|------|----------|------|
| **1. 标注 PRD** | 编辑 `reports/PRD-v3.6.md`，新增版本条目（版本号/日期/修订人/内容摘要），更新标题版本号 | `grep v3.6.XX reports/PRD-v3.6.md` 能找到本次版本 |
| **2. Git 推送** | `git add -A && git commit -m "v3.6.XX: <摘要>" && git push origin main`<br>`rsync -a --exclude='.git' ~/agentic-os-collective/ ~/Backups/agentic-os-$(date +%Y%m%d_%H%M)/` (本地快照) | `git log -1` 显示本次 commit |
| **3. Obsidian** | `python3 ~/.openclaw/workspace/knowledge-base/sync_tasks_to_obsidian.py` | 输出 `✅ 同步完成` |
| **4. Wiki** | 追加 `wiki/log.md` + 更新 `wiki/index.md`（total_pages/最近新增） | `tail -5 wiki/log.md` 显示本次条目 |

### 协同规则 (OpenClaw ↔ OpenCode)
- 双方**主动相互协助与验证测试**，任何一方完成修改后，另一方运行验证
- 如果一方遇到问题（死循环/路径错误/依赖缺失），另一方**主动协助协同解决**，不等用户介入
- 关键数据（EPISODE_MAP/角色名/PRD行数/VERSION）双方交叉验证后才 commit
- **双方都必须执行铁则 #0**，任一方漏步 = 两方都要负责

### 自动检测：PRD 版本滞后告警

仪表盘 `/dashboard` 顶部已集成 PRD 版本检查：如果当前代码版本号 > PRD 记录的最新版本号，显示 ⚠️ 红色告警条。
`VERSION` 文件（根目录）与 `reports/PRD-v3.6.md` 版本号必须同步更新。

---

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

NLS凭证: 从 `.env` 读取 `ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET / ALIYUN_APP_KEY` — 禁止硬编码
可用男声: zhiming/zhiyuan/zhihao/zhilin | 女声: xiaoyun/zhiqi | (zhifeng 不通 NLS 网关)
资源包余量: ~29817/30000 字符 (2026-04-29)，单集预算 <500 字符

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

## 任务完成规则 → 见顶部 ⛔ 铁则 #0

---

## 铁则: 假成功判定 (Fake Success Rule, 2026-04-30)

> **`"无效命令"` + `STATUS: completed` = ⚠️ MOCK/FAILED，必须重标记为失败。**

### 背景
- `shared/logs/executions/` 中 11/21 条 `STATUS: completed` 日志 stdout 含 `无效命令`
- 根因：旧执行器以 exit code=0 判定完成，忽略 stdout 内容
- 受影响脚本：`script_selector.py`, `role_designer.py` 等（无效参数导致打印 `无效命令` 但仍 exit 0）

### 规则
1. 任何脚本 stdout 包含 `无效命令` → 本次执行标记为 **⚠️ MOCK**，不得标 ✅
2. 所有 WBS/PRD 中依赖这些日志的 `STATUS: completed` 里程碑 → 重置为 ⚠️ 待重跑
3. 新脚本必须有非零退出码验证：`sys.exit(1)` on error, 不吞异常
4. WBS/PRD 完成度统计必须排除 ⚠️ MOCK 条目

### WBS 日志审计状态
- ❌ 已过时：`drama_merge.py 不存在` / `ffmpeg 未安装` / `Dashboard 不存在` / `task_wizard 0.0.0.0`（已修）
- ⚠️ 待修复：假成功清洗 (11条) / GLM_API_KEY 空值 / skill 入口验证模板

---

## LLM 对抗审核 (2026-04-30 突破)

| 模式 | 命令 | 耗时 | 费用 | 用途 |
|------|------|------|------|------|
| `--mock` | `drama_script --mock` | <1s | ¥0 | pipeline MS-4.5 管线默认 |
| `--mode multi-agent` | `python3 shared/core/adversarial_review.py drama_script <json>` | ~100s | ¥0 (CODING) | 最终质量闸门，人工审核前 |

### 管线集成
- **文件**: `shared/core/adversarial_review.py` — 模型路由 `aliyun/` → `coding/` (CODING 免费额度)
- **.env 加载**: 已补充 `dotenv.load_dotenv()` 自动加载
- **drama_pipeline.yaml**: 命令修正为 `drama_script --mock` (防止 100s 超时)
- **CODING Plan**: 剩余 48 天 / 48% 额度

### 审核结果示例 (EP03 shot_01)
```
综合评分: ~3.8/10 | 裁决: reject (驳回)
```
| 维度 | 发现 |
|------|------|
| 编剧规则合规 | 旁白与动作指令混淆、缺少标准场次编号 |
| 工业级分镜 | 缺景别/机位/运镜/时长参数 |
| 逻辑一致性 | "肩扛花枪+没膝积雪中踉跄"重心力学冲突 |
| 节奏控制 | 单镜头无内部调度、无戏剧钩子 |

### Dashboard 命令提示修正
- `detail_engine.py:480`: 从 `--mode multi-agent` → `drama_script --mock`
- `tk_pipeline.yaml`: 场景命令统一加 `--mock` 后缀

---

## 当前阻塞项 (2026-04-30)

| 项 | 状态 |
|---|------|
| fal.ai 视频生成 | 待用户充值 |
| 妙手发布 API | `MIAOSHOW_PUBLISH_ENABLED=false` |
| TK 达人联盟 | 紫鸟手动操作 |
| GLM API | `GLM_API_KEY=` 空值，当前管线走 NLS，GLM 暂不可用 |
