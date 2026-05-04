// === script_browser.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: toggleSB
async function toggleSB(epNum){
  const sectionId='sb-section-'+epNum;
  const body=document.getElementById(sectionId)||document.getElementById('sb-'+epNum);
  if(!body) return;
  const isOpen=body.classList.contains('accordion-expanded');
  toggleSection(sectionId);
  const rowEl=document.getElementById('eprow-'+epNum);
  if(rowEl) rowEl.classList.toggle('open',!isOpen);
  if(!isOpen && body.querySelector('.loading')){
    await loadStoryboard(epNum);
  }
}

// @@FUNC: openScriptBrowser
function openScriptBrowser(){
  var existing=document.getElementById('script-browser-drawer');
  if(existing){closeScriptBrowser();existing=null;}
  var backdrop=document.createElement('div');
  backdrop.id='script-browser-backdrop';
  backdrop.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.45);z-index:999';
  backdrop.onclick=function(){closeScriptBrowser();};
  document.body.appendChild(backdrop);
  var drawer=document.createElement('div');
  drawer.id='script-browser-drawer';
  drawer.style.cssText='position:fixed;top:0;right:0;bottom:0;width:65%;max-width:900px;background:#0f1018;z-index:1000;transform:translateX(100%);transition:transform .3s ease;display:flex;flex-direction:column;box-shadow:-4px 0 24px rgba(0,0,0,.5)';
  var h='<div style=\"flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 18px;background:#1a1d27;border-bottom:1px solid rgba(59,130,246,.2)\">';
  h+='<div style=\"display:flex;align-items:center;gap:10px\">';
  h+='<span style=\"font-size:15px;font-weight:700;color:#e4e6eb\">\u{1F4D6} \u5267\u672C\u6D4F\u89C8</span>';
  h+='<label style=\"display:flex;align-items:center;gap:4px;font-size:9px;color:#888;cursor:pointer;user-select:none\">';
  h+='<input type=\"checkbox\" id=\"script-preview-toggle\" onchange=\"toggleScriptBrowserMode()\" style=\"cursor:pointer;margin:0\"> \u9884\u89C8\u6A21\u5F0F</label>';
  h+='</div>';
  h+='<span onclick=\"closeScriptBrowser()\" style=\"cursor:pointer;font-size:22px;color:#555;line-height:1\">&times;</span>';
  h+='</div>';
  h+='<div id=\"script-browser-pills\" style=\"flex:0 0 auto;display:flex;gap:6px;padding:10px 16px;overflow-x:auto;border-bottom:1px solid #1e2130\"><span class=\"loading\">\u52A0\u8F7D\u5267\u96C6...</span></div>';
  h+='<div id=\"script-browser-content\" style=\"flex:1;overflow-y:auto;padding:16px 20px\"><div style=\"text-align:center;padding:40px;color:#888\">\u52A0\u8F7D\u4E2D...</div></div>';
  drawer.innerHTML=h;
  document.body.appendChild(drawer);
  requestAnimationFrame(function(){drawer.style.transform='translateX(0)';});
  fetch('/api/script').then(function(r){return r.json();}).then(function(d){
    var eps=d.episodes||d||[];
    if(!Array.isArray(eps))eps=Object.values(eps);
    window._scriptBrowserEps=eps;
    renderScriptBrowserPills(eps);
    if(eps.length>0){
      var firstEp=eps[0].episode||eps[0].ep||1;
      selectScriptBrowserEp(firstEp);
    }
  }).catch(function(e){
    var pills=document.getElementById('script-browser-pills');
    if(pills)pills.innerHTML='<span style=\"color:#ef4444;font-size:10px\">\u52A0\u8F7D\u5931\u8D25</span>';
  });
}

// @@FUNC: closeScriptBrowser
function closeScriptBrowser(){
  var d=document.getElementById('script-browser-drawer');
  var b=document.getElementById('script-browser-backdrop');
  if(d)d.style.transform='translateX(100%)';
  if(b)b.style.opacity='0';
  setTimeout(function(){if(d)d.remove();if(b)b.remove();},300);
}

// @@FUNC: renderScriptBrowserPills
function renderScriptBrowserPills(eps){
  var pills=document.getElementById('script-browser-pills');
  if(!pills)return;
  var h='';
  eps.forEach(function(ep,i){
    var epNum=ep.episode||ep.ep||(i+1);
    var title=ep.title||'EP'+String(epNum).padStart(2,'0');
    var score=ep.score||'';
    h+='<span class=\"script-ep-pill\" data-ep=\"'+epNum+'\" onclick=\"selectScriptBrowserEp('+epNum+')\" style=\"display:inline-flex;align-items:center;gap:4px;padding:5px 12px;border-radius:16px;font-size:10px;cursor:pointer;white-space:nowrap;background:rgba(255,255,255,.04);color:#888;border:1px solid transparent;transition:all .15s\">'+title+(score?' <span style=\"font-size:8px;color:#fbbf24\">'+score+'\u5206</span>':'')+'</span>';
  });
  pills.innerHTML=h;
}

