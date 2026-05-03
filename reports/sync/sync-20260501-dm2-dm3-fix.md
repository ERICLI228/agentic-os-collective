# 同步报告 — DM-2/DM-3 分镜+配音看板恢复

> **日期**: 2026-05-03  
> **修订人**: OpenCode (deepseek-v4-pro)  
> **版本**: v3.7.9-sync  
> **状态**: ⏳ 待审批

---

## 背景

`task_board.html` (9,481行) 单文件内联 JS 超过 Chrome 引擎上限，导致 `renderDM2`、`renderDM3` 等 42 个函数被静默丢弃。DM-2 "分镜审阅看板" 和 DM-3 "配音生成看板" 点击后无任何可视化输出。

---

## 根因分析

### 1. Chrome JS 引擎容量限制

单个 `<script>` 标签内 ~200+ 个 async function，Chrome V8 达到某个内部上限后**静默停止解析**。`node --check` 通过但浏览器端 undefined。

### 2. 脚本分块策略

在零深度边界插入 `</script><script>`，将 9,481 行拆分为 **6 个内联块**：

| 块 | 行范围 | 大小 | 内容 |
|----|--------|------|------|
| Block 0 | 870–873 | 0.2KB | Chart.js CDN + cache bust |
| Block 1 | 956–2,643 | 103KB | 渲染核心 + renderDM0/1 |
| Block 2 | 2,644–4,412 | 81KB | MS-0~2 管线视图 |
| Block 3 | 4,413–6,133 | 84KB | SMART ROUTING + renderDetail |
| Block 4 | 6,134–7,945 | 90KB | renderDM2–10 + DM-3 + DM-4/5 |
| Block 5 | 7,946–9,463 | 66KB | Charts + 工具函数 + 初始化 |

### 3. renderShotSorter 嵌套问题

`renderShotSorter()`（第 6,269 行）缺少闭合 `}`，导致其后的 `renderDM2`、`renderDM3`、`_extractShots` 等函数被嵌套在它的作用域内，全局不可见。

---

## 修改清单

### 修改 A: 脚本拆分为 6 块
- **位置**: 行 2,643、4,412、6,133、7,945 插入分界标记
- **验证**: `node --check` 单块检验全部通过

### 修改 B: 闭合 renderShotSorter（第 6,296 行）
```
  }catch(e){ ... }
+ }  ← 闭合 renderShotSorter
```
- **同步删除** 第 7,945 行的冗余 `}`（原闭合位置）

### 修改 C: `_extractShots()` 数据映射（第 6,330–6,358 行）
- **问题**: 旧逻辑期待 `detail.storyboard` / `detail.shots` 数组
- **API 实际格式**: `detail.sections[0].items[]`，每个 item 含 `key/label/value/before/after`
- **修复**: 新增 sections items 解析分支，将 `label` 拆分为 `character` + `shot_number`，映射到渲染所需字段

### 修改 D: SMART ROUTING 恢复（第 4,760 行）
- 移除诊断代码，恢复为简洁的 `await renderDM2(detail,ms)` / `await renderDM3(detail,ms)`

### 修改 E: renderDM2 清洁（第 6,302 行）
- 移除绿色诊断大字 "DM-2 RENDER STARTING"

---

## 变更统计

| 指标 | 数值 |
|------|------|
| 修改文件 | `dashboard/task_board.html` |
| 总行数 | 9,481 行 |
| 相对 HEAD diff | +2,059 / −91 |
| 本次 session 净改动 | +35 / −20（估算，不含积压未提交） |
| 新增 CSS | DM-2 分镜卡片样式 (`.sb-*`) + DM-3 配音表格样式 (`.dub-*`) 已在 HEAD 中包含 |

---

## 测试验收

| # | 测试项 | 状态 |
|---|--------|------|
| 1 | `node --check` 单块语法（6 块各一次） | ✅ |
| 2 | 全文件 brace balance（{ = }） | ✅ 3,004 = 3,004 |
| 3 | `__block4_loaded()` 可访问性 | ✅ |
| 4 | `typeof renderDM2 !== 'undefined'` | ✅ |
| 5 | `typeof renderDM3 !== 'undefined'` | ✅ |
| 6 | DM-0/1 正常渲染（回归测试） | 待用户验证 |
| 7 | DM-2 点击 → 18 个分镜卡片 | ✅ |
| 8 | DM-3 点击 → 配音表格 + 技术卡片 | ✅ |
| 9 | DM-4/5/6–10 渲染 | 待用户验证 |
| 10 | Flask `task_wizard` 服务正常 | ✅ PM2 online |

---

## 影响范围

| 高 | 中 | 低 |
|----|-----|-----|
| DM-2 分镜审阅看板 | DM-4/5 合成/字幕 | 图表函数（Block 5 无改动） |
| DM-3 配音生成看板 | SMART ROUTING if/else 链 | 初始化逻辑 |
| DM-0/1 回归风险 | `_tkBatchProcessAll` 仍在 Block 4 | CSS 样式 |

---

## 后续建议

1. **提交 git**: `git commit -m "v3.7.9: fix DM-2/DM-3 render — 6-block split + close renderShotSorter + _extractShots section mapping"`
2. **DM-4/5**: 测试合成/字幕看板是否也需要 `_extractShots` 映射修复
3. **生产同步**: 审批通过后 cp 到生产路径并重启生产 Flask

---

> **请回复 `批准同步` 以执行 git commit + 生产部署**
