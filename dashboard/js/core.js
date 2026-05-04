// === core.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@STATE: Global variables
var cur='tk', sel=null, lastData=null, all=[], _dashOpLock=false, searchQ='', filterSt='all';
var CHAR_MAP={'武松':'wusong','鲁智深':'luzhishen','林冲':'linchong','宋江':'songjiang','李逵':'likui','吴用':'wuyong','杨志':'yangzhi','晁盖':'chaogai'};
var CHARACTER_VOICES={};
var CHAR_ROLES={};
var CHAR_NAMES=['武松','鲁智深','林冲','宋江','李逵','吴用','杨志','晁盖'];
var pipelineFilter='all', chartMode='status', chartInstance=null;
var dlPanelOpen=false;

// @@FUNC: showLoading / hideLoading
function showLoading(){document.getElementById('loadingBar').classList.add('on')}
function hideLoading(){setTimeout(()=>{document.getElementById('loadingBar').classList.remove('on')},500)}

// @@FUNC: select
function select(id){sel=id;render()}


// @@FUNC: fetchVersion
async function fetchVersion(){
  try{
    const r = await fetch('/api/status');
    const d = await r.json();
    if(d.version){
      document.getElementById('appTitle').textContent='Agentic OS 指挥中心 '+d.version;
    }
  }catch(e){}
}

// @@FUNC: refresh
async function refresh(){
  if (_dashOpLock) { console.log('[refresh] skipped (operation in progress)'); return; }
  // 0-5: 安全状态检查 — 用户正在编辑/模态框打开/拖拽排序时跳过轮询
  var activeEl = document.activeElement;
  if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.isContentEditable)) {
    console.log('[refresh] skipped (user is editing)'); return;
  }
  if (document.querySelector('.modal.show, .popup-overlay, [style*="display:block"].modal')) {
    console.log('[refresh] skipped (modal open)'); return;
  }
  var dragEl = document.querySelector('[data-dragging="true"], .dragging, .sortable-dragging');
  if (dragEl) { console.log('[refresh] skipped (dragging)'); return; }
  showLoading();
  try{
    const r=await fetch('/api/dashboard'); lastData=await r.json();
    all=(lastData?.milestones||[]).map(m=>({...m,pipeline:m.pipeline||(String(m.ms_id||'').startsWith('DM')?'drama':'tk')}));
    render();
    setTimeout(function(){if(!sel&&typeof renderChartPanel==='function')renderChartPanel();},300);
    document.getElementById('lastRefresh').textContent=new Date().toLocaleTimeString();
  }catch(e){document.getElementById('lastRefresh').textContent='离线'}
  hideLoading();
}

// @@FUNC: switchTab
function switchTab(t){
  cur=t; sel=null;
  document.getElementById('tabTK').className='tab'+(t=='tk'?' active':'');
  document.getElementById('tabDM').className='tab'+(t=='drama'?' active':'');
  render();
}

// @@FUNC: switchToTab
function switchToTab(msId){
  if(msId.startsWith('MS-')) switchTab('tk');
  else if(msId.startsWith('DM-')) switchTab('drama');
  sel=msId;
  render();
  setTimeout(function(){
    var el=document.querySelector('.ms-item.sel');
    if(el) el.scrollIntoView({behavior:'smooth',block:'center'});
    var d=document.getElementById('detail');
    if(d) d.scrollIntoView({behavior:'smooth',block:'start'});
  },100);
}

// @@FUNC: triggerReReviewMS0
async function triggerReReviewMS0(){
  var btn=document.getElementById('rerun-btn-MS-0');
  if(btn){btn.disabled=true;btn.textContent='⏳ 重新检查中...';}
  try{
    var r=await fetch('/api/gate/MS-0/run',{method:'POST'});
    var d=await r.json();
    showToast('✔ 门禁检查完成','success');
    setTimeout(function(){select('MS-0')},800);
  }catch(e){
    showToast('✖ 重新检查失败: '+e.message,'error');
    if(btn){btn.disabled=false;btn.textContent='🔄 重新执行门禁检查';}
  }
}

// @@FUNC: toastMsg
function toastMsg(msg, keepMs=2000, type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='toast'+(type?' '+type:'')+' on';
  setTimeout(()=>{t.classList.remove('on');},keepMs);
}

// @@FUNC: zoomImg
function zoomImg(url){
  document.getElementById('modalImg').src=url;
  document.getElementById('modal').classList.add('on');
}

// @@FUNC: toggleSection
function toggleSection(sectionId){
  const body = document.getElementById(sectionId);
  if(!body){const b=document.querySelector('#'+sectionId);if(!b)return;body=b;}
  body.classList.toggle('accordion-expanded');
  const hdr = document.querySelector('[data-toggle="'+sectionId+'"]');
  if(hdr) hdr.classList.toggle('expanded');
}

// @@FUNC: toggleSec
function toggleSec(secId){
  toggleSection(secId);
}

