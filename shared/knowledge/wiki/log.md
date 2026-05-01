# 知识库操作日志

## [2026-04-27] init | 知识库初始化
- 创建 wiki 目录结构
- 创建 CLAUDE.md (AI Schema)
- 创建 index.md / log.md

## [2026-04-27] ingest | LLM Wiki 方法论文章
- Added: `raw/articles/llm-wiki-karpathy-methodology.md`
- Created: `wiki/concepts/llm-wiki-methodology.md`
- Updated: `wiki/index.md`

## [2026-04-27] implement | Clicky/CPR 设计理念集成
- Created: `shared/scripts/session-archiver.py` — 会话归档核心脚本
- Created: `scripts/archive-session.sh` — 一键归档命令
- Created: `wiki/concepts/session-archiving.md` — 归档机制概念页
- Updated: 根 `CLAUDE.md` — 加入归档规则和 `[[wikilinks]]` 规范
- 实现三个模式：决策提取 | 结构化日志 | 自动归档

## [2026-04-27] study | Clicky 4.8K ⭐ 源码分析
- **位置**: `~/.agents/skills/clicky-1.0.0/`
- **核心提取**: 结构化 Prompt 标签 `[ACTION:type:params]`、Cancel-and-Replace 并发模式、双日志体系
- **集成**: 已转化为 session-archiver.py 和 CLAUDE.md 规则

## [2026-04-27 02:21] session | 207935b5-57ca-4338-b482-3e6d4c6bf229.trajectory.jsonl
- **消息数**: 4
- **主题**:

- **关键决策**:

- **归档**: wiki/outputs/session-20260427-022125.md

## [2026-04-27 02:22] session | 207935b5-57ca-4338-b482-3e6d4c6bf229.jsonl
- 消息数: 4
- 主题:
  - [cron:73a1ac38-3e08-4416-840f-ade5d162e473 训练+视频 守护监控] 检查训练和视频合成进程是否存活。执行：
1. `ps aux | grep train_s2_v4_fixed | grep -v grep | head -3` — 训练进程
2. `ps aux | grep caffeinate | grep -v grep | head -3` —
- 决策:

- 归档: wiki/outputs/session-20260427-022221.md

## [2026-04-27 03:29] session | 8516823d-c468-492b-afee-66674dd7835d.jsonl
- 消息数: 323
- 主题:
  - Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-27 02:55 PDT] 这个处理好了
[media attached: media://inbound/image---7f725482-87fa-4
  - Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-27 02:30 PDT] 归档
  - Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-27 03:20 PDT] 集成 GitNexus至OPENCLAW作为持续持久的自动化基础设施能力 并索引短剧 Pipeline 项目
  - [Mon 2026-04-27 02:51 PDT] 执行【终端环境修复
⏳ VPN 替代方案获取
⏳ agent-skills/browser-harness Skill 格式转换】
  - Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-27 03:18 PDT] 这些对我们有什么用【Proactive Agent项目地址：GitHub https://github.com/thunlp/
  - [Mon 2026-04-27 03:20 PDT] 集成 GitNexus至OPENCLAW作为持续持久的自动化基础设施能力 并索引短剧 Pipeline 项目
  - [Mon 2026-04-27 03:18 PDT] 这些对我们有什么用【Proactive Agent项目地址：GitHub https://github.com/thunlp/ProactiveAgent，技术论文 https://arxiv.org/abs/2410.12361。清华与面壁智能联合开发的AI主动协助工具。GitNexus通过构建代码知识图谱解决AI编程助手不理解函数依赖的问题
  - [Queued user message that arrived while the previous turn was still active]
Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Mon 2026-04-2
- 决策:
  - 1. 运行 `save-session.sh` 创建快照
  - 3. 创建 `projects.md` 记录项目进展
  - 1. 运行 `save-session.sh` 创建快照
  - 3. 创建 `projects.md` 记录项目进展
  - 1. 运行 `save-session.sh` 创建快照
  - 3. 创建 `projects.md` 记录项目进展
  - 1. 运行 `save-session.sh` 创建快照
  - 3. 创建 `projects.md` 记录项目进展
  - - ⚠️ **无 embeddings**：索引时使用了 `--drop-embeddings`，语义搜索能力受限
  - - ⚠️ **无 embeddings**：索引时使用了 `--drop-embeddings`，语义搜索能力受限
