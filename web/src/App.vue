<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Dashboard from './components/Dashboard.vue'
import CommandCenter from './components/CommandCenter.vue'

const API_BASE = 'http://localhost:5001'
const data = ref(null)
const loading = ref(true)
const error = ref(null)

// 自动刷新
const refreshInterval = ref(null)
const autoRefresh = ref(true)

async function fetchData() {
  try {
    loading.value = true
    const res = await axios.get(`${API_BASE}/api/dashboard`)
    data.value = res.data
    error.value = null
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function resolveDecision(taskId, decisionId, choice) {
  try {
    await axios.post(`${API_BASE}/api/decision/${taskId}/${decisionId}`, { choice })
    await fetchData() // 刷新数据
  } catch (e) {
    error.value = e.message
  }
}

// 当前视图
const currentView = ref('command') // 默认显示指挥中心

// 切换视图
function switchView(view) {
  currentView.value = view
}

// 搜索关键词
const searchQuery = ref('')

// 筛选状态
const statusFilter = ref('all')

// 快捷键
function handleKeydown(e) {
  // 忽略输入框中的快捷键
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return
  
  switch(e.key.toLowerCase()) {
    case 'k':
      currentView.value = 'kanban'
      break
    case 'l':
      currentView.value = 'table'
      break
    case 't':
      currentView.value = 'timeline'
      break
    case '/':
      e.preventDefault()
      document.querySelector('.search-input')?.focus()
      break
    case 'r':
      fetchData()
      break
    case 'Escape':
      searchQuery.value = ''
      statusFilter.value = 'all'
      break
  }
}

onMounted(() => {
  fetchData()
  if (autoRefresh.value) {
    refreshInterval.value = setInterval(fetchData, 30000) // 30秒刷新
  }
  // 添加键盘监听
  window.addEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="app-container">
    <!-- 指挥中心视图 -->
    <CommandCenter v-if="currentView === 'command'" />

    <!-- 数据监控视图 -->
    <template v-else>
      <!-- 顶部导航 -->
      <header class="top-bar">
        <div class="logo">
          <button @click="switchView('command')" class="back-btn" title="返回指挥中心">←</button>
          <span class="logo-icon">📊</span>
          <span class="logo-text">数据监控</span>
        </div>
        
        <!-- 搜索框 -->
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input" 
            placeholder="搜索任务... (按 / 聚焦)"
          />
          <select v-model="statusFilter" class="status-filter">
            <option value="all">全部状态</option>
            <option value="running">运行中</option>
            <option value="pending">待处理</option>
            <option value="completed">已完成</option>
          </select>
        </div>
        
        <div class="actions">
          <span class="shortcut-hint">K:看板 L:列表 T:时间线 R:刷新</span>
          <button @click="fetchData" :disabled="loading" class="btn-refresh">
            {{ loading ? '刷新中...' : '刷新' }}
          </button>
          <span class="status-dot" :class="{ online: !error, offline: error }"></span>
        </div>
      </header>

      <!-- 主内容 -->
      <main v-if="data">
        <Dashboard 
          :data="data" 
          :search-query="searchQuery"
          :status-filter="statusFilter"
          @resolve-decision="resolveDecision"
        />
      </main>

      <!-- 加载状态 -->
      <div v-if="loading && !data" class="loading-state">
        <div class="spinner"></div>
        <p>加载 Dashboard 数据...</p>
      </div>

      <!-- 错误状态 -->
      <div v-if="error" class="error-state">
        <p>⚠️ 连接失败: {{ error }}</p>
        <button @click="fetchData">重试</button>
      </div>
    </template>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg-primary: #0d0d0d;
  --bg-secondary: #1a1a1a;
  --bg-card: #242424;
  --bg-hover: #2a2a2a;
  --text-primary: #e5e5e5;
  --text-secondary: #888;
  --text-muted: #666;
  --accent-blue: #5e6ad2;
  --accent-green: #4caf50;
  --accent-orange: #ff9800;
  --accent-red: #f44336;
  --border: #333;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.5;
}

.app-container {
  min-height: 100vh;
  padding: 0;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  text-decoration: none;
  font-size: 18px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: var(--accent);
  color: var(--bg-primary);
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shortcut-hint {
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-card);
  padding: 4px 8px;
  border-radius: 4px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  max-width: 400px;
  margin: 0 24px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.status-filter {
  padding: 8px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
}

.btn-refresh {
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover:not(:disabled) {
  background: var(--bg-hover);
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.online {
  background: var(--accent-green);
}

.status-dot.offline {
  background: var(--accent-red);
}

main {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--accent-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  color: var(--accent-red);
}

.error-state button {
  padding: 8px 16px;
  background: var(--accent-red);
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}
</style>