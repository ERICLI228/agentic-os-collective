---
title: "LLM Wiki 知识库方法论"
date_created: 2026-04-27
date_modified: 2026-04-27
summary: "基于 Karpathy 模式的知识库三层架构：raw + wiki + CLAUDE.md"
tags: [methodology, knowledge-management, AI]
type: concept
status: final
---

# LLM Wiki 知识库方法论

由 Andrej Karpathy 提出、经社区验证的一套个人/团队知识库方法论。核心思想是把 LLM 从"问完就忘的聊天窗口"升级为"持续复利的知识基础设施"。

## 三层架构

- **raw/** — 原始资料，唯一事实来源，AI 只读不改
- **wiki/** — 编译后结构化知识，AI 维护
- **CLAUDE.md** — Schema，控制 AI 行为的指令文件

## 四个循环

- **Ingest**：新资料 → 摘要 + 概念提取 + 交叉链接
- **Compile**：增量更新 wiki，不整页重写
- **Query**：基于 wiki 提问 → 带引用答案 → 存回
- **Lint**：健康检查（冲突/断链/孤儿/过期）

## 本项目的集成

- 根 `CLAUDE.md` 已加入知识回填规则
- `shared/knowledge/wiki/` 已构建完整目录结构
- Agent 每次执行任务自动回填

## 相关概念

- [[知识回填循环]]
- [[CLAUDE.md AI Schema]]
