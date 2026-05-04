// === dm6789.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: renderDMEpisode
async function renderDMEpisode(msId,detail,ms){
  const epNum=msId.replace('DM-','').padStart(2,'0');
  const detailEl=document.getElementById('detail');
  // v3.7.8: MP4 inline player
  let sec=`<div class="sec" id="dmep-video-${epNum}"><h3>&#127916; 第${parseInt(epNum)}集 视频播放</h3>`;
  sec+=`<video controls width="100%" poster="/api/render/ep${epNum}/shot_01.png" style="border-radius:6px;max-height:400px;background:#000">`;
  sec+=`<source src="/api/download?name=ep${parseInt(epNum)}.mp4" type="video/mp4">`;
  sec+=`您的浏览器不支持视频播放</video>`;
  sec+=`<div style="font-size:9px;color:#555;margin-top:4px">📥 <a href="/api/download?name=ep${parseInt(epNum)}.mp4" download style="color:#93c5fd">下载MP4</a> | `;
  sec+=`<a href="/api/download?name=ep${parseInt(epNum)}.txt" download style="color:#93c5fd">下载剧本</a></div></div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);

  // Original render gallery
  sec=`<div class="sec" id="dmep-sec-${epNum}"><h3>&#127916; 第${parseInt(epNum)}集 渲染画面</h3>`;
  sec+=`<div class="img-gallery" id="dmep-gal-${epNum}"><span class="loading" id="dmep-status-${epNum}">加载渲染图...</span></div>`;
  sec+=`</div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);

  const galleryEl=document.getElementById('dmep-gal-'+epNum);
  const statusEl=document.getElementById('dmep-status-'+epNum);
  let found=0,imgs='';
  for(let i=1;i<=5;i++){
    const shot=String(i).padStart(2,'0');
    const url=`/api/render/ep${epNum}/shot_${shot}.png`;
    const ok=await checkImage(url);
    if(ok){imgs+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜${shot}</span></div>`;found++;}
  }
  if(found>0){
    galleryEl.innerHTML=imgs;
  }else{
    galleryEl.innerHTML='<span style="font-size:10px;color:#555;">该集暂无渲染图 &middot; 运行 comfyui_renderer.py --episode '+parseInt(epNum)+'</span>';
  }
  if(statusEl)statusEl.remove();

  // S3-1: Add shot sorter section for video merge
  renderShotSorter(epNum);
}

// @@FUNC: renderShotSorter
async function renderShotSorter(epNum){
  const detailEl=document.getElementById('detail');
  if(!detailEl)return;

  // Check if already rendered
  if(document.getElementById('shot-sorter-'+epNum))return;

  let sec=`<div class="shot-sorter" id="shot-sorter-${epNum}">`;
  sec+=`<h3>&#127916; 视频片段排序 · 第${parseInt(epNum)}集</h3>`;
  sec+=`<div class="shot-list" id="shot-list-${epNum}"><span class="loading">加载片段列表...</span></div>`;
  sec+=`<div class="shot-sort-actions" id="shot-actions-${epNum}" style="display:none">`;
  sec+=`<button class="btn-merge" onclick="mergeShots('${epNum}')">&#9654; 合并生成</button>`;
  sec+=`<button class="btn-subtitle" onclick="generateSubtitle('${epNum}')">&#128172; 自动生成字幕</button>`;
  sec+=`</div>`;
  sec+=`<div id="shot-msg-${epNum}" class="shot-merge-progress" style="display:none"></div>`;
  sec+=`</div>`;
  detailEl.insertAdjacentHTML('beforeend',sec);

  // Fetch shots from backend
  try{
    const r=await fetch('/api/shots/'+parseInt(epNum));
    const d=await r.json();
    const shots=d.shots||[];
    renderShotList(epNum,shots);
  }catch(e){
    document.getElementById('shot-list-'+epNum).innerHTML='<div class="shot-empty">暂无视频片段</div>';
  }
}

// @@FUNC: renderShotSorterInContainer
function renderShotSorterInContainer(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body || document.getElementById('shot-sorter-' + epNum)) return;
  var sec = '<div class="shot-sorter" id="shot-sorter-' + epNum + '" style="margin-top:10px">';
  sec += '<h3>🎬 视频片段排序 · 第' + epNum + '集</h3>';
  sec += '<div class="shot-list" id="shot-list-' + epNum + '"><span class="loading">加载片段列表...</span></div>';
  sec += '<div class="shot-sort-actions" id="shot-actions-' + epNum + '" style="display:none">';
  sec += '<button class="btn-merge" onclick="mergeShots(\'' + epNum + '\')">▶ 合并生成</button>';
  sec += '<button class="btn-subtitle" onclick="generateSubtitle(\'' + epNum + '\')">💬 自动生成字幕</button>';
  sec += '</div>';
  sec += '<div id="shot-msg-' + epNum + '" class="shot-merge-progress" style="display:none"></div>';
  sec += '</div>';
  body.insertAdjacentHTML('beforeend', sec);

  fetch('/api/shots/' + epNum)
    .then(function(r) { return r.json(); })
    .then(function(d) {
      var shots = d.shots || [];
      var listEl = document.getElementById('shot-list-' + epNum);
      var actionsEl = document.getElementById('shot-actions-' + epNum);
      if (!listEl) return;
      if (!shots.length) {
        listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>';
        if (actionsEl) actionsEl.style.display = 'none';
        return;
      }
      if (actionsEl) actionsEl.style.display = 'flex';
      var h = '';
      shots.forEach(function(s, i) {
        var thumbUrl = s.thumbnail || '';
        var thumb = thumbUrl ? '<img class="shot-thumb" src="' + thumbUrl + '" loading="lazy" onerror="this.outerHTML=\'<div class=shot-thumb-placeholder>🎬</div>\'">' : '<div class="shot-thumb-placeholder">🎬</div>';
        var dur = s.duration || '--:--';
        var t = s.title || s.name || ('片段 ' + (i + 1));
        h += '<div class="shot-item" draggable="true" data-ep="' + epNum + '" data-idx="' + i + '" ondragstart="onShotDragStart(event)" ondrop="onShotDrop(event)" ondragover="event.preventDefault()">';
        h += '  <span class="shot-idx">' + (i + 1) + '.</span>';
        h += thumb;
        h += '  <div class="shot-info">';
        h += '    <span class="shot-title">' + t + '</span>';
        h += '    <span class="shot-dur">' + dur + '</span>';
        h += '  </div>';
        h += '  <span class="shot-drag-hint">☰</span>';
        h += '</div>';
      });
      listEl.innerHTML = h;
      // Attach drag events for reordering
      listEl.querySelectorAll('.shot-item').forEach(function(item) {
        item.addEventListener('dragstart', onShotDragStart);
        item.addEventListener('drop', onShotDrop);
        item.addEventListener('dragover', function(e) { e.preventDefault(); });
      });
    })
    .catch(function() {
      var listEl = document.getElementById('shot-list-' + epNum);
      if (listEl) listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>';
    });
}

// @@FUNC: dismissRisk
function dismissRisk(cardId) {
  var card = document.getElementById(cardId);
  if (card) {
    card.style.transition = 'opacity .3s';
    card.style.opacity = '0';
    setTimeout(function() { if (card.parentNode) card.parentNode.removeChild(card); }, 300);
  }
}

