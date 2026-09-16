import{createRequire}from'node:module';const require=createRequire(import.meta.url);const{chromium}=require('playwright');
const b=await chromium.launch({executablePath:'/opt/google/chrome/chrome',headless:true});const p=await b.newPage({viewport:{width:1500,height:1100},deviceScaleFactor:2});
await p.goto('https://anonymous-report-421.github.io/public-website/?lang=en&view=1',{waitUntil:'domcontentloaded',timeout:90000});
await p.locator('.rr-methods').waitFor({timeout:30000});await p.screenshot({path:'.build/assets/v0_7/report_page.png',fullPage:false});
await p.locator('.rr-methods').screenshot({path:'.build/assets/v0_7/report_architecture_original.png'});
console.log(await p.locator('.rr-methods').innerText());await b.close();
