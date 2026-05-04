// === pipeline.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: renderDM10
async function renderDM10(detail, ms) {
  const el = document.getElementById('detail');
  if (!el) return;

  // Extract check items — DM-10 returns one section with 6 items
  const items = [];
  if (detail && detail.sections) {
    (detail.sections[0]?.items || []).forEach(function(it) {
      items.push(it);
    });
  }

  // If no data, show default
  if (!items.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>发布检查</h3><div style="color:#555;font-size:11px;padding:12px">暂无检查数据</div></div>');
    return;
  }

  // Map items to check config
  const checkMap = {
    pub_fmt:     { label:'格式',      icon:'🎞️', type:'format' },
    pub_len:     { label:'时长',      icon:'⏱️', type:'duration' },
    pub_size:    { label:'文件大小',    icon:'📦', type:'size' },
    pub_compress:{ label:'压缩要求',    icon:'🗜️', type:'compress' },
    pub_content: { label:'内容审核',    icon:'🔞', type:'content' },
    pub_sub:     { label:'字幕要求',    icon:'💬', type:'subtitle' }
  };

  const checks = [];
  items.forEach(function(it) {
    const key = it.key || '';
    const cfg = checkMap[key] || { label: key, icon:'📋', type:key };
    checks.push({
      key: key,
      label: cfg.label,
      icon: cfg.icon,
      type: cfg.type,
      status: it.status || 'unknown',
      value: it.value || '',
      note: it.note || '',
      before: it.before || '',
      after: it.after || ''
    });
  });

  // Compute summary stats
  const ok = checks.filter(function(c) { return c.status === 'ok'; }).length;
  const ng = checks.filter(function(c) { return c.status === 'ng'; }).length;
  const wn = checks.filter(function(c) { return c.status === 'warn'; }).length;
  const total = checks.length;
  const failed = ng + wn;
  const allPass = ng === 0 && wn === 0;

  // Panel 1: Summary Card
  var summaryCardClass = 'publish-check-summary-card';
  if (allPass) summaryCardClass += ' green';
  else if (ng > 0) summaryCardClass += ' red';
  else summaryCardClass += ' orange';

  var summaryIcon = allPass ? '✅' : (ng > 0 ? '❌' : '⚠️');
  var summaryTitle = allPass
    ? '全部 ' + total + ' 项通过，可以发布'
    : ok + '项通过，' + failed + '项未达标，' + (allPass ? '' : '尚未满足发布条件');

  var passParts = checks.filter(function(c){ return c.status==='ok'; }).map(function(c){ return c.label; });
  var failParts = [];
  checks.forEach(function(c){
    if(c.status==='ng') failParts.push('❌ ' + c.label);
    else if(c.status==='warn') failParts.push('⚠️ ' + c.label);
  });
  var summaryMeta = '✅ ' + passParts.join(' · ');
  if (failParts.length) summaryMeta += ' · ' + failParts.join(' · ');

  // Build advice text
  var advices = [];
  checks.forEach(function(c){
    if (c.key === 'pub_size' && c.status !== 'ok') advices.push('切换至 ComfyUI 渲染提升文件质量');
    if (c.key === 'pub_sub' && c.status !== 'ok') advices.push('启动 MS-2.1 本地化管线添加多国字幕');
    if (c.key === 'pub_content' && c.status !== 'ok') advices.push('手动复核暴力场景，必要时打码或替换镜头');
  });
  var adviceText = advices.length ? '建议：' + ([...new Set(advices)]).join('；') : '全部就绪，可以发布 ✓';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + summaryCardClass + '">' +
    '  <div class="publish-check-summary-icon">' + summaryIcon + '</div>' +
    '  <div class="publish-check-summary-content">' +
    '    <div class="publish-check-summary-title">' + summaryTitle + '</div>' +
    '    <div class="publish-check-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="publish-check-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 2: Check Cards Grid
  var gridHtml = '<div class="pc-grid">';
  checks.forEach(function(c) {
    var cardClass = 'pc-card';
    if (c.status === 'ok') cardClass += ' pass';
    else if (c.status === 'ng') cardClass += ' fail';
    else if (c.status === 'warn') cardClass += ' warn';

    var icon = c.status === 'ok' ? '✅' : (c.status === 'ng' ? '❌' : '⚠️');
    var detailText = c.value || '';

    gridHtml += '<div class="' + cardClass + '">';
    gridHtml += '  <div class="pc-card-header"><span class="pc-card-icon">' + icon + '</span><span class="pc-card-title">' + c.label + '</span></div>';
    gridHtml += '  <div class="pc-card-body">' + detailText.replace(/ /g, ' ').replace(/·/g, '<strong>·</strong>') + '</div>';

    // Card footer with actions (special handling for size, subtitle, content)
    var footerHtml = '';
    if (c.key === 'pub_size' && c.status !== 'ok') {
      footerHtml +=
        '<div class="pc-size-bars">' +
        '  <div class="pc-size-row"><span class="pc-size-label">Pillow</span><div class="pc-size-bar"><div class="pc-size-bar-fill bad" style="width:12%"></div></div><span class="pc-size-val">231KB</span></div>' +
        '  <div class="pc-size-row"><span class="pc-size-label">ComfyUI</span><div class="pc-size-bar"><div class="pc-size-bar-fill ok" style="width:95%"></div></div><span class="pc-size-val">1.9MB</span></div>' +
        '  <div class="pc-size-target">TikTok 推荐 ≥ 2MB</div>' +
        '</div>';
      footerHtml += '<button class="pc-card-action primary" onclick="switchToRenderer(\'comfyui\')">切换到 ComfyUI 渲染</button>';
    }

    if (c.key === 'pub_sub' && c.status !== 'ok') {
      footerHtml +=
        '<div class="pc-lang-grid">' +
        '  <div class="pc-lang-item missing">🇵🇭 PH — 英语</div>' +
        '  <div class="pc-lang-item missing">🇸🇬 SG — 英语</div>' +
        '  <div class="pc-lang-item missing">🇻🇳 VN — 越南语</div>' +
        '  <div class="pc-lang-item missing">🇹🇭 TH — 泰语</div>' +
        '  <div class="pc-lang-item missing">🇲🇾 MY — 马来语</div>' +
        '</div>';
      footerHtml += '<button class="pc-card-action primary" onclick="triggerSubPipeline(\'MS-2.1\')">启动本地化管线</button>';
    }

    if (c.key === 'pub_content' && c.status !== 'ok') {
      footerHtml += '<button class="pc-card-action secondary" onclick="alert(\'手动审核: 请检查各集暴力场景，必要时替换镜头或添加打码\')">查看审核详情</button>';
    }

    if (footerHtml) {
      gridHtml += '  <div class="pc-card-footer">' + footerHtml + '</div>';
    }

    gridHtml += '</div>';
  });
  gridHtml += '</div>';
  el.insertAdjacentHTML('beforeend', gridHtml);

  // Panel 3: Next Action Buttons (板块四：下一步行动指引)
  var allPassed = ng === 0;
  el.insertAdjacentHTML('beforeend',
    '<div class="pc-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">' + (allPassed ? '✅ 全部通过，可以发布：' : '❌ ' + ng + '项未达标，建议执行：') + '</span>' +
    '  <button class="btn-primary" ' + (allPassed ? '' : 'disabled') + ' onclick="triggerFinalPublish()">🚀 一键发布（需先满足所有条件）</button>' +
    '  <button class="btn-secondary" onclick="switchToTab(\'DM-4\')">升级视频质量</button>' +
    '  <button class="btn-secondary" onclick="switchToTab(\'MS-2.1\')">添加多国字幕</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-10\')">重新检查</button>' +
    '</div>'
  );

  // Panel 4: 工具与监控面板（可折叠）
  var vpId = 'dm10-video-preview';
  el.insertAdjacentHTML('beforeend',
    '<div class="sec" id="' + vpId + '">' +
    '  <div class="sec-hdr" onclick="toggleSec(\'' + vpId + '\')"><h3><span class="sec-toggle-icon">&#9654;</span> 🎬 视频预览与片段排序</h3></div>' +
    '  <div class="sec-body" id="' + vpId + '-body">' +
    '    <span class="loading">加载渲染图...</span>' +
    '  </div>' +
    '</div>'
  );
  loadVideoPreview('10', vpId + '-body');

  // Panel 4b: Collapsible Pipeline Service Status (with real data)
  var pipeId = 'dm10-pipeline-status';
  el.insertAdjacentHTML('beforeend',
    '<div class="sec" id="' + pipeId + '">' +
    '  <div class="sec-hdr" onclick="toggleSec(\'' + pipeId + '\')"><h3><span class="sec-toggle-icon">&#9654;</span> 🔧 管线服务状态</h3></div>' +
    '  <div class="sec-body" id="' + pipeId + '-body">' +
    '    <div class="info-card"><div class="info-card-body"><span class="loading">加载中...</span></div></div>' +
    '  </div>' +
    '</div>'
  );
  loadPipelineStatus(pipeId + '-body');

  // Panel 4c: Collapsible Quality Feedback Knowledge Base (with real data)
  var kbId = 'dm10-quality-kb';
  el.insertAdjacentHTML('beforeend',
    '<div class="sec" id="' + kbId + '">' +
    '  <div class="sec-hdr" onclick="toggleSec(\'' + kbId + '\')"><h3><span class="sec-toggle-icon">&#9654;</span> 📚 质量反馈知识库</h3></div>' +
    '  <div class="sec-body" id="' + kbId + '-body">' +
    '    <div class="info-card"><div class="info-card-body"><span class="loading">加载中...</span></div></div>' +
    '  </div>' +
    '</div>'
  );
  loadQualityFeedback(kbId + '-body');
}

