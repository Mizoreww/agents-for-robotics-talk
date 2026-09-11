
'use strict';
const deck=JSON.parse(document.getElementById('deckData').textContent);
const el=id=>document.getElementById(id);let current=1;
for(const s of deck.slides){const o=document.createElement('option');o.value=s.number;o.textContent=s.number+' / '+deck.slides.length+' — '+s.title;el('slideSelect').append(o)}
const activeVideos=()=>[...document.querySelectorAll('video')];
function pause(){for(const v of activeVideos())v.pause()}
function show(n){pause();current=Math.max(1,Math.min(deck.slides.length,Number(n)));const slide=deck.slides[current-1];el('slideSelect').value=String(current);el('slideImage').src='slides/'+String(current).padStart(2,'0')+'.png';el('slideImage').alt='Slide '+current+': '+slide.title;el('videos').replaceChildren();
 const clips=deck.media.filter(m=>m.slide===current);for(const m of clips){const v=document.createElement('video');v.src=m.file;v.poster=m.poster;v.controls=true;v.playsInline=true;v.preload='metadata';v.muted=true;v.setAttribute('aria-label',m.name+' video');v.dataset.clip=m.name;v.style.cssText='left:'+m.x/12.8+'%;top:'+m.y/7.2+'%;width:'+m.w/12.8+'%;height:'+m.h/7.2+'%;';v.addEventListener('error',()=>{el('message').textContent='Video could not load: '+m.name+'. Keep the media folder beside this file.'});el('videos').append(v)}
 el('notes').textContent='SLIDE '+current+' · '+slide.title+'\n\n'+slide.notes;el('message').textContent=clips.length?clips.length+' offline video'+(clips.length>1?'s':'')+' on this slide.':'No video on this slide.';
 for(const id of ['play','pause','restart'])el(id).disabled=!clips.length;el('prev').disabled=current===1;el('next').disabled=current===deck.slides.length;history.replaceState(null,'','#slide-'+current);
}
el('prev').onclick=()=>show(current-1);el('next').onclick=()=>show(current+1);el('slideSelect').onchange=e=>show(e.target.value);
el('play').onclick=async()=>{try{await Promise.all(activeVideos().map(v=>v.play()));el('message').textContent='Playing '+activeVideos().length+' video'+(activeVideos().length>1?'s':'')+'.'}catch(e){el('message').textContent='Please use the play control on each video.'}};
el('pause').onclick=()=>{pause();el('message').textContent='Videos paused.'};el('restart').onclick=()=>{pause();for(const v of activeVideos())v.currentTime=0;el('message').textContent='Videos reset to the beginning.'};
el('notesButton').onclick=()=>{el('notes').hidden=!el('notes').hidden;el('notesButton').textContent=el('notes').hidden?'Show notes':'Hide notes';if(!el('notes').hidden)el('notes').scrollIntoView({behavior:'smooth',block:'start'})};
el('full').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();
document.addEventListener('keydown',e=>{if(['SELECT','INPUT','TEXTAREA'].includes(e.target.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();show(current+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(current-1)}});
const initial=location.hash.match(/^#slide-(\d+)$/);show(initial?Number(initial[1]):1);
