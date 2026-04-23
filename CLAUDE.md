# agentic-os-collective 项目架构说明

> 版本：2026-04-23
> 仓库：~/agentic-os-collective/
> 状态：生产环境

## 🎯 项目概述

本项目包含两个核心业务线：
1. **AI数字短剧自动化系统** (drama/)
2. **TK东南亚运营自动化系统** (tk/)

共享基础设施位于 `shared/` 目录。

---

## 📁 目录结构

```
agentic-os-collective/
├── drama/                    # AI短剧自动化
│   ├── openclaw/
│   │   ├── core/             # 核心引擎模块
│   │   │   ├── download_server.py        # 下载服务
│   │   │   ├── decision_listener.py      # 决策监听器
│   │   │   ├── token_governor_v1.py      # Token治理v1
│   │   │   ├── token_governor_v2.py      # Token治理v2
│   │   │   ├── safe_router.py            # 安全路由
│   │   │   ├── progress_logger.py        # 进度日志
│   │   │   ├── dashboard_api_v2.py       # Dashboard API
│   │   │   └── media_server.py           # 媒体服务
│   │   └── skills/
│   │       └── water-margin-drama/       # 水浒传短剧Skill
│   │           ├── water_margin_drama.py # 主脚本
│   │           ├── script_selector.py    # 剧本筛选
│   │           ├── role_designer.py      # 角色设计
│   │           ├── auto_publisher.py     # 自动发布
│   │           └── SKILL.md              # Skill说明
│
├── tk/                       # TK运营自动化
│   ├── openclaw/
│   │   ├── core/             # 核心引擎（与drama共享结构）
│   │   └ skills/
│   │       ├── claw-operator/            # TK运营Operator
│   │       └── feishu-tk-notifier/       # 飞书通知
│
├── shared/                   # 共享基础设施
│   ├── mcp_task_server.py    # MCP任务服务器
│   ├── execution_logger.py   # 执行日志器
│   ├── task_wizard.py        # 任务向导
│   ├── data/
│   │   └ init_db.py          # 数据库初始化
│   ├── knowledge/
│   │   └ best_practices.yaml # 最佳实践知识库
│   └── templates/
│       ├── tk_pipeline.yaml   # TK流水线模板
│       ├── drama_pipeline.yaml # 短剧流水线模板
│
├── dashboard/                # Dashboard UI
├── api/                      # API服务
├── gateway/                  # Gateway配置
├── hooks/                    # Git Hooks
├── tests/                    # 测试套件
└ reports/                   # 审查报告输出

```

---

## 🧩 核心模块说明

### 1. drama/openclaw/core/ (AI短剧核心引擎)

| 模块 | 功能 | 关键特性 |
|------|------|---------|
| `download_server.py` | 视频下载服务 | 支持多平台、断点续传 |
| `decision_listener.py` | 决策监听器 | 异步事件驱动 |
| `token_governor_v1.py` | Token治理v1 | 简单限额控制 |
| `token_governor_v2.py` | Token治理v2 | 智能预算分配 |
| `safe_router.py` | 安全路由 | 权限验证、流量控制 |
| `progress_logger.py` | 进度日志 | 实时监控、状态追踪 |
| `dashboard_api_v2.py` | Dashboard API | RESTful接口、数据聚合 |
| `media_server.py` | 媒体服务 | 视频处理、格式转换 |

### 2. drama/openclaw/skills/water-margin-drama/ (水浒传短剧Skill)

| 模块 | 功能 | 输入/输出 |
|------|------|----------|
| `water_margin_drama.py` | 主脚本 | 剧本→视频 |
| `script_selector.py` | 剧本筛选 | 原文→精选片段 |
| `role_designer.py` | 角色设计 | 角色→配音/形象 |
| `controversy_rewriter.py` | 争议改写 | 敏感剧情→合规版本 |
| `auto_publisher.py` | 自动发布 | 视频→平台上传 |
| `drama_audio.py` | 配音合成 | 文本→武松语音 |

### 3. tk/openclaw/core/ (TK运营核心引擎)

