// 任务渲染器 - 全透明流水线版本
// 解决 [object Object] 问题

function escapeHtml(text) {
  if (typeof text !== 'string') return JSON.stringify(text);
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function renderMilestone(milestone) {
  return `
    <div class="milestone-item" data-milestone-id="${milestone.id}">
      <div class="milestone-header">
        <strong>${milestone.id}</strong> - ${milestone.name || milestone.id}
        <span class="status badge ${milestone.status}">${milestone.status || 'pending'}</span>
      </div>
      ${renderMilestoneContent(milestone.execution_details)}
      ${renderDecisionButtons(milestone)}
    </div>
  `;
}

function renderMilestoneContent(execution_details) {
  if (!execution_details?.output_content) return '<div class="no-content">等待执行结果...</div>';
  const content = execution_details.output_content;
  if (typeof content === 'object' && content.data) {
    return renderOutputByType(content.type, content.data, content.artifacts);
  }
  // 回退兼容 content 字段
  if (content.content) {
    return `<div class="content-block"><pre>${escapeHtml(content.content)}</pre></div>`;
  }
  return `<div class="content-block"><pre>${JSON.stringify(content, null, 2)}</pre></div>`;
}

function renderOutputByType(type, data, artifacts) {
  switch (type) {
    case 'candidates':
      return renderCandidates(data);
    case 'controversy_analysis':
      return renderControversy(data);
    case 'full_script':
      return renderFullScript(data);
    case 'role_design':
      return renderRoles(data);
    default:
      return `<div class="content-block"><pre>${JSON.stringify(data, null, 2)}</pre></div>`;
  }
}

function renderCandidates(data) {
  if (!data.candidates) return '<div class="no-content">无候选数据</div>';
  return `
    <div class="content-block">
      <h4>📜 候选剧本列表</h4>
      <div class="candidates-list">
        ${data.candidates.map(c => `
          <div class="candidate-item ${data.recommended === c.id ? 'recommended' : ''}">
            <strong>${c.title || c.id}</strong>
            <span class="score">(评分: ${c.score || 'N/A'})</span>
            <p>${escapeHtml(c.summary || '')}</p>
            <button class="btn-select" onclick="selectCandidate('${c.id}')">选择此剧本</button>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function renderControversy(data) {
  return `
    <div class="content-block">
      <h4>⚠️ 争议检测报告</h4>
      ${data.original_script ? `<p><strong>原剧本：</strong><pre>${escapeHtml(data.original_script)}</pre></p>` : ''}
      ${data.detected_issues?.length ? `
        <h5>检测到的问题：</h5>
        ${data.detected_issues.map(i => `
          <div class="issue ${i.severity || 'medium'}">
            <strong>${(i.severity || '警告').toUpperCase()}: ${i.issue}</strong>
            <p>建议: ${i.suggestion || '暂无'}</p>
          </div>
        `).join('')}
      ` : ''}
      ${data.rewritten_script ? `<p><strong>改写后：</strong><pre>${escapeHtml(data.rewritten_script)}</pre></p>` : ''}
    </div>
  `;
}

function renderFullScript(data) {
  return `
    <div class="content-block">
      <h4>📄 完整剧本</h4>
      <pre class="script-preview">${escapeHtml(data.script || '无内容')}</pre>
      <p>字数: ${data.word_count || '未统计'} | 版本: ${data.version || 'v1'}</p>
    </div>
  `;
}

function renderRoles(data) {
  if (!data.roles) return '<div class="no-content">无角色数据</div>';
  return `
    <div class="content-block">
      <h4>🎭 角色设计</h4>
      ${data.roles.map(r => `
        <div class="role-item">
          <strong>${r.character}</strong>: ${r.voice || ''} / ${r.personality || r.traits?.join(', ') || ''}
        </div>
      `).join('')}
    </div>
  `;
}

function renderDecisionButtons(milestone) {
  if (!milestone.decision_point || milestone.status !== 'pending_decision') return '';
  const options = milestone.decision_options || ['通过', '修改', '驳回'];
  return `
    <div class="decision-buttons">
      <h5>📝 决策操作：</h5>
      ${options.map(opt => `
        <button class="btn-decision" onclick="resolveDecision('${milestone.id}', '${opt}')">
          ${getDecisionIcon(opt)} ${opt}
        </button>
      `).join('')}
    </div>
  `;
}

function getDecisionIcon(option) {
  const icons = {'通过': '✅', '修改': '✏️', '驳回': '❌', '确认改写': '✅', '重新改写': '🔄', '保留原版': '⏸️'};
  return icons[option] || '🔵';
}

function renderTaskMilestones(task) {
  const container = document.getElementById('milestones-container');
  if (!container) return;
  container.innerHTML = task.milestones?.map(m => renderMilestone(m)).join('\n') || '无里程碑';
}

function resolveDecision(milestoneId, option) {
  alert(`决策: ${milestoneId} - ${option}`);
}

function selectCandidate(candidateId) {
  alert(`选择剧本: ${candidateId}`);
}

// 全局暴露
window.renderMilestone = renderMilestone;
window.renderTaskMilestones = renderTaskMilestones;
window.resolveDecision = resolveDecision;
window.selectCandidate = selectCandidate;
