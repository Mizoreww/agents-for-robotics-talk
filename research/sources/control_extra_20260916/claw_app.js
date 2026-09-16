import {Stage} from './scene-renderer.js';
const $=s=>document.querySelector(s);
const demoInfo={
  threading:{defaultSpeed:8,model:'Dual ALOHA · native rope simulation',scope:'Native simulation with contact-triggered ideal point grasps.',events:[
    [0,'Pick up','Pick up a rope from the table','The rope begins unheld. The robot must create and maintain the route.'],
    [73.5,'Ring 1','Find a path through the first ring','Reorient the gripper and guide the rope through the opening while respecting the surrounding geometry.'],
    [128.8,'Handoff','Change the grasp, preserve the route','The receiving hand acquires the rope before the donor releases. The first crossing must remain.'],
    [178.5495,'Ring 2','Thread the second ring','A different ring orientation requires a new approach while the rope is already constrained by ring one.'],
    [224.3845,'Ring 3','Reach the third opening','Guide the free end through the final ring. Passing it once is not enough to finish the task.'],
    [294.4345,'Recovery','Recover a retreating rope end','During withdrawal, the free end slips back. Reacquire it and restore the three-ring route.'],
    [336.205,'Release','Place, release, and withdraw','Carry the end above the table, release the grasp, and withdraw. The final route survives without either hand holding it.']
  ]},
  claw:{defaultSpeed:4,model:'Dual ALOHA · kinematic replay',scope:'Pregrasped kinematic motion with ideal grasps; attributed object-space reference path.',events:[
    [0,'Interlock','Start with an interlocked pair','Each arm holds one part. Their relative geometry blocks a direct separation.'],
    [34,'Reorient','Change what is geometrically possible','Follow coordinated changes in relative orientation to move through the narrow configuration-space passage.'],
    [75,'Separate','Follow the way out','Both arms continue the constrained path until the two rigid parts can move apart.'],
    [105.117094695,'Transport','Bring the separated parts to their supports','The full robot bodies and the support fixtures remain in the scene throughout.'],
    [128.392910167,'Place','Seat both parts','Each part is brought to its fixed support before the corresponding grasp is released.'],
    [144.241660235,'Release','Release the first part','Open and withdraw the left hand while the second part remains held.'],
    [148.640406068,'Withdraw','Release the second part and move clear','Both parts finish on their supports. The robot has completed the planned geometric motion.']
  ]}
};
let stage,adapter,kind='claw',time=0,playing=false,raf=null,lastStamp=null,lastDraw=0,ready=false,switching=false,arm='left',state=null,seekGeneration=0,playGeneration=0;
const names=['Waist','Shoulder','Elbow','Forearm roll','Wrist angle','Wrist rotate','Finger 1','Finger 2'];
for(let i=0;i<8;i++)$('#joint-readout').insertAdjacentHTML('beforeend',`<div class="joint-row"><div class="joint-header"><span>${names[i]}</span><span class="joint-value" id="joint-${i}">—</span></div><div class="joint-track"><span class="actual" id="actual-${i}"></span><span class="target" id="target-${i}"></span></div></div>`);
function fmt(seconds){const minutes=Math.floor(seconds/60),s=(seconds%60).toFixed(1).padStart(4,'0');return `${minutes}:${s}`;}
function showError(error){console.error(error);setPlaying(false);ready=false;$('#loading').hidden=true;$('#error').hidden=false;$('#error').replaceChildren();const p=document.createElement('p');p.textContent=error.message||String(error);$('#error').append(p);const retry=document.createElement('button');retry.textContent='Reload scene';retry.onclick=()=>location.reload();$('#error').append(retry);}
function updateSpeed(){const speed=Number($('#speed').value),total=adapter?.duration||374;const watch=Math.ceil(total/speed);$('#watch-length').textContent=`~${Math.floor(watch/60)}m ${watch%60}s at ${speed}×`;}
function renderTelemetry(){
  if(!state||$('#action-panel').hidden)return;
  const offset=arm==='left'?0:8;
  for(let i=0;i<8;i++){
    const q=state.qpos[offset+i],ref=state.reference?.[offset+i],slider=i>=6;
    const lo=slider?0:-Math.PI,hi=slider?.045:Math.PI,percentage=x=>Math.max(0,Math.min(100,(x-lo)/(hi-lo)*100));
    $('#joint-'+i).textContent=Number.isFinite(q)?slider?`${(q*1000).toFixed(2)} mm`:`${(q*180/Math.PI).toFixed(1)}°`:'Unavailable';
    $('#actual-'+i).style.width=`${Number.isFinite(q)?percentage(q):0}%`;
    $('#target-'+i).hidden=!Number.isFinite(ref);if(Number.isFinite(ref))$('#target-'+i).style.left=`${percentage(ref)}%`;
  }
  $('.target-key').parentElement.hidden=!state.reference;
  if(state.kind==='threading'){
    const eq=state.equality;const held=arm==='left'?eq[2]||eq[4]:eq[3]||eq[5];
    $('#grip-state').textContent=held?'Grasp constraint active · acquired by contact':'Grasp constraint released';
  }else $('#grip-state').textContent=state.held[arm==='left'?0:1]?'Ideal rigid grasp active':'Part released to its support';
  if(state.ctrl){const start=arm==='left'?0:7;$('#control-readout').innerHTML=`<div class="control-values">${state.ctrl.slice(start,start+7).map((x,i)=>`${i<6?names[i]:'Gripper'}: ${i<6?x.toFixed(3)+' rad':(x*1000).toFixed(2)+' mm'}`).join('<br>')}</div>`;}
  else $('#control-readout').innerHTML='<p class="telemetry-note">Not recorded for this kinematic run.</p>';
  $('#telemetry-note').textContent=kind==='threading'?`Saved sample at ${fmt(state.sampleTime)}. Position-actuator inputs, not measured torque. Six arm channels and one coupled gripper channel per side. Bar lengths are display scales, not joint-limit tests.`:`Saved sample at ${fmt(state.sampleTime)}. Recorded joint trajectory; controller forces and reference signals are unavailable. Bar lengths are display scales, not joint-limit tests.`;
}
function updateUI(){
  $('#scrub').value=time;$('#time-current').textContent=fmt(time);$('#timeline-progress').style.width=`${time/adapter.duration*100}%`;
  const info=demoInfo[kind],idx=info.events.findLastIndex(e=>e[0]<=time+.001),event=info.events[Math.max(0,idx)];
  $('#chapter-index').textContent=`${String(idx+1).padStart(2,'0')} / ${info.events.length} · ${event[1].toUpperCase()}`;
  $('#chapter-title').textContent=event[2];$('#chapter-description').textContent=event[3];
  $('#event-label').textContent=kind==='threading'?(state?.phase?.label_en||'Full recorded run'):(adapter.data.timeline[state?.phaseIndex]?.label||event[1]);
  $('#chapters').querySelectorAll('button').forEach((b,i)=>{b.classList.toggle('active',i===idx);b.setAttribute('aria-current',i===idx?'step':'false');});
  $('#sample-note').textContent=`${$('#smooth').checked?'Smooth viewing between saved states':'Exact saved-state viewing'} · sample ${state?.sampleIndex+1||1}${state?.phase?.state_source_mode==='legacy-saved-qpos'?' · early recording format':''}`;
  if(state?.counts)document.querySelectorAll('.ring-tag').forEach((tag,i)=>{tag.classList.toggle('done',state.counts[i]===1);tag.textContent=`R${i+1} · ${state.counts[i]} crossing${state.counts[i]===1?'':'s'}`;});
  renderTelemetry();
}
async function seek(t){
  if(!adapter)return;const generation=++seekGeneration;const target=Math.max(0,Math.min(adapter.duration,t));
  const result=await adapter.seek(target,$('#smooth').checked);if(generation!==seekGeneration||!result)return;
  time=target;state=result;updateUI();stage.draw();
}
function buildTimeline(){
  const info=demoInfo[kind];$('#event-markers').replaceChildren();$('#chapters').replaceChildren();
  for(const [i,event] of info.events.entries()){
    const marker=document.createElement('button');marker.className='event-marker';marker.style.left=`${event[0]/adapter.duration*100}%`;marker.title=`${fmt(event[0])} · ${event[2]}`;marker.setAttribute('aria-label',`Jump to ${event[1]} at ${fmt(event[0])}`);marker.onclick=()=>{setPlaying(false);seek(event[0]).catch(showError);};$('#event-markers').append(marker);
    const chapter=document.createElement('button');chapter.className='chapter-button';chapter.innerHTML=`${event[1]}<span>${fmt(event[0])}</span>`;chapter.onclick=marker.onclick;$('#chapters').append(chapter);
  }
}
function setPlaying(value){
  playGeneration++;playing=Boolean(value&&ready&&!document.hidden);lastStamp=null;lastDraw=0;
  if(raf!==null)cancelAnimationFrame(raf);raf=null;
  $('#play-label').textContent=playing?'Pause':'Play';$('#play-icon').textContent=playing?'Ⅱ':'▶';$('#play').setAttribute('aria-label',playing?'Pause demonstration':'Play demonstration');
  if(playing)raf=requestAnimationFrame(animate);
}
async function animate(stamp){
  const playbackToken=playGeneration;raf=null;if(!playing||document.hidden){setPlaying(false);return;}
  if(lastStamp===null)lastStamp=stamp;
  if(stamp-lastDraw>=1000/30){
    const next=time+Math.min((stamp-lastStamp)/1000,.25)*Number($('#speed').value);lastStamp=stamp;lastDraw=stamp;
    try{await seek(next);}catch(e){showError(e);return;}
    if(playbackToken!==playGeneration)return;
    if(time>=adapter.duration){setPlaying(false);return;}
    if(kind==='threading'&&state.phase.end_s-time<3&&state.phaseIndex<adapter.data.phases.length-1)adapter.load(state.phaseIndex+1).catch(()=>{});
  }
  if(playing&&playbackToken===playGeneration)raf=requestAnimationFrame(animate);
}
async function switchDemo(next){
  if(switching)return;switching=true;setPlaying(false);ready=false;seekGeneration++;kind=next;time=0;state=null;
  $('#loading').hidden=false;$('#error').hidden=true;$('#play').disabled=$('#scrub').disabled=true;
  const info=demoInfo[kind];
  $('#speed').value=String(info.defaultSpeed);
  document.querySelectorAll('[data-demo]').forEach(b=>{const selected=b.dataset.demo===kind;b.disabled=true;b.classList.toggle('active',selected);b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1;});
  $('#demo-stage').setAttribute('aria-labelledby',`tab-${kind}`);$('#model-label').textContent=info.model;
  $('#scope-note').textContent=info.scope;
  $('#scene-tags').hidden=kind!=='threading';
  $('#action-description').textContent=kind==='threading'?'Recorded joints, planned references, and original position-actuator inputs.':'Recorded joint motion of the two arms. Kinematic execution; no torque trace.';
  try{
    adapter=await stage.open(kind);$('#scrub').max=adapter.duration;$('#time-total').textContent=fmt(adapter.duration);buildTimeline();ready=true;await seek(0);stage.view('task');
    document.querySelectorAll('[data-camera]').forEach(b=>b.classList.toggle('active',b.dataset.camera==='task'));
    $('#loading').hidden=true;$('#play').disabled=$('#scrub').disabled=false;updateSpeed();
    history.replaceState(null,'',`${location.pathname}?demo=${kind}${location.hash}`);
  }catch(e){showError(e);}finally{switching=false;document.querySelectorAll('[data-demo]').forEach(b=>b.disabled=false);}
}
$('#play').onclick=async()=>{if(!ready)return;if(time>=adapter.duration)await seek(0);setPlaying(!playing);};
$('#restart').onclick=()=>{setPlaying(false);seek(0).catch(showError);};
$('#scrub').oninput=()=>{setPlaying(false);seek(Number($('#scrub').value)).catch(showError);};
$('#speed').onchange=updateSpeed;$('#smooth').onchange=()=>seek(time).catch(showError);
$('#show-events').onchange=()=>{$('#event-markers').hidden=!$('#show-events').checked;$('#chapters').hidden=!$('#show-events').checked;};
function togglePanel(value){$('#action-panel').hidden=!value;$('#toggle-actions').setAttribute('aria-expanded',String(value));renderTelemetry();}
$('#toggle-actions').onclick=()=>togglePanel($('#action-panel').hidden);$('#close-actions').onclick=()=>togglePanel(false);
for(const b of document.querySelectorAll('[data-arm]'))b.onclick=()=>{arm=b.dataset.arm;document.querySelectorAll('[data-arm]').forEach(x=>x.classList.toggle('active',x===b));renderTelemetry();};
for(const b of document.querySelectorAll('[data-demo]'))b.onclick=()=>switchDemo(b.dataset.demo);
for(const b of document.querySelectorAll('[data-camera]'))b.onclick=()=>{stage.view(b.dataset.camera);document.querySelectorAll('[data-camera]').forEach(x=>x.classList.toggle('active',x===b));};
$('.demo-tabs').onkeydown=e=>{if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();const next=kind==='threading'?'claw':'threading';switchDemo(next).then(()=>$('#tab-'+next).focus());}};
$('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('#demo-stage').requestFullscreen();}catch(e){$('#fullscreen').title='Full screen is unavailable in this browser.';}};
document.addEventListener('visibilitychange',()=>{if(document.hidden)setPlaying(false);else stage?.draw();});
addEventListener('pagehide',()=>setPlaying(false));
document.addEventListener('keydown',e=>{
  if(!ready||['INPUT','SELECT','TEXTAREA','BUTTON','A','SUMMARY'].includes(document.activeElement?.tagName))return;
  if(e.code==='Space'){e.preventDefault();$('#play').click();}else if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();setPlaying(false);seek(time+(e.key==='ArrowLeft'?-5:5)).catch(showError);}
});
window.astraViewer={getState:()=>({ready,kind,time,playing,state,draws:stage?.drawCount,cacheSize:adapter?.cache?.size||0}),seek,setPlaying,switchDemo,getAdapter:()=>adapter,getStage:()=>stage};
try{stage=new Stage($('#view'));const requested=new URLSearchParams(location.search).get('demo');await switchDemo(requested==='threading'?'threading':'claw');}catch(e){showError(e);}
