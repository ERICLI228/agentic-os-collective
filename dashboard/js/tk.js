// === tk.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: onTKSearch
function onTKSearch(val) {
  var q = val.toLowerCase();
  var items = document.querySelectorAll('#list .ms-item');
  var visible = 0;
  items.forEach(function(el) {
    var text = (el.textContent || '').toLowerCase();
    var show = !q || text.indexOf(q) >= 0;
    el.style.display = show ? '' : 'none';
    if (show) visible++;
  });
  var total = document.querySelectorAll('#list .ms-item').length;
  var hint = document.getElementById('tkSearchHint');
  if (!hint) {
    hint = document.createElement('div');
    hint.id = 'tkSearchHint';
    hint.style.cssText = 'font-size:9px;color:#555;text-align:center;padding:4px';
    document.getElementById('list').appendChild(hint);
  }
  if (q) hint.textContent = visible + '/' + total + ' 匹配';
  else hint.textContent = '';
}

// @@FUNC: extractImages
function extractImages(note) {
  if(!note) return [];
  const imgs = [];
  const m1 = note.match(/image:\s*(\/api\/images\/file\/[^\s|]+)/g);
  if(m1) m1.forEach(m=>{ imgs.push({url:m.replace('image: ','').trim(), type:'product'}); });
  const m2 = note.match(/渲染:\s*(\/api\/render\/[^\s|]+)/g);
  if(m2) m2.forEach(m=>{ imgs.push({url:m.replace('渲染: ','').trim(), type:'render'}); });
  return imgs;
}

// @@FUNC: checkImage
function checkImage(url){
  return new Promise(r=>{
    const img = new Image();
    img.onload = ()=>r(true);
    img.onerror = ()=>r(false);
    img.src = url;
    setTimeout(()=>r(false), 3000);
  });
}

// @@FUNC: renderTKDetail
async function renderTKDetail(detail, ms) {
  var el = document.getElementById('detail');
  if (!detail || !detail.sections) return;
  el.innerHTML='';
  el.insertAdjacentHTML('beforeend', renderMilestoneTimeline(ms.ms_id));
  el.insertAdjacentHTML('beforeend', renderMilestoneSummary(detail, ms));
  var h='<div id="ms-detail-'+ms.ms_id+'" class="accordion-content">';
  detail.sections.forEach(function(s) {
    h += '<div class="sec"><h3>' + (s.title||'') + ' <span class="src-tag src-' + (s.source||'mock') + '\">[' + (s.source||'mock') + ']</span></h3>';
    (s.items||[]).forEach(function(it) {
      var label = it.label || it.key || '';
      var val = it.value || '';
      var note = it.note || '';
      h += '<div class="ent-row"><span class="ent-lbl">' + label + '</span><div class="ent-val"><span>' + val + '</span>';
      if (it.before) h += '<div class="before">\u2190 ' + it.before + '</div>';
      if (it.after) h += '<div class="after">\u2192 ' + it.after + '</div>';
      if (note) h += '<div class="note">' + note + '</div>';
      h += '</div></div>';
    });
    h += '</div>';
  });
  h+='</div>';
  el.insertAdjacentHTML('beforeend', h);
}

// @@FUNC: loadTKImageStatus
async function loadTKImageStatus(imgId){
  try{
    var r=await fetch('/api/images/'+imgId);
    if(!r.ok) return {id:imgId, files:{}};
    return await r.json();
  }catch(e){return {id:imgId, files:{}};}
}