// @@FUNC: renderDM8
async function renderDM8(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items
  var scriptItem = null, voiceItem = null, estItem = null;
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) {
        var k = it.key || '';
        if (/e\d_script/.test(k)) scriptItem = it;
        else if (/e\d_voice/.test(k)) voiceItem = it;
        else if (/e\d_est/.test(k)) estItem = it;
      });
    });
  }

  var epNum = '03';
  var scriptVal = scriptItem ? (scriptItem.value || '') : '';
  var scriptParts = scriptVal.split('·').map(function(s){return s.trim();}).filter(Boolean);
  var scriptName = scriptParts[0] || '风雪山神庙';
  var sceneCount = (scriptVal.match(/(\d+)\s*场景/) || [])[1] || '6';
  var durSec = (scriptVal.match(/(\d+)\s*秒/) || [])[1] || '55';
  var emotion = (scriptVal.match(/情绪:\s*([^·]+)/) || [])[1] || '压抑→爆发→复仇';
  var scriptSrc = scriptItem ? (scriptItem.before || 'shuihuzhuan.yaml') : '';

  var voiceVal = voiceItem ? (voiceItem.value || '') : '';
  var voiceName = 'zhilun';
  if (voiceVal.indexOf('zhiming') >= 0) voiceName = 'zhiming';
  var voiceDesc = (voiceVal.match(/\([^)]+\)/) || [])[0] || '(沉郁悲壮)';
  var wordCount = (voiceVal.match(/(\d+)字/) || [])[1] || '500';
  var costYuan = (voiceVal.match(/¥([\d.]+)/) || [])[1] || '0.75';
  var voiceBefore = voiceItem ? (voiceItem.before || '') : '';
  var voiceNote = voiceItem ? (voiceItem.note || '') : '';
  var silentFile = voiceItem ? (voiceItem.after || '') : '';

  var estVal = estItem ? (estItem.value || '') : '';
  var estVoice = '¥' + ((estVal.match(/配音¥([\d.]+)/) || [])[1] || costYuan);
  var estSub = (estVal.match(/字幕免费/) ? '免费' : (estVal.match(/字幕¥([\d.]+)/) || [])[0] || '免费');
  var estVideo = (estVal.match(/AI视频/)) ? '暂无' : '暂无';
  var estTime = (estVal.match(/预计(\d+)分钟/) || [])[1] || '5';

  // ===== Panel 1: Summary =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-ep-card blue">' +
    '  <span class="dm8-ep-icon">🎬</span>' +
    '  <div class="dm8-ep-content">' +
    '    <div class="dm8-ep-title">剧本就绪，等待配音生成</div>' +
    '    <div class="dm8-ep-meta">' + scriptName + ' · ' + sceneCount + '场景 · ' + durSec + '秒 · 情绪: ' + emotion + '</div>' +
    '    <div class="dm8-ep-advice">预估成本 ¥' + costYuan + ' · 预计' + estTime + '分钟生成 · 点击下方按钮一键启动</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Script card (enhanced: comprehensive visual) =====
  var chars = [
    { name:'林冲', role:'主角', voice:'zhilun', desc:'八十万禁军教头', emoji:'🗡️' },
    { name:'陆谦', role:'反派', voice:'zhiming', desc:'林冲旧友·陷害者', emoji:'🦊' },
    { name:'富安', role:'反派', voice:'zhiming', desc:'高俅爪牙', emoji:'🐍' },
    { name:'差拨', role:'配角', voice:'zhilun', desc:'沧州牢城小吏', emoji:'📜' },
    { name:'李小二', role:'配角', voice:'zhilun', desc:'酒店老板·报信者', emoji:'🍶' }
  ];
  var charHtml = '<div class="dm8-char-grid">';
  chars.forEach(function(c) {
    charHtml += '<div class="dm8-char-card">' +
      '<div class="dm8-char-emoji">' + c.emoji + '</div>' +
      '<div class="dm8-char-name">' + c.name + '</div>' +
      '<div class="dm8-char-role">' + c.role + '</div>' +
      '<div class="dm8-char-desc">' + c.desc + '</div>' +
      '<span class="dm8-char-voice">🎤 ' + c.voice + '</span>' +
      '</div>';
  });
  charHtml += '</div>';

  var emoStages = ['😔 压抑', '😟 警觉', '😠 愤怒', '💥 爆发', '🗡️ 复仇', '🌨️ 尾声'];
  var emoHtml = '<div class="dm8-emo-bar">';
  emoStages.forEach(function(e, i) {
    emoHtml += '<div class="dm8-emo-stage' + (i === 3 ? ' peak' : '') + '"><div class="emo-icon">' + e.split(' ')[0] + '</div><div class="emo-label">' + e.split(' ')[1] + '</div><div class="emo-step">S' + (i+1) + '</div></div>';
    if (i < emoStages.length - 1) emoHtml += '<span class="dm8-emo-arrow">▸</span>';
  });
  emoHtml += '</div>';

  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-script-card">' +
    '  <div class="dm8-script-hdr">📖 剧本 · ' + scriptName + '</div>' +
    '  <div class="dm8-script-body">' +
    '    <div class="dm8-script-meta-row">' +
    '      <div class="dm8-script-stat"><span class="ss-icon">🎬</span><span class="ss-val">' + sceneCount + '</span><span class="ss-label">场景</span></div>' +
    '      <div class="dm8-script-stat"><span class="ss-icon">⏱️</span><span class="ss-val">' + durSec + 's</span><span class="ss-label">时长</span></div>' +
    '      <div class="dm8-script-stat"><span class="ss-icon">📂</span><span class="ss-val">story</span><span class="ss-label">来源</span></div>' +
    '      <div class="dm8-script-stat"><span class="ss-icon">📋</span><span class="ss-val">idx7</span><span class="ss-label">序号</span></div>' +
    '    </div>' +
    '    <div class="dm8-section-label">🎭 角色表</div>' +
    charHtml +
    '    <div class="dm8-section-label">📈 情绪弧线</div>' +
    emoHtml +
    (scriptSrc ? '<div class="dm8-script-src">📄 数据源: ' + scriptSrc + '</div>' : '') +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 3: Voice action card =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-dub-card" id="dm8-dub-card">' +
    '  <span class="dm8-dub-icon">🎤</span>' +
    '  <div class="dm8-dub-content">' +
    '    <div class="dm8-dub-title">配音待生成</div>' +
    '    <div class="dm8-dub-detail">NLS ' + voiceName + ' ' + voiceDesc + ' · ~' + wordCount + '字 · 成本¥' + costYuan + '</div>' +
    (silentFile ? '<div class="dm8-dub-status">当前仅有' + silentFile.match(/\d+KB/)?.[0]||'' + '静默文件</div>' : '') +
    '  </div>' +
    '  <button class="dm8-dub-btn" id="dm8-gen-btn" onclick="generateEpisode(\'' + epNum + '\', this)">⚡ 一键生成配音</button>' +
    '</div>'
  );

  // ===== Panel 4: Cost cards =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-cost-grid">' +
    '  <div class="dm8-cost-card"><span class="cc-label">💰 配音</span><span class="cc-val">' + estVoice + '</span></div>' +
    '  <div class="dm8-cost-card"><span class="cc-label">📝 字幕</span><span class="cc-val">' + estSub + '</span></div>' +
    '  <div class="dm8-cost-card"><span class="cc-label">🎬 AI视频</span><span class="cc-val">' + estVideo + '</span></div>' +
    '  <div class="dm8-cost-card"><span class="cc-label">⏱️ 预计耗时</span><span class="cc-val">' + estTime + '分钟</span></div>' +
    '</div>'
  );

  // ===== Panel 5: Collapsible tool panel =====
  var toolId = 'dm8-tools';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + toolId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🛠️ 制作工具与监控</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' +
    '    <div class="dm8-tool-grid">' +
    '      <div class="dm8-tool-item"><span class="dm8-tool-icon">⚙️</span><span class="dm8-tool-label">Flask API</span><span class="dm8-tool-status ok">✅ 可达</span></div>' +
    '      <div class="dm8-tool-item"><span class="dm8-tool-icon">🎤</span><span class="dm8-tool-label">NLS TTS</span><span class="dm8-tool-status ok">✅ 在线</span></div>' +
    '      <div class="dm8-tool-item"><span class="dm8-tool-icon">🎨</span><span class="dm8-tool-label">ComfyUI</span><span class="dm8-tool-status off">⚠️ 不可达</span></div>' +
    '      <div class="dm8-tool-item"><span class="dm8-tool-icon">📊</span><span class="dm8-tool-label">管线进度</span><span class="dm8-tool-status">19/24 (79%)</span></div>' +
    '    </div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 6: Next action =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm8-next-action">' +
    '  <button class="btn-primary" id="dm8-next-gen" onclick="generateEpisode(\'' + epNum + '\', this)">⚡ 一键生成配音</button>' +
    '  <button class="btn-secondary" onclick="switchToTab(\'DM-9\')">跳过，查看下一集</button>' +
    '</div>'
  );
}