- 归档: wiki/outputs/session-20260427-032920.md
## [2026-04-27] lint | 健康检查
- **Report**: `wiki/outputs/lint-report-2026-04-27.md`
- **Pages**: 4
- **Orphans**: 3
- **Broken links**: 4

## [2026-04-27] ingest | Test Raw Note
- **Action**: ingest
- **Type**: concept

- **Saved**: `wiki/outputs/test-entry.md`
- **Pages consulted**: test, wikilink
- **Summary**: AI query result saved to wiki outputs

## [2026-04-27] lint | 健康检查
- **Report**: `wiki/outputs/lint-report-2026-04-27.md`
- **Pages**: 5
- **Orphans**: 1
- **Broken links**: 7


## 2026-04-27 — NLS TTS 全面集成

- **背景**: 用户购买的阿里云 NLS 资源包 NLSTTSBAG-xxx (30000次, 剩余29817次)
- **决策**: 禁用旧密钥 LTAI5t7yk35KYVBjCLTY1b9i → 新建专用 RAM 用户 `tts-service-user` (LTAI5t92pPDVgFvSWEWKuWZS)
- **变更**:
  - Clicky: `ElevenLabsTTSClient` + `AliyunNLSClient` → NLS-only, 移除 `say` 回退
  - openclaw-video `.env`: 修复为正确 LTAI 格式凭证
  - water-margin-drama: `audio_generator.py` + `drama_audio.py` → 移除 ElevenLabs + macos say, 统一 NLS
  - `.openclaw/workspace/scripts/local-tts.py`: DashScope CosyVoice → NLS
  - `.openclaw/workspace/skills/video-generation/tts.py`: 重写为 NLS-only
- **新文件**: `drama/openclaw/skills/water-margin-drama/aliyun_nls.py` (共享 NLS 模块)
- **凭证存储**: `~/.clicky/config.json` (Clicky), 环境变量 (Python 项目)
- **可用男声**: `zhiming` (知明), `zhiyuan` (知远), `zhihao` (志浩), `zhilin` (志林)
- **可用女声**: `xiaoyun` (晓芸), `zhiqi` (知琪)
- **注意**: `zhifeng` (知锋) 是 CosyVoice 模型, 不兼容 NLS 网关, 不能走资源包

## 2026-04-28 Miaoshou ERP Product API Investigation

### What was done
- Full reverse-engineering of Miaoshou ERP API (login, shops, collection box, products)
- Auto captcha OCR via Apple Vision framework (Swift, `VNRecognizeTextRequest`) → 95% accuracy
- All major APIs tested; collection box works (50 items), product listing API returns empty
- Root cause: shops have 0 products (never operated), need to find publish-to-shop API

### Key findings
| API | Status | Notes |
|-----|--------|-------|
| `POST /api/auth/account/login` | ✅ | AES-CBC encrypt mobile+password, captcha required |
| `GET /api/auth/shop/getAllShopV2` | ✅ | Returns 6 TikTok shops (SG/VN/TH/PH/MY/Global) |
| `POST /api/move/common_collect_box/searchDetailList` | ✅ | 50 items, needs `X-Breadcrumb: item-common-commonCollectBox` |
| `POST /api/item/item/searchItemList` | ❌ | Empty (0 products in shops) |
| `POST /api/order/package/searchOrderPackageList` | ✅ | 0 orders (normal for new shops) |
| Claim/Publish to shop API | 🔴 | **NOT FOUND** - 19 guessed endpoints all returned empty |

### Blocking issue
- TikTok shops registered but never operated → 0 products in Miaoshou listings
- 50 items in collection box (1688-sourced, `copyType: alibabaAir`, `platformItemId: None`)
- Missing: API endpoint to publish collection box items to specific TikTok shop
- Need browser automation or deeper JS analysis to find the publish API

### Next steps (when user unblocks)
1. Use `agent-browser` (installed at `/Users/hokeli/.npm-global/bin/agent-browser`) to open Miaoshou web UI
2. Navigate to collection box, click "发布到店铺/publish to shop"
3. Capture the exact API call via network tracing
4. Implement the publish flow

