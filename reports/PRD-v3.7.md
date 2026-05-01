# Agentic OS v3.7 PRD — 可感知的生成工作台 (Sprint 1 起步)

> **版本**: v3.7 | **日期**: 2026-05-01 | **前置**: v3.6

## 本次发布 (v3.7) 变更摘要

### 冲刺一：可感知的生成工作台
| # | 特性 | 状态 |
|---|------|------|
| 1 | **Asset Panel** 📦 — 右侧滑出抽屉，渲染图/剧本/分镜统一管理，按类型筛选 | ✅ |
| 2 | **Pipeline Monitor SSE** — 从 30s 轮询 → Server-Sent Events 3s 实时推送 | ✅ |
| 3 | **Toast 反馈** — 全部 save/action 函数覆盖 toastMsg (审核确认) | ✅ |

### 预冲刺体验修复
| # | 修复项 | 状态 |
|---|--------|------|
| 1 | DM-0 四维度审核明细 — 后端 `review_dimensions` → 前端正确读取展示 | ✅ |
| 2 | 音色卡片统一 — `CHARACTER_VOICES` fallback 显示参考音频状态 | ✅ |
| 3 | reReviewDM0 按钮修复 — `/api/review/{fid}` POST 端点已就绪 | ✅ |

### 资产层
| # | 特性 | 状态 |
|---|------|------|
| 4 | 109 演员全量写入 visual_bible.json | ✅ |
| 5 | prompt_en + video_prompts 全部重写 (98版演员面容) | ✅ |
| 6 | 109将画廊 (/gallery) — 筛选/搜索/排序/懒加载 | ✅ |
| 7 | SFX 混音集成 — merge_to_final 优先使用 final_with_sfx.aac | ✅ |
| 8 | DM-1 加载卡死修复 — videoPrompts 膨胀 3-4x | ✅ |
| 9 | ComfyUI 中文目录修复 — EP07/09/10 渲染图 2.0M (vs 250KB Pillow) | ✅ |

## 技术架构变更

### 新增端点
- `GET /api/pipeline/stream` — SSE 实时管线状态 (text/event-stream, 3s 间隔)
- `GET /gallery` — 109将画廊页面
- `POST /api/review/{fid}` — 重审触发

### 前端架构
- **SSE**: `EventSource('/api/pipeline/stream')` 替代 `setInterval(poll, 30000)`
- **Asset Panel**: `<div class="asset-panel">` 独立组件，按 render/script/episode 分 Tab
- **DM-0 review**: `renderFourDimReview()` 从 `detail.review_dimensions` 读取

### 管线恢复状态
| 剧集 | ComfyUI 渲染 | 状态 |
|------|-------------|------|
| EP07 武松打虎 | ep07_shot_01~03.png ✅ | 2.0M |
| EP08 武松斗杀西门庆 | ep08_shot_01~03.png ✅ | 2.0M |
| EP09 林冲雪夜上梁山 | ep09_shot_01~03.png ✅ | 2.0M |
| EP10 花和尚大闹五台山 | ep10_shot_01~03.png ✅ | 2.0M |
| EP01 鲁提辖拳打镇关西 | ep01_shot_*.png ❌ | Pillow fallback |
| EP02 鲁智深倒拔垂杨柳 | ep02_shot_*.png ❌ | Pillow fallback |

## 下一步 (Sprint 2)
- [ ] 可视化分镜选择器 (方案 A/B/C + Like/Dislike)
- [ ] 角色音色视听决策卡 (Pollo AI + GPT-SoVITS 试听集成)
- [ ] EP01/EP02 ComfyUI 渲染图补跑
