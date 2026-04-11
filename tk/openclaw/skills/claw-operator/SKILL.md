# Claw Operator Skill - 状态机 + 失败分类 + 自动恢复

> 基于 Claude Code 核心逻辑实现
> 为 OpenClaw 添加企业级自动化能力

---

## 功能概述

| 能力 | 描述 |
|------|------|
| **状态机** | 细粒度 worker 状态跟踪 |
| **失败分类** | 机器可读失败类型 |
| **自动恢复** | 预设恢复配方 |

---

## 状态机 (Worker Status)

```
spawning → trust_required → ready_for_prompt → prompt_accepted → running → blocked → finished → failed
```

### 状态定义

| 状态 | 说明 |
|------|------|
| `spawning` | 正在创建 worker |
| `trust_required` | 等待信任确认 |
| `ready_for_prompt` | 可以接收任务 |
| `prompt_accepted` | 任务已接收 |
| `running` | 正在执行 |
| `blocked` | 被阻塞（等待外部资源） |
| `finished` | 成功完成 |
| `failed` | 执行失败 |

---

## 失败分类 (Failure Taxonomy)

### 主要类别

| 类别 | 子类 | 说明 |
|------|------|------|
| `auth` | api_key_missing, rate_limit, token_expired | 认证/限流问题 |
| `network` | timeout, connection_refused, dns_fail | 网络问题 |
| `config` | missing_config, invalid_config, permission_denied | 配置问题 |
| `tool` | tool_not_found, tool_failed, tool_timeout | 工具执行问题 |
| `code` | syntax_error, compile_error, test_failed | 代码问题 |
| `infra` | disk_full, memory_limit, process_killed | 基础设施问题 |
| `delivery` | webhook_failed, feishu_error | 消息投递问题 |

---

## 自动恢复 (Recovery Recipes)

### 预设配方

| 失败类型 | 恢复动作 |
|----------|----------|
| `rate_limit` | 等待 60s 后重试，最多重试 3 次 |
| `auth` | 检查 API key，提示重新配置 |
| `timeout` | 增加超时时间，重试 1 次 |
| `network` | 检查网络连接，重试 2 次 |
| `delivery` | 检查 webhook 配置，尝试备用通道 |

---

## 使用方法

### 检查 cron 任务状态

```
请检查所有 cron 任务状态，分类失败类型，并尝试自动恢复失败任务
```

### 检查 worker 状态

```
请列出所有 worker 的当前状态
```

### 手动触发恢复

```
请尝试恢复 [任务名称]，使用 [recovery_recipe] 配方
```

---

## 实现文件

- `state_machine.py` - 状态机实现
- `failure_classifier.py` - 失败分类器
- `recovery_recipes.py` - 恢复配方
- `config.json` - 技能配置