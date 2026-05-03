# 🎬 Agentic OS v3.7.20 产品需求文档 (PRD)

> **文档类型**: 产品需求文档 (Product Requirements Document)
> **版本**: v3.7.20 (2026-05-03 05:30)
> **日期**: 2026 年 5 月 3 日
> **产品名称**: Agentic OS v3.7 用户体验升级版
> **产品愿景**: 一个指令启动 → 全程自动执行 → **关键节点等你决策** → 输出可发布成果
> **目标用户**: TK 跨境电商运营人员、AI短剧创作者、技术开发团队
> **文档状态**: ✅ v3.7.20 — DM-6/7 质量可视化 + 管线日志结构化 + DM-1 角色图删图/重绘 + 🎤→DM-3 管线串联 + 10项审计发现
> **前置版本**: v3.7.8 (2026-05-02)

---

## ✅ 当前可用（2026-05-03 05:30 实锤）

| 能力 | 状态 | 验证 |
|------|------|------|
| Flask Dashboard :5001 | ✅ 运行中 | task_board.html **10,634行** · 16功能模块+2工具面板 · JS语法零缺陷 · 新增3个后端API |
| API 端点 | ✅ 45+ | Flask :5001 (37+) + FastAPI :5004 (8+) · 新增DELETE/POST渲染管理API · 新增TTS代理端点 |
| TK 运营（13里程碑）| ✅ 全端点200 | 选品对比/图片处理/5国合规/采集门禁 |
| ├ MS-0 采集门禁 | 🆕 体检报告 | 运营健康仪表盘 + 门禁指标 + 路由检测 |
| ├ MS-2.3 商品图处理 | 🆕 处理工作台 | 4张真实商品图卡片 + 去背景/一键处理 + 批量串行 |
| ├ MS-5 日报推送 | 🆕 3按钮全通 | 手动推送(8群/7ok) + 预览弹窗 + 推送历史 |
| AI 短剧 | ✅ 10集管线 | EP01-EP10 final.mp4 · ComfyUI SDXL · NLS配音 · DM-6/7质量可视化完成 |
| ├ DM-1 角色系统 | ✅ 109角色 | visual_bible.json · 436张定妆照 · ✕删图+🔁重绘功能 · 🎤→DM-3配音串联 |
| ├ DM-3 配音设计 | ✅ SFX集成 | 6角色音色表 + 音效时间线可视化 + 🎤→DM-3跳转串联 |
| ├ DM-6/7 成品 | ✅ 质量评分 | 条形图(配音/画面/合成) + 文件规格卡 + 管线日志结构化 + 排播风险 |
| 决策节点 | ✅ 3个 | 市场判断/选品审核/发布审批 · 人工闸门生效 |
| 安全铁则 | ✅ SAFETY_RULES.md | v1.2 环境隔离+精准编辑+同步审批 · 注入CLAUDE.md |
| SQLite 数据库 | ✅ 7表 | pipeline_runs(5) · shop_health(5) · orders(4) · products(100) · milestones(24) |
| 管线审计 | 📋 已梳理 | 14项发现(P0×4/P1×4/P2×6) · 线下讨论决策 |

### 运行服务
- Flask :5001 · FastAPI :5004 · GPT-SoVITS :9880 · ComfyUI :8188 · Vite :5173 · easyclaw :8080

---

## 📜 版本修订历史（仅保留大版本）

| 版本 | 日期 | 修订人 | 核心变化 |
|------|------|--------|---------|
| v0.1~v1.0 | 04-09 ~ 04-23 | CEO + 工程经理 + Claude | 初始架构 → 双业务线分离 → 安全审查 → 正式定稿 |
| v3.3 | 04-24 | 阿牛 | 诚实修订: 完成度85%→35%，止血优先，GSTACK搁置 |
| v3.4 | 04-28 ~ 04-29 | 阿牛 + 外部评审 | 对抗审核增强 → 感知控制优先: 重建决策节点架构 |
| **v3.5** | **04-29** | **阿牛 + OpenClaw** | **Sprint 1.5完成: NLS/3-Agent/SQLite/6角色圣经/10模块覆盖 · 交互驾驶舱v2 · 决策节点** |
| **v3.6** | **04-30** | **阿牛 + OpenClaw + OpenCode** | **细节展开系统: 实体数据(非状态标签) · QA 80/80 · 脚本/角色/商品API · 6集管线全通 · 27→30端点** |
| **v3.7.0** | **05-01** | **阿牛 + OpenClaw + OpenCode** | **四大WBS冲刺: 管线监控/资产面板/分镜/剪辑合成/导演模式/反馈闭环/436定妆照** |
| v3.7.1 | 05-01 | OpenCode + 阿牛 | Dashboard JS全量语法修复(~274处) + 2xReferenceError+SyntaxError |
| v3.7.2 | 05-01 | OpenCode + 阿牛 | DM-1角色档案面板恢复(268行) + 缺失函数还原(applyDM1Filter等) |
| v3.7.3 | 05-01 | OpenCode + 阿牛 | MS-0门禁JS语法修复 + 跨业务线路由修复 + MS-2.3商品图工作台初版 |
| v3.7.4 | 05-02 | OpenCode + 阿牛 | MS-2.3工具箱重构(4张真实商品图卡片) · MS-5日报3按钮全通 + /api/publish · /api/l10n/retranslate/ · 面板15/15全量测试 · 重复id清零 |
| v3.7.5 | 05-02 | OpenCode + 阿牛 | pipeline_runs/shop_health表填充 · Vite :5173启动 · git remote token净化 · VERSION同步 · worktree同步 |
| v3.7.18 | 05-03 | OpenCode + 阿牛 | DM-6/7 质量评分条形图(配音🟢/画面🟡/合成🟠) + 文件规格卡(2列网格) · 管线日志替代裸文本(📦文件/🎤音频/🖼️渲染/🎬FFmpeg/⭐质量分类卡片) · DM-7排播风险检测(连续集鲁智深) · DM-3 SFX时间线 + 本地化审查按钮 · 版本缓存强制刷新 |
| v3.7.19 | 05-03 | OpenCode + 阿牛 | 📝编辑按钮→DM-1角色圣经自动展开编辑表单(身高/体型/面相/性格/配色/音色) · 🎤已配置→可点击跳转 · 语音→DM-3配音设计(正确管线节点) · 管线审计全面梳理(14项发现: P0=4/P1=4/P2=6) |
| v3.7.20 | 05-03 | OpenCode + 阿牛 | DM-1渲染图管理: ✕删除不良角度(DELETE /api/render) + ⚠️多角度一致性风险提示 + 🔁重新生成(POST /api/render/regenerate) · 3个后端API新增 · SAFETY_RULES.md(环境隔离+精准编辑+同步审批)注入CLAUDE.md · CLAUDE.md新增强制铁则#0.5 |

