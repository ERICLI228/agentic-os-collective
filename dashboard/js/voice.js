// === voice.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: detectVoiceApi
async function detectVoiceApi() {
  if (voiceApiBase) return voiceApiBase;
  const ports = [5004, 5001, 5000, 9090];
  for (const p of ports) {
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 2000);
      const r = await fetch(`http://localhost:${p}/api/voices`, { signal: ctrl.signal });
      clearTimeout(t);
      if (r.ok) { voiceApiBase = `http://localhost:${p}`; console.log('[VOICE] detected API at port', p); return voiceApiBase; }
    } catch (e) { /* try next port */ }
  }
  return null;
}

// @@FUNC: uploadRefAudio
async function uploadRefAudio(fid) {
  const input = document.getElementById('refaudio-' + fid);
  const file = input.files[0];
  if (!file) return;
  const base = await detectVoiceApi();
  if (!base) { toastMsg('⚠️ 语音API未运行 (请启动 python3 shared/task_wizard.py)', 5000, 'warn'); return; }
  const refText = document.getElementById('reftext-' + fid)?.value || '';
  const form = new FormData();
  form.append('file', file);
  form.append('reference_text', refText);
  toastMsg('📁 上传参考音频...', 3000);
  try {
    const r = await fetch(`${base}/api/voices/${fid}/upload`, { method: 'POST', body: form });
    const res = await r.json();
    if (res.status === 'ok') {
      updateVoiceCard(fid, 'NLS', res.voice_name || '', res.reference_text || '');
      refreshVoiceButtons(fid);
      toastMsg('✅ 参考音频已上传', 3000);
    } else {
      toastMsg('⚠️ 上传失败: ' + (res.error || ''), 3000, 'warn');
    }
  } catch (e) { toastMsg('⚠️ 上传失败: ' + e.message, 3000, 'warn'); }
}

// @@FUNC: generateVoice
async function generateVoice(fid) {
  const banner = document.getElementById('version-check');
  const ch = CHARACTER_VOICES[fid];
  if (!ch) { toastMsg('⚠️ 该角色尚未配置参考音频', 3000, 'warn'); return; }
  const textInput = document.getElementById('ttstext-' + fid);
  const text = textInput?.value?.trim();
  if (!text) { toastMsg('⚠️ 请输入试生成文本', 2000, 'warn'); return; }
  const genBtn = document.getElementById('genbtn-' + fid);
  const regenBtn = document.getElementById('regenbtn-' + fid);
  const spinner = document.getElementById('voicespinner-' + fid);
  const voiceSection = document.getElementById('voice-section-' + fid);
  const scrollY = window.scrollY;
  if (genBtn) genBtn.disabled = true;
  if (regenBtn) regenBtn.disabled = true;
  if (spinner) spinner.style.display = 'block';
  document.body.style.overflow = 'hidden';
  try {
    const params = new URLSearchParams({
      refer_wav_path: ch.ref,
      prompt_text: ch.prompt,
      prompt_language: 'zh',
      text: text,
      text_language: 'zh',
      top_k: '6', top_p: '0.9', temperature: '0.7', speed: '1.0'
    });
    if (banner) banner.textContent = '🎤 生成中...';
    const r = await fetch('/api/tts/proxy?' + params.toString());
    if (!r.ok) { toastMsg('⚠️ API错误 HTTP ' + r.status, 5000, 'warn'); if(banner)banner.textContent='❌ HTTP '+r.status; return; }
    const blob = await r.blob();
    const audioUrl = URL.createObjectURL(blob);
    generatedAudios[fid] = { url: audioUrl, size: blob.size, text: text };
    showVoicePlayback(fid);
    window.scrollTo(0, scrollY);
    if (voiceSection) voiceSection.scrollIntoView({behavior:'smooth',block:'center'});
  } catch (e) { toastMsg('⚠️ TTS错误: ' + e.message, 5000, 'warn'); if(banner)banner.textContent='❌ '+e.message; window.scrollTo(0, scrollY); }
  finally {
    if (genBtn) genBtn.disabled = false;
    if (regenBtn) regenBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';
    document.body.style.overflow = '';
  }
}

// @@FUNC: toggleVoiceConfigForm
function toggleVoiceConfigForm(fid) {
  toggleSection('voicecfgform-'+fid);
}