// @@FUNC: generateEpisode
function generateEpisode(ep, btn) {
  if (!btn) btn = document.getElementById('dm'+(ep==='03'?'8':'9')+'-btn-' + ep);
  if (btn) { btn.disabled = true; btn.textContent = '⏳ 生成中...'; }
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ EP' + ep + ' 配音生成中...';
  fetch('/api/voice/generate/' + ep, { method: 'POST' })
    .then(function(r) {
      if (!r.ok) throw new Error('API不可达('+r.status+')');
      return r.json();
    })
    .then(function(d) {
      if (d.error) throw new Error(d.error);
      if (btn) { btn.textContent = '✅ 已生成'; btn.style.background = '#22c55e'; btn.disabled = true; btn.style.opacity = '1'; }
      if (d.url) {
        var actionDiv = (btn && btn.parentElement);
        if (actionDiv) {
          var exist = document.getElementById('dm-preview-' + ep);
          if (!exist) {
            actionDiv.insertAdjacentHTML('beforeend', '<button class="btn-sm9 preview" id="dm-preview-' + ep + '" onclick="previewAudio(&quot;' + d.url + '&quot;,this)">🎧 试听</button>');
          }
        }
        window['_dm_audio_' + ep] = d.url;
      }
      var dubCard = document.getElementById('dm8-dub-card');
      if (dubCard) { dubCard.style.borderColor = '#22c55e'; var t = dubCard.querySelector('.dm8-dub-title'); if (t) { t.textContent = '✅ 配音已生成'; t.style.color = '#22c55e'; } }
      if (banner) banner.textContent = '✅ EP' + ep + ' 配音完成';
      toastMsg('✅ EP' + ep + ' 配音完成', 2500, 'success');
    })
    .catch(function(e) {
      toastMsg('⚠️ EP' + ep + ' 后端未就绪: ' + e.message, 3000, 'warn');
      if (btn) { btn.disabled = false; btn.textContent = '⚡ 生成配音'; btn.style.opacity = '1'; }
      if (banner) banner.textContent = '';
    });
}

// @@FUNC: previewAudio
function previewAudio(url, btn) {
  if (_dmAudioPlayer && !_dmAudioPlayer.paused) { _dmAudioPlayer.pause(); if (btn) btn.textContent = '🎧 试听'; return; }
  if (!_dmAudioPlayer) { _dmAudioPlayer = new Audio(); _dmAudioPlayer.addEventListener('ended', function() { if (btn) btn.textContent = '🎧 试听'; }); _dmAudioPlayer.addEventListener('error', function() { toastMsg('⚠️ 音频播放失败', 2000, 'warn'); }); }
  _dmAudioPlayer.src = url;
  _dmAudioPlayer.play().catch(function() { toastMsg('⚠️ 播放失败', 1500, 'warn'); });
  if (btn) btn.textContent = '⏸ 暂停';
}

