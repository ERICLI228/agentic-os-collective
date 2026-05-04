// === summary.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: render
function render(){
  let f=all.filter(m=>m.pipeline===cur);

// P1-12: apply search & filter
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
  let h='';
  // P1-12: filter indicator
  if(searchQ||filterSt!=='all'){
    const total=all.filter(m=>m.pipeline===cur).length;
    h+=`<div style="font-size:9px;color:#555;padding:2px 8px">筛选: ${f.length}/${total} 项</div>`;
  }

  const g={};
  f.forEach(m=>{const tid=m.task_id||'_';if(!g[tid])g[tid]=[];g[tid].push(m)});
  const tl={'TK-MS0-GATE':'MS-0 采集门禁','TK-SELECTION':'选品与市场判断','TK-LOCALIZE':'本地化与上架准备',
    'TK-PUBLISH':'发布与日报','TK-DM-PREP':'前期策划','TK-DM-PROD':'制片制作','TK-DM-DIST':'发布分发','_':'未分组'};

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

// @@FUNC: renderSummary
function renderSummary(){
  let f=all.filter(m=>m.pipeline===cur);
  if(searchQ) f=f.filter(m=>(m.ms_id+' '+(m.name||'')+' '+(m.task_id||'')).toLowerCase().includes(searchQ));
  if(filterSt!=='all') f=f.filter(m=>m.status===filterSt);
  const w=f.filter(m=>m.status=='waiting_approval');
  const ld=lastData||{};
  const orders=ld.orders||{total_orders:0,total_revenue:0,in_transit:0};
  const health=ld.shop_health||{total:0,healthy:0,warning:0,critical:0};
  const decs=ld.decisions||{total:0,approved:0,pending:0,rejected:0};
  const dm=ld.dm||{stats:{}};
  const tk=ld.tk||{stats:{}};
  let h='<div style="max-width:700px;margin:0 auto;">';

  // KPI Cards
  h+='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num">'+orders.total_orders+'</div><div class="lbl">总订单</div></div>';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num">'+orders.total_revenue+'</div><div class="lbl">总收入 ¥</div></div>';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num">'+orders.in_transit+'</div><div class="lbl">运输中</div></div>';
  h+='<div class="stat" style="flex:1;min-width:110px"><div class="num" style="color:'+(health.healthy>0?'#22c55e':health.critical>0?'#ef4444':'#f59e0b')+'">'+health.healthy+'/'+health.total+'</div><div class="lbl">店铺健康</div></div>';
  h+='</div>';

  // Pipeline progress
  const tkDone=tk.stats?.completed||0; const tkTotal=tk.stats?.total_milestones||0;
  const dmDone=dm.stats?.completed||0; const dmTotal=dm.stats?.total_milestones||0;
  const tkPct=tkTotal?Math.round(tkDone/tkTotal*100):0;
  const dmPct=dmTotal?Math.round(dmDone/dmTotal*100):0;
  h+='<div style="display:flex;gap:8px;margin-bottom:10px">';
  h+='<div style="flex:1;background:#1a1d27;border-radius:6px;padding:10px">';
  h+='<div style="font-size:11px;color:#888;margin-bottom:4px">TK运营进度</div>';
  h+='<div style="display:flex;align-items:center;gap:6px"><div class="pbar" style="flex:1"><div class="pfill" style="width:'+tkPct+'%;background:#3b82f6"></div></div><span style="font-size:11px;color:#93c5fd">'+tkDone+'/'+tkTotal+'</span></div></div>';
  h+='<div style="flex:1;background:#1a1d27;border-radius:6px;padding:10px">';
  h+='<div style="font-size:11px;color:#888;margin-bottom:4px">数字短剧进度</div>';
  h+='<div style="display:flex;align-items:center;gap:6px"><div class="pbar" style="flex:1"><div class="pfill" style="width:'+dmPct+'%;background:#8b5cf6"></div></div><span style="font-size:11px;color:#a78bfa">'+dmDone+'/'+dmTotal+'</span></div></div>';
  h+='</div>';

  // Decision stats
  h+='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num" style="color:#22c55e">'+decs.approved+'</div><div class="lbl">已批准</div></div>';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num" style="color:#f59e0b">'+decs.pending+'</div><div class="lbl">待决策</div></div>';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num" style="color:#ef4444">'+decs.rejected+'</div><div class="lbl">已驳回</div></div>';
  h+='<div class="stat" style="flex:1;min-width:60px"><div class="num">'+decs.total+'</div><div class="lbl">总决策</div></div>';
  h+='</div>';

  // Decision panel
  h+='<h3 style="color:#888;margin-bottom:8px;font-size:13px;">&#9873; 待决策项</h3>';
  if(!w.length){h+='<div style="color:#444;padding:16px;text-align:center;background:#1a1d27;border-radius:6px;margin-bottom:10px">无待决策项</div>'}
  else w.forEach(m=>{
    h+='<div style="background:#1f1a0f;border-left:3px solid #f59e0b;border-radius:6px;padding:12px;margin:8px 0;font-size:12px;">';
    h+='<b style="color:#fbbf24">&#9873; '+m.ms_id+' '+m.name+'</b><div style="color:#888;font-size:10px;margin-top:4px">'+(m.note||'')+'</div>';
    h+='<div style="margin-top:8px">';
    [{a:'approved',l:'&#10003; 批准',c:'btn-s'},{a:'modify',l:'&#9998; 修改',c:'btn-w'},{a:'rejected',l:'&#10007; 驳回',c:'btn-d'}].forEach(o=>{
      h+='<button class="btn '+o.c+'" onclick="event.stopPropagation();decide(\''+m.ms_id+'\',\''+o.a+'\')">'+o.l+'</button> ';
    });
    h+='</div></div>';
  });

  const d=f.filter(m=>m.status=='completed'||m.status=='approved').length;
  const p=f.length?Math.round(d/f.length*100):0;
  h+='<h3 style="color:#888;margin:14px 0 8px;font-size:12px;">'+(cur=='tk'?'TK运营':'数字短剧')+' 里程碑总览</h3>';
  h+='<div style="background:#1a1d27;border-radius:6px;padding:12px;">';
  h+='<div style="display:flex;align-items:center;gap:8px;">';
  h+='<div class="pbar"><div class="pfill" style="width:'+p+'%;background:#22c55e"></div></div>';
  h+='<span style="font-weight:700;color:#22c55e;font-size:13px;">'+d+'/'+f.length+'</span>';
  h+='</div>';
  h+='<div style="font-size:9px;color:#555;margin-top:6px;">&#10003; '+f.filter(function(m){return m.status=='completed'||m.status=='approved'}).map(function(m){return m.name}).join(' · ')+'</div>';
  h+='</div>';
  h+='</div>';
  document.getElementById('summaryView').innerHTML=h;
  setTimeout(function(){if(typeof renderChartPanel==='function')renderChartPanel();},200);
}

// @@FUNC: submitFeedback
async function submitFeedback() {
  var typeEl = document.getElementById('fb-type');
  var descEl = document.getElementById('fb-desc');
  if (!typeEl || !descEl) return;
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({type: typeEl.value, description: descEl.value, severity: 'minor', source: 'DM-0'})
    });
  } catch(e) {}
}

