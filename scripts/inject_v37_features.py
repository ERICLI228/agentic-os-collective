#!/usr/bin/env python3
"""Inject v3.7 features into task_board.html: pipeline monitor upgrade, asset panel, loading states."""
import os

TB = os.path.expanduser("~/agentic-os-collective/dashboard/task_board.html")
with open(TB) as f:
    html = f.read()

# 1. Pipeline monitor auto-refresh (already done above)
# 2. Add "资产" button after 画廊 link
old_asset_btn = '<a href="/gallery" class="compare-toggle" style="text-decoration:none" target="_blank">🖼 画廊</a>'
new_asset_btn = old_asset_btn + '\n  <span class="compare-toggle" id="assetToggle" onclick="toggleAssetPanel()" style="position:relative">📦 资产</span>'
if old_asset_btn in html and new_asset_btn not in html:
    html = html.replace(old_asset_btn, new_asset_btn)
    print("Added asset button")

# 3. Add asset panel HTML before </body>
asset_html = '''<!-- v3.7: Asset Panel -->
<div class="asset-panel" id="assetPanel">
  <div class="asset-panel-hdr"><span>📦 资产管理</span><span onclick="toggleAssetPanel()" style="cursor:pointer;font-size:16px">&times;</span></div>
  <div class="asset-tabs" id="assetTabs">
    <span class="asset-tab active" onclick="switchAssetTab(this,'all')">全部</span>
    <span class="asset-tab" onclick="switchAssetTab(this,'render')">角色图</span>
    <span class="asset-tab" onclick="switchAssetTab(this,'script')">剧本</span>
    <span class="asset-tab" onclick="switchAssetTab(this,'episode')">剧集</span>
  </div>
  <div class="asset-panel-body" id="assetBody"><div class="loading"><span class="spinner"></span>加载资产...</div></div>
</div>
<div class="asset-overlay" id="assetOverlay" onclick="toggleAssetPanel()"></div>
'''
if '</body>' in html and 'assetPanel' not in html:
    html = html.replace('</body>', asset_html + '\n</body>')
    print("Added asset panel HTML")

# 4. Add asset panel CSS before mark.search-hl
asset_css = '''
/* v3.7: Asset panel slide-out */
.asset-panel{position:fixed;top:0;right:0;width:380px;height:100vh;background:#1a1d27;z-index:1000;box-shadow:-4px 0 20px rgba(0,0,0,.5);transform:translateX(100%);transition:transform .25s ease;display:flex;flex-direction:column}
.asset-panel.open{transform:translateX(0)}
.asset-panel-hdr{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;border-bottom:1px solid #222;font-size:13px;font-weight:600}
.asset-panel-body{flex:1;overflow-y:auto;padding:8px 12px}
.asset-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:999;display:none}
.asset-overlay.on{display:block}
.asset-item{display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:4px;margin:3px 0;font-size:10px;background:rgba(255,255,255,.02);border:1px solid #222}
.asset-item:hover{background:rgba(74,158,255,.05);border-color:rgba(74,158,255,.15)}
.asset-item .thumb{width:36px;height:48px;border-radius:3px;object-fit:cover;background:#111;flex-shrink:0}
.asset-item .info{flex:1;min-width:0}
.asset-item .name{color:#c4d4e8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.asset-item .meta{color:#666;font-size:8px}
.asset-item .dl-btn{font-size:9px;padding:2px 6px;border-radius:3px;border:1px solid #333;cursor:pointer;color:#888;background:transparent}
.asset-item .dl-btn:hover{background:#2563eb;color:#fff;border-color:#2563eb}
.asset-tabs{display:flex;gap:4px;padding:6px 12px;border-bottom:1px solid #222}
.asset-tab{padding:3px 10px;border-radius:4px;font-size:10px;cursor:pointer;border:1px solid #333;color:#888;background:transparent}
.asset-tab.active{background:#2563eb;border-color:#2563eb;color:#fff}
'''
if 'mark.search-hl' in html and 'asset-panel' not in html:
    html = html.replace('mark.search-hl{background:#fbbf24;color:#000;border-radius:2px;padding:0 1px}',
                         asset_css + '\nmark.search-hl{background:#fbbf24;color:#000;border-radius:2px;padding:0 1px}')
    print("Added asset panel CSS")

# 5. Add toggleAssetPanel and loadAssetPanel functions before the last </script>
toggle_js = '''
function toggleAssetPanel(){
  const p=document.getElementById('assetPanel'),o=document.getElementById('assetOverlay');
  if(p.classList.contains('open')){p.classList.remove('open');o.classList.remove('on')}
  else{p.classList.add('open');o.classList.add('on');loadAssetPanel()}
}
function switchAssetTab(el,type){
  document.querySelectorAll('#assetTabs .asset-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');loadAssetPanel(type);
}
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
    else if(it.type==='script')h+='<div class="asset-item"><div class="info"><div class="name">📄 '+it.name+'</div><div class="meta">剧本</div></div><button class="dl-btn" onclick="window.open(\'/api/script/'+it.episode+'\')">📥</button></div>';
    else h+='<div class="asset-item"><div class="info"><div class="name">🎬 '+it.name+'</div><div class="meta">'+it.shots+'个分镜</div></div></div>';
  });
  body.innerHTML=count?'':'<div style="color:#555;text-align:center;padding:20px;font-size:11px">没有'+type+'类资产</div>'+h;
}
'''
last_script = html.rfind('</script>')
if last_script != -1 and 'function toggleAssetPanel()' not in html:
    html = html[:last_script] + toggle_js + html[last_script:]
    print("Added asset panel JS")

with open(TB, 'w') as f:
    f.write(html)
print("Done")

# Quick verification
with open(TB) as f:
    h = f.read()
print(f"assetToggle: {'assetToggle' in h}")
print(f"toggleAssetPanel: {'toggleAssetPanel' in h}")
print(f"asset-panel: {'asset-panel' in h}")
print(f"svcMonitor interval: {'setInterval(updatePipelineMonitor' in h}")