// @@FUNC: renderTKImageCards
function renderTKImageCards(images){
  var h='';
  images.forEach(function(img){
    var files=img.files||{};
    var hasOrig=!!files.original;
    var hasNobg=!!files.nobg;
    var hasFinal=!!files.final;
    var hasResult=hasNobg||hasFinal;
    var meta=_tkProductImages.find(function(p){return p.id===img.id;})||{label:img.id,desc:''};
    h+='<div class="img-card" style="max-width:'+(hasResult?'420':'200')+'px">';
    // Side-by-side comparison for processed images
    if(hasResult){
      h+='<div class="img-compare-container" style="display:flex;gap:4px">';
      h+='<div class="img-compare-side" style="flex:1;background:#1a1d27;border-radius:4px;overflow:hidden">';
      h+='<div style="font-size:9px;color:#888;text-align:center;padding:2px">📷 原图</div>';
      if(hasOrig) h+='<img src="'+files.original+'" loading="lazy" style="width:100%;height:120px;object-fit:contain" onerror="this.parentElement.innerHTML+=\'<div style=text-align:center;color:#555;padding:20px>加载失败</div>\'"/>';
      else h+='<div style="text-align:center;color:#555;font-size:10px;padding:20px">待生成</div>';
      h+='</div>';
      h+='<div class="img-compare-side" style="flex:1;background:#0f1a2e;border-radius:4px;overflow:hidden;border:1px solid rgba(34,197,94,.2)">';
      h+='<div style="font-size:9px;color:#22c55e;text-align:center;padding:2px;background:rgba(34,197,94,.08)">✅ 处理后</div>';
      var resultUrl=files.final||files.nobg||'';
      if(resultUrl) h+='<img src="'+resultUrl+'?t='+Date.now()+'" loading="lazy" style="width:100%;height:120px;object-fit:contain" onerror="this.parentElement.innerHTML+=\'<div style=text-align:center;color:#555;padding:20px>加载失败</div>\'"/>';
      else h+='<div style="text-align:center;color:#555;font-size:10px;padding:20px">待处理</div>';
      h+='</div>';
      h+='</div>';
      // Feedback input + reprocess
      h+='<div class="img-feedback-bar" style="padding:4px 6px;display:flex;gap:4px;align-items:center;border-top:1px solid #222">';
      h+='<input type="text" id="fb-'+img.id+'" placeholder="修改意见..." style="flex:1;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px 6px;border-radius:4px;font-size:10px">';
      h+='<button class="mini-btn" onclick="reprocessTKImage(\''+img.id+'\',this)">🔄 重新处理</button>';
      h+='</div>';
    }else{
      // Original view (no processing yet)
      h+='<div class="img-preview" style="height:180px;overflow:hidden;background:#1a1d27;display:flex;align-items:center;justify-content:center">';
      if(hasOrig){
        h+='<img src="'+files.original+'" loading="lazy" style="max-width:100%;max-height:100%;object-fit:contain" onerror="this.parentElement.innerHTML=\'<div class=img-placeholder-text style=font-size:11px;color:#666>预览加载失败</div>\'"/>';
      }else{
        h+='<div style="text-align:center;color:#555;font-size:11px;padding:20px">📷<br>待生成</div>';
      }
      h+='</div>';
    }
    // Card info (common)
    h+='<div class="img-card-info" style="padding:6px 8px;font-size:10px;border-top:1px solid #222">';
    h+='<div style="color:#ccc;font-weight:600;margin-bottom:2px">'+meta.label+'</div>';
    h+='<div style="color:#888;font-size:9px">'+meta.desc+'</div>';
    h+='<div style="margin-top:4px;display:flex;gap:3px;flex-wrap:wrap">';
    if(hasOrig) h+='<span class="bdg ok">原图</span>';
    if(hasNobg) h+='<span class="bdg cp" style="background:#1a2756;color:#93c5fd">去底</span>';
    if(hasFinal) h+='<span class="bdg ok">成品</span>';
    h+='</div>';
    h+='<div class="img-actions" style="margin-top:6px;display:flex;gap:3px;flex-wrap:wrap">';
    h+='<button class="mini-btn" onclick="processTKImage(\''+img.id+'\',\'rembg\',this)" '+(hasNobg?'disabled':'')+'>去背景</button>';
    h+='<button class="mini-btn" onclick="processTKImage(\''+img.id+'\',\'full\',this)">一键处理</button>';
    h+='<button class="mini-btn" onclick="processTKImage(\''+img.id+'\',\'check\',this)">合规检查</button>';
    h+='</div>';
    h+='</div>';
    h+='</div>';
  });
  return h;
}

