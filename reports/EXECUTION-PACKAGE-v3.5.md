# AGENTIC OS v3.5 完整执行任务包

> **环境**: macOS (darwin, arm64) | 工作目录: `/Users/hokeli/agentic-os-collective/`  
> **模型**: 默认 `ollama/llama3.2:3b` | 备选 `deepseek/deepseek-v4-flash` | 复杂 `aliyun/qwen3.6-plus` | 代码 `aliyun/qwen3-coder-plus`  
> **Gateway**: `localhost:18789` | **驾驶舱**: `localhost:5173` (Vite)  
> **飞书回调端点**: `https://agentic-os-gateway.fly.dev/feishu/card`  
> **OpenClaw 启动**: `openclaw gateway start` (launchd `~/Library/LaunchAgents/com.openclaw.gateway.plist`)

---

## 任务包概览

```
Sprint 0: 止血（感知优先）      → 4 任务，约 4 小时
Sprint 1: 你能看到（TK/短剧）  → 5 任务，约 18 小时
Sprint 2: 你能控制（决策/驾驶舱）→ 4 任务，约 32 小时
Sprint 3: 全场景覆盖           → 4 任务，约 28 小时
Sprint 4: 持续优化             → 4 任务，约 20 小时
─────────────────────────────────────────
共 21 个核心任务，约 102 小时
```

---

## Sprint 0 — 止血（你必须先能"看见"）

> **目标**: 让你能打开一个页面就看到系统在做什么  
> **原则**: 在驾驶舱建好前，不新增任何脚本复杂度

### 任务 0.1: 驾驶舱状态 API

| 项目 | 内容 |
|------|------|
| **文件** | `shared/task_wizard.py` (现有文件) |
| **改动** | 新增 `GET /api/status` 路由 |
| **返回格式** | JSON: `{ tasks: [{id, name, status, decision_pending}], milestones: [...], system_health: "ok" }` |
| **验收** | `curl http://localhost:5001/api/status` 返回任务列表 |

```
GET /api/status
→ 200 OK
{
  "tasks": [
    { "id": "MS-1", "name": "品类数据采集", "status": "running", "decision_pending": false },
    { "id": "MS-4", "name": "商品发布", "status": "waiting_approval", "decision_pending": true }
  ],
  "milestones": [
    { "ms": "MS-1.5", "name": "市场判断", "decision_point": true, "locked": true }
  ],
  "system_health": "ok"
}
```

### 任务 0.2: 飞书状态推送

| 项目 | 内容 |
|------|------|
| **文件** | `shared/feishu_status_push.py` (新建) |
| **功能** | 每 30 分钟推送一次系统状态到飞书群 |
| **卡片内容** | 当前任务数 + 完成数 + 待决策数 + 异常提醒 |
| **验收** | 飞书群收到一张带数字的状态卡片 |
| **注意** | 使用 `shared/feishu.py` 推送，无回调按钮，纯查看 |

```
┌─────────────────────────────────────┐
│ 📊 Agentic OS 系统状态               │
│                                     │
│ 总任务: 12 │ 完成: 7 │ 进行中: 3     │
│ ⚠️ 待决策: 2 (市场判断 + 发布审批)    │
│ 🟢 网关: 运行中 │ 🤖 Claude: 在线    │
│                                     │
│ ⏰ 下次推送: 30 分钟后               │
└─────────────────────────────────────┘
```

### 任务 0.3: 对抗审核框架搬迁

| 项目 | 内容 |
|------|------|
| **原位置** | `/Users/hokeli/AI_Short_Drama_Pipeline/adversarial_review.py` (743 行) |
| **目标位置** | `shared/core/adversarial_review.py` |
| **改动** | 修复 import 路径，确保 `python3 -c "from shared.core.adversarial_review import *"` 不报错 |
| **验收** | `python3 -m pytest shared/tests/test_adversarial_review.py` 通过 |

### 任务 0.4: 发布审批硬约束

