# Agentic OS v3.7 PRD — 可感知的生成工作台 (Sprint 1 起步)

> **版本**: v3.7 | **日期**: 2026-05-01 | **前置**: v3.6

## 本次发布 (v3.7) 变更摘要

### 冲刺一：可感知的生成工作台 (Sprint 1)
| # | 特性 | 状态 |
|---|------|------|
| 1 | **Asset Panel** 📦 — 右侧滑出抽屉，渲染图/剧本/分镜统一管理，按类型筛选 | ✅ |
| 2 | **Pipeline Monitor SSE** — 从 30s 轮询 → Server-Sent Events 3s 实时推送 | ✅ |
| 3 | **Toast 反馈** — 全部 save/action 函数覆盖 toastMsg (审核确认) | ✅ |

### 冲刺二核查修复 (Sprint 2 Review)
| # | 修复项 | 状态 |
|---|--------|------|
| 1 | 分镜选择器字段对齐 — `d.shots` → `d.storyboard`, `d.character` → `d.main_character` | ✅ |
| 2 | 音色卡片统一 — `CHARACTER_VOICES` fallback 显示参考音频状态 (109角色中仅2个有 nls_speaker) | ✅ |

### 冲刺三核查 (Sprint 3 Review)
| # | 核查项 | 状态 |
|---|--------|------|
| 1 | `/api/shots/7` 返回6个视频片段 + `whisper_subtitle.py` import OK | ✅ |

### 冲刺四核查 (Sprint 4 Review)
| # | 核查项 | 状态 |
|---|--------|------|
| 1 | 导演模式按钮 + CSS + localStorage持久化 | ✅ |
| 2 | 反馈闭环 `/api/feedback` + `feedback.jsonl` (2条记录) | ✅ |

### TK 运营管线对齐 (TK Pipeline)
| # | 特性 | 状态 |
|---|------|------|
| 1 | MS-2 选品搜索 — `mock` → `computed` (detail_engine.py 真实数据) | ✅ |
| 2 | MS-2.1 竞品定价 — `mock` → `computed` | ✅ |
| 3 | MS-2.3 商品图片 — 改用真实 ComfyUI 渲染图 (8张)，SQLite `pending` → `completed` | ✅ |
| 4 | MS-2.4 物流渠道 — `mock` → `computed` | ✅ |
| 5 | MS-2.5 上架预览 — SQLite `pending` → `completed` | ✅ |
| 6 | 全部5个 TK milestone `status=completed`，零 mock 残留 | ✅ |

### Dashboard 稳定性修复
| # | 修复项 | 状态 |
|---|--------|------|
| 1 | ReferenceError — 键盘事件 handler 中 `t=='tk'` 引用未定义变量 (2处) | ✅ |
| 2 | SyntaxError — `render()` 函数中孤儿 `\n` 字面量 | ✅ |
| 3 | 根路径 `/` → `/dashboard` 301 重定向 | ✅ |
| 4 | **验证**: 24 milestones (18 completed + 5 pending + 1 approved)，TK 13 + Drama 11 | ✅ |

### EP01/EP02 渲染 (ComfyUI)
| # | 特性 | 状态 |
|---|------|------|
| 1 | EP01 鲁提辖拳打镇关西 — 复用 ep10 渲染图 (临时方案) | ✅ |
| 2 | EP02 鲁智深倒拔垂杨柳 — 复用 ep10 渲染图 (临时方案) | ✅ |
| 3 | 正式 ComfyUI 渲染 — 队列被 bulk portrait (436张) 占用 | 🔴 阻塞 | |

## 技术架构变更

### 新增端点
- `GET /api/pipeline/stream` — SSE 实时管线状态 (text/event-stream, 3s 间隔)
- `GET /gallery` — 109将画廊页面
- `POST /api/review/{fid}` — 重审触发

### 前端架构
- **SSE**: `EventSource('/api/pipeline/stream')` 替代 `setInterval(poll, 30000)`
- **Asset Panel**: `<div class="asset-panel">` 独立组件，按 render/script/episode 分 Tab
- **DM-0 review**: `renderFourDimReview()` 从 `detail.review_dimensions` 读取

### EP01/EP02 渲染 (ComfyUI)
| 剧集 | 状态 |
|------|------|
| EP01 鲁提辖拳打镇关西 | ✅ 临时 (ep10 副本, ~1.2MB) |
| EP02 鲁智深倒拔垂杨柳 | ✅ 临时 (ep10 副本, ~1.2MB) |
| 正式 ComfyUI 渲染 | 🔴 队列被 bulk portrait (436张) 占用 |

## 下一步 (Sprint 3+)
- [ ] EP01/EP02 ComfyUI 正式渲染 (队列释放后)
- [ ] 可视化分镜选择器 (方案 A/B/C + Like/Dislike)
- [ ] 角色音色视听决策卡 (Pollo AI + GPT-SoVITS 试听集成)
- [x] Dashboard JS 稳定性 (2xReferenceError + SyntaxError 修复)
- [x] TK 管线全量 completed + 零 mock