与 drama 共享相同的架构模板，但业务逻辑不同。

| 模块 | 功能 | TK特定特性 |
|------|------|-----------|
| `download_server.py` | 视频下载 | TK平台适配 |
| `decision_listener.py` | 决策监听 | 运营策略决策 |
| `token_governor_v2.py` | Token治理 | 运营预算控制 |

### 4. shared/ (共享基础设施)

| 模块 | 功能 | 服务范围 |
|------|------|---------|
| `mcp_task_server.py` | MCP任务服务器 | drama + tk |
| `execution_logger.py` | 执行日志器 | 全项目 |
| `task_wizard.py` | 任务向导 | 任务创建流程 |
| `data/init_db.py` | 数据库初始化 | 数据库Schema |

---

## 🔑 关键文件路径

### 配置文件

| 文件 | 路径 | 用途 |
|------|------|------|
| TK流水线配置 | `shared/templates/tk_pipeline.yaml` | TK运营流程定义 |
| 短剧流水线配置 | `shared/templates/drama_pipeline.yaml` | 短剧生成流程定义 |
| 最佳实践知识库 | `shared/knowledge/best_practices.yaml` | 通用最佳实践 |
| TK Operator配置 | `tk/openclaw/skills/claw-operator/config.json` | TK运营参数 |

### 数据文件

| 文件 | 路径 | 用途 |
|------|------|------|
| 水浒传剧本库 | `drama/openclaw/skills/water-margin-drama/episode_list.json` | 剧本索引 |
| 角色库 | `drama/openclaw/skills/water-margin-drama/role_library.json` | 角色+配音配置 |

### 文档文件

| 文件 | 路径 | 用途 |
|------|------|------|
| 水浒传Skill说明 | `drama/openclaw/skills/water-margin-drama/SKILL.md` | Skill使用指南 |
| TK Operator Skill | `tk/openclaw/skills/claw-operator/SKILL.md` | TK运营指南 |

---

## 📋 命名约定

### 文件命名

| 类型 | 约定 | 示例 |
|------|------|------|
| Python模块 | `snake_case.py` | `download_server.py` |
| 配置文件 | `snake_case.yaml/json` | `tk_pipeline.yaml` |
| Skill文档 | `SKILL.md` | 固定名称 |
| 状态文件 | `*_state.json` | `confirmation_state.json` |

### 目录命名

| 类型 | 约定 | 示例 |
|------|------|------|
| Skill目录 | `skill-name/` | `water-margin-drama/` |
| 核心模块 | `core/` | 固定名称 |
| 共享目录 | `shared/` | 固定名称 |

---

## 🔗 依赖关系

### 外部依赖

| 依赖 | 用途 | 版本要求 |
|------|------|---------|
| OpenClaw | 核心框架 | 最新版 |
| GPT-SoVITS | 配音合成 | V3或V2 |
| Replicate | 动态视频生成 | 需余额 |
| 飞书 API | 通知推送 | Webhook配置 |

### 内部依赖

| 模块 | 依赖模块 | 依赖类型 |
|------|---------|---------|
| `drama/core/*` | `shared/mcp_task_server.py` | 强依赖 |
| `tk/core/*` | `shared/mcp_task_server.py` | 强依赖 |
| `water_margin_drama.py` | `drama/core/*` | 强依赖 |
| `claw-operator.py` | `tk/core/*` | 强依赖 |

---

## ⚠️ 已知问题

1. **架构重复**: `drama/core/` 与 `tk/core/` 结构相似，可能存在代码重复
2. **CLAUDE.md缺失**: 项目根目录缺少架构说明文档
3. **SOP文档缺失**: 未找到 TK-OPERATION-SOP.md 文件
4. **配置分散**: 配置文件分散在多个目录，缺少统一管理

---

## 📊 项目统计

| 类型 | 数量 |
|------|------|
| 总文件数 | 2831 |
| Python文件 | 55 |
| 配置文件 | 613 |
| 文档文件 | 118 |
| Skill数 | 2 (drama) + 2 (tk) |

---

*更新于 2026-04-23 00:50 PDT*
