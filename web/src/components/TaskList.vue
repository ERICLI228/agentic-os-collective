<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  tasks: { type: Array, default: () => [] },
  view: { type: String, default: 'table' }
})

const emit = defineEmits(['resolve-decision', 'task-created'])

// 状态
const selectedTask = ref(null)
const selectedMilestone = ref(null)
const milestoneDetails = ref(null)
const showTaskModal = ref(false)
const showMilestoneDrawer = ref(false)
const isExecuting = ref(false)

// 新建任务表单
const newTask = ref({
  project: 'drama',
  template: 'drama_pipeline',
  title: '',
  description: ''
})

const availableTemplates = ref([])

// 智能向导状态
const wizardStep = ref(1)
const titleValidation = ref({ valid: true, errors: [], suggestions: [] })
const recommendedTemplate = ref(null)
const descriptionGuide = ref([])
const isValidating = ref(false)

// 时间线过滤
const timelineFilter = ref({
  project: 'all',
  milestoneStatus: 'all',
  taskId: 'all'
})

// 过滤后的时间线任务
const filteredTimelineTasks = computed(() => {
  let tasks = props.tasks || []
  if (timelineFilter.value.project !== 'all') {
    tasks = tasks.filter(t => t.project_id === timelineFilter.value.project)
  }
  return tasks
})

// 时间线任务
const timelineTasks = computed(() => {
  let tasks = filteredTimelineTasks.value
  if (timelineFilter.value.taskId !== 'all') {
    tasks = tasks.filter(t => t.id === timelineFilter.value.taskId)
  }
  // 过滤里程碑状态
  if (timelineFilter.value.milestoneStatus !== 'all') {
    tasks = tasks.filter(t => t.milestones?.some(m => m.status === timelineFilter.value.milestoneStatus))
  }
  return tasks
})

// 状态映射
const statusMap = {
  'running': { label: '运行中', color: '#4caf50' },
  'pending': { label: '待处理', color: '#ff9800' },
  'completed': { label: '已完成', color: '#888' },
  'failed': { label: '失败', color: '#f44336' }
}

const priorityMap = {
  'P0': { label: 'P0', color: '#f44336' },
  'P1': { label: 'P1', color: '#ff9800' },
  'P2': { label: 'P2', color: '#4caf50' }
}

// 加载模板
async function loadTemplates() {
  try {
    const res = await fetch('/api/templates')
    const data = await res.json()
    availableTemplates.value = data.templates || []
  } catch (e) {
    console.error('Failed to load templates:', e)
  }
}

// 智能向导：验证标题
async function validateTitle() {
  if (!newTask.value.title.trim()) {
    titleValidation.value = { valid: true, errors: [], suggestions: [] }
    return
  }
  isValidating.value = true
  try {
    const res = await fetch('/api/task/wizard/validate-title', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTask.value.title })
    })
    titleValidation.value = await res.json()
    
    // 自动推荐模板
    if (newTask.value.title.length > 2) {
      await recommendTemplate()
    }
  } catch (e) {
    console.error('Validation failed:', e)
  }
  isValidating.value = false
}

// 智能向导：推荐模板
async function recommendTemplate() {
  try {
    const res = await fetch('/api/task/wizard/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: newTask.value.title, category: newTask.value.project })
    })
    recommendedTemplate.value = await res.json()
    if (recommendedTemplate.value.template) {
      newTask.value.template = recommendedTemplate.value.template
    }
  } catch (e) {
    console.error('Recommendation failed:', e)
  }
}

// 智能向导：加载描述指引
async function loadDescriptionGuide() {
  try {
    // 清除旧指引再加载
    descriptionGuide.value = []
    const res = await fetch(`/api/task/wizard/description-guide?category=${newTask.value.project}`)
    const data = await res.json()
    descriptionGuide.value = data.guide || []
    console.log('Loaded guide for', newTask.value.project, ':', descriptionGuide.value.length, 'items')
  } catch (e) {
    console.error('Failed to load guide:', e)
  }
}

