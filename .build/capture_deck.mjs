import {createRequire} from 'node:module';
import {mkdirSync} from 'node:fs';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const dest=process.argv[2]; mkdirSync(dest,{recursive:true});
const browser=await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true,args:['--mute-audio']});
const page=await browser.newPage({viewport:{width:1600,height:1000}});
await page.goto('http://127.0.0.1:8765/',{timeout:180000});
await page.waitForFunction(()=>typeof deck!=='undefined');
for(let n=1;n<=await page.evaluate(()=>deck.slides.length);n++){
 await page.evaluate(n=>show(n),n); await page.waitForFunction(()=>!loading);
 // Decode a frame before capturing: metadata alone can leave a loading spinner.
 await page.evaluate(async()=>{for(const v of document.querySelectorAll('#slide video')) await v.play();});
 await page.waitForTimeout(700);
 await page.evaluate(()=>{for(const v of document.querySelectorAll('#slide video')) v.pause();});
 await page.waitForTimeout(200);
 await page.locator('#slide').screenshot({path:`${dest}/${String(n).padStart(2,'0')}.png`});
}
await page.screenshot({path:`${dest}/controls.png`});
await page.setViewportSize({width:390,height:844}); await page.waitForTimeout(300);
await page.screenshot({path:`${dest}/mobile.png`});
await browser.close();