// @@FUNC: reprocessTKImage
async function reprocessTKImage(imgId, btn){
  var fb=document.getElementById('fb-'+imgId);
  var feedback=fb?fb.value.trim():'';
  if(btn){btn.disabled=true;btn.textContent='⏳...';}
  try{
    var r=await fetch('/api/images/'+imgId+'/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:'full',feedback:feedback})
    });
    if(!r.ok){showToast('❌ 处理失败',3000);return;}
    showToast('✅ 重新处理完成',3000,'success');
    if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  }catch(e){showToast('❌ '+e.message,3000);}
  if(btn){btn.disabled=false;btn.textContent='🔄 重新处理';}
}

// @@FUNC: renderTKCompliance
function renderTKCompliance(reqItems){
  var h='';
  h+='<div style="margin-bottom:8px;font-size:12px;color:#aaa;font-weight:600">📋 TK 5站图像合规标准</div>';
  h+='<div style="background:rgba(255,255,255,.02);border-radius:8px;border:1px solid rgba(255,255,255,.05);overflow:hidden">';
  h+='<table style="width:100%;border-collapse:collapse;font-size:12px">';
  h+='<tr style="background:rgba(255,255,255,.04)"><th style="text-align:left;padding:8px 12px;border-bottom:1px solid #333;color:#888;font-weight:500;width:30%">检查项</th><th style="text-align:left;padding:8px 12px;border-bottom:1px solid #333;color:#888;font-weight:500">标准</th></tr>';
  reqItems.forEach(function(it){
    var isWarn=it.status==='warn';
    h+='<tr style="'+(isWarn?'background:rgba(239,68,68,.05)':'')+'">';
    h+='<td style="padding:8px 12px;border-bottom:1px solid #222;'+(isWarn?'color:#f87171':'color:#ccc')+'">'+(isWarn?'⚠️ ':'✅ ')+(it.label||'')+'</td>';
    h+='<td style="padding:8px 12px;border-bottom:1px solid #222;color:#aaa">'+(it.value||'')+'</td>';
    h+='</tr>';
  });
  h+='</table></div>';
  return h;
}

// @@FUNC: processTKImage
async function processTKImage(imgId,action,btn){
  if(!imgId||!action) return;
  if(btn){btn.disabled=true;btn.textContent='处理中...';}
  try{
    var r=await fetch('/api/images/'+imgId+'/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:action})
    });
    var d=await r.json();
    if(!r.ok){showToast('❌ '+action+': '+(d.error||'失败'),3000);return;}
    var steps=(d.steps||[]).join(' · ');
    showToast('✅ '+imgId+' '+action+': '+(steps||'完成'),3000);
    // refresh image card status
    if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  }catch(e){
    showToast('❌ 处理失败: '+e.message,3000);
  }finally{
    if(btn){btn.disabled=false;btn.textContent=action==='rembg'?'去背景':action==='full'?'一键处理':'合规检查';}
  }
}

// @@FUNC: refreshTKImageCards
async function refreshTKImageCards(detail){
  var wb=document.getElementById('ms23-workbench');
  if(!wb) return;
  // reload image statuses
  var imgStatuses=[];
  for(var i=0;i<_tkProductImages.length;i++){
    var st=await loadTKImageStatus(_tkProductImages[i].id);
    imgStatuses.push(st);
  }
  // re-render just the cards section
  var cardHTML=renderTKImageCards(imgStatuses);
  var cardEl=document.getElementById('ms23-cards');
  if(cardEl) cardEl.innerHTML=cardHTML;
}

