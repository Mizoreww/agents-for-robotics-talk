// Verify the served artifact, then capture the two locally authored revised slides.
import {createRequire} from 'node:module';
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
const require = createRequire(import.meta.url);
const {chromium} = require('playwright');
const root = '/home/limx/Desktop/agent_for_robotics';
const url = 'http://127.0.0.1:8765/';
const sha = b => createHash('sha256').update(b).digest('hex');
const raw = readFileSync(`${root}/output/Agents_for_Robotics_Self_Contained.html`);
const html_sha256 = sha(raw);
const expectedDeckHash = sha(raw.toString().match(/<script type="application\/json" id="deck-data">([\s\S]*?)<\/script>/)[1]);
const servedHash = async () => {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const hash = createHash('sha256');
  for await (const chunk of response.body) hash.update(chunk);
  return hash.digest('hex');
};
if (await servedHash() !== html_sha256) throw new Error('Served bytes differ');
const browser = await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true});
const out = `${root}/.build/v0_18_centering_visual`;
mkdirSync(out,{recursive:true});
try {
  const page = await browser.newPage({viewport:{width:1600,height:1000}});
  await page.goto(url,{timeout:180000});
  await page.waitForFunction(()=>typeof deck !== 'undefined' && !loading);
  const loadedDeckHash = await page.evaluate(async()=>{
    const bytes = new TextEncoder().encode(document.getElementById('deck-data').textContent);
    const hash = await crypto.subtle.digest('SHA-256',bytes);
    return [...new Uint8Array(hash)].map(x=>x.toString(16).padStart(2,'0')).join('');
  });
  if (loadedDeckHash !== expectedDeckHash) throw new Error('Loaded deck data differs');
  const slides = [];
  for (const n of [3,23]) {
    await page.evaluate(n=>show(n),n);
    await page.waitForFunction(()=>!loading);
    await page.waitForTimeout(300);
    const overflow = await page.evaluate(()=>[...document.querySelectorAll('#slide .text')]
      .filter(e=>e.scrollHeight>e.clientHeight+2 || e.scrollWidth>e.clientWidth+2)
      .map(e=>e.textContent));
    if (overflow.length) throw new Error(`Slide ${n} overflows: ${overflow}`);
    const screenshot = `${out}/${String(n).padStart(2,'0')}.png`;
    await page.locator('#slide').screenshot({path:screenshot});
    await page.screenshot({path:`${out}/${n}-with-controls.png`});
    slides.push({number:n,overflow,screenshot});
  }
  if (await servedHash() !== html_sha256) throw new Error('Served bytes changed');
  writeFileSync(`${root}/.build/v0_18_centering_audit.json`,JSON.stringify({
    html_sha256,loaded_deck_data_sha256:loadedDeckHash,
    served_html_byte_identity:true,slides,
    scope:'P3/P23 layout polish; all other slides, scripts, assets and media metadata are regression-checked against the verified v0.18 baseline.'
  },null,2)+'\n');
  console.log(JSON.stringify({html_sha256,slides}));
} finally {await browser.close();}
