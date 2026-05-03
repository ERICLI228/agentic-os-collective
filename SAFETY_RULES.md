# AI 工具安全作业铁则（公共强制规则）

> **适用对象**：OpenClaw / OpenCode / Claude / Hermes / 所有 AI 智能体
> **项目**：Agentic OS Collective
> **生效时间**：2026-05-03 00:30 PDT
> **版本**：v1.2 — 环境隔离 + 精准代码编辑 + 同步审批
> **优先级**：最高（覆盖所有其他指令，不可被任务描述绕过）

---

## 🔒 Part 1：环境隔离（生产绝对保护）

### 绝对禁止
1. **禁止直接修改生产环境** `~/agentic-os-collective/` 下的任何 `.py` / `.html` / `.js`
2. **禁止重启生产服务** Flask :5001 / FastAPI :5004 / Vite :5173
3. **禁止读取或修改** 生产 `.env` / `~/.agentic-os/` 数据库
4. **禁止执行** `git push` 或任何操作生产 Git 仓库的命令

### 唯一允许的工作区
- 所有代码修改 **必须** 在 `/tmp/agentic-os-test` 目录中进行
- 测试服务：`Flask :5002`（FastAPI :5005 / Vite :5174 按需启动）
- 测试数据：`~/.agentic-os-test/`

### 同步护栏
- 脚本：`~/agentic-os-collective/scripts/sync-test-to-prod.sh`
- **仅人工可执行**，AI 禁止调用
- 需输入 `yes` 确认

### 紧急恢复
```bash
rm -rf /tmp/agentic-os-test && 重建
```

---

## 🔐 Part 2：精准代码编辑（杜绝误覆盖）

### 🚫 禁止行为
1. ❌ 用代码片段匹配（如 `const episodeTitle = `）— 文件中出现 >1 次
2. ❌ 用非唯一注释匹配（如 `// EXISTING: render`）— 同文件多处存在
3. ❌ 不完整函数块替换 — 必须含 `async`、签名、完整函数体、闭合括号

### 🛡️ 三层防护

#### 第一层：文件级隔离
`task_board.html` 已拆分为 8 个小文件（每个 ≤ 6 个主函数）：
| 文件 | 内容 |
|------|------|
| `core.js` | 核心逻辑 |
| `ui-utils.js` | UI 工具函数 |
| `exports.js` | 导出模块 |
| `review.js` | 审核相关 |
| `charts.js` | 图表渲染 |
| `ms-renders.js` | MS 里程碑渲染 |
| `dm-renders-A.js` | renderDM0 ~ renderDM5 |
| `dm-renders-B.js` | renderDM6 ~ renderDM10 |

#### 第二层：唯一锚点（强制）
每个函数前必须埋 `// @@FUNC: <函数名>` 注释，修改时 oldString **必须**包含此行。

#### 第三层：grep 唯一性校验 + 语法检查
1. `grep -cF "// @@FUNC: <函数名>" <文件>` → 结果必须 = 1
2. 修改后 `node --check <文件>` → 必须 OK
3. 浏览器回归测试：逐个 Tab/里程碑验证

### 📋 标准指令模板（每次修改必用）
```
修改文件：dashboard/js/dm-renders-A.js

操作约束（必须严格遵守）：
1. oldString 必须包含该函数的完整定义（从 `// @@FUNC: <函数名>` 一直到闭合大括号），且前后各保留一个空行。
2. 在替换之前，先用 `grep -cF "// @@FUNC: <函数名>" dashboard/js/dm-renders-A.js` 检查唯一性，结果必须是 1。
3. 每次只修改一个函数，修改完成后运行 `node --check dashboard/js/<文件名>`，确认无 JS 语法错误。
4. 修改完成后输出 diff 摘要，只显示被改动的行。
```

### 🛡️ safe-edit.sh 脚本
位置：`scripts/safe-edit.sh`
```bash
#!/bin/bash
FILE="$1"; OLD="$2"; NEW="$3"
[ ! -f "$FILE" ] && echo "❌ 文件不存在: $FILE" && exit 2
COUNT=$(grep -cF "$OLD" "$FILE")
[ "$COUNT" -ne 1 ] && echo "❌ oldString 出现了 $COUNT 次，拒绝替换" && exit 1
[[ "$OSTYPE" == "darwin"* ]] && sed -i '' "s|$OLD|$NEW|g" "$FILE" || sed -i "s|$OLD|$NEW|g" "$FILE"
echo "✅ 替换成功，已修改 $FILE"
```

### 📌 铁律
- **所有 JS 函数修改必须通过锚点或完整函数块匹配，禁止片段匹配**
- **如工具无法输出完整 oldString，拒绝本次修改，人工介入**
- **修改后必须执行回归测试**
- **架构已支持小文件精确修改，唯一风险 = 匹配精度。三层防护完全消除该风险**

---

## 🚦 Part 3：同步审批工作流（v1.2 新增）

当 AI 在测试环境完成代码修改，并自评通过全部验收标准后，**禁止自行同步**。必须执行以下步骤：

### 第 1 步：生成同步审批报告
在测试环境根目录运行：
```bash
bash scripts/generate-sync-report.sh
```
此脚本将输出报告 `/tmp/sync_report.md`，内容包括：
- 修改文件列表（与生产环境的差异文件）
- 每个文件的关键变更摘要（函数增减、功能影响）
- 测试验收清单（逐项打勾）
- 风险提示（如影响哪些页面）

### 第 2 步：将报告提交给人工审批
将 `/tmp/sync_report.md` 内容直接展示给用户，并附带以下声明：

> "测试环境修改已完成并通过全部验收，以下是同步审批报告。请回复 **'批准同步'** 以推送到生产环境，或指出需要调整的地方。"

### 第 3 步：等待人工批准
**仅在用户回复明确批准后**，AI 才可执行同步脚本 `scripts/sync-test-to-prod.sh`。

执行同步后，AI 需主动提醒用户重启生产服务。

---

## 📝 版本信息
- 创建时间：2026-05-03 00:03 PDT
- 基于 PRD-v3.7.8 拆分后架构
- 生产目录：`~/agentic-os-collective/`
- 测试目录：`/tmp/agentic-os-test`