| 项目 | 内容 |
|------|------|
| **文件** | `shared/publish_gate.py` (新建) |
| **功能** | 所有发布代码必须先调 `check_approval(task_id)`，不通过就抛 `PublishBlockedError` |
| **条件** | `os.environ.get("MIAOSHOW_PUBLISH_ENABLED") == "true"` AND `task_pending_approval → human_approved: true` |
| **验收** | `MIAOSHOW_PUBLISH_ENABLED=false` 时任何发布函数抛出异常 |

```python
# shared/publish_gate.py 核心逻辑
def check_approval(task_id: str) -> bool:
    """发布前检查：环境变量 + 人工审批"""
    if os.environ.get("MIAOSHOW_PUBLISH_ENABLED") != "true":
        raise PublishBlockedError(f"发布被阻止: MIAOSHOW_PUBLISH_ENABLED != true")
    
    # 检查 task_wizard 中的审批状态
    task = get_task(task_id)
    if not task.get("human_approved"):
        raise PublishBlockedError(f"发布被阻止: task {task_id} 未获得人工审批")
    
    return True
```

---

## Sprint 1 — 你能看到（本周，约 18 小时）

> **目标**: TK 运营有决策节点，短剧第一集产出可播放 MP4

### 任务 1.1: Pipeline 决策节点修复

| 项目 | 内容 |
|------|------|
| **文件** | `tk/openclaw/pipelines/tk_pipeline.yaml` |
| **改动** | 确认 MS-1.5 (市场判断) 和 MS-4 (发布审批) 节点的 `decision_point: true`，并新增 `decision_type` 字段 |
| **验收** | `python3 -c "import yaml; d=yaml.safe_load(open('tk/openclaw/pipelines/tk_pipeline.yaml')); assert d['milestones']['MS-1.5']['decision_point'] == True"` 不报错 |

```yaml
MS-1.5:
  name: "市场判断"
  decision_point: true
  decision_type: "market_assessment"   # 新增
  decision_options:
    - "值得做"
    - "换品类"
    - "不做"
  decision_timeout_hours: 48           # 48小时不决策则飞书提醒
```

### 任务 1.2: 飞书日报真实数据

| 项目 | 内容 |
|------|------|
| **文件** | `shared/feishu_daily.py` (新建，基于现有 daily_business_summary.py 逻辑) |
| **功能** | 每日 09:00 和 21:00 推送含真实/降级数据的状态卡片到飞书 |
| **数据来源** | 妙手 API (已连通) → 采集箱计数 / FastMoss (如有) / Mock 降级 |
| **验收** | 飞书群收到日报卡片，数字不是硬编码的 0 或 test |

### 任务 1.3: 选品分析飞书卡片

| 项目 | 内容 |
|------|------|
| **文件** | `shared/feishu_cards/selection_card.py` (新建) |
| **功能** | 生成一个带按钮的飞书卡片：[通过] [修改条件] [驳回] |
| **回调** | 按钮回调 → `shared/feishu_callback_handler.py` → 更新 task_wizard 中的决策状态 |
| **验收** | 你在飞书点 "通过" → 30秒内系统状态变为 `selection_approved` |

```
┌─────────────────────────────────────┐
│ 🛒 选品审核 - 3C数码配件             │
│                                     │
│ TOP3 推荐:                          │
│ 1. 手机壳(透明支架款) ¥3.2 → 售价$8.9│
│    📊 竞品: 34 | 📈 利润: 67%        │
│    ⭐ 对抗评分: 8.3/10               │
│ 2. 磁吸充电宝 ¥22 → 售价$15.9       │
│ 3. AirPods保护套 ¥1.8 → 售价$5.9    │
│                                     │
│ [✅ 通过TOP3] [✏️ 修改] [❌ 驳回]    │
└─────────────────────────────────────┘
```

### 任务 1.4: 创建 `drama_merge.py`

