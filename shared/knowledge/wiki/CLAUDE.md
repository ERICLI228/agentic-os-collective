# 知识库 AI Schema

## 总体说明

本知识库服务于 agentic-os-collective 项目，由 AI 负责维护 `wiki/` 内容；人类负责方向决策和 `raw/` 素材投喂。每次执行任务后应自动回填知识。

## 目录结构

```
shared/knowledge/
├── CLAUDE.md          # 本文件 - AI操作指令
├── best_practices.yaml
├── raw/               # 原始资料区（人类只读，AI不写）
│   ├── articles/      # 网页/文章剪藏
│   └── notes/         # 临时笔记
├── wiki/              # 编译后知识（AI读写维护）
│   ├── index.md       # 总索引 - 每页一句话摘要
│   ├── log.md         # 操作日志 - 只追加不覆盖
│   ├── concepts/      # 概念/方法论页面
│   ├── entities/      # 实体页面（人/工具/平台/组织）
│   ├── syntheses/     # 跨主题综合分析
│   └── outputs/       # 查询结果归档
└── templates/         # 待建
```

## 文件规范

- 文件名：kebab-case，全小写，如 `active-inference.md`
- YAML frontmatter：
  ```yaml
  ---
  title: "页面标题"
  date_created: YYYY-MM-DD
  date_modified: YYYY-MM-DD
  summary: "一句话说明"
  tags: [标签1, 标签2]
  type: concept | entity | synthesis | output
  status: draft | review | final
  ---
  ```
- 内部交叉引用使用 `[[wikilinks]]`
- 关键术语首次出现时加粗

## 操作规则

### INGEST（当 raw/ 中有新素材时）
1. 读取新素材
2. 在 `wiki/` 中创建对应摘要/概念/实体页面
3. 用 `[[wikilinks]]` 连接新内容和已有内容
4. 更新 `wiki/index.md`
5. 追加 `wiki/log.md`

### QUERY（当被问及知识库主题时）
1. 先读 `wiki/index.md` 了解范围
2. 读取相关页面
3. 输出带 `[[wikilink]]` 引用的综合答案
4. 答案保存到 `wiki/outputs/{question-slug}.md`
5. 更新 `index.md` 和 `log.md`

### LINT（定期健康检查）
1. 找页面冲突（用 ⚠️ 标注）
2. 找孤儿页面（无人链）
3. 找断链（`[[wikilinks]]` 指向不存在页面）
4. 检查 frontmatter 是否缺失
5. 标记过期内容（来源超过6个月）
6. 识别高频引用但未独立成页的概念
7. 能自动修的直接修，输出报告到 `wiki/outputs/lint-report-{date}.md`

## 质量标准

- 摘要 200-500 字，综合提炼不照抄
- 概念 500-1500 字，开头有清晰导语
- 所有判断需追溯来源
- 内容冲突用 ⚠️ 标出，写清双方来源
- 优先相信更新更近的资料

## 何时新建页面

- 概念/实体在 2+ 来源出现 → 创建完整页面
- 只出现 1 次 → 创建 stub（frontmatter + 定义 + 回源链接）
- 不允许存在无页面的 `[[wikilinks]]`