// @@FUNC: selectScriptBrowserEp
function selectScriptBrowserEp(epNum){
  window._scriptBrowserEp=epNum;
  var pills=document.getElementById('script-browser-pills');
  if(pills){
    var all=pills.querySelectorAll('.script-ep-pill');
    for(var i=0;i<all.length;i++){
      var match=all[i].dataset.ep==epNum;
      all[i].style.background=match?'rgba(59,130,246,.15)':'rgba(255,255,255,.04)';
      all[i].style.color=match?'#60a5fa':'#888';
      all[i].style.borderColor=match?'rgba(59,130,246,.3)':'transparent';
    }
  }
  var previewToggle=document.getElementById('script-preview-toggle');
  if(previewToggle&&previewToggle.checked){
    renderScriptBrowserPreview(epNum);
  }else{
    renderScriptBrowserDetail(epNum);
  }
}

// @@FUNC: toggleScriptBrowserMode
function toggleScriptBrowserMode(){
  var epNum=window._scriptBrowserEp||1;
  selectScriptBrowserEp(epNum);
}

// @@FUNC: renderScriptBrowserDetail
function renderScriptBrowserDetail(epNum){
  var content=document.getElementById('script-browser-content');
  if(!content)return;
  var epId=String(epNum).padStart(2,'0');
  content.innerHTML='<div style=\"text-align:center;padding:40px;color:#888\"><span class=\"loading\">\u52A0\u8F7D\u5206\u955C...</span></div>';
  fetch('/api/script/'+epId).then(function(r){return r.json();}).then(function(data){
    var sb=data.storyboard||[];
    var title=data.title||'EP'+epId;
    var score=data.score||'';
    var tags=(data.tags||[]).join(' \u00B7 ')||'';
    var ch=data.main_character||'';
    var scenes=data.scene_count||sb.length||0;
    var h='';
    h+='<h2 style=\"margin:0 0 4px;color:#e4e6eb;font-size:16px\">'+title+'</h2>';
    h+='<div style=\"margin-bottom:16px;font-size:10px;color:#888\">\u{1F464} '+ch+' \u00B7 \u2B50 '+score+'\u5206 \u00B7 \u{1F4CB} '+scenes+'\u573A\u666F \u00B7 '+tags+'</div>';
    if(!sb.length){h+='<div style=\"text-align:center;padding:40px;color:#555\">\u6682\u65E0\u5206\u955C\u6570\u636E</div>';}
    sb.forEach(function(sc,i){
      var tone=sc.emotion||'';
      var accent='#3b82f6';
      if(/爆|怒|杀|打|冲|愤|激烈/.test(tone))accent='#ff6b6b';
      else if(/悲|哭|哀|伤|泪/.test(tone))accent='#a78bfa';
      else if(/爱|情|温|柔|甜/.test(tone))accent='#fb7185';
      else if(/恐|惊|怕|慌|逃|急/.test(tone))accent='#fbbf24';
      else if(/静|冷|孤|沉|思|默/.test(tone))accent='#94a3b8';
      h+='<div style=\"margin-bottom:8px;padding:10px 14px;border-radius:8px;background:rgba(255,255,255,.02);border-left:3px solid '+accent+'\">';
      h+='<div style=\"display:flex;gap:8px;margin-bottom:4px;align-items:baseline\"><span style=\"font-size:10px;color:'+accent+';font-weight:700\">\u955C'+(i+1)+'</span><span style=\"font-size:9px;color:#fbbf24\">'+(sc.act||'')+'</span><span style=\"font-size:9px;color:#666\">'+(sc.duration||'')+'</span></div>';
      h+='<div style=\"font-size:12px;color:#ccc;line-height:1.7\">'+(sc.description||'')+'</div>';
      if(tone)h+='<div style=\"font-size:9px;color:#888;margin-top:3px\">\u{1F3AD} '+tone+'</div>';
      if(sc.dialogue)h+='<div style=\"font-size:10px;color:#aaa;font-style:italic;margin-top:3px;padding-left:8px\">\u201C'+sc.dialogue+'\u201D</div>';
      h+='</div>';
    });
    content.innerHTML=h;
  }).catch(function(e){
    content.innerHTML='<div style=\"color:#ef4444;text-align:center;padding:40px\">\u52A0\u8F7D\u5931\u8D25: '+e.message+'</div>';
  });
}

