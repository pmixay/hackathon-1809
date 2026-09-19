// Rebuild from repository evidence. Requires the bundled @oai/artifact-tool runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const {Presentation,PresentationFile}=await import(process.env.ARTIFACT_MODULE || '@oai/artifact-tool');
const load=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const base=await load('results/alternatives/P2z_earth_new_zbo_BASE/result.json');
const stress=await load('results/alternatives/P2z_earth_new_zbo_MANDATORY_STRESS/result.json');
const adapted=await load('results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS/result.json');
const ext=await load('results/extensibility/run/result.json');
// Discover exact names rather than assuming a strategy filename.
const dirs=await fs.readdir(path.join(root,'results/alternatives'));
const alternatives=[];
for(const prefix of ['P2_','P2z_','P3_','P4_']){
 const dir=dirs.find(d=>d.startsWith(prefix)&&d.endsWith('_BASE'));
 alternatives.push(await load(`results/alternatives/${dir}/result.json`));
}
const round=v=>Math.round(v).toLocaleString('ru-RU');
const slides=[
 {title:'TerraPlan',lines:['Топливное снабжение орбитального узла','2035–2040','CosmoHackathon 2026 · Кейс 2'],source:'docs/CASE_SUMMARY.md; docs/TEAM.md'},
 {title:'Задача оператора',lines:['Спрос растёт со 100 до 390 т/год.','Физический резерв покрывает 45 дней спроса.','Общий сервис ≥ 97 %, критический ≥ 99 % в BASE.','CAPEX: ≤ 1 800 млн до 2037, ≤ 2 800 млн до 2040.'],source:'data/case/demand.csv; data/case/constraints.csv'},
 {title:'Помесячный баланс и стоимость',lines:['Запас на конец = запас на начало + поставки − потери − выдача.','Потери начисляются один раз на валовый входящий поток.','Стоимость = закупка + резерв мощности + хранение + OPEX + CAPEX.','PV: реальная ставка 8 %, цены 2035 г. Единая база для альтернатив.'],source:'docs/architecture.md; src/terraplan/engine.py; configs/assumptions.yaml'},
 {title:'Контракты и инвестиции',lines:['Earth-Core: 190 т/год, 12 месяцев, take-or-pay 70 %.','Earth-Flex: 110 т/год, 4 месяца. Emergency: 80 т/год, 6 недель.','Earth-New: CAPEX 360 млн. ISRU: 1 250 млн, доступен с 2038.','ZBO: CAPEX 180 млн, потери 1,2 % вместо 4,5 %.'],source:'data/case/supply_sources.csv; data/case/investment_options.csv; data/case/storage_options.csv'},
 {title:'P2z выбран после жёсткого фильтра',chart:{categories:['P2 New','P2z New + ZBO','P3 ISRU + ZBO','P4 полный'],series:[{name:'PV BASE, млн у.е.',values:alternatives.map(r=>Math.round(r.kpi.pv_cost_mln)),fill:'#176a5b'}]},caption:'P2z не самый дешёвый в BASE, но выигрывает все раскрытые профили MCDA за счёт CAPEX и стоимости адаптации.',source:'results/alternatives/*_BASE/result.json; results/strategy/summary.md'},
 {title:'Обязательный стресс P2z',lines:[`Неизменный план: дефицит ${stress.kpi.shortage_total_t.toFixed(1)} т.`,`Нарушения резерва: ${stress.violations.filter(v=>v.rule_id==='RESERVE_45D').map(v=>v.year).join(', ')}.`,'Спрос +15 % с 2038. Цены A/B +25 % в 2038–2039.','P2z не использует ISRU: его проблема в стрессе — недостаточный график заказов и запас.'],source:'results/alternatives/P2z_earth_new_zbo_MANDATORY_STRESS/result.json; configs/scenarios/mandatory_stress.yaml'},
 {title:'Заблаговременная адаптация P2z',chart:{categories:['BASE','Стресс, план прежний','Стресс, адаптация'],series:[{name:'PV, млн у.е.',values:[base,stress,adapted].map(r=>Math.round(r.kpi.pv_cost_mln)),fill:'#176a5b'}]},caption:`Адаптация: дефицит ${round(adapted.kpi.shortage_total_t)} т, жёстких нарушений ${adapted.kpi.hard_violations}. График зависит от сценария: адаптированный план переполняет хранилище в BASE.`,source:'results/alternatives/P2z_earth_new_zbo_BASE/result.json; results/alternatives/P2z_earth_new_zbo_MANDATORY_STRESS/result.json; results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS/result.json'},
 {title:'Риски выбранной стратегии',lines:['Буфер запаса нужен до начала года: поздняя реакция не исправит резерв на 1 января.','EXP-09: задержка Earth-New уже на 3 месяца нарушает резерв P2z в 2038–2040.','EXP-11: ценовой шок A/B +25 % добавляет P2z 470,9 млн PV без физического дефицита.','EXP-07–10 исследуют P3. Их частоты нельзя переносить на P2z без нового расчёта.'],source:'results/earth_new_delay/summary.md; results/geopolitical_price_shock/summary.md; results/monte_carlo/summary.md'},
 {title:'Рабочий интерфейс оператора',lines:['Редактор заказов, резервов, инвестиций и начального запаса.','Расчёт BASE и обязательного стресса через единый Python-движок.','Нарушения показывают год, факт, лимит и причину.','Сравнение двух расчётов с изменением решений и расходов.'],source:'src/terraplan/web.py; src/terraplan/static/; docs/operator_guide.md'},
 {title:'Сохранение, выгрузка, расширение',lines:['Рабочий JSON сохраняет план, сценарий, копию данных и допущения.','ZIP содержит CSV, XLSX, JSON, входные данные и хеши расчёта.',`Демонстрация: Source-X и 2041 год, ${ext.years.length} лет, PV ${round(ext.kpi.pv_cost_mln)} млн. Исполнимость: ${ext.feasible?'да':'нет'}.`,'Source-X и спрос 2041 — TEAM_ASSUMPTION. Контрольные данные и ограничения сохранены.'],source:'results/extensibility/run/result.json; experiments/run_extensibility.py; tests/test_web.py'},
 {title:'Бюджет P2z по годам',chart:{categories:base.finance.map(r=>String(r.year)),series:[{name:'Всего, млн',values:base.finance.map(r=>Math.round(r.total_mln)),fill:'#176a5b'},{name:'CAPEX, млн (в составе итого)',values:base.finance.map(r=>r.capex_mln),fill:'#d5a747'}]},caption:'Earth-New: 360 млн в 2035. ZBO: 180 млн в 2037. CAPEX P2z до 2037: 540 млн.',source:'results/alternatives/P2z_earth_new_zbo_BASE/financial_breakdown.csv; docs/roadmap_budget.md'},
 {title:'Запуск и передача решения',lines:['python -m pip install -e ".[dev]"','python -m terraplan ui','Проверка: BASE, стресс, адаптация, сохранение, сравнение, Source-X / 2041.','Границы: локальный прототип, без оптимизатора и многопользовательского доступа.','Код и инструкции готовы к передаче. Публикация на GitVerse ещё не выполнена.'],source:'README.md; docs/operator_guide.md; docs/HANDOVER.md'},
];
const p=Presentation.create({slideSize:{width:1280,height:720}});
function text(s,value,x,y,w,h,size=30,color='#183b40',bold=false){const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=value;sh.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none'};return sh;}
const output=path.join(root,'docs/presentation');const build=path.join(root,'build/r4/deck');await fs.mkdir(build,{recursive:true});
for(let i=0;i<slides.length;i++){
 const d=slides[i],s=p.slides.add();s.background.fill=i===0?'#142f38':'#f5f6f3';
 text(s,d.title,70,i===0?150:48,1140,100,i===0?72:44,i===0?'#ffffff':'#183b40',true);
 if(d.lines)d.lines.forEach((line,j)=>text(s,line,74,(i===0?290:190)+j*77,1120,68,i===0?32:29,i===0?'#d0e3df':'#244d50'));
 if(d.chart){
 const chart=s.charts.add('bar',{position:{left:75,top:168,width:1120,height:380},...d.chart,barOptions:{direction:'column',grouping:'clustered'},hasLegend:d.chart.series.length>1,dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:23}},xAxis:{textStyle:{fontSize:21}},yAxis:{numberFormatCode:'#,##0',textStyle:{fontSize:21}}});
 for(const style of [chart.legend.textStyle,chart.dataLabels.textStyle,chart.xAxis.textStyle,chart.yAxis.textStyle]){style.typeface='Arial';style.fontSize=23;}
 text(s,d.caption,75,574,1110,74,25);
 }
 text(s,`${i+1} / ${slides.length}`,1120,670,105,28,17,i===0?'#d0e3df':'#6a807a');
 s.speakerNotes.textFrame.setText(`Источники в репозитории: ${d.source}. Все денежные показатели в млн условных единиц, постоянные цены 2035 г. Значения диаграмм округлены до целого, исходные точные значения сохранены в result.json.`);
}
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
for(let i=0;i<p.slides.items.length;i++){
 const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
}
if(process.env.PRESENTATION_SKILL){
 const {finalizePresentation}=await import(pathToFileURL(path.join(process.env.PRESENTATION_SKILL,'container_tools/artifact_tool_utils.mjs')).href);
 await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:path.join(output,'TerraPlan.pptx'),pythonExecutable:process.env.PRESENTATION_PYTHON,integrityValidatorPath:path.join(process.env.PRESENTATION_SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(process.env.PRESENTATION_SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Arial']},explicitTotalSlideCount:12,materializeLiteralChartWorkbooks:true,requiredNativeChartOwnerSlides:[5,7,11],verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
}else{await fs.copyFile(candidate,path.join(output,'TerraPlan.pptx'));}
await fs.writeFile(path.join(output,'slides.json'),JSON.stringify(slides,null,2));
console.log('Created 12 slides from results/ evidence.');