// @@FUNC: renderTKImageWorkbench
async function renderTKImageWorkbench(detail,ms){
  var detailEl=document.getElementById('detail');
  detailEl.insertAdjacentHTML('beforeend','<div class="sec" id="ms23-sec"><h3>📦 TK商品图处理工作台</h3><div id="ms23-workbench"><span class="loading">加载中...</span></div></div>');
  window._currentMS23Detail=detail;

  if(!detail||!detail.sections||!detail.sections.length){
    document.getElementById('ms23-workbench').innerHTML='<div style="text-align:center;padding:20px;color:#888;font-size:12px">⚠️ 暂无数据</div>';
    return;
  }

  var sections=detail.sections;
  var reqSection=sections.find(function(s){return s&&s.source==='real';})||sections[1]||{};
  var reqItems=(reqSection.items||[]).filter(function(it){return it&&typeof it==='object';});
  var actSection=sections.find(function(s){return s&&s.title&&s.title.indexOf('操作')>=0;})||sections[2]||{};
  var actItems=(actSection.items||[]).filter(function(it){return it&&typeof it==='object';});

  var wb=document.getElementById('ms23-workbench');
  var h='';

  // --- Pipeline visualization ---
  h+='<div style="background:#1a1d27;border-radius:8px;padding:12px;margin-bottom:12px">';
  h+='<div style="font-size:11px;color:#888;margin-bottom:8px">⚙️ 图像处理管线</div>';
  h+='<div style="display:flex;align-items:center;gap:4px;font-size:10px;color:#aaa;flex-wrap:wrap">';
  ['📷 原图','🔲 去背景','📐 尺寸调整','✅ 合规检查','🚀 发布'].forEach(function(step,i,arr){
    h+='<div style="background:rgba(37,99,235,.15);padding:4px 8px;border-radius:4px;border:1px solid rgba(37,99,235,.25);white-space:nowrap">'+step+'</div>';
    if(i<arr.length-1) h+='<span style="color:#444">→</span>';
  });
  h+='</div></div>';

  // --- Product Image Cards ---
  h+='<div style="margin-bottom:8px;font-size:12px;color:#aaa;font-weight:600">📷 商品图片 <span style="color:#666;font-weight:400">'+_tkProductImages.length+' 张</span></div>';
  // load all image statuses
  var imgStatuses=[];
  for(var i=0;i<_tkProductImages.length;i++){
    var st=await loadTKImageStatus(_tkProductImages[i].id);
    imgStatuses.push(st);
  }
  h+='<div id="ms23-cards" class="img-card-grid">'+renderTKImageCards(imgStatuses)+'</div>';

  // batch action bar
  h+='<div style="display:flex;gap:8px;margin-top:10px;margin-bottom:16px;flex-wrap:wrap">';
  h+='<button class="btn btn-s" onclick="batchProcessAll()">⚡ 一键批量处理全部</button>';
  h+='<span style="font-size:10px;color:#555;line-height:30px">处理流程: rembg → resize → compliance</span>';
  h+='</div>';

  // --- Compliance Requirements ---
  if(reqItems.length){
    h+=renderTKCompliance(reqItems);
  }

  // --- Quick Actions Panel ---
  if(actItems.length){
    // v3.6.29: 工具箱卡片代替技术命令列表
    h+='<div style="margin-top:16px;margin-bottom:8px;font-size:12px;color:#aaa;font-weight:600">🔧 商品图处理工具箱</div>';

    // 区块一：处理进度总览
    h+='<div class="toolbox-progress" id="toolbox-progress">';
    h+='<div class="progress-label">📊 图片处理进度</div>';
    h+='<div class="progress-bar-container"><div class="progress-bar-fill" id="toolbox-progress-fill" style="width:0%">0/4 已处理</div></div>';
    h+='<div class="progress-detail" id="toolbox-progress-detail">加载中...</div>';
    h+='</div>';

    // 区块二：三张功能卡片
    h+='<div class="toolbox-cards">';
    h+='<div class="tool-card" id="tool-card-rembg" onclick="handleRembg()">';
    h+='<div class="tool-card-icon">🎨</div>';
    h+='<div class="tool-card-title">一键去背景</div>';
    h+='<div class="tool-card-desc">为选中的商品图自动移除背景，生成纯白底图</div>';
    h+='<div class="tool-card-status" id="tool-status-rembg">准备就绪</div>';
    h+='</div>';
    h+='<div class="tool-card" id="tool-card-batch" onclick="handleBatchProcess()">';
    h+='<div class="tool-card-icon">⚡</div>';
    h+='<div class="tool-card-title">全部批量处理</div>';
    h+='<div class="tool-card-desc">一键处理所有待处理的商品图（去背景→调整尺寸→合规检查）</div>';
    h+='<div class="tool-card-status" id="tool-status-batch">准备就绪</div>';
    h+='</div>';
    h+='<div class="tool-card" id="tool-card-check" onclick="handleComplianceCheck()">';
    h+='<div class="tool-card-icon">✅</div>';
    h+='<div class="tool-card-title">合规检查</div>';
    h+='<div class="tool-card-desc">检查所有图片是否符合TK平台尺寸和格式规范</div>';
    h+='<div class="tool-card-status" id="tool-status-check">准备就绪</div>';
    h+='</div>';
    h+='</div>';

    // 区块三：技术详情折叠卡片
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术详情 (API调用路径)</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    actItems.forEach(function(act){
      var label=act.label||'';
      var desc=act.value||'';
      h+='<div class="ent-row"><span class="ent-lbl">'+label+'</span><div class="ent-val"><span>'+desc.substring(0,200)+'</span></div></div>';
    });
    h+='</div></div>';
  }

  wb.innerHTML=h;
}