| 项目 | 内容 |
|------|------|
| **文件** | `drama/openclaw/video_pipeline/drama_merge.py` (新建) |
| **功能** | 合并视频片段 + 配音轨 + 字幕，输出最终 MP4 |
| **验收** | `python3 drama/openclaw/video_pipeline/drama_merge.py --help` 不报错 |

### 任务 1.5: 短剧第一集端到端

| 项目 | 内容 |
|------|------|
| **流程** | 剧本生成 → 角色设计 → 分镜 → 配音 → 合成 → 审核 → MP4 |
| **执行** | 手动辅助运行每条命令，记录失败环节 |
| **验收** | 产出 `final.mp4` 且 `ffprobe final.mp4` 显示有效时长>0 |

---

## Sprint 2 — 你能控制（本月前两周，约 32 小时）

> **目标**: 驾驶舱可用，妙手 ERP 打通

### 任务 2.1: 驾驶舱决策界面

| 项目 | 内容 |
|------|------|
| **位置** | `web/` (现有 Vite 项目, port 5173) |
| **页面** | `/status` — 任务列表 + 待决策角标; `/decision/:task_id` — 决策表单; `/history` — 历史决策日志 |
| **数据源** | `GET /api/status` (任务 0.1) → 前端轮询每 10 秒 |
| **验收** | 打开 `localhost:5173/status` 看到任务列表，点击待决策任务跳转到决策页面 |

### 任务 2.2: 妙手 ERP 商品 API 逆向后打通

| 项目 | 内容 |
|------|------|
| **方法** | 浏览器自动化: 启动 Chrome `--remote-debugging-port=9222` → agent-browser `--auto-connect` |
| **目标** | 捕获发布 API 的 URL、参数、请求体格式 |
| **工具** | `agent-browser` + DevTools Protocol (Network 面板抓包) |
| **期望** | 先连通测试，输出明确结果（成功或失败日志） |
| **注意** | 需要你先关闭 紫鸟 或其他占用端口的程序，或使用独立 CDP 端口 |

### 任务 2.3: 选品对抗审核完整实现

| 项目 | 内容 |
|------|------|
| **文件** | `shared/core/adversarial_review.py` (已搬迁的任务 0.3 输出) → 新增 `tk_review` 场景 |
| **功能** | `review_product(product_data)` → 返回含五维评分和 decision 字段的评审结果 |
| **五维** | 竞品饱和度 / 利润空间 / 供应链 / 季节性 / 达人潜力 |
| **验收** | `python3 -c "from shared.core.adversarial_review import *; print(review_product(test_data))"` 返回评分结果 |

### 任务 2.4: 里程碑状态追踪

| 项目 | 内容 |
|------|------|
| **文件** | `shared/milestone_tracker.py` (新建) |
| **功能** | 中心化状态机，每个里程碑有 id/name/status/decision_pending/updated_at |
| **状态** | `pending → running → waiting_decision → approved/rejected → completed/failed` |
| **存储** | JSON 文件 `~/.agentic-os/milestones.json` (避免数据库依赖) |
| **验收** | 随时 `python3 -c "from shared.milestone_tracker import *; print(get_all_milestones())"` 可查状态 |

---

## Sprint 3 — 全场景覆盖（本月后两周，约 28 小时）

> **目标**: 对抗审核全场景，达人联盟

### 任务 3.1: `role_designer.py` 实现

| 项目 | 内容 |
|------|------|
| **文件** | `drama/openclaw/core/role_designer.py` |
| **功能** | 调用 Seedance / AutoGLM 生成角色三视图+视觉设定 |
| **验收** | 输出 `character_designs.json` 文件 |

### 任务 3.2: 广告文案对抗审核

| 项目 | 内容 |
|------|------|
| **文件** | `shared/core/adversarial_review.py` → 新增 `tk_ad_review` 场景 |
| **功能** | 四维审核：合规性/转化力/本地化/品牌一致性，8 分阈值 |
| **验收** | 能对测试文案返回评分结果 |

### 任务 3.3: 剧本对抗审核（前置）

