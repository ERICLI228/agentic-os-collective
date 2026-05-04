// === misc.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: reTranslate
async function reTranslate(code,btn){
  if(btn) btn.disabled=true;
  if(btn) btn.textContent='处理中...';
  try{
    var resp=await fetch('/api/l10n/retranslate/'+code,{method:'POST'});
    if(resp.ok){
      toastMsg(code+' 翻译重新生成完成',2000,'success');
      // Refresh MS-2.1 panel
      await loadDetail('MS-2.1');
    }else{
      toastMsg(code+' 翻译重新生成失败',3000,'error');
    }
  }catch(e){
    toastMsg('翻译API调用失败: '+e.message,3000,'error');
  }
  if(btn){
    btn.disabled=false;
    btn.textContent='重新翻译';
  }
}

// @@FUNC: previewVideoPrompt
function previewVideoPrompt(fid, key) {
  const el = document.getElementById('vpedit-' + fid + '-' + key);
  if (!el) {
    toastMsg('视频生成 API 接入中 · Pollo AI / Kling / Seedance · 提示词已就绪', 3500, 'warn');
    return;
  }
  // Toggle preview: close edit form first
  if (el.style.display === 'block') {
    el.style.display = 'none';
  }
  toastMsg('🎬 视频预览: 将在后期通过 Pollo AI / Kling API 生成 · 当前提示词已缓存', 3000);
}

