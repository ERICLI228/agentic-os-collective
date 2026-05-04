// === dm1_characters.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===
const TIANGANG_COUNT = 36;
const DM1_TOP10 = 10;
let currentDM1Filter = { query: '', category: '' };

// @@FUNC: renderDM1
async function renderDM1(detail, ms) {
  const detailEl = document.getElementById('detail');
  let sec = `<div class="sec" id="dm1-sec"><h3>🎭 角色档案系统 (DM-1)</h3>
    <p style="font-size:10px;color:#555;margin-bottom:4px">点击「编辑档案」修改角色设定 · 修改后自动检测是否需重新渲染</p>
    <div class="dm1-searchbar">
      <input class="dm1-search-box" id="dm1-search" placeholder="搜索角色名、称号或星宿…" oninput="onDM1Search(this.value)" value="" />
    </div>
    <div class="dm1-filter-chips" id="dm1-chips">
      <span class="dm1-chip active" onclick="onDM1Chip(this,'')">全部</span>
      <span class="dm1-chip" onclick="onDM1Chip(this,'tiangang')">三十六天罡</span>
      <span class="dm1-chip" onclick="onDM1Chip(this,'dishap')">七十二地煞</span>
      <span class="dm1-chip" onclick="onDM1Chip(this,'core')">主要角色</span>
    </div>
    <div id="dm1-characters">
      <div class="dm1-skeleton-grid">
        <div class="dm1-skeleton-card"><div class="sk-line w80"></div><div class="sk-line w60"></div><div class="sk-line w40"></div></div>
        <div class="dm1-skeleton-card"><div class="sk-line w80"></div><div class="sk-line w60"></div><div class="sk-line w40"></div></div>
        <div class="dm1-skeleton-card"><div class="sk-line w80"></div><div class="sk-line w60"></div><div class="sk-line w40"></div></div>
        <div class="dm1-skeleton-loading">正在加载角色档案...</div>
      </div>
    </div>
    <div class="dm1-showing" id="dm1-showing" style="display:none"></div>
  </div>`;
  detailEl.insertAdjacentHTML('beforeend', sec);
  const container = document.getElementById('dm1-characters');

  // Fetch all characters with bulk endpoint (single request)
  let results = [];
  try {
    const resp = await fetch('/api/characters/all');
    console.log('DM-1 fetch status:', resp.status);
    if (resp.ok) {
      const json = await resp.json();
      console.log('DM-1 json keys:', Object.keys(json));
      if (json && json.characters && Array.isArray(json.characters)) {
        results = json.characters;
        console.log('DM-1 first char:', results[0].name);
      }
    }
  } catch(e) {
    console.warn('DM-1 bulk fetch error:', e.message);
  }
  console.log('DM-1 results count:', results.length);
  if (results.length === 0) {
    container.innerHTML = '<div style="color:#f59e0b;padding:20px;text-align:center">⚠️ 角色数据加载失败。请检查服务端 /api/characters/all 端点是否正常。<br><button onclick="renderDM1(null,null)" style="margin-top:8px">🔄 重试</button></div>';
    return;
  }

  let html = '';
  results.forEach((data, i) => {
    if (!data) return;
    let name = data.name || CHAR_NAMES[i];
    let fid = data.pinyin || CHAR_MAP[name] || name;
    // Bulk API returns flat structure, legacy API returns nested profile
    let profile = data.profile || data;
    if (profile.profile && typeof profile.profile === 'object' && !Array.isArray(profile.profile)) {
      profile = profile.profile;
    }
    const renders = data.renders || [];
    const basic = profile.basic_info || {};
    const personality = profile.personality || {};
    const appearance = profile.appearance || {};
    const background = profile.background || {};
    const rawVoice = profile.voice || {};
    var voice = rawVoice;
    if (typeof voice === 'string') {
      var parsed = {};
      var m = voice.match(/nls_voice\s*=\s*(\S+)/);
      if (m) parsed.nls_speaker = m[1];
      var m2 = voice.match(/\(([^)]+)\)/);
      if (m2) parsed.description = m2[1];
      voice = parsed;
    }
    if (voice.nls_speaker || voice.provider) {
      CHARACTER_VOICES[fid] = {
        ref: voice.ref || '/Users/hokeli/GPT-SoVITS/output/' + fid + '_cosyvoice.wav',
        prompt: voice.reference_text || voice.sample_text || name + '在此！',
        speaker: voice.nls_speaker || '',
        provider: voice.provider || 'NLS'
      };
    }
    const videoPrompts = (typeof data.video_prompts === 'object' && !Array.isArray(data.video_prompts)) ? data.video_prompts : (typeof profile.video_prompts === 'object' && !Array.isArray(profile.video_prompts) ? profile.video_prompts : {});
    const title = profile.title || data.title || CHAR_ROLES[name] || '';
    const cp = appearance.color_palette || {};
    const mainRender = renders.length > 0 ? renders[0] : `/api/render/${fid}/shot_01.png`;

    html += `<div class="char-bible" id="charbible-${fid}">
      <div class="char-bible-header">
        <span class="cb-name">${name}</span>
        <span class="cb-title">${title}</span>
        <button class="cb-edit-btn" onclick="toggleCharBibleEdit('${fid}')">✏️ 编辑档案</button>
      </div>
      <div class="cb-body">
        <div class="cb-left">
          <img src="${mainRender}" loading="lazy" onclick="zoomImg('${mainRender}')" onerror="this.style.display='none'" />
          <div class="cb-thumbnails" id="cbthumbs-${fid}">`;
    // Count renders for consistency warning
    var renderCount = renders.length || 0;
    if (renderCount === 0) {
      for (var si = 1; si <= 3; si++) {
        var shot = String(si).padStart(2, '0');
        var url = '/api/render/' + fid + '/shot_' + shot + '.png';
        html += '<div class="cb-thumb-wrap"><img class="cb-thumb" src="' + url + '" loading="lazy" onclick="swapCharImg(\"' + fid + '\",\"' + url + '\",this)" onerror="this.parentElement.remove()" /><button class="cb-thumb-del" title="删除此角度" onclick="event.stopPropagation();deleteRenderFile(\"' + fid + '\",\"shot_' + shot + '.png\",this)" onmouseover="showDelTooltip(event,\"单击删除\")">✕</button></div>';
      }
    } else {
      renders.forEach(function(r, ri) {
        var url = typeof r === 'string' ? r : (r.url || r.src || '');
        if (!url) return;
        var filename = url.split('/').pop();
        html += '<div class="cb-thumb-wrap"><img class="cb-thumb' + (ri === 0 ? ' active' : '') + '" src="' + url + '" loading="lazy" onclick="swapCharImg(\"' + fid + '\",\"' + url + '\",this)" /><button class="cb-thumb-del" title="删除此角度" onclick="event.stopPropagation();deleteRenderFile(\"' + fid + '\",\"' + filename + '\",this)" onmouseover="showDelTooltip(event,\"单击删除\")">✕</button></div>';
      });
    }
    html += '</div>';
    // Consistency warning if 3+ renders
    if (renderCount >= 3) {
      html += '<div class="cb-consistency-warn"><span>⚠️ 多角度一致性风险</span><span style="font-size:8px;color:#888">有 ' + renderCount + ' 张渲染图，AI 多角度生成可能不一致。点击 ✕ 删除不一致的图 → 「🔁 重新生成」</span></div>';
    }
    var regenOnclick = "regenerateCharacter('" + fid + "',this)";
    html += '<div class="cb-thumb-actions"><button class="mini-btn" onclick="' + regenOnclick + '" style="font-size:9px;margin-top:4px">\u267B 重新生成所有角度</button></div>' +
        `</div>
        <div class="cb-right">
          <!-- 基本信息 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">📏</span> 基本信息</div>
            <div class="cb-section-content">${basic.height || ''} · ${basic.build || ''} · ${basic.face || ''} · ${basic.age || ''}</div>
          </div>
          <!-- 性格特征 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🎨</span> 性格特征</div>
            <div class="cb-section-content">
              <div class="cb-traits">${(personality.core_traits || []).map(t => `<span class="cb-trait">${t}</span>`).join('')}</div>
              <div style="font-size:10px;color:#888;margin-top:4px">${personality.emotional_range || ''}</div>
              <div style="font-size:10px;color:#666">${personality.speech_style || ''}</div>
            </div>
          </div>
          <!-- 口头禅 -->
          ${(personality.catchphrases || []).length > 0 ? `<div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🗣️</span> 口头禅</div>
            <div class="cb-section-content">${(personality.catchphrases || []).map(c => `<div class="cb-catchphrase">${c}</div>`).join('')}</div>
          </div>` : ''}
          <!-- 习性 -->
          ${(personality.habits || []).length > 0 ? `<div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🍺</span> 习性</div>
            <div class="cb-section-content">${(personality.habits || []).map(h => `<div class="cb-habits">• ${h}</div>`).join('')}</div>
          </div>` : ''}
          <!-- 服饰设计 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">👔</span> 服饰设计</div>
            <div class="cb-section-content">
              ${appearance.costume || '待补充'}
              <div class="cb-colors">${cp.primary ? `<div class="cb-color-swatch" style="background:${cp.primary}" title="主色"></div><span class="cb-color-label">主</span>` : ''}${cp.secondary ? `<div class="cb-color-swatch" style="background:${cp.secondary}" title="辅色"></div><span class="cb-color-label">辅</span>` : ''}${cp.accent ? `<div class="cb-color-swatch" style="background:${cp.accent}" title="点缀"></div><span class="cb-color-label">点缀</span>` : ''}</div>
              ${(appearance.accessories || []).length > 0 ? `<div style="font-size:9px;color:#666">配饰: ${(appearance.accessories || []).join(' · ')}</div>` : ''}
            </div>
          </div>
          <!-- 角色背景 -->
          <div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">📖</span> 角色背景</div>
            <div class="cb-section-content">
              ${background.origin ? `<div style="font-size:10px">出身: ${background.origin}</div>` : ''}
              ${(background.key_events || []).length > 0 ? `<div style="font-size:10px">关键事件: ${(background.key_events || []).join(' → ')}</div>` : ''}
              ${Object.keys(background.relationships || {}).length > 0 ? `<div class="cb-relations">关系: ${Object.entries(background.relationships || {}).map(([k, v]) => `<span class="rel-name">${k}</span>: ${v}`).join(' · ')}</div>` : ''}
            </div>
          </div>
          <!-- 音色 (Voice Config) -->
          <div class="cb-section cb-voice-wrap" id="voice-section-${fid}">
            <div class="cb-section-title"><span class="cb-icon">🎤</span> 音色</div>
            <!-- Voice info card -->
            <div class="cb-voice-card" id="voicecard-${fid}">
              <div class="cb-voice-card-body">
                <div class="cb-voice-card-row"><span class="vc-label">角色</span><span class="vc-val">${name}</span></div>
                <div class="cb-voice-card-row"><span class="vc-label">类型</span><span class="vc-val" id="vc-type-${fid}">${voice.nls_speaker ? 'NLS' : (voice.provider || '—')}</span></div>
                <div class="cb-voice-card-row"><span class="vc-label">音色</span><span class="vc-val" id="vc-voice-${fid}">${voice.nls_speaker ? voice.nls_speaker + ' · ' + (voice.description || '') : '未配置'}</span></div>
                <div class="cb-voice-card-row"><span class="vc-label">参考</span><span class="vc-val" id="vc-ref-${fid}">${voice.sample_text || voice.reference_text || '—'}</span></div>
              </div>
              <div class="cb-voice-card-btns">
                <button type="button" class="cb-btn cb-btn-cfg" id="cfgbtn-${fid}" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();toggleVoiceConfigForm('${fid}');return false">🎤 配置音色</button>
                <button type="button" class="cb-btn cb-btn-aud" id="audbtn-${fid}" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();auditionVoice('${fid}');return false" ${(voice.nls_speaker || CHARACTER_VOICES[fid]) ? '' : 'disabled'}>🔊 试听</button>
              </div>
            </div>
            <!-- Inline config form -->
            <div class="cb-voice-config-form" id="voicecfgform-${fid}" style="display:none">
              <div class="cb-voice-config-form-row">
                <label>提供商</label>
                <select id="cfg-provider-${fid}">
                  <option value="NLS" ${!voice.provider || voice.provider==='NLS' ? 'selected' : ''}>NLS（阿里云）</option>
                  <option value="MiniMax" ${voice.provider==='MiniMax' ? 'selected' : ''}>MiniMax</option>
                  <option value="ElevenLabs" ${voice.provider==='ElevenLabs' ? 'selected' : ''}>ElevenLabs</option>
                </select>
              </div>
              <div class="cb-voice-config-form-row">
                <label>音色名称</label>
                <input id="cfg-voice-${fid}" value="${voice.nls_speaker || ''}" placeholder="如 zhiming" />
              </div>
              <div class="cb-voice-config-form-row">
                <label>参考文本</label>
                <input id="cfg-reftext-${fid}" value="${voice.reference_text || voice.sample_text || ''}" placeholder="试听参考文本" />
              </div>
              <div class="cb-voice-config-form-btns">
                <button type="button" class="btn btn-save" onclick="saveVoiceConfig('${fid}')">💾 保存并试听</button>
                <button type="button" class="btn btn-cancel" onclick="toggleVoiceConfigForm('${fid}')">取消</button>
              </div>
            </div>
            <!-- Audio player row -->
            <div class="cb-voice-player-row" id="voiceplayerrow-${fid}" style="display:none">
              <div class="cb-voice-player" id="voiceplayer-${fid}">
                <audio id="voiceaudio-${fid}" controls></audio>
                <span class="cb-dur" id="voicedur-${fid}"></span>
              </div>
              <button type="button" class="cb-voice-close" id="voiceclose-${fid}" onclick="closeVoicePlayer('${fid}')" title="关闭播放">✕</button>
            </div>
            <!-- Custom TTS generation row -->
            <div class="cb-voice-row">
              <input class="cb-voice-input" id="ttstext-${fid}" placeholder="试生成文本..." value="${voice.sample_text || name + '在此！'}" style="flex:1" />
              <button type="button" class="cb-btn cb-btn-gen" id="genbtn-${fid}" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();generateVoice('${fid}');return false">🔊 生成</button>
              <button type="button" class="cb-btn cb-btn-gen" id="regenbtn-${fid}" style="display:none" onmousedown="event.preventDefault()" onclick="event.preventDefault();event.stopPropagation();generateVoice('${fid}');return false">🔄 重新生成</button>
            </div>
            <div id="voicespinner-${fid}" style="display:none;text-align:center;padding:4px">
              <span class="cb-voice-spinner"></span> <span style="font-size:10px;color:#6b8aad">生成中...</span>
            </div>
          </div>
          <!-- Video Prompts (三方案) -->
          ${Object.keys(videoPrompts).length > 0 ? `<div class="cb-section">
            <div class="cb-section-title"><span class="cb-icon">🎬</span> 视频提示词（三方案）</div>
            ${Object.entries(videoPrompts).map(([key, v]) => `
              <div class="cb-vp-card">
                <div class="cb-vp-card-hdr" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">
                  <span class="vp-icon">📋</span> ${v.title || key}
                  <span style="font-size:9px;color:#555">${v['参数'] || ''}</span>
                  <span style="margin-left:auto;display:flex;gap:3px">
                    <button class="vp-btn vp-preview-btn" onclick="event.stopPropagation();previewVideoPrompt('${fid}','${key}')" title="视频预览">🎥</button>
                    <button class="vp-btn" onclick="event.stopPropagation();editVideoPrompt('${fid}','${key}')" title="调整提示词">✏️</button>
                  </span>
                </div>
                <div class="cb-vp-card-body" style="display:none">
                  <div class="cb-vp-line"><span class="vp-label">描述</span><span class="vp-val">${v.desc || v['desc'] || ''}</span></div>
                  <div class="cb-vp-line"><span class="vp-label">提示词</span><span class="vp-val vp-prompt">${v.prompt || v['prompt'] || ''}</span></div>
                  ${v['简练版'] ? `<div class="cb-vp-line"><span class="vp-label">简练版</span><span class="vp-val vp-prompt">${v['简练版']}</span></div>` : ''}
                </div>
                <div class="cb-vp-edit" id="vpedit-${fid}-${key}" style="display:none">
                  <div class="cb-vp-edit-row"><label>描述</label><textarea id="vpedit-desc-${fid}-${key}">${(v.desc || v['desc'] || '')}</textarea></div>
                  <div class="cb-vp-edit-row"><label>提示词</label><textarea id="vpedit-prompt-${fid}-${key}">${(v.prompt || v['prompt'] || '')}</textarea></div>
                  <div class="cb-vp-edit-btns">
                    <button class="btn btn-save" onclick="saveVideoPrompt('${fid}','${key}')">💾 保存</button>
                    <button class="btn btn-cancel" onclick="editVideoPrompt('${fid}','${key}')">取消</button>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>` : ''}
          <!-- Actions -->
          <div class="cb-actions">
            <button class="cb-btn" id="rerender-btn-${fid}" onclick="reRenderChar('${fid}')">🔄 重新生成角色图</button>
            <button class="cb-btn" onclick="generateAIProfile('${fid}',this)">✨ AI 生成档案</button>
          </div>
          <div class="cb-rerender-progress" id="rerender-prog-${fid}">
            <div class="cb-prog-bar"><div class="cb-prog-fill" id="rerender-fill-${fid}"></div></div>
            <div class="cb-prog-text" id="rerender-text-${fid}">渲染中...</div>
          </div>
        </div>
      </div>
      <!-- Edit mode (hidden by default) -->
      <div class="cb-edit-mode" id="cbedit-${fid}">
        <div class="cb-field"><label>📏 身高</label><input id="edit-basic_height-${fid}" type="text" value="${basic.height || ''}" /></div>
        <div class="cb-field"><label>💪 体型</label><input id="edit-basic_build-${fid}" type="text" value="${basic.build || ''}" /></div>
        <div class="cb-field"><label>👤 面相</label><input id="edit-basic_face-${fid}" type="text" value="${basic.face || ''}" /></div>
        <div class="cb-field"><label>🎨 核心性格 (逗号分隔)</label><input id="edit-traits-${fid}" type="text" value="${(personality.core_traits || []).join(',')}" /></div>
        <div class="cb-field"><label>💭 情感层次</label><textarea id="edit-emotion-${fid}">${personality.emotional_range || ''}</textarea></div>
        <div class="cb-field"><label>🗣️ 说话风格</label><input id="edit-speech-${fid}" type="text" value="${personality.speech_style || ''}" /></div>
        <div class="cb-field"><label>💬 口头禅 (一行一句)</label><textarea id="edit-catchphrases-${fid}">${(personality.catchphrases || []).join('\n')}</textarea></div>
        <div class="cb-field"><label>🍺 习性 (一行一条)</label><textarea id="edit-habits-${fid}">${(personality.habits || []).join('\n')}</textarea></div>
        <div class="cb-field"><label>👔 服饰描述</label><textarea id="edit-costume-${fid}">${appearance.costume || ''}</textarea></div>
        <div class="cb-field"><label>🎨 配色</label>
          <div class="cb-color-input">
            <span class="cb-color-label">主</span><input type="color" id="edit-cp-primary-${fid}" value="${cp.primary || '#1a1a2e'}" />
            <span class="cb-color-label">辅</span><input type="color" id="edit-cp-secondary-${fid}" value="${cp.secondary || '#8b0000'}" />
            <span class="cb-color-label">点缀</span><input type="color" id="edit-cp-accent-${fid}" value="${cp.accent || '#d4a574'}" />
          </div>
        </div>
        <div class="cb-field"><label>📖 出身</label><input id="edit-origin-${fid}" type="text" value="${background.origin || ''}" /></div>
        <div class="cb-field"><label>🔑 关键事件 (逗号分隔)</label><input id="edit-events-${fid}" type="text" value="${(background.key_events || []).join(',')}" /></div>
        <div class="cb-field"><label>🎤 音色 Speaker</label><input id="edit-voice-${fid}" type="text" value="${voice.nls_speaker || ''}" /></div>
        <div class="cb-field"><label>🎤 音色描述</label><input id="edit-voice-desc-${fid}" type="text" value="${voice.description || ''}" /></div>
        <div class="cb-field"><label>📝 参考文本</label><input id="edit-reftext-${fid}" type="text" value="${voice.reference_text || ''}" /></div>
        <div class="cb-field"><label>📝 试生成文本</label><input id="edit-ttstext-${fid}" type="text" value="${voice.sample_text || ''}" /></div>
        <div class="cb-edit-btns">
          <button class="btn btn-save" onclick="saveCharBible('${fid}')">💾 保存修改</button>
          <button class="btn btn-cancel" onclick="toggleCharBibleEdit('${fid}')">取消</button>
          <button class="btn btn-ai" onclick="generateAIProfile('${fid}')">✨ AI 生成</button>
        </div>
      </div>
    </div>`;
  });
  container.innerHTML = html;
  // Populate cache for searching
  charDataCache = results.map((data, i) => {
    if (!data) return null;
    const name = data.name || CHAR_NAMES[i];
    const fid = data.pinyin || CHAR_MAP[name] || name;
    let profile = data.profile || data;
    if (profile.profile && typeof profile.profile === 'object' && !Array.isArray(profile.profile)) profile = profile.profile;
    const personality = profile.personality || {};
    const title = profile.title || CHAR_ROLES[name] || '';
    const star = profile.star_name || '';
    return { name, fid, title, star, isTiangang: i < TIANGANG_COUNT, index: i, el: document.getElementById('charbible-' + fid) };
  }).filter(Boolean);
  // Default: Top 10, show hint
  applyDM1Filter();

  // v3.7.3: 角色资产缩略图网格 (仅主要角色)
  renderDM1Assets(results);
}

// @@FUNC: renderDM1Assets
function renderDM1Assets(charResults){
  if(!charResults||!charResults.length)return;
  const topChars=charResults.slice(0,12);
  const detailEl=document.getElementById('detail');
  if(!detailEl)return;

  let h='<div class="sec" id="dm1-assets-sec"><h3>&#127912; 角色资产预览</h3>';
  h+='<p style="font-size:9px;color:#555;margin-bottom:8px">主要角色定妆照缩略图 · 点击放大</p>';
  h+='<div class="dm1-asset-grid">';
  topChars.forEach(function(c){
    const fid=c.pinyin||c.fid||(c.name||'').toLowerCase().replace(/\s+/g,'');
    const name=c.name||'';
    const title=c.title||c.profile?.title||'';
    let urls=[];
    var renders=c.renders||(c.profile&&c.profile.renders)||[];
    if(renders.length){
      urls=renders.map(function(r){return typeof r==='string'?r:(r.url||r.src||'');}).filter(Boolean);
    }
    if(!urls.length){
      urls=['/api/render/'+fid+'/shot_01.png','/api/render/'+fid+'/shot_02.png','/api/render/'+fid+'/shot_03.png'];
    }
    h+='<div class="dm1-asset-item">';
    h+='<div class="dm1-asset-name">'+name+'</div>';
    if(title) h+='<div class="dm1-asset-title">'+title+'</div>';
    h+='<div class="dm1-asset-thumbs">';
    urls.slice(0,4).forEach(function(u){
      if(u) h+='<img class="dm1-asset-thumb" src="'+u+'" loading="lazy" onclick="zoomImg(\''+u+'\')" onerror="this.style.display=\'none\'"/>';
    });
    h+='</div></div>';
  });
  h+='</div></div>';
  detailEl.insertAdjacentHTML('beforeend',h);
}

// @@FUNC: applyDM1Filter
function applyDM1Filter() {
  const q = (currentDM1Filter.query || '').toLowerCase();
  const cat = currentDM1Filter.category || '';
  let visible = 0;
  charDataCache.forEach(c => {
    // Refresh stale DOM refs after re-render
    if (c.el && !c.el.parentElement) c.el = document.getElementById('charbible-' + c.fid);
    if (!c.el) { c.el = document.getElementById('charbible-' + c.fid); }
    if (!c.el) return;
    let show = true;
    if (cat === 'tiangang') show = c.isTiangang;
    else if (cat === 'dishap') show = !c.isTiangang;
    else if (cat === 'core') show = c.index < 12;
    if (show && q) {
      const s = (c.name + ' ' + c.title + ' ' + c.star).toLowerCase();
      show = s.includes(q);
    }
    if (show && !q && !cat) show = c.index < DM1_TOP10;
    c.el.style.display = show ? '' : 'none';
    if (show) visible++;
  });
  const hint = document.getElementById('dm1-showing');
  if (!q && !cat) {
    hint.style.display = 'block';
    hint.textContent = '已展示 ' + visible + ' 位核心角色，共 ' + charDataCache.length + ' 位，请搜索查看更多';
  } else {
    hint.style.display = 'block';
    hint.textContent = '筛选结果: ' + visible + ' / ' + charDataCache.length + ' 位角色';
  }
}

// @@FUNC: onDM1Search
function onDM1Search(val) {
  clearTimeout(dm1Timer);
  dm1Timer = setTimeout(function() {
    currentDM1Filter.query = val;
    if (val) { currentDM1Filter.category = ''; document.querySelectorAll('#dm1-chips .dm1-chip').forEach(function(c){c.classList.remove('active')}); }
    applyDM1Filter();
  }, 300);
}

// @@FUNC: onDM1Chip
function onDM1Chip(el, cat) {
  document.querySelectorAll('#dm1-chips .dm1-chip').forEach(function(c){c.classList.remove('active')});
  el.classList.add('active');
  currentDM1Filter.category = cat;
  currentDM1Filter.query = '';
  document.getElementById('dm1-search').value = '';
  applyDM1Filter();
}

// @@FUNC: showAddCharForm
function showAddCharForm() {
  var existing = document.getElementById('dm1-add-char-modal');
  if (existing) { existing.remove(); return; }
  var modal = document.createElement('div');
  modal.id = 'dm1-add-char-modal';
  modal.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid #22c55e;border-radius:8px;padding:16px;z-index:500;width:380px;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,.5)';
  modal.innerHTML = '<div style="font-size:14px;font-weight:700;color:#22c55e;margin-bottom:12px">+ 新增角色</div>' +
    '<div class="dm1-add-field"><label>角色名 *</label><input id="dm1-add-name" placeholder="如：武松" /></div>' +
    '<div class="dm1-add-field"><label>称号</label><input id="dm1-add-title" placeholder="如：行者" /></div>' +
    '<div class="dm1-add-field"><label>星宿</label><input id="dm1-add-star" placeholder="如：天伤星" /></div>' +
    '<div class="dm1-add-field"><label>拼音 (英文ID)</label><input id="dm1-add-pinyin" placeholder="如：wusong" /></div>' +
    '<div class="dm1-add-field"><label>性别</label><select id="dm1-add-gender"><option value="男">男</option><option value="女">女</option></select></div>' +
    '<div class="dm1-add-field"><label>正/反派</label><select id="dm1-add-alignment"><option value="正">正派</option><option value="反">反派</option><option value="中">中立</option></select></div>' +
    '<div class="dm1-add-field"><label>核心性格 (逗号分隔)</label><input id="dm1-add-traits" placeholder="如：勇猛,忠义,暴烈" /></div>' +
    '<div class="dm1-add-field"><label>身高</label><input id="dm1-add-height" placeholder="如：185cm" /></div>' +
    '<div class="dm1-add-field"><label>体型</label><input id="dm1-add-build" placeholder="如：魁梧" /></div>' +
    '<div class="dm1-add-field"><label>服饰描述</label><input id="dm1-add-costume" placeholder="如：僧袍·铁禅杖" /></div>' +
    '<div class="dm1-add-field"><label>音色</label><input id="dm1-add-voice" placeholder="如：zhiming" /></div>' +
    '<div style="display:flex;gap:8px;margin-top:12px">' +
    '<button class="btn btn-s" onclick="submitNewChar()" style="flex:1">✓ 创建</button>' +
    '<button class="btn btn-cancel" onclick="document.getElementById(\'dm1-add-char-modal\').remove()" style="flex:1">取消</button></div>';
  modal.innerHTML += '<style>.dm1-add-field{margin-bottom:8px}.dm1-add-field label{display:block;font-size:10px;color:#888;margin-bottom:2px}.dm1-add-field input,.dm1-add-field select{width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:5px 8px;border-radius:4px;font-size:11px;box-sizing:border-box}</style>';
  document.body.appendChild(modal);
}

// @@FUNC: submitNewChar
async function submitNewChar() {
  var name = (document.getElementById('dm1-add-name')?.value || '').trim();
  if (!name) { toastMsg('⚠️ 角色名不能为空', 2000, 'warn'); return; }
  var pinyin = (document.getElementById('dm1-add-pinyin')?.value || '').trim() || name.toLowerCase().replace(/\s+/g,'');
  var data = {
    name: name,
    pinyin: pinyin,
    title: (document.getElementById('dm1-add-title')?.value || '').trim(),
    star: (document.getElementById('dm1-add-star')?.value || '').trim(),
    gender: (document.getElementById('dm1-add-gender')?.value || '男'),
    alignment: (document.getElementById('dm1-add-alignment')?.value || '正'),
    personality: {
      core_traits: ((document.getElementById('dm1-add-traits')?.value || '') + ',勇武,忠义').split(',').map(function(s){return s.trim();}).filter(Boolean),
      emotional_range: '范围广',
      speech_style: '沉稳有力'
    },
    appearance: {
      height: (document.getElementById('dm1-add-height')?.value || '').trim(),
      build: (document.getElementById('dm1-add-build')?.value || '').trim(),
      costume: (document.getElementById('dm1-add-costume')?.value || '').trim()
    },
    voice: {
      nls_speaker: (document.getElementById('dm1-add-voice')?.value || '').trim(),
      provider: 'NLS'
    },
    origin: '水浒传角色',
    key_events: []
  };
  var btn = event.target;
  if (btn) { btn.disabled = true; btn.textContent = '⏳ 创建中...'; }
  try {
    var r = await fetch('/api/character/' + pinyin, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    var d = await r.json();
    toastMsg('✅ 角色 ' + name + ' 已创建', 3000, 'success');
    document.getElementById('dm1-add-char-modal')?.remove();
    // Reload DM-1
    setTimeout(function() { select('DM-1'); }, 500);
  } catch(e) {
    toastMsg('❌ 创建失败: ' + e.message, 3000, 'error');
    if (btn) { btn.disabled = false; btn.textContent = '✓ 创建'; }
  }
}

// @@FUNC: extractCharRenderUrls
function extractCharRenderUrls(note) {
  if(!note) return null;
  const m = note.match(/\/api\/render\/(\w+)/);
  return m ? m[1] : null;
}

// @@FUNC: toggleCharBibleEdit
function toggleCharBibleEdit(fid) {
  const el=document.getElementById('cbedit-'+fid);
  if(el){ el.classList.toggle('show'); return; }
  // Edit form not in DOM — navigate to DM-1 and auto-open after render
  switchToTab('drama');
  scrollToDM1Edit(fid);
  toastMsg('🚀 正在打开 ' + fid + ' 角色编辑...', 3000);
  return;
}

// @@FUNC: scrollToDM1Edit
function scrollToDM1Edit(fid) {
  var checkCount = 0;
  var checkInterval = setInterval(function() {
    checkCount++;
    var cb = document.getElementById('charbible-' + fid);
    if (cb) {
      clearInterval(checkInterval);
      // Scroll to view and stabilize
      cb.scrollIntoView({ behavior: 'smooth', block: 'center' });
      select('DM-1');
      // Try to open edit after a small delay
      setTimeout(function() {
        var editEl = document.getElementById('cbedit-' + fid);
        if (editEl) {
          editEl.classList.add('show');
          editEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 600);
    }
    if (checkCount > 30) clearInterval(checkInterval);
  }, 300);
}

// @@FUNC: saveCharBible
async function saveCharBible(fid) {
  const toast = document.getElementById('toast');
  // Collect all form values
  const data = {};
  const basic = {};
  const personality = {};
  const appearance = {};
  const background = {};
  const voice = {};

  // Basic info
  const basicH = document.getElementById('edit-basic_height-' + fid);
  if (basicH) basic.height = basicH.value;
  const basicB = document.getElementById('edit-basic_build-' + fid);
  if (basicB) basic.build = basicB.value;
  const basicF = document.getElementById('edit-basic_face-' + fid);
  if (basicF) basic.face = basicF.value;
  if (Object.keys(basic).length > 0) data.basic_info = basic;

  // Personality
  const traits = document.getElementById('edit-traits-' + fid);
  if (traits) personality.core_traits = traits.value.split(',').map(s => s.trim()).filter(Boolean);
  const emotion = document.getElementById('edit-emotion-' + fid);
  if (emotion) personality.emotional_range = emotion.value;
  const speech = document.getElementById('edit-speech-' + fid);
  if (speech) personality.speech_style = speech.value;
  const cp = document.getElementById('edit-catchphrases-' + fid);
  if (cp) personality.catchphrases = cp.value.split('\n').map(s => s.trim()).filter(Boolean);
  const hab = document.getElementById('edit-habits-' + fid);
  if (hab) personality.habits = hab.value.split('\n').map(s => s.trim()).filter(Boolean);
  if (Object.keys(personality).length > 0) data.personality = personality;

  // Appearance
  const costume = document.getElementById('edit-costume-' + fid);
  if (costume) appearance.costume = costume.value;
  const cpP = document.getElementById('edit-cp-primary-' + fid);
  const cpS = document.getElementById('edit-cp-secondary-' + fid);
  const cpA = document.getElementById('edit-cp-accent-' + fid);
  if (cpP || cpS || cpA) {
    appearance.color_palette = {};
    if (cpP) appearance.color_palette.primary = cpP.value;
    if (cpS) appearance.color_palette.secondary = cpS.value;
    if (cpA) appearance.color_palette.accent = cpA.value;
  }
  if (Object.keys(appearance).length > 0) data.appearance = appearance;

  // Background
  const origin = document.getElementById('edit-origin-' + fid);
  if (origin) background.origin = origin.value;
  const events = document.getElementById('edit-events-' + fid);
  if (events) background.key_events = events.value.split(',').map(s => s.trim()).filter(Boolean);
  if (Object.keys(background).length > 0) data.background = background;

  // Voice
  const vs = document.getElementById('edit-voice-' + fid);
  if (vs) voice.nls_speaker = vs.value;
  const vd = document.getElementById('edit-voice-desc-' + fid);
  if (vd) voice.description = vd.value;
  const rt = document.getElementById('edit-reftext-' + fid);
  if (rt) voice.reference_text = rt.value;
  const st = document.getElementById('edit-ttstext-' + fid);
  if (st) voice.sample_text = st.value;
  if (Object.keys(voice).length > 0) data.voice = voice;

  if (Object.keys(data).length === 0) { toastMsg('⚠️ 无修改内容', 1500, 'warn'); return; }

  // Save
  try {
    const r = await fetch('/api/character/' + fid, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const res = await r.json();
    toastMsg('✅ 保存成功', 2000);
    // Check rerender suggestion
    if (res.rerender && res.rerender.need_rerender) {
      toastMsg('⚡ ' + res.rerender.reason + ' — 建议重新渲染', 4000, 'warn');
    }
    // 0-2: 关闭编辑面板，保持页面上下文 — 不触发全量刷新
    var cb = document.getElementById('charbible-' + fid);
    if (cb && cb.classList.contains('editing')) cb.classList.remove('editing');
    var editForm = document.getElementById('edit-form-' + fid);
    if (editForm) editForm.style.display = 'none';
  } catch (e) {
    toastMsg('❌ 保存失败: ' + e.message, 3000, 'error');
  }
}

// @@FUNC: reRenderChar
async function reRenderChar(fid) {
  const btn = document.getElementById('rerender-btn-' + fid);
  const prog = document.getElementById('rerender-prog-' + fid);
  const fill = document.getElementById('rerender-fill-' + fid);
  const text = document.getElementById('rerender-text-' + fid);
  if (!btn || !prog) return;

  btn.classList.add('busy');
  btn.textContent = '⏳ 渲染中...';
  prog.classList.add('show');
  fill.style.width = '0%';
  text.textContent = '提交渲染任务...';

  try {
    fill.style.width = '20%';
    text.textContent = '渲染中...';
    const r = await fetch('/api/character/' + fid + '/regenerate', { method: 'POST' });
    const res = await r.json();
    fill.style.width = '80%';
    text.textContent = res.message || '渲染任务已提交';
    fill.style.width = '100%';
    toastMsg('✅ 渲染任务已提交', 2000);
  } catch (e) {
    text.textContent = '渲染失败: ' + e.message;
    toastMsg('❌ 渲染失败', 3000, 'error');
  }
  btn.classList.remove('busy');
  btn.textContent = '🔄 重新生成角色图';
  setTimeout(() => prog.classList.remove('show'), 3000);
}

// @@FUNC: generateAIProfile
async function generateAIProfile(fid, btn) {
  if (!btn) btn = document.getElementById('ai-gen-btn-' + fid);
  if (btn) { btn.disabled = true; btn.textContent = '⏳ AI 生成中...'; btn.style.opacity = '0.7'; }
  toastMsg('✨ AI 正在分析角色并生成档案...', 5000);
  try {
    const r = await fetch('/api/character/' + fid + '/generate', { method: 'POST' });
    const res = await r.json();
    if (res.status === 'ok') {
      toastMsg('✅ ' + res.message, 3000, 'success');
      if (btn) { btn.textContent = '✅ 已生成'; btn.style.background = '#22c55e'; }
      setTimeout(function() { select('DM-1'); }, 1000);
    } else {
      toastMsg('❌ 生成失败: ' + (res.error || '未知错误'), 3000, 'error');
      if (btn) { btn.disabled = false; btn.textContent = '✨ AI 生成档案'; btn.style.opacity = '1'; }
    }
  } catch (e) {
    toastMsg('❌ 生成失败: ' + e.message, 3000, 'error');
    if (btn) { btn.disabled = false; btn.textContent = '✨ AI 生成档案'; btn.style.opacity = '1'; }
  }
}

// @@FUNC: swapCharImg
function swapCharImg(fid, url, thumbEl) {
  const bible = document.getElementById('charbible-' + fid);
  if (!bible) return;
  const img = bible.querySelector('.cb-left img');
  if (img) img.src = url;
  bible.querySelectorAll('.cb-thumb').forEach(t => t.classList.remove('active'));
  if (thumbEl) thumbEl.classList.add('active');
}

// @@FUNC: loadCharGal
async function loadCharGal(charName){
  const galleryEl=document.getElementById('chargal-'+charName);
  const statusEl=document.getElementById('chargal-status-'+charName);
  if(!galleryEl)return;
  try{
    const r=await fetch('/api/character/'+charName);
    const data=await r.json();
    const renders=data.renders||data.designs||data.images||[];
    if(renders.length>0){
      let imgs='';
      renders.forEach(rd=>{
        const url=typeof rd==='string'?rd:(rd.url||rd.src||'');
        const label=rd.label||rd.name||'';
        if(url)imgs+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.style.display='none'"/><span class="img-label">${label}</span></div>`;
      });
      galleryEl.innerHTML=imgs?`<div class="img-gallery">${imgs}</div>`:'<span style="font-size:10px;color:#555;">无渲染图</span>';
    }else{
      let found=0,imgs='';
      for(let i=1;i<=3;i++){
        const shot=String(i).padStart(2,'0');
        const url=`/api/render/${charName}/shot_${shot}.png`;
        const ok=await checkImage(url);
        if(ok){imgs+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${url}')"><img src="${url}" loading="lazy" onerror="this.parentElement.remove()"/><span class="img-label">镜${shot}</span></div>`;found++;}
      }
      galleryEl.innerHTML=found>0?`<div class="img-gallery">${imgs}</div>`:'<span style="font-size:10px;color:#555;">无渲染图 &middot; 点击"重新生成"</span>';
    }
    if(statusEl)statusEl.remove();
  }catch(e){
    galleryEl.innerHTML='<span style="font-size:10px;color:#555;">加载失败</span>';
    if(statusEl)statusEl.remove();
  }
}

