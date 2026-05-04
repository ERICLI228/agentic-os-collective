// === charts.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: renderChartPanel
function renderChartPanel() {
  if (document.getElementById('chartPanel')) return;
  const summaryEl = document.getElementById('summaryView');
  const targetEl = (summaryEl && window.getComputedStyle(summaryEl.parentElement).display !== 'none') ? summaryEl : document.getElementById('detail');
  if (!targetEl) return;

  const chartHTML = `<div class="chart-panel" id="chartPanel">
    <div class="chart-hdr">
      <h4>📊 管线数据可视化</h4>
      <div class="chart-filter-tags" style="display:flex;gap:4px;margin-bottom:6px">
        <span data-filter="all" class="chart-tag active" onclick="switchPipelineFilter('all',this)">全部</span>
        <span data-filter="tk" class="chart-tag" onclick="switchPipelineFilter('tk',this)">TK运营</span>
        <span data-filter="drama" class="chart-tag" onclick="switchPipelineFilter('drama',this)">数字短剧</span>
      </div>
      <div class="chart-tabs">
        <span class="chart-tab active" onclick="switchChart('status',this)">状态分布</span>
        <span class="chart-tab" onclick="switchChart('source',this)">数据源</span>
        <span class="chart-tab" onclick="switchChart('pipeline',this)">管线对比</span>
        <span class="chart-tab" onclick="switchChart('timeline',this)">里程碑时间轴</span>
      </div>
    </div>
    <canvas id="mainChart"></canvas>
  </div>`;
  targetEl.insertAdjacentHTML('afterbegin', chartHTML);
  function _ensureChart(){
    if(typeof Chart==='undefined'){setTimeout(_ensureChart,300);return;}
    updateChart('status');
  }
  setTimeout(_ensureChart,200);
}

// @@FUNC: switchChart
function switchChart(mode, tabEl) {
  chartMode = mode;
  document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
  if (tabEl) tabEl.classList.add('active');
  updateChart(mode);
}

// @@FUNC: updateChart
function updateChart(mode) {
  if (!lastData || !lastData.milestones) return;
  var ms = lastData.milestones;
  // v3.7.8: Apply pipeline filter
  if (pipelineFilter !== 'all') {
    ms = ms.filter(function(m){return m.pipeline === pipelineFilter;});
  }
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
  const ctx = document.getElementById('mainChart');
  if (!ctx) return;

  let labels, data, colors;

  if (mode === 'status') {
    const counts = {};
    ms.forEach(m => { counts[m.status] = (counts[m.status] || 0) + 1; });
    labels = Object.keys(counts);
    data = Object.values(counts);
    colors = labels.map(function(status) {
      switch(status) {
        case 'completed': return '#3b82f6';  // 蓝色
        case 'approved': return '#8b5cf6';   // 紫色
        case 'waiting_approval': return '#f59e0b';  // 橙色
        case 'pending': return '#06b6d4';    // 青色
        case 'running': return '#ec4899';    // 粉色
        case 'rejected': return '#ef4444';   // 红色
        default: return '#64748b';           // 石板灰
      }
    });
  } else if (mode === 'source') {
    const counts = {};
    ms.forEach(m => { counts[m.data_source || 'unknown'] = (counts[m.data_source || 'unknown'] || 0) + 1; });
    labels = Object.keys(counts);
    data = Object.values(counts);
    colors = ['#3b82f6', '#f59e0b', '#22c55e', '#8b5cf6', '#666'];
  } else if (mode === 'pipeline') {
    const tk = ms.filter(m => m.pipeline === 'tk');
    const dm = ms.filter(m => m.pipeline === 'drama');
    labels = ['TK运营', '数字短剧'];
    data = [
      tk.filter(m => m.status === 'completed' || m.status === 'approved').length,
      dm.filter(m => m.status === 'completed' || m.status === 'approved').length
    ];
    // Ensure we have valid values to prevent undefined in tooltips
    data = data.map(value => (typeof value !== 'undefined' && value !== null) ? value : 0);
    colors = ['#3b82f6', '#8b5cf6'];
  } else if (mode === 'timeline') {
    labels = ms.map(function(m){return m.fid||m.id});
    data = ms.map(function(m){
      return (m.status==='completed'||m.status==='approved')?100:
             (m.status==='running')?60:
             (m.status==='waiting_approval')?40:
             (m.status==='rejected')?20:10;
    });
    colors = ms.map(function(m){
      if(m.status==='completed'||m.status==='approved') return '#22c55e';
      if(m.status==='running') return '#3b82f6';
      if(m.status==='waiting_approval') return '#f59e0b';
      return '#64748b';
    });
  }

  chartInstance = new Chart(ctx, {
    type: (mode === 'pipeline' || mode === 'timeline') ? 'bar' : 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderColor: '#0f1117',
        borderWidth: 2,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#aaa', font: { size: 10 }, padding: 12 }
        },
        tooltip: {
          backgroundColor: '#1a1d27',
          titleColor: '#e4e6eb',
          bodyColor: '#aaa',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 6,
          callbacks: {
            label: function(context) {
              let label = context.label || '';
              let value = '';

              if (context.parsed !== null) {
                if (mode === 'pipeline') {
                  value = context.parsed.y !== undefined ? context.parsed.y : context.raw;
                } else {
                  value = context.parsed !== undefined ? context.parsed : context.raw;
                }
              } else {
                value = context.raw || 0;
              }

              return label + ': ' + value + ' 项';
            }
          }
        }
      },
      ...((mode === 'pipeline' || mode === 'timeline') ? {
        indexAxis: mode === 'timeline' ? 'y' : 'x',
        scales: {
          x: { ticks: { color: '#888', font: { size: 10 } }, grid: { color: '#222' } },
          y: { beginAtZero: true, ticks: { stepSize: 1, color: '#888' }, grid: { color: '#222' } }
        }
      } : {})
    }
  });
}

