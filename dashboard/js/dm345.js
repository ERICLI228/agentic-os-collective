// === dm345.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: renderDM3
async function renderDM3(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items from sections
  var voiceItems = [];
  var techItems = [];
  var engineInfo = {};
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) {
        var key = it.key || '';
        // Voice/NLS items
        if (key === 'nv_engine') { engineInfo = it; return; }
        if (key === 'nv_ws' || key === 'nv_lzs' || key === 'nv_lc' ||
            key === 'nv_sj' || key === 'nv_lk' || key === 'nv_wy') {
          voiceItems.push(it);
          return;
        }
        techItems.push(it);
      });
    });
  }

  // Character voice configs
  var charMap = {
    nv_ws:  { name:'武松',   voice:'zhiming', desc:'浑厚有力·男声',   trait:'勇猛/嗜酒/重义',      charId:'wusong',   ep:'01' },
    nv_lzs: { name:'鲁智深', voice:'zhiming', desc:'粗犷豪迈·男声',   trait:'狂野/正义/佛门暴力', charId:'luzhishen', ep:'02' },
    nv_lc:  { name:'林冲',   voice:'zhilun',  desc:'沉郁悲壮·男声',   trait:'压抑/爆发/悲剧',     charId:'linchong', ep:'03' },
    nv_sj:  { name:'宋江',   voice:'zhilun',  desc:'沉稳内敛·男声',   trait:'算计/隐忍/爆发',     charId:'songjiang',ep:'04' },
    nv_lk:  { name:'李逵',   voice:'zhiming', desc:'暴烈粗犷·男声',   trait:'孝心/暴躁/忠诚',     charId:'likui',    ep:'05' },
    nv_wy:  { name:'吴用',   voice:'zhilun',  desc:'沉稳睿智·男声',   trait:'智谋/从容/领袖',     charId:'wuyong',   ep:'06' }
  };

  // Compute summary
  var doneCount = 0, pendingCount = 0, ngCount = 0;
  var charRows = [];
  voiceItems.forEach(function(it) {
    var key = it.key || '';
    var cfg = charMap[key];
    if (!cfg) return;
    var status = it.status || 'unknown';
    var isDone = status === 'ok';
    var isNg = status === 'ng';
    if (isDone) doneCount++;
    else if (isNg) ngCount++;
    else pendingCount++;
    var statusText = '';
    var statusClass = '';
    if (isDone) {
      var val = it.value || '';
      statusText = '✅ ' + (val.match(/EP\d+/)?.[0] || '已生成');
      statusClass = 'tag-green';
    } else if (isNg) {
      statusText = '❌ 待生成';
      statusClass = 'tag-red';
    } else {
      statusText = '⏳ 处理中';
      statusClass = 'tag-yellow';
    }
    // Check if this voice is shared with another character
    var isConflict = false;
    voiceItems.forEach(function(other) {
      if (other.key === key) return;
      var otherCfg = charMap[other.key];
      if (otherCfg && otherCfg.voice === cfg.voice) isConflict = true;
    });
    charRows.push({
      key: key,
      name: cfg.name,
      voice: cfg.voice,
      desc: cfg.desc,
      trait: cfg.trait,
      charId: cfg.charId,
      ep: cfg.ep,
      status: status,
      statusText: statusText,
      statusClass: statusClass,
      isConflict: isConflict,
      note: it.note || '',
      before: it.before || '',
      after: it.after || '',
      value: it.value || ''
    });
  });

  // Count zhiming conflicts
  var zhimingCount = charRows.filter(function(r) { return r.voice === 'zhiming' && r.status !== 'ok'; }).length;
  var zhilunCount = charRows.filter(function(r) { return r.voice === 'zhilun' && r.status !== 'ok'; }).length;
  var allDone = doneCount === voiceItems.length;

  // Panel 1: Summary
  var sumClass = 'dub-summary-card';
  var sumIcon = '';
  if (allDone) { sumClass += ' green'; sumIcon = '✅'; }
  else if (ngCount > 0) { sumClass += ' orange'; sumIcon = '⚠️'; }
  else { sumClass += ' green'; sumIcon = '✅'; }

  var engineVal = engineInfo.value || '阿里云NLS TTS';
  var costText = '';
  techItems.forEach(function(t) {
    if (t.key === 'nv_cost') costText = t.value || '';
  });
  var summaryTitle = doneCount + '/' + voiceItems.length + '角色已生成配音，' + (voiceItems.length - doneCount) + '个待处理';
  var summaryMeta = '引擎: ' + engineVal;
  var adviceParts = [];
  if (zhimingCount > 0) adviceParts.push('武松/鲁智深共用zhiming音色需字幕区分');
  if (zhilunCount > 0) adviceParts.push('林冲/宋江/吴用共用zhilun音色需字幕区分');
  var adviceText = adviceParts.length ? '⚠️ 注意：' + adviceParts.join('；') : '✅ 所有角色配音就绪';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dub-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dub-summary-content">' +
    '    <div class="dub-summary-title">' + summaryTitle + '</div>' +
    '    <div class="dub-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="dub-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 2: Voice table
  var tableHtml = '<div class="dub-voice-table"><table><thead><tr>' +
    '<th>角色</th><th>音色</th><th>音色描述</th><th>匹配性格</th><th>状态</th><th>操作</th>' +
    '</tr></thead><tbody>';
  charRows.forEach(function(r) {
    var trClass = r.isConflict && r.status !== 'ok' ? ' class="conflict"' : '';
    var voiceTagClass = 'voice-tag ' + r.voice;
    tableHtml += '<tr' + trClass + ' id="dm3-voice-'+r.charId+'">';
    tableHtml += '  <td><strong>' + r.name + '</strong></td>';
    tableHtml += '  <td><span class="' + voiceTagClass + '">' + r.voice + '</span></td>';
    tableHtml += '  <td>' + r.desc + '</td>';
    tableHtml += '  <td>' + r.trait + '</td>';
    tableHtml += '  <td><span class="tag ' + r.statusClass + '">' + r.statusText + '</span></td>';
    tableHtml += '  <td>';
    // Play button for completed
    if (r.status === 'ok') {
      tableHtml += '<button class="btn-sm" onclick="playDubVoice(\'' + r.charId + '\')">▶ 试听</button>';
    } else {
      tableHtml += '<button class="btn-sm btn-primary" onclick="generateDubVoice(\'' + r.charId + '\', this)">生成配音</button>';
    }
    if (r.isConflict && r.status !== 'ok') {
      tableHtml += '<span class="voice-conflict-warn">⚠️ 音色冲突</span>';
    }
    tableHtml += '  </td>';
    tableHtml += '</tr>';
  });
  tableHtml += '</tbody></table></div>';
  el.insertAdjacentHTML('beforeend', tableHtml);

  // Panel 3: Tech cards with SFX visualization
  var techCardHtml = '<div class="dub-tech-cards">';
  var sfxCardHtml = '';
  techItems.forEach(function(t) {
    var key = t.key || '';
    var label = t.label || '';
    var val = t.value || '';
    var note = t.note || '';
    if (key === 'aq_bgm') {
      // SFX will be rendered as timeline below
      sfxCardHtml = '<div class="dub-tech-card sfx-card" id="dm3-sfx-card"><span>🔊 ' + label + '</span><strong>✅ SFX 已集成</strong><div id="dm3-sfx-timeline" style="margin-top:8px"><span class="loading">加载音效数据...</span></div></div>';
      return;
    }
    var icon = '';
    if (key === 'nv_cost') icon = '💰';
    else if (key === 'aq_sync') icon = '👄';
    else icon = '⚙️';
    var statusIcon = '';
    if (t.status === 'ok') statusIcon = '✅ ';
    else if (t.status === 'warn') statusIcon = '⚠️ ';
    else if (t.status === 'ng') statusIcon = '❌ ';
    techCardHtml += '<div class="dub-tech-card"><span>' + icon + ' ' + label + '</span><strong>' + statusIcon + val.split('·')[0] + '</strong><span>' + (note || '·') + '</span></div>';
  });
  techCardHtml += '</div>';
  if(sfxCardHtml) techCardHtml += sfxCardHtml;
  // Localization runner
  techCardHtml += '<div class="dub-tech-card" style="cursor:pointer;border-color:rgba(59,130,246,.2)" onclick="runLocalizationReview()"><span>🌏 本地化审查</span><strong>⚡ 点击运行5国本地化</strong><span id="loc-review-status" style="font-size:9px;color:#888">localization_reviewer.py 就绪</span></div>';
  techCardHtml += '<div id="loc-review-results" style="display:none"></div>';
  el.insertAdjacentHTML('beforeend', techCardHtml);
  // Load SFX timeline
  (function loadSFXTimeline(){
    var tl = document.getElementById('dm3-sfx-timeline');
    if(!tl) return;
    fetch('/api/sfx/1').then(function(r){return r.json()}).then(function(d){
      var tracks = d.tracks || [];
      if(!tracks.length){ tl.innerHTML='<span style="font-size:10px;color:#555">暂无音效数据</span>'; return; }
      var totalDur = Math.max.apply(null, tracks.map(function(t){ return (t.start_sec||0)+(t.duration_sec||0); })) || 23;
      var barW = Math.min(100, Math.max(60, tl.parentElement.offsetWidth - 120));
      var scale = barW / totalDur;
      var h = '<div style="position:relative;height:80px;margin:4px 0;font-size:9px">';
      // Time markers
      for(var ti=0; ti<=totalDur; ti+=5){
        h += '<span style="position:absolute;left:'+(60+ti*scale)+'px;top:0;color:#555;font-size:8px">' + ti + 's</span>';
      }
      tracks.forEach(function(t,idx){
        var left = 60 + (t.start_sec||0)*scale;
        var w = Math.max(20, (t.duration_sec||3)*scale);
        var top = 20 + idx*20;
        var colors = ['#4ade80','#60a5fa','#fbbf24','#f87171','#a78bfa','#fb923c'];
        var c = colors[idx % colors.length];
        h += '<div style="position:absolute;left:'+left+'px;top:'+top+'px;width:'+w+'px;height:16px;background:'+c+';opacity:.25;border-radius:3px;border:1px solid '+c+'" title="'+(t.scene||t.type||'')+' 音量:'+(t.volume||0)+'">';
        h += '<span style="position:absolute;left:4px;top:1px;color:'+c+';font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:'+(w-8)+'px">🎵 ' + (t.scene||'SFX') + '</span>';
        h += '</div>';
      });
      h += '</div>';
      // Track list
      h += '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">';
      tracks.forEach(function(t,idx){
        var colors = ['#4ade80','#60a5fa','#fbbf24','#f87171','#a78bfa','#fb923c'];
        h += '<span style="font-size:9px;padding:2px 8px;border-radius:3px;background:rgba(255,255,255,.03);border:1px solid '+colors[idx%colors.length]+';color:'+colors[idx%colors.length]+'">' + (t.scene||t.type||'SFX'+idx) + ' @' + (t.start_sec||0)+'s ×'+(t.volume||'?')+'</span>';
      });
      h += '</div>';
      tl.innerHTML = h;
    }).catch(function(){ tl.innerHTML='<span style="font-size:10px;color:#555">音效数据加载失败</span>'; });
  })();

  // Panel 4: Production monitoring dashboard
  var techSecId = 'dm3-tech-log';
  var tDone = Math.round(doneCount / voiceItems.length * 100) || 0;
  var usagePct = Math.round((29817 - 29817 * (voiceItems.length - doneCount) / voiceItems.length * 0.017) / 30000 * 100) || 99;
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + techSecId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>📊 制作监控仪表盘</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' +
    '    <div class="dm3-mon-grid">' +
    '      <div class="dm3-mon-card">' +
    '        <div class="dm3-mon-label">配音进度</div>' +
    '        <div class="dm3-mon-bar"><div class="dm3-mon-fill" style="width:' + tDone + '%"></div></div>' +
    '        <div class="dm3-mon-val">' + doneCount + '/' + voiceItems.length + ' 角色 (' + tDone + '%)</div>' +
    '      </div>' +
    '      <div class="dm3-mon-card">' +
    '        <div class="dm3-mon-label">NLS 资源包余量</div>' +
    '        <div class="dm3-mon-bar"><div class="dm3-mon-fill green" style="width:' + usagePct + '%"></div></div>' +
    '        <div class="dm3-mon-val">~29817/30000 字符 (99%)</div>' +
    '      </div>' +
    '      <div class="dm3-mon-card">' +
    '        <div class="dm3-mon-label">配音成本</div>' +
    '        <div class="dm3-mon-val large">¥0.75/集</div>' +
    '        <div class="dm3-mon-sub">6集合计≈¥4.50 · 极低成本</div>' +
    '      </div>' +
    '      <div class="dm3-mon-card">' +
    '        <div class="dm3-mon-label">音色冲突</div>' +
    '        <div class="dm3-mon-val large' + (zhimingCount>1||zhilunCount>1 ? ' warn' : '') + '">' + (zhimingCount>1||zhilunCount>1 ? '⚠️ 需字幕' : '✅ 无冲突') + '</div>' +
    '        <div class="dm3-mon-sub">zhiming×' + zhimingCount + ' zhilun×' + zhilunCount + '</div>' +
    '      </div>' +
    '    </div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 5: Next action
  el.insertAdjacentHTML('beforeend',
    '<div class="dub-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">✅ 配音生成检查完成，建议执行：</span>' +
    '  <button class="btn-primary" onclick="generateAllDubVoices()">⚡ 一键生成全部</button>' +
    '  <button class="btn-primary" onclick="switchToTab(\'DM-F\')">进入 DM-F 视频合成管线</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-3\')">重新检查配音状态</button>' +
    '</div>'
  );
}