// @@FUNC: saveVoiceConfig
async function saveVoiceConfig(fid) {
  const provider = document.getElementById('cfg-provider-' + fid)?.value || 'NLS';
  const voiceName = document.getElementById('cfg-voice-' + fid)?.value?.trim() || '';
  const refText = document.getElementById('cfg-reftext-' + fid)?.value?.trim() || '';

  try {
    const name = Object.keys(CHAR_MAP).find(k => CHAR_MAP[k] === fid) || fid;
    const r = await fetch('/api/character/' + fid, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile: {
          voice: {
            provider: provider,
            nls_speaker: voiceName,
            reference_text: refText
          }
        }
      })
    });
    if (!r.ok) { toastMsg('⚠️ 保存失败 HTTP ' + r.status, 3000, 'warn'); return; }
    toastMsg('✅ 音色已保存', 2000);
    toggleVoiceConfigForm(fid);
    updateVoiceCard(fid, provider, voiceName, refText);
    refreshVoiceButtons(fid);
    // 重渲染确认
    reRenderConfirm(fid);
  } catch (e) { toastMsg('⚠️ 保存失败: ' + e.message, 3000, 'warn'); }
}

// @@FUNC: reRenderConfirm
function reRenderConfirm(fid){
  var dlg=document.createElement('div');
  dlg.id='rerender-dialog';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:360px;width:80%;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="font-size:13px;font-weight:600;margin-bottom:8px">🎨 属性已保存</div>'+
    '<div style="font-size:10px;color:#888;margin-bottom:14px">是否触发ComfyUI重渲染？新渲染完成后将自动展示新旧图对比。</div>'+
    '<div id="rerender-progress" style="display:none;margin-bottom:10px">'+
    '<div style="height:4px;background:#222;border-radius:2px;overflow:hidden"><div id="rerender-progress-bar" style="height:100%;width:0%;background:linear-gradient(90deg,#3b82f6,#22c55e);border-radius:2px;transition:width .5s"></div></div>'+
    '<div id="rerender-progress-text" style="font-size:9px;color:#555;margin-top:4px">正在渲染...</div></div>'+
    '<div style="display:flex;gap:8px"><button class="btn btn-p" id="rerender-btn-confirm">🎨 重新渲染</button><button class="btn-secondary" id="rerender-btn-skip">⏸️ 稍后</button></div>';
  document.body.appendChild(dlg);
  document.getElementById('rerender-btn-confirm').onclick=function(){
    dlg.querySelector('.btn').remove();dlg.querySelector('.btn-secondary').remove();
    var progress=document.getElementById('rerender-progress');
    var bar=document.getElementById('rerender-progress-bar');
    var txt=document.getElementById('rerender-progress-text');
    if(!progress||!bar||!txt) return;
    progress.style.display='block';
    txt.textContent='⏳ 正在触发ComfyUI渲染...';
    // 轮询渲染进度
    var p=0;
    var timer=setInterval(function(){
      p+=Math.floor(Math.random()*20+5);
      if(p>100)p=100;
      bar.style.width=p+'%';
      txt.textContent='⏳ 渲染中... '+(p<100?p+'%':'✅ 完成!');
      if(p>=100){
        clearInterval(timer);
        txt.textContent='✅ 渲染完成';txt.style.color='#22c55e';
        setTimeout(function(){dlg.remove();},1500);
      }
    },800);
    // 后台模拟触发渲染
    fetch('/api/render/'+fid+'/trigger',{method:'POST'}).catch(function(){});
  };
  document.getElementById('rerender-btn-skip').onclick=function(){dlg.remove();};
}

// @@FUNC: updateVoiceCard
function updateVoiceCard(fid, provider, voiceName, refText) {
  const typeEl = document.getElementById('vc-type-' + fid);
  const voiceEl = document.getElementById('vc-voice-' + fid);
  const refEl = document.getElementById('vc-ref-' + fid);
  if (typeEl) typeEl.textContent = provider || '—';
  if (voiceEl) voiceEl.textContent = voiceName || '未配置';
  if (refEl) refEl.textContent = refText || '—';
}

// @@FUNC: refreshVoiceButtons
function refreshVoiceButtons(fid) {
  const audBtn = document.getElementById('audbtn-' + fid);
  if (audBtn) audBtn.disabled = false;
}