// @@FUNC: updateToolboxProgress
function updateToolboxProgress(){
  var total=_tkProductImages.length;
  if(!total) return;
  // 检查每个图片的处理状态
  Promise.all(_tkProductImages.map(function(p){return loadTKImageStatus(p.id);})).then(function(statuses){
    var done=0;
    statuses.forEach(function(s){
      if(s.files&&(s.files.final||s.files.nobg)) done++;
    });
    var pct=Math.round(done/total*100);
    var fill=document.getElementById('toolbox-progress-fill');
    var detail=document.getElementById('toolbox-progress-detail');
    if(fill){
      fill.style.width=pct+'%';
      fill.textContent=done+'/'+total+' 已处理';
    }
    if(detail) detail.textContent=(total-done)+' 张待处理 · '+done+' 张已完成';
  });
}

// @@FUNC: handleRembg
async function handleRembg(){
  var card=document.getElementById('tool-card-rembg');
  var status=document.getElementById('tool-status-rembg');
  if(!card||!status)return;
  card.classList.add('busy');
  status.className='tool-card-status processing';
  status.textContent='⏳ 处理中...';
  showToast('🎨 正在执行去背景处理...',3000);
  try{
    var r=await fetch('/api/images/phone_case_main/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:'rembg'})
    });
    var d=await r.json();
    if(!r.ok){showToast('❌ 去背景失败: '+(d.error||'未知'),3000,'error');status.className='tool-card-status error';status.textContent='处理失败';card.classList.remove('busy');return;}
    status.className='tool-card-status done';
    status.textContent='✅ 已完成';
    showToast('✅ 去背景完成',3000,'success');
    if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
    updateToolboxProgress();
  }catch(e){showToast('❌ 去背景失败: '+e.message,3000,'error');status.className='tool-card-status error';status.textContent='处理失败';}
  card.classList.remove('busy');
  setTimeout(function(){if(status)status.className='tool-card-status';status.textContent='准备就绪';},3000);
}

// @@FUNC: handleBatchProcess
async function handleBatchProcess(){
  var card=document.getElementById('tool-card-batch');
  var status=document.getElementById('tool-status-batch');
  if(!card||!status)return;
  card.classList.add('busy');
  status.className='tool-card-status processing';
  status.textContent='⏳ 批量处理中...';
  showToast('⚡ 开始批量处理 '+_tkProductImages.length+' 张图片...',3000);
  for(var i=0;i<_tkProductImages.length;i++){
    showToast('⏳ 处理 '+_tkProductImages[i].id+' ('+(i+1)+'/'+_tkProductImages.length+')...',2000);
    try{
      await fetch('/api/images/'+_tkProductImages[i].id+'/process',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({action:'full'})
      });
    }catch(e){}
  }
  showToast('✅ 全部批量处理完成 ('+_tkProductImages.length+'张)',4000,'success');
  status.className='tool-card-status done';
  status.textContent='✅ 已完成';
  if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  updateToolboxProgress();
  card.classList.remove('busy');
  setTimeout(function(){if(status)status.className='tool-card-status';status.textContent='准备就绪';},3000);
}

