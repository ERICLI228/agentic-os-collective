---
title: "Agentic OS v3.6 架构实体"
type: entity
date: 2026-04-30
version: v3.6.1
tags: [architecture, flask, comfyui, pipeline, dashboard]
related: [[miaoshou-erp-api]]
status: active

# Agentic OS v3.6 架构实体

## 双业务线

- **TK 运营自动化** (13 里程碑): MS-1~MS-4, 商品上架/定价/物流/合规/发布
- **AI 数字短剧制造流水线** (11 里程碑): DM-0~DM-10, 剧本/角色/渲染/配音/合成/发布

## 核心服务

| 服务 | 端口 | 技术栈 |
|------|------|--------|
| task_wizard.py (Flask) | :5001 | Flask + YAML + Pillow + rembg |
| ComfyUI SDXL | :8188 | SDXL 1.0 → M2 Max 38-GPU |
| SQLite | ~/.agentic-os/pipeline.db | orders + fulfillment_events |

## API 端点 (30个)

- 剧本: /api/script, /api/script/<ep>, /api/script/<ep>/export
- 角色: /api/character/<name> (CN+PY双通), /api/render/<char>/<file>
- 图片: /api/images, /api/images/<id>, /api/images/<id>/process (rembg/full/check/push_erp)
- 下载: /api/download?name=ep01.txt
- 决策: /api/decision, /api/detail/<ms_id>, /api/dashboard
- 信息: /api/info/items (139 items)
- 页面: /dashboard (v3.6 smart routing), /info

## 管线产出 (EP01-06)

| 集数 | 标题 | 角色 | 大小 | 渲染数 |
|------|------|------|------|--------|
| EP01 | 鲁提辖拳打镇关西 | 鲁智深 | 2.3MB | 3 |
| EP02 | 鲁智深倒拔垂杨柳 | 鲁智深 | 2.3MB | 3 |
| EP03 | 林冲风雪山神庙 | 林冲 | 2.0MB | 3 |
| EP04 | 宋江怒杀阎婆惜 | 宋江 | 1.9MB | 3 |
| EP05 | 杨志卖刀 | 杨志 | 2.0MB | 3 |
| EP06 | 智取生辰纲 | 晁盖 | 1.8MB | 3 |

## 关键文件

| 文件 | 行数 | 说明 |
|------|------|------|
| shared/task_wizard.py | 739 | Flask主服务·30端点 |
| shared/detail_engine.py | 817 | 14里程碑·DM-V/F/10 |
| shared/script_manager.py | 435 | 剧本/故事板/导出 |
| shared/comfyui_renderer.py | 215 | SDXL渲染器 |
| shared/core/image_processor.py | 289 | rembg/resize/ERP |
| shared/core/tk_pipeline_db.py | 441 | 订单+履约事件 |
| dashboard/task_board.html | 790 | smart routing |

## QA 测试

**80/80 PASS** — 全部端点 + 全部边界条件 (404/400) + 全部文件 (管线+渲染+ERP)

## 待决策事项

- MIAOSHOW_PUBLISH_ENABLED=false (需用户开启)
- Kling 视频升级 (¥15/EP, 微信支付)
- 紫鸟达人联盟 (手动操作)
- 5国字幕 + 环境音效 (管线已就绪)