// @@FUNC: playDubVoice
function playDubVoice(charId) {
  auditionVoice(charId);
}

// @@FUNC: generateDubVoice
function generateDubVoice(charId, btn) {
  if (btn) {
    btn.disabled = true;
    btn.textContent = '生成中...';
  }
  var banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 生成 ' + charId + ' 配音...';
  // Try GPT-SoVITS API directly
  var cfg = { wusong:{ref:'output/wusong/ref.wav',prompt:'我是武松，景阳冈打虎的好汉。'}, luzhishen:{ref:'output/luzhishen/ref.wav',prompt:'洒家鲁智深，拳打镇关西的好汉。'}, linchong:{ref:'output/linchong/ref.wav',prompt:'小人林冲，八十万禁军教头。'}, songjiang:{ref:'output/songjiang/ref.wav',prompt:'小可宋江，郓城县押司。'}, likui:{ref:'output/likui/ref.wav',prompt:'俺是黑旋风李逵。'}, wuyong:{ref:'output/wuyong/ref.wav',prompt:'小生吴用，人称智多星。'} };
  var ch = cfg[charId];
  if (!ch) { if(btn){btn.disabled=false;btn.textContent='生成配音';} toastMsg('⚠️ 未知角色: '+charId, 3000, 'warn'); return; }
  fetch('http://localhost:9880/?refer_wav_path='+encodeURIComponent(ch.ref)+'&prompt_text='+encodeURIComponent(ch.prompt)+'&prompt_language=zh&text='+encodeURIComponent(ch.prompt)+'&text_language=zh&top_k=6&top_p=0.9&temperature=0.7&speed=1.0')
    .then(function(r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.blob();
    })
    .then(function(blob) {
      var audioUrl = URL.createObjectURL(blob);
      var audio = new Audio(audioUrl);
      audio.play();
      if (banner) banner.textContent = '✅ ' + charId + ' 配音已生成并播放';
      if (btn) { btn.textContent = '✅ 已生成'; btn.className = 'btn-sm'; btn.disabled = true; }
      toastMsg('🎤 ' + charId + ' 配音生成成功', 3000, 'success');
    })
    .catch(function(e) {
      if (banner) banner.textContent = '❌ 生成失败: ' + e.message;
      if (btn) { btn.disabled = false; btn.textContent = '生成配音'; }
      toastMsg('❌ 生成失败: ' + e.message + ' (请确认 GPT-SoVITS 运行在 9880)', 5000, 'warn');
    });
}