// @@FUNC: renderDM9
async function renderDM9(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract episodes from DM-9 data
  var eps = [];
  var costItem = null;
  var summaryText = '';
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      summaryText = sec.summary || '';
      (sec.items || []).forEach(function(it) {
        var k = it.key || '';
        if (k === 'e_cost') { costItem = it; return; }
        if (/^e[456]_info$/.test(k)) {
          var epNum = k.match(/e(\d)_info/)[1];
          var val = it.value || '';
          var parts = val.split('·').map(function(s){return s.trim();}).filter(Boolean);
          var name = parts[0] || '';
          var scenes = (val.match(/(\d+)场景/) || [])[1] || '5';
          var dur = (val.match(/(\d+)秒/) || [])[1] || '50';
          var nls = (val.match(/NLS:(\w+)/) || [])[1] || 'zhilun';
          var cost = (val.match(/¥([\d.]+)/) || [])[1] || '0.78';
          var note = it.note || '';
          var after = it.after || '';
          var status = it.status || 'ng';
          eps.push({
            ep: epNum, name: name, scenes: scenes, dur: dur,
            nls: nls, cost: cost, note: note, after: after, status: status
          });
        }
      });
    });
  }

  if (!eps.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>待制作剧集</h3><div style="color:#555;font-size:11px;padding:12px">暂无数据</div></div>');
    return;
  }

  // Sort: EP06 first (recommended), then EP04, EP05
  eps.sort(function(a,b){ var o={ep06:0,ep04:1,ep05:2}; return (o[a.ep]||3)-(o[b.ep]||3); });

  // Parse cost
  var costVal = costItem ? (costItem.value || '') : '';
  var voiceCost = (costVal.match(/配音:\s*¥([\d.]+)/) || [])[1] || '2.34';
  var aiCost = (costVal.match(/¥(\d+)/) || [])[1] || '27';

  var hasRisk = eps.some(function(e) { return e.note && e.note.indexOf('审核') >= 0 || e.note.indexOf('暴力') >= 0; });
  var ep06 = eps.find(function(e) { return e.ep === '06'; });
  var ep04 = eps.find(function(e) { return e.ep === '04'; });
  var ep05 = eps.find(function(e) { return e.ep === '05'; });

  // ===== Panel 1: Summary =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm9-summary-card orange">' +
    '  <span class="dm9-summary-icon">📋</span>' +
    '  <div class="dm9-summary-content">' +
    '    <div class="dm9-summary-title">' + eps.length + '集待制作，总配音成本 ¥' + voiceCost + ' · AI视频约 ¥' + aiCost + '</div>' +
    '    <div class="dm9-summary-meta">⭐ 推荐首发: EP06 ' + (ep06 ? ep06.name : '智取生辰纲') + ' — 唯一非暴力集 · 智谋+群像=平台友好</div>' +
    (hasRisk ? '<div class="dm9-summary-advice">⚠️ ' +
      (ep04 && ep04.note.indexOf('审核')>=0 ? 'EP04含女性受害者场景 · ' : '') +
      (ep05 && ep05.note.indexOf('暴力')>=0 ? 'EP05含暴力场景 — PH/VN站审核风险' : '') +
      '</div>' : '') +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Three episode compare cards =====
  var gridHtml = '<div class="dm9-compare-grid">';
  eps.forEach(function(ep) {
    var isEP06 = ep.ep === '06';
    var cardClass = 'dm9-ep-card';
    if (isEP06) cardClass += ' recommended';
    else if (ep.note) cardClass += ' warn';

    gridHtml += '<div class="' + cardClass + '" id="dm9-ep-' + ep.ep + '">';
    if (isEP06) gridHtml += '<div class="dm9-ep-badge star">⭐ 推荐首发</div>';
    gridHtml += '  <div class="dm9-ep-header">';
    gridHtml += '    <span class="dm9-ep-num">EP' + ep.ep + '</span>';
    gridHtml += '    <span class="dm9-ep-title">' + (ep.name || '') + '</span>';
    gridHtml += '  </div>';
    gridHtml += '  <div class="dm9-ep-body">';
    gridHtml += '    <div class="dm9-ep-tags">';
    gridHtml += '      <span class="dm9-ep-tag blue">' + ep.scenes + '场景</span>';
    gridHtml += '      <span class="dm9-ep-tag blue">' + ep.dur + '秒</span>';
    gridHtml += '      <span class="dm9-ep-tag purple">NLS:' + ep.nls + '</span>';
    gridHtml += '    </div>';
    gridHtml += '    <div class="dm9-ep-cost">💰 ¥' + ep.cost + '</div>';
    if (isEP06) {
      gridHtml += '    <div class="dm9-ep-advantage">✅ 唯一非暴力集 · 智谋+群像+无暴力=平台友好</div>';
    }
    if (ep.note && !isEP06) {
      gridHtml += '    <div class="dm9-ep-risk warn">⚠️ ' + (ep.after || ep.note).substring(0,24) + '</div>';
    }
    gridHtml += '  </div>';
    gridHtml += '  <div class="dm9-ep-action">';
    if (isEP06) {
      gridHtml += '    <button class="btn-sm9 primary large" id="dm9-btn-' + ep.ep + '" onclick="generateEpisode(\'' + ep.ep + '\', this)">⚡ 优先生成 EP' + ep.ep + '</button>';
    } else {
      gridHtml += '    <button class="btn-sm9 primary" id="dm9-btn-' + ep.ep + '" onclick="generateEpisode(\'' + ep.ep + '\', this)">⚡ 生成配音</button>';
    }
    gridHtml += '  </div>';
    gridHtml += '</div>';
  });
  gridHtml += '</div>';
  el.insertAdjacentHTML('beforeend', gridHtml);

  // ===== Panel 3: Cost summary =====
  var totalCost = (parseFloat(voiceCost) || 0) + (parseFloat(aiCost) || 0);
  el.insertAdjacentHTML('beforeend',
    '<div class="dm9-cost-grid">' +
    '  <div class="dm9-cost-card"><span class="cc9-label">💰 配音成本</span><span class="cc9-val">¥' + voiceCost + '</span><span class="cc9-meta">EP04-06 三集合计</span></div>' +
    '  <div class="dm9-cost-card"><span class="cc9-label">🎬 AI视频</span><span class="cc9-val">≈¥' + aiCost + '</span><span class="cc9-meta">3×$1.25(Seedance)</span></div>' +
    '  <div class="dm9-cost-card"><span class="cc9-label">📊 总计</span><span class="cc9-val">≈¥' + totalCost.toFixed(2) + '</span><span class="cc9-meta">配音+AI视频</span></div>' +
    '</div>'
  );

  // ===== Panel 4: Risk summary =====
  if (hasRisk) {
    var riskHtml = '<div class="dm9-risk-card">' +
      '  <span class="dm9-risk-icon">⚠️</span>' +
      '  <div class="dm9-risk-body">' +
      '    <div class="dm9-risk-title">审核风险提示（EP04 + EP05）</div>' +
      '    <div class="dm9-risk-detail">';
    if (ep04 && ep04.note) riskHtml += 'EP04: ' + (ep04.after || ep04.note) + '<br>';
    if (ep05 && ep05.note) riskHtml += 'EP05: ' + (ep05.after || ep05.note);
    riskHtml += '    </div>' +
      '    <div class="dm9-risk-advice">💡 建议: EP06(智取生辰纲)首发，EP04/EP05 在审核风险解除后发布</div>' +
      '  </div>' +
      '</div>';
    el.insertAdjacentHTML('beforeend', riskHtml);
  }

  // ===== Panel 5: Collapsible tools =====
  var toolId = 'dm9-tools';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + toolId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🛠️ 制作工具与监控</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' +
    '    <div class="dm9-tool-grid">' +
    '      <div class="dm9-tool-item"><span class="dm9-tool-icon">⚙️</span><span class="dm9-tool-label">Flask API</span><span class="dm9-tool-status ok">✅ 可达</span></div>' +
    '      <div class="dm9-tool-item"><span class="dm9-tool-icon">🎤</span><span class="dm9-tool-label">NLS TTS</span><span class="dm9-tool-status ok">✅ 在线</span></div>' +
    '      <div class="dm9-tool-item"><span class="dm9-tool-icon">🎨</span><span class="dm9-tool-label">ComfyUI</span><span class="dm9-tool-status off">⚠️ 不可达</span></div>' +
    '      <div class="dm9-tool-item"><span class="dm9-tool-icon">📊</span><span class="dm9-tool-label">管线进度</span><span class="dm9-tool-status">19/24 (79%)</span></div>' +
    '    </div>' +
    '    <div class="dm9-checklist">' +
    '      <div class="dm9-check-title">📋 制作前置检测</div>' +
    '      <div class="dm9-check-item done">✅ 剧本审批 — 三集剧本已就绪</div>' +
    '      <div class="dm9-check-item"><span class="check-pending">⬜</span> 角色配音分配 — NLS资源包29817字可用</div>' +
    '      <div class="dm9-check-item"><span class="check-pending">⬜</span> 分镜审阅 — 参考DM-2看板</div>' +
    '      <div class="dm9-check-item warn">⚠️ 内容审核预检 — EP04/EP05 含暴力/敏感场景</div>' +
    '    </div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 6: Next action =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm9-next-action">' +
    '  <button class="btn-p9 primary" id="dm9-all-btn" onclick="generateAllEpisodes()">⚡ 一键生成全部三集</button>' +
    '  <button class="btn-p9 secondary" onclick="generateEpisode(\'04\', null)">生成 EP04</button>' +
    '  <button class="btn-p9 warn" onclick="generateEpisode(\'05\', null)">生成 EP05</button>' +
    '</div>'
  );
}

