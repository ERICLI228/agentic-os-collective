<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:5004'

const props = defineProps({
  taskId: { type: String, required: true },
  milestoneId: { type: String, default: '' },
  decisionPoint: { type: Object, default: null },
  outputContent: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['resolved', 'close'])

// 决策状态
const decisionType = ref('')
const comment = ref('')
const submitting = ref(false)
const result = ref(null)
const errorMsg = ref('')

// 审核内容
const activeTab = ref('script') // script | shots | audio | score

const scriptText = computed(() => {
  const d = props.outputContent?.data || {}
  return d.script || d.full_script || d.content || ''
})

const shots = computed(() => {
  const d = props.outputContent?.data || {}
  return d.shots || d.storyboard || d.scenes || []
})

const audioSamples = computed(() => {
  const d = props.outputContent?.data || {}
  return d.audio_samples || d.voice_samples || d.audio || []
})

const durationInfo = computed(() => {
  const d = props.outputContent?.data || {}
  return d.duration || d.duration_estimate || { total: null, scenes: [] }
})

const aiScore = computed(() => {
  const d = props.outputContent?.data || {}
  return d.ai_score || d.quality_score || d.score || null
})

const scriptMeta = computed(() => {
  const d = props.outputContent?.data || {}
  return {
    wordCount: d.word_count || (scriptText.value?.length || 0),
    version: d.version || 'v1',
    generator: d.generated_by || d.generator || 'AI',
    style: d.style || d.visual_style || 'default'
  }
})

const totalDuration = computed(() => {
  const d = durationInfo.value
  if (typeof d === 'string') return d
  if (typeof d.total === 'number') return `${d.total}s`
  const scenes = d.scenes || []
  if (scenes.length > 0) {
    const total = scenes.reduce((sum, s) => sum + (s.duration || s.seconds || 0), 0)
    return `${total}s`
  }
  return '待估算'
})

const scoreColor = (val) => {
  if (val >= 8) return '#4caf50'
  if (val >= 6) return '#ff9800'
  return '#f44336'
}

async function submitDecision(type) {
  if (submitting.value) return
  submitting.value = true
  errorMsg.value = ''
  result.value = null

  try {
    const payload = {
      task_id: props.taskId,
      milestone_id: props.milestoneId,
      decision_type: type === 'approve' ? 'approve' : type === 'reject' ? 'reject' : 'modify',
      comment: comment.value
    }
    const res = await axios.post(`${API_BASE}/api/decision/submit`, payload)

    if (type === 'modify' && comment.value) {
      await axios.post(`${API_BASE}/api/decision/retry`, {
        task_id: props.taskId,
        milestone_id: props.milestoneId,
        comment: comment.value
      })
    }

    result.value = type
    emit('resolved', { type, comment: comment.value })
    setTimeout(() => emit('close'), 1500)
  } catch (e) {
    errorMsg.value = e.response?.data?.error || e.message
  } finally {
    submitting.value = false
  }
}

const typeLabel = { approve: '通过', modify: '修改', reject: '驳回' }
</script>

<template>
  <div class="review-panel">
    <!-- Header -->
    <div class="review-header">
      <div class="review-title">
        <span class="review-icon">🎬</span>
        <span>剧本审核</span>
      </div>
      <button class="close-btn" @click="$emit('close')">✕</button>
    </div>

    <!-- Tab Bar -->
    <div class="tab-bar">
      <button :class="{ active: activeTab === 'script' }" @click="activeTab = 'script'">📄 完整剧本</button>
      <button :class="{ active: activeTab === 'shots' }" @click="activeTab = 'shots'">🎬 分镜预览</button>
      <button :class="{ active: activeTab === 'audio' }" @click="activeTab = 'audio'">🎤 配音试听</button>
      <button :class="{ active: activeTab === 'score' }" @click="activeTab = 'score'">📊 AI评分</button>
    </div>

    <!-- Tab Content -->
    <div class="review-content">
      <!-- Script Tab -->
      <div v-if="activeTab === 'script'" class="tab-content">
        <div class="script-meta-bar">
          <span>字数: {{ scriptMeta.wordCount.toLocaleString() }}</span>
          <span>版本: {{ scriptMeta.version }}</span>
          <span>生成: {{ scriptMeta.generator }}</span>
          <span>风格: {{ scriptMeta.style }}</span>
        </div>
        <div class="script-body" v-if="scriptText">
          <div v-for="(scene, i) in scriptText.split('\n\n').filter(Boolean)" :key="i" class="scene-block">
            <div class="scene-header">🎞️ 场景 {{ i + 1 }}</div>
            <div class="scene-text">{{ scene }}</div>
          </div>
        </div>
        <div v-else class="empty-state">暂无剧本内容</div>
      </div>

      <!-- Shots Tab -->
      <div v-if="activeTab === 'shots'" class="tab-content">
        <div class="shots-grid" v-if="shots.length > 0">
          <div v-for="(shot, i) in shots" :key="i" class="shot-card">
            <div class="shot-number">{{ i + 1 }}</div>
            <img v-if="shot.url || shot.preview" :src="shot.url || shot.preview" :alt="`Shot ${i + 1}`" class="shot-img" />
            <div v-else class="shot-placeholder">🎬</div>
            <div class="shot-info">
              <div class="shot-desc">{{ shot.description || shot.prompt || `分镜 ${i + 1}` }}</div>
              <div class="shot-duration" v-if="shot.duration">{{ shot.duration }}s</div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">暂无分镜预览</div>
      </div>

      <!-- Audio Tab -->
      <div v-if="activeTab === 'audio'" class="tab-content">
        <div class="audio-list" v-if="audioSamples.length > 0">
          <div v-for="(audio, i) in audioSamples" :key="i" class="audio-item">
            <div class="audio-character">{{ audio.character || audio.role || `配音 ${i + 1}` }}</div>
            <audio v-if="audio.url || audio.src" :src="audio.url || audio.src" controls class="audio-player"></audio>
            <div v-else class="audio-placeholder">
              <span>🎙️</span>
              <span>{{ audio.text || audio.line || '暂无音频' }}</span>
            </div>
            <div class="audio-meta" v-if="audio.emotion || audio.style">
              情感: {{ audio.emotion || audio.style }}
              <span v-if="audio.speed"> | 语速: {{ audio.speed }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">暂无配音试听</div>
      </div>

      <!-- Score Tab -->
      <div v-if="activeTab === 'score'" class="tab-content">
        <div v-if="aiScore" class="score-content">
          <div class="score-overall">
            <div class="score-circle" :style="{ borderColor: scoreColor(aiScore.overall || aiScore.total || aiScore.composite) }">
              <span class="score-value">{{ aiScore.overall || aiScore.total || aiScore.composite || 'N/A' }}</span>
              <span class="score-max">/10</span>
            </div>
            <div class="score-label">综合评分</div>
          </div>
          <div class="score-details">
            <div v-for="(val, key) in (aiScore.dimensions || aiScore.breakdown || {})" :key="key" class="score-row">
              <span class="score-dim">{{ key }}</span>
              <div class="score-bar-bg">
                <div class="score-bar-fill" :style="{ width: (val / 10 * 100) + '%', background: scoreColor(val) }"></div>
              </div>
              <span class="score-dim-val" :style="{ color: scoreColor(val) }">{{ val.toFixed(1) }}</span>
            </div>
          </div>
          <div v-if="aiScore.suggestions || aiScore.improvements" class="score-suggestions">
            <div class="suggestions-title">💡 改进建议</div>
            <ul>
              <li v-for="(s, i) in (aiScore.suggestions || aiScore.improvements || [])" :key="i">{{ s }}</li>
            </ul>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>尚未执行 AI 质量评估</p>
          <p class="sub-text">（FR-DR-005 需实现后才能显示评分）</p>
        </div>
      </div>
    </div>

    <!-- Duration Bar -->
    <div class="duration-bar" v-if="totalDuration !== '待估算'">
      <span class="duration-icon">⏱️</span>
      <span>时长估算: <strong>{{ totalDuration }}</strong></span>
    </div>

    <!-- Decision Area -->
    <div class="decision-area" v-if="!result">
      <textarea
        v-model="comment"
        placeholder="输入修改意见（选择「修改」时必填）..."
        class="comment-input"
        rows="2"
      ></textarea>
      <div class="decision-buttons">
        <button class="btn-approve" :disabled="submitting" @click="submitDecision('approve')">
          ✅ 通过
        </button>
        <button class="btn-modify" :disabled="submitting" @click="submitDecision('modify')">
          ✏️ 修改
        </button>
        <button class="btn-reject" :disabled="submitting" @click="submitDecision('reject')">
          ❌ 驳回
        </button>
      </div>
      <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
    </div>

    <!-- Result -->
    <div v-if="result" class="result-banner" :class="result">
      ✅ 决策已提交: {{ typeLabel[result] }}
      <span v-if="result === 'modify' && comment"> — 已触发重新执行</span>
    </div>
  </div>
</template>

<style scoped>
.review-panel {
  background: var(--bg-secondary, #1a1a1a);
  border: 1px solid var(--border, #333);
  border-radius: 16px;
  overflow: hidden;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border-bottom: 1px solid var(--border, #333);
}

.review-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary, #e5e5e5);
}

.review-icon { font-size: 22px; }

.close-btn {
  width: 32px; height: 32px;
  background: rgba(255,255,255,0.08);
  border: none;
  border-radius: 8px;
  color: var(--text-secondary, #888);
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover { background: rgba(255,255,255,0.15); color: #fff; }

.tab-bar {
  display: flex;
  border-bottom: 1px solid var(--border, #333);
  background: var(--bg-card, #242424);
}

.tab-bar button {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary, #888);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-bar button:hover { color: var(--text-primary, #e5e5e5); }
.tab-bar button.active {
  color: var(--accent-blue, #5e6ad2);
  border-bottom-color: var(--accent-blue, #5e6ad2);
}

.review-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  min-height: 200px;
  max-height: 50vh;
}

.script-meta-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: var(--bg-card, #242424);
  border-radius: 8px;
  font-size: 12px;
  color: var(--text-muted, #666);
}

.scene-block {
  margin-bottom: 16px;
  padding: 12px;
  background: var(--bg-card, #242424);
  border-radius: 8px;
  border-left: 3px solid var(--accent-blue, #5e6ad2);
}

.scene-header {
  font-weight: 600;
  color: var(--accent-blue, #5e6ad2);
  margin-bottom: 8px;
  font-size: 14px;
}

.scene-text {
  white-space: pre-wrap;
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary, #888);
}

.shots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
}

.shot-card {
  background: var(--bg-card, #242424);
  border-radius: 10px;
  overflow: hidden;
}

.shot-number {
  background: var(--accent-blue, #5e6ad2);
  color: #fff;
  text-align: center;
  padding: 4px;
  font-size: 12px;
  font-weight: 600;
}

.shot-img {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
  display: block;
}

.shot-placeholder {
  width: 100%;
  aspect-ratio: 16/9;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #111;
  font-size: 32px;
}

.shot-info {
  padding: 8px;
}

.shot-desc {
  font-size: 12px;
  color: var(--text-secondary, #888);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shot-duration {
  font-size: 11px;
  color: var(--text-muted, #666);
  margin-top: 4px;
}

.audio-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.audio-item {
  padding: 12px;
  background: var(--bg-card, #242424);
  border-radius: 8px;
}

.audio-character {
  font-weight: 600;
  color: var(--text-primary, #e5e5e5);
  margin-bottom: 8px;
}

.audio-player {
  width: 100%;
  height: 32px;
}

.audio-placeholder {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted, #666);
  font-size: 13px;
}

.audio-meta {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-muted, #666);
}

.score-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.score-overall {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.score-circle {
  width: 80px; height: 80px;
  border-radius: 50%;
  border: 4px solid;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-card, #242424);
}

.score-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary, #e5e5e5);
}
.score-max {
  font-size: 12px;
  color: var(--text-muted, #666);
}

.score-label {
  font-size: 14px;
  color: var(--text-secondary, #888);
}

.score-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.score-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.score-dim {
  width: 100px;
  font-size: 13px;
  color: var(--text-secondary, #888);
}

.score-bar-bg {
  flex: 1;
  height: 8px;
  background: #333;
  border-radius: 4px;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s;
}

.score-dim-val {
  width: 36px;
  font-size: 13px;
  font-weight: 600;
  text-align: right;
}

.score-suggestions {
  padding: 12px;
  background: rgba(255, 193, 7, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.suggestions-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: #ffc107;
}

.score-suggestions ul {
  margin: 0; padding-left: 18px;
}

.score-suggestions li {
  font-size: 13px;
  color: var(--text-secondary, #888);
  margin-bottom: 4px;
}

.duration-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg-card, #242424);
  border-top: 1px solid var(--border, #333);
  font-size: 13px;
  color: var(--text-secondary, #888);
}

.decision-area {
  padding: 16px;
  border-top: 1px solid var(--border, #333);
}

.comment-input {
  width: 100%;
  padding: 10px;
  background: var(--bg-card, #242424);
  border: 1px solid var(--border, #333);
  border-radius: 8px;
  color: var(--text-primary, #e5e5e5);
  font-size: 13px;
  resize: vertical;
  margin-bottom: 12px;
}

.comment-input:focus { outline: none; border-color: var(--accent-blue, #5e6ad2); }

.decision-buttons {
  display: flex;
  gap: 10px;
}

.btn-approve, .btn-modify, .btn-reject {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-approve { background: rgba(76,175,80,0.2); color: #4caf50; }
.btn-approve:hover { background: rgba(76,175,80,0.35); }

.btn-modify { background: rgba(255,152,0,0.2); color: #ff9800; }
.btn-modify:hover { background: rgba(255,152,0,0.35); }

.btn-reject { background: rgba(244,67,54,0.2); color: #f44336; }
.btn-reject:hover { background: rgba(244,67,54,0.35); }

.btn-approve:disabled, .btn-modify:disabled, .btn-reject:disabled { opacity: 0.4; cursor: not-allowed; }

.error-msg {
  margin-top: 10px;
  padding: 8px 12px;
  background: rgba(244,67,54,0.1);
  border-radius: 6px;
  color: #f44336;
  font-size: 13px;
}

.result-banner {
  padding: 12px 16px;
  text-align: center;
  font-weight: 600;
  font-size: 14px;
}
.result-banner.approve { background: rgba(76,175,80,0.15); color: #4caf50; }
.result-banner.modify { background: rgba(255,152,0,0.15); color: #ff9800; }
.result-banner.reject { background: rgba(244,67,54,0.15); color: #f44336; }

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-muted, #666);
}
.sub-text { font-size: 12px; margin-top: 8px; }
</style>
