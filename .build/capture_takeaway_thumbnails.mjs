// Capture the exact current P6/P17. Their deck records are frozen before this revision.
import {createRequire} from 'node:module';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const {chromium}=createRequire(import.meta.url)('playwright');
const root='/home/limx/Desktop/agent_for_robotics';
const dest=`${root}/.build/assets/v0_22`;
const sha=x=>createHash('sha256').update(x).digest('hex');
const baseline=JSON.parse(readFileSync(`${root}/.build/v0_22_baseline/deck.json`));
mkdirSync(dest,{recursive:true});
const browser=await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1304,height:900},deviceScaleFactor:2});
 await page.goto('http://127.0.0.1:8765/',{timeout:180000});
 await page.waitForFunction(()=>typeof deck!=='undefined'&&!loading);
 await page.evaluate(()=>document.fonts.ready);
 const captures=[];
 for(const n of [6,17]){
  assert.deepEqual(await page.evaluate(n=>deck.slides[n-1],n),baseline.slides[n-1]);
  await page.selectOption('#select',String(n));
  await page.waitForFunction(()=>!loading);
  await page.waitForTimeout(300);
  const file=`p${n}.png`;
  await page.locator('#slide').screenshot({path:`${dest}/${file}`});
  captures.push({slide:n,file,sha256:sha(readFileSync(`${dest}/${file}`)),source_html_sha256:sha(baseline.slides[n-1].html)});
 }
 writeFileSync(`${dest}/manifest.json`,JSON.stringify({captures},null,2));
 console.log('Captured exact P6/P17 thumbnails');
}finally{await browser.close();}