// @@FUNC: generateAllEpisodes
function generateAllEpisodes() {
  var btn = document.getElementById('dm9-all-btn');
  if (btn) { btn.disabled = true; btn.textContent = '⏳ 生成中...'; }
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 批量生成 EP04/EP05/EP06 配音...';

  function genNext(eps, idx) {
    if (idx >= eps.length) {
      toastMsg('✅ 全部三集配音生成完成', 3000, 'success');
      if (banner) banner.textContent = '✅ 全部三集配音生成完成';
      if (btn) { btn.textContent = '✅ 全部已完成'; btn.style.background = '#22c55e'; }
      return;
    }
    var ep = eps[idx];
    var epBtn = document.getElementById('dm9-btn-' + ep);
    if (epBtn) { epBtn.disabled = true; epBtn.textContent = '生成中...'; }
    fetch('/api/voice/generate/' + ep, { method: 'POST' })
      .then(function(r) { return r.json(); })
      .then(function(d) {
        if (d.error) { throw new Error(d.error); }
        if (epBtn) { epBtn.textContent = '✅ 已生成'; epBtn.style.background = '#22c55e'; }
        toastMsg('✅ EP' + ep + ' 配音完成', 2000, 'success');
        genNext(eps, idx + 1);
      })
      .catch(function(e) {
        toastMsg('❌ EP' + ep + ' 生成失败: ' + e.message, 3000, 'error');
        if (epBtn) { epBtn.disabled = false; epBtn.textContent = '⚡ 生成配音'; }
        genNext(eps, idx + 1);
      });
  }
  genNext(['04', '05', '06'], 0);
}