> 完整子版本详见表后附录（PHASE 1-5、QA报告、GAP清单）

### v3.6 子版本汇总 (05-01 合并)
| 版本 | 核心成果 |
|------|---------|
| v3.6.1 | QA全绿80/80 · 6集管线 · 25张角色渲染 · 30端点+Download API · 10项修复 |
| v3.6.2 | P0清零: DM-1角色卡·EPISODE_MAP·generate_script动态化·MS-0/1/3/5 stub补实·sfx全配 |
| v3.6.3~v3.6.5 | PHASE1-3: 假成功清洗·API对接·管线修复·LLM对抗审核CODING路线 |
| v3.6.6~v3.6.8 | UX审计(CEO): 11项UX全覆盖·Chart.js·5格式导出 |
| v3.6.9 | 109角色画廊页面 + SFX混音集成修复 |
| v3.6.10 | Dashboard UI: 科技清新风 + undefined filter + no-cache headers |
| v3.6.20 | PRD全量修订 (v3.6.9~v3.6.20 12个里程碑) + CLAUDE.md版本同步 |
| v3.6.24 | 补标注8端点/voice_clone/6角色/add_video_prompts脚本 · Task Completion Protocol强制引入 |
| v3.6.26 | 鲁智深basic_info补全 + LLM对抗审核管线验证 (CODING 93.8s 3.0/10) |
| v3.6.27 | 诚实收尾: visual_bible修复 + reReviewDM0 + 铁则强化 + 全量推送 |
| v3.6.28 | 剧本EP07-10 (武松打虎/西门庆/林冲雪夜/大闹五台山) + triggerReReview端点 + 定妆照替换 |
| v3.6.29 | DM-1性能优化(Top10+搜索+筛选+懒加载) + openclaw演员109/109完成 + GPT-SoVITS修复 |

### v3.7 子版本汇总
| 版本 | 核心成果 |
|------|---------|
| v3.7.0-P0~S4 | 预冲刺止血·资产面板·分镜选择器·剪辑合成·导演模式+反馈闭环 |
| v3.7.1 | Dashboard JS全量语法修复(~274处) |
| v3.7.2 | DM-1角色档案面板恢复 |
| v3.7.3 | 跨业务线路由修复 · MS-0门禁报告 · MS-2.3商品图工作台初版 |
| v3.7.4 | MS-2.3工具箱重构 · MS-5日报预览/推送/历史 · 15面板全量测试 · /api/publish · /api/l10n/retranslate/ |
| v3.7.5 | SQLite pipeline_runs(5)/shop_health(5)填充 · Vite :5173启动 · git token净化 · VERSION同步 |
| v3.7.6 | MS-2.3 数据过滤/状态映射/图片路径修复 |
| v3.7.7 | MS-2.3 强制数据适配+角色残骸清理+兜底占位图 · detailEl typo修复 · JS语法修复(img onerror) |
## 📊 PHASE 1-4 完成记录 (v3.6.4 新增)

### PHASE 1: 安全止血与数据卫生 (commits 040e061, 8208b6f, 28a4bd2)

| 任务 | 修复内容 | 验证 |
|------|---------|------|
| 假成功清洗 | 11条 `STATUS: completed` → `⚠️ MOCK` | `shared/logs/executions/` 全部修正 |
| execution_logger 加固 | 移除 `echo`/`ls` 允许前缀, 委托 base_executor `shell=False` | `validate_command()` 统一安全策略 |
| ffmpeg PATH 对齐 | `_find_ffmpeg()` 动态解析, 替代 Cellar 硬编码 | `drama_merge.py`, `pillow_storyboard.py` |
| quality_assessor 语法 | py_compile 验证通过 | 恢复至 `skills/water-margin-drama/` |
| CLAUDE.md 同步 | v3.6.2 标题 + 铁则: 假成功判定 | 完成度 82%/68% |

### PHASE 2: 前端 Cockpit API 对接 (commits b030875, 8cd42df, ada684c, d6f71c0, 67b01ba)

| 端点 | 修复前 | 修复后 | commit |
|------|--------|--------|--------|
| `/api/render/ep<ep>/shot_<n>.png` | 404 (前端按 episode 请求, 后端按 character 存储) | 200 → 别名路由 | b030875 |
| `/api/script` list | 无 `scene_count`/`render_files` | 返回渲染统计 | 8cd42df |
| `/api/script/3` | 404 (前端 `parseInt` 去零, 后端只认 "03") | `zfill(2)` 自动补零 | 8cd42df |
| `/api/decision` | 404 (任务文件不存在) | 宽容模式 → 写入 decisions 目录 | 8cd42df |
| `/api/script/3` 详情 | 无渲染统计 | 补充 `scene_count` + `render_files` | ada684c |
| `drama_merge.py` | `ModuleNotFoundError` (非项目根调用) | `sys.path.insert(PROJECT_ROOT)` | d6f71c0 |
| `pillow_storyboard.py` | 同上 | 同上 | d6f71c0 |
| `role_designer.py` | core/ 和 skills/ 双副本(内容不同) | 删除 core/ 过期副本(318行) | 67b01ba |

**端到端验证**: 38/38 API 端点 200 ✅（42 curl + 10 pytest PASS + v3.7 新增 SSE流式审核）

### PHASE 3: 管线修复 (commit 197591a)

| 修复 | 内容 |
|------|------|
| `drama_pipeline.yaml` v1.2 | 路径修正 + MS-4.5 对抗审核 |
| 9 阶段干跑 | MS-1~MS-8 全部 `--help`/`py_compile` 通过 |
| `shared/core/utils.py` | `_find_ffmpeg`/`_find_ffprobe` 共享工具 |

### PHASE 4: Dashboard 增强 (commit 197591a)

| 功能 | 状态 |
|------|------|
| P4-01 待决策黄色高亮 | ✅ |
| P4-02 MS-2.3 修改意见面板 | ✅ |
| P4-03 实时刷新 | ✅ |
| P4-04 决策面板增强 | ✅ |

### PHASE 5: LLM对抗审核管线集成 (v3.6.5)

| 任务 | 修复内容 | 验证 |
|------|---------|------|
| CODING 路线打通 | `adversarial_review.py` 模型 `aliyun/` → `coding/` + `.env` 自动加载 | 单Agent ~87s, 3-Agent ~100s, 0费用 |
| Dashboard 命令修正 | `detail_engine.py:480` 从 `--mode multi-agent` → `drama_script --mock` | 用户可见命令已同步 |
| pipeline 集成 | `pipeline_ep01.py` 新增 `--review mock/coding` 参数 | py_compile ✅ · dry-run 展示 Step 5 |
| drama_pipeline.yaml | MS-4.5 命令修正为 `drama_script --mock` | 防止 100s 超时 |
| 审核结果示例 | EP03 shot_01: 综合评分 3.8/10 → reject | 4维度真实审计: 编剧/分镜/逻辑/节奏 |
| CODING 额度 | Plan 剩余 48 天 / 48% | 足够日常审核使用 |