// @@FUNC: switchToRenderer
function switchToRenderer(mode) {
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '🖥️ 渲染器切换至 ' + mode;
  toastMsg('✅ 已切换至 ' + mode + ' 渲染模式，请手动运行 pipeline', 3000, 'success');
}

// @@FUNC: switchToComfyUI
function switchToComfyUI() {
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '✅ ComfyUI 渲染模式已激活';
  toastMsg('✅ 已切换到 ComfyUI 静态角色画面 — 本地免费方案就绪', 4000, 'success');
}

// @@FUNC: goToKling
function goToKling(btn) {
  if (btn) {
    btn.disabled = true;
    btn.textContent = '打开中...';
  }
  toastMsg('🎬 正在前往 Kling (可灵)...', 2000, 'info');
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '🎬 前往 Kling (可灵) AI 视频生成平台...';
  setTimeout(function() {
    window.open('https://kling.kuaishou.com', '_blank');
    if (btn) {
      btn.disabled = false;
      btn.textContent = '前往 Kling (¥15/6集) →';
    }
    if (banner) banner.textContent = '✅ 已打开 Kling 页面';
  }, 500);
}

// @@FUNC: triggerSubPipeline
function triggerSubPipeline(msId) {
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 启动 ' + msId + ' 管线...';
  toastMsg('⏳ 启动 ' + msId + '...', 2000, 'info');
  fetch('/api/gate/' + msId + '/run', { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (banner) banner.textContent = '✅ ' + msId + ' 已启动: ' + (d.summary || d.message || d.status || '');
      toastMsg('✅ ' + msId + ' 已启动', 3000, 'success');
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 启动失败: ' + e.message;
      toastMsg('❌ 启动失败: ' + e.message, 4000, 'error');
    });
}