// @@FUNC: renderDefault
function renderDefault(detail){
  let h='';
  if(detail.sections){
    detail.sections.forEach(s=>{
      const st=s.source||'mock';
      var sTitle=s.title||'';
      // v3.7.8g: DM-1 一致性检查仪表盘 (must check before 角色设计 to avoid false match)
      if(sTitle.indexOf('一致性检查')>=0||sTitle.indexOf('一致性')>=0){
        h+='<div class="sec"><h3>'+sTitle+' <span class="src-tag src-'+st+'">['+st+']</span></h3>';
        h+='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;margin:8px 0">';
        (s.items||[]).forEach(function(it){
          var label=it.label||'';
          var val=it.value||'';
          var note=it.note||'';
          var isPass=val.indexOf('✅')>=0||val.indexOf('通过')>=0||val.indexOf('统一')>=0;
          var isWarn=val.indexOf('⚠️')>=0||val.indexOf('冲突')>=0||val.indexOf('复用')>=0;
          var icon=isPass?'\u2705':isWarn?'\u26A0\uFE0F':'\u{1F4CB}';
          var statusText=isPass?'\u901A\u8FC7':isWarn?'\u9700\u5173\u6CE8':'';
          // Strip emoji/icon prefixes for clean description
          var cleanVal=val.replace(/[\u2705\u26A0\uFE0F\u{26A0}]\s*/gu,'').trim();
          // Color conflict blocks
          var extraHTML='';
          if(label.indexOf('配色')>=0||label.indexOf('颜色')>=0){
            var colors=['#8b0000','#1a1a2e','#0a0a0a'];
            var names=['林冲','武松','李逵'];
            extraHTML='<div style="display:flex;gap:6px;align-items:center;margin-top:6px">';
            colors.forEach(function(c,i){
              extraHTML+='<div style="display:flex;align-items:center;gap:3px"><span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:'+c+';border:2px solid rgba(255,255,255,.15)"></span><span style="font-size:8px;color:#888">'+names[i]+'</span></div>';
            });
            extraHTML+='</div>';
          }
          if(label.indexOf('音色')>=0||label.indexOf('配音')>=0){
            extraHTML='<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;font-size:9px"><span style="background:rgba(59,130,246,.12);color:#60a5fa;border-radius:4px;padding:3px 8px">zhiming \u2192 \u6B66\u677E/\u9C81\u667A\u6DF1</span><span style="background:rgba(34,197,94,.12);color:#34d399;border-radius:4px;padding:3px 8px">zhilun \u2192 \u6797\u51B2/\u5B8B\u6C5F/\u5434\u7528</span></div>';
          }
          h+='<div class="check-item-card'+(isWarn?' warning':'')+'" style="margin-bottom:0;border-left:3px solid '+(isWarn?'#f59e0b':'#22c55e')+'">';
          h+='<div class="check-item-header"><span class="check-item-icon">'+icon+'</span><span class="check-item-name">'+label+'</span><span class="check-item-status '+(isPass?'pass':'warn')+'">'+(isPass?'\u2714 \u901A\u8FC7':isWarn?'\u26A0 \u9700\u5173\u6CE8':'')+'</span></div>';
          h+='<div class="check-item-body">';
          if(cleanVal)h+='<div style="font-size:10px;color:#888;margin-bottom:4px">'+cleanVal+'</div>';
          if(extraHTML)h+=extraHTML;
          if(note)h+='<div style="font-size:9px;color:#555;margin-top:2px">\u{1F4AC} '+note+'</div>';
          h+='</div></div>';
        });
        h+='</div></div>';
        return;
      }
      // v3.7.8g: 分镜质量评估 — 可视化仪表盘 (镜头语言/光影设计/情绪覆盖)
      if(sTitle.indexOf('分镜质量')>=0||sTitle.indexOf('质量评估')>=0){
        var emoColors={'愤怒':'#ef4444','力量':'#22c55e','悲壮':'#f59e0b','恐惧':'#dc2626','复仇':'#f97316','胜利':'#06b6d4','紧张':'#eab308','豪迈':'#3b82f6','绝望':'#7c3aed'};
        var camIcons={'中景':'🎯','特写':'🔍','全景':'🏞️ ','仰角':'📐','俯角':'🪂','跟随':'🚶','广角':'🌐','双人':'👥'};
        var lightIcons={'月光':'🌙','火光':'🔥','烛光':'🕯️','晨曦':'🌅','逆光':'☀️','伦勃朗':'🎨','烈日':'💥','moody':'🌫️','剪影':'🧍'};
        h+='<div class="sec"><h3>'+sTitle+' <span class="src-tag src-'+st+'">['+st+']</span></h3>';
        h+='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;margin:8px 0">';
        (s.items||[]).forEach(function(it){
          var label=it.label||'';
          var val=it.value||'';
          var note=it.note||'';
          var isWarn=it.status==='warn';
          var accent=isWarn?'#f59e0b':'#22c55e';
          var icon=isWarn?'\u26A0\uFE0F':'\u2705';
          // Parse name:count pairs from value
          var parts=val.split('\u00B7').map(function(p){return p.trim();}).filter(function(p){return p;});
          var bars='';
          var totalCount=0;
          var entries=[];
          parts.forEach(function(p){
            var m=p.match(/^(\D+?)(\d+)$/);
            if(m){entries.push({name:m[1].trim(),count:parseInt(m[2])});totalCount+=parseInt(m[2]);}
          });
          var maxCount=entries.reduce(function(m,e){return Math.max(m,e.count);},1);
          entries.forEach(function(e){
            var pct=Math.round(e.count/maxCount*100);
            var bg=emoColors[e.name]||(isWarn?'rgba(245,158,11,.2)':'rgba(59,130,246,.2)');
            var barColor=emoColors[e.name]||(isWarn?'#fbbf24':'#60a5fa');
            var ico='';
            if(label.indexOf('镜头')>=0)ico=camIcons[e.name]||'';
            else if(label.indexOf('光影')>=0)ico=lightIcons[e.name]||'';
            else if(label.indexOf('情绪')>=0)ico=emoColors[e.name]?'\u{1F3A8}':'\u{1F4CA}';
            bars+='<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px">';
            if(ico)bars+='<span style="font-size:11px;width:18px;text-align:center">'+ico+'</span>';
            bars+='<span style="font-size:9px;color:#aaa;min-width:40px">'+e.name+'</span>';
            bars+='<span style="font-size:8px;color:#666;min-width:20px;text-align:right">'+e.count+'</span>';
            bars+='<div style="flex:1;height:8px;background:rgba(255,255,255,.04);border-radius:4px;overflow:hidden"><div style="height:100%;width:'+pct+'%;background:'+barColor+';border-radius:4px;transition:width .3s"></div></div>';
            bars+='</div>';
          });
          var warnStyle=isWarn?'border-left:3px solid #f59e0b;':'border-left:3px solid #22c55e;';
          h+='<div class="check-item-card'+(isWarn?' warning':'')+'" style="margin-bottom:0;'+warnStyle+'">';
          h+='<div class="check-item-header"><span class="check-item-icon">'+icon+'</span><span class="check-item-name">'+label+'</span><span class="check-item-status '+(isWarn?'warn':'pass')+'">'+(isWarn?'\u26A0 \u9700\u5173\u6CE8':'\u2714 \u5408\u683C')+'</span></div>';
          h+='<div class="check-item-body">';
          if(bars)h+='<div style="margin-bottom:6px">'+bars+'</div>';
          if(note)h+='<div style="font-size:9px;color:'+(isWarn?'#fbbf24':'#888')+';margin-top:2px"><span style="margin-right:4px">\u{1F4AC}</span>'+note+'</div>';
          h+='</div></div>';
        });
        h+='</div></div>';
        return;
      }
      // v3.7.8g: DM-1 角色卡片网格 — only for specific section titles
      var isCharSection=sTitle.indexOf('视觉设计')>=0||(sTitle.indexOf('角色')>=0&&sTitle.indexOf('一致性')<0);
      if((s.items||[]).length>0&&isCharSection){
        // Detect if items are character names (have traits data in value) or generic entries
        var hasCharData=(s.items||[]).some(function(it){var v=it.value||'';return v.indexOf('\u00B7')>=0||v.indexOf('cm')>=0;});
        if(hasCharData){
        h+='<div class="sec"><h3>'+sTitle+' <span class="src-tag src-'+st+'">['+st+']</span></h3>';
        h+='<div class="dm-char-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:8px 0">';
        (s.items||[]).forEach(function(it){
          var name=it.label||'';
          var val=it.value||'';
          var fid=(CHAR_MAP[name]||name||'').toLowerCase();
          // Parse traits from value
          var parts=val.split('\u00B7');
          var traitItems=parts.map(function(p){return p.trim();}).filter(function(p){return p.length>0;});
          var voiceInfo=CHARACTER_VOICES[fid]||{};
          var colors=['#4a3728','#1a1a2e','#8b0000','#0a0a0a','#2d5016','#1e3a5f','#5c4033','#3d2b1f'];
          var colorIdx=Math.abs((name.charCodeAt(0)||0))%colors.length;
          h+='<div class="dm-char-card" style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:10px;overflow:hidden;transition:all .2s">';
          // Portrait area
          h+='<div style="position:relative;width:100%;height:180px;background:#0f1018;overflow:hidden">';
          var q=String.fromCharCode(39);
          h+='<img src="/api/render/'+fid+'/portrait_0.png" loading="lazy" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='+q+'none'+q+';this.nextElementSibling.style.display='+q+'flex'+q+'" />';
          h+='<div class="char-fallback" style="display:none;position:absolute;top:0;left:0;right:0;bottom:0;flex-direction:column;align-items:center;justify-content:center;background:#0f1018;color:#555;font-size:40px">\u{1F3AD}</div>';
          // Name overlay
          h+='<div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.85));padding:20px 10px 8px">';
          h+='<div style="font-size:14px;font-weight:700;color:#fff;letter-spacing:1px">'+name+'</div>';
          h+='<div style="font-size:9px;color:#aaa;margin-top:1px">\u2728 '+(CHAR_ROLES[name]||'')+'</div>';
          h+='</div></div>';
          // Trait tags
          h+='<div style="padding:8px 10px 4px">';
          h+='<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px">';
          traitItems.forEach(function(t){
            var isNum=/\d/.test(t);
            h+='<span style="font-size:8px;padding:2px 7px;border-radius:10px;background:rgba(59,130,246,.1);color:#60a5fa">'+t.substring(0,15)+'</span>';
          });
          h+='</div>';
          // Voice info + color dot — clickable to navigate to DM-3 Voice Design
          h+='<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:9px;color:#888">';
          h+='<span style="cursor:pointer;text-decoration:underline;text-underline-offset:2px;color:'+(voiceInfo.ref?'#4ade80':'#888')+'" onclick="switchToTab(\'drama\');select(\'DM-3\');setTimeout(function(){var vr=document.getElementById(\'dm3-voice-'+fid+'\');if(vr){vr.scrollIntoView({behavior:\'smooth\',block:\'center\'});vr.style.background=\'rgba(59,130,246,.08)\';setTimeout(function(){vr.style.background=\'\'},2000);}},800)" title="点击跳转到 DM-3 配音设计">\u{1F3A4} '+(voiceInfo.ref?'\u5DF2\u914D\u7F6E':'\u672A\u914D\u7F6E')+'</span>';
          h+='<span title="色标" style="display:inline-block;width:14px;height:14px;border-radius:50%;background:'+colors[colorIdx]+';border:2px solid rgba(255,255,255,.12)"></span>';
          h+='</div>';
          // Actions
          h+='<div style="display:flex;gap:4px;padding-bottom:8px">';
          h+='<button class="mini-btn" onclick="toggleCharBibleEdit(\''+fid+'\')" style="font-size:9px">\u{1F4DD} \u7F16\u8F91</button>';
          h+='<button class="mini-btn" onclick="auditionVoice(\''+fid+'\',this)" style="font-size:9px">\u{1F50A} \u8BD5\u542C</button>';
          h+='</div></div></div>';
        });
        h+='</div>';
        h+='<div style="margin-top:8px;text-align:center"><button class="dm1-add-btn" onclick="showAddCharForm()" style="background:#22c55e;color:#fff;border:none;padding:6px 16px;border-radius:6px;font-size:11px;cursor:pointer;font-weight:600">+ 新增角色</button></div>';
        h+='</div></div>';
        return;
        } // hasCharData
      }
      const secId = 'sec-'+s.title.replace(/[^a-zA-Z0-9一-鿿]/g,'');
      // P0-1: Summary line always visible, body collapsible
      let summary = '';
      if(s.summary) summary = s.summary;
      else if(s.items){
        const ok = s.items.filter(i=>i.status==='ok').length;
        const total = s.items.length;
        summary = `${ok}/${total} 通过`;
      }
      h+=`<div class="sec" id="${secId}">`;
      h+=`<div class="sec-hdr" onclick="toggleSec('${secId}')"><h3><span class="sec-toggle-icon">&#9654;</span>${s.title} <span class="src-tag src-${st}">[${st}]</span> <span style="font-size:9px;color:#555;font-weight:400">${summary}</span></h3></div>`;
      h+=`<div class="sec-body">`;
      if(s.items){
        // P4-FIX: Pre-filter bad items before rendering (strip undefined/null/empty)
        const valid = (s.items||[]).filter(it => {
          if (!it) return false;
          if (it.key === 'rv_decision') return false;
          const l = it.label, k = it.key, v = it.value;
          const labelOk = (l != null && String(l).trim()) || (k != null && String(k).trim());
          const valOk = v != null && String(v).trim() || it.before || it.after || it.note;
          if (!labelOk && !valOk) { console.warn('[P4-STRIP]', JSON.stringify(it)); return false; }
          return labelOk && valOk;
        });
        valid.forEach(it=>{
        const ic2={'ok':'<span class="ic ok">&#10003;</span>','ng':'<span class="ic ng">&#10007;</span>','warn':'<span class="ic wn">&#9888;</span>','critical':'<span class="ic cr">&#128721;</span>','DIAG':'v3.6.19'};
        const displayLabel = it.label || it.key || '';
        const displayValue = it.value || '';
        const statusIcon = ic2[it.status] || ('[DIAG:'+it.status+']');
        h+=`<div class="ent-row">${statusIcon}<span class="ent-lbl">${displayLabel}</span><div class="ent-val"><span>${displayValue}</span>`;
        if(it.before)h+=`<div class="before">&larr; ${it.before}</div>`;
        if(it.after)h+=`<div class="after">&rarr; ${it.after}</div>`;
        if(it.note)h+=`<div class="note">&#9432; ${it.note}</div>`;
        const imgs = extractImages(it.note||'');
        if(imgs.length > 0){
          h+=`<div class="img-gallery">`;
          imgs.forEach(img=>{
            h+=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${img.url}')">
              <img src="${img.url}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=img-placeholder-text>图片未找到</div>'" />
              <span class="img-label">${img.type}</span>
            </div>`;
          });
          h+=`</div>`;
        }
        h+=`</div></div>`;
      });
      }
      h+=`</div></div>`;
    });
  }
  return h;
}

// @@FUNC: renderDetail
async function renderDetail(){
  const banner = document.getElementById('version-check');
  if (banner) banner.textContent = '⏳ 加载详情... ' + sel;
  document.getElementById('empty').style.display='none';
  document.getElementById('detail').style.display='block';
  const ms=all.find(m=>m.ms_id===sel);
  if(!ms){if(banner)banner.textContent='⚠️ 未找到: '+sel;return;}
  if(banner) banner.textContent = '⏳ 加载 ' + ms.ms_id + ' 详情...';

  const done=ms.status=='completed'||ms.status=='approved';
  const sl={completed:'已完成',waiting_approval:'等待决策',pending:'待执行',running:'执行中',approved:'已批准',rejected:'已驳回'};
  const sc=done?'#22c55e':ms.status=='waiting_approval'?'#f59e0b':'#666';
  const tag=ms.data_source!=='real'?`<span class="src-tag src-${ms.data_source}">${ms.data_source=='mock'?'[模拟]':'[推算]'}</span>`:'';

  let h=`<h2>${ms.ms_id} ${ms.name} ${tag}</h2>
    <div class="meta"><span style="color:${sc}">&bullet; ${sl[ms.status]||ms.status}</span><span>${ms.note||''}</span>`;
  if(ms.task_id)h+=`<span style="color:#556">任务: ${ms.task_id}</span>`;
  h+=`</div>`;

  let detail=null;
  try{
    const r=await fetch('/api/detail/'+ms.ms_id);
    detail=await r.json();
    const sectionCount = (detail.sections||[]).length;
    const itemCount = (detail.sections||[]).reduce((sum,s)=>sum+(s.items||[]).length,0);
    if(banner) banner.textContent = '✅ ' + ms.ms_id + ': ' + sectionCount + ' sections, ' + itemCount + ' items';
    // v3.7.9: 里程碑摘要卡（DM-1专用渲染 + 非DM/非MS-2.3自动显示）
    if(detail.summary && ms.ms_id!=='MS-2.3' && (!ms.ms_id.startsWith('DM-') || ms.ms_id==='DM-1')){
      const s=detail.summary;
      const scolor=s.status==='blocked'?'#ef4444':s.status==='warning'?'#f59e0b':'#22c55e';
      const sicon=s.status==='blocked'?'&#10060;':s.status==='warning'?'&#9888;':'&#9989;';
      h+='<div class="milestone-summary-card" style="display:flex;align-items:flex-start;gap:12px;padding:14px 16px;margin-bottom:10px;border-radius:8px;border-left:4px solid '+scolor+';background:rgba('+(s.status==='blocked'?'239,68,68':s.status==='warning'?'245,158,11':'34,197,94')+',.08)">';
      h+='<div style="font-size:22px;flex-shrink:0;padding-top:2px">'+sicon+'</div>';
      h+='<div style="flex:1;min-width:0"><div style="font-weight:600;font-size:13px;color:#e4e6eb">'+s.headline+'</div>';
      h+='<div style="font-size:11px;color:#888;margin-top:2px">'+s.core_metric+'</div>';
      // DM-1: show consistency warnings inline
      if(ms.ms_id==='DM-1'){
        var csSection = (detail.sections||[]).find(function(x){return x.title&&x.title.indexOf('一致性')>=0});
        if(csSection){
          (csSection.items||[]).forEach(function(it){
            if(it.status==='warn') h+='<div style="font-size:10px;color:#fbbf24;margin:3px 0;padding-left:8px;border-left:2px solid #f59e0b">⚠️ '+((it.value||'').replace(/^⚠️\s*/,''))+'</div>';
          });
        }
      }
      h+='</div>';
      h+='<div style="display:flex;gap:6px;flex-shrink:0">';
      h+='<button class="mini-btn" onclick="toggleSection(\''+ms.ms_id+'-detail\')">查看详情</button>';
      h+='<button class="mini-btn" style="color:#60a5fa" onclick="triggerReReview(\''+ms.ms_id+'\')">重新检查</button>';
      h+='</div></div>';
      // 将 renderDefault 输出包裹在 accordion-content 中
      var rd=renderDefault(detail);
      h+='<div class="accordion-content accordion-expanded" id="'+ms.ms_id+'-detail">'+rd+'</div>';
    // v3.7.8: DM-0 技术检查已在 renderDM0 内部折叠处理
    } else if(ms.ms_id.startsWith('DM-')){
      // All DM panels handled by specialized renderers in SMART ROUTING
    } else if(ms.ms_id!=='MS-2.3'){
      h+=renderDefault(detail);
    }
  }catch(e){h+=`<div class="sec"><h3>详情</h3><div style="color:#555;font-size:11px;">加载失败: ${e.message}</div></div>`;if(banner)banner.textContent='❌ 加载失败: '+e.message;}

  // Decision actions
  if(ms.decision_point&&ms.status=='waiting_approval'){
    h+=`<div class="sec"><h3>你的决策</h3>`;
    [{a:'approved',l:'批准发布',c:'btn-p'},{a:'modify',l:'修改',c:'btn-w'},{a:'rejected',l:'驳回',c:'btn-d'}].forEach(o=>{
      h+=`<button class="btn ${o.c}" onclick="decide('${ms.ms_id}','${o.a}')">${o.l}</button> `;
    });
    h+=`</div>`;
  }

  document.getElementById('detail').innerHTML=h;

  // SMART ROUTING
  if(ms.ms_id==='DM-0'){
    await renderDM0(detail,ms);
  }else if(ms.ms_id==='DM-1'){
    await renderDM1(detail,ms);
  }else if(ms.ms_id==='DM-2'){
    await renderDM2(detail,ms);
  }else if(ms.ms_id==='DM-3'){
    await renderDM3(detail,ms);
  }else if(ms.ms_id==='DM-4'){
    await renderDM4(detail,ms);
  }else if(ms.ms_id==='DM-5'){
    await renderDM5(detail,ms);
  }else if(ms.ms_id==='DM-8'){
    await renderDM8(detail,ms);
  }else if(ms.ms_id==='DM-9'){
    await renderDM9(detail,ms);
  }else if(ms.ms_id==='DM-10'){
    await renderDM10(detail,ms);
  }else if(ms.ms_id==='DM-6'){
    await renderDM6(ms.ms_id,detail,ms);
  }else if(ms.ms_id==='DM-7'){
    await renderDM6(ms.ms_id,detail,ms);
  }else if(ms.ms_id==='MS-0'){
    await renderMS0Gate(detail,ms);
  }else if(ms.ms_id==='MS-1'){
    await renderMS1(detail,ms);
  }else if(ms.ms_id==='MS-1.5'){
    await renderMS15(detail,ms);
  }else if(ms.ms_id==='MS-2'){
    await renderMS2(detail,ms);
  }else if(ms.ms_id==='MS-2.1'){
    await renderMS21(detail,ms);
  }else if(ms.ms_id==='MS-2.2'){
    await renderMS22(detail,ms);
  }else if(ms.ms_id==='MS-2.3'){
    await renderTKImageWorkbench(detail,ms);
  }else if(ms.ms_id==='MS-2.4'){
    await renderMS24(detail,ms);
  }else if(ms.ms_id==='MS-2.5'){
    await renderMS25(detail,ms);
  }else if(ms.ms_id==='MS-2.6'){
    await renderMS26(detail,ms);
  }else if(ms.ms_id==='MS-3'){
    await renderMS3(detail,ms);
  }else if(ms.ms_id==='MS-4'){
    await renderMS4(detail,ms);
  }else if(ms.ms_id==='MS-5'){
    await renderMS5(detail,ms);
  }else if(ms.ms_id && !ms.ms_id.startsWith('DM-') && !ms.ms_id.startsWith('daily')){
    await renderTKDetail(detail,ms);
  }
}

// @@FUNC: renderMilestoneTimeline
function renderMilestoneTimeline(msId){
  var ms = all;
  if(!ms || ms.length===0) return '';
  var h='<div class="milestone-timeline">';
  for(var i=0;i<ms.length;i++){
    var m=ms[i];
    var st=m.status||'pending';
    var cls='pending';
    if(st==='completed'||st==='approved') cls='done';
    else if(st==='running'||st==='waiting_approval') cls='active';
    else if(st==='rejected') cls='fail';
    var isCurrent = m.ms_id===msId;
    h+='<div class="tl-node" onclick="switchToTab(\''+m.ms_id+'\')" style="cursor:pointer">';
    h+='<div class="tl-line '+cls+'"></div>';
    h+='<div class="tl-dot '+cls+'"></div>';
    h+='<div class="tl-label'+(isCurrent?' current':'')+'">'+(m.name||m.ms_id||'')+'</div>';
    h+='</div>';
  }
  h+='</div>';
  return h;
}

// @@FUNC: renderMilestoneSummary
function renderMilestoneSummary(detail, ms){
  var summary=detail.summary||{};
  var status=ms.status||'pending';
  var cfg={'completed':{icon:'✅',cls:'ok'},'approved':{icon:'✅',cls:'ok'},'running':{icon:'⏳',cls:'warn'},'pending':{icon:'⏸️',cls:''},'waiting_approval':{icon:'⏳',cls:'warn'},'rejected':{icon:'❌',cls:'ng'}};
  var sc=cfg[status]||{icon:'\u23f8\ufe0f',cls:''};
  var hl=summary.headline||(ms.name||ms.ms_id)+' \u8be6\u60c5';
  var m=summary.core_metric||(summary.section_count ? summary.section_count+' \u6a21\u5757 \u00b7 '+summary.item_count+' \u6570\u636e\u9879' : '');
  return '<div class="milestone-summary-card '+sc.cls+'">'+
    '<div class="msc-left">'+sc.icon+'</div>'+
    '<div class="msc-center"><div class="msc-headline">'+hl+'</div><div class="msc-metrics">'+m+'</div></div>'+
    '<div class="msc-right">'+
    '<button class="btn btn-p" onclick="toggleSection(\u0027ms-detail-'+ms.ms_id+'\u0027)">\u67e5\u770b\u8be6\u60c5</button>'+
    '<button class="btn-secondary" style="margin-left:4px;font-size:10px" onclick="showMileDownloadMenu(&quot;dl-mile-'+ms.ms_id+'&quot;)">\u2601\ufe0f</button>'+
    '<div id="dl-mile-'+ms.ms_id+'" class="accordion-content mile-dl-menu">'+
    '<a href="#" onclick="window.open(\u0027/api/download?name='+ms.ms_id+'_report.txt\u0027)">\u{1f4c4} TXT</a>'+
    '<a href="#" onclick="window.open(\u0027/api/download?name='+ms.ms_id+'_data.json\u0027)">\u{1f4ca} JSON</a>'+
    '</div></div></div>';
}

// @@FUNC: showMileDownloadMenu
function showMileDownloadMenu(msId){
  var el=document.getElementById('dl-mile-'+msId);
  if(!el) return;
  el.classList.toggle('accordion-expanded');
}

// @@FUNC: showToast
function showToast(msg,type){
  var container=document.getElementById('toast-container');
  if(!container)return;
  var t=document.createElement('div');
  t.className='toast-item toast-'+(type||'info');
  t.textContent=msg;
  container.appendChild(t);
  setTimeout(function(){
    t.classList.add('fade-out');
    setTimeout(function(){if(t.parentNode)t.parentNode.removeChild(t);},300);
  },3000);
}

// @@FUNC: toggleCompare
function toggleCompare(imgs) {
  if (!imgs || imgs.length < 2) { toastMsg('需要至少 2 张图片才能对比', 2000, 'warn'); return; }
  compareMode = !compareMode;
  const gal = document.querySelector('.img-gallery');
  if (!gal) return;
  if (compareMode) {
    let h = '<div class="compare-view">';
    const labels = ['原始', '处理后', '去背景', '最终'];
    imgs.forEach((img, i) => {
      h += `<div class="compare-col"><div class="comp-label">${labels[i] || '图'+(i+1)}</div><img src="${img.url||img}" onclick="zoomImg('${img.url||img}')"/></div>`;
    });
    h += '</div>';
    gal.outerHTML = h;
    document.getElementById('kbdToggle').textContent = '🔲 退出对比';
  } else {
    renderDetail();
    document.getElementById('kbdToggle').textContent = '⌨ 快捷键';
  }
}

// @@FUNC: toggleKbdHint
function toggleKbdHint() {
  const el = document.getElementById('kbdHint');
  el.classList.toggle('show');
}

// @@FUNC: closeModal
function closeModal() {
  document.getElementById('modal').classList.remove('on');
}

// @@FUNC: highlightText
function highlightText(text, query) {
  if (!query || !text) return text;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${escaped})`, 'gi');
  return text.replace(regex, '<mark class="search-hl">$1</mark>');
}

// @@FUNC: toggleDlPanel
function toggleDlPanel() {
  dlPanelOpen = !dlPanelOpen;
  document.getElementById('dlPanel').classList.toggle('show', dlPanelOpen);
}

// @@FUNC: downloadAs
async function downloadAs(fmt) {
  toggleDlPanel();
  toastMsg('📥 正在生成 ' + fmt.toUpperCase() + '...', 2000);
  try {
    if (!lastData) { toastMsg('⚠️ 无数据可导出，请先刷新', 2000, 'warn'); return; }
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const fn = `agentic-os-${ts}.${fmt}`;

    if (fmt === 'json') {
      const blob = new Blob([JSON.stringify(lastData, null, 2)], { type: 'application/json' });
      triggerDownload(blob, fn);
    } else if (fmt === 'csv') {
      let csv = 'Milestone,Name,Status,DataSource,TaskID,Decision\n';
      (lastData.milestones || []).forEach(m => {
        csv += `"${m.ms_id}","${m.name || ''}","${m.status}","${m.data_source || ''}","${m.task_id || ''}","${m.decision || ''}"\n`;
      });
      triggerDownload(new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }), fn);
    } else if (fmt === 'csv-decisions') {
      let csv = 'Milestone,Action,Reason,Timestamp\n';
      (lastData.milestones || []).filter(m => m.decision).forEach(m => {
        csv += `"${m.ms_id}","${m.decision}","${m.decision_reason || ''}","${m.updated_at || ''}"\n`;
      });
      triggerDownload(new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }), fn);
    } else if (fmt === 'md') {
      let md = `# Agentic OS 状态报告\n\n生成时间: ${new Date().toLocaleString()}\n\n## 里程碑概览\n\n| Milestone | 名称 | 状态 | 数据源 |\n|---|---|---|---|\n`;
      (lastData.milestones || []).forEach(m => {
        md += `| ${m.ms_id} | ${m.name || '-'} | ${m.status} | ${m.data_source || '-'} |\n`;
      });
      md += `\n## 统计\n- 总计: ${(lastData.milestones || []).length}\n- 已完成: ${(lastData.milestones || []).filter(m => m.status === 'completed' || m.status === 'approved').length}\n- 待决策: ${(lastData.milestones || []).filter(m => m.status === 'waiting_approval').length}\n`;
      triggerDownload(new Blob([md], { type: 'text/markdown' }), fn);
    } else if (fmt === 'html') {
      const html = document.documentElement.outerHTML;
      triggerDownload(new Blob([html], { type: 'text/html' }), fn);
    } else {
      toastMsg('⚠️ 不支持格式: ' + fmt, 2000, 'warn'); return;
    }
    toastMsg('✅ ' + fmt.toUpperCase() + ' 导出成功', 2500);
  } catch (e) {
    toastMsg('❌ 导出失败: ' + e.message, 3000, 'error');
  }
}

// @@FUNC: triggerDownload
function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// @@FUNC: toggleAllSections
function toggleAllSections() {
  const allBodies = document.querySelectorAll('.sec-body.collapsible');
  const anyCollapsed = Array.from(allBodies).some(b => !b.classList.contains('expanded'));
  allBodies.forEach(b => {
    if (anyCollapsed) b.classList.add('expanded');
    else b.classList.remove('expanded');
  });
  document.querySelectorAll('.sec-hdr.collapsible').forEach(h => {
    if (anyCollapsed) h.classList.add('expanded');
    else h.classList.remove('expanded');
  });
}

// @@FUNC: makeSectionCollapsible
function makeSectionCollapsible(secId, title, contentHTML, defaultExpanded = false) {
  const expanded = expandedSections.has(secId) || defaultExpanded;
  return `<div class="sec" style="padding:8px 12px;margin-bottom:6px">
    <div class="sec-hdr collapsable ${expanded ? 'expanded' : ''}" id="sechdr-${secId}" onclick="toggleSection('${secId}')" style="cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px;font-size:11px;color:#888;padding:4px 0">
      <span class="sec-toggle-icon" style="transition:transform .2s;display:inline-block;transform:rotate(${expanded ? '90' : '0'}deg)">▶</span>
      ${title}
      <span style="margin-left:auto;font-size:8px;color:#555">${expanded ? '点击收起' : '点击展开'}</span>
    </div>
    <div class="sec-body collapsable ${expanded ? 'expanded' : ''}" id="secbody-${secId}" style="max-height:0;overflow:hidden;transition:max-height .3s ease-out;${expanded ? 'max-height:5000px' : ''}">
      ${contentHTML}
    </div>
  </div>`;
}

// @@FUNC: triggerReReview
async function triggerReReview(msId) {
  const btn = document.getElementById('rerun-btn-' + msId);
  if (btn) { btn.classList.add('busy'); btn.textContent = '⏳ 重审中...'; }
  // 创建/复用日志面板
  let logPanel = document.getElementById('review-log-panel');
  if (!logPanel) {
    logPanel = document.createElement('div');
    logPanel.id = 'review-log-panel';
    logPanel.className = 'review-log-panel';
    const detailEl = document.getElementById('detail');
    if (detailEl) detailEl.insertAdjacentElement('beforeend', logPanel);
  }
  logPanel.style.display = 'block';
  logPanel.innerHTML = '<div style="font-size:10px;color:#93c5fd;margin-bottom:6px">📋 审核日志</div>';
  function addLog(msg) {
    logPanel.insertAdjacentHTML('beforeend', '<div class="review-log-line">' + msg + '</div>');
    logPanel.scrollTop = logPanel.scrollHeight;
  }
  addLog('⏳ 准备审核 ' + msId + '...');
  try {
    const r1 = await fetch('/api/decision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_id: msId, action: 'modify', reason: '用户触发重新审核' })
    });
    if (!r1.ok) { addLog('❌ 重置失败: HTTP ' + r1.status); toastMsg('重置失败', 2500, 'error'); return; }
    addLog('✅ 状态已重置');

    const r2 = await fetch('/api/review/' + msId, { method: 'POST' });
    if (!r2.ok) { addLog('❌ 审核触发失败: HTTP ' + r2.status); toastMsg('审核触发失败', 2500, 'error'); return; }
    const result = await r2.json();

    // 模拟逐条显示日志
    var logs = result.logs || [];
    for (var i = 0; i < logs.length; i++) {
      addLog(logs[i]);
      await new Promise(function(r){setTimeout(r, 400);});
    }

    addLog('<strong style="color:#22c55e">✅ 审核完成: 评分 ' + (result.overall_score || 'N/A') + '/10</strong>');
    toastMsg('✅ 审核完成: 评分 ' + (result.overall_score || 'N/A') + '/10', 4000, 'success');
    setTimeout(refresh, 2000);
  } catch (e) {
    addLog('❌ 错误: ' + e.message);
    toastMsg('❌ 重审失败: ' + e.message, 3000, 'error');
  }
  if (btn) { btn.classList.remove('busy'); btn.textContent = '🔄 重新审核'; }
}

// @@FUNC: approveHuman
async function approveHuman(){
  toastMsg('🔄 正在提交人工审批...', 2000);
  try{
    var r=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:'MS-4',action:'approved',reason:'人工审批通过'})});
    if(!r.ok){toastMsg('审批提交失败: HTTP '+r.status,2500,'error');return;}
    toastMsg('✅ 人工审批已通过',3000,'success');
    setTimeout(function(){select('MS-4')},1000);
  }catch(e){toastMsg('❌ 审批失败: '+e.message,3000,'error');}
}