## 附录 A：双业务线里程碑矩阵（v3.6 更新）

### 🛒 TK 运营自动化 (13 里程碑)

| ID | 名称 | 类型 | 状态 | v3.6 更新 |
|----|------|------|------|-----------|
| MS-0 | 采集门禁 | 决策点 | ✅ | — |
| MS-1 | 数据采集 | 自动 | ✅ | — |
| MS-1.5 | 市场判断 | **你决策** | ✅ | AI五维分析→已批准 |
| MS-2 | 选品分析 | **你决策** | ✅ | TOP3: 蓝牙耳机8.42 |
| MS-2.1 | 内容本地化 | 自动 | ✅ | 5国15模板 |
| MS-2.2 | 类目映射 | 自动 | ✅ | TK类目匹配 |
| **MS-2.3** | **图像适配** | 自动 | **🏗️ 进行中** | **rembg已安装·4张产品图可查看·POST /api/images/{id}/process 可用·rembg→resize→compliance全流程通** |
| MS-2.4 | 定价策略 | 自动 | ✅ | 5国定价·8步利润计算公式 |
| MS-2.5 | 物流模板 | 自动 | ⏳ | 5国物流方案已分析·待配置 |
| MS-2.6 | 合规检查 | 自动 | ✅ | 3-Agent审核通过 8.24/10 |
| MS-3 | 发布准备 | 自动 | ✅ | 3品待发 |
| MS-4 | 发布审批 | **你决策** | ⏸️ | 等待 MIAOSHOW_PUBLISH_ENABLED |
| MS-5 | 日报推送 | 自动 | ✅ | 飞书日报 |

### 🎬 AI 数字短剧制造流水线 (11 里程碑)

| ID | 名称 | 类型 | 状态 | v3.6 更新 |
|----|------|------|------|-----------|
| **DM-0** | **剧本审核** | 自动 | **✅ 管线就绪** | **完整剧本查看/编辑/导出·5段式分镜故事板·LLM审核CODING路线通(~90s/0费)·pipeline --review 开关·shuihuzhuan.yaml实时同步** |
| **DM-1** | **角色设计** | 自动 | **✅ 档案就绪** | **角色 Bible v3.6.7: 8角色完整档案(性格/口头禅/习性/服饰/背景/关系) · 编辑模式+颜色选择器 · AI生成+重渲染检测 · 6角色前端面板(武松/鲁智深/林冲/宋江/李逵/吴用)** |
| DM-2 | EP01 鲁提辖拳打镇关西 | 自动 | ✅ | final.mp4 2.3MB/23s ComfyUI+NLS |
| DM-3 | EP02 鲁智深倒拔垂杨柳 | 自动 | ✅ | final.mp4 2.3MB/23s ComfyUI+NLS |
| DM-4 | EP03 林冲风雪山神庙 | 自动 | ✅ | **final.mp4 2.0MB/23s ComfyUI+NLS** |
| DM-5 | EP04 宋江怒杀阎婆惜 | 自动 | ✅ | **final.mp4 1.9MB/23s ComfyUI+NLS** |
| DM-6 | EP05 李逵沂岭杀四虎 | 自动 | ✅ | **final.mp4 2.0MB/23s ComfyUI+NLS** |
| DM-7 | EP06 智取生辰纲 | 自动 | ✅ | **final.mp4 1.8MB/23s ComfyUI+NLS·非暴力·首发推荐** |
| DM-V | AI视频升级 | **你决策** | ⏸️ | 推荐Kling(微信¥15/EP)·ComfyUI静态图过渡方案已就绪 |
| DM-S | NLS配音引擎 | 自动 | ✅ | 阿里云TTS 4音色 ~29817/30000字符 |
| DM-F | 视频合成管线 | 自动 | ✅ | ComfyUI+Pillow+ffmpeg --episode切换 |

---

## 📜 v3.5.4 → v3.6 核心修订摘要

| 维度 | v3.5.4（旧） | v3.6（新） |
|------|-----------|-----------|
| **核心问题** | 明细面板只显示状态标签(ok/ng) | **明细面板返回实体数据 (before/after/source/建议)** |
| **DM-0 剧本** | 摘要文本: "14集完整剧本" | **可查看/编辑/HTML导出·5段分镜故事板·POST修改实时同步shuihuzhuan.yaml** |
| **DM-1 角色** | 纯文本: "武松 188cm" | **ComfyUI渲染角色图·角色编辑API·音色/配色选择** |
| **MS-2.3 图像** | 纯文本: "phone_case_main.jpg 800×800" | **rembg已安装·图片展示·POST /api/images/{id}/process 一键rembg→resize→compliance** |
| **LLM审核** | 命令路径错误: `shared/adversarial_review.py` | **修正为 `shared/core/adversarial_review.py`** |
| **信息摘要** | 无 | **全球信息摘要面板（/info）·123条信息·10订阅源·TK相关度过滤** |
| **API端点数** | ~15 | **27个端点全部200** |
| **Flask 路由** | dashboard/info/api/dashboard/api/decision/api/detail | **+ /api/script, /api/script/{ep}, /api/script/{ep}/export, /api/character/{name}, /api/images, /api/images/{id}, /api/images/file/{f}, /api/images/{id}/process, /api/render/{char}/{f}, /api/info/items** |


## ⚠️ 当前真实完成度（v3.6.1 诚实评估）

> **双口径**: 基础设施脚本(脚本存在、CLI可运行) vs 核心控制功能(感知/决策/控制真实可用)
> **QA口径**: 自动化测试 (80/80 PASS)