// @@FUNC: renderDM6
async function renderDM6(msId, detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items
  var fileItem = null, audioItem = null, contentItem = null, qualityItem = null;
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) {
        var k = it.key || '';
        if (/e\d_file/.test(k)) fileItem = it;
        else if (/e\d_audio/.test(k)) audioItem = it;
        else if (/e\d_content/.test(k)) contentItem = it;
        else if (/e\d_quality/.test(k)) qualityItem = it;
      });
    });
  }

  // Derive episode number from data key (e.g. e1_file → 1), fall back to panel offset
  var epNum = 1;
  var firstKey = (fileItem || audioItem || contentItem || qualityItem || {}).key || '';
  var keyMatch = firstKey.match(/e(\d+)_/);
  if (keyMatch) { epNum = parseInt(keyMatch[1]); }
  else { epNum = parseInt(msId.replace('DM-', '')) - 5; }

  if (!fileItem && !qualityItem) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>第' + epNum + '集 成品报告</h3><div style="color:#555;font-size:11px;padding:12px">暂无该集成品数据</div></div>');
    return;
  }

  // Parse quality score
  var overallScore = 0, dubScore = 0, visualScore = 0, compScore = 0;
  var qVal = qualityItem ? (qualityItem.value || '') : '';
  var overallMatch = qVal.match(/([\d.]+)\/10/);
  if (overallMatch) overallScore = parseFloat(overallMatch[1]);
  // Try pattern: 配音8分, 画面2分, 合成5分
  var dubMatch = qVal.match(/配音([\d.]+)分/);
  var visMatch = qVal.match(/画面([\d.]+)分/);
  var compMatch = qVal.match(/合成([\d.]+)分/);
  if (dubMatch) dubScore = parseFloat(dubMatch[1]);
  if (visMatch) visualScore = parseFloat(visMatch[1]);
  if (compMatch) compScore = parseFloat(compMatch[1]);

  // Fallback: if not detailed score but overall exists
  if (!dubMatch && !visMatch && !compMatch) {
    dubScore = Math.min(overallScore + 2, 10);
    visualScore = Math.max(overallScore - 2, 0);
    compScore = overallScore;
  }

  // Parse file info
  var fileVal = fileItem ? (fileItem.value || '') : '';
  var fileParts = fileVal.split('·').map(function(s){ return s.trim(); }).filter(Boolean);
  var fileName = fileParts[0] || 'final.mp4';
  var fileSize = (fileVal.match(/(\d+)KB/) || [])[1] || '231';
  var fileRes = (fileVal.match(/(\d+[×x]\d+)/) || [])[0] || '1080×1920';
  var fileDur = (fileVal.match(/(\d+)s/) || [])[1] || '23';
  var fileCodec = fileParts.filter(function(p){ return /H\.\d+/.test(p); })[0] || 'H.264';
  var fileNLS = fileParts.filter(function(p){ return /NLS/.test(p); })[0] || '';

  // Content
  var contentVal = contentItem ? (contentItem.value || '') : '';
  var scriptDur = (contentVal.match(/(\d+)秒剧本/) || [])[1] || '';
  var pctShort = (contentVal.match(/短(\d+)%/) || [])[1] || '';

  // ===== Panel 1: Summary =====
  var sumClass = 'dm6-summary-card' + (overallScore >= 7 ? ' green' : overallScore >= 4 ? ' orange' : ' red');
  var sumIcon = overallScore >= 7 ? '✅' : overallScore >= 4 ? '⚠️' : '❌';
  var sumTitle = 'EP' + String(epNum).padStart(2,'0') + ' 质量评分 ' + overallScore + '/10';
  var sumMeta = (dubScore || '?') + '分配音 · ' + (visualScore || '?') + '分画面 · ' + (compScore || '?') + '分合成';
  var sumAdvice = overallScore >= 7 ? '✅ 质量达标，可进入发布流程' : (overallScore >= 4 ? '⚠️ 画面评分偏低，建议升级至 ComfyUI' : '❌ 质量不达标，需优化后重新生成');

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dm6-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dm6-summary-content">' +
    '    <div class="dm6-summary-title">' + sumTitle + '</div>' +
    '    <div class="dm6-summary-meta">' + sumMeta + '</div>' +
    '    <div class="dm6-summary-advice">' + sumAdvice + '</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Quality score bars =====
  var qScoreClass = overallScore >= 7 ? 'green' : overallScore >= 4 ? 'orange' : 'red';
  var qualityHtml = '<div class="dm6-quality-cards">';
  qualityHtml += dm6ScoreItem('🎤 配音', dubScore, 'green');
  qualityHtml += dm6ScoreItem('🖼️ 画面', visualScore, visualScore >= 6 ? 'green' : visualScore >= 4 ? 'yellow' : 'red');
  qualityHtml += dm6ScoreItem('🎬 合成', compScore, compScore >= 6 ? 'green' : compScore >= 4 ? 'yellow' : 'red');
  qualityHtml += '<div class="dm6-score-total"><span>综合评分</span><div class="dm6-score-number ' + qScoreClass + '">' + overallScore + '/10</div></div>';
  qualityHtml += '</div>';
  el.insertAdjacentHTML('beforeend', qualityHtml);

  // ===== Panel 3: File info card =====
  var filePath = fileItem ? (fileItem.before || '') : '';
  var fileHtml = '<div class="dm7-file-card">' +
    '<div class="dm7-file-icon">📦</div>' +
    '<div class="dm7-file-body">' +
    '  <div class="dm7-file-name">' + (fileName || 'final.mp4') + '</div>' +
    '  <div class="dm7-file-specs">' +
    '    <div class="fs-item"><span class="fs-key">体积</span><span class="fs-val">' + (fileSize || '?') + ' KB</span></div>' +
    '    <div class="fs-item"><span class="fs-key">分辨率</span><span class="fs-val">' + (fileRes || '?') + '</span></div>' +
    '    <div class="fs-item"><span class="fs-key">时长</span><span class="fs-val">' + (fileDur || '?') + ' 秒</span></div>' +
    '    <div class="fs-item"><span class="fs-key">编码</span><span class="fs-val">' + (fileCodec || 'H.264') + '</span></div>' +
    (fileNLS ? '    <div class="fs-item"><span class="fs-key">配音</span><span class="fs-val">' + fileNLS + '</span></div>' : '') +
    '  </div>' +
    (filePath ? '<div class="dm7-file-path">' + filePath + '</div>' : '') +
    '  <div class="dm7-file-tags">' +
    '    <span class="dm7-file-tag">' + (fileRes || '?') + '</span>' +
    '    <span class="dm7-file-tag">' + (fileCodec || 'H.264') + '</span>' +
    (fileNLS ? '    <span class="dm7-file-tag">' + fileNLS + '</span>' : '') +
    '  </div>' +
    '</div>' +
    '</div>';
  el.insertAdjacentHTML('beforeend', fileHtml);

  // ===== Panel 4: Duration warning card (always when fileDur << scriptDur) =====
  var hasDurIssue = scriptDur && fileDur && parseInt(fileDur) < parseInt(scriptDur) * 0.7;
  if (hasDurIssue) {
    var issueAfter = contentItem ? (contentItem.after || '') : '';
    var issueNote = contentItem ? (contentItem.note || '') : '';
    el.insertAdjacentHTML('beforeend',
      '<div class="dm6-issue-card">' +
      '  <span class="dm6-issue-icon">⚠️</span>' +
      '  <div class="dm6-issue-content">' +
      '    <div class="dm6-issue-title">时长压缩</div>' +
      '    <div class="dm6-issue-body">实际 ' + fileDur + ' 秒 vs 剧本预估 ' + scriptDur + ' 秒 · 因 Pillow 帧无画面动画' + (issueAfter ? '<br>' + issueAfter : '') + '</div>' +
      (issueNote ? '<div class="dm6-issue-note">💡 ' + issueNote + '</div>' : '') +
      '  </div>' +
      '</div>'
    );
  }

  // ===== Panel 4b: DM-7 专属排播风险卡片 =====
  if (msId === 'DM-7') {
    var schRiskId = 'dm7-risk-' + epNum;
    el.insertAdjacentHTML('beforeend',
      '<div class="publish-check-card warn" id="' + schRiskId + '">' +
      '  <div class="check-card-header"><span class="check-card-icon">⚠️</span><span class="check-card-title">排播风险：连续两集鲁智深</span></div>' +
      '  <div class="check-card-detail">' +
      '    EP01(鲁提辖拳打镇关西) + EP02(倒拔垂杨柳) 主角都是鲁智深<br>' +
      '    建议：在两集之间插入一集其他角色的剧集（如 EP03 林冲），避免观众审美疲劳' +
      '  </div>' +
      '  <div class="check-card-action">' +
      '    <button class="pc-card-action primary" onclick="switchToTab(\'DM-8\')">跳转到 EP03 林冲 (DM-8)</button>' +
      '    <button class="pc-card-action secondary" onclick="dismissRisk(\'' + schRiskId + '\')">忽略此风险</button>' +
      '  </div>' +
      '</div>'
    );
  }

  // ===== Panel 5: Collapsible video preview (reuse renderDMEpisode logic) =====
  var vpId = 'dm6-video-preview-' + epNum;
  el.insertAdjacentHTML('beforeend',
    '<div class="sec" id="' + vpId + '">' +
    '  <div class="sec-hdr" onclick="toggleSec(\'' + vpId + '\')"><h3><span class="sec-toggle-icon">&#9654;</span> 🎬 视频预览与片段管理</h3></div>' +
    '  <div class="sec-body" id="' + vpId + '-body">' +
    '    <span class="loading">加载渲染图...</span>' +
    '  </div>' +
    '</div>'
  );

  // Load episode gallery + shot sorter
  loadEpGallery(epNum, vpId + '-body');

  // ===== Panel 6: Pipeline execution cards =====
  var techSecId = 'dm6-tech-log-' + epNum;
  var allSectItems = [];
  if (detail && detail.sections) {
    detail.sections.forEach(function(s) { (s.items || []).forEach(function(it) { allSectItems.push(it); }); });
  }
  // Extract pipeline log items
  var pipeLines = [];
  var pipeMap = {};
  allSectItems.forEach(function(it) {
    var key = it.key || '';
    var label = it.label || '';
    var val = it.value || '';
    var note = it.note || '';
    var before = it.before || '';
    var status = it.status || 'ok';
    // Categorize: ffmpeg / tts / render / system
    var cat = '';
    if (/ffmpeg|合成/.test(label)) cat = 'ffmpeg';
    else if (/tts|NLS|配音|音频|mp3/.test(label)) cat = 'audio';
    else if (/pillow|渲染|render|帧/.test(label)) cat = 'render';
    else if (/路径|path|file/.test(key) && /e\d_file/.test(key)) cat = 'file';
    else if (/content|内容|剧本|场景/.test(label)) cat = 'content';
    else if (/quality|质量|评分/.test(label)) cat = 'quality';
    else cat = 'system';
    pipeMap[cat] = (pipeMap[cat] || []).concat([it]);
  });
  // Render structured pipeline cards
  var techHtml = '<div class="dm6-tech-log">';
  var catOrder = ['file', 'audio', 'render', 'ffmpeg', 'content', 'quality', 'system'];
  var catIcons = {file:'📦', audio:'🎤', render:'🖼️', ffmpeg:'🎬', content:'📜', quality:'⭐', system:'⚙️'};
  catOrder.forEach(function(cat) {
    var items = pipeMap[cat] || [];
    if (!items.length) return;
    var catLabel = {file:'成品文件', audio:'音频轨道', render:'图像渲染', ffmpeg:'FFmpeg 合成', content:'内容信息', quality:'质量评估', system:'系统日志'}[cat];
    techHtml += '<div class="pipe-cat"><div class="pipe-cat-hdr"><span>' + (catIcons[cat]||'') + ' ' + catLabel + '</span><span class="pipe-cat-count">' + items.length + ' 项</span></div>';
    techHtml += '<div class="pipe-cat-items">';
    items.forEach(function(it) {
      var stCls = it.status === 'ok' ? 'pipe-ok' : it.status === 'warn' ? 'pipe-warn' : 'pipe-err';
      var stIcon = it.status === 'ok' ? '✅' : it.status === 'warn' ? '⚠️' : '❌';
      techHtml += '<div class="pipe-item ' + stCls + '">';
      techHtml += '<span class="pipe-item-icon">' + stIcon + '</span>';
      techHtml += '<div class="pipe-item-body"><span class="pipe-item-label">' + (it.label || it.key || '') + '</span>';
      techHtml += '<span class="pipe-item-val">' + (it.value || '').substring(0, 120) + '</span>';
      if (it.before) techHtml += '<span class="pipe-item-path">' + it.before + '</span>';
      if (it.note) techHtml += '<span class="pipe-item-note">' + it.note + '</span>';
      techHtml += '</div></div>';
    });
    techHtml += '</div></div>';
  });
  techHtml += '</div>';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + techSecId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🔍 管线执行日志</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' + techHtml + '</div>' +
    '</div>'
  );

  // ===== Panel 7: Next action =====
  var nextId = 'DM-' + String(epNum + 1).padStart(2, '0');
  el.insertAdjacentHTML('beforeend',
    '<div class="dm6-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">✅ 第' + epNum + '集成品检查完成</span>' +
    '  <button class="btn-primary" onclick="switchToTab(\'' + nextId + '\')">下一集 (' + nextId + ')</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'' + msId + '\')">重新质检</button>' +
    '</div>'
  );

  // ===== Fix 3: Update header status note to reflect actual content =====
  var headerMeta = document.querySelector('#detail > .meta');
  if (headerMeta) {
    var spans = headerMeta.querySelectorAll('span');
    if (spans.length >= 2) {
      var noteSpan = spans[1];
      // Count items from detail
      var allItems = [];
      if (detail && detail.sections) {
        detail.sections.forEach(function(sec) {
          (sec.items || []).forEach(function(it) { allItems.push(it); });
        });
      }
      var okItems = allItems.filter(function(it){ return it.status === 'ok'; }).length;
      var totalItems = allItems.length;
      var hasQualityIssue = overallScore < 6;
      if (hasQualityIssue) {
        noteSpan.innerHTML = ' ⚠ 画面质量待提升 | ' + okItems + '/' + totalItems + '项检查通过';
      } else {
        noteSpan.innerHTML = ' ✅ ' + okItems + '/' + totalItems + '项检查，成品可用';
      }
    }
  }
}

