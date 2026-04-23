# TK 东南亚运营自动化 标准作业程序 (SOP)

> **版本**：v1.0  
> **生效日期**：2026-04-23  
> **适用系统**：`agentic-os-collective/tk/`  
> **维护人**：运营团队  
> **反向生成自**：`shared/templates/tk_pipeline.yaml` + `shared/knowledge/best_practices.yaml` + 执行日志分析

---

## 1. 业务流程概述

TK 运营自动化系统覆盖 **TikTok 东南亚 5 国**（印尼 / 越南 / 泰国 / 马来西亚 / 菲律宾）的 3C 品类全链路运营，通过 5 个自动化阶段实现从热门监控到数据上报的闭环。

```
┌─────────────┐    ┌─────────────┐  人工决策  ┌─────────────┐
│  MS-1       │───▶│  MS-2       │──────────▶│  MS-3       │
│  热门监控    │    │  爆款分析    │ 确认/重分析│  内容制作    │
│  每2小时     │    │  按需触发    │           │  按需触发    │
└─────────────┘    └─────────────┘           └──────┬──────┘
       ▲                  │                         │
       │            重新分析时回流                    ▼
       │                  │               ┌─────────────┐    ┌─────────────┐
       └──────────────────┘               │  MS-4       │───▶│  MS-5       │
                                          │  发布追踪    │    │  周报生成    │
                                          │  按需触发    │    │  每日23:00  │
                                          └─────────────┘    └─────────────┘
```

---

## 2. 阶段详解

### MS-1 热门监控

| 项目 | 内容 |
|------|------|
| **执行脚本** | `~/.agents/skills/proactive-operator/proactive-operator.sh` |
| **触发方式** | 定时自动（每 2 小时） |
| **超时限制** | 10 分钟 |
| **产出物** | `report_*.md`、`trending_products.json` |
| **决策节点** | 否 |

**执行内容**：
- 拉取 TikTok 东南亚各国 3C 品类热门视频数据
- 统计播放量、点赞量、评论数、分享数
- 生成热门产品列表，标注潜在爆款

---

### MS-2 爆款分析（含人工决策）

| 项目 | 内容 |
|------|------|
| **执行脚本** | `~/.openclaw/scripts/analyze_trending.py` |
| **触发方式** | MS-1 完成后自动触发 |
| **超时限制** | 5 分钟 |
| **产出物** | `analysis_report.json`、`product_recommendations.yaml` |
| **决策节点** | ✅ **是** — 需人工确认选品 |

**决策选项**：

| 选项 | 动作 | 说明 |
|------|------|------|
| ✅ 确认 | 进入 MS-3 | 同意当前选品建议 |
| 🔄 重新分析 | 回到 MS-1 | 数据不理想，重新采集 |

**爆款判定标准**（来自知识库）：
- 播放量 ≥ **300 万** → 标记为爆款
- 关注类目：ASMR 类、清洁类、定制类产品

---

### MS-3 内容制作

| 项目 | 内容 |
|------|------|
| **执行脚本** | `~/.openclaw/scripts/generate_content.py` |
| **触发方式** | 人工决策"确认"后 |
| **超时限制** | 5 分钟 |
| **产出物** | `video_scripts.json`、`content_calendar.yaml` |
| **决策节点** | 否 |

---

### MS-4 发布与追踪

| 项目 | 内容 |
|------|------|
| **执行脚本** | `~/.openclaw/scripts/publish_track.py` |
| **触发方式** | MS-3 完成后自动触发 |
| **超时限制** | 10 分钟 |
| **产出物** | `publish_status.json`、`performance_data.json` |
| **决策节点** | 否 |

---

### MS-5 周报生成

| 项目 | 内容 |
|------|------|
| **执行脚本** | `~/.openclaw/scripts/feishu/daily-report.sh` |
| **触发方式** | 每日 23:00 定时 |
| **超时限制** | 2 分钟 |
| **产出物** | `weekly_report.md`（推送至飞书群） |
| **决策节点** | 否 |

---

## 3. 定时任务清单

| Cron 表达式 | 触发时间 | 任务 | 说明 |
|------------|---------|------|------|
| `0 */2 * * *` | 每 2 小时整点 | MS-1 热门监控 | 7×24 小时持续运行 |
| `0 23 * * *` | 每天 23:00 | MS-5 周报生成 | 推送飞书日报 |

> **注**：MS-2 至 MS-4 由流水线内部串联触发，不单独设定 cron。

---

## 4. 关键监控指标及告警阈值

### 4.1 业务指标

| 指标 | 正常范围 | 告警阈值 | 告警动作 |
|------|---------|---------|---------|
| 视频播放量（爆款线） | < 300 万 | **≥ 300 万** | 立即触发爆款分析流程 |
| 爆款率（近 7 天） | 10%–50% | **> 50%** | 飞书预警，人工复核数据质量 |
| 日新增监控视频数 | > 100 条 | **< 50 条** | 检查 proactive-operator 连通性 |
| 选品确认等待时长 | < 24 小时 | **> 24 小时** | 飞书超时提醒 |

### 4.2 系统指标