| 模块 | v3.6 基础设施 | v3.6 核心控制 | v3.6.1 基础设施 | v3.6.1 核心控制 | 变化说明 |
|------|-------------|-------------|---------------|---------------|----------|
| 剧本生成/管理 | 85% | 70% | 85% | 75% | Download API + ep_num路由修复 |
| 角色设计 | 80% | 65% | 85% | 75% | 拼音/中文双通 + 25张渲染图(6角色) + voice/color POST |
| 图像适配 (MS-2.3) | 65% | 50% | 75% | 60% | push_erp→妙手草稿箱 + 4 action + 404边界 (1产品6变体) |
| 对抗审核框架 | 75% | 60% | 75% | 60% | DM-V/DM-F/DM-10新增 + import路径修正 |
| 驾驶舱决策界面 | 75% | 60% | 80% | 65% | Dashboard smart routing (DM-0/DM-1/MS-2.3) + inline编辑 |
| 信息订阅 | 80% | — | 85% | — | 139 items + 来源标注 |
| Dashboard HTML | 70% | — | 80% | — | 图片画廊 + 故事板展开/TXT+SRT下载 + zoom modal |
| 订单履约 | 60% | — | 75% | 55% | fulfillment_events表 + tracking + stats + 4条测试数据 |
| 6集管线 (ComfyUI+NLS) | — | — | **100%** | **100%** | EP01-06 ALL final.mp4 (1.8-2.4MB, 23s/集) |
| **总体（基础设施）** | **~78%** | — | **~82%** | — | 30端点 + ~6200行 |
| **总体（核心控制）** | — | **~62%** | — | **~68%** | QA 80/80 PASS·全部端点+边界验证 |
| **QA自动化** | — | — | — | **80/80** | 端点/文件/DB/边界 全覆盖 |
| **⚠️ 前端 UX（用户可用）** | — | — | — | **~30%** | 11项关键UX 0/11 实现（详见§v3.6.6 UX审计） |

---

## 📊 v3.6.6 UX 诚实审计（CEO 黄光耀评估 + 阿牛代码验证）

> **评估方法**: CEO 基于 20 年 IT 系统交付经验，以用户视角逐项验证。阿牛对照代码实锤验证每一项。
> **核心发现**: 后端 API 返回 200 + 80/80 QA 测试通过 = 内部指标几乎达标；**外部指标（用户真实可用性）严重滞后**。

### 逐项验证结果

| # | CEO 声称的差距 | CEO 评级 | 代码验证结果 | 实际状态 |
|---|--------------|---------|-------------|----------|
| 1 | 详情页默认展开全部明细，信息密度过高 | 🔴 高 | `milestone-summary`/`milestone-detail-content` 0 匹配；仅 `toggleSB()`(故事板) 和 `toggleCharEdit()`(角色编辑) 有折叠 | ❌ **确认**: 无通用折叠结构 |
| 2 | DM-0 审核只有总分，看不到四维度明细 | 🔴 严重 | 前端仅处理 `rv_score`(总分) + `rv_decision`(决策) + `findings`(笔记数组)；无编剧/分镜/逻辑/节奏分项 | ❌ **确认**: 四维度后端也未返回分项 |
| 3 | 修改后无法自动触发流程重走 | 🔴 关键 | `reset`/`重新审核`/`重走` 0 匹配；修改后无自动重置逻辑 | ❌ **确认**: 完全缺失 |
| 4 | 文件下载入口不统一 | 🟡 中 | 仅故事板区域有 TXT/SRT 按钮 (`downloadScript()`)；无统一下拉菜单 | ❌ **确认**: 分散在各处 |
| 5 | 产品图片无并排对比视图 | 🟡 中 | `.prod-compare` CSS 类存在但 JS 渲染函数 **未调用**；实际用 `img-gallery` 平铺 | ⚠️ **部分确认**: CSS 就绪，JS 未用 |
| 6 | 详情页无灵活伸缩/折叠 | 🔴 高 | 同上 #1 | ❌ **确认** |
| 7 | 缺少数据可视化图表 | 🟡 中 | `Chart.js`/`chart`/`canvas` 0 匹配 | ❌ **确认** |
| 8 | 修改意见提交后无反馈/无法触发重处理 | 🟡 中 | `textarea` 存在但提交后无状态反馈；无自动重处理 | ⚠️ **确认** |

### 11项关键 UX 功能覆盖率 (v3.7.8 更新)

| UX 功能 | v3.7.5 (前) | v3.7.8 (当前) | 代码证据 |
|---------|-------------|---------------|----------|
| 1. 摘要优先折叠/展开详情页 | ❌ 0% | ✅ **100%** | `renderMilestoneSummary` + `accordion-content` + `toggleSection` |
| 2. DM-0 四维度审核明细展示 | ❌ 0% | ✅ **100%** | `renderFourDimReview` 可折叠维度卡片(问题+建议) |
| 3. 修改→重处理→审核自动循环 | ❌ 0% | ✅ **80%** | `reReviewAfterEdit` + `showReReviewDialog` + 新旧分对比 |
| 4. 统一下载入口（下拉菜单） | ✅ 100% | ✅ **100%** | 顶部栏📥 + 里程碑📥 + 剧集MP4/TXT/SRT |
| 5. 图片并排对比视图 | ⚠️ 10% | ✅ **80%** | `img-compare-container` 原图/处理后/feedback/重新处理 |
| 6. 音色试听 | ❌ 0% | ❌ **0%** | 未在 Sprint 范围内 |
| 7. Chart.js 数据可视化 | ✅ 100% | ✅ **100%** | 利润瀑布图(8步) + 审核5维雷达 + 管线时间轴 |
| 8. 处理进度反馈（加载动画） | ⚠️ 20% | ✅ **60%** | 实时审核日志面板 + 角色渲染进度条 + 批量处理进度提示 |
| 9. Dashboard 搜索与过滤 | ✅ 80% | ✅ **80%** | 同左 |
| 10. 质量反馈知识库 | ❌ 0% | ❌ **0%** | 未在 Sprint 范围内 |
| 11. 自愈提示（连续失败提醒） | ❌ 0% | ❌ **0%** | 未在 Sprint 范围内 |
| **总计** | **~48%** | **~70%** | **11项中 6 项 100% + 3 项 80% + 12 项 60%（新增: 技术检查可视化卡片）** |

### 根本原因（与 CEO 分析一致）

1. **后端验证 ≠ 用户验证**: 80/80 QA 测试全为 curl/pytest 级别，**无一人模拟真实用户在浏览器上走完完整流程**
2. **前后端独立开发**: 后端 API 测试通过即标记完成，前端未做端到端用户流程验证
3. **完成定义偏差**: "API 返回 200" 被当作完成标准，但用户需要的是 "打开页面 → 看到信息 → 理解内容 → 做出决策 → 执行操作" 的完整闭环

### 补救路线（CEO WBS 确认）

| 冲刺 | 时间 | 核心任务 | 验收标准 |
|------|------|---------|----------|
| **Sprint 1** | 05-02 已完 | ✅ 摘要优先折叠设计 + DM-0 审核四维度 + 修改→重审循环 + 统一下载 + 图片对比 | 打开任意里程碑先见摘要，点击才展开详情 |
| **Sprint 2** | 05-02 已完 | ✅ 修改重走闭环 + 文件就地访问 + MP4内嵌播放 + 就地下载 + 剧本内嵌预览 | 改剧本后能重审，产品图并排对比，视频页面播放 |
| **Sprint 3** | 05-02 已完 | ✅ 利润瀑布图(8步) + 审核5维雷达图(点击展开说明) + 横向时间轴 | 瀑布图/雷达图/时间轴全部可用 |
| **Sprint 4** | 05-02 已完 | ✅ 验收测试清单 + PRD同步 | 7条反馈逐条测试 + PRD版本更新 |
| **未来** | 待定 | 音色试听 + 质量反馈知识库 + 自愈提示 | 剩余3项0%功能补齐

