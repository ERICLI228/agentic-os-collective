<script setup>
import { computed } from 'vue'

const props = defineProps({
  tasks: { type: Array, default: () => [] }
})

const emit = defineEmits(['resolve-decision'])

const pendingDecisions = computed(() => {
  const decisions = []
  props.tasks.forEach(task => {
    (task.decision_points || []).forEach(d => {
      if (d.status === 'pending') {
        decisions.push({
          ...d,
          taskId: task.id,
          taskName: task.name
        })
      }
    })
  })
  return decisions
})

function resolve(taskId, decisionId, choice) {
  emit('resolve-decision', taskId, decisionId, choice)
}
</script>

<template>
  <div v-if="pendingDecisions.length > 0" class="decision-panel">
    <h3 class="panel-title">
      <span class="alert-icon">⚠️</span>
      待处理决策 ({{ pendingDecisions.length }})
    </h3>
    <div class="decision-list">
      <div v-for="d in pendingDecisions" :key="d.id" class="decision-card">
        <div class="decision-info">
          <div class="decision-task">{{ d.taskName }}</div>
          <div class="decision-question">{{ d.question }}</div>
        </div>
        <div class="decision-actions">
          <button @click="resolve(d.taskId, d.id, '通过')" class="btn-approve">✓ 通过</button>
          <button @click="resolve(d.taskId, d.id, '拒绝')" class="btn-reject">✗ 拒绝</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.decision-panel {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--accent-orange);
}

.alert-icon {
  font-size: 18px;
}

.decision-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.decision-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  border-left: 3px solid var(--accent-orange);
}

.decision-info {
  flex: 1;
}

.decision-task {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.decision-question {
  font-weight: 500;
}

.decision-actions {
  display: flex;
  gap: 8px;
}

.btn-approve, .btn-reject {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-approve {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.btn-approve:hover {
  background: rgba(76, 175, 80, 0.3);
}

.btn-reject {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.btn-reject:hover {
  background: rgba(244, 67, 54, 0.3);
}
</style>