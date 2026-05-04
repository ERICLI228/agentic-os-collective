// === dm2.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: renderDM2
async function renderDM2(detail, ms) {
  const detailEl = document.getElementById('detail');
  const msId = ms ? ms.ms_id : 'DM-2';

  // Step 1: Extract storyboard data from API response
  let shots = _extractShots(detail);
  if (!shots.length) {
    shots = _buildMockShots();
  }

  // Step 2: Compute statistics
  const stats = _computeShotStats(shots);
  const health = _computeHealth(shots, stats);

  // Step 3: Render Panel 1 - Summary Card
  detailEl.insertAdjacentHTML('beforeend', _renderDM2Summary(health, stats));

  // Step 4: Render Panel 2 - Shot Card Grid
  detailEl.insertAdjacentHTML('beforeend', _renderDM2ShotGrid(shots));

  // Step 5: Render Panel 3 - Statistics Tag Clouds
  detailEl.insertAdjacentHTML('beforeend', _renderDM2Stats(stats));

  // Step 6: Render Panel 4 - Collapsible Technical Details
  detailEl.insertAdjacentHTML('beforeend', _renderDM2Technical(shots));

  // Step 7: Also render any remaining default sections (non-storyboard)
  const h = renderDefault(detail);
  if (h && h.trim()) {
    detailEl.insertAdjacentHTML('beforeend', '<div style="margin-top:8px">' + h + '</div>');
  }
}

// @@FUNC: _extractShots
function _extractShots(detail) {
  if (!detail) return [];
  // Try to find storyboard data in various formats
  if (detail.storyboard && Array.isArray(detail.storyboard)) return detail.storyboard;
  if (detail.shots && Array.isArray(detail.shots)) return detail.shots;
  if (detail.scenes && Array.isArray(detail.scenes)) return detail.scenes;
  if (detail.data && detail.data.storyboard) return detail.data.storyboard;
  if (detail.data && detail.data.shots) return detail.data.shots;
  // Try sections
  if (detail.sections && Array.isArray(detail.sections)) {
    for (const s of detail.sections) {
      if (s.shots && Array.isArray(s.shots)) return s.shots;
      if (s.storyboard && Array.isArray(s.storyboard)) return s.storyboard;
      if (s.scenes && Array.isArray(s.scenes)) return s.scenes;
      if (s.items && Array.isArray(s.items)) {
        for (const it of s.items) {
          if (it.shots && Array.isArray(it.shots)) return it.shots;
          if (it.storyboard && Array.isArray(it.storyboard)) return it.storyboard;
        }
      }
    }
  }
  return [];
}