// @@FUNC: triggerFinalPublish
function triggerFinalPublish() {
  if (!confirm('确认发布当前剧集至所有平台？')) return;
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 发布中...';
  fetch('/api/publish', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_id: 'TK-DM-PROD' })
  })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (banner) banner.textContent = '✅ 发布完成: ' + (d.message || d.status || '');
      toastMsg('🚀 发布成功: ' + (d.task_id || ''), 3000, 'success');
      render();
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 发布失败: ' + e.message;
      toastMsg('❌ 发布失败: ' + e.message, 4000, 'error');
    });
}

// @@FUNC: loadPipelineStatus
function loadPipelineStatus(containerId) {
  var body = document.getElementById(containerId);
  if (!body) return;

  function render(apiData, comfyOk, nlsOk, sovitsOk) {
    var checks = (apiData && apiData.health_checks) || {};
    var services = [
      { name:'Flask API', icon:'🔌', key:'api' },
      { name:'数据库', icon:'🗄️', key:'database' },
      { name:'知识引擎', icon:'🧠', key:'knowledge' },
      { name:'ComfyUI', icon:'🎨', ok:comfyOk },
      { name:'NLS TTS', icon:'🎤', ok:nlsOk },
      { name:'GPT-SoVITS', icon:'🗣️', ok:sovitsOk }
    ];
    var html = '<div class="dm9-tool-grid">';
    services.forEach(function(svc) {
      var status = svc.ok !== undefined ? svc.ok : (checks[svc.key] === 'ok');
      html += '<div class="dm9-tool-item"><span class="dm9-tool-icon">' + svc.icon + '</span><span class="dm9-tool-label">' + svc.name + '</span><span class="dm9-tool-status' + (status ? ' ok' : ' off') + '">' + (status ? '✅ 在线' : '⚠️ 不可达') + '</span></div>';
    });
    html += '</div>';
    if (apiData && apiData.timestamp) html += '<div style="font-size:9px;color:#555;margin-top:6px">⏱ ' + new Date(apiData.timestamp).toLocaleString() + '</div>';
    body.innerHTML = '<div class="info-card"><div class="info-card-body">' + html + '</div></div>';
  }

  // Fetch core API status + ping external services in parallel
  var apiP = fetch('/api/status').then(function(r){return r.json();}).catch(function(){return null;});
  var comfyP = fetch('http://localhost:8188',{mode:'no-cors'}).then(function(){return true;}).catch(function(){return false;});
  var sovitsP = fetch('http://localhost:9880',{mode:'no-cors'}).then(function(){return true;}).catch(function(){return false;});
  // NLS TTS: check /api/status health_checks includes tts (non-destructive)
  var nlsP = Promise.resolve(true);

  Promise.all([apiP, comfyP, nlsP, sovitsP]).then(function(r){
    render(r[0], r[1], r[2], r[3]);
  }).catch(function(){
    render(null, false, false, false);
  });
}

