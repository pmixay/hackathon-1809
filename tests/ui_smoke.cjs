// Optional real-browser acceptance. Start `python -m terraplan ui` first.
// npm's Playwright must be available; set PLAYWRIGHT_MODULE to a local module if needed.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.BROWSER_CHANNEL||'msedge'});
 try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(process.env.TERRAPLAN_URL||'http://127.0.0.1:8765');
 assert.equal(await page.locator('#preset').inputValue(),'P2z_earth_new_zbo');
 const run=async()=>{await page.locator('#run').click();await page.waitForFunction(()=>document.getElementById('status').textContent.startsWith('Расчёт завершён'));};
 await run();assert.match(await page.locator('#result-title').innerText(),/Все жёсткие/);
 await fs.mkdir('build/r4/browser',{recursive:true});
 await page.screenshot({path:'build/r4/browser/dashboard.png',fullPage:true});
  await page.locator('#reserve-chart svg');assert.match(await page.locator('.story').innerText(),/Обязательный стресс/);
  await page.locator('[data-tab=compare]').click();await page.locator('#pin').click();
  await page.locator('#scenario').selectOption('mandatory_stress');await run();
  await page.locator('#compare-run').click();await page.waitForSelector('#comparison-kpi table');
  assert.match(await page.locator('#comparison').innerText(),/Дефицит/);
 await page.locator('[data-tab=checks]').click();assert.match(await page.locator('#violations').innerText(),/RESERVE_45D/);
 await page.screenshot({path:'build/r4/browser/stress.png',fullPage:true});
 await page.locator('#preset').selectOption('P2z_earth_new_zbo_adapted');await page.locator('#load').click();await run();
 assert.match(await page.locator('#result-title').innerText(),/Все жёсткие/);
 const savedPromise=page.waitForEvent('download');await page.locator('#save').click();const saved=await savedPromise;await saved.saveAs('build/r4/browser/workspace.json');
 await page.locator('#extension').click();await run();assert.match(await page.locator('#result-title').innerText(),/TEAM_COPY_BASE/);
 assert.match(await page.locator('#balance').innerText(),/2\s?041/);
 await page.locator('#open').setInputFiles('build/r4/browser/workspace.json');await run();
 assert.match(await page.locator('#result-title').innerText(),/P2z_earth_new_zbo_adapted/);
 await page.locator('[data-tab=editor]').click();const first=page.locator('#orders tbody input[type=number]').nth(1);await first.fill('-1');
 await page.locator('#run').click();await page.waitForSelector('#error:not([hidden])');assert.match(await page.locator('#error').innerText(),/ordered_t/);
 await page.locator('#open').setInputFiles('build/r4/browser/workspace.json');await run();
 await page.locator('[data-tab=dashboard]').click();const zipPromise=page.waitForEvent('download');await page.locator('#zip').click();const zip=await zipPromise;await zip.saveAs('build/r4/browser/results.zip');
 assert.equal((await fs.readFile('build/r4/browser/results.zip')).subarray(0,2).toString(),'PK');
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'build/r4/browser/mobile.png',fullPage:true});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
 assert.deepEqual(errors,[]);console.log('PASS: BASE, stress, compare, adapted, save/reopen, Source-X/2041, invalid input, ZIP, mobile layout.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
