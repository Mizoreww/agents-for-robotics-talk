from pathlib import Path
import json, shutil, hashlib, html
ROOT=Path('/home/limx/Desktop/agent_for_robotics');B=ROOT/'.build';OUT=ROOT/'output';PLAYER=OUT/'offline_player'
records=json.loads((B/'slide_records_focus.json').read_text());placements=json.loads((B/'video_placements_focus.json').read_text())
assert len(records)==22 and sum(r['minutes'] for r in records)==60
for sub in ['slides','media','posters']:(PLAYER/sub).mkdir(parents=True,exist_ok=True)
clips={}
for f in ['clip_manifest.json','revision_clips.json','enpire_clip_manifest.json']:
 for entry in json.loads((B/f).read_text()):clips[entry['name']]=entry
media=[]
for item in placements:
 stem=Path(item['file']).stem;meta=clips[stem]
 assert hashlib.sha256(Path(item['file']).read_bytes()).hexdigest()==meta['sha256']
 shutil.copy2(item['file'],PLAYER/'media'/(stem+'.mp4'));shutil.copy2(B/'assets'/(stem+'.jpg'),PLAYER/'posters'/(stem+'.jpg'))
 media.append({**item,**meta,'file':'media/'+stem+'.mp4','poster':'posters/'+stem+'.jpg','sourceUrl':item['sourceUrl']})