// @@FUNC: renderScriptBrowserPreview
function renderScriptBrowserPreview(epNum){
  var content=document.getElementById('script-browser-content');
  if(!content)return;
  var epId=String(epNum).padStart(2,'0');
  content.innerHTML='<div style=\"text-align:center;padding:40px;color:#888\"><span class=\"loading\">\u52A0\u8F7D\u9884\u89C8...</span></div>';
  fetch('/api/script/'+epId+'/export?format=html').then(function(r){return r.text();}).then(function(html){
    var ifr=document.createElement('iframe');
    ifr.style.cssText='width:100%;height:100%;min-height:600px;border:none;background:#fff;border-radius:4px';
    content.innerHTML='';
    content.appendChild(ifr);
    var doc=ifr.contentDocument||ifr.contentWindow.document;
    doc.open();doc.write(html);doc.close();
  }).catch(function(e){
    content.innerHTML='<div style=\"color:#ef4444;text-align:center;padding:40px\">\u9884\u89C8\u52A0\u8F7D\u5931\u8D25</div>';
  });
}

// @@FUNC: showScriptSummary
function showScriptSummary(){
  var existing=document.getElementById('script-summary-dlg');
  if(existing)existing.remove();
  var dlg=document.createElement('div');
  dlg.id='script-summary-dlg';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:600px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><div style="font-size:14px;font-weight:600">📋 剧本摘要</div><span onclick="this.parentElement.parentElement.remove()" style="cursor:pointer;font-size:20px;color:#555">&times;</span></div><div id="script-summary-body" style="font-size:11px;color:#888"><span class="loading">加载中...</span></div>';
  document.body.appendChild(dlg);
  fetch('/api/script').then(function(r){return r.json();}).then(function(d){
    var eps = d.episodes || d || [];
    if(!Array.isArray(eps)) eps = Object.values(eps)||[];
    var body = document.getElementById('script-summary-body');
    if(!body) return;
    var html = '';
    eps.forEach(function(ep,i){
      var title = ep.title||ep.name||'第'+(i+1)+'集';
      var score = ep.score||'—';
      var scenes = ep.scene_count||ep.scenes||0;
      var tags = (ep.tags||[]).join(' · ')||'';
      html += '<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #222">';
      html += '<span style="min-width:40px;color:#60a5fa;font-weight:600">EP'+(i+1+'').padStart(2,'0')+'</span>';
      html += '<span style="flex:1;color:#e4e6eb">'+title+'</span>';
      html += '<span style="font-size:9px;color:#888">'+scenes+'场景 · 评分'+score+'</span>';
      html += '<span style="font-size:9px;color:#555">'+tags+'</span>';
      html += '<span style="font-size:9px;cursor:pointer;color:#60a5fa" onclick="showScriptDetail('+(i+1)+');this.closest(&quot;#script-summary-dlg&quot;).remove()">\ud83d\udd0d</span>';
      html += '</div>';
    });
    body.innerHTML = html || '<div style="text-align:center;padding:20px">暂无剧本数据</div>';
  }).catch(function(e){
    var body = document.getElementById('script-summary-body');
    if(body) body.innerHTML = '<div style="color:#ef4444">加载失败: '+e.message+'</div>';
  });
}