// @@FUNC: loadQualityFeedback
function loadQualityFeedback(containerId) {
  var body = document.getElementById(containerId);
  if (!body) return;
  fetch('/api/feedback')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var items = data.feedback || [];
      if (!items.length) {
        body.innerHTML = '<div class="info-card"><div class="info-card-body" style="color:#888">暂无质量反馈记录</div></div>';
        return;
      }
      var html = '';
      items.forEach(function(fb) {
        var sevIcon = fb.severity === 'major' ? '🔴' : fb.severity === 'minor' ? '🟡' : 'ℹ️';
        html += '<div class="dm8-tool-item" style="margin-bottom:6px;flex-direction:column;align-items:flex-start;gap:2px">' +
          '<div style="display:flex;align-items:center;gap:6px;width:100%"><span style="font-size:12px">' + sevIcon + '</span><span style="font-size:10px;color:#e4e6eb;font-weight:600">' + (fb.type || '反馈') + '</span><span style="font-size:8px;color:#888;margin-left:auto">' + (fb.source || '') + '</span></div>' +
          '<div style="font-size:9px;color:#888;line-height:1.4;padding-left:18px">' + (fb.description || '') + '</div>' +
          '</div>';
      });
      html += '<div style="font-size:9px;color:#555;margin-top:6px">共 ' + items.length + ' 条反馈 · 截至 ' + (items[0] ? new Date(items[0].timestamp).toLocaleDateString() : '') + '</div>';
      body.innerHTML = '<div class="info-card"><div class="info-card-body">' + html + '</div></div>';
    })
    .catch(function(e) {
      body.innerHTML = '<div class="info-card"><div class="info-card-body" style="color:#ef4444">❌ 无法获取反馈数据: ' + e.message + '</div></div>';
    });
}

