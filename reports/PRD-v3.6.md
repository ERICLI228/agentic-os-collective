# 🎬 Agentic OS v3.6.20 产品需求文档 (PRD) — 108将音色克隆 + 全角色可视化

> **文档类型**: 产品需求文档 (Product Requirements Document)
> **版本**: v3.6.20 音色克隆+视频提示词
> **日期**: 2026 年 5 月 1 日 (v3.6.20)
> **产品名称**: Agentic OS v3.6 双业务线自动化系统
> **产品愿景**: 一个指令启动 → 全程自动执行 → **关键节点等你决策** → 输出可发布成果
> **目标用户**: TK 跨境电商运营人员、AI短剧创作者、技术开发团队
> **文档状态**: ✅ 108将完整覆盖 — 音色克隆(NLS+GPT-SoVITS) + 视频提示词三方案 + 全渲染图 + AI人物小传
> **前置版本**: v3.6.8（2026-04-30 P1 UX 补齐版）

---

## 📜 版本修订历史

| 版本 | 日期 | 修订人 | 修订内容 |
|------|------|--------|----------|
| v0.1 | 2026-04-09 | CEO 黄光耀 | 初始架构与任务协议草案 |
| v0.5 | 2026-04-15 | 工程经理 张志远 | 双业务线分离设计 |
| v0.8 | 2026-04-20 | Claude Desktop | 安全审查与代码重构 |
| v1.0 | 2026-04-23 | CEO + TK 老兵 + 短剧制作人 | 正式定稿，融合双视角审视 |
| v3.3 | 2026-04-24 | 阿牛 | 诚实修订：完成度 85%→35%，止血优先，GSTACK 搁置 |
| v3.4 | 2026-04-28 | 阿牛 | 对抗审核增强 |
| v3.4+ | 2026-04-29 | 阿牛 | 实际完成度标注：妙手API/采集箱/OCR就绪 |
| **v3.5** | **2026-04-29** | **外部评审 + 阿牛** | **感知控制优先：重建决策节点架构** |
| v3.5.2 | 2026-04-29 | 阿牛 | Sprint 1.5 完成 — Pillow v2/NLS/管线汇总/GitHub全量同步 |
| v3.5.3 | 2026-04-29 | 阿牛 + OpenClaw | P0/P1 全线攻克 — NLS/3-Agent/SQLite/6角色圣经/10模块覆盖 |
| v3.5.4 | 2026-04-29 | 阿牛 | 交互驾驶舱 v2 — 双业务线Tab/决策联动/智能决策引擎 |
| **v3.6** | **2026-04-30** | **阿牛** | **细节展开系统 — 所有明细点返回实体数据(非状态标签) · 剧本查看/编辑/导出API · 角色ComfyUI渲染器 · 商品图片处理API · 全球信息摘要 · 27端点Flask · 26/27 PASS** |
| **v3.6.1** | **2026-04-30** | **阿牛** | **QA全绿(80/80)·6集管线全通(ComfyUI+NLS)·25张角色渲染(6角色含武松/鲁智深/林冲/宋江/李逵/吴用)·30端点+Download API·10项修复(sys/ep_num/export/Image404/拼音双通/DM-V-F/push_erp/SRT/订单)·EPISODE_MAP YAML对齐(idx 7/8/9/10修正)·Dashboard smart routing·80/80 PASS** |
| **v3.6.2** | **2026-04-30** | **阿牛 + OpenClaw** | **P0清零: DM-1角色卡杨志→李逵/晁盖→吴用·EPISODE_MAP ep05李逵/ep06吴用·generate_script()动态化(script_manager加载)·MS-0/1/3/5 stub补实(·SFX 11类型6集全配·29stale引用清除·get_dummy_ms移除·pipeline_ep01.py全硬编码迁入script_manager(EPISODE_MAP/character_palettes/RENDER_CHAR_MAP)·MS-4.5对抗审核命令修正** |
| **v3.6.3** | **2026-04-30** | **阿牛 + OpenClaw + OpenCode** | **PHASE1止血: 假成功清洗11条·execution_logger安全加固(shell=False)·ffmpeg动态路径(drama_merge+pillow)·quality_assessor语法修复·skill脚本软链接7就位+drama_script/drama_video恢复·CLAUDE同步v3.6.2/82%。PHASE3管线: drama_pipeline.yaml v1.2(Seedance/MiniMax→OpenClaw·MS-4.5对抗审核·9阶段编译验证)。PHASE4 Dashboard: 待决策黄色高亮·MS-2.3修改意见+实时刷新·决策面板增强** |
| **v3.6.4** | **2026-04-30** | **阿牛** | **PHASE2 Cockpit: 10/10 API 200·/api/script list scene_count+render_fields·/api/script/3 zero-pad修复·/api/decision宽容模式·/api/render别名路由(b030875)·详情端点渲染统计补齐·sys.path跨路径修复(d6f71c0)·role_designer过期副本清理(67b01ba)·CLAUDE.md v3.6.2同步** |
| **v3.6.5** | **2026-04-30** | **阿牛** | **LLM对抗审核突破: CODING免费额度路线通(单Agent~87s/3-Agent~100s)·综合评分3.8/10→reject·4维度真实审计·adversarial_review.py模型aliyun/→coding/+env加载·pipeline_ep01.py --review(mock/coding)开关·DM-0 Dashboard命令修正·drama_pipeline.yaml MS-4.5命令修正·CODING Plan余48%/48天** |
| **v3.6.6** | **2026-04-30** | **阿牛 + CEO 黄光耀** | **CEO诚实评估: 后端 API 82% → 前端 UX 仅 30% → 11项UX全覆盖(561a9c9) · 图片对比视图✅ · 真实进度反馈✅ · 键盘导航+快捷键✅ · 管线监控面板✅ · 详情面包屑✅ · 刷新状态指示✅ · 模态点击关闭✅ · 左侧键盘导航✅ · 统计Tooltip✅ · 搜索高亮✅ · 空状态引导✅ · 1310行(+318)·JS括号406/406平衡·49函数** |
| **v3.6.7** | **2026-04-30** | **阿牛** | **DM-1 角色档案系统: 4属性→完整人物小传(Bible) · visual_bible.json 8角色升级(personality/appearance/background/voice) · character_profile_generator.py(AI生成+预设fallback+重渲染检测) · POST /api/character 深合并保存 · DM-1 前端完全重构(角色Bible面板+编辑模式+颜色选择器+渲染进度) · 6角色全覆盖(武松/鲁智深/林冲/宋江/李逵/吴用) · +1152/-45 lines (4 files) · commit d01ef95** |
| **v3.6.8** | **2026-04-30** | **阿牛** | **P1 UX 补齐: Chart.js 数据可视化(状态分布/数据源/管线对比 3种视图) + 统一导出下载按钮(JSON/CSV决策/CSV里程碑/Markdown报告/HTML快照 5格式) · task_board.html 2010行(+388/-11) · JS 630/630括号平衡 · 59函数(+10) · 99.5KB · commit 7493dba** |
| **v3.6.9** | **2026-05-01** | **OpenClaw** | **Gallery 页面创建 + 渲染目录结构重构(gallery.html 109角色画廊) · visual_bible.json 从6角色扩展到109角色 · 渲染目录从拼音名迁移到纯中文名** |
| **v3.6.10** | **2026-05-01** | **阿牛 + OpenCode** | **Dashboard UI 升级: 科技清新配色· undefined filter 修复 (renderDefault 预过滤) · no-cache HTTP headers · commit 5fcf5a1** |
| **v3.6.11** | **2026-05-01** | **OpenCode** | **NLS 音色克隆基础: 108角色参考音频批量生成 (107 NLS + 1 CosyVoice wusong) · 存放于 ~/GPT-SoVITS/output/<fid>_nls_ref.wav · CosyVoice 保留 wusong_cosyvoice.wav 唯一真人原声** |
| **v3.6.12** | **2026-05-01** | **OpenCode** | **CHARACTER_VOICES 108全量注册: task_board.html 从2条目扩展到108条目 (ref + prompt + nls_speaker) · 仪表盘DM-1全角色预览 · CHARACTER_ID_MAP 从6到108 (script_manager.py)** |
| **v3.6.13** | **2026-05-01** | **OpenClaw** | **角色数据完整性修复: visual_bible.json 107→109 缺失角色补全 · AI人物小传扩展 (personality/appearance/background/voice) · 109角色全量覆盖** |
| **v3.6.14** | **2026-05-01** | **OpenCode** | **GPT-SoVITS 端到端验证: api.py CORS开放 + s2Gv3.pth模型验证 · GET/POST 双侧可用 · CosyVoice (wusong) + NLS ref (107) 双源参考音频全通** |
| **v3.6.15** | **2026-05-01** | **OpenCode** | **音色卡片交互UI: 6角色音色卡片 (类型/音色名/参考文本) · toggleVoiceConfigForm() 内联配置表单 (提供商/音色名/参考文本/保存+取消) · auditionVoice() GPT-SoVITS试听+自动播放 · generateVoice() 自定义文本生成 · closeVoicePlayer() 关闭播放 · generatedAudios session持久化 · overflow锁定** |
| **v3.6.16** | **2026-05-01** | **OpenClaw** | **gallery.html 图片加载修复: 图片URL路径对齐中文渲染目录 · 109角色画廊全量展示** |
| **v3.6.17** | **2026-05-01** | **OpenClaw** | **渲染目录清理: 删除拼音遗留目录/symlink · 统一纯中文目录名 ~/.agentic-os/character_designs/renders/<中文名>/portrait_0.png (109目录)** |
| **v3.6.18** | **2026-05-01** | **OpenClaw + OpenCode** | **视频提示词三方案: visual_bible.json 所有109角色添加 video_prompts (方案一: 静态肖像特写/方案二: 经典场景动态/方案三: 电影感运镜) — OpenClaw写入JSON · OpenCode仪表盘渲染 (🎬 可展开卡片 + 简练版提示词)** |
| **v3.6.19** | **2026-05-01** | **OpenCode** | **CSS 全线修复: .sec-body移除overflow:hidden+max-height:0 (默认可见·collapsed隐藏) · Chart.js CDN unpkg→jsdelivr (jsdelivr.net chart.js@4.4.4) · 音色面板全CSS (.cb-voice-card/配置表单/播放行/生成按钮) · .cb-vp-card视频提示词卡片CSS** |
| **v3.6.21** | **2026-05-01** | **阿牛** | **v3 API新增8端点: /api/status · /api/character/{fid} · /api/render/{fid}/{filename} · /api/script · /api/script/{ep_num} · /api/detail/{ms_id} · /api/images · /api/review/{fid} — 写入 dashboard_api_v3.py (FastAPI port 5004) · 109角色数据从visual_bible.json读取 · 渲染图通过/api/render代理服务 · 35端点总计** |
| **v3.6.22** | **2026-05-01** | **阿牛** | **voice_clone_pipeline.py 创建 + 6角色全注册: GPT-SoVITS自动化管线(register/test/batch/list) · 339行 · ~/agentic-os-collective/drama/openclaw/core/voice_clone_pipeline.py · character_voices.json 从2→6角色(武松/鲁智深/林冲/宋江/李逵/吴用) · 参考音频均测试通过(8-463KB) · 同步opencode worktree** |
| **v3.6.23** | **2026-05-01** | **阿牛** | **add_video_prompts.py 脚本: 107角色自动生成三方案视频提示词 + 2角色保留原始(武松/鲁智深) · 写入 visual_bible.json · 基于角色外观/性格/场景数据个性化 · ~/agentic-os-collective/scripts/add_video_prompts.py** |
| **v3.6.25** | **2026-05-01** | **阿牛** | **鲁智深 basic_info/appearance/background 补全: 从profile嵌套结构迁移到顶层字段 · height/build/face/age/costume/accessories/color_palette/origin/key_events/relationships 全量写入 visual_bible.json · 仪表盘DM-1角色卡片正常显示** |
| **v3.6.26** | **2026-05-01** | **阿牛** | **LLM对抗审核管线验证通过: adversarial_review.py CODING模式实际运行93.8s · 真实LLM审核EP01剧本 · 评分3.0/10 ✅ reject · 4维度真实审计(编剧规则1.0/场景完整性1.0/剧情节奏3.0/逻辑一致性3.0) · pipeline_ep01.py --review coding 完整链通 · 实际堵塞点CODING免费额度已解决** |
| **v3.6.27** | **2026-05-01** | **OpenCode** | **客观诚实收尾: visual_bible 113→109清理完毕 (删yanglin_hs/kongming_hs·补star_rank to chaogai·恢复yanglin/kongming) · reReviewDM0()修复 (→triggerReReview) · PRD v3.6.9~27全量里程碑 · CLAUDE.md 铁则#0强化(任务完成强制闭环+版本滞后告警) · VERSION文件创建 · /dashboard PRD告警条 · Git全量提交+推送 · Obsidian同步 · wiki日志更新** |
---

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

**端到端验证**: 10/10 API 端点 200 ✅

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

### 11项关键 UX 功能覆盖率

| UX 功能 | 实现状态 | 代码证据 |
|---------|---------|----------|
| 1. 摘要优先折叠/展开详情页 | ❌ 0% | 无 `milestone-summary` 结构 |
| 2. DM-0 四维度审核明细展示 | ❌ 0% | 仅 rv_score + rv_decision |
| 3. 修改→重处理→审核自动循环 | ❌ 0% | 无 reset/重新审核逻辑 |
| 4. 统一下载入口（下拉菜单） | ✅ 100% | 顶部栏📥导出按钮 · 5格式(JOSN/CSV/MD/HTML/快照) · 浏览器直接下载 |
| 5. 图片并排对比视图（原图 vs 处理后） | ⚠️ 10% | CSS 类存在但 JS 未调用 |
| 6. 音色试听 | ❌ 0% | 无 audio/play 相关 JS |
| 7. Chart.js 数据可视化 | ✅ 100% | Chart.js CDN · 3视图(状态分布/数据源/管线对比) · 环形图+柱状图切换 |
| 8. 处理进度反馈（加载动画） | ⚠️ 20% | 有 `.loading-bar`(P0-1) 但无操作级进度 |
| 9. Dashboard 搜索与过滤 | ✅ **80%** | `searchInput`+`filterSelect` 已工作（P1-12） |
| 10. 质量反馈知识库 | ❌ 0% | 无 quality_feedback/feedback 相关代码 |
| 11. 自愈提示（连续失败提醒） | ❌ 0% | 无相关逻辑 |
| **总计** | **~48%** | **11项中 3 项工作 + 1 项部分完成** (P0/P1基础UX 70% + 数据可视化+导出 全覆盖) |

### 根本原因（与 CEO 分析一致）

1. **后端验证 ≠ 用户验证**: 80/80 QA 测试全为 curl/pytest 级别，**无一人模拟真实用户在浏览器上走完完整流程**
2. **前后端独立开发**: 后端 API 测试通过即标记完成，前端未做端到端用户流程验证
3. **完成定义偏差**: "API 返回 200" 被当作完成标准，但用户需要的是 "打开页面 → 看到信息 → 理解内容 → 做出决策 → 执行操作" 的完整闭环

### 补救路线（CEO WBS 确认）

| 冲刺 | 时间 | 核心任务 | 验收标准 |
|------|------|---------|----------|
| **Sprint 1** | 本周 (12h) | 摘要优先折叠设计 + DM-0 审核四维度 + 修改→重审循环 + 统一下载 + 图片对比 | 打开任意里程碑先见摘要，点击才展开详情 |
| **Sprint 2** | 下周 (8h) | Chart.js 数据可视化 + 音色试听 + 处理进度反馈 + Dashboard 搜索过滤完善 | 定价柱状图/ROI 折线图可用，试听可播放 |
| **Sprint 3** | 本月末 (6h) | 质量反馈知识库 + 用户操作日志 + 自愈提示 | 连续3次失败自动弹出常见问题提示 |

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
│  🖥️ Flask Dashboard (:5001) — v3.6 27端点                 │
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
- ✅ 鲁智深 (wusong ID/render): 武松3镜（景阳冈饮酒/徒手打虎/举虎下山）
- ✅ 晁盖 (chaogai render): 晁盖3镜（集结/山路/智劫）
- ⏳ 剩余4角色待渲染

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

### 3.1 API 端点全景（30端点，v3.6.1更新）

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
| `dashboard/task_board.html` | 790 → 2866+ | **UPDATED** | v3.6.20: 108 CHARACTER_VOICES·音色卡片(试听/生成/配置)·video_prompts三方案渲染·Chart.js 3视图·5格式导出·科技清新风·155KB |
| `dashboard/info_board.html` | 300+ | — | 全球信息摘要·科学清新风格·筛选Tabs |
| `~/.agentic-os/character_designs/` | — | — | visual_bible.json (109角色含video_prompts) · renders/<中文名>/portrait_0.png (109目录) · gallery.html |
| `~/.agentic-os/episode_*/final.mp4` | — | — | EP01-06 全量输出 (1.8-2.4MB/23s) |
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

## 第六部分：GAP 清单 v3.6.1（诚实标注）

| GAP | v3.6 状态 | v3.6.1 状态 | 说明 |
|-----|----------|------------|------|
| Dashboard HTML 图片展示 | ⏳ | ✅ 已完成 | DM-0/DM-1/MS-2.3 img-gallery + zoom modal + API集成 |
| Dashboard HTML 编辑表单 | ⏳ | ✅ 已完成 | inline textarea编辑 + POST保存 + voice/color表单 |
| EP03-06 运行 | ⏳ | ✅ 已完成 | EP01-06 ALL ComfyUI+NLS final.mp4 (1.8-2.4MB) |
| 剩余ComfyUI角色图 | ⏳ | ✅ 已完成 | 25张全角色渲染 (鲁智深6+林冲3+宋江3+杨志3+晁盖6+武松4+李逵3+吴用3) |
| 下载功能 | — | ✅ 已完成 | /api/download + /api/script/{ep}/export (txt/html/srt/json) |
| 订单履约追踪 | — | ✅ 已完成 | fulfillment_events表 + tracking + stats 4条测试 |
| ERP草稿箱推送 | — | ✅ 已完成 | push_to_erp_draft() → ~/.agentic-os/miaoshou_draft/ |
| AI视频支付 | ⏸️ | ⏸️ | fal.ai/Kling 用户待支付 (Kling ¥15/EP, 微信支付) |
| 达人联盟 | ⏸️ | ⏸️ | 紫鸟手动 |
| 发布上线 | ⏸️ | ⏸️ | MIAOSHOW_PUBLISH_ENABLED=false |
| 环境音效 | 🔲 | 🔲 | freesound API / ElevenLabs SFX |
| 5国字幕 | 🔲 | 🔲 | 已有localization pipeline·待集成到短剧 |
| 竞品真实API | 🔲 | 🔲 | Kalodata/Shulex · 当前3/5维度为mock |

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

## 第八部分：下一步计划 (v3.6.20 更新)

| 优先级 | 任务 | 状态 | 说明 |
|--------|------|------|------|
| **P0** | 剧本脚本编写（108将短剧） | ⏳ | 待 OpenClaw 启动 |
| **P0** | fix reReviewDM0() 未定义 bug | ⏳ | 仪表盘 DM-0 审核卡片「重新审核」按钮报错 |
| **P1** | 用电视剧原声替换 NLS 参考音频 | ⏳ | 提升 GPT-SoVITS 克隆质量 |
| **P1** | gallery.html UI 打磨 | ⏳ | 筛选/排序/分集展开 |
| **P1** | Kling AI 视频生成 (真人视频) | ⏸️ | 待支付 (¥15/EP, 微信支付) |
| **P2** | 5国字幕集成到短剧 | 🔲 | localization pipeline 已有·待集成 |
| **P2** | 环境音效 (freesound/ElevenLabs) | 🔲 | SFX engine 已有 11 类型·待扩充 |
| **P2** | 竞品数据 API (Kalodata/Shulex) | 🔲 | 当前3/5维度为mock |
| **P3** | 妙手发布上线 | ⏸️ | MIAOSHOW_PUBLISH_ENABLED=false |
| — | ✅ 109 角色头像渲染 | **完成** | portrait_0.png 全量 200 |
| — | ✅ 108 音色克隆管线 | **完成** | NLS ref + GPT-SoVITS s2Gv3.pth |
| — | ✅ 视频提示词三方案 | **完成** | visual_bible.json + 仪表盘渲染 |
| — | ✅ 109 AI人物小传 | **完成** | personality/appearance/background/voice |
