// Optional real-browser acceptance. Start `python -m terraplan ui` first.
// npm's Playwright must be available; set PLAYWRIGHT_MODULE to a local module if needed.
// The operator console lives at /console: "/" serves the solution landing page (site/index.html).
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_EXECUTABLE}:{channel:process.env.BROWSER_CHANNEL||'msedge'})});
 try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const origin=(process.env.TERRAPLAN_URL||'http://127.0.0.1:8765').replace(/\/+$/,'');
 await page.goto(origin+'/console');
 // landing page is served at the root and links to the console
 const landing=await browser.newPage();await landing.goto(origin+'/');
 assert.match(await landing.title(),/TerraPlan/i);
 assert.ok(await landing.locator('a[href*="console"]').count()>0,'на странице решения нет ссылки на пульт оператора');
 await landing.close();
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
 // несколько ошибок сразу: оператор получает список, а не первую попавшуюся
 const second=page.locator('#reservations tbody input[type=number]').nth(1);await second.fill('-5');
 await page.locator('#run').click();await page.waitForSelector('#error li');
 const problems=await page.locator('#error li').allInnerTexts();
 assert.ok(problems.length>=2,'ожидался список из нескольких проблем ввода');
 assert.ok(problems.some(t=>/ordered_t/.test(t))&&problems.some(t=>/reserved_capacity_t/.test(t)));
 await page.locator('#open').setInputFiles('build/r4/browser/workspace.json');await run();
 // структурированный редактор данных: правка цены канала через форму меняет показатели
 await page.locator('[data-tab=data]').click();
 const priceCell=page.locator('#supply-table tbody tr').first().locator('input').nth(3);
 const oldPrice=Number(await priceCell.inputValue());
 const pvBefore=Number((await page.locator('#kpis').innerText()).match(/PV расходов[^\d-]*([\d  ,.]+)/)[1].replace(/[  ]/g,'').replace(',','.'));
 await priceCell.fill(String(oldPrice+1));
 await page.locator('#case-notes').fill('TEAM_ASSUMPTION: цена канала +1 млн/т, проверка чувствительности');
 await run();
 const pvAfter=Number((await page.locator('#kpis').innerText()).match(/PV расходов[^\d-]*([\d  ,.]+)/)[1].replace(/[  ]/g,'').replace(',','.'));
 assert.ok(pvAfter>pvBefore,`правка цены должна повышать PV: ${pvBefore} -> ${pvAfter}`);
 await page.screenshot({path:'build/r4/browser/data-editor.png',fullPage:true});
 await page.locator('#reset').click();await run();
 // блок геополитики: шок цены применяется и снимается на копии сценария
 await page.locator('[data-tab=geo]').click();
 await page.locator('#geo-label').fill('ограничение экспорта');
 await page.locator('#geo-pct').fill('25');
 await page.locator('#geo-just').fill('условный сценарий команды, не прогноз');
 await page.locator('#geo-enabled').check();
 await page.locator('#geo-apply').click();
 await page.waitForFunction(()=>document.getElementById('status').textContent.includes('ценовым шоком завершён'));
 assert.match(await page.locator('#geo-state').innerText(),/приме/i);
 assert.match(await page.locator('#geo-overlay').innerText(),/\d/);
 await page.locator('#geo-compare').click();await page.waitForSelector('#geo-comparison table');
 assert.match(await page.locator('#geo-comparison').innerText(),/PV расходов/);
 await page.screenshot({path:'build/r4/browser/geopolitics.png',fullPage:true});
 await page.locator('#geo-restore').click();
 await page.waitForFunction(()=>document.getElementById('status').textContent.includes('исходными ценами завершён'));
 assert.match(await page.locator('#geo-state').innerText(),/не примен/i);
 await page.locator('[data-tab=dashboard]').click();
 await page.locator('[data-tab=dashboard]').click();const zipPromise=page.waitForEvent('download');await page.locator('#zip').click();const zip=await zipPromise;await zip.saveAs('build/r4/browser/results.zip');
 assert.equal((await fs.readFile('build/r4/browser/results.zip')).subarray(0,2).toString(),'PK');
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'build/r4/browser/mobile.png',fullPage:true});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
 assert.deepEqual(errors,[]);console.log('PASS: landing page + console route, BASE, stress, compare, adapted, save/reopen, Source-X/2041, invalid input (list), contract-field edit, geopolitics on/off, ZIP, mobile layout.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