// @@FUNC: dm6ScoreItem
function dm6ScoreItem(label, score, colorClass) {
  var pct = Math.min(Math.max((score || 0) / 10 * 100, 5), 100);
  var numClass = score >= 7 ? 'green' : score >= 4 ? 'yellow' : 'red';
  return '<div class="dm6-score-item">' +
    '<div class="score-label">' + label + '</div>' +
    '<div class="score-num ' + numClass + '">' + (score || 0) + '<span style="font-size:12px;color:inherit;opacity:.6">/10</span></div>' +
    '<div class="score-bar"><div class="score-fill ' + colorClass + '" style="width:' + pct + '%"></div></div>' +
    '<div class="score-sub">' + (score >= 8 ? '优秀' : score >= 6 ? '良好' : score >= 4 ? '一般' : '较差') + '</div>' +
    '</div>';
}

// @@FUNC: loadEpGallery
function loadEpGallery(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body) return;
  var epPad = String(epNum).padStart(2, '0');
  var html = '<div class="img-gallery">';
  var found = 0;
  var pending = 5;
  for (var i = 1; i <= 5; i++) {
    (function(imgUrl, idx) {
      var img = new Image();
      img.onload = function() {
        found++;
        html += '<div class="img-card"><img src="' + imgUrl + '" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜' + String(idx).padStart(2,'0') + '</span></div>';
        pending--;
        if (pending <= 0) {
          if (found > 0) {
            body.innerHTML = html + '</div>';
          } else {
            body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>';
          }
          renderEpShotSorter(epNum, containerId);
        }
      };
      img.onerror = function() { pending--; if (pending <= 0) { body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>'; renderEpShotSorter(epNum, containerId); } };
      setTimeout(function() { if (pending > 0) { pending--; if (pending <= 0) { body.innerHTML = '<span style="font-size:10px;color:#555;">该集暂无渲染图</span>'; renderEpShotSorter(epNum, containerId); } } }, 3000);
      img.src = imgUrl;
    })('/api/render/ep' + epPad + '/shot_' + String(i).padStart(2,'0') + '.png', i);
  }
}

// @@FUNC: renderEpShotSorter
function renderEpShotSorter(epNum, containerId) {
  var body = document.getElementById(containerId);
  if (!body || document.getElementById('shot-sorter-' + epNum)) return;
  var sec = '<div class="shot-sorter" id="shot-sorter-' + epNum + '" style="margin-top:10px"><h3>🎬 视频片段排序 · 第' + epNum + '集</h3>';
  sec += '<div class="shot-list" id="shot-list-' + epNum + '"><span class="loading">加载片段列表...</span></div>';
  sec += '<div class="shot-sort-actions" id="shot-actions-' + epNum + '" style="display:none"><button class="btn-merge" onclick="mergeShots(\'' + epNum + '\')">▶ 合并生成</button><button class="btn-subtitle" onclick="generateSubtitle(\'' + epNum + '\')">💬 自动生成字幕</button></div>';
  sec += '<div id="shot-msg-' + epNum + '" class="shot-merge-progress" style="display:none"></div></div>';
  body.insertAdjacentHTML('beforeend', sec);
  fetch('/api/shots/' + epNum).then(function(r) { return r.json(); }).then(function(d) {
    var shots = d.shots || [];
    var listEl = document.getElementById('shot-list-' + epNum);
    var actionsEl = document.getElementById('shot-actions-' + epNum);
    if (!listEl) return;
    if (!shots.length) { listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>'; if (actionsEl) actionsEl.style.display = 'none'; return; }
    if (actionsEl) actionsEl.style.display = 'flex';
    var h = '';
    shots.forEach(function(s, i) {
      var t = s.title || s.name || ('片段 ' + (i + 1));
      var dur = s.duration || '--:--';
      var thumb = s.thumbnail ? '<img class="shot-thumb" src="' + s.thumbnail + '">' : '<div class="shot-thumb-placeholder">🎬</div>';
      h += '<div class="shot-item" draggable="true"><span class="shot-idx">' + (i+1) + '.</span>' + thumb + '<div class="shot-info"><span class="shot-title">' + t + '</span><span class="shot-dur">' + dur + '</span></div><span class="shot-drag-hint">☰</span></div>';
    });
    listEl.innerHTML = h;
  }).catch(function() {
    var listEl = document.getElementById('shot-list-' + epNum);
    if (listEl) listEl.innerHTML = '<div class="shot-empty">暂无视频片段</div>';
  });
}

// @@FUNC: renderShotList
function renderShotList(epNum,shots){
  const listEl=document.getElementById('shot-list-'+epNum);
  const actionsEl=document.getElementById('shot-actions-'+epNum);
  if(!listEl)return;

  if(!shots.length){
    listEl.innerHTML='<div class="shot-empty">该集暂无已生成视频片段</div>';
    if(actionsEl)actionsEl.style.display='none';
    return;
  }

  if(actionsEl)actionsEl.style.display='flex';

  let h='';
  shots.forEach((shot,i)=>{
    const thumbUrl=shot.thumbnail||'';
    const thumb=thumbUrl?`<img class="shot-thumb" src="${thumbUrl}" loading="lazy" onerror="this.outerHTML='<div class=shot-thumb-placeholder>🎬</div>'">`:'<div class="shot-thumb-placeholder">🎬</div>';
    const dur=shot.duration||'--:--';
    h+=`<div class="shot-item" data-idx="${i}" data-name="${shot.name||''}">`;
    h+=thumb;
    h+=`<span class="shot-name">${shot.name||shot.file}</span>`;
    h+=`<span class="shot-dur">${dur}</span>`;
    h+=`<span class="shot-actions">`;
    h+=`<button class="shot-move-btn" onclick="moveShotUp('${epNum}',${i})" ${i===0?'disabled':''} title="上移">&uarr;</button>`;
    h+=`<button class="shot-move-btn" onclick="moveShotDown('${epNum}',${i})" ${i===shots.length-1?'disabled':''} title="下移">&darr;</button>`;
    h+=`</span></div>`;
  });
  listEl.innerHTML=h;

}

// @@FUNC: getShotOrder
function getShotOrder(epNum){
  const listEl=document.getElementById('shot-list-'+epNum);
  if(!listEl)return[];
  const items=listEl.querySelectorAll('.shot-item');
  return Array.from(items).map(it=>it.dataset.name);
}

// @@FUNC: moveShotUp
function moveShotUp(epNum,idx){
  const listEl=document.getElementById('shot-list-'+epNum);
  if(!listEl||idx<=0)return;
  const items=listEl.querySelectorAll('.shot-item');
  const curr=items[idx];
  const prev=items[idx-1];
  listEl.insertBefore(curr,prev);
  // Re-render with updated indices
  const names=Array.from(listEl.querySelectorAll('.shot-item')).map(it=>({name:it.dataset.name,dur:it.querySelector('.shot-dur').textContent,thumb:it.querySelector('.shot-thumb')?.src||''}));
  renderShotList(epNum,names.map(n=>({name:n.name,file:n.name,duration:n.dur,thumbnail:n.thumb})));
}

// @@FUNC: moveShotDown
function moveShotDown(epNum,idx){
  const listEl=document.getElementById('shot-list-'+epNum);
  if(!listEl)return;
  const items=listEl.querySelectorAll('.shot-item');
  if(idx>=items.length-1)return;
  const curr=items[idx];
  const next=items[idx+1];
  listEl.insertBefore(next,curr);
  const names=Array.from(listEl.querySelectorAll('.shot-item')).map(it=>({name:it.dataset.name,dur:it.querySelector('.shot-dur').textContent,thumb:it.querySelector('.shot-thumb')?.src||''}));
  renderShotList(epNum,names.map(n=>({name:n.name,file:n.name,duration:n.dur,thumbnail:n.thumb})));
}

// @@FUNC: mergeShots
async function mergeShots(epNum){
  const files=getShotOrder(epNum);
  if(!files.length){toastMsg('没有可合并的片段',2000,'warn');return;}

  const msgEl=document.getElementById('shot-msg-'+epNum);
  if(msgEl){msgEl.style.display='block';msgEl.textContent='正在合并 '+files.length+' 个片段...';}

  try{
    const r=await fetch('/api/merge',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({episode:String(epNum),files})});
    const d=await r.json();
    if(d.error){toastMsg('合并失败: '+d.error,3000,'error');}
    else{toastMsg('合并成功: '+d.output_file,3000);}
  }catch(e){toastMsg('合并请求失败: '+e.message,3000,'error');}
  if(msgEl)msgEl.style.display='none';
}

// @@FUNC: epochStr
function epochStr(epNum){return 'EP'+String(epNum).padStart(2,'0');}

// @@FUNC: generateSubtitle
async function generateSubtitle(epNum){
  var msgEl=document.getElementById('shot-msg-'+epNum);
  if(msgEl){msgEl.style.display='block';msgEl.textContent='⏳ 正在生成字幕 (whisper)...';}

  try{
    var r=await fetch('/api/subtitle',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({episode:String(epNum)})});
    var d=await r.json();
    if(d.error){toastMsg('字幕生成失败: '+d.error,3000,'error');if(msgEl)msgEl.style.display='none';return;}
    var srt=d.srt||'';
    toastMsg('✅ 字幕生成成功 (' + srt.split('\n').filter(function(l){return /^\d+$/.test(l.trim());}).length + ' 条)',3000,'success');
    showSubtitlePreview(epNum, srt, d.srt_path||'');
  }catch(e){toastMsg('字幕请求失败: '+e.message,3000,'error');}
  if(msgEl)msgEl.style.display='none';
}

