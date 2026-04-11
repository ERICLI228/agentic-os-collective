# 水浒传AI数字短剧 - 能力文档

## 概述

本系统为OpenClaw平台提供 **一键式AI短剧制作** 能力，基于水浒传IP生成自动化短视频。

## 能力清单

### ✅ 已集成能力

| 能力 | 模型 | 位置 | 状态 |
|------|------|------|------|
| 剧本生成 | GLM-4-7 | volcengine | 可用 |
| 视频生成 | Seedance 2.0 | volcengine | 可用 |
| 视频存储 | TOS | volcengine | 可用 |
| 自动化脚本 | make-drama.sh | water-margin-drama/ | 可用 |

### ⏳ 待集成能力

| 能力 | 状态 |
|------|------|
| TTS配音 | 待开发 |
| FFmpeg合成 | 待开发 |
| 批量生成 | 待开发 |

## 使用方式

### 一句话指令
```
帮我制作一集"鲁智深倒拔垂杨柳"AI短剧
```

### 命令行
```bash
# 一键生成
~/.openclaw/skills/water-margin-drama/make-drama.sh "鲁智深倒拔垂杨柳"

# 指定参数
~/.openclaw/skills/water-margin-drama/make-drama.sh "武松打虎" "9:16" "10"
```

## 技术栈

- **底层模型**: 火山引擎 ARK API
- **视频生成**: Seedance 2.0 Fast
- **大语言模型**: GLM-4-7 (免费额度)
- **存储**: TOS 对象存储 (10GB免费)

## 资源配额

| 资源 | 额度 | 有效期 |
|------|------|--------|
| GLM-4.7 推理 | 免费 | 长期 |
| Seedance 2.0 | 500万tokens | 长期 |
| TOS 存储 | 10GB | 6个月 |
| TOS 流量 | 10GB | 6个月 |

## 备份信息

- 本地备份: `~/Backups/OpenClaw-capabilities/20260409/`
- 配置文件: `~/.openclaw/openclaw.json`
- Skills: `~/.openclaw/skills/water-margin-drama/`

## 更新日志

- 2026-04-09: 初始版本，集成GLM-4.7 + Seedance 2.0