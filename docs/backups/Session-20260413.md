# 全量备份说明 - 2026-04-13 会话成果

## 📦 备份内容概览

| 类别 | 文件数 | 说明 |
|------|--------|------|
| **核心API** | 15 | dashboard_api_v2.py等核心服务 |
| **Dashboard页面** | 3 | index.html, tk-center.html, status.html |
| **TK编辑器页面** | 12 | editor.html, accounts.html等 |
| **Vue组件** | 5 | TaskList.vue, App.vue等前端组件 |
| **配置文件** | 4 | openclaw.json, package.json等 |
| **脚本文件** | 30 | 启动脚本、同步脚本、修复脚本 |
| **任务数据** | 5 | DRAMA/TK任务JSON |
| **知识库** | ~50 | Obsidian笔记、模板 |
| **产出文件** | 4 | 视频、剧本、角色图片 |

---

## 🏗️ 系统架构

### 端口分配

| 端口 | 服务 | 用途 |
|------|------|------|
| **5002** | 指挥中心 | 主控制面板 |
| **5001** | Dashboard API | REST API服务 |
| **5173** | Vue数据面板 | 任务详情展示 |
| **3000** | TK编辑器 | 东南亚运营工具 |
| **3008** | Clawith | 数字员工平台 |
| **18789** | Gateway | WebSocket网关 |

### 目录结构

```
~/.openclaw/
├── core/
│   ├── dashboard_api_v2.py    # 主API (Flask)
│   ├── safe_router.py         # 安全路由
│   ├── task_updater.py        # 任务更新器
│   ├── feishu_alert.py        # 飞书告警
│   └── token_governor_v1.py   # Token管理
│
├── dashboard/
│   ├── index.html             # 指挥中心主页
│   ├── tk-center.html         # TK运营中心
│   └── SYSTEM-ARCHITECTURE.md # 系统文档
│
├── workspace/
│   ├── tasks/active/*.json    # 活跃任务
│   ├── knowledge-base/        # 知识库同步
│   ├── MEMORY.md              # 长期记忆
│   └── OPERATIONS.md          # 运营指令
│
├── scripts/
│   ├── LAUNCH-SERVICES.sh     # 服务启动
│   ├── restart-dashboard-api.sh
│   ├── fix_milestones.py      # 里程碑数据注入
│   └── sync_tasks_to_obsidian.py
│
└── projects/
    ├── drama/config.yaml      # 短剧流水线配置
    ├── tk/config.yaml         # TK运营配置
    └── feishu_webhooks.yaml   # 飞书Webhook配置

~/tk-workflow-editor/public/
├── index.html                 # TK主页
├── editor.html                # 可视化编辑器
├── dashboard.html             # 监控仪表盘
├── accounts.html              # 账号管理
├── config-center.html         # 配置中心
├── permissions.html           # 权限管理
├── southeast-asia-3c-report.html  # 3C报告
├── weekly-report.html         # 周报
├── v3-workflow.html           # V3工作流
├── video-transcriber.html     # 视频转录
└── status.html                # 状态监控

~/agentic-os-collective/web/src/
├── App.vue                    # Vue主应用
├── main.js                    # Vue入口
├── components/
│   ├── TaskList.vue           # 任务列表+里程碑抽屉
│   ├── Dashboard.vue          # 数据面板
│   ├── KPIPanel.vue           # KPI统计
│   └── DecisionPanel.vue      # 决策面板
│
└── vite.config.js             # Vite配置

~/drama/
├── output/                    # 视频产出
├── scripts/                   # 剧本文件
└── characters/                # 角色设计

~/knowledge-base/              # Obsidian知识库
├── 03-资源/代码项目/
│   ├── TK编辑器/
│   ├── Drama制作/
│   └── OpenClaw核心/
├── 05-每日日志/2026-04/
└── templates/                 # 任务模板
```

---

## 🔄 业务流程图

### 短剧流水线 (Drama Pipeline)

```
用户创建任务
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-1 剧本筛选                                        │
│  ├─ AI搜索候选剧本 (3个)                              │
│  ├─ 显示匹配度 (92%/85%/78%)                         │
│  ├─ 记录选择原因                                      │
│  └─ 产出: script_c1.txt                              │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-2 争议改写                                        │
│  ├─ 检测争议点 (暴力描写/动物保护)                     │
│  ├─ AI生成解决方案                                    │
│  ├─ 改写剧本                                          │
│  └─ 产出: rewritten_script.txt                       │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-3 角色设计                                        │
│  ├─ 设计角色外貌/性格                                  │
│  ├─ 分配配音风格                                      │
│  └─ 产出: character_cards.png                        │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-4 GLM-4.7生成剧本                                 │
│  ├─ ⚠️ 决策点 (通过/修改/驳回)                        │
│  ├─ 用户审核                                          │
│  └─ 产出: final_script.txt                           │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-5 人工审核                                        │
│  ├─ 用户决策                                          │
│  └─ 记录审核意见                                      │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-6 Seedance视频生成                                │
│  ├─ AI生成视频                                        │
│  └─ 产出: wusong_ep01.mp4                            │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  MS-7 配音合成                                        │
│  ├─ 阿里云Sambert配音                                 │
│  ├─ 音视频合成                                        │
│  └─ 最终产出: wusong_ep01_final.mp4                  │
└─────────────────────────────────────────────────────┘
    ↓
任务完成 → 通知飞书群
```

### TK东南亚运营流程

