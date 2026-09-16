// Verify the academic footers at the existing size, color and position.
import {createRequire} from 'node:module';
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const require = createRequire(import.meta.url);
const {chromium} = require('playwright');
const root = '/home/limx/Desktop/agent_for_robotics';
const html = readFileSync(`${root}/output/Agents_for_Robotics_Self_Contained.html`, 'utf8');
const sha = data => createHash('sha256').update(data).digest('hex');
const html_sha256 = sha(html);
const servedHash = async () => {
  const response = await fetch('http://127.0.0.1:8765/');
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const hash = createHash('sha256');
  for await (const bytes of response.body) hash.update(bytes);
  return hash.digest('hex');
};
const browser = await chromium.launch({executablePath:'/opt/google/chrome/chrome', headless:true});
try {
  if (await servedHash() !== html_sha256) throw new Error('Served bytes differ');
  const page = await browser.newPage({viewport:{width:1600,height:1000}});
  await page.goto('http://127.0.0.1:8765/', {timeout:180000});
  await page.waitForFunction(() => typeof deck !== 'undefined' && !loading);
  const dom = await page.locator('#deck-data').textContent();
  const expected = html.match(/<script type="application\/json" id="deck-data">([\s\S]*?)<\/script>/)[1];
  if (sha(dom) !== sha(expected)) throw new Error('Loaded deck differs');
  const footers = [];
  for (let number=23;number<=34;number++) {
    await page.evaluate(n => show(n), number);
    await page.waitForFunction(() => !loading);
    const record = await page.locator('.footer').evaluate((e, number) => {
      const css=getComputedStyle(e);
      return {number, text:e.textContent, left:e.offsetLeft, top:e.offsetTop,
        bottom:e.offsetTop+e.offsetHeight, width:e.clientWidth, scrollWidth:e.scrollWidth,
        fontSize:css.fontSize, fontFamily:css.fontFamily, color:css.color};
    }, number);
    if (record.bottom>720 || record.scrollWidth>record.width || record.left!==64 ||
        record.top!==678 || record.fontSize!=='11px' || record.color!=='rgb(119, 119, 111)') {
      throw new Error(`Footer layout changed: ${JSON.stringify(record)}`);
    }
    footers.push(record);
  }
  if (await servedHash() !== html_sha256) throw new Error('Served bytes changed');
  writeFileSync(`${root}/.build/v0_19_citation_layout_audit.json`,
    JSON.stringify({html_sha256, loaded_deck_data_sha256:sha(dom), footers},null,2));
  console.log(`12 academic footers fit at unchanged size/color/position: ${html_sha256}`);
} finally {
  await browser.close();
}