// @@FUNC: handleComplianceCheck
async function handleComplianceCheck(){
  var card=document.getElementById('tool-card-check');
  var status=document.getElementById('tool-status-check');
  if(!card||!status)return;
  card.classList.add('busy');
  status.className='tool-card-status processing';
  status.textContent='⏳ 检查中...';
  showToast('✅ 正在执行合规检查...',3000);
  try{
    var r=await fetch('/api/images/phone_case_main/process',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:'check'})
    });
    var d=await r.json();
    if(!r.ok){showToast('❌ 合规检查失败: '+(d.error||'未知'),3000,'error');status.className='tool-card-status error';status.textContent='检查失败';card.classList.remove('busy');return;}
    var report=d.result||d;
    var msg='合规检查结果:\n';
    if(typeof report==='object'){
      Object.keys(report).forEach(function(k){msg+=k+': '+JSON.stringify(report[k])+'\n';});
    }else{msg+=report;}
    alert('📋 合规检查报告\n\n'+msg);
    status.className='tool-card-status done';
    status.textContent='✅ 已完成';
    showToast('✅ 合规检查完成',3000,'success');
  }catch(e){showToast('❌ 合规检查失败: '+e.message,3000,'error');status.className='tool-card-status error';status.textContent='检查失败';}
  card.classList.remove('busy');
  setTimeout(function(){if(status)status.className='tool-card-status';status.textContent='准备就绪';},3000);
}

// @@FUNC: batchProcessAll
async function batchProcessAll(){
  showToast('⚡ 开始批量处理 '+_tkProductImages.length+' 张图片...',3000);
  for(var i=0;i<_tkProductImages.length;i++){
    showToast('⏳ 处理 '+_tkProductImages[i].id+' ('+(i+1)+'/'+_tkProductImages.length+')...',2000);
    try{
      await fetch('/api/images/'+_tkProductImages[i].id+'/process',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({action:'full'})
      });
    }catch(e){}
  }
  showToast('✅ 批量处理完成',3000);
  if(window._currentMS23Detail) refreshTKImageCards(window._currentMS23Detail);
  updateToolboxProgress();
}

// @@FUNC: _getImageStatus
function _getImageStatus(img){
  if(img.status==='done'||img.status==='approved') return 'done';
  if(img.processing===true||img.status==='processing') return 'processing';
  return 'pending';
}