for r in records:shutil.copy2(B/'final_artifact_rendered'/f'{r["number"]:02d}.png',PLAYER/'slides'/f'{r["number"]:02d}.png')
# Only public content and portable paths are included in the companion.
for m in media:m.pop('source_file',None)
data=json.dumps({'slides':records,'media':media},ensure_ascii=False).replace('</','<\\/')
page='''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agents for Robotics — Focused Talk</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#eef1f0;color:#1a1a1a;font-family:"Noto Sans",Arial,sans-serif}
main{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 12px 20px;gap:9px}
#stage{position:relative;aspect-ratio:16/9;width:min(calc(100vw - 24px),calc((100vh - 112px)*16/9));background:white;box-shadow:0 3px 22px #18383218}
#slideImage{display:block;width:100%;height:100%}video{position:absolute;object-fit:contain;background:transparent}
nav{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:7px;max-width:96vw}
button,select{font:14px "Noto Sans",Arial,sans-serif;border:1px solid #b7ceca;border-radius:6px;padding:7px 11px;background:white;color:#215851;cursor:pointer}
button:hover{background:#e4f1ee}button:disabled{opacity:.45;cursor:default}select{max-width:44vw}#message{font-size:12px;color:#56746f;margin:0;min-height:16px}
#notes{max-width:1050px;padding:25px 36px;background:white;margin:15px auto;line-height:1.7;border-radius:8px;white-space:pre-wrap;font-size:17px}
#notes[hidden]{display:none}#notes a{color:#167e77}.help{font-size:12px;color:#65716e}body:fullscreen{background:#101716}
@media(max-width:700px){#stage{width:calc(100vw - 12px)}main{padding:6px;justify-content:flex-start}select{max-width:60vw}#notes{padding:18px;font-size:15px}}
@media print{nav,#message,.help{display:none}#stage{width:100vw;box-shadow:none}}
</style></head><body>
<main><div id="stage"><img id="slideImage" alt="Presentation slide"><div id="videos"></div></div>
<nav aria-label="Presentation controls"><button id="prev">Previous</button><label for="slideSelect">Slide</label><select id="slideSelect" aria-label="Slide"></select><button id="next">Next</button><button id="play">Play videos</button><button id="pause">Pause videos</button><button id="restart">Restart videos</button><button id="notesButton">Show notes</button><button id="full">Fullscreen</button></nav>
<p id="message" role="status" aria-live="polite"></p><div class="help">Arrow keys: navigate. Click each video for individual playback. Videos and slides work offline.</div>
</main><article id="notes" hidden aria-label="Speaker notes"></article>
<script id="deckData" type="application/json">'''+data+'''</script>
<script>
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
const initial=location.hash.match(/^#slide-(\\d+)$/);show(initial?Number(initial[1]):1);
</script></body></html>'''
# Python string escaping must not introduce raw newlines into JavaScript literals.
page=page.replace("+'\n\n'+slide.notes", "+'\\n\\n'+slide.notes")
(PLAYER/'index.html').write_text(page)
(PLAYER/'media_credits.json').write_text(json.dumps(media,ensure_ascii=False,indent=2))
notes=['# Agents for Robotics — Speaker Notes\n','22 slides. 60-minute suggested pacing including demonstrations and discussion.\n']
for r in records:notes.append(f'## {r["number"]}. {r["title"]}\n\n{r["notes"]}\n')
(OUT/'Speaker_Notes.md').write_text('\n'.join(notes))
outline=['# Agents for Robotics — Focused Talk\n','## 当前版本\n','依据最新反馈，正文从 36 页收敛至 **22 页**。只细讲 **Claude Plays Robotics、Agentic Real2Sim、ENPIRE**，保留约 60 分钟节奏（包含视频、机制解释与现场讨论）。其余工作只作为短 demo 或保留在调研材料里，不增加第四个细讲章节。\n','叙事：目标与问题 → 三个标杆的机制、证据与局限 → 综合理解与总结。Astra 应用视频穿插其中。\n','## 页序\n','| 页 | 标题 | 分钟 |\n|---:|---|---:|']
for r in records:outline.append(f'| {r["number"]} | {r["title"]} | {r["minutes"]:g} |')
outline+=['\n## 媒体与版式\n','- 15 个内嵌 MP4，其中两个由项目原始 GIF 转换。共 '+str(round(sum(m['duration_seconds'] for m in media)))+' 秒，均无额外加速。\n- 7 张原始论文/项目图；ENPIRE 的框架和 pin-insertion 结果仅做注明的区域裁剪，保留人类协助、坐标轴与图例。\n- 综合框图使用可编辑的原生形状，明确标为 synthesis。\n- 沿用参考 talk 的衬线标题、无衬线正文、白底青绿、SUSTech/CLEAR 与灰色脚注。\n- 引用、分母、重试/复位口径、人工介入和证据边界见每页英文讲稿。\n','## 保留材料\n','完整来源与未在正文展开的工作继续保存在 research/survey_notes.md 和 research/sources.json。旧 36 页方案保存在 .build/talk_outline_36_slides.md，不再是当前执行版本。']
(ROOT/'talk_outline.md').write_text('\n'.join(outline))
story=['# Focused Talk — Media Storyboard\n','Active delivery: 22 slides, three deep case studies, 15 embedded clips.\n','| Slide | Clip | Source interval | Duration | Primary source |\n|---:|---|---|---:|---|']
for m in media:story.append(f'| {m["slide"]} | {m["name"]} | {m["start_seconds"]:g}–{m["start_seconds"]+m["duration_seconds"]:g}s | {m["duration_seconds"]:.2f}s | [original]({m["sourceUrl"]}) |')
story+=['\nAll clips are H.264 / yuv420p, muted for live narration, with no additional speedup. The source itself may be edited or accelerated. Each delivered clip passed a full decode.','\nNative paper/project figures appear on slides 5, 7, 11, 12, 15, 17 and 18 as source images, as requested. The ENPIRE method panel retains human/environment/tool relationships; the pin panel retains axes and legends.','\nSocial demonstrations on slides 2, 9, 13 and 19 are not benchmark evidence. The microphone clip is explicitly kinematic replay. The hand is an unvalidated design artifact.','\nPPTX uses native editable text and synthesis diagrams. The offline player uses rendered backgrounds plus local positioned videos, so its fonts do not depend on the viewer machine.']
(ROOT/'research/media_storyboard.md').write_text('\n'.join(story))
print('Companion built:',len(records),'slides;',len(media),'videos;',round(sum(m['duration_seconds'] for m in media),2),'seconds')