// @@FUNC: showScriptDetail
function showScriptDetail(epNum){
  var existing=document.getElementById('script-detail-dlg');
  if(existing)existing.remove();
  var dlg=document.createElement('div');
  dlg.id='script-detail-dlg';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:700px;width:90%;max-height:85vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><div style="font-size:14px;font-weight:600">🔍 EP'+String(epNum).padStart(2,'0')+' 剧本详情</div><span onclick="this.parentElement.parentElement.remove()" style="cursor:pointer;font-size:20px;color:#555">&times;</span></div><div id="script-detail-body"><span class="loading">加载中...</span></div>';
  document.body.appendChild(dlg);
  fetch('/api/script/'+epNum).then(function(r){return r.json();}).then(function(data){
    var body=document.getElementById('script-detail-body');
    if(!body) return;
    var html='';
    html+='<div style="margin-bottom:10px"><span style="font-size:12px;font-weight:600;color:#e4e6eb">'+(data.title||'')+'</span>';
    if(data.score) html+=' · <span style="font-size:10px;color:#22c55e">评分 '+data.score+'/10</span>';
    html+='</div>';
    var sb=data.storyboard||data.scenes||[];
    if(!Array.isArray(sb)) sb=Object.values(sb)||[];
    sb.forEach(function(sc){
      html+='<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:6px;padding:8px 10px;margin-bottom:6px">';
      html+='<div style="display:flex;gap:6px;margin-bottom:4px"><span style="font-size:9px;color:#60a5fa;font-weight:600;min-width:30px">#'+(sc.seq||'—')+'</span><span style="font-size:10px;color:#fbbf24;font-weight:600">'+(sc.act||'')+'</span><span style="font-size:9px;color:#555">'+(sc.duration||'')+'</span></div>';
      html+='<div style="font-size:10px;color:#ccc;margin-bottom:2px">'+(sc.description||'')+'</div>';
      if(sc.emotion) html+='<div style="font-size:9px;color:#888">情感: '+sc.emotion+'</div>';
      if(sc.dialogue) html+='<div style="font-size:9px;color:#aaa;font-style:italic">对白: '+sc.dialogue+'</div>';
      html+='</div>';
    });
    body.innerHTML=html||'<div style="text-align:center;padding:20px;color:#555">无分镜数据</div>';
  }).catch(function(e){
    var body=document.getElementById('script-detail-body');
    if(body) body.innerHTML='<div style="color:#ef4444">加载失败: '+e.message+'</div>';
  });
}

// @@FUNC: previewScriptHTML
function previewScriptHTML(epNum){
  var epId=String(epNum||1).padStart(2,"0");
  var existing=document.getElementById("script-preview-dlg");
  if(existing)existing.remove();
  var dlg=document.createElement("div");
  dlg.id="script-preview-dlg";
  dlg.style.cssText="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);z-index:1000;display:flex;flex-direction:column";
  dlg.innerHTML=["<div style=\"flex:0 0 auto;display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:#1a1d27;border-bottom:1px solid rgba(59,130,246,.3)\">",
    "<div style=\"font-size:14px;font-weight:600;color:#e4e6eb\">📥 EP"+epId+" HTML预览</div>",
    "<div>",
    "<button class=\"mini-btn\" id=\"dl-dlbtn\">⬇ 下载</button>",
    "<span onclick=\"this.closest('#script-preview-dlg').remove()\" style=\"cursor:pointer;font-size:20px;color:#555;margin-left:8px\">&times;</span>",
    "</div></div>",
    "<div id=\"script-preview-body\" style=\"flex:1;overflow:hidden;background:#fff\"><span class=\"loading\">渲染HTML...</span></div>"].join("");
  document.body.appendChild(dlg);
  setTimeout(function(){var b=document.getElementById("dl-dlbtn");if(b)b.onclick=function(){window.open("/api/script/"+epId+"/export?format=html")};},0);
  fetch("/api/script/"+epId+"/export?format=html").then(function(r){return r.text();}).then(function(html){
    var body=document.getElementById("script-preview-body");
    if(!body)return;
    var ifr=document.createElement("iframe");
    ifr.style.cssText="width:100%;height:100%;border:none";
    body.innerHTML="";
    body.appendChild(ifr);
    var doc=ifr.contentDocument||ifr.contentWindow.document;
    doc.open();doc.write(html);doc.close();
  }).catch(function(e){
    fetch("/api/script/"+epId).then(function(r){return r.json();}).then(function(data){
      var body=document.getElementById("script-preview-body");
      if(!body)return;
      var sb=data.storyboard||data.scenes||[];
      var title=data.title||"EP"+epId;
      var score=data.score||"";
      var tags=(data.tags||[]).join(", ")||"";
      var ch=data.main_character||"";
      var h=["<div style=\"font-family:PingFang SC,serif;padding:24px;color:#1a1a2e;max-width:800px;margin:0 auto\">",
        "<h1 style=\"text-align:center;color:#e94560;border-bottom:2px solid #e94560;padding-bottom:10px;margin-bottom:8px\">"+title+"</h1>",
        "<div style=\"text-align:center;color:#888;font-size:12px;margin-bottom:20px\">"+ch+(score?" \u00B7 "+score+"\u5206":"")+(tags?" \u00B7 "+tags:"")+"</div>"];
      if(sb.length){
        h.push("<h3 style=\"color:#e94560;border-left:3px solid #e94560;padding-left:10px\">分镜脚本</h3>");
        sb.forEach(function(sc,i){
          var tone=sc.emotion||"";
          var toneColor="#16213e";var accentColor="#00d2ff";
          if(/爆|怒|杀|打|冲|战|愤|激烈/.test(tone)){toneColor="#2d1111";accentColor="#ff6b6b";}
          else if(/悲|哀|哭|痛|伤|泪/.test(tone)){toneColor="#1e1e2d";accentColor="#a78bfa";}
          else if(/爱|情|温|柔|甜|吻|抱/.test(tone)){toneColor="#2d1b1b";accentColor="#fb7185";}
          else if(/恐|惊|怕|慌|逃|急/.test(tone)){toneColor="#2d1b1e";accentColor="#fbbf24";}
          else if(/静|冷|孤|沉|思|默/.test(tone)){toneColor="#1a1e2d";accentColor="#94a3b8";}
          else if(/疑|问|谜/.test(tone)){toneColor="#1e1e2d";accentColor="#a78bfa";}
          h.push("<div style=\"background:"+toneColor+"!important;border-radius:8px;padding:12px;margin-bottom:8px;border-left:4px solid "+accentColor+"\">");
          h.push("<div style=\"display:flex;gap:8px;margin-bottom:4px\"><span style=\"font-size:10px;color:"+accentColor+";font-weight:700\">镜"+(i+1)+"</span><span style=\"font-size:10px;color:#fbbf24\">"+(sc.act||"")+"</span><span style=\"font-size:9px;color:#888\">"+(sc.duration||"")+"</span></div>");
          h.push("<div style=\"font-size:13px;color:#e0e0e0;line-height:1.7\">"+(sc.description||"")+"</div>");
          if(tone)h.push("<div style=\"font-size:10px;color:"+accentColor+";margin-top:4px\">"+(sc.emotion||"")+"</div>");
          if(sc.dialogue)h.push("<div style=\"font-size:12px;color:#aaa;font-style:italic;margin-top:4px;padding-left:8px\">\u201C"+sc.dialogue+"\u201D</div>");
          h.push("</div>");
        });
      }
      h.push("<div style=\"text-align:center;padding:20px;color:#888;font-size:10px\">Agentic OS v3.7 \u00B7 水浒传AI短剧</div>");
      h.push("</div>");
      body.innerHTML=h.join("");
      var downloadBtn=document.getElementById("dl-dlbtn");
      if(downloadBtn)downloadBtn.onclick=function(){
        var blob=new Blob(["<html><head><meta charset=utf-8><title>"+title+"</title></head><body>"+h.join("")+"</body></html>"],{type:"text/html"});
        var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="ep"+epId+"-preview.html";a.click();
      };
    }).catch(function(e2){
      if(body)body.innerHTML=["<div style=\"color:#ef4444;text-align:center;padding:40px\">","预览失败","</div>"].join("");
    });
  });
}

