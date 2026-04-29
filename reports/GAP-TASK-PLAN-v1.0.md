# Agentic OS v3.5 拉齐计划 — 从 55% → 85%

> 基准: PRD v3.5 第四部分 (45 FR)  
> 真实完成度: ~55% (PRD 标注 85% 不可信)  
> 日期: 2026-04-29  
> 核心差距: 安全未修 + 决策单向 + 短剧降级 + 计划外堆量

---

## P0 — 安全 & 安全 (Day 1, ~4h)

### TASK-SEC-01: TK/短剧路由隔离
**关联**: FR-BS-003, 红线4 | **现状**: 无校验，TK任务可误调短剧脚本

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `test_tk_routing.py` 创建 | 3/3 PASS: TK→operator✅, TK→drama❌, drama→drama✅ | 0.5h |
| `registry.yaml` non-overlapping compatible_tasks | 两套 skill 无交叉 | 0.5h |
| `skill_loader.validate_task_skill()` 实现 | 调用返回 True/False，False 抛出 RouteBlockedError | 0.5h |

### TASK-SEC-02: execution_logger 命令注入修复
**关联**: FR-BS-005, 红线3/4 | **现状**: `shell=True` 残留，可注射

| 子任务 | 验收 | 预估 |
|--------|------|------|
| 替换所有 `shell=True` → `shell=False` | grep -rn "shell=True" shared/ 返回空 | 0.5h |
| `run_and_log()` 增加注入检测 | `echo $(rm -rf ~)` 被拒绝+记录 | 0.5h |
| `ALLOWED_COMMAND_PREFIXES` 清理 | 移除 `echo` 等危险前缀 | 0.25h |

### TASK-SEC-03: 全仓库硬编码扫描
**关联**: FR-BS-004, 红线3 | **现状**: CLAUDE.md 已清, adversarial_review 已清, 但未全量扫描

| 子任务 | 验收 | 预估 |
|--------|------|------|
| 5 组 grep 扫描全部返回空 | `grep -rn "sk-[a-zA-Z0-9]" --include='*.py' \| grep -v '.env'` 返回 0 | 0.25h |
| 所有 API key 统一经 `config.py` | 代码中无 `os.environ.get` 裸调 | 0.25h |

---

## P0 — 决策双向化 (Day 1-2, ~6h)

### TASK-DEC-01: 飞书决策回调端点
**关联**: FR-BS-014 | **现状**: 全单向，决策靠手动文件轮询

| 子任务 | 验收 | 预估 |
|--------|------|------|
| Flask `/api/callback/feishu` 端点 | POST 接收飞书卡片交互事件 | 1h |
| 决策卡片发送 + 回调处理 | 用户点击[通过]→ 飞书回调 → 任务状态推进 | 1.5h |
| 三节点各自卡片: market_assessment / selection / publish | 每节点推卡 → 点选 → 30s 内推进 | 1.5h |

### TASK-DEC-02: 驾驶舱数据链路接通
**关联**: FR-CO-001~002 | **现状**: Vite 壳在 :5173, 数据空

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `/api/dashboard/summary` 返回真实双线 KPI | curl 返回 JSON 含 TK+短剧摘要 | 0.5h |
| Dashboard 首页显示任务列表 + 待决策角标 | 浏览器打开 :5173 → 看到任务 | 0.5h |
| 决策提交按钮接通 `/api/decision` | 点击按钮 → 状态更新 → 刷新可见 | 1h |

---

## P1 — 短剧影视级 (Day 2-4, ~12h)

### TASK-DRM-01: NLS 配音替换 macOS say
**关联**: FR-DR-007 | **现状**: macOS say 机械声 | **前提**: 用户在 .env 填 ALIYUN_* 三件套

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `aliyun_nls.py` 调用 NLS 实时 TTS | 生成 .wav 文件, 大小 >10KB | 1h |
| `pipeline_ep01.py` NLS 模式 | `--voice nls` 切换 → 产出含真人配音的 final.mp4 | 1h |
| 预算控制: 单集 <500 字符 | 日志打印 TTS 调用字符数 | 0.5h |

### TASK-DRM-02: Seedance / fal.ai 视频生成
**关联**: FR-DR-004 | **现状**: Pillow 渐变色块 | **前提**: 读 fal.ai SKILL 确认免费额度

| 子任务 | 验收 | 预估 |
|--------|------|------|
| fal.ai Seedance API 集成 | `text-to-video` 返回 mp4 URL | 2h |
| 每个分镜生成 3-5s 视频片段 | 5 个 .mp4 分镜片段 | 2h |
| 替换 pipeline_ep01 的 Pillow 帧 → Seedance 视频 | final.mp4 画面为 AI 生成 | 1.5h |
| 降级策略: fal.ai 不可用 → Pillow | `--fallback pillow` 参数 | 0.5h |

### TASK-DRM-03: 3-Agent 对抗审核架构
**关联**: FR-DR-005 | **现状**: 单 LLM 评分，非三角色