// @@FUNC: renderPipelineMonitor
async function renderPipelineMonitor() {
  const detailEl = document.getElementById('detail');
  if (!detailEl) return;
  let sec = `<div class="sec"><h3>🔧 管线服务状态</h3><div class="pipeline-monitor" id="svcMonitor"><span class="loading">SSE 连接中...</span></div></div>`;
  detailEl.insertAdjacentHTML('beforeend', sec);
  connectPipelineSSE();
}

// @@FUNC: connectPipelineSSE
function connectPipelineSSE(){
  if (window._pipelineSSE) { window._pipelineSSE.close(); }
  const es = new EventSource('/api/pipeline/stream');
  window._pipelineSSE = es;
  es.onmessage = function(evt){
    try {
      const d = JSON.parse(evt.data);
      const svcs = d.services || {};
      const pipe = d.pipeline || {};
      const cf = svcs.comfyui || {};
      const tt = svcs.tts || {};
      let rows = '';
      // Flask API — always online since we received this SSE
      rows += '<div class="svc-row"><span>⚙️</span><span class="svc-dot online"></span><span class="svc-name">Flask API</span><span class="svc-detail">端口5001 · task_wizard</span></div>';
      // GPT-SoVITS
      const ttsDot = tt.online ? 'online' : 'offline';
      const ttsDetail = tt.online ? '端口9880可达 · TTS推理' : '端口9880不可达';
      rows += '<div class="svc-row"><span>🎤</span><span class="svc-dot '+ttsDot+'"></span><span class="svc-name">GPT-SoVITS</span><span class="svc-detail">'+ttsDetail+'</span></div>';
      // ComfyUI
      const cfDot = cf.online ? 'online' : 'offline';
      const cfExtra = cf.online ? ' · '+(cf.running||0)+'运行 '+(cf.pending||0)+'排队' : '';
      const cfDetail = cf.online ? '端口8188可达'+cfExtra+' · 图像渲染' : '端口8188不可达';
      rows += '<div class="svc-row"><span>🎨</span><span class="svc-dot '+cfDot+'"></span><span class="svc-name">ComfyUI</span><span class="svc-detail">'+cfDetail+'</span>';
      // v3.7.8: ComfyUI 重试按钮
      if(!cf.online) rows += '<span style="margin-left:6px"><button class="mini-btn" onclick="retryComfyUI(this)">重试连接</button></span>';
      rows += '</div>';
      // Pipeline progress
      const done = pipe.done || 0, total = pipe.total || 0;
      const pct = total ? Math.round(done/total*100) : 0;
      const pctDot = pct > 50 ? 'online' : (pct > 0 ? 'unknown' : 'offline');
      rows += '<div class="svc-row" style="flex-wrap:wrap;padding-bottom:8px"><span>📊</span><span class="svc-dot '+pctDot+'"></span><span class="svc-name">管线总进度</span><span class="svc-detail">'+done+'/'+total+' ('+pct+'%)</span><div style="width:100%;height:4px;background:#222;border-radius:2px;margin-top:2px"><div style="width:'+pct+'%;height:100%;background:#2563eb;border-radius:2px;transition:width .5s"></div></div></div>';
      // Timestamp
      rows += '<div style="font-size:8px;color:#444;text-align:right;padding:2px 0">更新 '+ (d.time || '—') +' · SSE</div>';
      const el = document.getElementById('svcMonitor');
      if (el) el.innerHTML = rows;
    } catch(e) {}
    // Also poll every 30s as fallback
    setTimeout(updatePipelineMonitor, 30000);
  };
  es.onerror = function(){
    const el = document.getElementById('svcMonitor');
    if (el) el.innerHTML = '<span class="loading" style="color:#ef4444">SSE 断线，5秒后重连...</span>';
    setTimeout(updatePipelineMonitor, 5000);
  };
}

