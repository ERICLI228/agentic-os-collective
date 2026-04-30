# 🎬 Agentic OS v3.6.2 产品需求文档 (PRD) — P0清零 + 动态管线版

> **文档类型**: 产品需求文档 (Product Requirements Document)  
> **版本**: v3.6.2 P0清零 + 动态管线版  
> **日期**: 2026 年 4 月 30 日 (v3.6.2)  
> **产品名称**: Agentic OS v3.5 双业务线自动化系统  
> **产品愿景**: 一个指令启动 → 全程自动执行 → **关键节点等你决策** → 输出可发布成果  
> **目标用户**: TK 跨境电商运营人员、AI短剧创作者、技术开发团队  
> **文档状态**: ✅ 已定稿（v3.6.2: P0清零 + 动态管线 + MS-0/1/3/5 stub全补实 + generate_script动态化）
> **前置版本**: v3.5（2026-04-29 感知控制优先版）→ v3.5.4（2026-04-29 交互驾驶舱 v2）

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
| **v3.6.2** | **2026-04-30** | **阿牛 + OpenClaw** | **P0清零: DM-1角色卡杨志→李逵/晁盖→吴用·EPISODE_MAP ep05李逵/ep06吴用·generate_script()动态化(script_manager加载)·MS-0/1/3/5 stub补实(门禁/采集/发布/日报)·SFX 11类型6集全配·29stale引用清除·get_dummy_ms移除** |

---

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
| **DM-0** | **剧本审核** | 自动 | **🏗️ 进行中** | **完整剧本查看/编辑/导出·5段式分镜故事板·LLM审核命令路径修正·shuihuzhuan.yaml实时同步** |
| **DM-1** | **角色设计** | 自动 | **🏗️ 进行中** | **ComfyUI渲染器已生成鲁智深3镜+晁盖3镜·6角色设计可编辑·NLS音色/配色选择·POST /api/character/{name}** |
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
| `/api/render/{char_id}/{filename}` | GET | ComfyUI渲染图文件服务 |

**支持角色**: 武松 / 鲁智深 / 林冲 / 宋江 / 杨志 / 晁盖
**角色属性**: traits / height / face / weapon / voice / color

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
| `shared/task_wizard.py` | 740 | — | Flask主服务·30端点·CORS·sys/ep_num/download修复 |
| `shared/detail_engine.py` | 797 | **UPDATED** | 14里程碑·DM-1角色卡全修复(李逵/吴用)·MS-0/1/3/5 stub补实·0处stale引用 |
| `shared/script_manager.py` | 454 | — | 剧本查看/编辑/导出·6集故事板·YAML同步·_export_srt·EP05李逵/EP06吴用 |
| `shared/comfyui_renderer.py` | 259 | **UPDATED** | ComfyUI SDXL 渲染器·--help likui/wuyong修正 |
| `shared/core/image_processor.py` | 240 | — | rembg·resize·compliance·push_to_erp_draft |
| `shared/core/tk_pipeline_db.py` | 731 | — | orders扩展+fulfillment_events·4条测试数据 |
| `shared/analytics_engine.py` | 700 | **UPDATED** | EPISODE_MAP ep05李逵/ep06吴用·DRAMA_EMOTIONAL_ARCS更新 |
| `shared/core/sfx_engine.py` | 497 | **UPDATED** | 11音效类型(含喧哗/拳击/木材)·6集全配·sfx_manifest.json |
| `shared/localization_reviewer.py` | 268 | — | 5国LLM翻译·禁忌词过滤·可读性评分 |
| `shared/decision_engine.py` | 345 | — | 3-Agent审核→DecisionBrief·风险矩阵 |
| `shared/core/adversarial_review.py` | 886 | — | 3-Agent对抗审核框架·6场景 |
| `dashboard/task_board.html` | 790 | — | v3.6 smart routing·DM-0/DM-1/MS-2.3专用渲染·图片画廊·inline编辑·下载 |
| `dashboard/info_board.html` | 300+ | — | 全球信息摘要·科学清新风格·筛选Tabs |
| `drama/openclaw/core/pipeline_ep01.py` | 597 | **UPDATED** | generate_script()动态化(script_manager加载)·6集全适配·ACT_TYPE_MAP |
| `stories/shuihuzhuan.yaml` | — | — | YAML idx 7/8/9/10 对齐 EPISODE_MAP |
| `reports/PRD-v3.6.md` | 418+ | **UPDATED** | v3.6.2 版本·行数同步·完成度矩阵 |
| `~/.agentic-os/pipeline.db` | — | — | orders(4) + fulfillment_events(3) |
| `~/.agentic-os/character_designs/renders/` | — | — | 6角色(武松/鲁智深/林冲/宋江/李逵/吴用)·25 PNG |
| `~/.agentic-os/episode_*/final.mp4` | — | — | EP01-06 全量输出 (1.8-2.4MB/23s) |
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

## 第八部分：下一步计划

| 优先级 | 任务 | 预计耗时 |
|--------|------|---------|
| **P0** | Dashboard HTML照片展示（剧本/角色/产品图） | 2h |
| **P0** | Dashboard HTML编辑表单（剧本/角色修改UI） | 2h |
| **P1** | EP06首发(智取生辰纲·非暴力) + 5国字幕 | 1h |
| **P1** | 生成剩余4角色12镜 ComfyUI渲染图 | 15min×12=3h |
| **P1** | Kling AI视频支付→1集测试 | 待支付 |
| **P2** | 环境音效管线（freesound API） | 1h |
| **P2** | 竞品数据API接入（Kalodata/Shulex） | 待API获取 |
| **P3** | MIAOSHOW_PUBLISH_ENABLED→发布3品 | 1h |
| **P3** | 达人联盟开通（紫鸟） | 30min |