// @@FUNC: editSB
function editSB(epNum,seq){
  const el=document.getElementById('edit-'+epNum+'-'+seq);
  if(!el)return;
  el.classList.add('show');
}

// @@FUNC: saveSBEdit
async function saveSBEdit(epNum,seq){
  const descEl=document.getElementById('desc-'+epNum+'-'+seq);
  const editEl=document.getElementById('edit-'+epNum+'-'+seq);
  if(!descEl||!editEl)return;
  const newDesc=descEl.value;
  try{
    const r=await fetch('/api/script/'+parseInt(epNum),{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({seq:parseInt(seq),description:newDesc})
    });
    if(r.ok){
      toastMsg('分镜已更新: 第'+epNum+'集 #'+seq);
      editEl.classList.remove('show');
      const sbCard=editEl.closest('.sb-card');
      if(sbCard){
        const descDiv=sbCard.querySelector('.sb-desc');
        if(descDiv)descDiv.textContent=newDesc;
      }
    }else{toastMsg('保存失败')}
  }catch(e){toastMsg('保存失败: '+e.message)}
}

// @@FUNC: cancelSBEdit
function cancelSBEdit(epNum,seq){
  const el=document.getElementById('edit-'+epNum+'-'+seq);
  if(el)el.classList.remove('show');
}

// @@FUNC: downloadScript
function downloadScript(epNum,fmt){
  const ep=parseInt(epNum);
  const url='/api/download?name=ep'+String(ep).padStart(2,'0')+'.'+fmt;
  window.open(url,'_blank');
}

// @@FUNC: previewScriptInline
async function previewScriptInline(epNum){
  const sectionId='inline-script-'+epNum;
  const body=document.getElementById(sectionId);
  if(!body) return;
  const isOpen=body.classList.contains('accordion-expanded');
  toggleSection(sectionId);
  if(isOpen) return;
  const editor=document.getElementById('script-editor-'+epNum);
  if(!editor) return;
  try{
    var r=await fetch('/api/download?name=ep'+String(epNum).padStart(2,'0')+'.txt');
    var text=await r.text();
    editor.value=text;
  }catch(e){editor.value='加载失败: '+e.message;return;}
}

