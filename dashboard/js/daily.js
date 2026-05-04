// === daily.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: triggerDailyReport
async function triggerDailyReport(){
  var btn=document.getElementById('btn-daily-push');
  if(btn){btn.classList.add('busy');btn.disabled=true;btn.textContent='⏳ 推送中...';}
  toastMsg('🔄 正在手动推送今日日报...', 3000);
  try{
    var r=await fetch('/api/daily-report/push',{method:'POST'});
    if(!r.ok){toastMsg('推送失败: HTTP '+r.status,3000,'error');return;}
    toastMsg('✅ 今日日报推送成功',4000,'success');
  }catch(e){toastMsg('❌ 推送失败: '+e.message,3000,'error');}
  if(btn){btn.classList.remove('busy');btn.disabled=false;btn.textContent='🔄 手动推送今日日报';}
}

// @@FUNC: previewDailyReport
function previewDailyReport(){
  toastMsg('👁️ 正在加载日报预览...', 2000);
  fetch('/api/daily-report/preview').then(function(r){return r.json();}).then(function(d){
    if(!d||!d.preview||!d.preview.groups){showToast('❌ 预览加载失败',3000);return;}
    var groups=d.preview.groups;
    var h='<div style="max-width:700px;margin:0 auto;max-height:80vh;overflow-y:auto">';
    h+='<div style="font-size:12px;color:#888;margin-bottom:8px">📊 日报预览 — '+d.preview.generated_at+' · '+groups.length+' 群</div>';
    groups.forEach(function(g){
      h+='<div style="background:#1a1d27;border-radius:8px;padding:12px;margin-bottom:8px;border-left:3px solid #3b82f6">';
      h+='<div style="font-weight:600;font-size:12px;margin-bottom:6px">'+g.emoji+' '+g.name+' — '+g.title+'</div>';
      h+='<div style="font-size:10px;color:#aaa;white-space:pre-wrap;line-height:1.5;max-height:200px;overflow-y:auto">'+(g.content||'(无内容)')+'</div>';
      h+='</div>';
    });
    h+='</div>';
    var dlg=document.createElement('div');
    dlg.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);z-index:300;display:flex;align-items:center;justify-content:center;cursor:pointer';
    dlg.innerHTML='<div style="background:#0f1117;border-radius:12px;padding:20px;max-width:750px;width:95%;cursor:default" onclick="event.stopPropagation()">'+h+'<button class="btn btn-w" style="margin-top:12px" onclick="this.parentElement.parentElement.remove()">关闭</button></div>';
    dlg.onclick=function(){dlg.remove();};
    document.body.appendChild(dlg);
  }).catch(function(e){showToast('❌ 预览失败: '+e.message,3000);});
}

// @@FUNC: viewPushHistory
function viewPushHistory(){
  toastMsg('📋 加载推送历史...', 2000);
  fetch('/api/daily-report/history').then(function(r){return r.json();}).then(function(d){
    var h='<div style="max-width:700px;margin:0 auto;max-height:80vh;overflow-y:auto">';
    h+='<div style="font-size:12px;color:#888;margin-bottom:8px">📋 推送历史 — 共 '+d.total+' 次</div>';
    (d.history||[]).forEach(function(entry,i){
      var ts=entry.timestamp||'';
      var trigger=entry.trigger||'auto';
      var ok=(entry.results||{}).ok||0;
      var fail=(entry.results||{}).fail||0;
      h+='<div style="background:#1a1d27;border-radius:6px;padding:8px 12px;margin-bottom:4px;display:flex;align-items:center;gap:8px;font-size:11px">';
      h+='<span style="color:#888">#'+(d.total-i)+'</span>';
      h+='<span style="color:#aaa">'+ts.substring(0,19).replace('T',' ')+'</span>';
      h+='<span style="color:#888;font-size:9px">'+trigger+'</span>';
      h+='<span style="color:#22c55e">✅ '+ok+'</span>';
      if(fail>0) h+='<span style="color:#ef4444">❌ '+fail+'</span>';
      h+='</div>';
    });
    if(!d.history||!d.history.length) h+='<div style="color:#555;text-align:center;padding:20px">暂无推送记录</div>';
    h+='</div>';
    var dlg=document.createElement('div');
    dlg.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);z-index:300;display:flex;align-items:center;justify-content:center;cursor:pointer';
    dlg.innerHTML='<div style="background:#0f1117;border-radius:12px;padding:20px;max-width:650px;width:95%;cursor:default" onclick="event.stopPropagation()">'+h+'<button class="btn btn-w" style="margin-top:12px" onclick="this.parentElement.parentElement.remove()">关闭</button></div>';
    dlg.onclick=function(){dlg.remove();};
    document.body.appendChild(dlg);
  }).catch(function(e){showToast('❌ 加载失败: '+e.message,3000);});
}