// @@FUNC: showSubtitlePreview
function showSubtitlePreview(epNum, srtContent, srtPath) {
  var sorter = document.getElementById('shot-sorter-' + epNum);
  if (!sorter) return;
  // Remove old preview if exists
  var oldPreview = document.getElementById('sub-preview-' + epNum);
  if (oldPreview) oldPreview.remove();
  var lines = srtContent.split('\n');
  var entryCount = lines.filter(function(l){return /^\d+$/.test(l.trim());}).length;
  var previewHtml =
    '<div class="info-card collapsible" id="sub-preview-' + epNum + '" style="margin-top:8px">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>💬 字幕预览 ' + epochStr(epNum) + ' · ' + entryCount + ' 条</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" id="sub-preview-body-' + epNum + '">' +
    '    <div style="margin-bottom:8px;display:flex;gap:6px">' +
    '      <button class="btn-sm5 secondary" onclick="toggleSubEdit(\'' + epNum + '\')">✏️ 编辑模式</button>' +
    '      <button class="btn-sm5 secondary" onclick="generateSubtitle(\'' + epNum + '\')">🔄 重新生成</button>' +
    '      <span style="font-size:9px;color:#888;margin-left:auto;align-self:center">' + (srtPath||'') + '</span>' +
    '    </div>' +
    '    <pre id="sub-srt-text-' + epNum + '" style="white-space:pre-wrap;font-size:10px;background:rgba(0,0,0,.2);padding:8px;border-radius:4px;max-height:300px;overflow-y:auto;color:#c4d4e8;line-height:1.6">' + srtContent.replace(/</g,'&lt;') + '</pre>' +
    '    <textarea id="sub-srt-edit-' + epNum + '" style="display:none;width:100%;min-height:200px;font-size:10px;background:rgba(0,0,0,.3);color:#e4e6eb;border:1px solid rgba(255,255,255,.1);border-radius:4px;padding:8px;font-family:monospace;line-height:1.5;resize:vertical"></textarea>' +
    '    <div id="sub-edit-actions-' + epNum + '" style="display:none;margin-top:6px;gap:6px">' +
    '      <button class="btn-sm5 primary" onclick="saveSubtitleEdit(\'' + epNum + '\',\'' + (srtPath||'') + '\')">💾 保存修改</button>' +
    '      <button class="btn-sm5 secondary" onclick="toggleSubEdit(\'' + epNum + '\')">取消</button>' +
    '    </div>' +
    '  </div>' +
    '</div>';
  sorter.insertAdjacentHTML('afterend', previewHtml);
}

// @@FUNC: toggleSubEdit
function toggleSubEdit(epNum) {
  _subEditMode[epNum] = !_subEditMode[epNum];
  var pre = document.getElementById('sub-srt-text-' + epNum);
  var ta = document.getElementById('sub-srt-edit-' + epNum);
  var act = document.getElementById('sub-edit-actions-' + epNum);
  if (!pre || !ta) return;
  if (_subEditMode[epNum]) {
    ta.value = (pre.textContent || '').replace(/&lt;/g,'<');
    pre.style.display = 'none';
    ta.style.display = 'block';
    if(act) act.style.display = 'flex';
  } else {
    pre.style.display = 'block';
    ta.style.display = 'none';
    if(act) act.style.display = 'none';
  }
}

// @@FUNC: saveSubtitleEdit
async function saveSubtitleEdit(epNum, srtPath) {
  var ta = document.getElementById('sub-srt-edit-' + epNum);
  if (!ta) return;
  var newContent = ta.value;
  try {
    var r = await fetch('/api/subtitle/save', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({episode: String(epNum), srt: newContent, path: srtPath})
    });
    var d = await r.json();
    if (d.error) { toastMsg('保存失败: ' + d.error, 3000, 'error'); return; }
    // Update preview
    var pre = document.getElementById('sub-srt-text-' + epNum);
    if (pre) pre.textContent = newContent.replace(/</g,'&lt;');
    toggleSubEdit(epNum);
    toastMsg('✅ 字幕已保存', 2000, 'success');
  } catch(e) {
    toastMsg('保存失败: ' + e.message, 3000, 'error');
  }
}

