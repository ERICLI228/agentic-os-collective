# 🎬 水浒传AI数字短剧 - 增强版自动制作系统

> 一句话启动 | 行业级工作流 | 合规优先 | 音视频全链路

> **⚠️ 诚实标注（2026-04-24 v3.3修订）**：总体完成度约 **45%**（↑35%）
> - 剧本生成 ✅ 65% | 争议改写 ⚠️ 30% (GLM直连修复) | 角色设计 ⚠️ 25% (API已接入)
> - 分镜视频 ✅ 70% | 配音合成 ⚠️ 35% (多角色TTS可用) | 自动发布 ⚠️ 15% (dev模式)
> - 🆕 AI质量自评 ✅ 50% (quality_assessor.py) | 🆕 审核面板 ✅ ReviewPanel.vue

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

- 2026-04-24 v3.3: 诚实修订，标注真实完成度 35%，调整 P0/P1/P2 优先级，明确搁置事项
- 2026-04-09 v2.1: 新增TTS配音 + FFmpeg合成
- 2026-04-09 v2.0: 增强工作流 + 合规检查
- 2026-04-09 v1.0: 初始版本

---

## 🚧 P0/P1/P2 优先级（v3.3）

### P0 本周（止血优先，约18小时）
1. 修复 TK 命令路由 Bug（skill_loader 拦截跨业务线调度）
2. 写 daily_business_summary.py（GMV/订单/库存/达人简报飞书推送）
3. 手动辅助跑通短剧第 1 集（Seedance 2.0 + MiniMax TTS + FFmpeg → 可播放 MP4）
4. 增强审核面板（剧本全文+分镜缩略图+配音试听+通过/修改/驳回）
5. 开通 TikTok 达人联盟（15% 佣金，首批 10 个达人）

### P1 本月（约40小时）
1. 店小秘 ERP API 对接
2. 实现 role_designer.py（Seedance/AutoGLM 角色定妆照）
3. 实现 audio_generator.py（ElevenLabs 主角 + MiniMax 配角）
4. AI 质量自评节点 MS-4.5
5. 视觉圣经基础版（三视图+调色板+道具图）

### P2 次月
1. 达人 CRM 基础版
2. 早期爆款预测模型（前 4h 数据）
3. 完播率追踪
4. 3PL 物流对接

### 搁置事项（不要求代码实现）
- GSTACK 专家团队调度器（仅保留 RACI 矩阵）
- 自进化机制（数据不足，无限搁置）
- 第三条业务线（现有两条未跑通）
- ORM 迁移（SQLite 已足够）
- 完整单元测试套件（等流水线稳定后补）

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

*版本: v3.3 诚实修订版 | 2026-04-24*