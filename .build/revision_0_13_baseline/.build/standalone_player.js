'use strict';
const $=id=>document.getElementById(id);
const deck=JSON.parse($('deck-data').textContent);
let current=1,epoch=0,urls=[],loading=false,allScript=false;
const videos=()=>Array.from($('slide').querySelectorAll('video'));
const assetURL=key=>'data:'+deck.assets[key].mime+';base64,'+deck.assets[key].data;
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const groups=new Map();
for(const s of deck.slides){
 let g=groups.get(s.group);if(!g){g=document.createElement('optgroup');g.label=s.group;groups.set(s.group,g);$('select').append(g)}
 const o=document.createElement('option');o.value=s.number;o.textContent=String(s.number).padStart(2,'0')+' / '+deck.slides.length+' · '+s.title;g.append(o);
}
function resize(){const scale=$('stage').getBoundingClientRect().width/1280;$('slide').style.transform='scale('+scale+')'}
new ResizeObserver(resize).observe($('stage'));
function pause(){for(const v of videos())v.pause()}
function dispose(){
 for(const v of videos()){v.pause();v.removeAttribute('src');v.load()}
 for(const u of urls)URL.revokeObjectURL(u);urls=[];
}
async function materialize(id,token){
 const b64=$(id).textContent.trim(),chunks=[];
 for(let offset=0;offset<b64.length;offset+=524288){
  if(token!==epoch)return null;
  const raw=atob(b64.slice(offset,offset+524288));const bytes=new Uint8Array(raw.length);
  for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);chunks.push(bytes);
  if(offset%2097152===0)await new Promise(resolve=>setTimeout(resolve,0));
 }
 return new Blob(chunks,{type:'video/mp4'});
}
function controls(hasMedia){for(const id of ['play','pause','restart'])$(id).disabled=!hasMedia||loading}
function notes(s){
 if(allScript){
  $('note-title').textContent='Agents for Robotics · Full script';
  $('timing').textContent='中文讲稿 · 专有名词保留英文 · '+deck.slides.length+' slides · 约 '+deck.slides.reduce((total,s)=>total+s.minutes,0)+' 分钟，含视频、读图与停顿';
  $('note-body').innerHTML=deck.slides.map(p=>'<section class="script-section"><h2>'+String(p.number).padStart(2,'0')+'. '+escapeHTML(p.title)+'</h2>'+p.notesHtml+(p.sources.length?'<div class="section-sources">'+p.sources.map(q=>'<a target="_blank" rel="noopener noreferrer" href="'+escapeHTML(q.url)+'">'+escapeHTML(q.label)+'</a>').join(' · ')+'</div>':'')+'</section>').join('');
  $('sources').innerHTML='';return;
 }

 $('note-title').textContent=String(s.number).padStart(2,'0')+'. '+s.title;
 const start=Math.floor(s.startMinutes)+':'+(s.startMinutes%1?'30':'00');
 $('timing').textContent='Suggested start '+start+' · '+s.minutes+' minutes including media, figure walkthrough and pauses';
 $('note-body').innerHTML=s.notesHtml;
 const srcs=[...s.sources];for(const m of deck.media.filter(m=>m.slide===s.number)){if(!srcs.some(x=>x.url===m.sourceUrl))srcs.push({label:'Original video · '+m.name,url:m.sourceUrl})}
 $('sources').innerHTML=srcs.length?'<strong>Primary sources</strong><ul>'+srcs.map(x=>'<li><a target="_blank" rel="noopener noreferrer" href="'+escapeHTML(x.url)+'">'+escapeHTML(x.label)+'</a></li>').join('')+'</ul>':'';
}
async function show(number){
 const token=++epoch;dispose();current=Math.max(1,Math.min(deck.slides.length,Number(number)||1));
 const s=deck.slides[current-1];loading=true;$('select').value=String(current);
 const defs='<svg width="0" height="0" aria-hidden="true"><defs><marker id="gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#646464"/></marker><marker id="teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#2ba39b"/></marker></defs></svg>';
 const footer=s.sources.length?'<a href="'+escapeHTML(s.sources[0].url)+'" target="_blank" rel="noopener noreferrer">'+escapeHTML(s.footer)+'</a>':escapeHTML(s.footer);
 $('slide').innerHTML=defs+s.html+'<div class="footer">'+footer+'</div><div class="page-no">'+current+'</div>';
 $('slide').setAttribute('aria-label','Slide '+current+': '+s.title);$('slide').dataset.slide=String(current);
 for(const im of $('slide').querySelectorAll('img[data-asset]'))im.src=assetURL(im.dataset.asset);
 notes(s);resize();$('prev').disabled=current===1;$('next').disabled=current===deck.slides.length;
 const clips=deck.media.filter(m=>m.slide===current);controls(clips.length);
 $('message').textContent=clips.length?'Preparing embedded video'+(clips.length>1?'s':'')+'…':'Slide '+current+' / '+deck.slides.length+' · '+s.group;
 try{history.replaceState(null,'','#slide-'+current)}catch(_){/* File readers may restrict history. */}
 for(const m of clips){
  const v=document.createElement('video');v.controls=true;v.playsInline=true;v.muted=true;v.preload='auto';v.poster=assetURL(m.posterKey);v.dataset.clip=m.name;v.setAttribute('aria-label',m.name+' video');
  v.style.cssText='left:'+m.x+'px;top:'+m.y+'px;width:'+m.w+'px;height:'+m.h+'px;';$('slide').append(v);
  v.addEventListener('error',()=>{if(token===epoch)$('message').textContent='This browser could not decode '+m.name+'. Open the HTML in a current desktop Chrome or Edge browser.'});
  try{
   const blob=await materialize(m.payloadId,token);if(token!==epoch||!blob)return;
   const u=URL.createObjectURL(blob);urls.push(u);v.src=u;
  }catch(_){if(token===epoch){loading=false;$('message').textContent='Video preparation failed. Try reopening this file in a desktop browser.'}return}
 }
 if(token!==epoch)return;loading=false;controls(clips.length);
 if(clips.length)$('message').textContent=clips.length+' embedded video'+(clips.length>1?'s':'')+' ready · no Internet required';
}
async function play(){
 if(loading||!videos().length)return;
 try{await Promise.all(videos().map(v=>v.play()));$('message').textContent='Playing '+videos().length+' video'+(videos().length>1?'s':'')+'.'}catch(_){$('message').textContent='Use the play control on the video to begin.'}
}
$('prev').onclick=()=>show(current-1);$('next').onclick=()=>show(current+1);$('select').onchange=e=>show(e.target.value);
$('play').onclick=play;$('pause').onclick=()=>{pause();$('message').textContent='Videos paused.'};
$('restart').onclick=()=>{pause();for(const v of videos())v.currentTime=0;$('message').textContent='Videos reset to the beginning.'};
$('notes-toggle').onclick=()=>{const open=$('notes').hidden;$('notes').hidden=!open;$('notes-toggle').setAttribute('aria-expanded',String(open));$('notes-toggle').querySelector('span').textContent=open?'Hide script':'Speaker script';if(open)$('notes').scrollIntoView({behavior:'smooth',block:'start'})};
$('all-script').onclick=()=>{allScript=!allScript;$('all-script').querySelector('span').textContent=allScript?'Current slide':'Full script';$('all-script').setAttribute('aria-pressed',String(allScript));notes(deck.slides[current-1]);$('notes').scrollIntoView({block:'start'})};
function focusView(on){document.body.classList.toggle('focus-view',on);$('fullscreen').setAttribute('aria-pressed',String(on));$('fullscreen').querySelector('span').textContent=on?'Exit view':'Fullscreen';resize()}
$('fullscreen').onclick=()=>{
 if(document.body.classList.contains('focus-view')){
  focusView(false);if(document.fullscreenElement){try{document.exitFullscreen().catch(()=>{})}catch(_){}}return;
 }
 focusView(true);
 try{document.documentElement.requestFullscreen().catch(()=>{})}catch(_){/* Focus view remains available without native fullscreen. */}
};
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement)focusView(false)});
function openFigure(im){$('large-figure').src=im.src;$('large-figure').alt=im.alt;$('figure-caption').textContent=im.alt;$('figure-dialog').showModal()}
$('slide').addEventListener('click',e=>{if(e.target.matches('img.original'))openFigure(e.target)});
$('slide').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches('img.original'))openFigure(e.target)});
$('close-figure').onclick=()=>$('figure-dialog').close();
$('figure-dialog').addEventListener('click',e=>{if(e.target===$('figure-dialog'))$('figure-dialog').close()});
document.addEventListener('keydown',e=>{
 if($('figure-dialog').open||['SELECT','INPUT','TEXTAREA'].includes(e.target.tagName))return;
 if(e.key==='ArrowRight'){e.preventDefault();show(current+1)}
 else if(e.key==='ArrowLeft'){e.preventDefault();show(current-1)}
 else if(e.key==='Home'){e.preventDefault();show(1)}else if(e.key==='End'){e.preventDefault();show(deck.slides.length)}
 else if(e.key===' '&&e.target.tagName!=='BUTTON'){e.preventDefault();videos().some(v=>!v.paused)?pause():play()}
 else if(e.key.toLowerCase()==='n')$('notes-toggle').click();else if(e.key.toLowerCase()==='f')$('fullscreen').click();
});
window.addEventListener('pagehide',dispose);
const initial=location.hash.match(/^#slide-(\d+)$/);show(initial?Number(initial[1]):1);