**核心原则**: 暂停新功能开发（环境音效/5国字幕/竞品 API 全部延后），**专注体验补课**。

### v3.6.8 P1 UX 补齐记录 (commit 7493dba)

| UX # | 功能 | 修复内容 | 验证 |
|------|------|---------|------|
| P1-4 | 统一下载按钮 | 顶部栏「📥 导出」按钮 → 下拉菜单 → 5格式导出 | JSON/CSV/CSV决策/Markdown/HTML 全部生成成功+浏览器下载 |
| P1-6 | Chart.js 数据可视化 | 3种视图切换: 状态分布(环形图) / 数据源(环形图) / 管线对比(柱状图) | 自动注入 detail 面板 · Chart.js CDN 加载 · 3种模式切换正常 |
| CSS 清理 | 下载 CSS 重复定义修复 | `.dl-menu`/`.dl-dropdown` 两套冲突定义 → 统一为 `.dl-wrap`/`.dl-btn`/`.dl-panel` | 样式无冲突，下拉菜单定位正确 |

**文件**: `dashboard/task_board.html` 1622→2010 行 (+388/-11)
**JS**: 630/630 括号平衡 · 59 函数(+10) · 99.5KB
**新增函数**: `toggleDlPanel()`, `downloadAs()`, `triggerDownload()`, `renderChartPanel()`, `switchChart()`, `updateChart()`

### v3.6.6 UX 补齐记录 (commit 561a9c9)

| UX # | 功能 | 修复内容 | 验证 |
|------|------|---------|------|
| UX-1 | 图片对比视图 | `toggleCompare()` 分屏对比，labels 自动标注 | 2+图片点击切换对比/普通模式 |
| UX-2 | 真实进度反馈 | 按钮 busy 状态 + `refreshStatus` 同步指示 + changed 检测 toast | 操作时按钮变灰+"处理中..." |
| UX-3 | 键盘快捷键 | `←/→` Tab 切换 · `↑/↓` 列表导航 · `Enter` 打开 · `Esc` 关闭/返回 · `R` 刷新 · `/` 搜索 · `?` 快捷键面板 | `keydown` 全局监听，input/textarea 中自动跳过 |
| UX-4 | 管线监控面板 | `renderPipelineMonitor()` 检测 Flask/GPT-SoVITS/ComfyUI 端口 + 管线总进度 | `fetch()` HEAD 检测 + `/api/dashboard` 统计 |
| UX-6 | 刷新状态指示 | `setRefreshStatus()` + `refresh()` 重写 + changed 检测 toast | 同步中时黄色脉冲 + 待决策自动告警 |
| UX-7 | 模态点击关闭 | `closeModal()` 统一入口，背景点击 + Escape 双路径 | `onclick="closeModal()"` |
| UX-8 | 左侧键盘导航 | `.kb-focus` 样式 + `↑/↓` 导航 + `Enter` 点击 | `scrollIntoView({block:'nearest'})` |
| UX-9 | 统计 Tooltip | `initStatTooltips()` hover 说明 | stat 数字 `cursor:help` + `title` |
| UX-10 | 搜索高亮 | `highlightText()` + render 后 patch `<mark>` | 搜索关键词黄色高亮 |
| UX-11 | 空状态引导 | `renderSummary()` 追加操作提示 | Tab 切换时显示对应引导文案 |

**文件**: `dashboard/task_board.html` 1185→1310 行 (+318/-2)
**JS**: 406/406 括号平衡 · 49 函数(+18) · 47KB

---

## 第一部分：产品概述

### 1.1 产品定位

Agentic OS v3.6 是一个**基于智能体架构的双业务线自动化中台**，通过统一基座管理 TK 跨境电商运营和 AI 数字短剧制作两条独立业务线。产品以"**一个指令启动、全程自动执行、关键节点等你决策**"为核心体验。

**v3.6 核心升级**: 所有明细面板从"ok/ng"状态标签升级为**实体数据展示**——每个步骤显示 before/after 对比、数据源标签（[真实]/[模拟]/[推算]）、实体列表、推理链条。

### 1.2 三层架构

