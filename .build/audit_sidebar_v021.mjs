// Real-browser regression for the docked script, bound to served and loaded bytes.
import {createRequire} from 'node:module';
import {readFileSync, writeFileSync, mkdirSync, rmSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root='/home/limx/Desktop/agent_for_robotics';
const out=`${root}/.build`;
const url=process.argv[2]||'http://127.0.0.1:8765/';
const sha=data=>createHash('sha256').update(data).digest('hex');
const html=readFileSync(`${root}/output/Agents_for_Robotics_Self_Contained.html`,'utf8');
const html_sha256=sha(html);
const expectedData=html.match(/<script type="application\/json" id="deck-data">([\s\S]*?)<\/script>/)[1];
// Content revisions are tested separately; this UI audit binds the current served deck.
const servedHash=async()=>{
 const response=await fetch(url);assert(response.ok);
 const hash=createHash('sha256');
 for await(const bytes of response.body)hash.update(bytes);
 return hash.digest('hex');
};
const auditFile=`${out}/v0_21_sidebar_audit.json`;
rmSync(auditFile,{force:true});
mkdirSync(`${out}/v0_21_visual`,{recursive:true});
const browser=await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true,
 args:['--autoplay-policy=no-user-gesture-required','--mute-audio']});
const audit={html_sha256,loaded_deck_data_sha256:sha(expectedData),layouts:[],checks:[],errors:[]};
try{
 assert.equal(await servedHash(),html_sha256);
 const page=await browser.newPage({viewport:{width:1600,height:1000}});
 page.on('pageerror',e=>audit.errors.push(e.message));
 await page.goto(url,{timeout:180000});
 await page.waitForFunction(()=>typeof deck!=='undefined'&&!loading);
 await page.evaluate(()=>document.fonts.ready);
 assert.equal(sha(await page.locator('#deck-data').textContent()),sha(expectedData));
 const settle=()=>page.waitForTimeout(380);
 const go=async n=>{await page.selectOption('#select',String(n));await page.waitForFunction(()=>!loading);};
 const measure=()=>page.evaluate(()=>{
  const rect=id=>{const r=document.getElementById(id).getBoundingClientRect();
   return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
  const main=document.querySelector('main').getBoundingClientRect();
  return {viewport:innerWidth,height:innerHeight,docWidth:document.documentElement.scrollWidth,
   docHeight:document.documentElement.scrollHeight,stage:rect('stage'),canvas:rect('slide'),
   notes:rect('notes'),main:{left:main.left,right:main.right,bottom:main.bottom},
   buttons:[...document.querySelectorAll('.toolbar button,.toolbar select,#notes button')]
    .filter(e=>e.offsetParent!==null).map(e=>{const r=e.getBoundingClientRect();
     return {id:e.id,left:r.left,right:r.right,top:r.top,bottom:r.bottom};}),
   open:document.body.classList.contains('script-open')};
 });
 const checkLayout=(m,label)=>{
  assert(m.docWidth<=m.viewport+1,`${label}: document width`);
  assert(m.stage.width>150,`${label}: visible stage`);
  assert(Math.abs(m.stage.width/m.stage.height-16/9)<.01,`${label}: aspect ratio`);
  assert(Math.abs(m.canvas.width-m.stage.width)<1,`${label}: canvas fits`);
  assert(m.stage.left>=m.main.left&&m.stage.right<=m.main.right+1,`${label}: stage contained`);
  for(const b of m.buttons){assert(b.left>=0&&b.right<=m.viewport+1,`${label}: ${b.id} overflow`);}
  if(m.open&&m.viewport>700){
   assert(m.stage.right<=m.notes.left+1,`${label}: slide covered`);
   assert(m.docHeight<=m.height+1,`${label}: page scrolls instead of script`);
   assert(m.notes.width>=320,`${label}: readable script`);
   for(const b of m.buttons.filter(b=>!['notes-close','all-script'].includes(b.id)))
    assert(b.right<=m.notes.left+1,`${label}: toolbar covered`);
  }else if(m.open){assert(m.notes.top>=m.main.bottom-1,`${label}: mobile overlap`);}
  audit.layouts.push({label,...m});
 };
 await go(33);
 const closed=await measure();checkLayout(closed,'desktop-closed');
 await page.screenshot({path:`${out}/v0_21_visual/desktop-closed.png`});
 // Sample the real animation, including rapidly changing stage geometry.
 await page.evaluate(()=>{
  window.dockFrames=[];
  const end=performance.now()+700;
  function sample(){
   const s=$('stage').getBoundingClientRect(),n=$('notes').getBoundingClientRect();
   if(document.body.classList.contains('script-open'))window.dockFrames.push({right:s.right,left:n.left,width:s.width});
   if(performance.now()<end)requestAnimationFrame(sample);
  }requestAnimationFrame(sample);
 });
 await page.click('#notes-toggle');await settle();
 const open=await measure();checkLayout(open,'desktop-open');
 assert(open.stage.width<closed.stage.width-100);
 assert.equal(await page.getAttribute('#notes-toggle','aria-expanded'),'true');
 assert.equal(await page.locator('#notes-close').evaluate(e=>e===document.activeElement),true);
 assert.equal(await page.locator('#notes').evaluate(e=>e.inert),false);
 await page.screenshot({path:`${out}/v0_21_visual/desktop-open.png`});
 await page.waitForTimeout(400);
 const frames=await page.evaluate(()=>window.dockFrames);
 assert(frames.length>=5);assert(frames.every(f=>f.right<=f.left+1),'animation overlap');
 assert(new Set(frames.map(f=>Math.round(f.width))).size>2,'stage did not animate');
 audit.animationFrames=frames;
 await page.click('#all-script');await settle();
 assert.equal(await page.locator('.script-section').count(),37);
 await page.locator('#notes-scroll').evaluate(e=>e.scrollTop=1400);
 assert(await page.locator('#notes-scroll').evaluate(e=>e.scrollTop)>500);
 assert.equal(await page.evaluate(()=>scrollY),0);
 const headerBefore=await page.locator('#notes header').boundingBox();
 await page.locator('#notes-scroll').evaluate(e=>e.scrollTop+=800);
 assert.deepEqual(await page.locator('#notes header').boundingBox(),headerBefore);
 await page.screenshot({path:`${out}/v0_21_visual/full-script.png`});
 await page.click('#all-script');
 assert.equal(await page.locator('#notes-scroll').evaluate(e=>e.scrollTop),0);
 await page.click('#next');await page.waitForFunction(()=>!loading);
 assert((await page.locator('#note-title').textContent()).startsWith('34.'));
 await page.locator('#notes-scroll').focus();
 await page.keyboard.press('Home');assert.equal(await page.inputValue('#select'),'34');
 await page.keyboard.press('Escape');await settle();
 assert(await page.locator('#notes').evaluate(e=>e.hidden&&e.inert));
 assert(await page.locator('#notes-toggle').evaluate(e=>e===document.activeElement));
 assert(Math.abs((await measure()).stage.width-closed.stage.width)<1);
 audit.checks.push('animation has no overlap','independent scrolling and fixed header','full/current script and slide sync','Escape and focus restoration');
 // Quick reversals must not leave an obsolete hide timer active.
 await page.evaluate(()=>{setScriptOpen(true);setScriptOpen(false);setScriptOpen(true);});
 await settle();assert(await page.locator('#notes').evaluate(e=>!e.hidden&&!e.inert));
 await page.click('#notes-close');await settle();
 await page.keyboard.press('n');await settle();assert.equal(await page.getAttribute('#notes-toggle','aria-expanded'),'true');
 await page.keyboard.press('n');await settle();assert.equal(await page.getAttribute('#notes-toggle','aria-expanded'),'false');
 await page.click('#notes-toggle');await settle();
 await page.locator('#select').focus();await page.keyboard.press('Escape');await settle();
 assert.equal(await page.getAttribute('#notes-toggle','aria-expanded'),'false');
 assert(await page.locator('#select').evaluate(e=>e===document.activeElement));
 audit.checks.push('rapid reversals','N toggle and Close button');
 audit.checks.push('Escape with focused slide selector');
 // Neither video identity nor the playhead may reset when docking.
 await go(33);
 await page.click('#play');await page.waitForTimeout(1100);
 await page.evaluate(()=>{window.beforeDockVideos=videos();window.beforeDockTimes=videos().map(v=>v.currentTime);});
 await page.click('#notes-toggle');await settle();
 await page.click('#notes-close');await settle();
 const playback=await page.evaluate(()=>videos().map((v,i)=>({same:v===window.beforeDockVideos[i],
  before:window.beforeDockTimes[i],after:v.currentTime,paused:v.paused,error:v.error?.code??null})));
 assert(playback.length===4&&playback.every(v=>v.same&&!v.paused&&!v.error&&v.after>v.before));
 audit.playback=playback;await page.click('#pause');
 await page.click('#notes-toggle');await settle();
 await page.click('#fullscreen');await settle();
 assert(await page.evaluate(()=>document.body.classList.contains('focus-view')));
 audit.nativeFullscreen=await page.evaluate(()=>!!document.fullscreenElement);
 checkLayout(await measure(),'fullscreen-open');
 await page.keyboard.press('f');await settle();
 await go(5);await page.click('#slide img.original');
 await page.keyboard.press('Escape');await settle();
 assert(!(await page.locator('#figure-dialog').evaluate(e=>e.open)));
 assert.equal(await page.getAttribute('#notes-toggle','aria-expanded'),'true');
 audit.checks.push('video playback remains continuous','fullscreen split layout','figure Escape precedence');
 for(const [width,height] of [[1280,800],[1024,768],[820,430],[701,500],[390,844],[568,320]]){
  await page.setViewportSize({width,height});await settle();
  checkLayout(await measure(),`${width}x${height}-open`);
  assert(await page.locator('#notes-scroll').evaluate(e=>{
   const css=getComputedStyle(e);
   return e.clientHeight-parseFloat(css.paddingTop)-parseFloat(css.paddingBottom)>=100;
  }),`${width}x${height}: script reading area too short`);
  await page.screenshot({path:`${out}/v0_21_visual/${width}-open.png`,fullPage:width<=700});
  await page.click('#notes-close');await settle();checkLayout(await measure(),`${width}x${height}-closed`);
  await page.click('#notes-toggle');await settle();
 }
 await page.setViewportSize({width:1280,height:800});
 await page.emulateMedia({reducedMotion:'reduce'});await settle();
 assert.equal(await page.locator('.presenter').evaluate(e=>getComputedStyle(e).transitionDuration),'0s');
 await page.keyboard.press('n');await page.waitForTimeout(50);
 assert(await page.locator('#notes').evaluate(e=>e.hidden));
 await page.keyboard.press('n');await page.waitForTimeout(50);checkLayout(await measure(),'reduced-motion');
 await page.click('#notes-close');await settle();
 await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('main').evaluate(e=>getComputedStyle(e).display),'none');
 assert.equal(await page.locator('#notes').evaluate(e=>getComputedStyle(e).display),'block');
 assert.equal(await page.locator('#notes-scroll').evaluate(e=>getComputedStyle(e).overflowY),'visible');
 audit.checks.push('responsive desktop and stacked mobile','reduced motion','print layout');
 assert.deepEqual(audit.errors,[]);
 assert.equal(await servedHash(),html_sha256);
 writeFileSync(auditFile,JSON.stringify(audit,null,2));
 console.log(`Sidebar checks passed: ${html_sha256}`);
}finally{await browser.close();}