| 项目 | 内容 |
|------|------|
| **文件** | `shared/core/adversarial_review.py` → 新增 `drama_script_review` 场景 |
| **功能** | 剧本生成后立即前置审核，不通过不进入制作流程 |
| **验收** | 剧本产出后自动触发审核评分 |

### 任务 3.4: 开通 TikTok 达人联盟

| 项目 | 内容 |
|------|------|
| **动作** | 设置 15% 佣金，邀请首批 ≥10 个达人 |
| **工具** | 浏览器操作 TikTok Shop 后台 (手动或 agent-browser 协助) |
| **验收** | 飞书群收到达人联盟开通确认记录 |

---

## Sprint 4 — 持续优化（次月，约 20 小时）

> **目标**: 预测模型 + 系统稳定

### 任务 4.1: 早期爆款预测模型

- 基于前 4 小时数据（曝光/点击/加购/转化）训练简单回归模型
- 验收：预测准确率 > 70%

### 任务 4.2: 完播率追踪

- 短剧发布后追踪每集完播率数据
- 验收：数据每小时更新

### 任务 4.3: 3PL 物流对接

- 订单自动推送至物流商 API
- 验收：订单→物流单号自动返回

### 任务 4.4: 达人 CRM 基础版

- 达人信息管理 + 合作追踪
- 验收：可添加/查看/筛选达人

---

## 五条红线（硬约束）

> 以下规则已写入 `shared/knowledge/best_practices.yaml`，任何 Agent 违反即停止执行

| # | 红线 | 说明 | 违反处理 |
|---|------|------|---------|
| 1 | **禁止自动发布** | 所有发布动作必须检查 `MIAOSHOW_PUBLISH_ENABLED=true` 且任务 JSON 中有 `human_approved: true` | Agent 停止，记录违规日志 |
| 2 | **禁止跳过决策节点** | pipeline 中 `decision_point: true` 的阶段必须等到 `/api/decision` 被调用 | 任务状态设为 failed |
| 3 | **禁止硬编码密钥** | 所有 API Key 从 `shared/config.py` 读取 (从 `.env` 加载) | Code review 不通过 |
| 4 | **禁止跨业务线调度** | 执行前必须调 `skill_loader.validate_task_skill(task_id, skill_name)` | 路由拦截报错 |
| 5 | **禁止覆盖已有数据** | 写入前检查目标文件是否存在，存在时追加时间戳后缀 | 写入失败，保留原文件 |

---

## Mac 环境注意事项

| Linux 常见做法 | macOS 替代 | 说明 |
|---------------|-----------|------|
| `systemctl` | `launchctl` + `launchd plist` | `~/Library/LaunchAgents/` 存放 plist |
| `apt install` | `brew install` | Homebrew 安装路径 `/opt/homebrew/bin/` |
| `/etc/cron.d/` | `launchd` 或 `crontab -e` | launchd 推荐，开机自启 |
| `/tmp/` | `/tmp/` 可用但重启清空 | 持久数据放 `~/.agentic-os/` |
| `xdg-open` | `open` | macOS 用 `open` 打开文件/URL |
| `/home/user/` | `/Users/username/` | 用户目录路径不同 |
| `python3` | `/opt/homebrew/bin/python3` | Homebrew Python 位置 |
| Chrome `--headless` | 同参数可用 | GPU 加速需注意 arm64 兼容性 |

---

## 快速启动

```bash
# 0. 检查环境
python3 --version && node --version && brew --version

# 1. 启动 OpenClaw Gateway
openclaw gateway start

# 2. 启动驾驶舱 (Vite)
cd /Users/hokeli/agentic-os-collective/web && npm run dev &

# 3. 验证状态 API
curl http://localhost:5001/api/status

# 4. 检查飞书推送 (需先配置 FEISHU_WEBHOOK_URL)
python3 shared/feishu_status_push.py --test

# 5. 启动 Chronicle (状态追踪)
```