// @@FUNC: _renderTKCards
function _renderTKCards(){
  const container=document.getElementById('ms23-workbench');
  if(!container)return;
  const imgs=_tkImageData;
  // Count by status (v3.7.6 P2: use unified function)
  let nAll=imgs.length, nPending=0, nDone=0, nProcessing=0;
  imgs.forEach(function(img){
    const s=_getImageStatus(img);
    if(s==='done') nDone++;
    else if(s==='processing') nProcessing++;
    else nPending++;
  });

  let h='';
  // Filter bar
  h+='<div class="img-filter-bar">';
  h+='<button class="img-filter-btn'+(_tkImageFilter==='all'?' active':'')+'" data-filter="all" onclick="_tkImageFilter=\'all\';_renderTKCards()">全部 ('+nAll+')</button>';
  h+='<button class="img-filter-btn'+(_tkImageFilter==='pending'?' active':'')+'" data-filter="pending" onclick="_tkImageFilter=\'pending\';_renderTKCards()">待处理 ('+nPending+')</button>';
  if(nProcessing>0) h+='<button class="img-filter-btn'+(_tkImageFilter==='processing'?' active':'')+'" data-filter="processing" onclick="_tkImageFilter=\'processing\';_renderTKCards()">处理中 ('+nProcessing+')</button>';
  h+='<button class="img-filter-btn'+(_tkImageFilter==='done'?' active':'')+'" data-filter="done" onclick="_tkImageFilter=\'done\';_renderTKCards()">已完成 ('+nDone+')</button>';
  h+='<button class="img-batch-btn" onclick="_tkBatchProcessAll()">&#9889; 一键批量处理全部</button>';
  h+='</div>';

  // Info card
  h+='<div class="info-card collapsible">';
  h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
  h+='<span>&#128203; TK商品图合规标准</span>';
  h+='<span class="toggle-icon">&#9660;</span>';
  h+='</div>';
  h+='<div class="info-card-body" style="display:none">';
  h+='<ul>';
  h+='<li><strong>主图：</strong>800×800px，白底，占画面80%</li>';
  h+='<li><strong>详情图：</strong>600×800px，最多9张</li>';
  h+='<li><strong>&#127483;&#127455; 越南站：</strong>主图禁止中文，建议加越南语卖点</li>';
  h+='</ul>';
  h+='</div></div>';

  // Card grid
  h+='<div class="img-card-grid">';
  imgs.forEach(function(img,idx){
    const pid=img.id||img.name||img.sku||('img-'+idx);
    const pname=img.name||img.title||pid;
    // v3.7.6 P2: Use unified status function
    const st=_getImageStatus(img);
    const isDone=(st==='done');
    const isProcessing=(st==='processing');
    // v3.7.6 P1: Fix image path — fallback to /api/images/file/<id>
    let orig=img.original||img.orig||'';
    if(!orig&&pid){orig='/api/images/file/'+encodeURIComponent(pid);}
    const nobg=img.nobg||img.no_bg||'';
    const fin=img.final||img.fin||'';
    const show=(_tkImageFilter==='all'||(_tkImageFilter==='done'&&isDone)||(_tkImageFilter==='pending'&&!isDone&&st==='pending')||(_tkImageFilter==='processing'&&st==='processing'));
    if(!show)return;

    let statusTag;
    if(isDone) statusTag='<span class="img-status-tag green">已完成</span>';
    else if(isProcessing) statusTag='<span class="img-status-tag yellow">处理中</span>';
    else statusTag='<span class="img-status-tag yellow">待处理</span>';

    h+='<div class="img-card" data-status="'+st+'" data-idx="'+idx+'">';
    h+='<div class="img-preview">';
    h+='<img src="'+orig+'" loading="lazy" onerror="this.parentElement.innerHTML=\'&lt;div class=\"img-placeholder-text\"&gt;图片加载失败&lt;/div&gt;\'"/>';
    h+=statusTag;
    h+='</div>';

    if(isDone){
      h+='<div class="img-compare-area">';
      h+='<span style="font-size:9px;color:#888">处理后</span>';
      const showImg=fin||nobg||orig;
      if(showImg) h+='<img src="'+showImg+'" loading="lazy" onclick="zoomImg(\''+showImg+'\')" onerror="this.style.display=\'none\'"/>';
      else h+='<div style="font-size:9px;color:#555">无处理后图片</div>';
      h+='</div>';
    }else if(isProcessing){
      h+='<div class="img-actions">';
      h+='<button class="btn-rembg" disabled>处理中...</button>';
      h+='<button class="btn-full" disabled>处理中...</button>';
      h+='</div>';
    }else{
      h+='<div class="img-actions">';
      h+='<button class="btn-rembg" data-img="'+pid+'" data-idx="'+idx+'" onclick="event.stopPropagation();_tkProcessImage(\''+pid+'\','+idx+',\'rembg\',this)">去背景</button>';
      h+='<button class="btn-full" data-img="'+pid+'" data-idx="'+idx+'" onclick="event.stopPropagation();_tkProcessImage(\''+pid+'\','+idx+',\'full\',this)">一键处理</button>';
      h+='</div>';
    }
    h+='</div>';
  });
  h+='</div>';
  container.innerHTML=h;
}