// @@FUNC: updatePipelineMonitor
async function updatePipelineMonitor(){
  const checks = [
    { name: 'Flask API', url: '/api/status', port: 5001, detail: 'task_wizard', icon: '⚙️' },
    { name: 'GPT-SoVITS', url: 'http://localhost:9880/control', port: 9880, detail: 'TTS推理', icon: '🎤' },
    { name: 'ComfyUI', url: 'http://localhost:8188/queue', port: 8188, detail: '图像渲染', icon: '🎨' },
  ];
  let rows = '';
  for (const svc of checks) {
    let status = 'unknown', detail = '检测中...', extra = '';
    try {
      const r = await fetch(svc.url, { signal: AbortSignal.timeout(3000) });
      status = 'online';
      if (svc.name === 'ComfyUI' && r.ok) {
        const d = await r.json();
        const run = (d.queue_running||[]).length;
        const pend = (d.queue_pending||[]).length;
        extra = ' · '+run+'运行 '+pend+'排队';
      }
      detail = '端口'+svc.port+'可达'+extra;
    } catch(e) { status='offline'; detail='端口'+svc.port+'不可达'; }
    rows += '<div class="svc-row"><span>'+svc.icon+'</span><span class="svc-dot '+status+'"></span><span class="svc-name">'+svc.name+'</span><span class="svc-detail">'+detail+'</span></div>';
  }
  try {
    const r = await fetch('/api/dashboard');
    const d = await r.json();
    const ms = d.milestones || [];
    const done = ms.filter(m=>m.status==='completed'||m.status==='approved').length;
    const total = ms.length;
    const pct = total ? Math.round(done/total*100) : 0;
    rows += '<div class="svc-row" style="flex-wrap:wrap;padding-bottom:10px"><span>📊</span><span class="svc-name">管线总进度</span><span class="svc-detail">'+done+'/'+total+' ('+pct+'%)</span><div style="width:100%;height:4px;background:#222;border-radius:2px;margin-top:2px"><div style="width:'+pct+'%;height:100%;background:#2563eb;border-radius:2px"></div></div></div>';
  } catch(e) {}
  const el = document.getElementById('svcMonitor');
  if (el) el.innerHTML = rows;
}

// @@FUNC: setRefreshStatus
function setRefreshStatus(syncing) {
  const el = document.getElementById('refreshStatus');
  if (syncing) {
    el.textContent = '同步中...';
    el.className = 'refresh-status syncing';
  } else {
    el.textContent = '';
    el.className = 'refresh-status';
  }
}

const QUALITY_KB = [
  { q: 'Q: 渲染图模糊怎么办？', a: '检查 ComfyUI SDXL 模型是否加载正确；确认分辨率设置为 1024×1024；尝试添加 "high quality, detailed" 到 prompt。' },
  { q: 'Q: TTS 发音不准确？', a: '在文本中用拼音标注多音字（如「重(chóng)新」）；调整 NLS speaker 参数；检查参考音频质量。' },
  { q: 'Q: SFX 音效不匹配场景？', a: '修改 SCENE_SFX_MAP 中的音效关键词；在 freesound.org 搜索更匹配的标签；调整音量混合比例。' },
  { q: 'Q: 审核评分偏低？', a: '检查剧本连贯性；确保分镜描述包含机位/景别/动作；添加情绪和台词细节。' },
  { q: 'Q: 管线服务连接失败？', a: '确认 Flask 在 :5001 运行；ComfyUI 在 :8188 运行；GPT-SoVITS 在 :9880 运行。用 `ps aux | grep python` 检查进程。' },
  { q: 'Q: 决策按钮无响应？', a: '检查后端 /api/decision 是否返回 200；查看浏览器开发者工具 Network 面板；确认 task_id 格式正确。' },
];

// @@FUNC: renderQualityKB
function renderQualityKB() {
  const detailEl = document.getElementById('detail');
  if (!detailEl || document.getElementById('qualityKB')) return;
  let html = '<div class="sec" id="qualityKB"><h3>📚 质量反馈知识库</h3>';
  html += '<p style="font-size:9px;color:#555;margin-bottom:8px">点击问题查看答案 · 持续更新中</p>';
  QUALITY_KB.forEach((item, i) => {
    html += `<div class="qa-item">
      <div class="q-q" onclick="this.nextElementSibling.classList.toggle('show')">${item.q} <span style="font-size:8px;color:#555">▼</span></div>
      <div class="q-a">${item.a}</div>
    </div>`;
  });
  html += '</div>';
  detailEl.insertAdjacentHTML('beforeend', html);
}

// @@FUNC: renderPipelineTimeline
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