// @@FUNC: generateAllDubVoices
function generateAllDubVoices() {
  var banner = document.getElementById('version-check');
  var pending = ['wusong','luzhishen','linchong','songjiang','likui','wuyong'];
  if (banner) banner.textContent = '⏳ 批量生成 ' + pending.length + ' 个角色配音...';
  toastMsg('⏳ 开始批量生成 ' + pending.length + ' 个角色配音', 3000, 'info');
  // Sequential generation to avoid overloading GPT-SoVITS
  var i = 0;
  function genNext() {
    if (i >= pending.length) {
      if (banner) banner.textContent = '✅ 全部 ' + pending.length + ' 个角色配音生成完成';
      toastMsg('✅ 全部配音生成完成', 3000, 'success');
      return;
    }
    var charId = pending[i];
    generateDubVoice(charId, null);
    i++;
    setTimeout(genNext, 2000); // 2s interval between generations
  }
  genNext();
}

// @@FUNC: renderDM4
async function renderDM4(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  var items = [];
  if (detail && detail.sections) {
    (detail.sections[0]?.items || []).forEach(function(it) { items.push(it); });
  }
  if (!items.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>字幕帧方案</h3><div style="color:#555;font-size:11px;padding:12px">暂无数据</div></div>');
    return;
  }

  function findItem(key) { return items.find(function(it) { return it.key === key; }); }
  var whatItem = findItem('pf_what');
  var whyItem = findItem('pf_why');
  var issueItem = findItem('pf_issue');
  var altItem = findItem('pf_alt');
  var specItem = findItem('pf_spec');

  var hasIssue = items.some(function(it) { return it.status === 'ng'; });

  // ===== Panel 1: Upgrade conclusion summary =====
  var specVal = specItem ? (specItem.value || '').split('·').map(function(s){return s.trim()})[0] || '' : '';
  el.insertAdjacentHTML('beforeend',
    '<div class="upgrade-summary-card">' +
    '  <div class="upgrade-summary-icon">⚠️</div>' +
    '  <div class="upgrade-summary-content">' +
    '    <div class="upgrade-summary-title">当前 Pillow 字幕帧质量偏低，建议升级到 ComfyUI</div>' +
    '    <div class="upgrade-summary-meta">' + (specVal || '231KB') + ' · 静态文字画面 · TikTok 算法可能降权 · ComfyUI 免费可用</div>' +
    '    <div class="upgrade-summary-advice">推荐立即升级到 ComfyUI 静态角色画面（免费 · 本地 GPU · 完播率预计 +50%）</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 2: Three-scheme comparison cards =====
  var compHtml = '<div class="upgrade-compare-grid">';

  // Pillow (current)
  var curVal = whatItem ? (whatItem.value || 'Pillow生成PNG字幕帧 → ffmpeg合并 → .mp4') : '';
  compHtml += '<div class="upgrade-card current">';
  compHtml += '  <span class="upgrade-card-badge">当前使用</span>';
  compHtml += '  <div class="upgrade-card-header">Pillow 字幕帧</div>';
  compHtml += '  <div class="upgrade-card-specs"><span>231KB/23s</span><span>纯文字画面</span><span>💰 免费</span></div>';
  compHtml += '  <div class="upgrade-card-quality"><div class="quality-bar red" style="width:20%">画质 2/10</div></div>';
  compHtml += '  <div class="upgrade-card-risk">⚠️ TikTok 判定 low-quality → 降权</div>';
  compHtml += '  <div class="upgrade-card-status">✅ 已跑通 · 当前使用中</div>';
  compHtml += '</div>';

  // ComfyUI (recommended)
  compHtml += '<div class="upgrade-card recommended">';
  compHtml += '  <span class="upgrade-card-badge highlight">⭐ 推荐升级</span>';
  compHtml += '  <div class="upgrade-card-header">ComfyUI 静态角色画面</div>';
  compHtml += '  <div class="upgrade-card-specs"><span>约 2MB/集</span><span>有角色形象</span><span>💰 免费</span></div>';
  compHtml += '  <div class="upgrade-card-quality"><div class="quality-bar yellow" style="width:50%">画质 5/10</div></div>';
  compHtml += '  <div class="upgrade-card-benefit">✅ 完播率预计 +50% · 本地 GPU · 约 10 分钟/集</div>';
  compHtml += '  <button class="btn-primary btn-sm" onclick="switchToComfyUI()">⚡ 一键升级</button>';
  compHtml += '</div>';

  // fal.ai / Kling (future)
  compHtml += '<div class="upgrade-card future">';
  compHtml += '  <span class="upgrade-card-badge">未来目标</span>';
  compHtml += '  <div class="upgrade-card-header">fal.ai / Kling AI 视频</div>';
  compHtml += '  <div class="upgrade-card-specs"><span>2-10MB/集</span><span>真 AI 视频</span><span>💰 ¥2.5-15/集</span></div>';
  compHtml += '  <div class="upgrade-card-quality"><div class="quality-bar green" style="width:85%">画质 8.5/10</div></div>';
  compHtml += '  <div class="upgrade-card-block">🔒 fal.ai 未付费 · Kling 微信支付可用</div>';
  compHtml += '  <button class="btn-secondary btn-sm" onclick="switchToTab(\'DM-5\')">前往 DM-5 解决付费</button>';
  compHtml += '</div>';

  compHtml += '</div>';
  el.insertAdjacentHTML('beforeend', compHtml);

  // ===== Panel 3: Quality defect warning card =====
  var issueVal = issueItem ? (issueItem.value || '231KB/23s · 静态文字画面 · TikTok算法判定low-quality → 降权') : '';
  el.insertAdjacentHTML('beforeend',
    '<div class="publish-check-card fail">' +
    '  <div class="check-card-icon">❌</div>' +
    '  <div style="flex:1;min-width:0">' +
    '    <div class="check-card-title">质量缺陷警告</div>' +
    '    <div class="check-card-detail">' + issueVal + '</div>' +
    '    <div class="check-card-advice">建议至少升级到 ComfyUI 静态画面（免费 · 开源）· 比纯字幕提升 50%+ 完播率</div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 4: Technical specs card =====
  el.insertAdjacentHTML('beforeend',
    '<div class="dm4-tech-grid">' +
    '  <div class="dm4-tech-card"><div class="tc-icon">📦</div><div class="tc-label">格式</div><div class="tc-value">MP4 H.264</div></div>' +
    '  <div class="dm4-tech-card"><div class="tc-icon">📱</div><div class="tc-label">分辨率</div><div class="tc-value">1080×1920</div><div class="tc-sub">9:16 竖屏</div></div>' +
    '  <div class="dm4-tech-card"><div class="tc-icon">⏱️</div><div class="tc-label">时长</div><div class="tc-value">23s</div></div>' +
    '  <div class="dm4-tech-card"><div class="tc-icon">🎞️</div><div class="tc-label">帧率</div><div class="tc-value">24fps</div></div>' +
    '  <div class="dm4-tech-card"><div class="tc-icon">🎵</div><div class="tc-label">BGM</div><div class="tc-value">无</div></div>' +
    '</div>'
  );

  // ===== Panel 5: Collapsible tools & monitoring =====
  var toolsId = 'dm4-tools-panel';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + toolsId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🛠️ 工具与管线监控</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' +
    '    <div class="dm4-tools-grid">' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🎬</div><div class="tool-name">视频播放器</div><div class="tool-status ok">✅ 可用</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🔀</div><div class="tool-name">片段排序器</div><div class="tool-status ok">✅ 可用</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🖥️</div><div class="tool-name">ComfyUI 管线</div><div class="tool-status ' + (hasIssue ? 'warn' : 'ok') + '">' + (hasIssue ? '⚠️ 待切换' : '✅ 就绪') + '</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🐍</div><div class="tool-name">Python Pillow</div><div class="tool-status ok">✅ 已跑通</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🤖</div><div class="tool-name">fal.ai 视频</div><div class="tool-status ng">❌ 未付费</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🎥</div><div class="tool-name">ffmpeg 合成</div><div class="tool-status ok">✅ 可用</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">📊</div><div class="tool-name">质量反馈知识库</div><div class="tool-status ok">✅ 活跃</div></div>' +
    '      <div class="dm4-tool-card"><div class="tool-icon">🔄</div><div class="tool-name">TikTok 合规检查</div><div class="tool-status warn">⚠️ 文字-低质</div></div>' +
    '    </div>' +
    '  </div>' +
    '</div>'
  );

  // ===== Panel 6: Next action =====
  el.insertAdjacentHTML('beforeend',
    '<div class="gate-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">✅ DM-4 升级路径分析完成 — 推荐升级到 ComfyUI</span>' +
    '  <button class="btn-primary btn-lg" onclick="switchToComfyUI()">⭐ 一键升级到 ComfyUI（推荐）</button>' +
    '  <button class="btn-secondary" onclick="switchToTab(\'DM-5\')">前往 fal.ai 付费方案</button>' +
    '</div>'
  );
}

// @@FUNC: renderDM5
async function renderDM5(detail, ms) {
  var el = document.getElementById('detail');
  if (!el) return;

  // Extract items from both sections
  var allItems = [];
  if (detail && detail.sections) {
    detail.sections.forEach(function(sec) {
      (sec.items || []).forEach(function(it) { allItems.push(it); });
    });
  }
  if (!allItems.length) {
    el.insertAdjacentHTML('beforeend', '<div class="sec"><h3>AI视频生成</h3><div style="color:#555;font-size:11px;padding:12px">暂无数据</div></div>');
    return;
  }

  function fi(key) { return allItems.find(function(it) { return it.key === key; }); }
  var blWhat = fi('bl_what');
  var blReg = fi('bl_reg');
  var blAlt = fi('bl_alt');
  var blPrompt = fi('bl_prompt');
  var blPipeline = fi('bl_pipeline');
  var exQuality = fi('ex_quality');
  var exTime = fi('ex_time');
  var exRisk = fi('ex_risk');

  // Summary
  var blocked = blWhat && blWhat.status === 'ng';
  var apiReady = blPipeline && blPipeline.status === 'ok';

  // Panel 0: Quality evolution pipeline & cost comparison
  el.insertAdjacentHTML('beforeend',
    '<div style="font-size:10px;color:#888;font-weight:600;margin:0 0 4px">📈 画质进化路线</div>' +
    '<div class="dm5-pipeline-bar">' +
    '  <div class="dm5-pipeline-stage current"><div class="pl-icon">📄</div><div class="pl-name">Pillow</div><div class="pl-score">2/10 · 免费</div></div>' +
    '  <span class="dm5-pipeline-arrow">→</span>' +
    '  <div class="dm5-pipeline-stage recommended"><div class="pl-icon">🖥️</div><div class="pl-name">ComfyUI</div><div class="pl-score">5/10 · 免费</div></div>' +
    '  <span class="dm5-pipeline-arrow">→</span>' +
    '  <div class="dm5-pipeline-stage"><div class="pl-icon">🎬</div><div class="pl-name">Kling</div><div class="pl-score">8.5/10 · ¥15</div></div>' +
    '  <span class="dm5-pipeline-arrow">→</span>' +
    '  <div class="dm5-pipeline-stage"><div class="pl-icon">🌐</div><div class="pl-name">Seedance</div><div class="pl-score">8.5/10 · $7.5</div></div>' +
    '</div>'
  );
  el.insertAdjacentHTML('beforeend',
    '<div style="font-size:10px;color:#888;font-weight:600;margin:12px 0 4px">💰 6集成品成本预估</div>' +
    '<div class="dm5-cost-grid">' +
    '  <div class="dm5-cost-card"><div class="cc-icon">📄</div><div class="cc-name">Pillow</div><div class="cc-price">¥0</div><div class="cc-meta">即时生成</div></div>' +
    '  <div class="dm5-cost-card recommended"><div class="cc-icon">🖥️</div><div class="cc-name">ComfyUI</div><div class="cc-price">¥0</div><div class="cc-meta">~10分钟/集</div></div>' +
    '  <div class="dm5-cost-card recommended"><div class="cc-icon">🎬</div><div class="cc-name">⭐ Kling</div><div class="cc-price">¥15</div><div class="cc-meta">1-3分钟/镜</div></div>' +
    '  <div class="dm5-cost-card"><div class="cc-icon">🌐</div><div class="cc-name">Seedance</div><div class="cc-price">$7.50</div><div class="cc-meta">2-5分钟/镜</div></div>' +
    '</div>'
  );

  // Summary
  var sumClass = 'dm5-summary-card' + (blocked ? ' red' : ' green');
  var sumIcon = blocked ? '❌' : '✅';
  var altVal = blAlt ? (blAlt.value || '').substring(0, 60) : 'Kling(可灵) ¥15/6集';
  var promptVal = blPrompt ? '18个prompt就绪' : '';
  var summaryTitle = blocked ? 'AI视频生成阻塞: fal.ai 未付费' : 'AI视频生成就绪';
  var summaryMeta = promptVal + ' | 推荐替代: ' + altVal;
  var adviceText = blocked
    ? '⚠️ 建议：优先试用 Kling（中文界面+微信/支付宝支付），或继续使用 ComfyUI 本地生成'
    : '✅ API Key 已就绪，可随时启动 AI 视频生成';

  el.insertAdjacentHTML('beforeend',
    '<div class="' + sumClass + '">' +
    '  <div class="dm5-summary-icon">' + sumIcon + '</div>' +
    '  <div class="dm5-summary-content">' +
    '    <div class="dm5-summary-title">' + summaryTitle + '</div>' +
    '    <div class="dm5-summary-meta">' + summaryMeta + '</div>' +
    '    <div class="dm5-summary-advice">' + adviceText + '</div>' +
    '  </div>' +
    '</div>'
  );

  // Panel 2: Block & Solution cards grid (优化一：增强支付阻塞卡片)
  var blockHtml = '<div class="dm5-block-grid">';

  // Payment block card with prominent Kling solution
  blockHtml += '<div class="dm5-block-card fail">';
  blockHtml += '  <div class="dm5-block-header fail-hdr">🔒 支付阻塞</div>';
  blockHtml += '  <div class="dm5-block-body">';
  if (blWhat) blockHtml += (blWhat.value || 'fal.ai 需外币卡').replace(/·/g, '<br>') + '<br>';
  blockHtml += '  </div>';
  // 解决方案入口
  blockHtml += '  <div class="dm5-solution-entrance">';
  blockHtml += '    <div class="dm5-solution-text">💰 推荐替代方案：Kling (可灵) — 支持微信支付</div>';
  blockHtml += '    <div class="dm5-solution-btns">';
  blockHtml += '      <button class="btn-sm5 primary kling-btn" onclick="goToKling(this)">前往 Kling (¥15/6集) →</button>';
  blockHtml += '      <button class="btn-sm5 secondary" onclick="switchToRenderer(\'comfyui\')">ComfyUI 本地免费方案</button>';
  blockHtml += '    </div>';
  blockHtml += '  </div>';
  if (blReg) blockHtml += '  <div class="dm5-block-note">' + (blReg.value || '').substring(0, 80) + '...</div>';
  blockHtml += '</div>';

  // Risk card
  blockHtml += '<div class="dm5-block-card warn">';
  blockHtml += '  <div class="dm5-block-header warn-hdr">⚠️ 一致性风险</div>';
  blockHtml += '  <div class="dm5-block-body">';
  if (exRisk) blockHtml += (exRisk.value || '多镜角色长相不一致').replace(/·/g, '<br>');
  blockHtml += '  </div>';
  if (exRisk && exRisk.note) {
    blockHtml += '  <div class="dm5-block-note">💡 ' + exRisk.note + '</div>';
  }
  blockHtml += '</div>';

  // Prompt ready card
  if (blPrompt) {
    blockHtml += '<div class="dm5-block-card ok">';
    blockHtml += '  <div class="dm5-block-header ok-hdr">📝 Prompt</div>';
    blockHtml += '  <div class="dm5-block-body">' + (blPrompt.value || '18个prompt全部编写') + '</div>';
    if (blPrompt.note) blockHtml += '  <div class="dm5-block-note">💡 ' + blPrompt.note + '</div>';
    blockHtml += '</div>';
  }

  // Pipeline ready card
  if (blPipeline) {
    blockHtml += '<div class="dm5-block-card ok">';
    blockHtml += '  <div class="dm5-block-header ok-hdr">🔧 接入管线</div>';
    blockHtml += '  <div class="dm5-block-body">' + (blPipeline.value || '代码就绪') + '</div>';
    if (blPipeline.note) blockHtml += '  <div class="dm5-block-note">💡 ' + blPipeline.note + '</div>';
    blockHtml += '</div>';
  }

  blockHtml += '</div>';
  el.insertAdjacentHTML('beforeend', blockHtml);

  // Panel 3: Solution comparison cards with quality bars
  var techHtml = '<div class="dm5-tech-grid">';
  var plans = [
    { name:'Kling', icon:'🎬', price:'¥15/6集', meta:'微信支付 | 1-3分钟/镜', quality:85, qLabel:'高', reco:true, tags:[{t:'微信/支付宝',c:'green'},{t:'中文界面',c:'blue'},{t:'本月可用',c:'green'}] },
    { name:'Seedance', icon:'🌐', price:'$7.50/6集', meta:'外币卡 | 2-5分钟/镜', quality:85, qLabel:'高', reco:false, tags:[{t:'需外币卡',c:'yellow'},{t:'英文界面',c:'yellow'}] },
    { name:'ComfyUI', icon:'🖥️', price:'免费', meta:'本地GPU | ~10分钟/集', quality:50, qLabel:'中', reco:false, tags:[{t:'免费·开源',c:'green'},{t:'本地运行',c:'blue'},{t:'可立即开始',c:'green'}] },
    { name:'Pillow', icon:'📄', price:'免费', meta:'即时生成 | 纯文字画面', quality:20, qLabel:'低', reco:false, tags:[{t:'无画面',c:'yellow'},{t:'TikTok降权',c:'yellow'}] }
  ];
  plans.forEach(function(p) {
    var qFillClass = p.quality >= 80 ? 'high' : p.quality >= 40 ? 'mid' : 'low';
    techHtml += '<div class="dm5-tech-card' + (p.reco ? ' recommended' : '') + '">';
    if (p.reco) techHtml += '<div class="reco-badge">⭐ 推荐</div>';
    techHtml += '  <div class="tc-icon">' + p.icon + '</div>';
    techHtml += '  <div class="tc-name">' + p.name + '</div>';
    techHtml += '  <div class="tc-price">' + p.price + '</div>';
    techHtml += '  <div class="tc-meta">' + p.meta + '</div>';
    techHtml += '  <div class="tc-quality"><div class="tc-quality-bar"><div class="tc-quality-fill ' + qFillClass + '" style="width:' + p.quality + '%"></div></div><span style="font-size:9px;color:#888;margin-top:2px">画质 ' + p.quality/10 + '/10 &nbsp;' + (p.quality>=80?'🟢':p.quality>=40?'🟡':'🔴') + ' ' + p.qLabel + '</span></div>';
    techHtml += '  <div class="tc-tags">';
    p.tags.forEach(function(t) { techHtml += '<span class="tc-tag ' + t.c + '">' + t.t + '</span>'; });
    techHtml += '  </div>';
    techHtml += '</div>';
  });
  techHtml += '</div>';
  el.insertAdjacentHTML('beforeend', techHtml);

  // Panel 3.3: Quality prediction + time estimate (director's decision data)
  if (exQuality || exTime) {
    var predHtml = '<div style="font-size:10px;color:#888;font-weight:600;margin:12px 0 4px">📊 产出预测</div><div class="dm5-pred-grid">';
    if (exQuality) {
      var qVal = exQuality.value || 'Seedance: 1080p · 24fps · 8K photorealistic';
      var qBefore = exQuality.before || '';
      predHtml += '<div class="dm5-pred-card wide"><div class="pred-icon">🎨</div><div class="pred-label">预期画质</div><div class="pred-val">' + qVal.replace(/·/g,'<br>') + '</div>';
      if (qBefore) predHtml += '<div class="pred-compare">' + qBefore + '</div>';
      predHtml += '</div>';
    }
    if (exTime) {
      var tVal = exTime.value || 'Seedance: 约2-5分钟/镜 · 18镜≈60分钟';
      predHtml += '<div class="dm5-pred-card"><div class="pred-icon">⏱️</div><div class="pred-label">生成时间</div><div class="pred-val">' + tVal.replace(/·/g,'<br>') + '</div></div>';
    }
    predHtml += '</div>';
    el.insertAdjacentHTML('beforeend', predHtml);
  }

  // Panel 3.4: Pipeline flow diagram
  el.insertAdjacentHTML('beforeend',
    '<div style="font-size:10px;color:#888;font-weight:600;margin:12px 0 4px">🔀 生成管线</div>' +
    '<div class="dm5-flow-bar">' +
    '  <div class="dm5-flow-step done"><div class="flow-icon">📖</div><div class="flow-label">bible</div></div><span class="dm5-flow-arrow">→</span>' +
    '  <div class="dm5-flow-step done"><div class="flow-icon">🐍</div><div class="flow-label">pipeline</div></div><span class="dm5-flow-arrow">→</span>' +
    '  <div class="dm5-flow-step block"><div class="flow-icon">🔑</div><div class="flow-label">API Key</div></div><span class="dm5-flow-arrow">→</span>' +
    '  <div class="dm5-flow-step"><div class="flow-icon">🤖</div><div class="flow-label">AI生成</div></div><span class="dm5-flow-arrow">→</span>' +
    '  <div class="dm5-flow-step"><div class="flow-icon">🎥</div><div class="flow-label">ffmpeg</div></div>' +
    '</div>' +
    '<div style="font-size:9px;color:#f59e0b;margin:4px 0 12px">⚠️ 阻塞在「API Key」→ 解决后 10 分钟内可跑通整条管线</div>'
  );

  // Panel 3.5: Consistency risk warning
  if (exRisk) {
    el.insertAdjacentHTML('beforeend',
      '<div class="dm5-consistency-risk">' +
      '  <div class="risk-icon">⚠️</div>' +
      '  <div>' +
      '    <div class="risk-title">一致性风险警告</div>' +
      '    <div class="risk-body">' + (exRisk.value || '').replace(/·/g, '<br>') + '</div>' +
      (exRisk.note ? '<div class="risk-mitigation">💡 ' + exRisk.note + '</div>' : '') +
      '  </div>' +
      '</div>'
    );
  }

  // Panel 3.6: Kling hint (when blocked)
  if (blocked) {
    el.insertAdjacentHTML('beforeend',
      '<div class="dm5-kling-hint">💡 推荐方案：Kling (可灵) — 中文界面 + 微信/支付宝支付 · ¥15/6集 · 1-3分钟/镜 · 国内可用</div>'
    );
  }

  // Panel 3.7: 优化四：fal.ai 注册流程折叠
  if (blReg) {
    var regId = 'dm5-reg-flow';
    el.insertAdjacentHTML('beforeend',
      '<div class="info-card collapsible dm5-reg-card" id="' + regId + '">' +
      '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
      '    <span>📋 fal.ai 注册流程（5步）</span><span class="toggle-icon">▼</span>' +
      '  </div>' +
      '  <div class="info-card-body" style="display:none">' +
      '    <div class="dm5-block-body">' + (blReg.value || '') + '</div>' +
      '  </div>' +
      '</div>'
    );
    if (blocked) {
      el.insertAdjacentHTML('beforeend',
        '<div class="dm5-kling-hint">提示：推荐使用 Kling 替代 fal.ai，无需此注册流程</div>'
      );
    }
  }

  // Panel 4: Collapsible tech log
  var techSecId = 'dm5-tech-log';
  el.insertAdjacentHTML('beforeend',
    '<div class="info-card collapsible" id="' + techSecId + '">' +
    '  <div class="info-card-header" onclick="toggleInfoCard(this)">' +
    '    <span>🔍 AI视频技术日志 (原始数据)</span><span class="toggle-icon">▼</span>' +
    '  </div>' +
    '  <div class="info-card-body" style="display:none">' + renderDefault(detail) + '</div>' +
    '</div>'
  );

  // Panel 5: Next action
  el.insertAdjacentHTML('beforeend',
    '<div class="dm5-next-action">' +
    '  <span style="font-size:11px;color:#888;flex:1">' + (blocked ? '❌ AI视频生成阻塞 — 以下是可用方案：' : '✅ AI视频生成就绪，选择方案启动：') + '</span>' +
    '  <button class="btn-primary btn-lg" onclick="window.open(\'https://kling.kuaishou.com\')">⭐ 前往 Kling (¥15/6集 · 推荐)</button>' +
    '  <button class="btn-secondary" onclick="switchToComfyUI()">🖥️ 用 ComfyUI 免费生成</button>' +
    '  <button class="btn-secondary" onclick="triggerReReview(\'DM-5\')">重新检查</button>' +
    '</div>'
  );
}

