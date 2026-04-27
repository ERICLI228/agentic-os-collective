# Wiki Ops — 知识库运维技能

触发词: "编译 wiki" | "知识库巡检" | "查 wiki: xxx" | "回答并归档"

## 命令

### 编译 wiki

将 raw/ 中的原始素材编译为 wiki 页面。

```
python3 ~/agentic-os-collective/shared/scripts/wiki-ingest.sh <raw-file> --type <concept|entity|source>
```

AI 执行流程:
1. 读取 raw/ 中的素材文件
2. 用 template 创建 wiki 页面（带 YAML frontmatter + [[wikilinks]]）
3. 条目索引 index.md → 运行 `python3 wiki-ingest.py`
4. 更新 log.md

### 查 wiki: xxx

AI 回答知识库问题后自动归档。

1. 读 `wiki/index.md` → 定位相关页面
2. 读取页面内容
3. 综合回答，使用 `[[wikilinks]]` 引用
4. 运行 `python3 ~/agentic-os-collective/shared/scripts/wiki-query.py <slug> <title> <answer>`

### 知识库巡检

运行 lint 检查。

```
python3 ~/agentic-os-collective/shared/scripts/wiki-lint.py
```

输出保存到 `wiki/outputs/lint-report-{date}.md`

### Lint Cron 设置

```
0 9 * * 1 cd ~/agentic-os-collective && python3 shared/scripts/wiki-lint.py
```
