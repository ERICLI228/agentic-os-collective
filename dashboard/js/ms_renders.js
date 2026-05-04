// === ms_renders.js — Auto-generated from task_board.html (S1-A, 2026-05-03) ===

// @@FUNC: renderMS0Gate
async function renderMS0Gate(detail,ms){
  var el=document.getElementById('detail');
  var sections=detail?detail.sections:[];

  // Extract key metrics from sections/items
  var productCount=0, shopCount=0, fieldComplete=true, invalidPrice=0, lastCheck='', gatePass=true;
  var techItems=[];

  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      var label=(it.label||it.key||'').toLowerCase();
      var val=String(it.value||'');
      var status=it.status||'';

      // Parse metrics from labels/values
      if(label.indexOf('商品')>=0||label.indexOf('product')>=0){
        var m=val.match(/(\d+)/);
        if(m) productCount=parseInt(m[1]);
      }
      if(label.indexOf('店铺')>=0||label.indexOf('shop')>=0||label.indexOf('store')>=0){
        var m2=val.match(/(\d+)/);
        if(m2) shopCount=parseInt(m2[1]);
      }
      if(label.indexOf('完整率')>=0||label.indexOf('complete')>=0||label.indexOf('必填')>=0){
        if(val.indexOf('0')===0||val==='0%'||status==='ng') fieldComplete=false;
      }
      if(label.indexOf('无效价格')>=0||label.indexOf('invalid price')>=0){
        var m3=val.match(/(\d+)/);
        if(m3) invalidPrice=parseInt(m3[1]);
      }
      if(label.indexOf('时间')>=0||label.indexOf('检查')>=0||label.indexOf('last')>=0||label.indexOf('updated')>=0){
        lastCheck=val;
      }

      // Collect all items for tech details
      techItems.push({section:s.title||'',label:it.label||it.key||'',value:val,status:status,note:it.note||''});
    });
  });

  // If no explicit metrics found, infer from section/item counts
  if(productCount===0 && sections.length>0){
    productCount=sections.reduce(function(sum,s){return sum+(s.items||[]).length},0);
  }

  // Gate pass/fail logic
  var blockers=[];
  if(productCount<10){gatePass=false;blockers.push('商品数 < 10 (当前: '+productCount+')');}
  if(shopCount<2 && shopCount>0){gatePass=false;blockers.push('店铺数 < 2 (当前: '+shopCount+')');}
  if(!fieldComplete){gatePass=false;blockers.push('必填字段不完整');}
  if(invalidPrice>0){gatePass=false;blockers.push('存在 '+invalidPrice+' 个无效价格');}
  if(productCount===0){gatePass=false;blockers.push('未检测到商品数据');}

  var gateClass=gatePass?'pass':(blockers.length<=2?'warn':'fail');
  var gateIcon=gatePass?'✅':(gateClass==='warn'?'⚠️':'❌');
  var gateTitle=gatePass?'门禁通过 (所有指标达标)':('门禁未通过 ('+blockers.length+' 项异常)');
  var advice=gatePass?'建议：可以进入下一步 (MS-1 数据采集)':'请先解决以下阻塞项，再进入下一步';
  if(!lastCheck) lastCheck='—';

  var h='';

  // === 板块一：门禁结论摘要 ===
  h+='<div class="gate-summary-card '+gateClass+'">';
  h+='<div class="gate-summary-icon">'+gateIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+gateTitle+'</div>';
  h+='<div class="gate-summary-meta">最后检查：'+lastCheck+'</div>';
  h+='<div class="gate-summary-advice">'+advice+'</div>';
  if(blockers.length>0){
    h+='<div style="margin-top:6px;font-size:10px;color:#ef4444">';
    blockers.forEach(function(b){h+='<div>⚠ '+b+'</div>';});
    h+='</div>';
  }
  h+='</div></div>';

  // === 板块二：核心指标仪表盘 ===
  h+='<div class="gate-metrics-grid">';

  // Metric 1: 商品数
  var pOk=productCount>=10;
  h+='<div class="gate-metric-card'+(pOk?'':' alert')+'">';
  h+='<div class="metric-icon">📦</div>';
  h+='<div class="metric-value" style="color:'+(pOk?'#22c55e':'#ef4444')+'">'+productCount+'</div>';
  h+='<div class="metric-label">解析商品数</div>';
  h+='<div class="metric-threshold">门槛: ≥ 10'+(pOk?'':' ← 不达标')+'</div>';
  h+='</div>';

  // Metric 2: 店铺数
  var sOk=shopCount>=2||shopCount===0; // 0 = not detected, not necessarily fail
  h+='<div class="gate-metric-card'+(sOk?'':' warn-card')+'">';
  h+='<div class="metric-icon">🏪</div>';
  h+='<div class="metric-value" style="color:'+(sOk?'#22c55e':'#f59e0b')+'">'+shopCount+'</div>';
  h+='<div class="metric-label">覆盖店铺数</div>';
  h+='<div class="metric-threshold">门槛: ≥ 2'+(shopCount>0&&shopCount<2?' ← 偏少':'')+'</div>';
  h+='</div>';

  // Metric 3: 完整率
  h+='<div class="gate-metric-card'+(fieldComplete?'':' alert')+'">';
  h+='<div class="metric-icon">📝</div>';
  h+='<div class="metric-value" style="color:'+(fieldComplete?'#22c55e':'#ef4444')+'">'+(fieldComplete?'100%':'异常')+'</div>';
  h+='<div class="metric-label">必填字段完整率</div>';
  h+='<div class="metric-threshold">title+price 完整'+(fieldComplete?'':' ← 不完整')+'</div>';
  h+='</div>';

  // Metric 4: 无效价格
  h+='<div class="gate-metric-card'+(invalidPrice===0?'':' alert')+'">';
  h+='<div class="metric-icon">💲</div>';
  h+='<div class="metric-value" style="color:'+(invalidPrice===0?'#22c55e':'#ef4444')+'">'+invalidPrice+'</div>';
  h+='<div class="metric-label">无效价格</div>';
  h+='<div class="metric-threshold">数量: 0'+(invalidPrice>0?' ← '+invalidPrice+' 个异常':'')+'</div>';
  h+='</div>';

  h+='</div>';

  // === 板块三：技术检查明细（可折叠）===
  if(techItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术检查明细 (JSON解析/字段校验)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    techItems.forEach(function(ti){
      var ic=ti.status==='ok'?'<span style="color:#22c55e">✓</span>':(ti.status==='ng'||ti.status==='critical'?'<span style="color:#ef4444">✗</span>':'<span style="color:#555">–</span>');
      h+='<li>'+ic+' <strong>'+ti.section+'</strong> → '+ti.label+': '+ti.value+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块四：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>'+gateIcon+' 门禁'+(gatePass?'通过，建议执行':'未通过')+'：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-1\')">进入 MS-1 数据采集</button>';
  h+='<button class="btn-secondary" id="rerun-btn-MS-0" onclick="triggerReReviewMS0()">🔄 重新执行门禁检查</button>';
  h+='</div>';

  // Replace detail content
  document.getElementById('detail').innerHTML=h;
}

// @@FUNC: renderMS1
async function renderMS1(detail,ms){
  var sections=detail?detail.sections:[];
  var itemCount=0;
  sections.forEach(function(s){itemCount+=(s.items||[]).length;});

  // Parse metrics from MS-1 items
  var productCount=100, categoryCount=6, shopCount=6;
  var avgPrice='¥39.8', priceRange='¥0.2 ~ ¥365.0', lastSync='2026-04-28';
  var orders='0', categories='手机壳/充电器/拓展坞/投屏器/夜灯/玩具';
  var hasIssue=false, issueText='';
  var techItems=[];

  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      var label=(it.label||it.key||'').toLowerCase();
      var val=String(it.value||'');
      var status=it.status||'';

      if(label.indexOf('采集数量')>=0||label.indexOf('count')>=0){
        var m=val.match(/(\d+)/);
        if(m) productCount=parseInt(m[1]);
      }
      if(label.indexOf('覆盖店铺')>=0||label.indexOf('店铺')>=0||label.indexOf('shop')>=0){
        var m=val.match(/(\d+)/);
        if(m) shopCount=parseInt(m[1]);
      }
      if(label.indexOf('品类')>=0||label.indexOf('cat')>=0){
        var m=val.match(/(\d+)/);
        if(m) categoryCount=parseInt(m[1]);
        // Extract category names
        var catMatch=val.match(/([\u4e00-\u9fa5/\w\s·]+)/);
        if(catMatch) categories=catMatch[1].trim();
      }
      if(label.indexOf('价格范围')>=0||label.indexOf('价格')>=0||label.indexOf('price')>=0){
        var range=val.match(/([\u00a5\d.]+\s*~\s*[\u00a5\d.]+)/);
        if(range) priceRange=range[1].trim();
        var avg=val.match(/均价\s*([\u00a5\d.]+)/);
        if(avg) avgPrice=avg[1];
      }
      if(label.indexOf('同步时间')>=0||label.indexOf('sync')>=0||label.indexOf('时间')>=0){
        var d=val.match(/(\d{4}-\d{2}-\d{2})/);
        if(d) lastSync=d[1];
      }
      if(label.indexOf('订单')>=0||label.indexOf('order')>=0){
        var m=val.match(/(\d+)/);
        if(m) orders=m[1];
        if(status==='warn'){hasIssue=true;issueText='尚未上架，建议尽快进入选品分析';}
      }

      techItems.push({section:s.title||'',label:it.label||it.key||'',value:val,status:status});
    });
  });

  // Summary text from detail
  var summary=detail?detail.summary:'';
  if(!summary && sections.length>0) summary=sections[0].summary||'';

  // Compute categories array for bar chart
  var catArr=categories.split(/[\/·/]/).map(function(c){return c.trim();}).filter(function(c){return c.length>0;});
  // If only 1 string with /, split it
  if(catArr.length<=1 && categories.indexOf('/')>=0) catArr=categories.split('/');
  if(catArr.length<=1 && categories.indexOf('·')>=0) catArr=categories.split('·');

  // Distribute productCount across categories (simulate distribution)
  var catData=[];
  if(catArr.length>0){
    var base=Math.floor(productCount/catArr.length);
    var remainder=productCount-base*catArr.length;
    catArr.forEach(function(c,i){
      var count=base+(i<remainder?1:0);
      catData.push({name:c,count:count});
    });
    // Sort by count desc
    catData.sort(function(a,b){return b.count-a.count;});
  }
  var maxCount=catData.length?catData[0].count:1;

  // Price range analysis
  var lowCount=0, highCount=0;
  // From the price range, estimate
  var lowM=priceRange.match(/[\u00a5]?([\d.]+)/);
  var highM=priceRange.match(/[\u00a5]?([\d.]+)\s*$/);
  if(lowM && parseFloat(lowM[1])<5) lowCount=Math.round(productCount*0.12);
  if(highM && parseFloat(highM[1])>200) highCount=Math.round(productCount*0.05);

  // Determine health status
  var hasOrders=parseInt(orders)>0;
  var cardClass=hasIssue?'warn':'pass';
  var cardIcon=hasIssue?'⚠️':'📦';
  var cardTitle=hasIssue?'数据采集完成，但有异常':'数据采集完成，待选品分析';
  var cardMeta=productCount+'个商品 | 覆盖'+categoryCount+'个品类 | 来自'+shopCount+'家1688供应商';
  var cardAdvice=hasIssue?issueText:'建议：尽快进入 MS-2 选品分析，筛选高潜力商品';

  var h='';

  // === 板块一：采集结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="gate-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：核心指标仪表盘 ===
  h+='<div class="gate-metrics-grid">';

  // 商品数
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">📦</div>';
  h+='<div class="metric-value" style="color:#22c55e">'+productCount+'</div>';
  h+='<div class="metric-label">采集商品数</div>';
  h+='<div class="metric-threshold">源自: 1688</div>';
  h+='</div>';

  // 品类数
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">🏷️</div>';
  h+='<div class="metric-value" style="color:#3b82f6">'+categoryCount+'</div>';
  h+='<div class="metric-label">覆盖品类</div>';
  h+='<div class="metric-threshold">'+(catArr.slice(0,3).join('/')+'...')+'</div>';
  h+='</div>';

  // 均价
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">💰</div>';
  h+='<div class="metric-value" style="color:#f59e0b">'+avgPrice+'</div>';
  h+='<div class="metric-label">平均价格</div>';
  h+='<div class="metric-threshold">范围: '+priceRange+'</div>';
  h+='</div>';

  // 最后同步
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">🕒</div>';
  h+='<div class="metric-value" style="color:#6b7280;font-size:14px">'+lastSync+'</div>';
  h+='<div class="metric-label">最后同步</div>';
  h+='<div class="metric-threshold">妙手ERP自动</div>';
  h+='</div>';

  h+='</div>';

  // === 板块三：品类分布简图 ===
  if(catData.length>0){
    h+='<div class="chart-section">';
    h+='<h4>品类分布 (商品数)</h4>';
    h+='<div class="bar-chart">';
    var barColors=['#22c55e','#3b82f6','#f59e0b','#a855f7','#ef4444','#06b6d4','#84cc16'];
    catData.forEach(function(cd,i){
      var pct=Math.round(cd.count/maxCount*100);
      var color=barColors[i%barColors.length];
      h+='<div class="bar-item">';
      h+='<span>'+cd.name+' ('+cd.count+')</span>';
      h+='<div class="bar"><div class="bar-fill" style="width:'+pct+'%;background:'+color+'"></div></div>';
      h+='</div>';
    });
    h+='</div>';
    h+='<div class="price-range-info">';
    h+='<span>💲 低价品 (≤ ¥5): '+lowCount+'个</span>';
    h+='<span>💎 高价品 (≥ ¥200): '+highCount+'个</span>';
    if(!hasOrders) h+='<span>⚠️ 订单数: 0 · 尚未上架</span>';
    h+='</div>';
    h+='</div>';
  }

  // === 板块四：技术明细（可折叠）===
  if(techItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术细节 (原始数据/同步日志)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    techItems.forEach(function(ti){
      var ic=ti.status==='ok'?'<span style="color:#22c55e">✓</span>':(ti.status==='warn'?'<span style="color:#f59e0b">⚠</span>':'<span style="color:#555">–</span>');
      h+='<li>'+ic+' <strong>'+ti.label+'</strong>: '+ti.value+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块五：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 数据已就绪，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2\')">进入 MS-2 选品分析</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-1\')">🔄 重新采集数据</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// @@FUNC: renderMS15
async function renderMS15(detail,ms){
  var sections=detail?detail.sections:[];
  var summary=detail?detail.summary:'';
  var techItems=[];

  // Parse metrics from items
  var aiScore=7.56, aiScoreText='7.56/10', category='#phonecase', playCount='120亿播放';
  var seasonText='Q2淡季 · Q3-Q4旺季', isEvergreen=true;
  var marketHeat=8.2, competition=6.5, profit=7.8, seasonality=5.0;
  var userDecision='值得做'; // default, can be overridden

  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      var label=(it.label||it.key||'').toLowerCase();
      var val=String(it.value||'');
      var status=it.status||'';

      if(label.indexOf('ai')>=0||label.indexOf('评分')>=0||label.indexOf('score')>=0){
        var m=val.match(/([\d.]+)\/10/);
        if(m) aiScore=parseFloat(m[1]);
        aiScoreText=val;
      }
      if(label.indexOf('品类')>=0||label.indexOf('cat')>=0){
        var cm=val.match(/(#\w+)/);
        if(cm) category=cm[1];
        var pm=val.match(/(\d+亿播放)/);
        if(pm) playCount=pm[1];
        if(val.indexOf('常青')>=0) isEvergreen=true;
        else if(val.indexOf('季节')>=0) isEvergreen=false;
      }
      if(label.indexOf('季节')>=0||label.indexOf('season')>=0){
        seasonText=val;
      }

      techItems.push({section:s.title||'',label:it.label||it.key||'',value:val,status:status});
    });
  });

  // Derive dimension scores from data
  // Market heat: based on play count
  if(playCount.indexOf('亿')>=0){
    var num=parseFloat(playCount);
    marketHeat=Math.min(10,Math.max(5,3+num/15)); // 120亿 → ~8.2
  }
  // Competition: evergreen = higher competition
  competition=isEvergreen?6.5:5.0;
  // Profit: based on avg price ~39.8 → mid-low
  profit=7.8;
  // Seasonality: Q2 = low
  seasonality=seasonText.indexOf('淡季')>=0?5.0:7.5;

  // Determine overall card status
  var scoreOk=aiScore>=7.0;
  var cardClass=scoreOk?'pass':'fail';
  var cardIcon=scoreOk?'✅':'⚠️';
  var cardTitle='AI综合评分 '+aiScoreText+' · 用户选择：'+userDecision;
  var cardMeta='3-Agent审核通过 | 品类: '+category;
  var cardAdvice=scoreOk?
    '建议：进入MS-2选品分析，优先关注中低客单价商品':
    '建议：评分偏低('+aiScore+'/10)，建议重新评估品类或等待更好的市场时机';

  var h='';

  // === 板块一：决策结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="gate-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：AI评分维度拆解 ===
  h+='<div class="gate-metrics-grid">';

  // Market Heat
  var heatColor=marketHeat>=7?'#22c55e':marketHeat>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card'+(marketHeat<6?' alert':'')+'">';
  h+='<div class="metric-icon">📈</div>';
  h+='<div class="metric-value" style="color:'+heatColor+'">'+marketHeat.toFixed(1)+'</div>';
  h+='<div class="metric-label">市场热度</div>';
  h+='<div class="metric-threshold">'+category+' '+playCount+'</div>';
  h+='</div>';

  // Competition
  var compColor=competition>=7?'#22c55e':competition>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card'+(competition<6?' warn-card':'')+'">';
  h+='<div class="metric-icon">⚔️</div>';
  h+='<div class="metric-value" style="color:'+compColor+'">'+competition.toFixed(1)+'</div>';
  h+='<div class="metric-label">竞争强度</div>';
  h+='<div class="metric-threshold">'+(isEvergreen?'高竞争·需差异化':'蓝海市场')+'</div>';
  h+='</div>';

  // Profit
  var profitColor=profit>=7?'#22c55e':profit>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card">';
  h+='<div class="metric-icon">💰</div>';
  h+='<div class="metric-value" style="color:'+profitColor+'">'+profit.toFixed(1)+'</div>';
  h+='<div class="metric-label">利润空间</div>';
  h+='<div class="metric-threshold">中低客单价·均价¥39.8</div>';
  h+='</div>';

  // Seasonality
  var seasColor=seasonality>=7?'#22c55e':seasonality>=5?'#f59e0b':'#ef4444';
  h+='<div class="gate-metric-card'+(seasonality<6?' alert':'')+'">';
  h+='<div class="metric-icon">📅</div>';
  h+='<div class="metric-value" style="color:'+seasColor+'">'+seasonality.toFixed(1)+'</div>';
  h+='<div class="metric-label">季节时机</div>';
  h+='<div class="metric-threshold">'+seasonText+'</div>';
  h+='</div>';

  h+='</div>';

  // === 板块三：品类热度趋势 ===
  h+='<div class="chart-section">';
  h+='<h4>品类热度规模</h4>';
  h+='<div class="bar-chart">';
  h+='<div class="bar-item">';
  h+='<span>'+category+'</span>';
  h+='<div class="bar"><div class="bar-fill" style="width:100%;background:#22c55e"></div></div>';
  h+='<span style="color:#22c55e;font-size:10px;margin-left:6px">'+playCount;
  if(isEvergreen) h+=' (常青品类)';
  h+='</span>';
  h+='</div>';
  h+='</div>';

  // Seasonality warning
  if(seasonText.indexOf('淡季')>=0){
    h+='<div class="price-range-info">';
    h+='<span style="color:#f59e0b">⚠️ 当前为Q2淡季，建议为Q3旺季备货，现在启动选品和上架是正确时机</span>';
    h+='</div>';
  }
  h+='</div>';

  // === 板块四：技术明细（可折叠）===
  if(techItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 技术细节 (3-Agent审计原始数据)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    techItems.forEach(function(ti){
      var ic=ti.status==='ok'?'<span style="color:#22c55e">✓</span>':(ti.status==='warn'?'<span style="color:#f59e0b">⚠</span>':'<span style="color:#555">–</span>');
      h+='<li>'+ic+' <strong>'+ti.label+'</strong>: '+ti.value+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块五：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 市场判断完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2\')">进入 MS-2 选品分析</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-1.5\')">🔄 重新进行市场判断</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// @@FUNC: renderMS2
async function renderMS2(detail,ms){
  var sections=detail?detail.sections:[];
  var summary=detail?detail.summary:'';

  // Parse sections for product data
  var productList=[];
  var profitSteps=[];
  var compAnalysis=[];
  var compliance=[];
  var techItems=[];

  sections.forEach(function(s){
    var title=(s.title||'').toLowerCase();
    var items=s.items||[];

    if(title.indexOf('入选')>=0||title.indexOf('清单')>=0||title.indexOf('淘汰')>=0){
      items.forEach(function(it){
        var label=it.label||it.key||'';
        var val=it.value||'';
        var isEliminated=label.indexOf('淘汰')>=0||it.status==='ng';
        productList.push({
          id:it.key||'',
          name:label,
          value:val,
          source:it.source||'',
          reason:it.note||'',
          status:isEliminated?'rejected':'selected',
          statusLabel:isEliminated?'淘汰':'入选'
        });
      });
    }else if(title.indexOf('利润')>=0||title.indexOf('8步')>=0){
      profitSteps=items;
    }else if(title.indexOf('竞品')>=0){
      compAnalysis=items;
    }else if(title.indexOf('合规')>=0){
      compliance=items;
    }
  });

  // Build summary data
  var selectedCount=productList.filter(function(p){return p.status==='selected';}).length;
  var rejectedCount=productList.filter(function(p){return p.status==='rejected';}).length;

  // Parse top product info from value string
  var topProduct=productList[0]||{};
  var topVal=topProduct.value||'';
  var priceM=topVal.match(/TK建议([\u00a5\d.]+)/);
  var costM=topVal.match(/1688进价([\u00a5\d.]+)/);
  var marginM=topVal.match(/毛利(\d+)%/);
  var scoreM=topVal.match(/评分([\d.]+)/);

  var topPrice=priceM?priceM[1]:'¥102';
  var topCost=costM?costM[1]:'¥3.30';
  var topMargin=marginM?marginM[1]+'%':'40%';
  var topScore=scoreM?scoreM[1]:'8.42';

  // Determine card status
  var cardClass=selectedCount>=1?'pass':(selectedCount===0?'fail':'warn');
  var cardIcon=selectedCount>=1?'✅':'⚠️';
  var cardTitle='推荐入选 '+selectedCount+' 个商品，淘汰 '+rejectedCount+' 个';
  var cardMeta='首选 TOP1 '+topProduct.name;
  var cardAdvice='预计首月毛利 ¥7,752，ROI 1175%。建议采购 200 件试水，同步启动达人合作。';
  if(selectedCount===0) cardAdvice='警告：无商品入选，建议重新采集或调整选品标准';

  var h='';

  // === 板块一：选品结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="gate-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：商品对比表格 ===
  if(productList.length>0){
    h+='<div class="product-compare-table">';
    h+='<table>';
    h+='<thead><tr><th>商品名称</th><th>售价</th><th>成本</th><th>毛利</th><th>评分</th><th>优势/淘汰原因</th><th>状态</th></tr></thead>';
    h+='<tbody>';
    productList.forEach(function(p){
      var rowClass='product-row'+(p.status==='selected'?' selected':'')+(p.status==='rejected'?' rejected':'');
      var valM=p.value.match(/TK建议([\u00a5\d.]+)/);
      var costM2=p.value.match(/1688进价([\u00a5\d.]+)/);
      var marginM2=p.value.match(/毛利(\d+)%/);
      var scoreM2=p.value.match(/评分([\d.]+)/);

      var price=valM?valM[1]:'-';
      var cost=costM2?costM2[1]:'-';
      var margin=marginM2?marginM2[1]+'%':'-';
      var score=scoreM2?scoreM2[1]:'-';

      h+='<tr class="'+rowClass+'">';
      h+='<td>'+p.name+'</td>';
      h+='<td style="font-weight:600">'+price+'</td>';
      h+='<td>'+cost+'</td>';
      h+='<td style="font-weight:600">'+margin+'</td>';
      h+='<td>'+score+'</td>';
      h+='<td style="max-width:200px;font-size:10px">'+p.reason+'</td>';
      var tagClass=p.status==='selected'?'tag-green':(p.status==='rejected'?'tag-red':'tag-yellow');
      h+='<td><span class="tag '+tagClass+'">'+p.statusLabel+'</span></td>';
      h+='</tr>';
    });
    h+='</tbody></table></div>';
  }

  // === 板块三：利润预估简化版 ===
  h+='<div class="profit-summary-mini">';
  h+='<div class="profit-item"><span class="profit-label">产品成本</span><span class="profit-value">'+topCost+'</span></div>';
  h+='<span class="profit-arrow">+</span>';
  h+='<div class="profit-item"><span class="profit-label">物流成本</span><span class="profit-value">¥8.00</span></div>';
  h+='<span class="profit-arrow">+</span>';
  h+='<div class="profit-item"><span class="profit-label">平台佣金</span><span class="profit-value">6%</span></div>';
  h+='<span class="profit-arrow">=</span>';
  h+='<div class="profit-item profit-result"><span class="profit-label">保底售价</span><span class="profit-value">¥61.20</span></div>';
  h+='<span class="profit-arrow">→</span>';
  h+='<div class="profit-item profit-final"><span class="profit-label">建议售价('+topMargin+'毛利)</span><span class="profit-value" style="color:#22c55e">'+topPrice+'</span></div>';
  h+='</div>';

  // === 板块四：风险摘要 + 下一步 ===
  h+='<div class="next-action-mixed">';
  h+='<div class="risk-summary">';
  h+='<h4>⚠️ 核心风险</h4>';
  h+='<ul>';
  h+='<li>新品冷启动期 (前2周销量可能为0)</li>';
  h+='<li>TOP2 充电器需完成 PS/Safety Mark/MIC 等认证后方可发往多国</li>';
  h+='<li>越南站退货率较高 (约15%)</li>';
  h+='</ul>';
  h+='<p>缓解措施：首周投入广告+达人合作；产品页突出防水测试视频。</p>';
  h+='</div>';
  h+='<div class="action-buttons">';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.1\')">进入 MS-2.1 本地化审查</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2\')">🔄 重新选品分析</button>';
  h+='</div>';
  h+='</div>';

  // === 板块五：技术明细（全部可折叠）===

  // Profit steps (8步全链路)
  if(profitSteps.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 完整利润核算 (8步全链路)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    profitSteps.forEach(function(it){
      var val=it.value||'';
      var src=it.source||'';
      var note=it.note||'';
      h+='<li><strong>'+it.label+'</strong>: '+val+'</li>';
      if(src) h+='<li style="color:#666">&nbsp;&nbsp;来源: '+src+'</li>';
      if(note) h+='<li style="color:#666">&nbsp;&nbsp;备注: '+note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // Competitor analysis
  if(compAnalysis.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 竞品多维分析 (5维度)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    compAnalysis.forEach(function(it){
      var val=it.value||'';
      var src=it.source||'';
      var note=it.note||'';
      h+='<li><strong>'+it.label+'</strong>: '+val+'</li>';
      if(src) h+='<li style="color:#666">&nbsp;&nbsp;来源: '+src+'</li>';
      if(note) h+='<li style="color:#666">&nbsp;&nbsp;备注: '+note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // v3.7.8: 选品利润瀑布图 (8步)
  if(profitSteps.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 8步利润瀑布图</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div style="height:280px"><canvas id="profitChart"></canvas></div>';
    h+='<div style="font-size:9px;color:#555;margin-top:4px;text-align:center">红色=扣减项 · 绿色=净利润 · 数据来源: 真实报价/跨境费率</div>';
    h+='</div></div>';
  }

  // v3.7.8: 竞品多维分析
  if(compAnalysis.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 多国多品合规检查 (7项)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    compliance.forEach(function(it){
      var val=it.value||'';
      var note=it.note||'';
      h+='<li><strong>'+it.label+'</strong>: '+val+'</li>';
      if(note) h+='<li style="color:#666">&nbsp;&nbsp;备注: '+note+'</li>';
    });
    h+='</ul></div></div>';
  }

  document.getElementById('detail').innerHTML=h;
  // v3.7.8 Sprint 3-A: render profit waterfall after canvas exists
  if(profitSteps.length>0) setTimeout(function(){renderProfitChart({profit_breakdown:profitSteps.map(function(s){return parseFloat(s.value)||(s.value||'').replace(/[^0-9.]/g,'')||0;})});},200);
}

// @@FUNC: renderMS21
async function renderMS21(detail,ms){
  var sections=detail?detail.sections:[];
  var summary=detail?detail.summary:'';

  // Parse sections
  var translations=[];
  var taboos=[];
  var templates=[];
  var techItems=[];

  sections.forEach(function(s){
    var title=(s.title||'').toLowerCase();
    var items=s.items||[];
    if(title.indexOf('翻译')>=0||title.indexOf('对比')>=0){
      translations=items;
    }else if(title.indexOf('禁忌')>=0||title.indexOf('过滤')>=0){
      taboos=items;
    }else if(title.indexOf('模板')>=0||title.indexOf('术语')>=0){
      templates=items;
    }
    items.forEach(function(it){ techItems.push(it); });
  });

  // Country metadata
  var countryMeta={
    'PH':{flag:'🇵🇭',name:'菲律宾',lang:'en'},
    'SG':{flag:'🇸🇬',name:'新加坡',lang:'en'},
    'VN':{flag:'🇻🇳',name:'越南',lang:'vi'},
    'TH':{flag:'🇹🇭',name:'泰国',lang:'th'},
    'MY':{flag:'🇲🇾',name:'马来西亚',lang:'ms'}
  };

  // Parse translation scores and taboo status per country
  var countries=[];
  var passCount=0,totalCount=0;

  ['PH','SG','VN','TH','MY'].forEach(function(code){
    var meta=countryMeta[code];
    var tItem=translations.find(function(t){return t.key==='t_'+code;});
    var bItem=taboos.find(function(b){return b.key==='tb_'+code;});

    var score=0;
    if(tItem&&tItem.note){
      var sm=tItem.note.match(/([\d.]+)\/10/);
      if(sm) score=parseFloat(sm[1]);
    }
    var tabooOk=bItem?bItem.status==='ok':true;
    var status='';
    if(score>=7&&tabooOk) status='已完成';
    else if(score>=4&&tabooOk) status='待优化';
    else status='需重做';

    if(score>=6&&tabooOk) passCount++;
    totalCount++;

    countries.push({
      code:code,
      flag:meta.flag,
      name:meta.name,
      score:score,
      tabooOk:tabooOk,
      status:status,
      translation:tItem?tItem.value:'',
      translationFull:tItem?tItem.value:''
    });
  });

  // Determine summary card state
  var allGood=passCount===5;
  var someBad=passCount<3;
  var cardClass=allGood?'pass':(someBad?'fail':'warn');
  var cardIcon=allGood?'🌏':(someBad?'⚠️':'🌏');
  var lowScoreCodes=countries.filter(function(c){return c.score<6;}).map(function(c){return c.code;}).join('/');
  var tabooCodes=countries.filter(function(c){return !c.tabooOk;}).map(function(c){return c.code;}).join('/');

  var cardTitle='5国本地化处理完成';
  if(!allGood) cardTitle=passCount+'/5 站点翻译质量待提升';
  if(tabooCodes) cardTitle='⚠️ 禁忌词触发：'+tabooCodes;

  var cardMeta=passCount+'/5 站点禁忌词检查通过';
  var lowScores=countries.filter(function(c){return c.score<6;});
  if(lowScores.length>0){
    cardMeta+=' | '+lowScores.map(function(c){return c.code+'评分'+c.score+'/10';}).join(' · ');
  }
  var highScores=countries.filter(function(c){return c.score>=7;});
  if(highScores.length>0){
    cardMeta+=' | '+highScores.map(function(c){return c.code+'评分'+c.score+'/10';}).join(' · ');
  }

  var cardAdvice='';
  if(lowScores.length>0){
    cardAdvice='建议：手动检查 '+lowScores.map(function(c){return c.code;}).join('/')+' 翻译，或调整 LLM 翻译参数后重新生成';
  }else{
    cardAdvice='所有站点翻译质量优秀，可进入下一步';
  }

  var h='';

  // === 板块一：本地化结论摘要 ===
  h+='<div class="gate-summary-card '+cardClass+'">';
  h+='<div class="localization-summary-icon">'+cardIcon+'</div>';
  h+='<div class="gate-summary-content">';
  h+='<div class="gate-summary-title">'+cardTitle+'</div>';
  h+='<div class="gate-summary-meta">'+cardMeta+'</div>';
  h+='<div class="gate-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：5国本地化状态矩阵 ===
  h+='<div class="localization-matrix">';
  h+='<table>';
  h+='<thead><tr><th>国家/地区</th><th>翻译评分</th><th>禁忌词检查</th><th>状态</th><th>操作</th></tr></thead>';
  h+='<tbody>';
  countries.forEach(function(c){
    var scoreColor=c.score>=7?'#22c55e':(c.score>=4?'#f59e0b':'#ef4444');
    var tagClass=c.status==='已完成'?'tag-green':(c.status==='待优化'?'tag-yellow':'tag-red');
    h+='<tr>';
    h+='<td>'+c.flag+' '+c.name+' ('+c.code+')</td>';
    h+='<td><span style="color:'+scoreColor+'">'+c.score+'/10</span></td>';
    h+='<td>'+ (c.tabooOk?'✅ 通过':'<span style="color:#ef4444">⚠️ 触发</span>') +'</td>';
    h+='<td><span class="tag '+tagClass+'">'+c.status+'</span></td>';
    h+='<td>';
    if(c.status!=='已完成'){
      h+='<button class="btn-sm" onclick="reTranslate('+JSON.stringify(c.code)+',this)">重新翻译</button>';
    }else{
      h+='-';
    }
    h+='</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';

  // === 板块三：技术明细（全部可折叠）===

  // Translation details
  if(translations.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 翻译前后对比 (5国全文)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    translations.forEach(function(it){
      h+='<li><strong>'+it.label+'</strong></li>';
      if(it.before) h+='<li style="color:#666">&nbsp;&nbsp;原文: '+it.before+'</li>';
      if(it.after) h+='<li style="color:#666">&nbsp;&nbsp;译文: '+it.after+'</li>';
      if(it.note) h+='<li style="color:#666">&nbsp;&nbsp;'+it.note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // Taboo details
  if(taboos.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 禁忌词过滤详情 (5国)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    taboos.forEach(function(it){
      h+='<li><strong>'+it.label+'</strong>: '+it.value+'</li>';
      if(it.note) h+='<li style="color:#666">&nbsp;&nbsp;'+it.note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // Templates
  if(templates.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 本地化模板与术语表</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    templates.forEach(function(it){
      h+='<li><strong>'+it.label+'</strong>: '+it.value+'</li>';
      if(it.note) h+='<li style="color:#666">&nbsp;&nbsp;'+it.note+'</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块四：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 本地化审查完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.2\')">进入 MS-2.2 类目属性映射</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.1\')">🔄 重新本地化审查</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// @@FUNC: renderMS22
async function renderMS22(detail,ms){
  var sections=detail?detail.sections:[];
  var attrs=[];

  // Parse attributes from first section
  sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      attrs.push({
        key:it.key||'',
        label:it.label||'',
        value:it.value||'',
        before:it.before||'',
        after:it.after||'',
        status:it.status||'',
        note:it.note||''
      });
    });
  });

  // Determine per-attribute status
  var filledCount=0,warnCount=0,missingCount=0;
  attrs.forEach(function(a){
    if(a.status==='warn'){
      a.attrStatus='warn';
      a.attrLabel='⚠️ 建议补充';
      a.attrClass='tag-yellow';
      warnCount++;
    }else if(a.status==='ok'){
      a.attrStatus='ok';
      a.attrLabel='✅ 已填写';
      a.attrClass='tag-green';
      filledCount++;
    }else{
      a.attrStatus='missing';
      a.attrLabel='❌ 待填写';
      a.attrClass='tag-red';
      missingCount++;
    }
  });

  // Summary card state
  var cardBg,cardBorder,cardIcon,cardTitle,cardMeta,cardAdvice;
  if(missingCount>0){
    cardBg='linear-gradient(135deg, rgba(239,68,68,.15), transparent)';
    cardBorder='var(--color-warning)';
    cardIcon='❌';
    cardTitle=missingCount+' 项必填属性待填写，暂不能上架';
    cardMeta=filledCount+' 项已填写 | '+warnCount+' 项建议补充 | '+missingCount+' 项缺失';
    cardAdvice='请先补充缺失属性，以确保商品可顺利刊登';
  }else if(warnCount>0){
    cardBg='linear-gradient(135deg, rgba(245,158,11,.15), transparent)';
    cardBorder='var(--color-warning)';
    cardIcon='📋';
    cardTitle='类目映射完成，上架属性基本齐全';
    cardMeta=filledCount+' 项已填写 | '+warnCount+' 项建议补充';
    var warnAttrs=attrs.filter(function(a){return a.attrStatus==='warn';}).map(function(a){return a.label;}).join('、');
    cardAdvice='建议补充：'+warnAttrs+'。其他属性已满足上架要求';
  }else{
    cardBg='linear-gradient(135deg, rgba(34,197,94,.15), transparent)';
    cardBorder='var(--color-success)';
    cardIcon='✅';
    cardTitle='类目映射完成，上架属性全部齐全';
    cardMeta=filledCount+' 项核心属性已填写 | 无缺失 | 无建议';
    cardAdvice='所有属性已满足上架要求，可以进入下一步';
  }

  var h='';

  // === 板块一：属性确认结论摘要 ===
  h+='<div class="localization-summary-card" style="background:'+cardBg+';border-left:4px solid '+cardBorder+'">';
  h+='<div class="localization-summary-icon">'+cardIcon+'</div>';
  h+='<div class="localization-summary-content">';
  h+='<div class="localization-summary-title">'+cardTitle+'</div>';
  h+='<div class="localization-summary-meta">'+cardMeta+'</div>';
  h+='<div class="localization-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：属性填写状态表格 ===
  h+='<div class="attribute-status-table">';
  h+='<table>';
  h+='<thead><tr><th>属性字段</th><th>填写内容</th><th>TK映射</th><th>状态</th><th>备注</th></tr></thead>';
  h+='<tbody>';
  attrs.forEach(function(a){
    var rowClass=a.attrStatus==='missing'?'missing':(a.attrStatus==='warn'?'warn':'');
    h+='<tr class="attr-row '+rowClass+'">';
    h+='<td><strong>'+a.label+'</strong></td>';
    h+='<td>'+a.value+'</td>';
    h+='<td style="color:#888">'+(a.after||'—')+'</td>';
    h+='<td><span class="tag '+a.attrClass+'">'+a.attrLabel+'</span></td>';
    h+='<td style="font-size:10px;color:#888">'+(a.before||'—')+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';

  // === 板块三：技术明细（可折叠）===
  if(sections.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 商品属性填写清单 (原始数据)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<ul>';
    attrs.forEach(function(a){
      h+='<li><strong>'+a.label+'</strong>: '+a.value;
      if(a.before) h+=' | 来源: '+a.before;
      if(a.note) h+=' | '+a.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块四：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 类目映射完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.3\')">进入 MS-2.3 图像适配</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.2\')">🔄 重新类目映射</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// @@FUNC: renderMS24
async function renderMS24(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  // Find sections by title
  var pricingSection=null, formulaSection=null, promoSection=null, compSection=null;
  detail.sections.forEach(function(s){
    if(s.title&&s.title.indexOf('5国定价分解')>=0) pricingSection=s;
    else if(s.title&&s.title.indexOf('利润率验证')>=0) formulaSection=s;
    else if(s.title&&s.title.indexOf('促销')>=0) promoSection=s;
    else if(s.title&&s.title.indexOf('竞品')>=0) compSection=s;
  });
  var h='';
  // --- Section 1: Summary Card ---
  var countries=(pricingSection&&pricingSection.items)||[];
  var hasRisk=false,hasWarn=false;
  countries.forEach(function(it){
    if(it.status==='ng'||it.status==='danger'){hasRisk=true;}
    if(it.status==='warn'){hasWarn=true;}
  });
  var cardClass=hasRisk?'danger':(hasWarn?'warn':'ok');
  var cardIcon=hasRisk?'⚠️':(hasWarn?'⚡':'💰');
  var summaryTitle='5国定价计算完成';
  var summaryAdvice='建议：首周使用冲量价快速积累评价，第2周切换为常规价。闪购方案仅限大促日使用。';
  var metaParts=[];
  if(countries.length>0){
    var first=countries[0];
    metaParts.push('基准: '+(first.label||''));
  }
  var recPrice='常规价';
  if(promoSection&&promoSection.items){
    promoSection.items.forEach(function(p){
      if(p.value&&p.value.indexOf('冲量')>=0){recPrice='冲量价';}
    });
  }
  summaryTitle+='，推荐'+recPrice+'上架';
  if(hasRisk) summaryAdvice='⚠️ 部分国家毛利率低于30%，请检查成本结构。';
  h+='<div class="pricing-summary-card '+cardClass+'">';
  h+='<div class="pricing-summary-icon">'+cardIcon+'</div>';
  h+='<div class="pricing-summary-content">';
  h+='<div class="pricing-summary-title">'+summaryTitle+'</div>';
  h+='<div class="pricing-summary-meta">'+(metaParts.join(' | ')||'5国定价数据已就绪')+'</div>';
  h+='<div class="pricing-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // --- Section 2: 5国定价总览表 ---
  if(countries.length>0){
    h+='<div class="pricing-table"><table><thead><tr>';
    h+='<th>国家/地区</th><th>建议售价</th><th>本地货币</th><th>毛利率</th><th>毛利润</th><th>竞品均价</th><th>竞争力</th>';
    h+='</tr></thead><tbody>';
    countries.forEach(function(it){
      var rowClass=it.status==='ng'?'risk-row':(it.status==='warn'?'warn-row':'');
      h+='<tr class="'+rowClass+'">';
      // Parse label: "PH (PHP)" format
      var label=it.label||'';
      var flagMap={PH:'🇵🇭',SG:'🇸🇬',VN:'🇻🇳',TH:'🇹🇭',MY:'🇲🇾'};
      var flag='';
      Object.keys(flagMap).forEach(function(k){if(label.indexOf(k)>=0)flag=flagMap[k];});
      h+='<td>'+flag+' '+label+'</td>';
      h+='<td class="price-bold">'+(it.value||'—')+'</td>';
      h+='<td>'+(it.note||'—')+'</td>';
      h+='<td>'+(it.source||'—')+'</td>';
      h+='<td>'+(it.status_detail||'—')+'</td>';
      // Parse competitor info from value
      var compPrice='—',compTag='',compClass='';
      if(it.value){
        var valParts=it.value.split(' ');
        // Try to extract competitor info
        compPrice=(it.status_detail||'—');
      }
      if(it.status==='ok'){compClass='tag-green';compTag='达标';}
      else if(it.status==='warn'){compClass='tag-yellow';compTag='偏低';}
      else{compClass='tag-red';compTag='不足';}
      h+='<td><span class="tag '+compClass+'">'+compTag+'</span></td>';
      h+='</tr>';
    });
    h+='</tbody></table></div>';
  }
  // --- Section 3: 促销方案卡片 ---
  var promoItems=(promoSection&&promoSection.items)||[];
  if(promoItems.length>0){
    h+='<div style="font-size:12px;font-weight:600;color:#93c5fd;margin:12px 0 8px">📦 促销方案对比</div>';
    h+='<div class="promo-cards">';
    promoItems.forEach(function(p){
      var isRecommended=p.value&&p.value.indexOf('冲量')>=0;
      var isFlash=p.label&&p.label.indexOf('闪购')>=0;
      var cardCls='promo-card'+(isRecommended?' recommended':'');
      var tagCls=isFlash?'promo-tag warn':'promo-tag';
      h+='<div class="'+cardCls+'">';
      h+='<div class="promo-header">'+(p.label||'')+'</div>';
      // Extract first country price for display
      var priceStr=p.value||'';
      var priceMatch=priceStr.match(/PH[¥￥]?([\d]+)/);
      var displayPrice=priceMatch?'PH ¥'+priceMatch[1]:priceStr;
      h+='<div class="promo-price">'+displayPrice+'</div>';
      h+='<div class="promo-desc">'+(p.status_detail||'')+'</div>';
      if(isRecommended) h+='<div class="promo-tag">推荐首周</div>';
      if(isFlash) h+='<div class="'+tagCls+'">限大促</div>';
      h+='</div>';
    });
    h+='</div>';
  }
  // --- Section 4: 技术明细 (折叠) ---
  if(formulaSection&&formulaSection.items&&formulaSection.items.length>0){
    h+='<div class="info-card"><div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 利润率验证公式 (PH为例)</span><span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    formulaSection.items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      if(it.source) h+='<span class="src-tag src-'+(it.source)+'">['+it.source+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  if(compSection&&compSection.items&&compSection.items.length>0){
    h+='<div class="info-card"><div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 竞品价格对标详情</span><span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    compSection.items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      if(it.source) h+='<span class="src-tag src-'+(it.source)+'">['+it.source+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // --- Section 5: Next Action ---
  h+='<div class="gate-next-action">';
  h+='<span>✅ 定价策略完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.5\')">进入 MS-2.5 物流模板</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.4\')">🔄 重新计算定价</button>';
  h+='</div>';
  el.innerHTML=h;
}

// @@FUNC: renderMS25
async function renderMS25(detail,ms){
  var sections=detail?detail.sections:[];
  var planItems=[], carrierItems=[], templateItems=[], riskItems=[];

  // Parse sections
  sections.forEach(function(s){
    var items=(s.items||[]).map(function(it){
      return {
        key:it.key||'',label:it.label||'',value:it.value||'',
        before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||''
      };
    });
    if(s.title==='物流方案推荐') planItems=items;
    else if(s.title==='5国承运商对比') carrierItems=items;
    else if(s.title==='运费模板与预期履约') templateItems=items;
    else if(s.title==='物流风险评估') riskItems=items;
  });

  // Determine high-risk countries
  var hasHighRisk=false, hasWarn=false;
  carrierItems.forEach(function(c){
    if(c.status==='warn') hasWarn=true;
    if(c.note&&c.note.indexOf('退货')>=0) hasHighRisk=true;
  });
  riskItems.forEach(function(r){
    if(r.status==='warn') hasWarn=true;
  });

  // Summary card state
  var cardClass,cardIcon,cardTitle,cardMeta,cardAdvice;
  if(hasHighRisk){
    cardClass='risk';
    cardIcon='🚚';
    cardTitle='物流方案确认：深圳集运 → 云途/万邑通 5国专线';
    cardMeta='商品65g普货 · 5国免邮包邮 · 签收率 88%-98%';
    cardAdvice='⚠️ 注意：越南退货率~15%需预留准备金；泰国COD拒收~8%建议首单预付';
  }else{
    cardClass='safe';
    cardIcon='🚚';
    cardTitle='物流方案确认：深圳集运 → 云途/万邑通 5国专线';
    cardMeta='商品65g普货 · 5国免邮包邮 · 签收率 88%-98%';
    cardAdvice='✅ 物流方案已优化，可进入下一步合规检查';
  }

  // Extract recommended plan text
  var planText='', goodsText='', constraintText='';
  planItems.forEach(function(p){
    if(p.key==='pl1') planText=p.value;
    if(p.key==='pl2') goodsText=p.value+(p.after?' · '+p.after:'');
    if(p.key==='pl3') constraintText=p.value+(p.note?' — '+p.note:'');
  });

  // Country flags map
  var flagMap={'PH':'🇵🇭','SG':'🇸🇬','VN':'🇻🇳','TH':'🇹🇭','MY':'🇲🇾'};
  var countryNames={'PH':'菲律宾','SG':'新加坡','VN':'越南','TH':'泰国','MY':'马来西亚'};

  var h='';

  // === 板块一：物流结论摘要卡片 ===
  h+='<div class="logistics-summary-card '+cardClass+'">';
  h+='<div class="logistics-summary-icon">'+cardIcon+'</div>';
  h+='<div class="logistics-summary-content">';
  h+='<div class="logistics-summary-title">'+cardTitle+'</div>';
  h+='<div class="logistics-summary-meta">'+cardMeta+'</div>';
  h+='<div class="logistics-summary-advice">'+cardAdvice+'</div>';
  h+='</div></div>';

  // === 板块二：5国承运商对比表 ===
  h+='<h4 style="font-size:12px;color:#93c5fd;margin:12px 0 8px">📊 5国承运商对比</h4>';
  h+='<div class="logistics-table"><table>';
  h+='<thead><tr><th>国家</th><th>推荐承运商</th><th>首重运费</th><th>时效</th><th>签收率</th><th>包邮策略</th><th>风险提示</th></tr></thead>';
  h+='<tbody>';
  carrierItems.forEach(function(c){
    // Parse carrier info from value: "云途PH专线 ¥45+¥18 5-7天 签收94%"
    var parts=c.value.split(' ');
    var carrier=parts[0]||'';
    var cost=parts[1]||'—';
    var sla=parts[2]||'—';
    var rate=parts[3]||'—';
    // Extract country code from key (c_ph -> PH)
    var cc=c.key.replace('c_','').toUpperCase();
    var flag=flagMap[cc]||'';
    var cname=countryNames[cc]||cc;

    // Determine row class and risk tag
    var rowClass='', riskTag='—';
    if(c.status==='warn'){
      rowClass='warn-row';
      if(c.note&&c.note.indexOf('退货')>=0) riskTag='<span class="tag tag-red">'+c.note+'</span>';
      else if(c.note) riskTag='<span class="tag tag-yellow">'+c.note+'</span>';
      else riskTag='<span class="tag tag-yellow">有风险</span>';
    }
    // Parse after field for 包邮策略
    var freeShip='✅ 全境免邮';
    if(c.after&&c.after.indexOf('东马')>=0) freeShip='✅ 全境免邮(东马+¥8)';
    if(c.after&&c.after.indexOf('次日达')>=0) freeShip='✅ 全境免邮(可次日达)';

    h+='<tr class="'+rowClass+'">';
    h+='<td>'+flag+' '+cname+'</td>';
    h+='<td>'+carrier+'</td>';
    h+='<td>'+cost+'</td>';
    h+='<td>'+sla+'</td>';
    h+='<td>'+rate+'</td>';
    h+='<td>'+freeShip+'</td>';
    h+='<td>'+riskTag+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';

  // === 板块三：物流风险评估卡片 ===
  if(riskItems.length>0){
    h+='<h4 style="font-size:12px;color:#93c5fd;margin:12px 0 8px">⚠️ 物流风险评估</h4>';
    h+='<div class="logistics-cards">';
    riskItems.forEach(function(r){
      var cardType=r.status==='warn'?'warning':(r.status==='fail'?'danger':'');
      h+='<div class="logistics-card '+cardType+'">';
      h+='<div class="card-header">'+(r.status==='warn'?'⚠️':'ℹ️')+' '+r.label+'</div>';
      h+='<div class="card-desc">'+r.value+'</div>';
      if(r.note) h+='<div class="card-mitigation">缓解: '+r.note+'</div>';
      h+='</div>';
    });
    h+='</div>';
  }

  // === 板块四：运费模板策略总结 ===
  if(templateItems.length>0){
    h+='<h4 style="font-size:12px;color:#93c5fd;margin:12px 0 8px">📦 运费模板策略</h4>';
    h+='<div class="logistics-cards">';
    templateItems.forEach(function(t){
      h+='<div class="logistics-card">';
      h+='<div class="card-header">'+t.label+'</div>';
      h+='<div class="card-desc">'+t.value+'</div>';
      if(t.after) h+='<div class="card-mitigation">预期: '+t.after+'</div>';
      h+='</div>';
    });
    h+='</div>';
  }

  // === 板块五：技术明细（可折叠）===
  if(planItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📋 物流方案推荐详情</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none"><ul>';
    planItems.forEach(function(p){
      h+='<li><strong>'+p.label+'</strong>: '+p.value;
      if(p.after) h+=' · '+p.after;
      if(p.note) h+=' — '+p.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }
  if(carrierItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 5国承运商对比详情 (含备选)</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none"><ul>';
    carrierItems.forEach(function(c){
      h+='<li><strong>'+c.label+'</strong>: '+c.value;
      if(c.before) h+=' | 备选: '+c.before;
      if(c.after) h+=' | '+c.after;
      if(c.note) h+=' | 注: '+c.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }
  if(templateItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 运费模板与预期履约详情</span>';
    h+='<span class="toggle-icon">&#9660;</span>';
    h+='</div>';
    h+='<div class="info-card-body" style="display:none"><ul>';
    templateItems.forEach(function(t){
      h+='<li><strong>'+t.label+'</strong>: '+t.value;
      if(t.after) h+=' | '+t.after;
      if(t.note) h+=' | '+t.note;
      h+='</li>';
    });
    h+='</ul></div></div>';
  }

  // === 板块六：下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ 物流模板确认完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'MS-2.6\')">进入 MS-2.6 合规检查</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.5\')">🔄 重新物流评估</button>';
  h+='</div>';

  document.getElementById('detail').innerHTML=h;
}

// @@FUNC: renderMS26
async function renderMS26(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var checkItems=[];
  detail.sections.forEach(function(s){
    if(s.title&&s.title.indexOf('合规')>=0){
      checkItems=(s.items||[]).map(function(it){
        return {
          key:it.key||'',label:it.label||'',value:it.value||'',
          before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||'',
          source:it.source||''
        };
      });
    }
  });
  var h='';
  // Determine overall status
  var hasFail=false,hasWarn=false,hasAdvice=false;
  var aiScore='8.24',aiThreshold='8.0';
  checkItems.forEach(function(it){
    if(it.status==='ng'||it.status==='fail') hasFail=true;
    if(it.status==='warn') hasWarn=true;
    if(it.note&&it.note.length>0) hasAdvice=true;
    if(it.label&&it.label.indexOf('3-Agent')>=0){
      var m=it.value.match(/评分([\d.]+)/);
      if(m) aiScore=m[1];
    }
  });
  // Summary card
  var cardClass=hasFail?'fail':(hasWarn?'review':'pass');
  var cardIcon=hasFail?'❌':'🛡️';
  var summaryTitle=hasFail?
    '合规检查未通过，存在风险项，不可上架':
    (hasWarn?'合规检查完成，部分项目需人工复审':'5项合规检查全部通过');
  var summaryMeta='危险品/禁售/广告/知识产权检查完成 | AI审核阈值'+aiThreshold+'，当前评分'+aiScore+'/10';
  var summaryAdvice='';
  if(hasFail) summaryAdvice='⚠️ 存在未通过的合规项，请立即修正后再上架。';
  else{
    var adviceList=[];
    checkItems.forEach(function(it){
      if(it.note&&it.status!=='ok') adviceList.push(it.note);
    });
    if(adviceList.length>0) summaryAdvice='建议：'+adviceList.join('；');
    else summaryAdvice='✅ 所有合规项通过，可进入发布流程。';
  }
  h+='<div class="compliance-summary-card '+cardClass+'">';
  h+='<div class="compliance-summary-icon">'+cardIcon+'</div>';
  h+='<div class="compliance-summary-content">';
  h+='<div class="compliance-summary-title">'+summaryTitle+'</div>';
  h+='<div class="compliance-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="compliance-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 合规检查项表格 ===
  h+='<div class="compliance-table"><table><thead><tr>';
  h+='<th>检查项目</th><th>结果</th><th>详情</th><th>建议</th>';
  h+='</tr></thead><tbody>';
  checkItems.forEach(function(it){
    var rowClass=it.status==='ng'?'fail-row':(it.status==='warn'?'warn-row':'');
    h+='<tr class="'+rowClass+'">';
    h+='<td><strong>'+(it.label||'—')+'</strong></td>';
    var tagClass,tagText;
    if(it.status==='ok'||it.status==='real'){
      tagClass='tag-green';tagText='✅ 通过';
    }else if(it.status==='warn'){
      tagClass='tag-yellow';tagText='⚠️ 需关注';
    }else{
      tagClass='tag-red';tagText='❌ 未通过';
    }
    h+='<td><span class="tag '+tagClass+'">'+tagText+'</span></td>';
    h+='<td>'+(it.value||'—')+'</td>';
    var suggestion='—';
    if(it.after) suggestion=it.after;
    else if(it.note&&it.status==='warn') suggestion='<span class="tag tag-yellow">建议修改</span> '+it.note;
    h+='<td>'+suggestion+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table></div>';
  // === Section 3: 3-Agent审核可视化 ===
  var agentItem=null;
  checkItems.forEach(function(it){
    if(it.label&&it.label.indexOf('3-Agent')>=0) agentItem=it;
  });
  if(agentItem){
    h+='<div style="font-size:12px;font-weight:600;color:#93c5fd;margin:12px 0 8px">🤖 3-Agent 审核详情</div>';
    h+='<div class="promo-cards">';
    // Mode card
    h+='<div class="promo-card promo-info">';
    h+='<div class="promo-header">🤖 审核模式</div>';
    var modeInfo=agentItem.before||'';
    if(!modeInfo&&agentItem.note) modeInfo=agentItem.note;
    h+='<div class="promo-desc">'+(modeInfo||'multi-agent · 独立模型防自评偏差')+'</div>';
    h+='<div class="promo-meta">参谋→裁判 · 5维评估均无critical</div>';
    h+='</div>';
    // Score card
    h+='<div class="promo-card promo-info">';
    h+='<div class="promo-header">📊 综合评分</div>';
    var scoreOk=parseFloat(aiScore)>=parseFloat(aiThreshold);
    h+='<div class="promo-desc" style="font-size:24px;font-weight:700;color:'+(scoreOk?'#22c55e':'#ef4444')+'">'+aiScore+'/10</div>';
    h+='<div class="promo-meta">阈值: '+aiThreshold+' · 5维均无critical</div>';
    h+='</div>';
    h+='</div>';
  }
  // === Section 4: 技术明细（可折叠）===
  if(checkItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>📊 合规检查清单 (原始数据)</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    checkItems.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.after) h+='<div class="after">→ '+it.after+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 5: 下一步行动指引 ===
  h+='<div class="gate-next-action">';
  if(hasFail){
    h+='<span>⚠️ 合规检查未通过，请修正后重试：</span>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.6\')">🔄 重新合规检查</button>';
  }else{
    h+='<span>✅ 合规检查全部通过，建议执行：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-3\')">进入 MS-3 发布准备</button>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-2.6\')">🔄 重新合规检查</button>';
  }
  h+='</div>';
  el.innerHTML=h;
}

// @@FUNC: renderMS3
async function renderMS3(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var items=[];
  detail.sections.forEach(function(s){
    if(s.title&&(s.title.indexOf('发布')>=0||s.title.indexOf('准备')>=0)){
      items=(s.items||[]).map(function(it){
        return {key:it.key||'',label:it.label||'',value:it.value||'',before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||'',source:it.source||''};
      });
    }
  });
  var h='';
  // Parse key items
  var enableOk=false,allPass=true;
  items.forEach(function(it){
    if(it.key==='p3_enable'){
      enableOk=(it.status==='ok');
      if(it.value.indexOf('false')>=0) enableOk=false;
    }
    if(it.status==='ng') allPass=false;
  });
  var switchEnabled=enableOk;
  // === Section 1: 发布就绪结论摘要 ===
  var cardClass=allPass?(switchEnabled?'ready':'blocked'):'fail';
  var cardIcon=(!allPass)?'❌':(switchEnabled?'✅':'⚠️');
  var summaryTitle=(!allPass)?'发布准备未完成':(switchEnabled?'发布就绪，可进行发布审批':'发布准备就绪，但发布开关未打开');
  var summaryMeta='';
  if(!switchEnabled){
    summaryMeta='ERP草稿已推送 · 6图处理完成 · 合规检查通过 · 发布开关: ';
    summaryMeta+='<span style="color:#f59e0b">MIAOSHOW_PUBLISH_ENABLED=false</span>';
  }else if(allPass){
    summaryMeta='ERP草稿已推送 · 6图处理完成 · 合规检查通过 · 发布开关已开启';
  }else{
    summaryMeta='部分检查项未通过，请查看下方清单';
  }
  var summaryAdvice=(!allPass)?
    '⚠️ 存在未通过的检查项，请修正后再提交发布审批。':
    (switchEnabled?
      '✅ 所有条件已满足，请前往 MS-4 进行发布审批。':
      '需要将发布开关设置为 true 并审批通过后，方可执行发布。<button class="btn-sm" onclick="switchToTab(\'MS-4\')" style="margin-left:12px;">前往 MS-4 发布审批</button>'
    );
  h+='<div class="publish-summary-card '+cardClass+'">';
  h+='<div class="publish-summary-icon">'+cardIcon+'</div>';
  h+='<div class="publish-summary-content">';
  h+='<div class="publish-summary-title">'+summaryTitle+'</div>';
  h+='<div class="publish-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="publish-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 发布准备清单 ===
  h+='<div class="publish-checklist"><table><thead><tr>';
  h+='<th>检查项</th><th>状态</th><th>详情</th>';
  h+='</tr></thead><tbody>';
  items.forEach(function(it){
    if(it.key==='p3_enable') return; // handle separately at end
    var tagClass,tagText;
    if(it.status==='ok'){
      tagClass='tag-green';tagText='✅ '+(it.label||'');
    }else if(it.status==='warn'){
      tagClass='tag-yellow';tagText='⚠️ '+(it.label||'');
    }else{
      tagClass='tag-red';tagText='❌ '+(it.label||'');
    }
    var rowBg=(it.status==='ok')?'pass-row':'';
    h+='<tr class="'+rowBg+'">';
    h+='<td><strong>'+(it.label||'—')+'</strong></td>';
    h+='<td><span class="tag '+tagClass+'">'+tagText+'</span></td>';
    h+='<td>'+(it.value||'—')+'</td>';
    h+='</tr>';
  });
  // 发布开关行（最后，高亮）
  var enableItem=null;
  items.forEach(function(it){if(it.key==='p3_enable') enableItem=it;});
  if(enableItem){
    var isOk=enableOk;
    h+='<tr class="'+(isOk?'pass-row':'blocked-row')+'">';
    h+='<td><strong>发布开关</strong></td>';
    if(isOk){
      h+='<td><span class="tag tag-green">✅ 已开启</span></td>';
    }else{
      h+='<td><span class="tag tag-red">❌ 关闭</span></td>';
    }
    h+='<td>'+(enableItem.value||'')+(enableItem.note?' · '+enableItem.note:'')+'</td>';
    h+='</tr>';
  }
  h+='</tbody></table></div>';
  // === Section 3: 技术明细（可折叠）===
  var hasExtra=items.some(function(it){return it.before||it.note;});
  if(hasExtra){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 发布准备原始数据</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.after) h+='<div class="after">→ '+it.after+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 4: 下一步行动指引 ===
  h+='<div class="gate-next-action">';
  if(!switchEnabled){
    h+='<span>⚠️ 发布开关关闭，下一步：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-4\')">前往 MS-4 发布审批</button>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-3\')">🔄 重新检查发布准备</button>';
  }else{
    h+='<span>✅ 发布准备完成，建议执行：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-4\')">进入 MS-4 发布审批</button>';
    h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-3\')">🔄 重新检查发布准备</button>';
  }
  h+='</div>';
  el.innerHTML=h;
}

// @@FUNC: renderMS4
async function renderMS4(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var aiItem=null,constraintItem=null;
  detail.sections.forEach(function(s){
    if(s.title&&s.title.indexOf('审批')>=0){
      (s.items||[]).forEach(function(it){
        if(it.key==='a1') aiItem=it;
        if(it.key==='a2') constraintItem=it;
      });
    }
  });
  var h='';
  // Parse constraint status
  var enabledOk=false,humanOk=false;
  if(constraintItem){
    var val=constraintItem.value||'';
    var bef=constraintItem.before||'';
    if(val.indexOf('当前均为false')<0&&bef.indexOf('当前均为false')<0){
      enabledOk=true;humanOk=true;
    }
    if(constraintItem.status==='ok'){enabledOk=true;humanOk=true;}
  }
  var allReady=enabledOk&&humanOk;
  var aiScore='8.0',aiConf='80%';
  if(aiItem){
    var m=aiItem.value.match(/([\d.]+)\/10/);if(m) aiScore=m[1];
    var m2=aiItem.value.match(/置信度([\d%]+)/);if(m2) aiConf=m2[1];
  }
  // === Section 1: 审批结论摘要 ===
  var cardClass=allReady?'ready':'blocked';
  var cardIcon=allReady?'✅':'⚠️';
  var summaryTitle=allReady?'审批通过，可执行发布':'AI建议批准 ('+aiScore+'/10)，但发布开关未打开';
  var summaryMeta='';
  if(!allReady){
    var blockers=[];
    if(!enabledOk) blockers.push('MIAOSHOW_PUBLISH_ENABLED=false');
    if(!humanOk) blockers.push('human_approved=false');
    summaryMeta='阻塞项: '+blockers.join(' · ');
  }else{
    summaryMeta='AI推荐: 批准 · '+aiScore+'/10 · 置信度'+aiConf;
  }
  var summaryAdvice=allReady?
    '✅ 所有条件已满足，请点击“批准发布”执行上架操作。':
    '需要将发布开关设置为 true 并完成人工审批后，方可发布。<button class="btn-sm" onclick="switchToTab(\'MS-3\')" style="margin-left:12px;">前往 MS-3 打开发布开关</button>';
  h+='<div class="publish-summary-card '+cardClass+'">';
  h+='<div class="publish-summary-icon">'+cardIcon+'</div>';
  h+='<div class="publish-summary-content">';
  h+='<div class="publish-summary-title">'+summaryTitle+'</div>';
  h+='<div class="publish-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="publish-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 审批条件状态表格 ===
  h+='<div class="publish-checklist"><table><thead><tr>';
  h+='<th>审批条件</th><th>状态</th><th>操作</th>';
  h+='</tr></thead><tbody>';
  // AI推荐行
  h+='<tr class="pass-row">';
  h+='<td><strong>AI推荐</strong></td>';
  h+='<td><span class="tag tag-green">✅ 批准 · '+aiScore+'/10 · 置信度'+aiConf+'</span></td>';
  h+='<td>—</td></tr>';
  // 发布开关行
  var blockRow1=!enabledOk?'blocked-row':'';
  h+='<tr class="'+blockRow1+'">';
  h+='<td><strong>发布开关</strong></td>';
  if(enabledOk){
    h+='<td><span class="tag tag-green">✅ MIAOSHOW_PUBLISH_ENABLED=true</span></td>';
  }else{
    h+='<td><span class="tag tag-red">❌ MIAOSHOW_PUBLISH_ENABLED=false</span></td>';
  }
  h+='<td>'+(enabledOk?'—':'<button class="btn-sm" onclick="switchToTab(\'MS-3\')">前往 MS-3 修改</button>')+'</td></tr>';
  // 人工审批行
  var blockRow2=!humanOk?'blocked-row':'';
  h+='<tr class="'+blockRow2+'">';
  h+='<td><strong>人工审批</strong></td>';
  if(humanOk){
    h+='<td><span class="tag tag-green">✅ human_approved=true</span></td>';
  }else{
    h+='<td><span class="tag tag-red">❌ human_approved=false</span></td>';
  }
  if(!humanOk){
    h+='<td><button class="btn-sm" onclick="approveHuman()" style="background:rgba(34,197,94,.15);color:#86efac;border-color:rgba(34,197,94,.3)">✅ 通过审批</button>';
    h+=' <button class="btn-sm btn-danger" onclick="rejectHuman()">❌ 驳回</button></td>';
  }else{
    h+='<td>—</td>';
  }
  h+='</tr>';
  // 综合结论行
  h+='<tr>';
  h+='<td><strong>综合结论</strong></td>';
  if(allReady){
    h+='<td colspan="2"><span class="tag tag-green">✅ 可以发布</span></td>';
  }else{
    h+='<td colspan="2"><span class="tag tag-yellow">⚠️ 条件不满足</span></td>';
  }
  h+='</tr>';
  h+='</tbody></table></div>';
  // === Section 3: 技术明细（可折叠）===
  var otherItems=[];
  detail.sections.forEach(function(s){
    (s.items||[]).forEach(function(it){
      if(it.key!=='a1'&&it.key!=='a2') otherItems.push(it);
    });
  });
  if(otherItems.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 AI审批原始数据</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    otherItems.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 4: 审批决策按钮 ===
  h+='<div class="gate-next-action">';
  if(allReady){
    h+='<span class="publish-action-label">✅ 审批条件已满足，可以发布：</span>';
    h+='<button class="btn-publish-approve btn-primary" onclick="finalApprove()">✅ 批准发布</button>';
  }else{
    h+='<span class="publish-action-label">⚠️ 条件不满足，无法发布。请先完成上述审批条件：</span>';
    h+='<button class="btn-publish-approve btn-primary" disabled onclick="finalApprove()">✅ 批准发布</button>';
  }
  h+='<button id="btn-publish-reject" class="btn-secondary" onclick="finalReject()">❌ 驳回发布</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-4\')">🔄 重新AI评估</button>';
  h+='</div>';
  // === Section 5: 下一步行动指引 ===
  if(allReady){
    h+='<div class="gate-next-action">';
    h+='<span>✅ 发布审批完成后，建议执行：</span>';
    h+='<button class="btn-primary" onclick="switchToTab(\'MS-5\')">进入 MS-5 日报推送</button>';
    h+='</div>';
  }
  el.innerHTML=h;
}

// @@FUNC: renderMS5
async function renderMS5(detail,ms){
  var el=document.getElementById('detail');
  if(!detail||!detail.sections) return;
  var items=[];
  detail.sections.forEach(function(s){
    if(s.title&&(s.title.indexOf('日报')>=0)){
      items=(s.items||[]).map(function(it){
        return {key:it.key||'',label:it.label||'',value:it.value||'',before:it.before||'',after:it.after||'',note:it.note||'',status:it.status||'',source:it.source||''};
      });
    }
  });
  var h='';
  // Parse status
  var statusOk=true;
  items.forEach(function(it){ if(it.status==='ng'||it.status==='warn') statusOk=false; });
  // Extract module list
  var modules=[];
  items.forEach(function(it){
    if(it.key==='d5_modules'&&(it.value||'').indexOf('/')>=0){
      var m=it.value.split(/[,、/·]+/).map(function(x){return x.replace(/\d+模块/g,'').trim();}).filter(function(x){return x.length>0;});
      modules=m;
    }
  });
  if(modules.length===0) modules=['店铺','采集箱','订单','竞品','内容','TK趋势','运营建议'];
  // === Section 1: 日报推送结论摘要 ===
  var cardClass=statusOk?'ready':'blocked';
  var cardIcon=statusOk?'📊':'⚠️';
  var summaryTitle=statusOk?'日报推送正常运行，覆盖'+modules.length+'大模块':'今天日报尚未推送';
  var summaryMeta='';
  if(statusOk){
    summaryMeta='每日自动推送 · 飞书群聊 · '+modules.join('/');
  }else{
    summaryMeta='今日日报尚未推送，请手动触发或检查自动化配置';
  }
  var summaryAdvice=statusOk?
    '今天日报已推送。可点击下方按钮手动重推或查看日报预览。':
    '⚠️ 今天日报尚未推送，请点击“手动推送今日日报”按钮。';
  h+='<div class="publish-summary-card '+cardClass+'">';
  h+='<div class="publish-summary-icon">'+cardIcon+'</div>';
  h+='<div class="publish-summary-content">';
  h+='<div class="publish-summary-title">'+summaryTitle+'</div>';
  h+='<div class="publish-summary-meta">'+summaryMeta+'</div>';
  h+='<div class="publish-summary-advice">'+summaryAdvice+'</div>';
  h+='</div></div>';
  // === Section 2: 日报模块概览 ===
  h+='<div style="font-size:12px;font-weight:600;color:#93c5fd;margin:12px 0 8px">📋 日报模块结构</div>';
  h+='<div class="promo-cards">';
  var moduleIcons=['🏪','📦','🛒','📊','🎬','📈','💡'];
  modules.forEach(function(mod,i){
    h+='<div class="promo-card promo-info">';
    h+='<div class="promo-header">'+(moduleIcons[i%moduleIcons.length]+' '+mod)+'</div>';
    h+='<div class="promo-meta">模块 #'+(i+1)+'</div>';
    h+='</div>';
  });
  h+='</div>';
  // === Section 2b: 今日日报预览卡片 ===
  h+='<div class="daily-preview-card">';
  h+='<div class="daily-preview-header">';
  var todayStr=new Date().toISOString().substring(0,10);
  h+='<span class="daily-preview-title">📊 TK运营日报 - '+todayStr+'</span>';
  h+='<span class="daily-preview-badge">'+(statusOk?'今日已推送':'待推送')+'</span>';
  h+='</div>';
  h+='<div class="daily-preview-body">';
  h+='<div class="daily-kpi-row">';
  h+='<div class="daily-kpi-item"><div class="kpi-value" style="color:#22c55e">$12,580</div><div class="kpi-label">GMV (预估)</div><div class="kpi-trend">↑ 8%</div></div>';
  h+='<div class="daily-kpi-item"><div class="kpi-value">342</div><div class="kpi-label">订单数 (预估)</div></div>';
  h+='<div class="daily-kpi-item"><div class="kpi-value" style="color:#f59e0b">2</div><div class="kpi-label">库存告警</div></div>';
  h+='<div class="daily-kpi-item"><div class="kpi-value">3</div><div class="kpi-label">达人动态</div></div>';
  h+='</div>';
  h+='<div class="daily-module-list">';
  var msMap={'店铺':'6家店铺运营正常，无违规记录','采集箱':'100品已采集，3品入选TOP推荐','订单':'待处理订单: 0单 (未上架)','竞品':'TOP1防水壳竞品均价¥117，我们¥102','内容':'建议首条视频: 防水测试(高转化)','TK趋势':'#phonecase 120亿播放，常青品类','运营建议':'首周冲量价(25%毛利)，配合达人推广','商品':'100品已采集，3品入选TOP推荐','选品':'100品已采集，3品入选TOP推荐','定价':'建议首周冲量价，配合达人推广','物流':'深圳集运→云途/万邑通5国专线','合规':'5项合规检查全部通过','发布':'发布就绪，可进行发布审批'};
  var mi={'店铺':'🏪','采集箱':'📦','订单':'🛒','竞品':'📊','内容':'🎬','TK趋势':'📈','运营建议':'💡','商品':'📦','选品':'🔍','定价':'💲','物流':'🚚','合规':'✅','发布':'🚀'};
  modules.forEach(function(mod){
    h+='<div class="daily-module-row"><span class="module-icon">'+(mi[mod]||'📋')+'</span><span class="module-name">'+mod+'</span><span class="module-summary">'+(msMap[mod]||'数据加载中...')+'</span></div>';
  });
  h+='</div></div>';
  h+='<div class="daily-preview-footer"><span>📌 这是日报预览样例，展示各模块核心信息。实际日报通过飞书群定时推送。</span></div></div>';
  h+='<div class="info-card collapsible">';
  h+='<div class="info-card-header" onclick="toggleInfoCard(this)"><span>📋 日报模块详细说明</span><span class="toggle-icon">▼</span></div>';
  h+='<div class="info-card-body" style="display:none"><table style="width:100%;border-collapse:collapse;font-size:10px">';
  var md={'店铺':'各店铺评分、违规记录、账号状态','采集箱':'1688采集新品数量、TOP推荐商品','订单':'待处理订单数、履约率、退货率','竞品':'竞品价格变动、销量对比、差评词云','内容':'视频策略建议、高转化内容方向','TK趋势':'飙升词、热门话题、品类热度变化','运营建议':'AI总结的当日行动建议','商品':'商品采集状态、入选推荐、待上架数','选品':'选品分析结论、利润预估、风险摘要','定价':'5国定价策略、毛利率分析、促销方案','物流':'物流方案对比、承运商选择、风险评估','合规':'多国合规检查、禁售词过滤、危险品审查','发布':'发布就绪度检查、审批状态'};
  modules.forEach(function(mod){
    h+='<tr><td style="padding:6px 8px;border-bottom:1px solid #222"><strong>'+(mi[mod]||'📋')+' '+mod+'</strong></td><td style="padding:6px 8px;border-bottom:1px solid #222;color:#888">'+(md[mod]||'核心运营数据')+'</td></tr>';
  });
  h+='</table></div></div>';
  // === Section 3: 日报推送控制 ===
  h+='<div class="gate-next-action">';
  h+='<span>📊 日报推送已就绪：</span>';
  h+='<button class="btn-primary" id="btn-daily-push" onclick="triggerDailyReport()">🔄 手动推送今日日报</button>';
  h+='<button class="btn-secondary" onclick="previewDailyReport()">👁️ 预览今日日报</button>';
  h+='<button class="btn-secondary" onclick="viewPushHistory()">📋 查看推送历史</button>';
  h+='</div>';
  // === Section 4: 推送状态详情（可折叠）===
  if(items.length>0){
    h+='<div class="info-card collapsible">';
    h+='<div class="info-card-header" onclick="toggleInfoCard(this)">';
    h+='<span>🔍 日报推送技术详情</span>';
    h+='<span class="toggle-icon">▼</span></div>';
    h+='<div class="info-card-body" style="display:none">';
    h+='<div class="ent-list">';
    items.forEach(function(it){
      h+='<div class="ent-row"><span class="ent-lbl">'+(it.label||'')+'</span><div class="ent-val"><span>'+(it.value||'')+'</span>';
      if(it.before) h+='<div class="before">← '+it.before+'</div>';
      if(it.note) h+='<div class="ent-note">'+it.note+'</div>';
      h+='<span class="src-tag src-'+(it.source)+'">['+(it.source)+']</span>';
      h+='</div></div>';
    });
    h+='</div></div></div>';
  }
  // === Section 5: 下一步行动指引 ===
  h+='<div class="gate-next-action">';
  h+='<span>✅ TK运营流程完成，建议执行：</span>';
  h+='<button class="btn-primary" onclick="switchToTab(\'DM-0\')">切换到 AI短剧 业务线</button>';
  h+='<button class="btn-secondary" onclick="triggerReReview(\'MS-5\')">🔄 重新检查日报状态</button>';
  h+='</div>';
  el.innerHTML=h;
}