// @@FUNC: rejectHuman
async function rejectHuman(){
  toastMsg('🔄 正在提交驳回...', 2000);
  try{
    var r=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:'MS-4',action:'rejected',reason:'人工审批驳回'})});
    if(!r.ok){toastMsg('驳回提交失败: HTTP '+r.status,2500,'error');return;}
    toastMsg('✅ 已驳回发布',3000,'warn');
    setTimeout(function(){select('MS-4')},1000);
  }catch(e){toastMsg('❌ 驳回失败: '+e.message,3000,'error');}
}

// @@FUNC: finalApprove
async function finalApprove(){
  toastMsg('🔄 正在执行批准发布...', 2000);
  try{
    var r=await fetch('/api/publish',{method:'POST'});
    if(!r.ok){toastMsg('发布失败: HTTP '+r.status,2500,'error');return;}
    var d=await r.json();
    toastMsg('✅ 发布成功',4000,'success');
    setTimeout(function(){select('MS-5')},1500);
  }catch(e){toastMsg('❌ 发布失败: '+e.message,3000,'error');}
}

// @@FUNC: finalReject
async function finalReject(){
  if(!confirm('确认驳回发布申请？此操作将重置 MS-4 状态。')) return;
  toastMsg('🔄 正在驳回发布...', 2000);
  try{
    var r=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task_id:'MS-4',action:'rejected',reason:'最终驳回发布'})});
    if(!r.ok){toastMsg('驳回失败: HTTP '+r.status,2500,'error');return;}
    toastMsg('✅ 已驳回，MS-4 已重置',3000,'warn');
    setTimeout(function(){select('MS-4')},1000);
  }catch(e){toastMsg('❌ 驳回失败: '+e.message,3000,'error');}
}

