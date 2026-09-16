import {createRequire} from 'node:module';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const {chromium}=createRequire(import.meta.url)('playwright');
const root='/home/limx/Desktop/agent_for_robotics';
const out=`${root}/.build/v0_22_visual`;
mkdirSync(out,{recursive:true});
const sha=x=>createHash('sha256').update(x).digest('hex');
const html=readFileSync(`${root}/output/Agents_for_Robotics_Self_Contained.html`,'utf8');
const html_sha256=sha(html);
const servedHash=async()=>{
 const response=await fetch('http://127.0.0.1:8765/');assert(response.ok);
 const hash=createHash('sha256');for await(const bytes of response.body)hash.update(bytes);
 return hash.digest('hex');
};
const browser=await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true});
try{
 assert.equal(await servedHash(),html_sha256);
 const page=await browser.newPage({viewport:{width:1600,height:1000}});
 await page.goto('http://127.0.0.1:8765/',{timeout:180000});
 await page.waitForFunction(()=>typeof deck!=='undefined'&&!loading);
 await page.evaluate(()=>document.fonts.ready);
 const loaded=await page.locator('#deck-data').textContent();
 assert.equal(sha(loaded),sha(html.match(/<script type="application\/json" id="deck-data">([\s\S]*?)<\/script>/)[1]));
 for(const n of [35,36]){
  await page.selectOption('#select',String(n));await page.waitForFunction(()=>!loading);
  await page.waitForTimeout(400);
  assert.equal(await page.locator('#slide .text').evaluateAll(es=>es.filter(e=>e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2).length),0);
  await page.locator('#slide').screenshot({path:`${out}/${n}.png`});
 }
 const thumbnails=page.locator('#slide img.original');assert.equal(await thumbnails.count(),2);
 for(let i=0;i<2;i++){
  const thumb=thumbnails.nth(i);const expected=await thumb.getAttribute('src');
  await thumb.click();
  assert.equal(await page.locator('#large-figure').getAttribute('src'),expected);
  await page.waitForFunction(()=>$('large-figure').complete&&$('large-figure').naturalWidth>0);
  await page.screenshot({path:`${out}/thumbnail-${i}.png`});
  await page.keyboard.press('Escape');
 }
 await page.click('#notes-toggle');await page.waitForTimeout(400);
 assert((await page.locator('#note-body').textContent()).includes('Sim2Real'));
 const slide=await page.locator('#stage').boundingBox(),notes=await page.locator('#notes').boundingBox();
 assert(slide.x+slide.width<=notes.x);
 await page.screenshot({path:`${out}/36-script.png`});
 assert.equal(await servedHash(),html_sha256);
 writeFileSync(`${root}/.build/v0_22_closing_audit.json`,JSON.stringify({html_sha256,loaded_deck_data_sha256:sha(loaded),slides:[35,36],thumbnail_enlargements:2,script_synced:true,overflows:0},null,2));
 console.log('Closing-page audit passed',html_sha256);
}finally{await browser.close();}
