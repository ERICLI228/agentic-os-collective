<script setup>
import { computed } from 'vue'

const props = defineProps({
  kpi: { type: Object, default: () => ({}) },
  tasks: { type: Array, default: () => [] }
})

const projects = [
  { key: 'drama', name: '短剧项目', color: '#e91e63' },
  { key: 'tk', name: 'TK 运营', color: '#5e6ad2' }
]

// 项目 KPI
const kpiCards = computed(() => {
  return projects.map(p => {
    const data = props.kpi[p.key] || {}
    const budgetUsed = data.budget_used || 0
    const budgetLimit = data.budget_limit || 1
    const budgetPercent = Math.round((budgetUsed / budgetLimit) * 100)
    
    return {
      ...p,
      running: data.running || 0,
      budgetUsed,
      budgetLimit,
      budgetPercent,
      budgetWarning: budgetPercent > 80
    }
  })
})

// 总体统计
const stats = computed(() => {
  const allTasks = props.tasks || []
  const total = allTasks.length
  const running = allTasks.filter(t => t.status === 'running').length
  const completed = allTasks.filter(t => t.status === 'completed').length
  const completedRate = total > 0 ? Math.round((completed / total) * 100) : 0
  
  return { total, running, completed, completedRate }
})
</script>

<template>
  <div class="kpi-panel">
    <!-- 总体统计 -->
    <div class="kpi-card stats-card">
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-value">{{ stats.total }}</span>
          <span class="stat-label">总任务</span>
        </div>
        <div class="stat-item running">
          <span class="stat-value">{{ stats.running }}</span>
          <span class="stat-label">进行中</span>
        </div>
        <div class="stat-item success">
          <span class="stat-value">{{ stats.completed }}</span>
          <span class="stat-label">已完成</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ stats.completedRate }}%</span>
          <span class="stat-label">完成率</span>
        </div>
      </div>
    </div>
    
    <!-- 项目 KPI -->
    <div v-for="card in kpiCards" :key="card.key" class="kpi-card">
      <div class="kpi-header">
        <div class="project-icon" :style="{ background: card.color }">
          {{ card.key === 'drama' ? '🎬' : '🛒' }}
        </div>
        <div class="project-info">
          <h3>{{ card.name }}</h3>
          <span class="project-key">{{ card.key }}</span>
        </div>
      </div>
      
      <div class="kpi-metrics">
        <div class="metric">
          <span class="metric-value">{{ card.running }}</span>
          <span class="metric-label">运行中任务</span>
        </div>
        
        <div class="metric">
          <span class="metric-value" :class="{ warning: card.budgetWarning }">
            {{ card.budgetPercent }}%
          </span>
          <span class="metric-label">预算使用</span>
        </div>
      </div>
      
      <div class="budget-bar">
        <div 
          class="budget-fill" 
          :style="{ 
            width: `${card.budgetPercent}%`,
            background: card.budgetWarning ? 'var(--accent-orange)' : card.color
          }"
        ></div>
      </div>
      
      <div class="budget-detail">
        {{ (card.budgetUsed / 1000).toFixed(1) }}k / {{ (card.budgetLimit / 1000).toFixed(0) }}k tokens
      </div>
    </div>
  </div>
</template>

<style scoped>
.kpi-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.stats-card {
  background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 8px;
}

.stat-value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-item.running .stat-value {
  color: var(--accent-blue);
}

.stat-item.success .stat-value {
  color: var(--accent-green);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
}

.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
}

.kpi-card:hover {
  border-color: var(--border);
  box-shadow: var(--shadow);
}

.kpi-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.project-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.project-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.project-key {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
}

.kpi-metrics {
  display: flex;
  gap: 32px;
  margin-bottom: 16px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.metric-value.warning {
  color: var(--accent-orange);
}

.metric-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.budget-bar {
  height: 6px;
  background: var(--bg-secondary);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.budget-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.budget-detail {
  font-size: 12px;
  color: var(--text-muted);
  text-align: right;
}
</style>