// @@FUNC: showCompareView
function showCompareView(galleryEl) {
  if (!galleryEl) return;
  const imgs = galleryEl.querySelectorAll('.img-card img');
  if (imgs.length < 2) { toastMsg('需要至少 2 张图片才能对比', 2000, 'warn'); return; }

  compareMode = true;
  const labels = ['原始', '处理后', '去背景', '最终', '镜1', '镜2', '镜3'];
  let h = '<div class="compare-view" style="display:flex;gap:8px;overflow-x:auto;padding:8px 0">';
  Array.from(imgs).forEach((img, i) => {
    h += `<div class="compare-col" style="flex:0 0 auto;text-align:center">
      <div class="comp-label" style="font-size:9px;color:#888;margin-bottom:4px">${labels[i] || '图'+(i+1)}</div>
      <img src="${img.src}" style="max-height:300px;border-radius:4px;cursor:pointer" onclick="zoomImg('${img.src}')" />
    </div>`;
  });
  h += '</div><div style="text-align:center;margin-top:8px"><button class="mini-btn" onclick="exitCompare(this)">✕ 退出对比</button></div>';
  galleryEl.outerHTML = h;
}

// @@FUNC: exitCompare
function exitCompare(btn) {
  renderDetail();
  compareMode = false;
}

// @@FUNC: showOpProgress
function showOpProgress(containerId, msg, percent) {
  let bar = document.getElementById('op-prog-' + containerId);
  if (!bar) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.insertAdjacentHTML('beforeend',
      `<div id="op-prog-${containerId}" style="margin-top:8px">
        <div style="font-size:9px;color:#888;margin-bottom:2px" id="op-prog-msg-${containerId}">${msg}</div>
        <div style="height:4px;background:#222;border-radius:2px;overflow:hidden">
          <div id="op-prog-fill-${containerId}" style="height:100%;background:#3b82f6;width:${percent}%;transition:width .3s;border-radius:2px"></div>
        </div>
      </div>`);
  } else {
    const msgEl = document.getElementById('op-prog-msg-' + containerId);
    const fillEl = document.getElementById('op-prog-fill-' + containerId);
    if (msgEl) msgEl.textContent = msg;
    if (fillEl) fillEl.style.width = percent + '%';
  }
}

