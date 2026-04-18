<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:5001'
const projects = ref([])
const currentProject = ref('tk-southeast-asia')
const loading = ref(true)
const error = ref(null)
const selectedTask = ref(null)
const showModal = ref(false)

// 统计数据
const stats = ref({
  total: 0,
  running: 0,
  completed: 0,
  pending: 0,
  failed: 0
})

// KPI 卡片点击
async function fetchStats() {
  try {
    loading.value = true
    const res = await axios.get(`${API_BASE}/api/dashboard`)
    stats.value = {
      total: res.data.total || 0,
      running: res.data.running || 0,
      completed: res.data.completed || 0,
      pending: res.data.pending || 0,
      failed: res.data.failed || 0
    }
    error.value = null
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// 切换项目
async function switchProject(projectId) {
  currentProject.value = projectId
  await fetchStats()
}

// 任务列表
const tasks = ref([])

async function fetchTasks() {
  try {
    const res = await axios.get(`${API_BASE}/api/tasks`)
    tasks.value = res.data.tasks || []
  } catch (e) {
    console.error('Failed to fetch tasks:', e)
  }
}

// 查看任务详情
function viewTask(task) {
  selectedTask.value = task
  showModal.value = true
}

// 关闭模态框
function closeModal() {
  showModal.value = false
  selectedTask.value = null
}

// 状态样式
function statusClass(status) {
  return {
    'running': status === 'running',
    'completed': status === 'completed',
    'pending': status === 'pending',
    'failed': status === 'failed'
  }
}

// 状态文本
function statusText(status) {
  const map = {
    running: '🔵 运行中',
    completed: '🟢 已完成',
    pending: '🟡 待处理',
    failed: '🔴 失败'
  }
  return map[status] || status
}

onMounted(async () => {
  await Promise.all([fetchStats(), fetchTasks()])
})
</script>

<template>
  <div class="command-center">
    <!-- 顶部标题 -->
    <header class="header">
      <h1>🎯 Agentic OS v3.1 指挥中心</h1>
      <div class="project-switcher">
        <select v-model="currentProject" @change="switchProject(currentProject)">
          <option value="tk-southeast-asia">🇹🇭 TK 东南亚 3C</option>
          <option value="drama-production">🎬 AI 短剧生产线</option>
          <option value="voice-clone">🎙️ VoiceClone Pro</option>
        </select>
      </div>
    </header>

    <!-- KPI 网格 -->
    <div class="kpi-grid">
      <div class="kpi-card" @click="fetchTasks">
        <div class="label">总任务</div>
        <div class="value blue">{{ stats.total }}</div>
      </div>
      <div class="kpi-card">
        <div class="label">运行中</div>
        <div class="value green">{{ stats.running }}</div>
      </div>
      <div class="kpi-card">
        <div class="label">已完成</div>
        <div class="value yellow">{{ stats.completed }}</div>
      </div>
      <div class="kpi-card">
        <div class="label">待处理</div>
        <div class="value orange">{{ stats.pending }}</div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <router-link to="/dashboard" class="action-btn">📊 数据面板</router-link>
      <a href="http://localhost:5173" class="action-btn">📈 可视化</a>
      <button @click="fetchStats" class="action-btn">🔄 刷新</button>
    </div>

    <!-- 任务列表 -->
    <h2 class="section-title">任务列表</h2>
    <div class="task-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="tasks.length === 0" class="empty-state">暂无任务</div>
      <div
        v-for="task in tasks"
        :key="task.id"
        class="task-item"
        @click="viewTask(task)"
      >
        <div class="task-status" :class="statusClass(task.status)"></div>
        <div class="task-info">
          <div class="title">{{ task.title || task.id }}</div>
          <div class="meta">
            {{ statusText(task.status) }} · {{ task.project || currentProject }}
          </div>
        </div>
      </div>
    </div>

    <!-- 任务详情模态框 -->
    <div v-if="showModal" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeModal">&times;</span>
        <h2>{{ selectedTask.title || selectedTask.id }}</h2>
        <div class="task-detail">
          <p><strong>状态:</strong> {{ statusText(selectedTask.status) }}</p>
          <p><strong>项目:</strong> {{ selectedTask.project }}</p>
          <p><strong>创建时间:</strong> {{ selectedTask.created_at }}</p>
          <div v-if="selectedTask.description" class="description">
            <strong>描述:</strong>
            <p>{{ selectedTask.description }}</p>
          </div>
          <div v-if="selectedTask.decision_points?.length" class="decisions">
            <strong>决策点:</strong>
            <div v-for="dp in selectedTask.decision_points" :key="dp.id" class="decision-item">
              <p>{{ dp.question }}</p>
              <span class="decision-status" :class="dp.status">{{ dp.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.command-center {
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  min-height: 100vh;
  color: #f1f5f9;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h1 {
  font-size: 28px;
  color: #38bdf8;
}

.project-switcher select {
  padding: 8px 16px;
  border-radius: 8px;
  background: #1e293b;
  color: #fff;
  border: 1px solid #334155;
  font-size: 14px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.kpi-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  border: 2px solid #334155;
  cursor: pointer;
  transition: all 0.2s;
}

.kpi-card:hover {
  background: rgba(56, 189, 248, 0.1);
}

.kpi-card .label {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 8px;
}

.kpi-card .value {
  font-size: 36px;
  font-weight: bold;
}

.kpi-card .value.blue { color: #38bdf8; }
.kpi-card .value.green { color: #4ade80; }
.kpi-card .value.yellow { color: #facc15; }
.kpi-card .value.orange { color: #fb923c; }

.quick-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.action-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.section-title {
  font-size: 20px;
  margin: 24px 0 16px;
  color: #cbd5e1;
}

.task-list {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #334155;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #334155;
  cursor: pointer;
}

.task-item:hover {
  background: rgba(56, 189, 248, 0.1);
}

.task-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 16px;
}

.task-status.running {
  background: #38bdf8;
  animation: pulse 2s infinite;
}

.task-status.completed {
  background: #4ade80;
}

.task-status.pending {
  background: #facc15;
}

.task-status.failed {
  background: #f87171;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.task-info {
  flex: 1;
}

.task-info .title {
  font-weight: 600;
}

.task-info .meta {
  font-size: 12px;
  color: #94a3b8;
}

.modal {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #1e293b;
  border-radius: 20px;
  padding: 30px;
  max-width: 700px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  border: 1px solid #38bdf8;
}

.close {
  float: right;
  cursor: pointer;
  font-size: 24px;
  color: #94a3b8;
}

.task-detail {
  margin-top: 16px;
}

.task-detail p {
  margin: 8px 0;
}

.description {
  margin-top: 16px;
  padding: 12px;
  background: #0f172a;
  border-radius: 8px;
}

.decisions {
  margin-top: 16px;
}

.decision-item {
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  background: #0f172a;
}

.decision-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-top: 8px;
}

.decision-status.pending {
  background: #facc15;
  color: #0f172a;
}

.decision-status.completed {
  background: #4ade80;
  color: #0f172a;
}

.decision-status.rejected {
  background: #f87171;
  color: #0f172a;
}

.loading, .empty-state {
  text-align: center;
  padding: 40px;
  color: #64748b;
}
</style>
