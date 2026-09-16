// Browser audits for the self-contained deck, bound to the current HTML hash.
// Runs Google Chrome (H.264-capable) through Playwright against the loopback copy in standalone_isolation.
// Usage: NODE_PATH=qa_deps/node_modules node browser_audit.mjs [http://127.0.0.1:8765/]
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const B = '/home/limx/Desktop/agent_for_robotics/.build/';
const html = readFileSync('/home/limx/Desktop/agent_for_robotics/output/Agents_for_Robotics_Self_Contained.html');
const html_sha256 = createHash('sha256').update(html).digest('hex');
const url = process.argv[2] || 'http://127.0.0.1:8765/';
const browser = await chromium.launch({ executablePath: '/opt/google/chrome/chrome', headless: true, args: ['--disable-background-timer-throttling', '--autoplay-policy=no-user-gesture-required', '--mute-audio'] });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.on('pageerror', e => console.error('pageerror', e.message));
await page.goto(url, { waitUntil: 'load', timeout: 180000 });
await page.waitForFunction(() => typeof deck !== 'undefined' && deck.slides.length > 0);
const settle = () => page.waitForFunction(() => !loading, null, { timeout: 60000 }).then(() => page.waitForTimeout(300));
const goto = async n => { await page.evaluate(n => show(n), n); await settle(); };
// Layout: text overflow, image loading, video elements per slide.
const layout = { html_sha256, slides: [] };
const total = await page.evaluate(() => deck.slides.length);
for (let n = 1; n <= total; n++) {
  await goto(n);
  layout.slides.push(await page.evaluate(n => {
    const s = deck.slides[n - 1];
    const overflow = [...document.querySelectorAll('#slide .text')].filter(e => e.scrollHeight > e.clientHeight + 2 || e.scrollWidth > e.clientWidth + 2).map(e => ({ text: e.textContent.slice(0, 60), sh: e.scrollHeight, ch: e.clientHeight, sw: e.scrollWidth, cw: e.clientWidth }));
    const images = [...document.querySelectorAll('#slide img')].map(i => ({ alt: i.alt.slice(0, 40), loaded: i.complete && i.naturalWidth > 0 }));
    const videoClips = [...document.querySelectorAll('#slide video')].map(v => v.dataset.clip);
    return { number: n, title: s.title, overflow, images, videoClips };
  }, n));
}
writeFileSync(B + 'standalone_layout_audit.json', JSON.stringify(layout, null, 2));
console.log('layout', layout.slides.filter(s => s.overflow.length).map(s => [s.number, s.overflow]), 'unloaded', layout.slides.flatMap(s => s.images.filter(i => !i.loaded)).length);
// Playback: play, stable pause, restart for every slide with clips.
const playback = { html_sha256, slides: [] };
const withClips = await page.evaluate(() => [...new Set(deck.media.map(m => m.slide))].sort((a, b) => a - b));
for (const n of withClips) {
  await goto(n);
  await page.evaluate(() => play());
  await page.waitForTimeout(1500);
  const snap = () => page.evaluate(() => videos().map(v => ({ clip: v.dataset.clip, time: v.currentTime, paused: v.paused, error: v.error ? v.error.code : null, ready: v.readyState })));
  const playing = await snap();
  await page.evaluate(() => pause()); await page.waitForTimeout(300); const pausedNow = await snap();
  await page.waitForTimeout(800); const pauseLater = await snap();
  await page.click('#restart'); await page.waitForTimeout(300); const restart = await snap();
  playback.slides.push({ slide: n, playing, pause: pausedNow, pauseLater, restart });
}
writeFileSync(B + 'standalone_playback_audit.json', JSON.stringify(playback, null, 2));
console.log('playback', playback.slides.map(s => [s.slide, s.playing.map(v => [v.clip, +v.time.toFixed(2), v.paused, v.error])]));
// UI: chapter transitions, keyboard, focus view, figure dialog, script views.
const ui = { html_sha256, transitions: [], keyboard: {}, figureDialog: {}, focusView: {} };
for (const n of await page.evaluate(() => deck.slides.filter(s => s.chapter_opening).map(s => s.number))) {
  await goto(n); const intro = await page.getAttribute('#slide', 'aria-label');
  await goto(n + 1); const caseTitle = await page.getAttribute('#slide', 'aria-label');
  await goto(n); const back = await page.evaluate(() => current);
  ui.transitions.push({ opening: n, intro, caseTitle, back });
}
await page.keyboard.press('End'); await settle(); ui.keyboard.endSlide = await page.evaluate(() => current);
await page.keyboard.press('Home'); await settle(); ui.keyboard.homeSlide = await page.evaluate(() => current);
await page.click('#fullscreen'); await page.waitForTimeout(400);
ui.focusView = await page.evaluate(() => ({ enabled: document.body.classList.contains('focus-view'), native: !!document.fullscreenElement }));
await page.keyboard.press('f'); await page.waitForTimeout(400);
ui.keyboard.focusExited = await page.evaluate(() => !document.body.classList.contains('focus-view'));
await goto(5); await page.click('#slide img.original'); await page.waitForTimeout(600);
ui.figureDialog = await page.evaluate(() => ({ open: $('figure-dialog').open, loaded: $('large-figure').complete && $('large-figure').naturalWidth > 0 }));
await page.keyboard.press('Escape'); await page.waitForTimeout(200); ui.figureDialog.closed = await page.evaluate(() => !$('figure-dialog').open);
ui.addedFigures = [];
for (const n of [11, 12, 13, 14, 19, 24, 26, 28]) {
 await goto(n); await page.click('#slide img.original'); await page.waitForTimeout(300);
 ui.addedFigures.push(await page.evaluate(n => ({slide:n,open:$('figure-dialog').open,loaded:$('large-figure').complete && $('large-figure').naturalWidth>0}),n));
 await page.keyboard.press('Escape');
}
await goto(5); await page.keyboard.press('n'); await page.waitForTimeout(200);
ui.currentScript = await page.evaluate(() => ({ heading: $('note-title').textContent, text: $('note-body').textContent.slice(0, 120) }));
await page.click('#all-script'); await page.waitForTimeout(300);
ui.fullScriptHeadings = await page.evaluate(() => [...$('note-body').querySelectorAll('h2')].map(h => h.textContent));
await page.click('#all-script'); await page.keyboard.press('n');
writeFileSync(B + 'standalone_ui_audit.json', JSON.stringify(ui, null, 2));
console.log('ui', JSON.stringify({ transitions: ui.transitions.map(t => [t.opening, t.back]), keyboard: ui.keyboard, focusView: ui.focusView, figureDialog: ui.figureDialog, headings: ui.fullScriptHeadings.length }));
// Mobile: 390 px viewport, controls inside the viewport, no horizontal document overflow.
await page.setViewportSize({ width: 390, height: 844 }); await goto(1); await page.waitForTimeout(500);
const measure = () => page.evaluate(() => ({ viewport: window.innerWidth, documentWidth: document.documentElement.scrollWidth, buttons: [...document.querySelectorAll('nav button, nav select, aside button')].filter(b => b.offsetParent !== null).map(b => { const r = b.getBoundingClientRect(); return { label: (b.textContent || b.getAttribute('aria-label') || '').trim().slice(0, 30), rect: { left: r.left, right: r.right, width: r.width, height: r.height } }; }) }));
const mobile = { html_sha256, ...(await measure()) };
await page.keyboard.press('n'); await page.waitForTimeout(300); mobile.script = await measure(); await page.keyboard.press('n');
writeFileSync(B + 'standalone_mobile_audit.json', JSON.stringify(mobile, null, 2));
console.log('mobile', mobile.viewport, mobile.documentWidth, 'buttons outside:', mobile.buttons.filter(b => b.rect.left < 0 || b.rect.right > mobile.viewport + .5).length, 'script buttons outside:', mobile.script.buttons.filter(b => b.rect.left < 0 || b.rect.right > mobile.script.viewport + .5).length);
await browser.close();
console.log('done', html_sha256);
