(function initDashboard(){
  console.log('[INIT] DOM readyState='+document.readyState);
  try {
    if(typeof refresh==='function'){ refresh(); setInterval(refresh, 30000); console.log('[INIT] 30s polling started'); }
    else { console.error('[INIT] refresh() not found'); }
  } catch(e){
    console.error('[INIT] FAILED:', e.message);
    var el = document.getElementById('lastRefresh');
    if(el){ el.textContent='INIT ERROR: '+e.message; el.style.color='#ef4444'; }
  }
})();