// 加载里程碑详情
async function loadMilestoneDetails(taskId, milestoneId) {
  console.log('加载里程碑详情:', taskId, milestoneId)
  try {
    const res = await fetch(`/api/tasks/${taskId}/milestone/${milestoneId}`)
    const data = await res.json()
    console.log('返回数据:', data)
    milestoneDetails.value = data.milestone
    selectedMilestone.value = milestoneId
    console.log('milestoneDetails 设置完成:', milestoneDetails.value)
  } catch (e) {
    console.error('Failed to load milestone details:', e)
  }
}

// 打开任务详情抽屉 (点击任务行)
async function openTaskDrawer(task) {
  selectedTask.value = task
  // 默认选择第一个未完成的里程碑
  const firstPending = task.milestones?.find(m => m.status !== 'completed')
  if (firstPending) {
    showMilestoneDrawer.value = true
    await loadMilestoneDetails(task.id, firstPending.id)
  } else if (task.milestones?.length > 0) {
    // 如果都已完成，显示最后一个
    showMilestoneDrawer.value = true
    await loadMilestoneDetails(task.id, task.milestones[task.milestones.length - 1].id)
  }
}

// 点击里程碑圆点
async function onMilestoneClick(task, milestone) {
  selectedTask.value = task
  showMilestoneDrawer.value = true
  await loadMilestoneDetails(task.id, milestone.id)
}

// 打开新建任务弹窗
function openCreateTask() {
  newTask.value = {
    project: 'drama',
    template: 'drama_pipeline',
    title: '',
    description: ''
  }
  wizardStep.value = 1
  titleValidation.value = { valid: true, errors: [], suggestions: [] }
  recommendedTemplate.value = null
  loadDescriptionGuide()
  showTaskModal.value = true
}

// 创建任务
async function createTask() {
  try {
    const res = await fetch('/api/tasks/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTask.value)
    })
    const data = await res.json()
    if (data.task_id) {
      showTaskModal.value = false
      emit('task-created', data.task_id)
      // 自动执行第一阶段
      const firstMs = data.task?.milestones?.[0]?.id
      if (firstMs) {
        await executeMilestone(data.task_id, firstMs)
      }
    }
  } catch (e) {
    console.error('Failed to create task:', e)
  }
}

// 执行里程碑
async function executeMilestone(taskId, milestoneId) {
  if (isExecuting.value) return
  isExecuting.value = true
  try {
    const res = await fetch(`/api/tasks/${taskId}/execute/${milestoneId}`, {
      method: 'POST'
    })
    const data = await res.json()
    // 刷新详情
    await loadMilestoneDetails(taskId, milestoneId)
  } catch (e) {
    console.error('Failed to execute milestone:', e)
  } finally {
    isExecuting.value = false
  }
}

// 决策相关状态
const showDecisionInput = ref(false)
const decisionComment = ref('')
const pendingDecisionType = ref('')

// 获取决策按钮样式
function getDecisionBtnClass(opt) {
  if (opt.includes('通过') || opt.includes('同意') || opt === 'approve') return 'btn-approve'
  if (opt.includes('修改') || opt.includes('驳回') || opt === 'modify' || opt === 'reject') return 'btn-modify'
  return 'btn-default'
}

// 处理决策选择
function handleDecision(option) {
  if (option.includes('修改') || option === 'modify') {
    showDecisionInput.value = true
    pendingDecisionType.value = 'modify'
  } else if (option.includes('驳回') || option === 'reject') {
    pendingDecisionType.value = 'reject'
    submitDecision()
  } else {
    pendingDecisionType.value = 'approve'
    submitDecision()
  }
}

// 提交决策
async function submitDecision() {
  if (!selectedTask.value || !selectedMilestone.value) return
  
  try {
    const res = await fetch('/api/decision/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        task_id: selectedTask.value.id,
        milestone_id: selectedMilestone.value,
        decision_type: pendingDecisionType.value,
        comment: decisionComment.value
      })
    })
    const data = await res.json()
    if (data.status === 'ok') {
      // 刷新详情
      await loadMilestoneDetails(selectedTask.value.id, selectedMilestone.value)
      showDecisionInput.value = false
      decisionComment.value = ''
    }
  } catch (e) {
    console.error('Failed to submit decision:', e)
  }
}

// 看板列
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

// 初始化
onMounted(() => {
  loadTemplates()
})
</script>