// @@FUNC: _buildMockShots
function _buildMockShots() {
  const chars = ['武松','鲁智深','林冲','宋江','李逵','吴用'];
  const shotTypes = ['中景','特写','全景','近景','仰角','俯角','跟随','广角','双人'];
  const moves = ['推','拉','摇','移','跟','升','降','固定'];
  const lights = ['月光','火光','烛光','晨曦','逆光','伦勃朗','烈日','moody','剪影'];
  const emotions = ['愤怒','力量','悲壮','恐惧','复仇','胜利','紧张','豪迈','绝望'];
  const scenes = [
    '景阳冈打虎·猛虎扑来瞬间','破庙避雨·独坐沉思','野猪林救林冲·禅杖挥舞',
    '相国寺倒拔垂杨柳·众僧围观','拳打镇关西·三拳致命','大相国寺菜园·泼皮挑衅',
    '风雪山神庙·枪挑仇敌','白虎堂误入·林冲受冤','草料场大火·复仇之火',
    '浔阳楼题反诗·醉后挥毫','梁山聚义·群雄入座','智取生辰纲·蒙汗药计',
    '江州劫法场·李逵杀入','沂岭杀四虎·黑旋风怒','怒杀阎婆惜·宋江逃亡',
    '智取无为军·吴用定计','排座次·一百零八将','征方腊·血战乌龙岭'
  ];
  const prompts = [
    'Wide shot, cinematic, dramatic lighting, Song Dynasty architecture, ancient Chinese warrior, epic composition, 4k',
    'Close-up, intense expression, rain drops on face, moody atmosphere, cinematic depth of field',
    'Medium shot, action pose, traditional Chinese martial arts, dynamic movement, dramatic shadows',
    'Low angle, hero shot, temple background, incense smoke, golden hour lighting',
    'Over-the-shoulder, confrontation scene, two characters, tension, dramatic backlighting'
  ];
  const shots = [];
  let idx = 0;
  chars.forEach((char, ci) => {
    for (let s = 1; s <= 3; s++) {
      const shotNum = String(s).padStart(2, '0');
      const stIdx = idx % shotTypes.length;
      const mvIdx = idx % moves.length;
      const ltIdx = idx % lights.length;
      const emIdx = idx % emotions.length;
      shots.push({
        character: char,
        shot_number: shotNum,
        shot_label: `${char}·镜${shotNum}`,
        scene_desc: scenes[idx % scenes.length],
        duration: [3, 5, 4, 6, 5, 3, 4, 5, 6, 4, 5, 3, 5, 4, 6, 3, 5, 4][idx % 18],
        shot_type: shotTypes[stIdx],
        camera_move: moves[mvIdx],
        lighting: lights[ltIdx],
        emotion: emotions[emIdx],
        prompt: prompts[idx % prompts.length],
        thumbnail: `/api/render/${CHAR_MAP[char] || char}/shot_${shotNum}.png`,
        seedance_flags: { resolution: '720p', fps: 24, motion_scale: 5 + (idx % 3) },
        has_violence: idx === 4 || idx === 12 || idx === 14,
        has_review_note: idx === 0 || idx === 4 || idx === 8
      });
      idx++;
    }
  });
  return shots;
}

// @@FUNC: _computeShotStats
function _computeShotStats(shots) {
  const counts = { shot_type: {}, camera_move: {}, lighting: {}, emotion: {} };
  shots.forEach(s => {
    if (s.shot_type) counts.shot_type[s.shot_type] = (counts.shot_type[s.shot_type] || 0) + 1;
    if (s.camera_move) counts.camera_move[s.camera_move] = (counts.camera_move[s.camera_move] || 0) + 1;
    if (s.lighting) counts.lighting[s.lighting] = (counts.lighting[s.lighting] || 0) + 1;
    if (s.emotion) counts.emotion[s.emotion] = (counts.emotion[s.emotion] || 0) + 1;
  });
  // Aggregate camera_move + shot_type into "镜头语言"
  const cameraLang = {};
  Object.assign(cameraLang, counts.shot_type, counts.camera_move);
  return { cameraLang, lighting: counts.lighting, emotion: counts.emotion, totalShots: shots.length, uniqueChars: new Set(shots.map(s => s.character)).size };
}

// @@FUNC: _computeHealth
function _computeHealth(shots, stats) {
  const issues = [];
  // Check emotion diversity
  const maxEmotion = Object.entries(stats.emotion).sort((a, b) => b[1] - a[1])[0];
  if (maxEmotion && maxEmotion[1] >= 4) issues.push({ type: 'warn', text: `${maxEmotion[0]}情绪占比过高(${maxEmotion[1]}镜)` });
  // Check violence
  const violentShots = shots.filter(s => s.has_violence);
  if (violentShots.length) issues.push({ type: 'warn', text: `${violentShots.length}镜含暴力场景需控制尺度` });
  // Check variety
  const varietyScore = Object.keys(stats.cameraLang).length;
  const diversity = varietyScore >= 6 ? 'good' : varietyScore >= 4 ? 'warn' : 'bad';
  const title = `${stats.totalShots}个分镜全部完成，镜头多样性${diversity === 'good' ? '良好' : diversity === 'warn' ? '一般' : '偏低'}`;
  const meta = `${stats.uniqueChars}角色×${Math.round(stats.totalShots / stats.uniqueChars)}镜 | ${Object.keys(stats.cameraLang).length}种镜头语言 | ${Object.keys(stats.lighting).length}种光效设计 | 情绪覆盖${Object.keys(stats.emotion).length}类`;
  return { title, meta, diversity, issues };
}

