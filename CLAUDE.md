# agentic-os-collective Schema

> 版本：2026-04-27 | 仓库：~/agentic-os-collective/

## 项目结构

```
agentic-os-collective/
├── drama/     # AI数字短剧自动化
│   └── openclaw/
│       ├── core/     # 下载/决策/Token治理/路由
│       └── skills/water-margin-drama/  # 水浒传短剧
├── tk/        # TK东南亚运营
│   └── openclaw/
│       ├── core/     # 与drama共享结构
│       └── skills/claw-operator/       # 运营Operator
├── shared/    # 共享基础设施
│   ├── mcp_task_server.py
│   ├── execution_logger.py
│   └── knowledge/   # 知识库（见下方Schema）
├── dashboard/ api/ gateway/ hooks/ tests/ reports/
```

## AI 行为规则

### 知识回填（每次任务后必须执行）
完成任务后，检查是否有新的可沉淀知识：

1. **如果是新发现的方法/方案/结论** → 写入 `shared/knowledge/raw/notes/`
2. **如果是可复用的最佳实践** → 更新 `shared/knowledge/best_practices.yaml`
3. **如果回答了一个复杂问题** → `wiki-query.py` 存档到 `wiki/outputs/`
4. **如果是新概念/实体** → `wiki-ingest.py` 在 `wiki/concepts/` 或 `wiki/entities/` 中创建页面
5. **操作完成后** → 更新 `wiki/index.md` 和 `wiki/log.md`

### 提问时的行为（Query 闭环）
1. 先读 `shared/knowledge/wiki/CLAUDE.md`（Schema）
2. 再读 `wiki/index.md`（现有内容概览）
3. 加载相关页面后回答，带 `[[wikilink]]` 引用
4. 答案存回 `wiki/outputs/`（运行 `python3 shared/scripts/wiki-query.py <slug> "<title>" <answer>`）

### Ingest 自动化
当 `shared/knowledge/raw/` 中有新素材时：
1. 读取素材内容
2. 选择页面类型（concept | entity | source）
3. 使用 `shared/knowledge/templates/{type}.md` 创建 wiki 页面（含 YAML frontmatter + [[wikilinks]]）
4. 更新 `wiki/index.md` 和 `wiki/log.md`
5. 或直接运行：`python3 shared/scripts/wiki-ingest.py <raw-file> --type <type>`

### Lint 定时巡检
每周一运行健康检查：
```bash
python3 ~/agentic-os-collective/shared/scripts/wiki-lint.py
```
检查项：孤儿页面、断链、缺失 frontmatter、内容冲突、高频引用但未成页

### 命名约定
| 类型 | 格式 | 示例 |
|------|------|------|
| Python模块 | `snake_case.py` | `download_server.py` |
| 配置文件 | `snake_case.yaml` | `tk_pipeline.yaml` |
| Skill目录 | `skill-name/` | `water-margin-drama/` |
| Wiki页面 | `kebab-case.md` | `active-inference.md` |

### 依赖关系
- 所有核心模块强依赖 `shared/mcp_task_server.py`
- 外部依赖：OpenClaw, GPT-SoVITS, Replicate, 飞书API
- 配音依赖：GPT-SoVITS V3+ 模型权重

### 已知问题
1. drama/tk 架构重复，共用代码可提取到 shared/
2. SOP文档缺失如 TK-OPERATION-SOP.md

### 模型路由
| 场景 | 模型 | 说明 |
|------|------|------|
| 默认 | `ollama/llama3.2:3b` | 本地快速 |
| 备选 | `deepseek/deepseek-v4-flash` | 直连api.deepseek.com |
| 复杂 | `aliyun/qwen3.6-plus` | CODING计划免费额度 |
| 代码 | `aliyun/qwen3-coder-plus` | CODING计划 |

## 会话归档（Clicky/CPR 理念）

每次会话结束时（或用户说"结束"、"归档"、"保存"时）执行：

```bash
bash ~/agentic-os-collective/scripts/archive-session.sh
```

这将：
1. 提取本次会话的关键决策和主题
2. 结构化日志写入 `shared/knowledge/wiki/log.md`
3. 完整归档保存到 `wiki/outputs/session-{timestamp}.md`
4. 更新 `wiki/index.md` 索引
5. 追加到 `workspace/memory/timeline.md`

在回答中如涉及重要决策，使用 `[[wikilinks]]` 格式标注，便于知识库链接。