<template>
  <!-- 顶部操作栏 -->
  <div class="toolbar">
    <button class="btn-primary" @click="openCreateTask">+ 新建任务</button>
  </div>

  <!-- 列表视图 -->
  <div v-if="view === 'table'" class="table-view">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>任务名称</th>
          <th>里程碑进度</th>
          <th>状态</th>
          <th>创建时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id" class="task-row" @click="openTaskDrawer(task)">
          <td class="mono">{{ truncate(task.id, 10) }}</td>
          <td>
            <div class="task-name">{{ task.name || '未命名任务' }}</div>
            <div v-if="task.description" class="task-desc">{{ truncate(task.description, 50) }}</div>
          </td>
          <td>
            <div class="milestone-progress">
              <span class="progress-text">
                {{ task.milestones?.filter(m => m.status === 'completed').length || 0 }}/{{ task.milestones?.length || 0 }}
              </span>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: ((task.milestones?.filter(m => m.status === 'completed').length || 0) / (task.milestones?.length || 1)) * 100 + '%' }"
                ></div>
              </div>
            </div>
            <!-- 里程碑列表 -->
            <div class="milestone-list">
              <span 
                v-for="m in task.milestones" 
                :key="m.id"
                class="milestone-dot"
                :class="m.status"
                :title="m.name"
                @click="onMilestoneClick(task, m)"
              ></span>
            </div>
          </td>
          <td>
            <span class="status-badge" :style="{ background: statusMap[task.status]?.color + '20', color: statusMap[task.status]?.color }">
              {{ statusMap[task.status]?.label || task.status }}
            </span>
          </td>
          <td class="mono">{{ formatDate(task.created_at) }}</td>
        </tr>
        <tr v-if="tasks.length === 0">
          <td colspan="5" class="empty-state">暂无任务</td>
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
        <div v-for="task in tasksByStatus[col.status]" :key="task.id" class="kanban-card" @click="openTaskDrawer(task)">
          <div class="card-header">
            <span class="project-tag small" :class="task.project_id">
              {{ task.project_id === 'drama' ? '短剧' : 'TK' }}
            </span>
          </div>
          <div class="card-title">{{ task.name || '未命名任务' }}</div>
          <!-- 里程碑进度 -->
          <div class="card-milestones">
            <span 
              v-for="m in task.milestones?.slice(0,8)" 
              :key="m.id"
              class="milestone-dot small"
              :class="m.status"
              :title="m.name"
            ></span>
            <span v-if="task.milestones?.length > 8" class="more">+{{ task.milestones.length - 8 }}</span>
          </div>
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
    <div class="timeline-controls">
      <div class="filter-group">
        <label>项目</label>
        <select v-model="timelineFilter.project" class="filter-select">
          <option value="all">全部</option>
          <option value="drama">短剧</option>
          <option value="tk">TK运营</option>
        </select>
      </div>
      <div class="filter-group">
        <label>里程碑状态</label>
        <select v-model="timelineFilter.milestoneStatus" class="filter-select">
          <option value="all">全部</option>
          <option value="pending">待处理</option>
          <option value="running">进行中</option>
          <option value="completed">已完成</option>
          <option value="blocked">受阻</option>
        </select>
      </div>
      <div class="filter-group">
        <label>任务</label>
        <select v-model="timelineFilter.taskId" class="filter-select">
          <option value="all">全部任务</option>
          <option v-for="t in filteredTimelineTasks" :key="t.id" :value="t.id">
            {{ t.name || truncate(t.id, 10) }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="timeline-content">
      <div v-if="timelineTasks.length === 0" class="timeline-empty">
        <p>暂无符合条件的任务时间线</p>
      </div>
      <div v-for="task in timelineTasks" :key="task.id" class="timeline-task-block" @click="openTaskDrawer(task)">
        <div class="timeline-task-header">
          <span class="project-tag" :class="task.project_id">{{ task.project_id === 'drama' ? '短剧' : 'TK' }}</span>
          <span class="timeline-task-name">{{ task.name || truncate(task.id, 10) }}</span>
          <span class="timeline-task-status" :class="task.status">{{ statusMap[task.status]?.label }}</span>
        </div>
        <div class="timeline-milestones">
          <div v-for="m in task.milestones" :key="m.id" class="milestone-node" :class="m.status" @click.stop="onMilestoneClick(task, m)">
            <div class="milestone-marker"></div>
            <div class="milestone-info">
              <span class="milestone-name">{{ m.name }}</span>
              <span class="milestone-time">{{ formatDate(m.updated_at || m.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 新建任务弹窗 (智能向导增强) -->
  <div v-if="showTaskModal" class="modal-overlay" @click.self="showTaskModal = false">
    <div class="modal" style="width: 560px;">
      <div class="modal-header">
        <h3>✨ 新建任务 (智能向导)</h3>
        <button class="close-btn" @click="showTaskModal = false">×</button>
      </div>
      <div class="modal-body">
        <!-- 项目类型选择 -->
        <div class="form-group">
          <label>🎯 项目类型</label>
          <div class="category-select">
            <div 
              class="category-option" 
              :class="{ active: newTask.project === 'drama' }"
              @click="newTask.project = 'drama'; loadDescriptionGuide()"
            >
              🎬 AI数字短剧
            </div>
            <div 
              class="category-option" 
              :class="{ active: newTask.project === 'tk' }"
              @click="newTask.project = 'tk'; loadDescriptionGuide()"
            >
              🛒 TK东南亚运营
            </div>
          </div>
        </div>
        
        <!-- 任务标题 (智能验证) -->
        <div class="form-group">
          <label>📝 任务标题</label>
          <input 
            v-model="newTask.title" 
            @input="validateTitle"
            :class="{ 'input-error': !titleValidation.valid }"
            placeholder="例如：武松打虎第2集复仇爽剧"
          />
          <!-- 验证错误 -->
          <div v-if="titleValidation.errors?.length" class="validation-msg error">
            <span>⚠️</span> {{ titleValidation.errors[0] }}
          </div>
          <!-- 智能建议 -->
          <div v-if="titleValidation.suggestions?.length" class="validation-msg suggestion">
            <span>💡</span> {{ titleValidation.suggestions[0] }}
          </div>
        </div>
        
        <!-- 智能推荐模板 -->
        <div v-if="recommendedTemplate" class="smart-recommend">
          <div class="recommend-header">📌 智能推荐</div>
          <div class="recommend-content">
            <div class="recommend-name">{{ recommendedTemplate.name }}</div>
            <div class="recommend-desc">{{ recommendedTemplate.description }}</div>
            <div class="recommend-meta">
              <span>⏱️ {{ recommendedTemplate.time_estimate }}</span>
              <span>📋 {{ recommendedTemplate.best_practices?.length || 0 }}项最佳实践</span>
            </div>
            <!-- 最佳实践列表 -->
            <div class="best-practices" v-if="recommendedTemplate.best_practices?.length">
              <span v-for="bp in recommendedTemplate.best_practices" :key="bp" class="bp-tag">{{ bp }}</span>
            </div>
          </div>
        </div>
        
        <!-- 任务描述 -->
        <div class="form-group">
          <label>📋 任务描述</label>
          <textarea 
            v-model="newTask.description" 
            placeholder="描述您的任务需求..."
            rows="3"
          ></textarea>
          <!-- 描述填写指引 -->
          <div v-if="descriptionGuide.length" class="guide-box">
            <div class="guide-title">💡 填写指引</div>
            <ul>
              <li v-for="(item, idx) in descriptionGuide" :key="idx">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-secondary" @click="showTaskModal = false">取消</button>
        <button 
          class="btn-primary" 
          @click="createTask"
          :disabled="!titleValidation.valid || !newTask.title"
        >
          🚀 创建并启动
        </button>
      </div>
    </div>
  </div>

  <!-- 里程碑详情抽屉 -->
  <div v-if="showMilestoneDrawer" class="drawer-overlay" @click.self="showMilestoneDrawer = false">
    <div class="drawer">
      <div class="drawer-header">
        <h3>里程碑详情</h3>
        <button class="close-btn" @click="showMilestoneDrawer = false">×</button>
      </div>
      <div class="drawer-body" v-if="milestoneDetails">
        <div class="detail-section">
          <div class="detail-label">里程碑</div>
          <div class="detail-value">{{ milestoneDetails.name }}</div>
        </div>
        <div class="detail-section">
          <div class="detail-label">状态</div>
          <span class="status-badge" :style="{ background: statusMap[milestoneDetails.status]?.color + '20', color: statusMap[milestoneDetails.status]?.color }">
            {{ statusMap[milestoneDetails.status]?.label || milestoneDetails.status }}
          </span>
        </div>
        <div class="detail-section" v-if="milestoneDetails.executor">
          <div class="detail-label">执行者</div>
          <div class="detail-value">{{ milestoneDetails.executor }}</div>
        </div>
        
        <!-- 执行详情 -->
        <div v-if="milestoneDetails.execution_details" class="execution-details">
          <div class="detail-section">
            <div class="detail-label">执行命令</div>
            <code class="detail-code">{{ milestoneDetails.execution_details.command }}</code>
          </div>
          <div class="detail-section">
            <div class="detail-label">耗时</div>
            <div class="detail-value">{{ milestoneDetails.execution_details.duration }}s</div>
          </div>
          <div class="detail-section" v-if="milestoneDetails.execution_details.stdout_preview">
            <div class="detail-label">输出预览</div>
            <pre class="detail-pre">{{ milestoneDetails.execution_details.stdout_preview }}</pre>
          </div>
          <div class="detail-section" v-if="milestoneDetails.execution_details.log_file">
            <div class="detail-label">日志文件</div>
            <div class="detail-value">{{ milestoneDetails.execution_details.log_file }}</div>
          </div>
        </div>
        
        <!-- 预期产出物 -->
        <div class="detail-section" v-if="milestoneDetails.expected_artifacts?.length">
          <div class="detail-label">📦 预期产出物</div>
          <div class="artifact-list">
            <span v-for="a in milestoneDetails.expected_artifacts" :key="a" class="artifact-item">{{ typeof a === 'object' ? (a.name || a.title || JSON.stringify(a)) : a }}</span>
          </div>
        </div>
        
        <!-- 实际产出内容 (第九阶段核心) - 统一 data 结构 -->
        <div v-if="milestoneDetails.execution_details?.output_content" class="output-section">
          <div class="detail-section">
            <div class="detail-label">📋 产出内容</div>
            <span class="status-badge" style="background: rgba(76, 175, 80, 0.2); color: #4caf50;">
              {{ milestoneDetails.execution_details.output_content.type }}
            </span>
          </div>
          
          <!-- data.candidates 候选剧本 -->
          <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.data?.candidates?.length">
            <div class="detail-label">📜 候选剧本</div>
            <div class="candidates-list">
              <div v-for="c in milestoneDetails.execution_details.output_content.data.candidates" :key="c.id" class="candidate-item">
                <div class="candidate-title">{{ c.title }} <span class="score">({{ c.score }})</span></div>
                <div class="candidate-summary">{{ c.summary }}</div>
              </div>
            </div>
          </div>
          
          <!-- data.roles 角色设计 -->
          <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.data?.roles?.length">
            <div class="detail-label">🎭 角色设计</div>
            <div class="roles-list">
              <div v-for="r in milestoneDetails.execution_details.output_content.data.roles" :key="r.character" class="role-item">
                <strong>{{ r.character }}</strong>: {{ r.voice }} / {{ r.personality || r.traits?.join(', ') }}
              </div>
            </div>
          </div>
          
          <!-- data.script 完整剧本 -->
          <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.data?.script">
            <div class="detail-label">📄 剧本内容</div>
            <pre class="detail-pre content-scroll">{{ milestoneDetails.execution_details.output_content.data.script }}</pre>
          </div>
          
          <!-- data.detected_issues 争议分析 -->
          <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.data?.detected_issues?.length">
            <div class="detail-label">⚠️ 争议检测</div>
            <div class="issues-list">
              <div v-for="issue in milestoneDetails.execution_details.output_content.data.detected_issues" :key="issue.issue" class="issue-item" :class="issue.severity">
                <strong>{{ issue.issue }}</strong>
                <span class="suggestion">建议: {{ issue.suggestion }}</span>
              </div>
            </div>
          </div>
          
          <!-- 回退兼容: content 字段 -->
          <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.content">
            <div class="detail-label">内容</div>
            <pre class="detail-pre content-scroll">{{ milestoneDetails.execution_details.output_content.content }}</pre>
          </div>
        </div>
        
        <!-- 决策点交互区域 -->
        <div v-if="milestoneDetails.decision_required" class="decision-section">
          <div class="decision-header">🚨 待决策</div>
          
          <!-- 产出内容预览 -->
          <div v-if="milestoneDetails.execution_details?.output_content" class="output-preview">
            <div class="detail-section">
              <div class="detail-label">产出类型</div>
              <span class="status-badge" style="background: rgba(255, 152, 0, 0.2); color: #ff9800;">
                {{ milestoneDetails.execution_details.output_content.type }}
              </span>
            </div>
            <div class="detail-section">
              <div class="detail-label">产出标题</div>
              <div class="detail-value">{{ milestoneDetails.execution_details.output_content.title }}</div>
            </div>
            <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.content">
              <div class="detail-label">内容预览</div>
              <pre class="detail-pre">{{ milestoneDetails.execution_details.output_content.content.substring(0, 500) }}</pre>
            </div>
            <div class="detail-section" v-if="milestoneDetails.execution_details.output_content.suggestions?.length">
              <div class="detail-label">💡 建议方案</div>
              <ul class="suggestions-list">
                <li v-for="s in milestoneDetails.execution_details.output_content.suggestions" :key="s">{{ s }}</li>
              </ul>
            </div>
          </div>
          
          <!-- 决策选项 -->
          <div class="decision-options">
            <div class="detail-label">选择操作</div>
            <div class="option-buttons">
              <button 
                v-for="opt in milestoneDetails.decision_options" 
                :key="opt"
                class="btn-decision"
                :class="getDecisionBtnClass(opt)"
                @click="handleDecision(opt)"
                :disabled="isExecuting"
              >
                {{ opt }}
              </button>
            </div>
            <div v-if="showDecisionInput" class="decision-input">
              <textarea v-model="decisionComment" placeholder="输入修改意见..." rows="3"></textarea>
              <button class="btn-primary" @click="submitDecision">提交决策</button>
            </div>
          </div>
        </div>
        
        <!-- 执行按钮 -->
        <div class="action-buttons" v-if="!milestoneDetails.decision_required && milestoneDetails.status !== 'completed'">
          <button 
            class="btn-primary" 
            @click="executeMilestone(selectedTask.id, selectedMilestone)"
            :disabled="isExecuting"
          >
            {{ isExecuting ? '执行中...' : '▶ 执行此阶段' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.toolbar { display: flex; gap: 12px; margin-bottom: 16px; }
.btn-primary { background: var(--accent-blue); color: #fff; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border); padding: 10px 20px; border-radius: 8px; cursor: pointer; }

.table-view { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { text-align: left; padding: 12px 16px; font-weight: 500; color: var(--text-secondary); border-bottom: 1px solid var(--border); }
td { padding: 16px; border-bottom: 1px solid var(--border); vertical-align: top; }
.task-row:hover { background: var(--bg-hover); }
.task-name { font-weight: 500; margin-bottom: 4px; }
.task-desc { font-size: 13px; color: var(--text-secondary); }
.mono { font-family: 'SF Mono', monospace; font-size: 12px; color: var(--text-muted); }
.status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.empty-state { text-align: center; padding: 48px; color: var(--text-muted); }

/* 里程碑进度 */
.milestone-progress { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.progress-text { font-size: 12px; color: var(--text-secondary); min-width: 30px; }
.progress-bar { flex: 1; height: 4px; background: var(--bg-secondary); border-radius: 2px; max-width: 80px; }
.progress-fill { height: 100%; background: var(--accent-blue); border-radius: 2px; transition: width 0.3s; }
.milestone-list { display: flex; gap: 4px; flex-wrap: wrap; }
.milestone-dot { width: 12px; height: 12px; border-radius: 50%; cursor: pointer; border: 2px solid var(--bg-primary); }
.milestone-dot.pending { background: #ff9800; }
.milestone-dot.running { background: #2196f3; }
.milestone-dot.completed { background: #4caf50; }
.milestone-dot.failed { background: #f44336; }
.milestone-dot.small { width: 8px; height: 8px; }

/* 看板 */
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
.card-title { font-weight: 500; margin-bottom: 8px; }
.card-milestones { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 8px; }
.card-milestones .more { font-size: 10px; color: var(--text-muted); }
.card-footer { display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-muted); }
.project-tag { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; }
.project-tag.drama { background: rgba(233, 30, 99, 0.15); color: #e91e63; }
.project-tag.tk { background: rgba(94, 106, 210, 0.15); color: #5e6ad2; }
.project-tag.small { padding: 2px 6px; font-size: 11px; }

/* 弹窗 */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.drawer-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; }
.modal { background: var(--bg-card); border-radius: 12px; width: 480px; max-width: 90%; max-height: 90vh; overflow: auto; }
.drawer { background: var(--bg-card); border-radius: 12px 0 0 12px; width: 500px; max-width: 90%; height: 100vh; position: fixed; right: 0; top: 0; overflow: auto; }
.modal-header, .drawer-header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid var(--border); }
.modal-header h3, .drawer-header h3 { margin: 0; font-size: 18px; }
.close-btn { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--text-secondary); }
.modal-body, .drawer-body { padding: 20px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 20px; border-top: 1px solid var(--border); }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-weight: 500; font-size: 14px; }
.form-group select, .form-group input, .form-group textarea { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-secondary); color: var(--text-primary); font-size: 14px; }
.form-group textarea { min-height: 80px; resize: vertical; }

.detail-section { margin-bottom: 16px; }
.detail-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }
.detail-value { font-size: 14px; }
.detail-code { display: block; background: var(--bg-secondary); padding: 8px 12px; border-radius: 6px; font-size: 12px; overflow-x: auto; }
.detail-pre { background: var(--bg-secondary); padding: 12px; border-radius: 6px; font-size: 12px; max-height: 200px; overflow: auto; white-space: pre-wrap; word-break: break-all; }
.artifact-list { display: flex; flex-wrap: wrap; gap: 8px; }
.artifact-item { background: var(--bg-secondary); padding: 4px 10px; border-radius: 4px; font-size: 12px; }
.action-buttons { margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); }
.execution-details { background: var(--bg-secondary); padding: 16px; border-radius: 8px; margin-top: 16px; }

/* 第八阶段：智能向导样式 */
.category-select { display: flex; gap: 12px; }
.category-option { flex: 1; padding: 16px; border: 2px solid var(--border); border-radius: 8px; cursor: pointer; text-align: center; transition: all 0.2s; }
.category-option:hover { border-color: var(--accent-blue); }
.category-option.active { border-color: var(--accent-blue); background: rgba(56, 189, 248, 0.1); }

.input-error { border-color: #f44336 !important; }
.validation-msg { font-size: 12px; margin-top: 6px; padding: 8px; border-radius: 6px; }
.validation-msg.error { background: rgba(244, 67, 54, 0.1); color: #f44336; }
.validation-msg.suggestion { background: rgba(255, 152, 0, 0.1); color: #ff9800; }

.smart-recommend { background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(99, 102, 241, 0.1)); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 16px; margin-bottom: 16px; }
.recommend-header { font-weight: 600; font-size: 14px; color: #38bdf8; margin-bottom: 8px; }
.recommend-name { font-weight: 600; font-size: 16px; margin-bottom: 4px; }
.recommend-desc { font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; }
.recommend-meta { display: flex; gap: 16px; font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }
.best-practices { display: flex; flex-wrap: wrap; gap: 6px; }
.bp-tag { background: var(--bg-secondary); padding: 4px 10px; border-radius: 4px; font-size: 11px; }

.guide-box { background: rgba(76, 175, 80, 0.1); border-radius: 8px; padding: 12px; margin-top: 8px; }
.guide-title { font-weight: 600; font-size: 13px; color: #4caf50; margin-bottom: 8px; }
.guide-box ul { margin: 0; padding-left: 16px; font-size: 12px; color: var(--text-secondary); }
.guide-box li { margin-bottom: 4px; }

/* 第九阶段：决策交互样式 */
.decision-section { background: linear-gradient(135deg, rgba(255, 152, 0, 0.1), rgba(244, 67, 54, 0.1)); border: 2px solid rgba(255, 152, 0, 0.3); border-radius: 12px; padding: 16px; margin-top: 16px; }
.decision-header { font-size: 16px; font-weight: 600; color: #ff9800; margin-bottom: 12px; }
.output-preview { background: var(--bg-secondary); border-radius: 8px; padding: 12px; margin-bottom: 12px; }
.suggestions-list { margin: 8px 0 0 16px; padding: 0; }
.suggestions-list li { font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }
.decision-options { margin-top: 16px; }
.option-buttons { display: flex; gap: 12px; margin: 12px 0; }
.btn-decision { padding: 10px 20px; border-radius: 8px; border: none; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.btn-decision.btn-approve { background: #4caf50; color: white; }
.btn-decision.btn-modify { background: #ff9800; color: white; }
.btn-decision.btn-default { background: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border); }
.btn-decision:hover { transform: translateY(-2px); }
.decision-input { margin-top: 12px; }
.decision-input textarea { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-secondary); color: var(--text-primary); font-size: 14px; }

/* 第九阶段增强样式 */
.output-section { background: var(--bg-secondary); border-radius: 8px; padding: 16px; margin-top: 16px; }
.content-scroll { max-height: 200px; overflow-y: auto; white-space: pre-wrap; font-size: 12px; }
.candidates-list, .roles-list { margin-top: 8px; }
.candidate-item { background: var(--bg-primary); padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4caf50; }
.candidate-title { font-weight: 600; color: var(--text-primary); }
.candidate-title .score { color: #ff9800; font-size: 12px; }
.candidate-summary { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }
.role-item { padding: 6px 0; border-bottom: 1px solid var(--border); }
.role-item:last-child { border-bottom: none; }
.issues-list { margin-top: 8px; }
.issue-item { padding: 8px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid; }
.issue-item.high { border-color: #f44336; background: rgba(244, 67, 54, 0.1); }
.issue-item.medium { border-color: #ff9800; background: rgba(255, 152, 0, 0.1); }
.issue-item .suggestion { display: block; font-size: 12px; color: var(--text-secondary); margin-top: 4px; }
.role-item:last-child { border-bottom: none; }

/* 时间线视图 */
.timeline-view { padding: 20px; }
.timeline-controls { display: flex; gap: 16px; margin-bottom: 24px; padding: 16px; background: var(--bg-secondary); border-radius: 12px; }
.filter-group { display: flex; align-items: center; gap: 8px; }
.filter-group label { font-size: 13px; color: var(--text-secondary); }
.filter-select { padding: 8px 12px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: var(--text-primary); font-size: 14px; min-width: 140px; }
.timeline-content { display: flex; flex-direction: column; gap: 20px; }
.timeline-empty { text-align: center; padding: 60px; color: var(--text-muted); }
.timeline-task-block { background: var(--bg-secondary); border-radius: 12px; padding: 20px; cursor: pointer; transition: all 0.2s; border: 1px solid var(--border); }
.timeline-task-block:hover { border-color: var(--accent-blue); }
.timeline-task-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.timeline-task-name { font-size: 16px; font-weight: 600; color: var(--text-primary); }
.timeline-task-status { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 500; }
.timeline-task-status.running { background: rgba(76, 175, 80, 0.2); color: '#4caf50'; }
.timeline-task-status.pending { background: rgba(255, 152, 0, 0.2); color: '#ff9800'; }
.timeline-task-status.completed { background: rgba(136, 136, 136, 0.2); color: '#888'; }
.timeline-milestones { display: flex; flex-direction: column; gap: 12px; position: relative; padding-left: 24px; }
.timeline-milestones::before { content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: var(--border); }
.milestone-node { display: flex; align-items: center; gap: 12px; position: relative; padding: 10px 14px; background: var(--bg-card); border-radius: 8px; transition: all 0.2s; cursor: pointer; }
.milestone-node:hover { background: var(--bg-hover); }
.milestone-marker { width: 12px; height: 12px; border-radius: 50%; position: absolute; left: -20px; }
.milestone-node.pending .milestone-marker { background: #ff9800; border: 2px solid var(--bg-secondary); }
.milestone-node.running .milestone-marker { background: #4caf50; animation: pulse 2s infinite; }
.milestone-node.completed .milestone-marker { background: #888; }
.milestone-node.blocked .milestone-marker { background: #f44336; }
.milestone-info { display: flex; flex-direction: column; gap: 4px; }
.milestone-name { font-size: 14px; color: var(--text-primary); }
.milestone-time { font-size: 12px; color: var(--text-muted); }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); } 50% { box-shadow: 0 0 0 6px rgba(76, 175, 80, 0); } }
</style>