### Files created/modified
- `/tmp/ocr_captcha3.swift` — Swift OCR script (Apple Vision)
- `~/Desktop/miaoshou_product_sync.py` — auto sync script

### Credentials (for automation)
- Username: `19864839993` / Password: `A@magic9`
- AES Key: `@3438jj;siduf832`
- OCR: Swift `VNRecognizeTextRequest`, `recognitionLevel: .accurate`, `usesLanguageCorrection: false`
- Login token lifetime: ~24h

## [2026-04-28 06:42] session | d67d41f5-cdfb-43d3-abb8-f930b2676490.jsonl
- 消息数: 11
- 主题:
  - [cron:ba76a5d2-72ba-4d4d-958e-5813a2907d4d 视频合成完成检查] 检查 20 个 wandering_v3 视频是否全部完成：
1. ls /Users/hokeli/ComfyUI/output/wandering_v3_*.mp4 | wc -l
2. 如果 < 20 个，检查 ComfyUI 队列状态和进度，汇报当前完成数/剩余数/预计时间，回复 NO
- 决策:

- 归档: wiki/outputs/session-20260428-064211.md

## [2026-04-29 19:00] session | 9c50506a-5b28-45ac-b1ef-ed7266502c19.jsonl
- 消息数: 15
- 主题:
  - [cron:0fbcb3bd-797c-4fdc-a212-f84c92281d9b GPT-SoVITS TTS 推理就绪检查] 检查 GPT-SoVITS TTS 推理服务是否就绪。执行：
 1. `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9880/` 检查服务是否在线（400=正常，说明服务在运行）
 2. `ps aux 
- 决策:
  - **结论：✅ TTS 推理已就绪，可正常使用！**
- 归档: wiki/outputs/session-20260429-190052.md

## [2026-04-30] session | v3.6.1 全系统QA + PRD注释 + GitHub同步 + Obsidian登记

- **会话类型**: OpenCode (quick-cabin worktree)
- **主题**:
  - v3.6→v3.6.1 10项关键修复 (sys import / ep_num prefix / export tuple / Image404 / 拼音双通 / DM-V/F / push_erp / SRT导出 / 订单履约 / 6集管线)
  - 80/80 QA全绿验证 (30端点 + 全部边界 + 全部文件)
  - PRD-v3.6.md 注释更新: 完成度矩阵 (86%/72%) + GAP表 + 端点全景 + 测试报告
  - GitHub: df10af7→240a068 推送到 main (+591/-294, 7 files)
- **关键决策**:
  - Dashboard smart routing 就绪 (DM-0/DM-1/MS-2.3 专用渲染器)
  - 6集全管线 ComfyUI+NLS 全部通过 (EP01-06 final.mp4)
  - 决策: 保持30端点 Flasket稳定, 不再新增端点
  - GAP: AI视频支付/达人联盟/5国字幕/环境音效 待用户决策
- **知识库产出**:
  - 创建: `wiki/entities/agentic-os-v3.6-architecture.md`
  - 更新: `wiki/index.md` (total_pages: 10→14, 新增实体+综合分析)
  - 更新: `wiki/log.md` (本条目)
  - 更新: `reports/PRD-v3.6.md` (v3.6.1 注释版)

- **会话**: 2026-05-01, 05:45 PDT — PRD 全面修订 v3.6.9→v3.6.20 + Git push + Obsidian 同步
- **完成工作**:
  - PRD-v3.6.md 修订历史新增 12 个里程碑 (v3.6.9~v3.6.20)
  - CLAUDE.md 版本号同步 v3.6.2→v3.6.20
  - Git push to origin/main (commit 59c7ba4)
  - Obsidian sync 9/9 tasks
- **关键文件变更**:
  - `reports/PRD-v3.6.md` (564→613+ lines, +12 version entries)
  - `CLAUDE.md` (v3.6.2→v3.6.20, 完成度更新)
- **版本覆盖**: v3.6.9 Gallery · v3.6.10 Dashboard UI · v3.6.11 NLS音色 · v3.6.12 CHARACTER_VOICES 108 · v3.6.13 角色数据补全 · v3.6.14 GPT-SoVITS · v3.6.15 音色UI · v3.6.16 gallery修复 · v3.6.17 目录清理 · v3.6.18 video_prompts三方案 · v3.6.19 CSS修复 · v3.6.20 图像路由修复
