<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Dashboard from './components/Dashboard.vue'

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

onMounted(() => {
  fetchData()
  if (autoRefresh.value) {
    refreshInterval.value = setInterval(fetchData, 30000) // 30秒刷新
  }
})
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航 -->
    <header class="top-bar">
      <div class="logo">
        <span class="logo-icon">⚡</span>
        <span class="logo-text">Agentic OS</span>
      </div>
      <div class="actions">
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