```
┌─────────────────────────────────────────────────────┐
│  定时监控 (每2小时)                                   │
│  ├─ 16品类热门数据采集                                │
│  ├─ 爆款检测 (>300万播放)                             │
│  └─ 异常告警                                          │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  数据分析                                             │
│  ├─ 竞品分析                                          │
│  ├─ ROI计算                                           │
│  └─ 周报生成                                          │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│  运营工具                                             │
│  ├─ 可视化编辑器 (editor.html)                        │
│  ├─ V3工作流 (v3-workflow.html)                      │
│  ├─ 视频转录 (video-transcriber.html)                │
│  └─ 配置管理 (config-center.html)                    │
└─────────────────────────────────────────────────────┘
```

---

## 📡 API端点清单

### Dashboard API (5001)

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/dashboard` | GET | 获取全部数据 |
| `/api/tasks/<id>/milestone/<mid>` | GET | 里程碑详情 |
| `/api/decision/<tid>/<did>` | POST | 提交决策 |
| `/api/download` | GET | 文件下载 |
| `/api/templates` | GET | 任务模板 |
| `/api/health` | GET | 健康检查 |
| `/api/task/wizard/validate-title` | POST | 标题验证 |
| `/api/task/wizard/recommend` | POST | 模板推荐 |

### 数据结构 (里程碑)

```json
{
  "id": "MS-1",
  "name": "剧本筛选完成",
  "status": "completed",
  "decision_point": false,
  "execution_details": {
    "output_content": {
      "type": "script_selection",
      "data": {
        "candidates": [
          {"id": "c1", "title": "武松打虎", "score": 0.92}
        ],
        "selected": "c1",
        "selection_reason": "匹配度最高"
      }
    },
    "artifacts": [{"name": "script_c1.txt", "url": "..."}],
    "decision_history": [...]
  }
}
```

---

## 🎨 本次会话关键修改

### 1. 指挥中心里程碑伸缩抽屉

**文件**: `~/.openclaw/dashboard/index.html`

**关键代码**:
```javascript
async function toggleMilestoneDetail(el) {
  const mId = el.dataset.milestoneId;
  const tId = el.dataset.taskId;
  
  // 展开/收起
  if (el.classList.contains('expanded')) {
    el.classList.remove('expanded');
    return;
  }
  
  // 加载详情
  const r = await fetch(`${API_BASE}/api/tasks/${tId}/milestone/${mId}`);
  const d = await r.json();
  
  // 根据output_content.type显示不同内容
  if (oc.type === 'script_selection') { ... }
  if (oc.type === 'controversy_resolution') { ... }
  if (oc.type === 'character_design') { ... }
}
```

### 2. Vue数据面板看板/时间线视图

**文件**: `~/agentic-os-collective/web/src/components/TaskList.vue`

**新增时间线过滤**:
```javascript
const timelineFilter = ref({
  project: 'all',        // 项目过滤
  milestoneStatus: 'all', // 里程碑状态
  taskId: 'all'          // 任务选择
});
```

### 3. TK运营中心重新设计

**文件**: `~/.openclaw/dashboard/tk-center.html`

**风格**: 科技清新风 (Inter字体 + 紫色渐变)

### 4. 下载功能修复

**问题**: URL路径错误 `/artifacts/` → `/api/download?name=`

**修复**: 添加搜索目录 + 创建测试文件(>1000字节)

---

## 🔗 GitHub仓库

| 仓库 | 用途 |
|------|------|
| **agentic-os-collective** | 代码+配置+Vue组件 |
| **agentic-os-knowledge-base** | 知识库+任务同步 |

### Commit记录 (本次会话)

| Commit Hash | 说明 |
|-------------|------|
| `f2e9d02` | daily backup: 2026-04-13 |
| `7229e63` | feat: 指挥中心里程碑伸缩抽屉 |
| `98ca724` | feat: 数据面板看板/时间线视图 |
| `0fe6736` | fix: TK子页面返回按钮样式 |

---

## 🔄 回滚方法

### 回滚到特定commit

```bash
# 查看commit历史
cd ~/agentic-os-collective
git log --oneline -10

# 回滚到特定版本
git checkout <commit-hash>

# 或创建回滚分支
git checkout -b rollback-20260413 <commit-hash>
```

### 恢复本地备份

```bash
# 恢复Dashboard页面
cp ~/Backups/Full-Backup-20260413-Session/dashboard-pages/*.html ~/.openclaw/dashboard/

# 恢复Vue组件
cp ~/Backups/Full-Backup-20260413-Session/vue-components/*.vue ~/agentic-os-collective/web/src/components/

# 恢复API
cp ~/Backups/Full-Backup-20260413-Session/openclaw-core/*.py ~/.openclaw/core/
```

---

## 📝 文件清单 (关键代码)

### 核心API
- `dashboard_api_v2.py` - 主API服务
- `safe_router.py` - 安全路由
- `task_updater.py` - 任务更新
- `execution_logger.py` - 执行日志

### Dashboard页面
- `index.html` - 指挥中心 (含里程碑抽屉)
- `tk-center.html` - TK运营中心
- `SYSTEM-ARCHITECTURE.md` - 系统文档

### Vue组件
- `TaskList.vue` - 任务列表+里程碑详情 (800+行)
- `App.vue` - Vue主应用
- `Dashboard.vue` - 数据面板容器

### TK编辑器
- `editor.html` - 可视化编辑器
- `accounts.html` - 账号管理
- `config-center.html` - 配置中心

### 脚本
- `fix_milestones.py` - 里程碑数据注入
- `sync_tasks_to_obsidian.py` - Obsidian同步
- `LAUNCH-SERVICES.sh` - 服务启动

---

*备份创建于: 2026-04-13 03:00 PDT*
*总文件数: 120+*