```
┌───────────────────────────────────────────────────────────┐
│  🧑 你 — 飞书卡片 + Dashboard 网页                         │
│  感知(看到状态) → 判断(看懂数据) → 决策(点通过/修改/驳回)     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  📱 飞书决策层 (你每天接触的界面)                             │
│  ┌─────────────────────┐  ┌──────────────────────┐         │
│  │ 日报卡片              │  │ 决策卡片              │         │
│  └─────────────────────┘  └──────────────────────┘         │
│                                                           │
│  🖥️ Flask Dashboard (:5001) — v3.7 38+端点 (Flask 30+ · FastAPI 8+)               │
│  ┌─────────────────────┐  ┌──────────────────────┐         │
│  │ 指挥中心 /dashboard   │  │ 全球摘要 /info         │         │
│  │ 剧本详情 /api/script  │  │ 角色图 /api/render     │         │
│  │ 图片处理 /api/images  │  │ 里程碑 /api/detail     │         │
│  └─────────────────────┘  └──────────────────────┘         │
│                                                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  🤖 自动化执行层                                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐  │
│  │ 数据分析  │ │ 内容本地化│ │ ComfyUI渲染器 │ │ bg_remove│  │
│  │ analytics │ │ localization│ comfyui_render│ │ image_processor│
│  └──────────┘ └──────────┘ └──────────────┘ └──────────┘  │
│                                                           │
│  📦 数据层                                                 │
│  妙手ERP / TikTok API / 阿里云NLS / ComfyUI (本地SDXL)      │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## 第二部分：v3.6 新增功能模块

### 2.1 剧本管理系统（DM-0）

**文件**: `shared/script_manager.py` (454行)

| 功能 | API 端点 | 说明 |
|------|---------|------|
| 剧本列表 | `GET /api/script` | 6集概要: 标题/主角/评分/渲染状态 |
| 剧本详情 | `GET /api/script/01` | 5段式分镜故事板 + 角色设计 + 审查规则 |
| 剧本修改 | `POST /api/script/01 {"title":"新标题"}` | 修改shuihuzhuan.yaml + CURRENT_EPISODES 实时同步 |
| HTML导出 | `GET /api/script/01/export?format=html` | 完整排版HTML文件（含角色设计/分镜/审查规则） |
| TXT导出 | `GET /api/script/01/export?format=txt` | 纯文本剧本导出 |

**故事板模板覆盖**:
- ✅ 鲁提辖拳打镇关西 (5段: 渭州酒馆→肉铺→三拳→街头)
- ✅ 鲁智深倒拔垂杨柳 (5段: 菜园→展示→拔树→震撼→归隐)
- ✅ 林冲风雪山神庙 (5段: 草料场→山神庙→密谋→复仇→梁山)
- ✅ 宋江怒杀阎婆惜 (5段: 书房→威胁→争吵→刺杀→黎明的决心)
- ✅ 杨志卖刀 (5段: 市集→挑衅→演示→杀牛二→入狱)
- ✅ 智取生辰纲 (5段: 策划→山路→博弈→得手→消失)

**已修正**: LLM审核命令从 `shared/adversarial_review.py` 修正为 `shared/core/adversarial_review.py`

### 2.2 ComfyUI 静态图渲染器（DM-1）

**文件**: `shared/comfyui_renderer.py` (215行)

**本地环境**: ComfyUI :8188 + SDXL 1.0 + Apple M2 Max 38核 GPU

| 功能 | 命令 | 说明 |
|------|------|------|
| 测试 | `--test` | 512×912 小图验证连通（~30秒/张） |
| 单集 | `--episode 01` | 渲染1集3镜角色图 |
| 全量 | `--all` | 6集×3镜=18张（~15分钟） |
| 参数 | `--width 768 --height 1344 --steps 25` | 9:16 竖屏 TikTok规格 |

**已完成渲染**:
- ✅ **109角色×4角度 = 436张定妆照** (ComfyUI SDXL · 768×1024 · 476MB)
- ✅ 109角色 portrait_0.png 全量输出（纯中文目录名）
- ✅ EP01-EP10 每集角色渲染（武松/鲁智深/林冲/宋江/李逵/吴用/杨志/晁盖/花荣/扈三娘…）

**质量评估**: 静态图 5/10 → Pillow字帧 2/10 → 目标AI视频 8.5/10

### 2.3 商品图片处理系统（MS-2.3）

**文件**: `shared/core/image_processor.py` (208行) + task_wizard.py image API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/images` | GET | 产品图片列表（从catalog.json） |
| `/api/images/{id}` | GET | 单张图片元数据 + 变体列表 |
| `/api/images/file/{filename}` | GET | 图片文件服务（支持原图/nobg/final） |
| `/api/images/{id}/process` | POST | 处理请求: `{"action":"rembg|resize|full|check"}` |

**已安装**: rembg (pip3 安装) + Pillow

**处理流水线**:
1. `rembg`: 去背景 → 纯白底（输出 `_nobg.jpg`）
2. `resize`: 1:1 居中裁剪 → 1000×1000px（输出 `_final.jpg`）
3. `check`: 合规检查（尺寸/分辨率/文件大小）
4. `full`: 一键 rembg→resize→compliance（输出 `_final.jpg`）

**已验证**: phone_case_main.jpg 通过 full 流水线（rembg: ok → resize: ok → compliance: pass）

### 2.4 全球信息摘要

**页面**: `http://localhost:5001/info`
**API**: `GET /api/info/items` — 从 `~/.agentic-os/info_subscriber/items.json` 读取

**数据**: 123条信息 · 10订阅源 · 按发布时间排序 · TK关键词自动打标

**页面特性**:
- 科学清新风格（暗蓝渐变 → 浅色卡片对比布局）
- 顶部统计栏: 订阅源/总条目/今日新增/实时标识
- 来源分布条: Reddit/YouTube/Blog 占比
- 筛选Tabs: 全部 | TK电商 | Reddit | YouTube | Blog
- 每张卡片: 来源徽章 + 可点击标题链接 + 摘要 + TK相关度进度条

### 2.5 角色设计编辑 API（DM-1）

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/character/{name}` | GET | 返回角色设计 + 渲染图列表 |
| `/api/character/{name}` | POST | 更新角色属性: `{"voice":"zhiqiang","color":"#ff6b6b","traits":["新特性"]}` |
| `/api/render/{char_id}/{filename}` | GET | 渲染图文件服务 (PNG), 修复 pinyin→CN 回退 (109角色全通，REVERSE_MAP) |
| `/api/character/{name}` | POST | 更新角色: voice/config/video_prompts (JSON深合并) — 108将全支持 |

**支持角色**: 武松 / 鲁智深 / 林冲 / 宋江 / 杨志 / 晁盖 / 李逵 / 吴用 / 花荣 / … (108将全覆盖, 109位含晁盖)
**角色属性**: traits / height / face / weapon / voice / color / video_prompts(三方案)
**渲染图**: 109角色×1 PNG (portrait_0.png, 纯中文目录名)
**音色**: 108个 CHARACTER_VOICES (NLS TTS参考音频 + GPT-SoVITS s2Gv3.pth)

---

## 第三部分：当前架构明细

### 3.1 API 端点全景（38端点，v3.7.3更新）

```
Flask :5001 (shared/task_wizard.py)
├── 页面
│   ├── /dashboard          — 指挥中心 HTML (v3.6 smart routing)
│   ├── /info               — 全球信息摘要 HTML (139 items)
├── 仪表盘
│   ├── /api/dashboard      — 24里程碑状态
│   ├── /api/detail/<ms_id> — 里程碑详情(DM-0~10, MS-2.1~4, DM-V/F)
│   ├── /api/decision       — 决策操作 POST
│   ├── /api/tasks          — 任务列表(兼容)
├── 剧本 (NEW v3.6)
│   ├── /api/script         — 6集剧本列表
│   ├── /api/script/<ep>    — 单集剧本详情(GET)+修改(POST)
│   └── /api/script/<ep>/export — 导出 txt/html/srt/json
├── 角色 (NEW v3.6)
│   ├── /api/character/<name> — 角色设计查看/修改 (CN+PY双通)
│   └── /api/render/<char>/<file> — ComfyUI渲染图 (25 PNG)
├── 图片 (NEW v3.6)
│   ├── /api/images          — 产品图列表 (1产品6变体)
│   ├── /api/images/<id>     — 单张产品图 (orig/nobg/final, 404)
│   ├── /api/images/file/<f> — 图片文件
│   └── /api/images/<id>/process — 图片处理 (rembg/full/check/push_erp)
├── 下载 (NEW v3.6.1)
│   └── /api/download?name=  — 剧本下载 ep01.txt/html/srt/json
├── 信息 (NEW v3.6)
│   └── /api/info/items      — 全球信息摘要数据 (139 items)
├── 任务向导
│   ├── /api/task/wizard/knowledge
│   ├── /api/task/wizard/description-guide
│   ├── /api/task/wizard/validate-title
│   ├── /api/task/wizard/recommend
│   └── /api/task/wizard/create
└── 兼容
    └── /api/status          — 系统运行状态