// @@FUNC: hideOpProgress
function hideOpProgress(containerId) {
  const el = document.getElementById('op-prog-' + containerId);
  if (el) el.remove();
}

// @@FUNC: trackFailure
function trackFailure(key) {
  failureCounts[key] = (failureCounts[key] || 0) + 1;
  lastFailureKey = key;
  if (failureCounts[key] >= 3) {
    showSelfHealTip(key);
  }
}

// @@FUNC: trackSuccess
function trackSuccess(key) {
  failureCounts[key] = 0;
  hideSelfHealTip();
}

// @@FUNC: showSelfHealTip
function showSelfHealTip(key) {
  const rightEl = document.getElementById('detail');
  if (!rightEl || document.getElementById('selfHealTip')) return;

  const tips = {
    'render': '渲染连续失败：\n1. 检查 ComfyUI 是否在 :8188 运行\n2. 查看 ComfyUI 控制台错误日志\n3. 尝试重启 comfyui_renderer.py',
    'tts': 'TTS 连续失败：\n1. 检查 GPT-SoVITS 是否在 :9880 运行\n2. 确认 .env 中 NLS 密钥有效\n3. 尝试 macOS say 命令 fallback',
    'decision': '决策 API 连续失败：\n1. 检查 Flask 是否在 :5001 运行\n2. 查看 task_wizard.py 日志\n3. 确认 task_id 格式正确',
    'default': '操作连续失败，请检查对应服务状态'
  };

  const tip = tips[key] || tips['default'];
  const html = `<div class="self-heal" id="selfHealTip">
    <span class="sh-dismiss" onclick="hideSelfHealTip()">✕</span>
    <div class="sh-title">💡 自动诊断提示 (${key})</div>
    <div class="sh-body" style="white-space:pre-line">${tip}</div>
  </div>`;
  rightEl.insertAdjacentHTML('afterbegin', html);
}

