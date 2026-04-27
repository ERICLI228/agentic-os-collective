---
title: "LLM Wiki - Karpathy 个人知识库方法论"
date_created: 2026-04-27
date_modified: 2026-04-27
source: "https://mp.weixin.qq.com/s/ueCIydLLACyqGP5SrAhpjQ"
type: article
tags: [methodology, knowledge-base, CLAUDE.md, obsidian]
status: final
---

# LLM Wiki - Karpathy 个人知识库方法论

原文由石榴爸爸翻译整理自 Karpathy 推特。核心思想：把 AI 从"问完就忘的聊天工具"变成"持续积累的知识基础设施"。

## 核心架构

**三层结构：**
1. `raw/` — 原始资料区（只读，人负责投喂）
2. `wiki/` — 编译后知识（AI 读写维护）
3. `CLAUDE.md` — Schema/指令文件（控制 AI 行为）

**四个持续循环：**
- **Ingest（摄入）** — 新资料→摘要+概念+连接
- **Compile（编译）** — 更新 wiki 页面和索引
- **Query（提问）** — 基于 wiki 做研究，答案存回
- **Lint（巡检）** — 健康检查：冲突/断链/过期

## 关键原则

1. **回填循环** — 每次回答/任务结果存回 wiki，形成复利
2. **CLAUDE.md 作为 AI Schema** — 告诉 AI 怎么组织、什么规则、什么操作
3. **纯文本永续性** — Markdown 格式，无厂商锁定
4. **增量更新** — 不整页重写，只补充新内容

## 对我们系统的价值

已在本项目 `shared/knowledge/wiki/` 中落地：
- `CLAUDE.md` — AI Schema 指令
- `index.md/log.md` — 索引和日志
- 目录结构：raw/（原始资料）、wiki/concepts/（概念）、wiki/entities/（实体）、wiki/outputs/（查询输出）
- 知识回填规则已写入根 CLAUDE.md