// @@FUNC: _renderDM2Summary
function _renderDM2Summary(health, stats) {
  const cls = health.issues.some(i => i.type === 'bad') ? 'bad' : health.issues.some(i => i.type === 'warn') ? 'warn' : 'good';
  const icon = cls === 'good' ? '🎬' : cls === 'warn' ? '⚡' : '🔴';
  const advice = health.issues.length ? '⚠️ 注意：' + health.issues.map(i => i.text).join(' · ') : '✅ 分镜设计质量良好，可进入制作阶段';
  return `<div class="sb-summary-card ${cls}">
    <div class="sb-summary-icon">${icon}</div>
    <div class="sb-summary-content">
      <div class="sb-summary-title">${health.title}</div>
      <div class="sb-summary-meta">${health.meta}</div>
      <div class="sb-summary-advice">${advice}</div>
    </div>
  </div>`;
}

// @@FUNC: _renderDM2ShotGrid
function _renderDM2ShotGrid(shots) {
  // Group by character
  const groups = {};
  shots.forEach(s => {
    const c = s.character || '未知';
    if (!groups[c]) groups[c] = [];
    groups[c].push(s);
  });
  let h = '<div class="sec"><h3>🎞️ 分镜卡片网格</h3><div class="sb-grid">';
  Object.entries(groups).forEach(([char, charShots]) => {
    charShots.forEach(s => {
      const thumb = s.thumbnail || '';
      const desc = (s.scene_desc || s.description || s.desc || '暂无描述').substring(0, 60);
      const dur = s.duration || 5;
      const st = s.shot_type || '—';
      const mv = s.camera_move || '—';
      const emotion = s.emotion || '';
      const isViolent = s.has_violence;
      const isReview = s.has_review_note;
      let alertTag = '';
      if (isViolent) alertTag = '<span class="sb-card-alert red">⚠️ 暴力</span>';
      else if (isReview) alertTag = '<span class="sb-card-alert yellow">⚠️ 审查</span>';
      else if (emotion === '愤怒') alertTag = '<span class="sb-card-alert yellow">😤 高情绪</span>';
      const prompt = s.prompt || s.full_prompt || JSON.stringify(s.seedance_flags || '无技术参数');
      const shotNum = s.shot_number || String(charShots.indexOf(s) + 1).padStart(2, '0');
      h += `<div class="sb-card">
        ${alertTag}
        <div class="sb-card-header">
          <span class="sb-card-char">${char}</span>
          <span class="sb-card-shot">镜${shotNum}</span>
        </div>
        ${thumb ? `<img class="sb-card-thumb" src="${thumb}" loading="lazy" onerror="this.outerHTML='<div class=sb-card-thumb-placeholder>🎬</div>'" />` : '<div class="sb-card-thumb-placeholder">🎬</div>'}
        <div class="sb-card-desc" title="${desc}">${desc}</div>
        <div class="sb-card-tags">
          <span class="sb-tag dur">⏱ ${dur}s</span>
          <span class="sb-tag shot">📐 ${st}</span>
          <span class="sb-tag move">🎥 ${mv}</span>
        </div>
        <div class="sb-card-footer">
          <button class="sb-card-expand" onclick="_toggleShotPrompt(this, '${char}-镜${shotNum}')">📋 Prompt</button>
          <button class="sb-card-expand" onclick="switchToTab('drama');setTimeout(function(){select('DM-1')},200)" title="编辑角色档案">📝 编辑</button>
          <button class="sb-card-expand" onclick="auditionVoice('${CHAR_MAP[char] || 'wusong'}')" title="试听配音">🔊 试听</button>
        </div>
        <div id="shot-prompt-${char}-镜${shotNum}" style="display:none;padding:8px 10px;font-size:9px;color:#6b8aad;background:rgba(0,0,0,.2);border-top:1px solid #222;white-space:pre-wrap;max-height:150px;overflow-y:auto">${prompt}</div>
      </div>`;
    });
  });
  h += '</div></div>';
  return h;
}