// @@FUNC: hideSelfHealTip
function hideSelfHealTip() {
  const el = document.getElementById('selfHealTip');
  if (el) el.remove();
}

// @@FUNC: autoCollapseDetails
function autoCollapseDetails() {
  const secBodies = document.querySelectorAll('.sec-body');
  secBodies.forEach((body) => {
    body.classList.remove('collapsed');
    const hdr = body.closest('.sec')?.querySelector('.sec-hdr');
    if (hdr) hdr.classList.add('expanded');
  });
}

// @@FUNC: toggleAssetPanel
function toggleAssetPanel(){
  console.log("assetToggle clicked");
  const p=document.getElementById('assetPanel'),o=document.getElementById('assetOverlay');
  if(p.classList.contains('open')){p.classList.remove('open');o.classList.remove('on')}
  else{p.classList.add('open');o.classList.add('on');loadAssetPanel()}
}

// @@FUNC: switchAssetTab
function switchAssetTab(el,type){
  document.querySelectorAll('#assetTabs .asset-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');loadAssetPanel(type);
}

// @@FUNC: loadAssetPanel
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

// @@FUNC: toggleDirectorMode
function toggleDirectorMode() {
  var left = document.querySelector('.left');
  var topbar = document.querySelector('.topbar');
  var version = document.getElementById('VER_BADGE');
  var kbd = document.getElementById('kbdToggle');
  var expandAll = document.getElementById('expandAll');
  var dlwrap = document.querySelector('.dl-wrap');
  var assetBtn = document.getElementById('assetToggle');
  var galleryLink = document.querySelector('a[href="/gallery"]');
  var dirBtn = document.getElementById('dirModeBtn');
  var prdAlert = document.getElementById('prdStaleAlert');
  var isActive = document.body.classList.toggle('director-mode');

  if (isActive) {
    if (left) left.style.display = 'none';
    if (version) version.style.display = 'none';
    if (kbd) kbd.style.display = 'none';
    if (expandAll) expandAll.style.display = 'none';
    if (dlwrap) dlwrap.style.display = 'none';
    if (assetBtn) assetBtn.style.display = 'none';
    if (galleryLink) galleryLink.style.display = 'none';
    if (prdAlert) prdAlert.style.display = 'none';
    if (dirBtn) dirBtn.textContent = '🎬 退出导演模式';
    // Hide src-tags
    document.querySelectorAll('.src-tag').forEach(function(e) { e.style.display = 'none'; });
    // Hide stats bar
    document.querySelectorAll('.stats').forEach(function(e) { e.style.display = 'none'; });
  } else {
    if (left) left.style.display = '';
    if (version) version.style.display = '';
    if (kbd) kbd.style.display = '';
    if (expandAll) expandAll.style.display = '';
    if (dlwrap) dlwrap.style.display = '';
    if (assetBtn) assetBtn.style.display = '';
    if (galleryLink) galleryLink.style.display = '';
    if (prdAlert) prdAlert.style.display = '';
    if (dirBtn) dirBtn.textContent = '🎬 导演模式';
    document.querySelectorAll('.src-tag').forEach(function(e) { e.style.display = ''; });
    document.querySelectorAll('.stats').forEach(function(e) { e.style.display = ''; });
  }
  localStorage.setItem('director_mode', isActive ? '1' : '0');
}

