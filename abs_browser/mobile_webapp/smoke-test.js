'use strict';
const assert = require('node:assert/strict');
const WebSocket = require(process.env.ABS_BROWSER_APP_DIR + '/node_modules/ws');
const BASE = 'http://127.0.0.1:3010';
const CDP = 'http://127.0.0.1:9222';
const sleep = ms => new Promise(r => setTimeout(r, ms));
function pass(s){ console.log('PASS | '+s); }
async function getJson(url, timeout=5000){
  const r=await fetch(url,{signal:AbortSignal.timeout(timeout),cache:'no-store'});
  const body=await r.json().catch(()=>({}));
  assert.equal(r.ok,true,url+' returned HTTP '+r.status);
  return body;
}
async function streamTest(){
  return new Promise((resolve,reject)=>{
    const ws=new WebSocket('ws://127.0.0.1:3010/abs-mobile/stream',{perMessageDeflate:false});
    let done=false;
    const timer=setTimeout(()=>finish(new Error('No real Chromium screencast frame received in 10 seconds.')),10000);
    function finish(err){if(done)return;done=true;clearTimeout(timer);try{ws.close();}catch{}err?reject(err):resolve();}
    ws.on('message',raw=>{
      let m;try{m=JSON.parse(raw.toString());}catch{return;}
      if(m.type==='frame'&&typeof m.data==='string'&&m.data.length>100)finish();
      if(m.type==='error')finish(new Error(m.message||'Mirror stream error'));
    });
    ws.on('error',finish);
  });
}
async function cdpTouchAudit(){
  const version=await getJson(CDP+'/json/version');
  const browser=new WebSocket(version.webSocketDebuggerUrl,{perMessageDeflate:false,handshakeTimeout:5000});
  await new Promise((resolve,reject)=>{browser.once('open',resolve);browser.once('error',reject);});
  let id=0,targetId=null,sessionId=null;
  const pending=new Map();
  browser.on('message',raw=>{
    let m;try{m=JSON.parse(raw.toString());}catch{return;}
    if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(new Error(m.error.message||m.error.code)):p.resolve(m.result||{});}
  });
  function cmd(method,params={},session){
    const n=++id;
    return new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{pending.delete(n);reject(new Error('CDP timeout: '+method));},6000);
      pending.set(n,{resolve,reject,timer});
      browser.send(JSON.stringify({id:n,method,params,...(session?{sessionId:session}:{})}));
    });
  }
  async function evaluate(expression){
    const r=await cmd('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true},sessionId);
    if(r.exceptionDetails)throw new Error('Page evaluation failed: '+expression);
    return r.result?.value;
  }
  async function touch(type,points){
    await cmd('Input.dispatchTouchEvent',{type,touchPoints:points},sessionId);
    await sleep(45);
  }
  const point=(x,y,id)=>({x,y,id,force:1,radiusX:1,radiusY:1});
  try{
    const created=await cmd('Target.createTarget',{url:'about:blank'});
    targetId=created.targetId;
    const attached=await cmd('Target.attachToTarget',{targetId,flatten:true});
    sessionId=attached.sessionId;
    await cmd('Page.enable',{},sessionId);
    await cmd('Runtime.enable',{},sessionId);
    await cmd('Emulation.setDeviceMetricsOverride',{width:412,height:800,deviceScaleFactor:1,mobile:true,screenWidth:412,screenHeight:800},sessionId);
    await cmd('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5},sessionId);
    const html='<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=5,user-scalable=yes"><style>html,body{margin:0;padding:0}#field{position:fixed;left:10px;top:10px;width:220px;height:46px;z-index:5;font-size:18px}#space{height:7000px;background:linear-gradient(#fff,#9cf)}</style><input id="field" placeholder="touch test"><div id="space"></div>';
    await cmd('Page.navigate',{url:'data:text/html;charset=utf-8,'+encodeURIComponent(html)},sessionId);
    let loaded=false;for(let i=0;i<40;i++){try{if(await evaluate("document.readyState==='complete'")){loaded=true;break;}}catch{}await sleep(100);}
    assert.equal(loaded,true,'Temporary touch-audit page did not finish loading.');
    await sleep(250);
    await touch('touchStart',[point(50,30,1)]);
    await touch('touchEnd',[]);
    await sleep(100);
    assert.equal(await evaluate("document.activeElement && document.activeElement.id"),'field','A real touch did not focus the input.');
    pass('CDP touch tap focuses an input on a clean isolated Chromium tab.');
    await evaluate('window.scrollTo(0,0)');
    await touch('touchStart',[point(300,680,1)]);
    for(const y of [610,530,450,370,290,230])await touch('touchMove',[point(300,y,1)]);
    await touch('touchEnd',[]);
    await sleep(450);
    const scrollY=await evaluate('scrollY');
    assert.ok(scrollY>80,'Touch swipe did not scroll page (scrollY='+scrollY+').');
    pass('One-finger touch sequence scrolls the isolated page (scrollY='+Math.round(scrollY)+').');
    await evaluate('window.scrollTo(0,0)');
    const scaleBefore=await evaluate('visualViewport.scale');
    await touch('touchStart',[point(130,360,1),point(250,360,2)]);
    await touch('touchMove',[point(105,360,1),point(275,360,2)]);
    await touch('touchMove',[point(80,360,1),point(300,360,2)]);
    // CDP requires TouchMove with only remaining active contacts when one finger lifts,
    // followed by a TouchEnd with an empty touchPoints array when the last finger lifts.
    await touch('touchMove',[point(80,360,1)]);
    await touch('touchEnd',[]);
    await sleep(600);
    const scaleAfter=await evaluate('visualViewport.scale');
    assert.ok(scaleAfter>scaleBefore*1.05,'Two-finger pinch did not change visualViewport.scale (before='+scaleBefore+', after='+scaleAfter+').');
    pass('Two-finger pinch changes mobile page scale ('+scaleBefore.toFixed(2)+' -> '+scaleAfter.toFixed(2)+').');
  }finally{
    if(targetId)await cmd('Target.closeTarget',{targetId}).catch(()=>{});
    for(const p of pending.values()){clearTimeout(p.timer);p.reject(new Error('audit closed'));}
    try{browser.close();}catch{}
  }
}
(async()=>{
  const health=await getJson(BASE+'/health');
  assert.equal(health.ok,true,'Mobile mirror health failed.');
  pass('Mirror HTTP health and Chromium DevTools connection are healthy.');
  const state=await getJson(BASE+'/api/state');
  assert.equal(state.ok,true);assert.equal(state.connected,true);
  assert.ok(state.targetId&&state.viewport?.width>0&&state.viewport?.height>0);
  pass('Live page target and mobile viewport are available.');
  const html=await (await fetch(BASE+'/abs-mobile')).text();
  assert.ok(html.includes('ABS Browser')&&html.includes('typing-active'),'Phone-first UI or keyboard proxy missing.');
  await streamTest();
  pass('Actual Chromium screencast frame reaches the mirror WebSocket.');
  await cdpTouchAudit();
  console.log('ABS MOBILE MIRROR END-TO-END SMOKE TEST PASS');
})().catch(e=>{console.error('FAIL | '+(e.stack||e.message||String(e)));process.exit(1);});