```

## 3.2 关键文件清单 (v3.6.2更新)

| 文件 | 行数 | v3.6.2状态 | 说明 |
|------|------|-----------|------|
| `shared/task_wizard.py` | 740 → 820+ | — | Flask主服务·30端点·CORS·/api/render/拼音回退(REVERSE_MAP) · 109角色全通 |
| `shared/detail_engine.py` | 797 | — | 14里程碑·DM-1角色卡全修复(108将全量)·MS-0/1/3/5 stub补实·0处stale引用 |
| `shared/script_manager.py` | 454 → 500+ | **UPDATED** | 剧本查看/编辑/导出·6集故事板·YAML同步·CHARACTER_ID_MAP 108条目·_get_render_dir简化 |
| `shared/comfyui_renderer.py` | 259 | **UPDATED** | ComfyUI SDXL 渲染器·--help likui/wuyong修正 |
| `shared/core/image_processor.py` | 240 | — | rembg·resize·compliance·push_to_erp_draft |
| `shared/core/tk_pipeline_db.py` | 731 | — | orders扩展+fulfillment_events·4条测试数据 |
| `shared/analytics_engine.py` | 700 | **UPDATED** | EPISODE_MAP ep05李逵/ep06吴用·DRAMA_EMOTIONAL_ARCS更新 |
| `shared/core/sfx_engine.py` | 497 | **UPDATED** | 11音效类型(含喧哗/拳击/木材)·6集全配·sfx_manifest.json |
| `shared/localization_reviewer.py` | 268 | — | 5国LLM翻译·禁忌词过滤·可读性评分 |
| `shared/decision_engine.py` | 345 | — | 3-Agent审核→DecisionBrief·风险矩阵 |
| `shared/core/adversarial_review.py` | 886 | — | 3-Agent对抗审核框架·6场景 |
| `dashboard/task_board.html` | 3684行 / 203KB | **v3.7.3** | 10功能模块 · JS括号1532/1532 · 108 CHARACTER_VOICES · 音色卡片(试听/生成/配置) · video_prompts三方案渲染 · Chart.js 3视图 · 5格式导出 · 科技清新风 · DM-1跨业务线路由修复(22:07) |
| `dashboard/info_board.html` | 300+ | — | 全球信息摘要·科学清新风格·筛选Tabs |
| `~/.agentic-os/character_designs/` | — | — | visual_bible.json (109角色含video_prompts) · renders/<中文名>/portrait_0.png (109目录) · gallery.html |
| `~/.agentic-os/episode_*/final.mp4` | — | — | EP01-EP10 全量输出 (1.8-2.1MB/集) |
| `~/GPT-SoVITS/output/` | — | **NEW** | 108个参考音频: <fid>_nls_ref.wav (107 NLS) + wusong_cosyvoice.wav (CosyVoice原声) |
| `~/.agentic-os/products/` | — | — | catalog.json + images/ 1产品6变体图(jpg/nobg/final) |
| `~/.agentic-os/miaoshou_draft/` | — | — | 妙手ERP草稿箱同步 (phone_case_main.json+jpg) |
| `~/.agentic-os/info_subscriber/items.json` | — | — | 123条信息摘要 |

---

## 第四部分：v3.6.1 QA 测试报告（80/80 PASS）

### 测试套件 v3.6.1 完整结果

| 模块 | 测试数 | 结果 | 说明 |
|------|--------|------|------|
| Smoke | 3 | ✅ | Dashboard / Info / Status 全200 |
| Script API | 14 | ✅ | List 6集 + Detail 6集×5场景 + Edit+Restore + 4格式导出 |
| Character API | 14 | ✅ | CN+PY双通(12查) + POST更新 + 404边界 |
| Render | 2 | ✅ | 18 pipeline PNGs + 404 handled |
| Image API | 8 | ✅ | List + GET + 404 + 3项process + ERP push + file serve |
| Download | 26 | ✅ | 6集×4格式(24条) + bad name 400 + missing 404 |
| Order DB | 1 | ✅ | 4 orders, $328.70, 2 in_transit + tracking |
| Decision+Detail | 7 | ✅ | Decision(404=不存在) + DM-0/1/MS-2.3/V/F/10 |
| Info | 1 | ✅ | 139 items |
| Task Wizard | 3 | ✅ | Knowledge + Desc Guide + Validate Title |
| Edge Cases | 3 | ✅ | Script 404 + Process bad action + DL missing |
| Files (offline) | 3 | ✅ | Pipeline 6/6 mp4 + 25 PNGs + ERP 2 files |
| **总计** | **80** | **✅ 80/80** | **全端点 + 全边界 + 全文件 通过** |

### 终端到终端验证

```
# 剧本：列表 → 查看 → 编辑 → 恢复 → 导出
curl /api/script                     ✓ 6 episodes
curl /api/script/ep06                ✓ 智取生辰纲 · 5 scenes · 6 renders
curl -X POST /api/script/06 -d '...' ✓ 编辑+恢复
curl /api/download?name=ep06.srt     ✓ 字幕导出 (6集×4格式)

# 角色：CN → PY → 渲染 → 修改
curl /api/character/鲁智深           ✓ 195cm · 6 renders
curl /api/character/luzhishen        ✓ pinyin→鲁智深 · 6 renders
curl /api/render/luzhishen/ep01_shot_01.png ✓ 18张全通

# 商品：列表 → 处理 → ERP推送 → 文件
curl /api/images                     ✓ 4 products
curl -X POST /api/images/.../process ✓ rembg→nobg · full→final · check→pass
curl -X POST /api/images/.../process -d '{"action":"push_erp"}' ✓ 妙手草稿箱