// @@FUNC: retryComfyUI
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

// @@FUNC: renderMilestoneCharts
function renderMilestoneCharts(fid) {
  if (fid === 'DM-0') {
    var d = lastData.decisions ? lastData.decisions['DM-0'] : null;
    if (d) renderReviewRadar(d);
  } else if (fid === 'MS-1' || fid === 'MS-2') {
    var ms = findMilestone(fid);
    if (ms && ms.meta) renderProfitChart(ms.meta);
  }
}

// @@FUNC: render (main rendering)
function render(){
  let f=all.filter(m=>m.pipeline===cur);
  if(searchQ) f=f.filter(m=>(m.ms_id+' '+(m.name||'')+' '+(m.task_id||'')).toLowerCase().includes(searchQ));
  if(filterSt!=='all') f=f.filter(m=>m.status===filterSt);
  document.getElementById('tkCount').textContent=all.filter(m=>m.pipeline=='tk').length;
  document.getElementById('dmCount').textContent=all.filter(m=>m.pipeline=='drama').length;

  const done=f.filter(m=>m.status=='completed'||m.status=='approved').length;
  const pnd=f.filter(m=>m.status=='waiting_approval').length;
  const mck=f.filter(m=>m.data_source=='mock').length;
  document.getElementById('statDone').textContent=done;
  document.getElementById('statPending').textContent=pnd;
  document.getElementById('statMock').textContent=mck;
  document.getElementById('statTotal').textContent=f.length;
  if(searchQ||filterSt!=='all'){
    const total=all.filter(m=>m.pipeline===cur).length;
    let fi=`<div style="font-size:9px;color:#555;padding:2px 8px">筛选: ${f.length}/${total} 项</div>`;
    document.getElementById('list').insertAdjacentHTML('afterbegin',fi);
  }

  const g={};
  f.forEach(m=>{const tid=m.task_id||'_';if(!g[tid])g[tid]=[];g[tid].push(m)});
  const tl={'TK-MS0-GATE':'MS-0 采集门禁','TK-SELECTION':'选品与市场判断','TK-LOCALIZE':'本地化与上架准备',
    'TK-PUBLISH':'发布与日报','TK-DM-PREP':'前期策划','TK-DM-PROD':'制片制作','TK-DM-DIST':'发布分发','_':'未分组'};

  let h='';
  for(const [tid,ml] of Object.entries(g)){
    const dt=ml.filter(m=>m.status=='completed'||m.status=='approved').length;
    const cls=dt===ml.length?'g':dt>0?'y':'n';
    h+=`<div class="task-hdr"><span class="td ${cls}"></span><span class="tn">${tl[tid]||tid}</span><span class="tp">${dt}/${ml.length}</span></div>`;
    ml.forEach(m=>{
      const dc=m.status=='completed'||m.status=='approved'?'d':m.status=='waiting_approval'?'w':'p';
      const ic=m.status=='completed'||m.status=='approved'?'&#10003;':m.status=='waiting_approval'?'&#9699;':'&#9711;';
      let b='';
      if(m.data_source!=='real')b+=`<span class="bdg ${m.data_source=='mock'?'mk':'cp'}">${m.data_source=='mock'?'模拟':'推算'}</span>`;
      if(m.decision_point&&m.status=='waiting_approval')b+='<span class="bdg dc">待决策</span>';
      if(m.decision_point&&m.decision=='approved')b+='<span class="bdg ok">已批准</span>';
      h+=`<div class="ms-item${sel===m.ms_id?' sel':''}${m.status=='waiting_approval'?' waiting':''}" onclick="select('${m.ms_id}')">
        <span class="dot ${dc}"></span><span class="nm">${ic} ${m.ms_id} ${m.name}</span>${b}</div>`;
    });
  }
  document.getElementById('list').innerHTML=h;

  if(sel)renderDetail();
  else{document.getElementById('empty').style.display='block';document.getElementById('detail').style.display='none';renderSummary()}
}