// @@FUNC: saveChar
async function saveChar(charName){
  const voiceEl=document.getElementById('voice-'+charName);
  const colorEl=document.getElementById('color-'+charName);
  const data={};
  if(voiceEl)data.voice=voiceEl.value;
  if(colorEl)data.color=colorEl.value;
  try{
    const r=await fetch('/api/character/'+charName,{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    if(r.ok){
      toastMsg('角色已更新: '+charName);
      document.getElementById('charedit-'+charName).classList.remove('show');
      loadCharGal(charName);
    }else toastMsg('更新失败');
  }catch(e){toastMsg('更新失败: '+e.message)}
}

// @@FUNC: reRender
async function reRender(charName){
  const btn=document.getElementById('rerender-btn-'+charName);
  if(btn){btn.classList.add('busy');btn.textContent='⏳ 排队中...';}
  toastMsg('🎨 渲染 '+charName+' 中...',3000);
  try{
    const r = await fetch('/api/character/'+charName+'/render',{method:'POST'});
    if(!r.ok){toastMsg('渲染请求失败: HTTP '+r.status,2500);if(btn)btn.classList.remove('busy');return;}
    const d = await r.json();
    toastMsg('✅ '+charName+' 渲染完成',3000);
    if(sel && sel.startsWith('DM-1')) renderDetail();
  }catch(e){toastMsg('渲染异常: '+e.message,2500);if(btn)btn.classList.remove('busy');}
}

