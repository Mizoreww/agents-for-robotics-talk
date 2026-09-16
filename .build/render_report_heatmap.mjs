import {createRequire} from 'node:module';
import {readFileSync,writeFileSync} from 'node:fs';
const require=createRequire(import.meta.url);const {chromium}=require('playwright');
const root='/home/limx/Desktop/agent_for_robotics/.build/assets/v0_13';
const source=JSON.parse(readFileSync(`${root}/heatmap_dom.json`));
const browser=await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true});
const page=await browser.newPage({viewport:{width:1240,height:1100},deviceScaleFactor:2});
// Render an offline original DOM capture. No report code runs and no requests leave the renderer.
await page.route('**/*',route=>route.abort());
await page.setContent('<!doctype html><html><meta charset="UTF-8"><body>'+source.html+'</body></html>');
const audit=await page.evaluate(source=>{
 const root=document.querySelector('section');const els=[root,...root.querySelectorAll('*')];
 if(els.length!==source.styles.length)throw Error('DOM closure differs');
 for(let i=0;i<els.length;i++)for(const [k,v]of source.styles[i].style)els[i].style.setProperty(k,v);
 document.body.style.cssText='margin:0;padding:12px;background:white;width:1216px';
 for(const e of els){
  if(['SECTION','DIV','HEADER','TABLE','THEAD','TBODY','TR','TD','TH'].includes(e.tagName)){
   e.style.setProperty('height','auto');e.style.setProperty('max-height','none');
   e.style.setProperty('overflow','visible');e.style.setProperty('width','auto');e.style.setProperty('max-width','none');
  }
 }
 root.style.width='1216px';root.querySelector('table').style.width='1216px';
 for(const b of root.querySelectorAll('button'))b.style.visibility='hidden';
 const cells=[...root.querySelectorAll('td,th')].map(e=>e.innerText);
 const expected=source.styles.filter(e=>e.text!==null).map(e=>e.text);
 if(JSON.stringify(cells)!==JSON.stringify(expected))throw Error('Cell text changed');
 const r=root.getBoundingClientRect();
 const outside=[...root.querySelectorAll('td,th')].filter(e=>{let b=e.getBoundingClientRect();return b.right>r.right+.5||b.bottom>r.bottom+.5}).length;
 if(outside)throw Error('Cells outside export');
 return {cells,rows:root.querySelectorAll('tr').length,width:r.width,height:r.height,layout_change:'Only expand original DOM overflow/width and automatic heights; preserve cell content, source styles and colors.'};
},source);
await page.locator('section').first().screenshot({path:`${root}/task-score-table-complete.png`});
writeFileSync(`${root}/heatmap_render_audit.json`,JSON.stringify(audit,null,2));await browser.close();console.log({rows:audit.rows,width:audit.width,height:audit.height});