| 子任务 | 验收 | 预估 |
|--------|------|------|
| 参谋 Agent (Claude/GLM): 挑刺 → 5 维评分 | 输出批判性 JSON | 1.5h |
| 裁判 Agent (独立调用): 裁量 → 最终 decision | 避免自我评分偏差 | 1h |
| `adversarial_review.py` `--mode multi-agent` | 非 mock 模式跑通 | 0.5h |

---

## P1 — TK 运营补齐 (Day 3-4, ~8h)

### TASK-TKO-01: MS-0 数据质量门禁
**关联**: FR-TK-002 | **现状**: 无校验，脏数据直通

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `data_validator.py` 校验采集箱数据 | price>0, title 非空, SKU 有效 | 1h |
| pipeline MS-1 前插入 MS-0 gate | 未通过 → 飞书告警 + 暂停 | 0.5h |

### TASK-TKO-02: 竞品监控
**关联**: FR-TK-003, FR-TK-004 | **现状**: 仅有定价计算器

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `competitor_monitor.py` 竞品价格+销量采集 | 输出 competitor_report.json | 2h |
| 飞书告警: 竞品降价 >15% | 推送告警卡片 | 0.5h |

### TASK-TKO-03: 店铺健康度
**关联**: FR-TK-011 | **现状**: pipeline 引用但代码缺失

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `shop_health_monitor.py` | 检查 6 店违规点/扣分/处罚 | 1.5h |
| 飞书告警: 违规/扣分 | 推送告警卡片 | 0.5h |

### TASK-TKO-04: 订单拉取
**关联**: FR-TK-007 | **现状**: 只能发，不能读

| 子任务 | 验收 | 预估 |
|--------|------|------|
| 妙手订单 API 逆向 | 获取订单列表 JSON | 1h |
| 更新 feishu_daily 含真实订单数 | 日报显示真实订单 | 0.5h |

### TASK-TKO-05: 达人联盟 (手动)
**关联**: FR-TK-010, Sprint 3.4 | **现状**: 紫鸟阻隔

| 子任务 | 验收 | 预估 |
|--------|------|------|
| 紫鸟登录 → TK Seller → Affiliate → 15% → 邀请≥10 达人 | 飞书群有开通记录 | 0.5h (手动) |

---

## P2 — 基础设施 (Day 4, ~3h)

### TASK-INF-01: 统一配置迁移完成
**关联**: FR-BS-004 | **现状**: config.py 存在但未全局使用

| 子任务 | 验收 | 预估 |
|--------|------|------|
| 5 组 grep 全部空 | host='0.0.0.0' / API_BASE 裸写 / api_key 裸写 / token 裸写 / secret 裸写 | 0.5h |
| task_wizard.py host → config.API_HOST | 默认 127.0.0.1 | 0.25h |

### TASK-INF-02: Token 预算集成
**关联**: FR-BS-002 | **现状**: governor 存在但未接入 pipeline

| 子任务 | 验收 | 预估 |
|--------|------|------|
| pipeline 每一步前 check_budget() | 超预算 → 暂停 + 飞书提醒 | 1h |

### TASK-INF-03: 周报推送
**关联**: FR-TK-014 | **现状**: 只有日报

| 子任务 | 验收 | 预估 |
|--------|------|------|
| `feishu_weekly.py` | 每周一 09:00 推周报到飞书 | 1h |

---

## 排期总览

| 阶段 | 天数 | 任务数 | 预估 | 目标 |
|------|------|--------|------|------|
| **P0 安全** | Day 1 上午 | 3 | 2.5h | 零硬编码、路由隔离、命令安全 |
| **P0 决策** | Day 1 下午 | 2 | 3.5h | 飞书可点击决策、驾驶舱有数据 |
| **P1 短剧** | Day 2-3 | 3 | 9.5h | NLS 配音 + AI 视频 + 3-Agent 审核 |
| **P1 TK** | Day 3-4 | 5 | 7h | 竞品监控 + 店铺健康 + 订单拉取 |
| **P2 基础** | Day 4 | 3 | 2.5h | 配置统一 + Token 预算 + 周报 |
| **合计** | 4 天 | 16 | **25h** | 55% → 85% |

## 依赖关系

```
SEC-01 ──→ SEC-02 ──→ SEC-03 ──→ DEC-01 ──→ DEC-02
                                      │
                      DRM-03 ←────────┤
                          │           │
DRM-01 (需 .env Key) ────┴─── DRM-02 (需 fal.ai 额度)
                          │
TKO-01 ──→ TKO-02 ──→ TKO-03 ──→ TKO-04
                                      │
                    INF-01 ←── INF-02 ← INF-03
```

## 阻塞项

| 阻塞 | 影响任务 | 解决人 |
|------|----------|--------|
| ALIYUN_* 三件套未填 .env | DRM-01 不能启动 | 阿牛手动填 |
| fal.ai 免费额度未确认 | DRM-02 可能降级 | 先读 fal.ai SKILL |
| 紫鸟不支持 CDP | TKO-04 订单拉取可能无法自动化 | 手动/半自动 |
| Sprint 3.4 达人联盟 | TKO-05 | 阿牛手动完成 |