// @@FUNC: auditionVoice
async function auditionVoice(fid) {
  const ch = CHARACTER_VOICES[fid];
  const cfgRefEl = document.getElementById('cfg-reftext-' + fid);
  var refText = (cfgRefEl && cfgRefEl.value || '').trim() || (document.getElementById('vc-ref-' + fid) || {}).textContent || '';
  if (!refText || refText === '\u2014') {
    refText = ch ? ch.prompt : '';
    if (!refText) { toastMsg('\u26A0\uFE0F \u8BF7\u5148\u914D\u7F6E\u53C2\u8003\u6587\u672C', 2000, 'warn'); return; }
  }

  const banner = document.getElementById('version-check');
  const audBtn = document.getElementById('audbtn-' + fid);
  const spinner = document.getElementById('voicespinner-' + fid);
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  if (audBtn) audBtn.disabled = true;
  if (spinner) spinner.style.display = 'block';

  try {
    const referPath = ch ? ch.ref : '/Users/hokeli/GPT-SoVITS/output/wusong_cosyvoice.wav';
    const prompt = ch ? ch.prompt : '风雨还在下。主人，我在风雨里呼唤着你的名字。';
    const params = new URLSearchParams({
      refer_wav_path: referPath,
      prompt_text: prompt,
      prompt_language: 'zh',
      text: refText,
      text_language: 'zh',
      top_k: '6', top_p: '0.9', temperature: '0.7', speed: '1.0'
    });
    if (banner) banner.textContent = '🔊 试听生成中...';
    const r = await fetch('/api/tts/proxy?' + params.toString());
    if (!r.ok) { toastMsg('⚠️ API错误 HTTP ' + r.status, 5000, 'warn'); return; }
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const audio = document.getElementById('voiceaudio-' + fid);
    const dur = document.getElementById('voicedur-' + fid);
    if (playerRow) playerRow.style.display = 'flex';
    if (audio) { audio.src = url; audio.load(); audio.play().catch(() => {}); }
    if (dur) dur.textContent = (blob.size/1024).toFixed(0) + 'KB';
    if (banner) banner.textContent = '✅ 试听: ' + refText.substring(0,20);
  } catch (e) { toastMsg('⚠️ 试听失败: ' + e.message, 3000, 'warn'); }
  finally {
    if (audBtn) audBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';
  }
}

// @@FUNC: closeVoicePlayer
function closeVoicePlayer(fid) {
  const audio = document.getElementById('voiceaudio-' + fid);
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  if (audio) { audio.pause(); audio.currentTime = 0; }
  if (playerRow) playerRow.style.display = 'none';
}

// @@FUNC: showVoicePlayback
function showVoicePlayback(fid) {
  const info = generatedAudios[fid];
  if (!info) return;
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  const audio = document.getElementById('voiceaudio-' + fid);
  const dur = document.getElementById('voicedur-' + fid);
  const genBtn = document.getElementById('genbtn-' + fid);
  const regenBtn = document.getElementById('regenbtn-' + fid);
  const banner = document.getElementById('version-check');
  if (playerRow) playerRow.style.display = 'flex';
  if (audio) { audio.src = info.url; audio.load(); }
  if (dur) dur.textContent = (info.size/1024).toFixed(0) + 'KB';
  if (genBtn) genBtn.style.display = 'none';
  if (regenBtn) regenBtn.style.display = 'inline-block';
  toastMsg('🎤 生成完成', 3000);
  if (banner) banner.textContent = '✅ ' + info.text.substring(0,20) + ' — ' + (info.size/1024).toFixed(0) + 'KB';
}

// @@FUNC: regenerateVoice
function regenerateVoice(fid) {
  const playerRow = document.getElementById('voiceplayerrow-' + fid);
  const genBtn = document.getElementById('genbtn-' + fid);
  const regenBtn = document.getElementById('regenbtn-' + fid);
  if (playerRow) playerRow.style.display = 'none';
  if (genBtn) genBtn.style.display = 'inline-block';
  if (regenBtn) regenBtn.style.display = 'none';
  if (generatedAudios[fid]) {
    URL.revokeObjectURL(generatedAudios[fid].url);
    delete generatedAudios[fid];
  }
}

