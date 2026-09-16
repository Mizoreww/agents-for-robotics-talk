// Additional v0.8 verification: original-figure screenshots and whole new-clip playback.
// Visual inspection is recorded separately; playback progression is not experiment validation.
import {createRequire} from 'node:module';
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const require = createRequire(import.meta.url);
const {chromium} = require('playwright');
const root = '/home/limx/Desktop/agent_for_robotics';
const sha = b => createHash('sha256').update(b).digest('hex');
const html_sha256 = sha(readFileSync(`${root}/output/Agents_for_Robotics_Self_Contained.html`));
const streamServedHash = async () => {
  const response = await fetch('http://127.0.0.1:8765/');
  if (!response.ok) throw new Error(`Loopback HTTP ${response.status}`);
  const hash = createHash('sha256');
  for await (const chunk of response.body) hash.update(chunk);
  return hash.digest('hex');
};
const browser = await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true,args:['--mute-audio','--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling']});
try {
  const page = await browser.newPage({viewport:{width:1600,height:1000}});
  // Stream outside CDP: neither the inspector cache nor route.fulfill handles this huge body reliably.
  if (await streamServedHash() !== html_sha256) throw new Error('Served HTML differs before navigation');
  await page.goto('http://127.0.0.1:8765/',{timeout:180000});
  await page.waitForFunction(()=>typeof deck !== 'undefined' && !loading);
  const loadedDeckHash = await page.evaluate(async()=>{
    const bytes=new TextEncoder().encode(document.getElementById('deck-data').textContent);
    const digest=await crypto.subtle.digest('SHA-256',bytes);
    return [...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,'0')).join('');
  });
  const expectedDeck = readFileSync(`${root}/output/Agents_for_Robotics_Self_Contained.html`,'utf8').match(/<script type="application\/json" id="deck-data">([\s\S]*?)<\/script>/)[1];
  if (loadedDeckHash !== sha(expectedDeck)) throw new Error('Loaded deck data differs from delivery');
  const go = async n => {await page.evaluate(n=>show(n),n);await page.waitForFunction(()=>!loading);await page.waitForTimeout(200);};
  const figures=[];
  for (const [n,index] of [[5,0],[5,1],[5,2],[12,0],[16,0],[21,0],[23,0]]) {
    await go(n);await page.locator('#slide img.original').nth(index).click();
    await page.waitForFunction(()=>document.getElementById('large-figure').complete);
    const file=`${root}/.build/v0_8_visual/figure-${n}-${index}.png`;
    await page.screenshot({path:file});
    figures.push({slide:n,index,file});
    await page.keyboard.press('Escape');
  }
  const playback=[];
  for (const [n,name] of [[10,'keyboard'],[18,'office_newton'],[25,'quad_rl'],[11,'asim_delta'],[11,'asim_waypoint']]) {
    await go(n);
    const video=page.locator(`video[data-clip="${name}"]`);
    await video.evaluate(async v=>{v.loop=false;v.currentTime=0;v.playbackRate=1;await v.play();});
    const samples=[];
    let ended=false;
    for (let i=0;i<45;i++) {
      await page.waitForTimeout(1000);
      const sample=await video.evaluate(v=>({time:v.currentTime,duration:v.duration,ended:v.ended,paused:v.paused,error:v.error?.code??null,frames:v.getVideoPlaybackQuality().totalVideoFrames}));
      samples.push(sample);
      if (sample.error) throw new Error(`Decode error ${name}`);
      if (sample.ended) {ended=true;break;}
      if (i>2 && sample.time<=samples[i-2].time) throw new Error(`Playback stalled: ${name}`);
    }
    if (!ended) throw new Error(`Playback did not complete: ${name}`);
    playback.push({slide:n,clip:name,samples,ended});
  }
  await go(10);await page.keyboard.press('n');
  await page.screenshot({path:`${root}/.build/v0_8_visual/script-desktop.png`});
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:`${root}/.build/v0_8_visual/script-mobile.png`,fullPage:true});
  if (await streamServedHash() !== html_sha256) throw new Error('Served HTML changed during audit');
  const report={html_sha256,served_html_byte_identity:true,loaded_deck_data_sha256:loadedDeckHash,identity_check:'Streamed HTTP bytes before/after browser run plus SHA-256 of actual loaded deck-data DOM',figures,playback,scope:'Complete uninterrupted playback at 1x presentation rate; source speedups retained. Separate visual review uses sequential 1-second samples.'};
  writeFileSync(`${root}/.build/v0_8_extended_audit.json`,JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({html_sha256,figures:figures.length,completeClips:playback.map(x=>x.clip)}));
} finally {await browser.close();}
