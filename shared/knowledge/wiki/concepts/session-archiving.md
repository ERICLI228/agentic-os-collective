---
title: "会话归档机制"
date_created: 2026-04-27
date_modified: 2026-04-27
summary: "基于 Clicky/CPR 理念的三大设计模式：决策提取、结构化日志、自动归档"
tags: [methodology, session-management, archiving, logging]
type: concept
status: final
---

# 会话归档机制

## 来源

从两个开源项目提取：
- **Clicky**（4.8K ⭐）— 结构化 Prompt 标签 `[POINT:x,y:label]`、Cancel-and-Replace 并发、双日志体系
- **CPR**（294 ⭐）— `/preserve` `/compress` `/resume` 三命令的会话生命周期管理

## 三大设计模式

### 1. 会话结束前主动保存关键决策
借鉴 Clicky 的 `[POINT:]` 标签 + CPR 的 `/preserve`，在会话结束时自动：
- 扫描会话中所有 AI 回复，提取含"决定/选择/设置/切换/创建"关键词的句子
- 写入 `shared/knowledge/wiki/log.md`（结构化日志）
- 归档完整摘要到 `wiki/outputs/session-{timestamp}.md`

### 2. 结构化日志格式
采用 YAML frontmatter + `[[wikilinks]]` 的统一格式：
```yaml
---
title: "会话归档"
date_created: 2026-04-27
session_file: "xxx.jsonl"
message_count: 42
type: output
status: final
tags: [session-archive]
---
```
日志规范：
- `wiki/log.md` — 只追加不覆盖，按时间排序
- `wiki/outputs/` — 每会话一篇完整归档
- `workspace/memory/timeline.md` — 关键决策时间线（去重汇总）

### 3. 自动归档机制
触发方式：
- 用户说"结束"/"归档"/"保存" → 手动触发
- `post-llm-call` hook → 自动检测会话结束
- `bash ~/agentic-os-collective/scripts/archive-session.sh` → 一键运行

## 实现文件
- `shared/scripts/session-archiver.py` — 核心：提取→格式→归档
- `scripts/archive-session.sh` — 命令行入口
- 根 `CLAUDE.md` — 归档规则定义

## 相关概念
- [[llm-wiki-methodology]]