# 详情：全里程碑实体数据
curl /api/detail/DM-V                ✓ Kling vs fal.ai · DM-F 管线步骤
curl /api/detail/DM-0                ✓ 故事板展开 · DM-1 角色画廊
```

---

## 第五部分：三个决策节点（v3.6 增强）

与 v3.5 相同，但在 v3.6 中，每个决策节点的明细面板现在展示实体数据：

### 节点A：市场判断
**新增**: 点击 MS-1.5 → `/api/detail/MS-1.5` 返回五维市场评分 + 品类趋势数据 + 季节性分析

### 节点B：选品审核  
**新增**: 点击 MS-2 → `/api/detail/MS-2` 返回 8步利润公式(before/after each step) + 5维竞品维度含来源标签 + 供应商对比

### 节点C：发布审批
**新增**: 硬约束保持 `MIAOSHOW_PUBLISH_ENABLED=true` + `human_approved: true`

---

## 第六部分：GAP 清单（v3.7.3 诚实标注）

> 同类信息已合并至第八部分（下一步计划），本部分只保留实锤已完成的GAP。

### ✅ 已关闭 GAP

| GAP | 关闭版本 | 实锤 |
|-----|---------|------|
| Dashboard HTML 图片展示 | v3.6.1 | DM-0/DM-1/MS-2.3 img-gallery + zoom modal |
| Dashboard HTML 编辑表单 | v3.6.1 | inline textarea编辑 + POST保存 |
| EP03-06 运行 | v3.6.1 | EP01-06 ALL ComfyUI+NLS final.mp4 |
| 剩余ComfyUI角色图 | v3.6.1 | 25张全角色渲染 |
| 下载功能 | v3.6.1 | /api/download + /api/script/{ep}/export |
| 订单履约追踪 | v3.6.1 | fulfillment_events表 + tracking |
| ERP草稿箱推送 | v3.6.1 | push_to_erp_draft() |
| Dashboard JS语法修复 | v3.7.1 | 6类~274处 · node --check PASS |
| DM-1面板恢复 | v3.7.2 | 完整恢复(+5 commits) |
| 跨业务线路由 | v3.7.3 | DM-1只在短剧Tab |
| MS-0门禁报告 | v3.7.3 | 前端体检报告面板 |
| MS-2.3商品图工作台 | v3.7.3 | 筛选/批处理/Toast |

### 🔲 仍开放 GAP（完整列表见第八部分）
| GAP | 状态 |
|-----|------|
| AI视频支付 | ⏸️ Kling ¥15/EP, 微信支付 |
| 达人联盟 | ⏸️ 紫鸟手动 |
| 发布上线 | ⏸️ MIAOSHOW_PUBLISH_ENABLED=false |
| 环境音效 | 🔲 freesound API / ElevenLabs SFX |
| 5国字幕 | 🔲 localization pipeline待集成 |
| 竞品真实API | 🔲 当前3/5维度为mock |

---

## 第七部分：🚫 五条红线（同 v3.5 保持不变）

| # | 红线 | 违反处理 |
|---|------|---------|
| 1 | 禁止自动发布 | Agent 停止执行 |
| 2 | 禁止跳过决策节点 | 任务状态 failed |
| 3 | 禁止硬编码密钥 | code review 不通过 |
| 4 | 禁止跨业务线调度 | 路由拦截报错 |
| 5 | 禁止覆盖已有数据 | 追加时间戳后缀 |

---

## 第八部分：下一步计划（合并版 — 替代原 GAP 清单+第八部分重复内容）

### 即将推进（P0）
| 任务 | 状态 | 说明 |
|------|------|------|
| 剧本脚本编写（108将短剧EP11-EP14） | ⏳ | shuihuzhuan.yaml已预留，_build_storyboard待补模板 |
| 批量定妆图质量审核 | ⏳ | 436张已生成，需确认是否达到98版电视剧质感 |
| gallery.html UI 打磨 | ⏳ | 筛选/排序/分集展开 |
| **MS-0 后端门禁API** `/api/gate/MS-0/run` | **🆕 前端就绪，后端待实现** | 前端 `triggerReReviewMS0()` 已写，需后端端点 |

### 待解决（P1）
| 任务 | 状态 | 说明 |
|------|------|------|
| ~~Dashboard空白修复~~ | ✅ 已修复 | 语法错误(61b34c8) + 孤儿代码泄漏(6d8d618) + 跨业务线路由修复 |
| ~~DM-1跨业务线路由修复~~ | ✅ 已修复 | renderDetail() TK分支清理 |
| Pollo AI / Kling API 集成视频预览 | ⏳ | S2-2预览动态按钮已放mock，需API Key |

### 阻塞项（⛔ BLOCKED）
| 任务 | 阻因 |
|------|------|
| 用电视剧原声替换NLS参考音频 | 素材不足：仅8秒测试片段，需完整98版电视剧集 |
| 竞品真实API (Kalodata/Shulex) | 当前3/5维度为mock |

### 延后（P2/P3）
| 任务 | 状态 |
|------|------|
| 环境音效扩充 (freesound/ElevenLabs) | 🔲 SFX engine 11类型已有，待扩充 |
| 5国字幕集成到短剧 | 🔲 localization pipeline已有·待集成 |
| 妙手发布上线 | ⏸️ MIAOSHOW_PUBLISH_ENABLED=false |
| Kling AI视频生成(真人视频) | ⏸️ 微信¥15/EP |
| 达人联盟 | ⏸️ 紫鸟手动 |
| P0: DM-0 剧本原稿对照 | 📋 审计发现·线下讨论 |
| P0: DM-6/7 视频播放按钮 | 📋 审计发现·线下讨论 |
| P0: 导演总览视图(单屏看清全局) | 📋 审计发现·线下讨论 |
| P1: DM-3 charMap动态加载(去硬编码6角色) | 📋 审计发现·线下讨论 |
| P1: DM-4 渲染队列管理 | 📋 审计发现·线下讨论 |
| P1: mock/real 数据标识统一 | 📋 审计发现·线下讨论 |

### v3.7.20 关键数据

| 指标 | 数值 |
|------|------|
| Dashboard 行数 | **10,634** (较 v3.7.8 +3,241 行) |
| API 端点总数 | **45+** (新增3个: DELETE渲染/REGENERATE渲染/TTS代理) |
| JS 语法 | ✅ node --check 零错误 |
| Python 语法 | ✅ py_compile 通过 |
| 角色数 | 109 (visual_bible.json) |
| 渲染图 | 436+ 张 |
| 审计发现 | 14 项 (P0×4 / P1×4 / P2×6) |
| Git commits (5月2日) | 25+ commits (Sprint 1-4 + DM-0面板完善 + 技术检查可视化 + 按钮改造) |
| task_board.html | **7,393行 / 386KB** |
| API端点总数 | 42+ (Flask :5001 34+ · FastAPI :5004 8+) · MS-2.3处理/合规/检查端点 · MS-5日报推送/预览/历史端点 · POST /api/review/trigger/{episode} |
| 角色定妆照 | 109角色×4张=436张 (476MB) |
| EP01-10 final.mp4 | 全部1.8-2.1MB (Pillow+ComfyUI双模式) |
| 运行服务 | 5001 Flask / 5004 FastAPI / 9880 GPT-SoVITS / 8188 ComfyUI |
| — | ✅ 109 角色头像渲染 | portrait_0.png 全量 200 |
| — | ✅ 108 音色克隆管线 | NLS ref + GPT-SoVITS s2Gv3.pth |
| — | ✅ 视频提示词三方案 | visual_bible.json + 仪表盘渲染 |
| — | ✅ 109 AI人物小传 | personality/appearance/background/voice |
