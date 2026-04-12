<script setup>
import { ref, computed } from 'vue'
import KPIPanel from './KPIPanel.vue'
import TaskList from './TaskList.vue'
import DecisionPanel from './DecisionPanel.vue'

const props = defineProps({
  data: { type: Object, required: true },
  searchQuery: { type: String, default: '' },
  statusFilter: { type: String, default: 'all' }
})

const emit = defineEmits(['resolve-decision'])

const currentView = ref('table') // table | kanban | timeline

const kpiData = computed(() => props.data?.kpi || {})
const activeTasks = computed(() => {
  let tasks = props.data?.active_tasks || []
  
  // 按状态筛选
  if (props.statusFilter && props.statusFilter !== 'all') {
    tasks = tasks.filter(t => t.status === props.statusFilter)
  }
  
  // 按关键词搜索
  if (props.searchQuery) {
    const q = props.searchQuery.toLowerCase()
    tasks = tasks.filter(t => 
      (t.name && t.name.toLowerCase().includes(q)) ||
      (t.description && t.description.toLowerCase().includes(q)) ||
      (t.id && t.id.toLowerCase().includes(q))
    )
  }
  
  return tasks.slice(0, 30)
})
const pendingDecisions = computed(() => props.data?.pending_decisions || 0)

function handleResolve(taskId, decisionId, choice) {
  emit('resolve-decision', taskId, decisionId, choice)
}
</script>

<template>
  <div class="dashboard">
    <!-- KPI 概览 -->
    <KPIPanel :kpi="kpiData" :tasks="activeTasks" />

    <!-- 视图切换 -->
    <div class="view-controls">
      <div class="view-tabs">
        <button 
          v-for="view in ['table', 'kanban', 'timeline']" 
          :key="view"
          @click="currentView = view"
          :class="['tab', { active: currentView === view }]"
        >
          {{ view === 'table' ? '列表' : view === 'kanban' ? '看板' : '时间线' }}
        </button>
      </div>
      <div class="stats">
        <span class="badge">{{ activeTasks.length }} 个活跃任务</span>
        <span v-if="pendingDecisions > 0" class="badge warning">
          {{ pendingDecisions }} 个待决策
        </span>
      </div>
    </div>

    <!-- 任务区域 -->
    <div class="content-area">
      <TaskList 
        :tasks="activeTasks" 
        :view="currentView"
        @resolve-decision="handleResolve"
      />
    </div>

    <!-- 决策面板 -->
    <DecisionPanel 
      :tasks="activeTasks"
      @resolve-decision="handleResolve"
    />
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.view-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.view-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-card);
  padding: 4px;
  border-radius: 8px;
}

.tab {
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.tab:hover {
  color: var(--text-primary);
}

.tab.active {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.stats {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 12px;
  background: var(--bg-card);
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-secondary);
}

.badge.warning {
  background: rgba(255, 152, 0, 0.2);
  color: var(--accent-orange);
}

.content-area {
  min-height: 400px;
}
</style>