// @@FUNC: editVideoPrompt
function editVideoPrompt(fid, key) {
  const el = document.getElementById('vpedit-' + fid + '-' + key);
  if (!el) return;
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

// @@FUNC: saveVideoPrompt
function saveVideoPrompt(fid, key) {
  const descEl = document.getElementById('vpedit-desc-' + fid + '-' + key);
  const promptEl = document.getElementById('vpedit-prompt-' + fid + '-' + key);
  if (!descEl || !promptEl) return;
  const patch = { descriptor: descEl.value, prompt: promptEl.value };
  // Stage 1: save to localStorage (immediate)
  const cacheKey = 'vp_' + fid + '_' + key;
  localStorage.setItem(cacheKey, JSON.stringify(patch));
  // Stage 2: API call (placeholder — will POST to /api/character/{fid}/video-prompt later)
  toastMsg('💾 提示词已保存 (localStorage) · API 同步待后期接入', 2500);
  // Close edit form
  const el = document.getElementById('vpedit-' + fid + '-' + key);
  if (el) el.style.display = 'none';
}

// @@FUNC: deleteRenderFile
async function deleteRenderFile(fid, filename, btnEl) {
  if (!confirm('确定删除 ' + fid + ' 的角度图 ' + filename + ' ？\n删除后可点击「🔁 重新生成」恢复。')) return;
  if (btnEl) btnEl.textContent = '⏳';
  try {
    var r = await fetch('/api/render/' + fid + '/' + filename, { method: 'DELETE' });
    var d = await r.json();
    if (d.status === 'ok') {
      toastMsg('🗑️ ' + d.message, 2500, 'success');
      // Remove the thumbnail wrapper
      if (btnEl && btnEl.parentElement) btnEl.parentElement.remove();
    } else {
      toastMsg('❌ ' + d.message, 3000, 'error');
      if (btnEl) btnEl.textContent = '✕';
    }
  } catch (e) {
    toastMsg('❌ 删除失败: ' + e.message, 3000, 'error');
    if (btnEl) btnEl.textContent = '✕';
  }
}

// @@FUNC: regenerateCharacter
async function regenerateCharacter(fid, btnEl) {
  if (!confirm('重新生成 ' + fid + ' 的渲染图？\n这将调用 ComfyUI/图片生成管线，约需 1-2 分钟。')) return;
  if (btnEl) { btnEl.disabled = true; btnEl.textContent = '⏳ 提交中...'; }
  toastMsg('🎨 触发 ' + fid + ' 重新渲染...', 5000);
  try {
    var r = await fetch('/api/render/' + fid + '/regenerate', { method: 'POST' });
    var d = await r.json();
    if (d.status === 'ok') {
      toastMsg('✅ ' + d.message + ' · 自动轮询中', 3000, 'success');
      if (btnEl) { btnEl.textContent = '⏳ 渲染中...'; }
      // Poll every 6s for up to 2min, checking for new renders
      var polls = 0, maxPolls = 20;
      var checkRender = function() {
        polls++;
        fetch('/api/character/' + fid)
          .then(function(rr) { return rr.json(); })
          .then(function(data) {
            var renders = data.renders || data.designs || [];
            if (renders.length >= 3 || polls >= maxPolls) {
              if (btnEl) { btnEl.disabled = false; btnEl.textContent = '🔁 重新生成所有角度'; }
              select('DM-1');
              if (renders.length >= 3) toastMsg('✅ ' + fid + ' 渲染完成 (' + renders.length + ' 角度)', 3000, 'success');
              else toastMsg('⚠️ 轮询结束，请手动刷新查看', 3000, 'warn');
            } else {
              if (btnEl) btnEl.textContent = '⏳ 渲染中 (' + (polls*6) + 's)...';
              setTimeout(checkRender, 6000);
            }
          })
          .catch(function() {
            if (polls < maxPolls) setTimeout(checkRender, 6000);
            else { if (btnEl) { btnEl.disabled = false; btnEl.textContent = '🔁 重新生成所有角度'; } select('DM-1'); }
          });
      };
      setTimeout(checkRender, 3000);
    } else {
      toastMsg('❌ ' + (d.message || '提交失败'), 4000, 'error');
      if (btnEl) { btnEl.disabled = false; btnEl.textContent = '🔁 重新生成所有角度'; }
    }
  } catch (e) {
    toastMsg('❌ 生成失败: ' + e.message, 4000, 'error');
    if (btnEl) { btnEl.disabled = false; btnEl.textContent = '🔁 重新生成所有角度'; }
  }
}

// @@FUNC: toggleInfoCard
function toggleInfoCard(headerEl){
  var body=headerEl.nextElementSibling;
  var icon=headerEl.querySelector('.toggle-icon');
  if(!body||!icon)return;
  // 检查是否已绑定 data-toggle 属性
  var toggleId=headerEl.dataset.toggle||body.id;
  if(toggleId) return toggleSection(toggleId);
  if(body.style.display==='none'){
    body.style.display='block';
    icon.innerHTML='&#9650;';
  }else{
    body.style.display='none';
    icon.innerHTML='&#9660;';
  }
}

// @@FUNC: loadVideoPreview
function loadVideoPreview(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body) return;
  var html = '<div class="img-gallery">';
  var found = 0;
  var done = function() {};
  var pending = 5;
  for (var i = 1; i <= 5; i++) {
    var shot = String(i).padStart(2, '0');
    var url = '/api/render/ep' + String(parseInt(epNum)).padStart(2,'0') + '/shot_' + shot + '.png';
    // Use sync-style via async IIFE
    (function(imgUrl, idx) {
      var img = new Image();
      img.onload = function() {
        found++;
        html += '<div class="img-card" onclick="event.stopPropagation();zoomImg(\'' + imgUrl + '\')"><img src="' + imgUrl + '" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜' + String(idx).padStart(2,'0') + '</span></div>';
        pending--;
        if (pending <= 0) {
          if (found > 0) {
            body.innerHTML = html + '</div>';
          } else {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
          // Also render shot sorter
          renderShotSorterInContainer(parseInt(epNum), containerId);
        }
      };
      img.onerror = function() {
        pending--;
        if (pending <= 0) {
          if (found > 0) {
            body.innerHTML = html + '</div>';
          } else {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
          renderShotSorterInContainer(parseInt(epNum), containerId);
        }
      };
      // Timeout bail 3s
      setTimeout(function() {
        if (pending > 0) {
          pending--;
          if (pending <= 0) {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
        }
      }, 3000);
      img.src = imgUrl;
    })(url, i);
  }
}

// @@FUNC: switchPipelineFilter
function switchPipelineFilter(id, el){
  pipelineFilter = id;
  document.querySelectorAll('.chart-tag').forEach(function(t){t.classList.remove('active');});
  if(el) el.classList.add('active');
  updateChart(chartMode);
}

// @@FUNC: initDashboard
(function initDashboard(){
  console.log('[INIT] Dashboard starting, DOM readyState='+document.readyState);
  try {
    refresh();
    setInterval(refresh, 30000);
    console.log('[INIT] refresh() called, 30s polling started');
  } catch(e) {
    console.error('[INIT] FAILED:', e.message);
    var el = document.getElementById('lastRefresh');
    if (el) { el.textContent = 'INIT ERROR: ' + e.message; el.style.color = '#ef4444'; }
  }
})();

function toggleAssetPanel(){
  console.log("assetToggle clicked");
  const p=document.getElementById('assetPanel'),o=document.getElementById('assetOverlay');
  if(p.classList.contains('open')){p.classList.remove('open');o.classList.remove('on')}
  else{p.classList.add('open');o.classList.add('on');loadAssetPanel()}
}
function switchAssetTab(el,type){
  document.querySelectorAll('#assetTabs .asset-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');loadAssetPanel(type);
}
async function loadAssetPanel(type){
  const body=document.getElementById('assetBody');
  body.innerHTML='<div class="loading"><span class="spinner"></span>加载 '+ (type||'全部') +' 资产...</div>';
  let items=[];
  try{
    if(!type||type==='all'||type==='render'){
      const r=await fetch('/api/images');const d=await r.json();
      (d.images||[]).slice(0,50).forEach(img=>items.push({name:img.name,type:'render',url:img.url,character:img.character,size:img.size}));
    }
    if(!type||type==='all'||type==='script'){
      const r=await fetch('/api/script');const d=await r.json();
      (d.episodes||[]).forEach(ep=>items.push({name:'第'+ep.episode+'集',type:'script',episode:ep.episode,file:ep.file||''}));
    }
    if(!type||type==='all'||type==='episode'){
      for(let e=1;e<=10;e++){
        try{
          const r=await fetch('/api/script/'+e);const d=await r.json();
          items.push({name:d.title||'第'+e+'集',type:'episode',episode:e,shots:(d.shots||[]).length,file:'/api/script/'+e});
        }catch(ex){}
      }
    }
  }catch(e){}
  if(!items.length){body.innerHTML='<div style="color:#555;text-align:center;padding:20px;font-size:11px">暂无资产</div>';return;}
  items.sort((a,b)=>a.name.localeCompare(b.name));
  let h='';let count=0;
  items.forEach(it=>{
    if(type&&type!=='all'&&it.type!==type)return;
    count++;
    if(it.type==='render')h+='<div class="asset-item"><img class="thumb" src="'+it.url+'" loading="lazy" onerror="this.style.display=\'none\'"/><div class="info"><div class="name">'+it.character+' · '+it.name+'</div><div class="meta">'+(it.size/1024).toFixed(0)+'KB</div></div><button class="dl-btn" onclick="window.open(\''+it.url+'\')">📥</button></div>';
    else if(it.type==='script')h+='<div class="asset-item"><div class="info"><div class="name">📄 '+it.name+'</div><div class="meta">剧本</div></div><button class="dl-btn" onclick="window.open(&quot;/api/script/&quot;+it.episode+&quot;)">📥</button></div>';
    else h+='<div class="asset-item"><div class="info"><div class="name">🎬 '+it.name+'</div><div class="meta">'+it.shots+'个分镜</div></div></div>';
  });
  body.innerHTML=count?'':'<div style="color:#555;text-align:center;padding:20px;font-size:11px">没有'+type+'类资产</div>'+h;
}

// v3.7 S2-2: Add video preview mock buttons to DM-1 character cards
(function injectPreviewButtons() {
  var checkExist = setInterval(function() {
    var btns = document.querySelectorAll('[id^="rerender-btn-"]');
    if (btns.length > 0) {
      clearInterval(checkExist);
      btns.forEach(function(btn) {
        var fid = btn.id.replace('rerender-btn-', '');
        if (document.getElementById('preview-btn-' + fid)) return;
        var preview = document.createElement('button');
        preview.id = 'preview-btn-' + fid;
        preview.className = 'cb-btn';
        preview.textContent = '🎬 预览动态';
        preview.onclick = function() {
          toastMsg('🎬 视频预览: Pollo AI / Kling API 未配置', 3000, 'warn');
        };
        btn.parentNode.insertBefore(preview, btn);
      });
    }
  }, 1000);
})();



// ================================================================
// Sprint 3: 里程碑内嵌图表 (利润瀑布图 / 审核雷达图 / 管线时间轴)
// ================================================================
let radarChartInst = null;
let timelineChartInst = null;
let profitChartInst = null;

// v3.7.8: 审核五维雷达图 + 点击维度展开文字说明
var reviewDimDescriptions = [];

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
function showDimDesc(index) {
  var d = reviewDimDescriptions[index];
  if(!d) return;
  var existing=document.getElementById('radar-desc-panel');
  if(existing)existing.remove();
  var panel=document.createElement('div');
  panel.id='radar-desc-panel';
  var scoreColor = d.score >= 6 ? '#22c55e' : d.score >= 4 ? '#f59e0b' : '#ef4444';
  panel.style.cssText='margin-top:6px;padding:8px 10px;background:rgba(0,0,0,.2);border-radius:6px;font-size:10px;border-left:3px solid '+scoreColor;
  panel.innerHTML='<strong style="color:'+scoreColor+'">'+d.name+': '+d.score+'/10</strong><br><span style="color:#888">'+d.desc+'</span>';
  var radarContainer = document.getElementById('dm0Radar');
  if(radarContainer) radarContainer.parentElement.appendChild(panel);
}

// v3.7.8: ComfyUI 连接重试
function retryComfyUI(btn){
  if(!btn) return;
  btn.disabled = true;
  btn.textContent = '⏳ 检测中...';
  fetch('http://localhost:8188')
    .then(function(r){
      btn.textContent = '✅ 可达';
      btn.style.color = '#22c55e';
      toastMsg('✅ ComfyUI 连接正常', 3000, 'success');
      // 刷新服务状态
      var svcMonitor = document.getElementById('svcMonitor');
      if(svcMonitor) { svcMonitor.innerHTML = '<span class="loading">刷新状态...</span>'; loadPipelineMonitor(); }
    })
    .catch(function(e){
      btn.textContent = '❌ 不可达';
      btn.style.color = '#ef4444';
      toastMsg('❌ ComfyUI 端口8188不可达，请启动服务', 3000, 'error');
    })
    .finally(function(){
      setTimeout(function(){ btn.disabled = false; btn.textContent = '重试连接'; btn.style.color = ''; }, 5000);
    });
}

function renderPipelineTimeline() {
  const canvas = document.getElementById('timelineChart');
  if (!canvas) return;
  if (timelineChartInst) { timelineChartInst.destroy(); timelineChartInst = null; }
  var ms = lastData.milestones || [];
  if (!ms.length) return;
  var labels = ms.map(function(m){return m.fid||m.id});
  var data = ms.map(function(m){
    var score = (m.status === 'completed' || m.status === 'approved') ? 100 :
                (m.status === 'running') ? 60 :
                (m.status === 'waiting_approval') ? 40 :
                (m.status === 'rejected') ? 20 : 10;
    return score;
  });
  var bgColors = ms.map(function(m) {
    if (m.status === 'completed'||m.status==='approved') return '#22c55e';
    if (m.status === 'running') return '#3b82f6';
    if (m.status === 'waiting_approval') return '#f59e0b';
    return '#64748b';
  });
  timelineChartInst = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{ label: '进度%', data: data, backgroundColor: bgColors, borderRadius: 4, barThickness: 14 }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: { x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' }, max: 100 }, y: { ticks: { color: '#e2e8f0', font: { size: 9 } } } },
      plugins: { legend: { display: false } }
    }
  });
}

// v3.7.8: 8步利润瀑布图
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

// v3.7.8: Auto-render charts when milestone detail opens
function renderMilestoneCharts(fid) {
  if (fid === 'DM-0') {
    var d = lastData.decisions ? lastData.decisions['DM-0'] : null;
    if (d) renderReviewRadar(d);
  } else if (fid === 'MS-1' || fid === 'MS-2') {
    var ms = findMilestone(fid);
    if (ms && ms.meta) renderProfitChart(ms.meta);
  }
}


// @@FUNC: showDimDesc
function showDimDesc(index) {
  var d = reviewDimDescriptions[index];
  if(!d) return;
  var existing=document.getElementById('radar-desc-panel');
  if(existing)existing.remove();
  var panel=document.createElement('div');
  panel.id='radar-desc-panel';
  var scoreColor = d.score >= 6 ? '#22c55e' : d.score >= 4 ? '#f59e0b' : '#ef4444';
  panel.style.cssText='margin-top:6px;padding:8px 10px;background:rgba(0,0,0,.2);border-radius:6px;font-size:10px;border-left:3px solid '+scoreColor;
  panel.innerHTML='<strong style="color:'+scoreColor+'">'+d.name+': '+d.score+'/10</strong><br><span style="color:#888">'+d.desc+'</span>';
  var radarContainer = document.getElementById('dm0Radar');
  if(radarContainer) radarContainer.parentElement.appendChild(panel);
}