| 指标 | 正常范围 | 告警阈值 | 告警动作 |
|------|---------|---------|---------|
| MS-1 执行时长 | < 5 分钟 | **> 8 分钟（timeout×0.8）** | 预警日志 |
| MS-1 近 24h 失败率 | < 5% | **> 10%** | 暂停自动执行，飞书人工告警 |
| API 账户余额 | > $50 | **< $20** | 飞书告警 + 自动切换免费方案 |
| 数据库文件大小 | < 500 MB | **> 800 MB** | 触发归档任务 |

### 4.3 数据质量指标

| 指标 | 说明 | 告警条件 |
|------|------|---------|
| JSON 解析失败率 | 外部 API 返回格式异常 | > 5% |
| 任务 ID 命名合规率 | 必须符合 `TK-*` 格式 | < 100% → 触发路由校验 |
| 跨业务线路由错误 | TK 任务调用了 drama 脚本 | **任意 1 次** → P0 告警 |

---

## 5. 异常处理流程

### 5.1 API 余额不足（HTTP 402）

```
检测到 402 错误
  ├─ 记录日志：status=failed, error=402_insufficient_balance
  ├─ 飞书推送：「⚠️ API 余额不足，已启动降级策略」
  ├─ 自动切换：降级到免费 API 或本地模型
  ├─ 等待 24 小时后自动重试
  └─ 若连续 3 天 402 → 升级为 P0，停止该业务线自动运行
```

### 5.2 执行超时

```
subprocess.TimeoutExpired 被捕获
  ├─ 里程碑状态 → failed（超时）
  ├─ 记录实际执行时长到日志
  ├─ 自动重试（最多 3 次，间隔 5 分钟）
  └─ 超过 3 次 → 飞书人工告警，停止该任务自动重试
```

### 5.3 跨业务线路由错误（生产 Bug）

> ⚠️ **已发现**：TK 任务（TK-20260410-001）执行了 drama 脚本（`water-margin-drama/controversy_rewriter.py`），导致里程碑状态写入错误任务 ID。

```
执行前 skill_loader.validate_task_skill() 校验
  ├─ 校验不通过（TK 任务 ≠ drama skill）
  │   ├─ 立即终止任务调度
  │   ├─ 飞书 P0 告警：「路由错误：{task_id} 匹配到错误 skill」
  │   └─ 记录到 execution_logs（action=routing_error）
  └─ 校验通过 → 正常执行
```

**永久修复方案**（见 `shared/skill_registry/skill_loader.py`）：
在每个 pipeline 入口调用：
```python
from shared.skill_registry.skill_loader import validate_task_skill
ok, reason = validate_task_skill(task_id, skill_name)
if not ok:
    raise RuntimeError(f"路由错误: {reason}")
```

### 5.4 数据库连接失败

```
sqlite3.OperationalError
  ├─ 检查 DB_PATH 文件是否存在且可写
  ├─ 若不存在：执行 python3 shared/data/init_db.py
  ├─ 若权限问题：检查目录权限（chmod 644 *.db）
  └─ 重新触发迁移：python3 -c "from shared.data.init_db import migrate_json_to_sqlite; migrate_json_to_sqlite()"
```

### 5.5 飞书 Webhook 推送失败

```
requests.RequestException（推送飞书）
  ├─ 检查 FEISHU_WEBHOOK_URL 环境变量是否已设置
  ├─ 测试命令：
  │   curl -X POST $FEISHU_WEBHOOK_URL \
  │        -H 'Content-Type: application/json' \
  │        -d '{"msg_type":"text","content":{"text":"连通性测试"}}'
  ├─ 若 Webhook 失效：登录飞书重新生成 → 更新 .env
  └─ 降级：写入本地日志，等待人工查阅
```

---

## 6. 任务命名规范

| 字段 | 格式 | 示例 |
|------|------|------|
| 完整 ID | `TK-[地区]-[品类]-[YYYYMMDD]-[序号]` | `TK-VN-美妆-20260423-001` |
| 简化 ID | `TK-[YYYYMMDD]-[序号]` | `TK-20260423-001` |

**规则**：
- 必须以 `TK-` 开头（用于 skill 路由校验）
- 只允许字母、数字、连字符，不含空格
- 长度 ≤ 64 字符

---

## 7. 上线前检查清单

在每次部署或重启系统前，逐项确认：

- [ ] `.env` 文件存在且包含所有必填密钥（运行 `python3 shared/config.py` 验证）
- [ ] `FEISHU_WEBHOOK_URL` 可正常推送（手动 curl 测试）
- [ ] 数据库文件可写（`ls -la shared/data/agentic.db`）
- [ ] `tk_pipeline.yaml` 中所有 `command` 均指向 `claw-operator` 脚本（非 drama 脚本）
- [ ] `skill_registry/registry.yaml` 中 TK skill 的 `compatible_tasks` 包含 `TK-*`
- [ ] `API_HOST` 配置为 `127.0.0.1`（非 `0.0.0.0`）
- [ ] cron 任务已注册（`crontab -l` 验证）

---

*本文档由 Claude Sonnet 4.6 基于 `tk_pipeline.yaml`、`best_practices.yaml`、执行日志反向生成*  
*下次人工复核日期：2026-05-23*
