<script setup>
import { computed } from 'vue'

const props = defineProps({
  tasks: { type: Array, default: () => [] },
  view: { type: String, default: 'table' }
})

const emit = defineEmits(['resolve-decision'])

const statusMap = {
  'running': { label: '运行中', color: '#4caf50' },
  'pending': { label: '待处理', color: '#ff9800' },
  'completed': { label: '已完成', color: '#888' },
  'error': { label: '错误', color: '#f44336' }
}

const priorityMap = {
  'high': { label: '高', color: '#f44336' },
  'medium': { label: '中', color: '#ff9800' },
  'low': { label: '低', color: '#4caf50' }
}

const kanbanColumns = [
  { status: 'running', title: '运行中', color: '#4caf50' },
  { status: 'pending', title: '待处理', color: '#ff9800' },
  { status: 'completed', title: '已完成', color: '#888' }
]

const tasksByStatus = computed(() => {
  const grouped = { running: [], pending: [], completed: [], error: [] }
  props.tasks.forEach(task => {
    const status = task.status || 'pending'
    if (grouped[status]) {
      grouped[status].push(task)
    } else {
      grouped.pending.push(task)
    }
  })
  return grouped
})

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function truncate(str, len = 40) {
  if (!str) return '-'
  return str.length > len ? str.slice(0, len) + '...' : str
}
</script>

<template>
  <!-- 列表视图 -->
  <div v-if="view === 'table'" class="table-view">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>任务名称</th>
          <th>项目</th>
          <th>状态</th>
          <th>优先级</th>
          <th>创建时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id" class="task-row">
          <td class="mono">{{ truncate(task.id, 8) }}</td>
          <td>
            <div class="task-name">{{ task.name || '未命名任务' }}</div>
            <div v-if="task.description" class="task-desc">{{ truncate(task.description, 50) }}</div>
          </td>
          <td>
            <span class="project-tag" :class="task.project_id">
              {{ task.project_id === 'drama' ? '短剧' : 'TK' }}
            </span>
          </td>
          <td>
            <span class="status-badge" :style="{ background: statusMap[task.status]?.color + '20', color: statusMap[task.status]?.color }">
              {{ statusMap[task.status]?.label || task.status }}
            </span>
          </td>
          <td>
            <span class="priority-badge" :class="task.priority || 'medium'">
              {{ priorityMap[task.priority]?.label || '中' }}
            </span>
          </td>
          <td class="mono">{{ formatDate(task.created_at) }}</td>
        </tr>
        <tr v-if="tasks.length === 0">
          <td colspan="6" class="empty-state">暂无任务</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 看板视图 -->
  <div v-else-if="view === 'kanban'" class="kanban-view">
    <div v-for="col in kanbanColumns" :key="col.status" class="kanban-column">
      <div class="column-header">
        <span class="column-dot" :style="{ background: col.color }"></span>
        <span class="column-title">{{ col.title }}</span>
        <span class="column-count">{{ tasksByStatus[col.status]?.length || 0 }}</span>
      </div>
      <div class="column-content">
        <div v-for="task in tasksByStatus[col.status]" :key="task.id" class="kanban-card">
          <div class="card-header">
            <span class="project-tag small" :class="task.project_id">
              {{ task.project_id === 'drama' ? '短剧' : 'TK' }}
            </span>
          </div>
          <div class="card-title">{{ task.name || '未命名任务' }}</div>
          <div v-if="task.description" class="card-desc">{{ truncate(task.description, 60) }}</div>
          <div class="card-footer">
            <span class="mono">{{ truncate(task.id, 6) }}</span>
            <span class="card-date">{{ formatDate(task.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 时间线视图 -->
  <div v-else-if="view === 'timeline'" class="timeline-view">
    <div class="timeline">
      <div v-for="task in tasks" :key="task.id" class="timeline-item">
        <div class="timeline-dot" :style="{ background: statusMap[task.status]?.color }"></div>
        <div class="timeline-content">
          <div class="timeline-header">
            <span class="project-tag" :class="task.project_id">
              {{ task.project_id === 'drama' ? '短剧' : 'TK' }}
            </span>
            <span class="timeline-time">{{ formatDate(task.created_at) }}</span>
          </div>
          <div class="timeline-title">{{ task.name || '未命名任务' }}</div>
          <div v-if="task.description" class="timeline-desc">{{ truncate(task.description, 80) }}</div>
        </div>
      </div>
      <div v-if="tasks.length === 0" class="empty-state">暂无任务</div>
    </div>
  </div>
</template>

<style scoped>
.table-view { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { text-align: left; padding: 12px 16px; font-weight: 500; color: var(--text-secondary); border-bottom: 1px solid var(--border); }
td { padding: 16px; border-bottom: 1px solid var(--border); vertical-align: top; }
.task-row:hover { background: var(--bg-hover); }
.task-name { font-weight: 500; margin-bottom: 4px; }
.task-desc { font-size: 13px; color: var(--text-secondary); }
.mono { font-family: 'SF Mono', monospace; font-size: 12px; color: var(--text-muted); }
.project-tag { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; }
.project-tag.drama { background: rgba(233, 30, 99, 0.15); color: #e91e63; }
.project-tag.tk { background: rgba(94, 106, 210, 0.15); color: #5e6ad2; }
.project-tag.small { padding: 2px 6px; font-size: 11px; }
.status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.priority-badge { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; }
.priority-badge.high { background: rgba(244, 67, 54, 0.15); color: #f44336; }
.priority-badge.medium { background: rgba(255, 152, 0, 0.15); color: #ff9800; }
.priority-badge.low { background: rgba(76, 175, 80, 0.15); color: #4caf50; }
.empty-state { text-align: center; padding: 48px; color: var(--text-muted); }

.kanban-view { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.kanban-column { background: var(--bg-secondary); border-radius: 12px; min-width: 280px; }
.column-header { display: flex; align-items: center; gap: 8px; padding: 16px; border-bottom: 1px solid var(--border); }
.column-dot { width: 8px; height: 8px; border-radius: 50%; }
.column-title { font-weight: 500; flex: 1; }
.column-count { font-size: 13px; color: var(--text-secondary); background: var(--bg-card); padding: 2px 8px; border-radius: 10px; }
.column-content { padding: 12px; min-height: 200px; }
.kanban-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
.kanban-card:hover { border-color: var(--accent-blue); transform: translateY(-2px); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.card-title { font-weight: 500; margin-bottom: 4px; }
.card-desc { font-size: 12px; color: var(--text-secondary); margin-bottom: 12px; }
.card-footer { display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-muted); }

.timeline-view { padding: 16px; }
.timeline { position: relative; padding-left: 24px; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: var(--border); }
.timeline-item { position: relative; padding: 16px 0 16px 24px; }
.timeline-dot { position: absolute; left: -20px; top: 20px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--bg-primary); }
.timeline-content { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }
.timeline-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.timeline-time { font-size: 12px; color: var(--text-muted); }
.timeline-title { font-weight: 500; margin-bottom: 4px; }
.timeline-desc { font-size: 13px; color: var(--text-secondary); }</style>