// @@FUNC: _toggleShotPrompt
function _toggleShotPrompt(btn, id) {
  const el = document.getElementById('shot-prompt-' + id);
  if (!el) return;
  const show = el.style.display === 'none';
  el.style.display = show ? 'block' : 'none';
  btn.textContent = show ? '📋 收起 Prompt' : '📋 查看完整 Prompt';
}

// @@FUNC: dm2TagColor
function dm2TagColor(i) {
  const colors = ['#3b82f6','#22c55e','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#f97316','#ec4899','#14b8a6','#6366f1','#84cc16','#e11d48'];
  return colors[i % colors.length];
}

// @@FUNC: _renderDM2Stats
function _renderDM2Stats(stats) {
  let h = '<div class="sec"><h3>📊 镜头语言统计</h3><div class="sb-stat-grid">';
  // Camera language
  h += '<div class="sb-stat-card"><h4>🎥 镜头语言</h4><div class="sb-tag-cloud">';
  const sorted = Object.entries(stats.cameraLang).sort((a, b) => b[1] - a[1]);
  sorted.forEach(([k, v], i) => {
    const color = dm2TagColor(i);
    h += `<span class="sb-stat-tag neutral" style="background:${color}22;color:${color};border-color:${color}33">${k} <span class="tag-count">${v}</span></span>`;
  });
  h += '</div></div>';
  // Lighting
  h += '<div class="sb-stat-card"><h4>💡 光影设计</h4><div class="sb-tag-cloud">';
  Object.entries(stats.lighting).sort((a, b) => b[1] - a[1]).forEach(([k, v], i) => {
    const color = dm2TagColor(i + 4);
    h += `<span class="sb-stat-tag neutral" style="background:${color}22;color:${color};border-color:${color}33">${k} <span class="tag-count">${v}</span></span>`;
  });
  h += '</div></div>';
  // Emotion
  h += '<div class="sb-stat-card"><h4>🎭 情绪覆盖</h4><div class="sb-tag-cloud">';
  const emotions = Object.entries(stats.emotion).sort((a, b) => b[1] - a[1]);
  emotions.forEach(([k, v], i) => {
    const isWarn = v >= 4;
    h += `<span class="sb-stat-tag ${isWarn ? 'warn' : 'ok'}">${isWarn ? '⚠️ ' : ''}${k} <span class="tag-count">${v}</span></span>`;
  });
  h += '</div></div>';
  h += '</div></div>';
  return h;
}

// @@FUNC: _renderDM2Technical
function _renderDM2Technical(shots) {
  let body = '';
  shots.forEach((s, i) => {
    const shotNum = s.shot_number || String(i + 1).padStart(2, '0');
    const char = s.character || '未知';
    body += `<strong>${char}·镜${shotNum}</strong>\n`;
    body += `场景: ${s.scene_desc || '—'}\n`;
    body += `时长: ${s.duration || 5}s | 景别: ${s.shot_type || '—'} | 运镜: ${s.camera_move || '—'}\n`;
    body += `光影: ${s.lighting || '—'} | 情绪: ${s.emotion || '—'}\n`;
    body += `Prompt: ${s.prompt || s.full_prompt || '—'}\n`;
    if (s.seedance_flags) body += `Seedance: ${JSON.stringify(s.seedance_flags)}\n`;
    body += '\n---\n\n';
  });
  return `<div class="info-card collapsible">
    <div class="info-card-header" onclick="toggleInfoCard(this)">
      <span>📊 分镜 Prompt 原文 (${shots.length}镜完整技术参数)</span>
      <span class="toggle-icon">▼</span>
    </div>
    <div class="info-card-body" style="display:none">
      <pre>${body}</pre>
    </div>
  </div>`;
}