// @@FUNC: saveInlineScript
async function saveInlineScript(epNum){
  var editor=document.getElementById('script-editor-'+epNum);
  if(!editor||!editor.value.trim()) return;
  try{
    var r=await fetch('/api/script/'+parseInt(epNum),{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({content:editor.value})});
    if(r.ok) toastMsg('✅ 剧本已保存',2000);
  }catch(e){toastMsg('保存失败: '+e.message,2000);}
}

// @@FUNC: showReReviewDialog
function showReReviewDialog(epNum, oldScore){
  var existing=document.getElementById('rereview-dialog');
  if(existing)existing.remove();
  var dlg=document.createElement('div');
  dlg.id='rereview-dialog';
  dlg.style.cssText='position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1d27;border:1px solid rgba(59,130,246,.3);border-radius:12px;padding:20px;z-index:500;max-width:380px;width:80%;box-shadow:0 8px 32px rgba(0,0,0,.6)';
  dlg.innerHTML='<div style="font-size:13px;font-weight:600;margin-bottom:10px">✅ 剧本已保存</div>'+
    (oldScore!==null?'<div style="font-size:10px;color:#888;margin-bottom:8px">上次得分: <strong style="color:'+(oldScore>=6?'#22c55e':oldScore>=4?'#f59e0b':'#ef4444')+'">'+oldScore+'/10</strong></div>':'')+
    '<div style="font-size:10px;color:#888;margin-bottom:14px">是否立即触发AI重新审核？新旧得分将自动对比。</div>'+
    '<div style="display:flex;gap:8px"><button class="btn btn-p" id="rereview-btn-confirm">✅ 重新审核</button><button class="btn-secondary" id="rereview-btn-skip">⏸️ 稍后</button></div>';
  document.body.appendChild(dlg);
  return new Promise(function(resolve){
    document.getElementById('rereview-btn-confirm').onclick=function(){dlg.remove();resolve(true);};
    document.getElementById('rereview-btn-skip').onclick=function(){dlg.remove();resolve(false);};
  });
}

// @@FUNC: startEditSB
function startEditSB(epNum,seq){
  const bodyEl=document.getElementById('sb-body-'+epNum+'-'+seq);
  const btn=document.getElementById('sb-editbtn-'+epNum+'-'+seq);
  if(!bodyEl||!btn)return;
  const actEl=bodyEl.querySelector('.sb-act');
  const nameEl=bodyEl.querySelector('.sb-name');
  const descEl=bodyEl.querySelector('.sb-desc');
  const dialEl=bodyEl.querySelector('.sb-dialogue');
  _sbUndo[epNum+'-'+seq]={
    act:actEl?actEl.textContent:'',
    name:nameEl?nameEl.textContent:'',
    desc:descEl?descEl.textContent:'',
    dialogue:dialEl?dialEl.textContent:''
  };
  btn.textContent='↩ 撤销';
  btn.onclick=()=>undoSB(epNum,seq);
  bodyEl.innerHTML=`<div class="inline-edit show">
    <textarea id="sb-new-act" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px" placeholder="动作">${_sbUndo[epNum+'-'+seq].act}</textarea>
    <textarea id="sb-new-name" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px" placeholder="角色">${_sbUndo[epNum+'-'+seq].name}</textarea>
    <textarea id="sb-new-desc" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px;min-height:40px" placeholder="场景">${_sbUndo[epNum+'-'+seq].desc}</textarea>
    <textarea id="sb-new-dialogue" style="width:100%;background:#111;border:1px solid #333;color:#e4e6eb;padding:4px;border-radius:4px;font-size:10px;min-height:30px" placeholder="台词">${_sbUndo[epNum+'-'+seq].dialogue}</textarea>
    <div class="edit-btns">
      <button class="mini-btn" onclick="saveSB('${epNum}',${seq})">保存</button>
      <button class="mini-btn" onclick="cancelSB('${epNum}',${seq})">取消</button>
    </div>
  </div>`;
}

