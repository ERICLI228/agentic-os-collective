# 🎬 水浒传AI数字短剧 - 增强版自动制作系统

> 一句话启动 | 行业级工作流 | 合规优先 | 音视频全链路

## 🚀 一句话指令

```
帮我制作一集"武松打虎"AI短剧
```

或指定参数：
```
生成30秒的鲁智深倒拔垂杨柳，竖屏9:16，幽默风格，需要配音
```

---

## 📋 完整工作流 (7阶段)

| 阶段 | 任务 | 模型/工具 | 状态 |
|------|------|-----------|------|
| 1️⃣ | 剧本生成 | GLM-4.7 | ✅ |
| 2️⃣ | **人工审核** | 推送飞书 | ✅ |
| 3️⃣ | 分镜优化 | GLM-4.7 | ✅ |
| 4️⃣ | 视频生成 | Seedance 2.0 | ✅ |
| 5️⃣ | **配音合成** | TTS + FFmpeg | ✅ 新 |
| 6️⃣ | 背景音乐 | FFmpeg混音 | ✅ 新 |
| 7️⃣ | 上传TOS | 自动 | ✅ |

---

## 🎤 TTS配音方案

### 免费方案 (已集成)
- **macOS Say**: 使用系统内置语音
- 中文语音: Ting-Ting (婷婷), Eddy, Mei-Jia 等
- 用法: `--tts "文字内容"`

### 付费方案 (可选)
- ElevenLabs: 更自然的人声
- 需要API Key配置

---

## 🎵 FFmpeg合成功能

### 已实现
| 功能 | 命令 | 说明 |
|------|------|------|
| 音视频合并 | `--merge video.mp4 audio.m4a` | 替换原音频 |
| 背景音乐混音 | `--mix video.mp4 bgm.mp3` | 混合两路音频 |
| 完整流水线 | `--full video_url script output` | 一键完成 |

---

## 📖 使用示例

### 方式1: 一句话全自动化 (带配音)
```
请帮我完成"鲁智深倒拔垂杨柳"的AI短剧制作，需要配音
```

### 方式2: 分步执行
```
/script 武松打虎         → 生成剧本
/video 武松打虎         → 生成视频
/tts "武松来到景阳冈..." → 生成配音
/merge                  → 合成最终视频
```

### 方式3: 命令行
```bash
# 生成配音
python3 drama_audio.py --tts "鲁智深倒拔垂杨柳"

# 合并音视频
python3 drama_audio.py --merge 视频.mp4 配音.m4a

# 完整流水线
python3 drama_audio.py --full "视频URL" "配音文字" "输出名称"
```

---

## ⚖️ 合规规则

### 🔴 禁止内容
- 歪曲原著、低俗恶搞、血腥暴力

### 🟡 需改写
- 宋江招安、李逵滥杀、女性角色

### 详见: `compliance-check.md`

---

## 🎭 角色设计

### 核心角色提示词
详见: `role-prompts.md`

---

## 📁 文件结构

```
~/.openclaw/skills/water-margin-drama/
├── SKILL.md              # 本文档
├── make-drama.sh         # 视频生成脚本
├── drama_audio.py        # 音视频合成 (新)
├── role-prompts.md       # 角色提示词
├── compliance-check.md   # 合规清单
├── temp/                 # 临时文件
└── output/               # 输出文件
```

---

## ⚙️ 配置

- GLM-4.7: `glm-4-7-251222`
- Seedance 2.0: `doubao-seedance-2-0-fast-260128`
- ARK_API_KEY: 已配置

---

## 🔄 更新日志

- 2026-04-09 v2.1: 新增TTS配音 + FFmpeg合成
- 2026-04-09 v2.0: 增强工作流 + 合规检查
- 2026-04-09 v1.0: 初始版本

---

## 🔄 任务驱动工作流 (基于 auto-coding-agent-demo)

### task.json 任务清单

```bash
# 查看任务列表
cat task.json | jq '.tasks[] | {id, title, passes}'
```

| 任务ID | 名称 | 状态 |
|--------|------|------|
| 1 | 剧本生成 | ⏳ |
| 2 | 人工审核 | ⏳ (阻塞) |
| 3 | 角色设计 | ⏳ |
| 4 | 分镜优化 | ⏳ |
| 5 | 视频生成 | ⏳ (阻塞) |
| 6 | TTS配音 | ⏳ |
| 7 | 音视频合成 | ⏳ |
| 8 | 上传TOS | ⏳ (阻塞) |
| 9 | 飞书通知 | ⏳ |

### 确认机制

```bash
# 开始新项目
python3 confirmation.py start "武松打虎"

# 确认各阶段
python3 confirmation.py script "人工审核通过"
python3 confirmation.py roles "角色设计OK"
python3 confirmation.py video "视频确认"

# 检查状态
python3 confirmation.py

# 检查是否可以进入某阶段
python3 confirmation.py check video
```

### 阻塞处理

当任务阻塞时，系统会：
1. 停止当前任务
2. 输出阻塞信息
3. 等待人工介入

详见 `CLAUDE.md`

---

*基于 auto-coding-agent-demo 最佳实践*

*版本: v2.2.0 | 2026-04-10*