// @@FUNC: _tkProcessImage
function _tkProcessImage(pid,idx,action,btn){
  if(!btn)return;
  btn.disabled=true;
  btn.textContent='处理中...';
  const card=btn.closest('.img-card');
  if(card) card.setAttribute('data-status','processing');

  fetch('/api/images/'+encodeURIComponent(pid)+'/process',{method:'POST',
    headers:{'Content-Type':'application/json'},body:JSON.stringify({action:action,note:''})})
  .then(function(r){return r.json();})
  .then(function(d){
    if(d.error){
      showToast('✖ 处理失败: '+d.error,'error');
      if(btn){btn.disabled=false;btn.textContent=action==='rembg'?'去背景':'一键处理';}
      if(card) card.setAttribute('data-status','pending');
    }else{
      // Update image data
      if(_tkImageData[idx]){
        _tkImageData[idx].status='done';
        if(d.final_path) _tkImageData[idx].final=d.final_path+'?t='+Date.now();
        if(d.nobg_path) _tkImageData[idx].nobg=d.nobg_path+'?t='+Date.now();
      }
      showToast('✔ 图片处理成功','success');
      _renderTKCards();
    }
  })
  .catch(function(e){
    showToast('✖ 处理失败: '+e.message,'error');
    if(btn){btn.disabled=false;btn.textContent=action==='rembg'?'去背景':'一键处理';}
    if(card) card.setAttribute('data-status','pending');
  });
}

// @@FUNC: _tkBatchProcessAll
async function _tkBatchProcessAll(){
  const pending=[];
  _tkImageData.forEach(function(img,idx){
    if(_getImageStatus(img)==='pending') pending.push({img:img,idx:idx});
  });
  if(!pending.length){showToast('⚠ 没有待处理的图片','warn');return;}
  showToast('⚡ 开始批量处理 '+pending.length+' 张图片...','info');
  for(var i=0;i<pending.length;i++){
    var item=pending[i];
    var pid=item.img.id||item.img.name||item.img.sku||('img-'+item.idx);
    await new Promise(function(resolve){
      fetch('/api/images/'+encodeURIComponent(pid)+'/process',{method:'POST',
        headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'full',note:''})})
      .then(function(r){return r.json();})
      .then(function(d){
        if(!d.error){
          if(_tkImageData[item.idx]) _tkImageData[item.idx].status='done';
          showToast('✔ '+(i+1)+'/'+pending.length+' 处理完成','success');
        }else{
          showToast('✖ '+(i+1)+'/'+pending.length+' 失败: '+d.error,'error');
        }
        _renderTKCards();
      })
      .catch(function(e){
        showToast('✖ '+(i+1)+'/'+pending.length+' 异常: '+e.message,'error');
      })
      .finally(function(){resolve();});
    });
  }
  showToast('✔ 批量处理全部完成','success');
}

// @@FUNC: processImage
async function processImage(imgId,action,btn){
  const noteEl=document.getElementById('note-'+imgId);
  const note=noteEl?noteEl.value:'';
  if(btn){btn.classList.add('busy'); btn.textContent='处理中...';}
  try{
    const r=await fetch('/api/images/'+imgId+'/process',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify({action,note})});
    const d=await r.json();
    if(d.error)toastMsg(action+' 失败: '+d.error);
    else {
      toastMsg(action+' 完成: '+(d.steps?d.steps.join(' → '):''));
      if(d.final_path){
        const galleryEl=document.getElementById('prod-gallery-'+imgId);
        const afterEl=document.getElementById('prod-after-'+imgId);
        if(galleryEl&&afterEl){
          afterEl.outerHTML=`<div class="img-card" onclick="event.stopPropagation();zoomImg('${d.final_path}?t='+Date.now())"><img src="${d.final_path}?t=${Date.now()}" loading="lazy" onerror="this.style.display='none'"/><span class="img-label">处理后</span></div>`;
        }
      }
    }
  }catch(e){toastMsg('处理失败: '+e.message)}
  if(btn){btn.classList.remove('busy');btn.textContent=action;}
}