// @@FUNC: loadStoryboard
async function loadStoryboard(epNum){
  var el = document.getElementById('sb-' + epNum);
  if (!el) return;
  try {
    var r = await fetch('/api/script/' + epNum);
    var d = await r.json();
    var shots = d.storyboard || d.shots || [];
    if (!shots.length) { el.innerHTML = '<span style="color:#555;font-size:10px">无分镜</span>'; return; }
    // Fetch character video prompts for scheme preview
    var charName = d.main_character || d.character || '';
    var videoPrompts = {};
    if (charName) {
      try {
        var cr = await fetch('/api/character/' + charName);
        var cd = await cr.json();
        var design = cd.design || cd;
        videoPrompts = design.video_prompts || {};
      } catch(e) {}
    }
    var schemes = ['方案一','方案二','方案三'];
    var h = '';
    shots.forEach(function(s, i) {
      var seq = s.id || s.seq || (i + 1);
      var act = s.act || s.act_name || '';
      var name = s.character || s.char_name || d.character || '';
      var desc = s.narration || s.description || s.scene || '';
      var dialogue = s.dialogue || s.line || '';
      var sid = epNum + '-' + seq;
      // Like/Dislike state from localStorage
      var fb = localStorage.getItem('sb_fb_' + sid);
      var liked = fb === 'like', disliked = fb === 'dislike';
      h += '<div class="sb-card" style="margin-bottom:8px">';
      h += '<div class="sb-seq">' + seq + '</div>';
      h += '<div class="sb-body" id="sb-body-' + sid + '">';
      if (act) h += '<div class="sb-act">' + act + '</div>';
      if (name) h += '<div class="sb-name">' + name + '</div>';
      if (desc) h += '<div class="sb-desc">' + desc + '</div>';
      if (dialogue) h += '<div class="sb-dialogue">' + dialogue + '</div>';
      // Scheme buttons + preview panel
      h += '<div style="display:flex;gap:4px;margin-top:6px;flex-wrap:wrap;align-items:center">';
      schemes.forEach(function(scheme) {
        var vp = videoPrompts[scheme] || {};
        var title = vp.title || '';
        var prompt = vp.prompt || vp['简练版'] || '';
        var hasData = !!prompt;
        h += '<button class="mini-btn scheme-btn" id="schbtn-' + sid + '-' + scheme + '" '
          + 'onclick="toggleSchemePreview(\'' + sid + '\',\'' + scheme + '\')" '
          + 'data-prompt="' + (prompt ? prompt.replace(/"/g,'&quot;').substring(0,120) : '') + '" '
          + 'data-title="' + (title ? title.replace(/"/g,'&quot;') : '') + '" '
          + 'style="' + (hasData ? '' : 'opacity:.4') + '">🎬 ' + scheme + (title ? '<span style="font-size:7px;display:block;color:#666">' + title + '</span>' : '') + '</button>';
      });
      // Like/Dislike
      h += '<button class="mini-btn sb-fb-btn" id="sblike-' + sid + '" onclick="toggleSBFeedback(\'' + sid + '\',\'like\',\'' + charName + '\')" style="color:' + (liked ? '#22c55e' : '#666') + ';border-color:' + (liked ? '#22c55e' : '#333') + ';margin-left:4px">' + (liked ? '❤️' : '👍') + '</button>';
      h += '<button class="mini-btn sb-fb-btn" id="sbdislike-' + sid + '" onclick="toggleSBFeedback(\'' + sid + '\',\'dislike\',\'' + charName + '\')" style="color:' + (disliked ? '#ef4444' : '#666') + ';border-color:' + (disliked ? '#ef4444' : '#333') + '">' + (disliked ? '💔' : '👎') + '</button>';
      h += '<button class="mini-btn" id="sb-editbtn-' + sid + '" onclick="startEditSB(\'' + epNum + '\',' + seq + ')">✏ 编辑</button>';
      h += '</div>';
      // Scheme preview panel (hidden by default)
      h += '<div class="scheme-preview" id="schpreview-' + sid + '" style="display:none;background:rgba(0,0,0,.2);border-radius:4px;padding:8px;margin-top:4px;font-size:9px;color:#888"></div>';
      h += '</div></div>';
    });
    el.innerHTML = h;
  } catch(e) {
    el.innerHTML = '<span style="color:#ef4444;font-size:10px">加载失败: ' + e.message + '</span>';
  }
}

// @@FUNC: toggleSchemePreview
function toggleSchemePreview(sid, scheme){
  var cont = document.getElementById('schpreview-' + sid);
  var btn = document.getElementById('schbtn-' + sid + '-' + scheme);
  var title = btn.getAttribute('data-title') || '';
  var prompt = btn.getAttribute('data-prompt') || '';
  if (!cont) return;
  // Close if already open for this scheme
  if (cont.getAttribute('data-active') === scheme) {
    cont.style.display = 'none';
    cont.removeAttribute('data-active');
    return;
  }
  cont.setAttribute('data-active', scheme);
  cont.style.display = 'block';
  cont.innerHTML = '<div style="font-weight:600;color:#93c5fd;margin-bottom:4px">' + scheme + (title ? ': ' + title : '') + '</div>'
    + '<div style="color:#ccc;white-space:pre-wrap;line-height:1.5;max-height:120px;overflow-y:auto">' + (prompt || '—') + '</div>'
    + '<div style="margin-top:6px;display:flex;gap:4px">'
    + '<button class="mini-btn" style="color:#22c55e" onclick="toggleSBFeedback(\'' + sid + '\',\'like\')">❤️</button>'
    + '<button class="mini-btn" style="color:#ef4444" onclick="toggleSBFeedback(\'' + sid + '\',\'dislike\')">💔</button>'
    + '</div>';
}

// @@FUNC: toggleSBFeedback
function toggleSBFeedback(sid, type, charName){
  var likeBtn = document.getElementById('sblike-' + sid);
  var disBtn = document.getElementById('sbdislike-' + sid);
  var current = localStorage.getItem('sb_fb_' + sid);
  if (current === type) {
    localStorage.removeItem('sb_fb_' + sid);
    if (likeBtn) { likeBtn.style.color = '#666'; likeBtn.style.borderColor = '#333'; likeBtn.textContent = '👍'; }
    if (disBtn) { disBtn.style.color = '#666'; disBtn.style.borderColor = '#333'; disBtn.textContent = '👎'; }
    toastMsg('已清除反馈', 1000);
  } else {
    localStorage.setItem('sb_fb_' + sid, type);
    if (likeBtn) { likeBtn.style.color = type === 'like' ? '#22c55e' : '#666'; likeBtn.style.borderColor = type === 'like' ? '#22c55e' : '#333'; likeBtn.textContent = type === 'like' ? '❤️' : '👍'; }
    if (disBtn) { disBtn.style.color = type === 'dislike' ? '#ef4444' : '#666'; disBtn.style.borderColor = type === 'dislike' ? '#ef4444' : '#333'; disBtn.textContent = type === 'dislike' ? '💔' : '👎'; }
    toastMsg(type === 'like' ? '❤️ 标记喜欢' : '💔 标记不喜欢', 1500);
    // Log feedback
    try {
      var ts = new Date().toISOString();
      var fb = JSON.parse(localStorage.getItem('sb_feedback_log') || '[]');
      fb.push({sid: sid, type: type, character: charName || '', timestamp: ts});
      if (fb.length > 200) fb = fb.slice(-100);
      localStorage.setItem('sb_feedback_log', JSON.stringify(fb));
    } catch(e) {}
  }
}

// @@FUNC: undoSB
function undoSB(epNum,seq){
  const u=_sbUndo[epNum+'-'+seq];if(!u)return;
  const bodyEl=document.getElementById('sb-body-'+epNum+'-'+seq);
  const btn=document.getElementById('sb-editbtn-'+epNum+'-'+seq);
  if(bodyEl)bodyEl.innerHTML=`<div class="sb-act">${u.act}</div><div class="sb-name">${u.name}</div><div class="sb-desc">${u.desc}</div>${u.dialogue?`<div class="sb-dialogue">${u.dialogue}</div>`:''}`;
  if(btn){btn.textContent='✏ 编辑';btn.onclick=()=>startEditSB(epNum,seq);}
  delete _sbUndo[epNum+'-'+seq];
  toastMsg('已撤销',1500);
}

// @@FUNC: cancelSB
function cancelSB(epNum,seq){
  const btn=document.getElementById('sb-editbtn-'+epNum+'-'+seq);
  if(btn){btn.textContent='✏ 编辑';btn.onclick=()=>startEditSB(epNum,seq);}
  delete _sbUndo[epNum+'-'+seq];
  loadStoryboard(epNum);
}

// @@FUNC: saveSB
async function saveSB(epNum,seq){
  const act=document.getElementById('sb-new-act')?.value||'';
  const name=document.getElementById('sb-new-name')?.value||'';
  const desc=document.getElementById('sb-new-desc')?.value||'';
  const dialogue=document.getElementById('sb-new-dialogue')?.value||'';
  try{
    const r=await fetch('/api/script/'+epNum,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenes:[{seq,act,name,desc,dialogue}]})});
    if(r.ok){toastMsg('分镜已更新: 第'+epNum+'集 #'+seq,2000);delete _sbUndo[epNum+'-'+seq];loadStoryboard(epNum);}
    else toastMsg('保存失败',2000);
  }catch(e){toastMsg('保存失败: '+e.message,2000)}
}

