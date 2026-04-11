<script setup>
import { computed } from 'vue'

const props = defineProps({
  kpi: { type: Object, default: () => ({}) }
})

const projects = [
  { key: 'drama', name: '短剧项目', color: '#e91e63' },
  { key: 'tk', name: 'TK 运营', color: '#5e6ad2' }
]

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
</script>

<template>
  <div class="kpi-panel">
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
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
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