// @@FUNC: renderReviewRadar
function renderReviewRadar(data) {
  const canvas = document.getElementById('dm0Radar');
  if (!canvas) return;
  if (radarChartInst) { radarChartInst.destroy(); radarChartInst = null; }
  const dims = data.dimensions || [];
  if (!dims.length){ console.warn('[Radar] No dimension data'); return; }
  // 使用与 renderDM0 一致的四维名称
  var allDims = [
    {name:'编剧质量', score:0},
    {name:'分镜设计', score:0},
    {name:'逻辑一致性', score:0},
    {name:'节奏把控', score:0},
    {name:'场景完整性', score:0},
  ];
  // 多维度名称模糊匹配
  function matchDim(dName){
    if(!dName) return -1;
    for(var i=0;i<allDims.length;i++){
      var a = allDims[i].name;
      if(a.indexOf(dName)>=0||dName.indexOf(a)>=0) return i;
    }
    // Semantic keywords
    var keywords = [
      ['编剧','剧本','writing','script'],
      ['分镜','场景','scene','storyboard'],
      ['逻辑','logic','consistency'],
      ['节奏','pacing','rhythm'],
      ['叙事','narrative','完整性','complete'],
    ];
    for(var i=0;i<keywords.length;i++){
      for(var k=0;k<keywords[i].length;k++){
        if(dName.indexOf(keywords[i][k])>=0) return i;
      }
    }
    return -1;
  }
  dims.forEach(function(d) {
    var idx = matchDim(d.name||'');
    if(idx>=0 && idx<allDims.length){
      allDims[idx].score = typeof d.score==='number'?d.score:(d.total_score||5);
    }
  });
  // 若仍全0，用前5个维度的score
  if(allDims.every(function(d){return d.score===0;})){
    dims.slice(0,5).forEach(function(d,i){if(i<allDims.length){allDims[i].name=d.name||allDims[i].name;allDims[i].score=typeof d.score==='number'?d.score:5;}});
  }
  var labels = allDims.map(function(d){return d.name;});
  var scores = allDims.map(function(d){return d.score;});
  var colors = ['#3b82f680','#8b5cf680','#f59e0b80','#22c55e80','#a78bfa80'];
  var descKeys = {'编剧质量':'编剧规则评审: 剧情遵循基本叙事逻辑','分镜设计':'分镜设计评估: 各场景描述充分、衔接自然','逻辑一致性':'逻辑一致性检查: 因果关系自洽、无逻辑漏洞','节奏把控':'剧情节奏分析: 高潮铺垫合理、张弛有度','场景完整性':'场景完整性评估: 各场景描述完整、过渡流畅'};
  reviewDimDescriptions = allDims.map(function(d){return {name:d.name, score:d.score, desc:descKeys[d.name]||d.name+'评估'};});
  var radarContainer = canvas.parentElement;
  if(!radarContainer) return;
  radarChartInst = new Chart(canvas, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{label: '审核评分', data: scores, backgroundColor: 'rgba(59,130,246,0.2)', borderColor: '#3b82f6', borderWidth: 2, pointBackgroundColor: colors}]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      onClick: function(e, activeEls) { if(activeEls.length){showDimDesc(activeEls[0].index);} },
      scales: { r: { suggestedMin: 0, suggestedMax: 10, ticks: { color: '#94a3b8', backdropColor: 'transparent', stepSize: 2 }, grid: { color: '#334155' }, pointLabels: { color: '#e2e8f0', font: { size: 10 } } } },
      plugins: { legend: { labels: { color: '#e2e8f0' } }, tooltip: { enabled: false } }
    }
  });
}

// @@FUNC: renderProfitChart
function renderProfitChart(msData) {
  var canvas = document.getElementById('profitChart');
  if (!canvas) return;
  if (profitChartInst) { profitChartInst.destroy(); profitChartInst = null; }
  var labels = ['1688成本','国内物流','国际物流','平台佣金','支付手续费','汇率折损','落地成本','净利润'];
  var isCost = [true, true, true, true, true, true, false, false];
  var data = msData && msData.profit_breakdown ? msData.profit_breakdown.map(function(x){return parseFloat(x);}) : [33,8,15,8,3,5,72,30];
  while(data.length < 8) data.push(0);
  profitChartInst = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '金额(¥)',
        data: data.slice(0,8),
        backgroundColor: data.slice(0,8).map(function(v,i){return isCost[i] ? '#ef4444' : '#22c55e';}),
        borderRadius: 4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        y: { ticks: { color: '#e2e8f0', font: {size:10} }, grid: { color: '#334155' } },
        x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' }, beginAtZero: true }
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: function(ctx){return ctx.raw + ' ¥';} } }
      }
    }
  });
}

