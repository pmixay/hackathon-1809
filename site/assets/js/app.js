(function(){
"use strict";
var NS='http://www.w3.org/2000/svg';
function el(name,attrs,parent){var e=document.createElementNS(NS,name);
  for(var k in attrs)e.setAttribute(k,attrs[k]);
  if(parent)parent.appendChild(e);return e;}
function ru(v,dec){var s=dec?v.toFixed(dec).replace('.',','):String(Math.round(v));
  return s.replace(/\B(?=(\d{3})+(?!\d))/g,' ');}

/* ---------- starfield ---------- */
var seed=20250919;function rnd(){seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296;}
[['s1',210,1.1,.05],['s2',150,1.7,.13],['s3',80,2.6,.25]].forEach(function(c){
  var host=document.getElementById(c[0]);if(!host)return;
  host.dataset.par=c[3];
  var frag=document.createDocumentFragment();
  for(var i=0;i<c[1];i++){
    var d=document.createElement('div');d.className='star';
    d.style.width=c[2]+'px';d.style.height=c[2]+'px';
    d.style.left=(rnd()*100)+'vw';d.style.top=(rnd()*130)+'vh';
    d.style.opacity=(0.2+rnd()*0.7).toFixed(2);
    if(rnd()>0.88){d.style.background='#9ED2FF';d.style.boxShadow='0 0 7px 1px rgba(158,210,255,.85)';}
    if(rnd()>0.8){d.style.animation='tw '+(3+rnd()*5).toFixed(1)+'s ease-in-out '+(rnd()*5).toFixed(1)+'s infinite';}
    frag.appendChild(d);}
  host.appendChild(frag);});

/* ---------- reveal + counters ---------- */
function count(node){
  if(node.dataset.done)return;node.dataset.done='1';
  var to=parseFloat(node.dataset.to),sep=node.dataset.sep?1:0,start=null,dur=1400;
  if(!to){node.textContent='0';return;}
  requestAnimationFrame(function step(t){
    if(!start)start=t;
    var p=Math.min((t-start)/dur,1),v=to*(1-Math.pow(1-p,3));
    node.textContent=sep?ru(v):String(Math.round(v));
    if(p<1)requestAnimationFrame(step);});
}
var drawn={};
var io=new IntersectionObserver(function(entries){
  entries.forEach(function(e){
    if(!e.isIntersecting)return;
    var node=e.target,sibs=node.parentNode.children,idx=0;
    for(var i=0;i<sibs.length;i++){if(sibs[i]===node){idx=i;break;}}
    node.style.transitionDelay=(Math.min(idx,6)*80)+'ms';
    node.classList.add('in');
    node.querySelectorAll('.cnt').forEach(count);
    if(node.querySelector('#supplyChart')&&!drawn.supply){drawn.supply=1;growSupply();}
    if(node.querySelector('.pb')&&!drawn.plans){drawn.plans=1;growPlans();}
    if(node.classList.contains('flow'))node.classList.add('fly');
    io.unobserve(node);});
},{threshold:.2,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv').forEach(function(e){io.observe(e);});
document.querySelectorAll('.hero .cnt').forEach(count);

/* ---------- supply chart: what is needed vs what arrives ---------- */
var YEARS=['2035','2036','2037','2038','2039','2040'];
var NEED=[100,140,190,250,320,390];
/* actual deliveries per year, results/alternatives/P2z_earth_new_zbo_BASE/source_schedule.csv */
var GOT=[[109.9,0,0],[153.1,0,0],[190,13.2,0],[190,71.8,0],[190,130,12.6],[190,130,74.7]];
var CH_COLOR=['#4C8DFF','#3FE096','#59C8FF'];
var SW=1180,SH=500,SPB=70,SPT=40,SMAX=420,SPH=SH-SPB-SPT;
var supplyBars=[],groups=[];
var CH_NAME=['Основной канал','Новый канал','Гибкий канал'];
function showYear(i){
  groups.forEach(function(g,k){g.classList.toggle('dim',k!==i);});
  var box=document.getElementById('supplyRead');if(!box)return;
  box.replaceChildren();
  var wrap=document.createElement('div');wrap.className='box';
  var yr=document.createElement('span');yr.className='yr';yr.textContent=YEARS[i];wrap.append(yr);
  var need=document.createElement('span');need.className='kv';
  need.append('нужно ');
  var nb=document.createElement('strong');nb.textContent=ru(NEED[i],0)+' т';need.append(nb);
  wrap.append(need);
  for(var j=0;j<3;j++){
    if(GOT[i][j]<=0)continue;
    var kv=document.createElement('span');kv.className='kv';
    var dot=document.createElement('i');dot.style.background=CH_COLOR[j];kv.append(dot,CH_NAME[j]+' ');
    var b=document.createElement('strong');b.textContent=ru(GOT[i][j],1)+' т';kv.append(b);
    wrap.append(kv);}
  box.append(wrap);
}
function clearYear(){
  groups.forEach(function(g){g.classList.remove('dim');});
  var box=document.getElementById('supplyRead');if(!box)return;
  box.replaceChildren();
  var hint=document.createElement('span');hint.className='hint';
  hint.textContent='Наведите на год, чтобы увидеть разбор';
  box.append(hint);
}
(function buildSupply(){
  var svg=document.getElementById('supplyChart');if(!svg)return;
  var base=SH-SPB,slot=(SW-80)/6,barW=52,gap=26,groupW=barW*2+gap;
  el('line',{x1:40,y1:base,x2:SW-40,y2:base,stroke:'rgba(125,175,235,.3)','stroke-width':1.5},svg);
  YEARS.forEach(function(year,i){
    var x0=40+slot*i+(slot-groupW)/2;
    var grp=el('g',{class:'grp'},svg);
    /* needed: dashed outline */
    var nh=NEED[i]/SMAX*SPH;
    var need=el('rect',{x:x0,y:base,width:barW,height:0,rx:6,fill:'rgba(155,184,216,.12)',
      stroke:'#9BB8D8','stroke-width':2,'stroke-dasharray':'7 5'},grp);
    supplyBars.push({node:need,h:nh,y:base-nh});
    el('text',{x:x0+barW/2,y:base-nh-14,'text-anchor':'middle','font-family':'Benzin',
      'font-weight':700,'font-size':19,fill:'#9BB8D8',class:'sv',opacity:0},grp).textContent=NEED[i];
    /* arrived: stacked by channel */
    var stackX=x0+barW+gap,acc=0;
    for(var j=0;j<3;j++){
      var v=GOT[i][j];if(v<=0)continue;
      var h=v/SMAX*SPH,yTop=base-(acc+v)/SMAX*SPH;
      var seg=el('rect',{x:stackX,y:base,width:barW,height:0,rx:5,fill:CH_COLOR[j]},grp);
      supplyBars.push({node:seg,h:h,y:yTop});
      acc+=v;}
    var total=GOT[i][0]+GOT[i][1]+GOT[i][2];
    el('text',{x:stackX+barW/2,y:base-total/SMAX*SPH-14,'text-anchor':'middle','font-family':'Benzin',
      'font-weight':800,'font-size':21,fill:'#fff',class:'sv',opacity:0},grp).textContent=ru(total,0);
    el('text',{x:x0+groupW/2,y:base+38,'text-anchor':'middle','font-family':'Benzin',
      'font-weight':600,'font-size':21,fill:'#B9D8F5'},grp).textContent=year;
    groups.push(grp);
    var hit=el('rect',{x:40+slot*i,y:SPT-20,width:slot,height:base-SPT+56,fill:'transparent',
      class:'hit'},svg);
    hit.addEventListener('mouseenter',function(){showYear(i);});
    hit.addEventListener('focus',function(){showYear(i);});
    hit.setAttribute('tabindex','0');
    hit.addEventListener('blur',clearYear);});
  svg.addEventListener('mouseleave',clearYear);
  el('text',{x:40,y:SPT-6,'font-family':'Montserrat','font-weight':600,'font-size':17,
    fill:'#8FAEC9'},svg).textContent='тонн в год';
})();
function growSupply(){
  supplyBars.forEach(function(b,i){
    setTimeout(function(){
      b.node.setAttribute('height',b.h.toFixed(1));
      b.node.setAttribute('y',b.y.toFixed(1));
      b.node.style.transition='height .9s cubic-bezier(.2,.7,.2,1),y .9s cubic-bezier(.2,.7,.2,1)';
    },60+i*45);});
  setTimeout(function(){
    document.querySelectorAll('#supplyChart .sv').forEach(function(t){
      t.style.transition='opacity .5s';t.setAttribute('opacity',1);});},700);
}

/* ---------- plan bars ---------- */
function growPlans(){
  document.querySelectorAll('.pb .fill').forEach(function(f,i){
    setTimeout(function(){f.style.width=f.dataset.w+'%';},80+i*70);});
}

/* ---------- ракета летит по цепочке от Земли к миссиям ---------- */
(function(){
  var flow=document.querySelector('.flow'),rocket=document.getElementById('rocket');
  if(!flow||!rocket)return;
  var calm=matchMedia('(prefers-reduced-motion: reduce)');
  var pts=[],raf=null,t0=null,DUR=6400,LIFT=74;
  function measure(){
    var box=flow.getBoundingClientRect();
    pts=[].slice.call(flow.querySelectorAll('.fnode .ico')).map(function(n){
      var r=n.getBoundingClientRect();
      return {x:r.left-box.left+r.width/2,y:r.top-box.top+r.height/2};});
  }
  function at(p){
    if(pts.length<3)return null;
    var seg=p<0.5?0:1,lp=seg===0?p/0.5:(p-0.5)/0.5,a=pts[seg],b=pts[seg+1];
    return {x:a.x+(b.x-a.x)*lp,y:a.y+(b.y-a.y)*lp-Math.sin(lp*Math.PI)*LIFT};
  }
  function step(ts){
    if(!t0)t0=ts;
    var p=((ts-t0)%DUR)/DUR,here=at(p),ahead=at(Math.min(p+0.012,1));
    if(here&&ahead){
      var ang=Math.atan2(ahead.y-here.y,ahead.x-here.x)*180/Math.PI+90;
      rocket.style.transform='translate('+(here.x-19).toFixed(1)+'px,'+(here.y-19).toFixed(1)+'px) rotate('+ang.toFixed(1)+'deg)';
      rocket.style.opacity=(p<0.07?p/0.07:(p>0.93?(1-p)/0.07:1)).toFixed(2);
    }
    raf=requestAnimationFrame(step);
  }
  function start(){
    if(raf||calm.matches||innerWidth<=1060)return;
    measure();if(pts.length<3)return;
    t0=null;raf=requestAnimationFrame(step);
  }
  function stop(){if(raf){cancelAnimationFrame(raf);raf=null;}rocket.style.opacity=0;}
  /* летит только пока раздел на экране: за его пределами кадры не тратятся */
  new IntersectionObserver(function(es){
    es.forEach(function(e){e.isIntersecting?start():stop();});},{threshold:.15}).observe(flow);
  addEventListener('resize',function(){if(raf)measure();else stop();});
})();

/* ---------- crisis chart: stock on 1 January against the 45-day rule ---------- */
/* results/alternatives/P2z_earth_new_zbo_MANDATORY_STRESS and
   results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS, yearly_balance.csv */
var CRISIS={
  A:{years:['2038','2039','2040'],have:[30.8,2.0,0],need:[35.4,45.4,55.3],
     verdict:'Норма нарушена три года подряд: не хватает 4,6, 43,4 и 55,3 тонны.',ok:false},
  B:{years:['2038','2039','2040'],have:[35.4,45.4,55.3],need:[35.4,45.4,55.3],
     verdict:'Норма выполнена каждый год. Заказы 2036 и 2037 годов подняли запас вовремя.',ok:true}
};
var CW=1180,CHH=510,CPB=110,CPT=46,CMAX=62,CPH=CHH-CPB-CPT;
var crisisNodes=null;
(function buildCrisis(){
  var svg=document.getElementById('crisisChart');if(!svg)return;
  var base=CHH-CPB,slot=(CW-80)/3,barW=90,gap=26,groupW=barW*2+gap;
  crisisNodes={have:[],need:[],haveText:[],needText:[],gap:[],tie:[],x0:[],barW:barW,gap2:gap,groupW:groupW};
  [0,20,40,60].forEach(function(v){
    var y=base-v/CMAX*CPH;
    el('line',{x1:40,y1:y,x2:CW-40,y2:y,stroke:'rgba(125,175,235,.13)','stroke-width':1},svg);
    el('text',{x:34,y:y+6,'text-anchor':'end','font-family':'Montserrat','font-weight':600,
      'font-size':16,fill:'#8FAEC9'},svg).textContent=v;});
  el('line',{x1:40,y1:base,x2:CW-40,y2:base,stroke:'rgba(125,175,235,.3)','stroke-width':1.5},svg);
  ['2038','2039','2040'].forEach(function(year,i){
    var x0=40+slot*i+(slot-groupW)/2;
    crisisNodes.have.push(el('rect',{x:x0,y:base,width:barW,height:0,rx:7,fill:'#3FE096'},svg));
    crisisNodes.haveText.push(el('text',{x:x0+barW/2,y:base,'text-anchor':'middle','font-family':'Benzin',
      'font-weight':800,'font-size':23,fill:'#fff'},svg));
    crisisNodes.need.push(el('rect',{x:x0+barW+gap,y:base,width:barW,height:0,rx:7,
      fill:'rgba(155,184,216,.12)',stroke:'#9BB8D8','stroke-width':2,'stroke-dasharray':'7 5'},svg));
    crisisNodes.needText.push(el('text',{x:x0+barW+gap+barW/2,y:base,'text-anchor':'middle',
      'font-family':'Benzin','font-weight':700,'font-size':21,fill:'#B9D8F5'},svg));
    el('text',{x:x0+groupW/2,y:base+40,'text-anchor':'middle','font-family':'Benzin',
      'font-weight':600,'font-size':22,fill:'#B9D8F5'},svg).textContent=year;
    crisisNodes.gap.push(el('text',{x:x0+groupW/2,y:base+70,'text-anchor':'middle','font-family':'Benzin',
      'font-weight':800,'font-size':20,fill:'#FF7D91',opacity:0},svg));
    crisisNodes.tie.push(el('line',{x1:x0-8,x2:x0+barW+8,y1:base,y2:base,stroke:'#FF7D91',
      'stroke-width':2.5,'stroke-dasharray':'6 5',opacity:0},svg));
    crisisNodes.x0.push(x0);});
  el('text',{x:40,y:CPT-12,'font-family':'Montserrat','font-weight':600,'font-size':17,
    fill:'#8FAEC9'},svg).textContent='тонн на 1 января';
})();
function drawCrisis(key){
  if(!crisisNodes)return;
  var d=CRISIS[key],base=CHH-CPB;
  for(var i=0;i<3;i++){
    var hv=d.have[i]/CMAX*CPH,nd=d.need[i]/CMAX*CPH,short=d.have[i]+0.05<d.need[i];
    var bar=crisisNodes.have[i];
    bar.style.transition='height .8s cubic-bezier(.2,.7,.2,1),y .8s cubic-bezier(.2,.7,.2,1),fill .5s';
    bar.setAttribute('height',hv.toFixed(1));bar.setAttribute('y',(base-hv).toFixed(1));
    bar.setAttribute('fill',short?'#FF7D91':'#3FE096');
    crisisNodes.haveText[i].textContent=ru(d.have[i],1)+' т';
    /* когда норма проходит близко над столбцом, подпись уходит внутрь него */
    var tight=short&&(nd-hv)<48&&hv>72;
    crisisNodes.haveText[i].setAttribute('y',(tight?base-hv+34:base-hv-14).toFixed(1));
    crisisNodes.haveText[i].setAttribute('fill',tight?'#2A0713':(short?'#FF7D91':'#fff'));
    crisisNodes.need[i].style.transition='height .8s cubic-bezier(.2,.7,.2,1),y .8s cubic-bezier(.2,.7,.2,1)';
    crisisNodes.need[i].setAttribute('height',nd.toFixed(1));
    crisisNodes.need[i].setAttribute('y',(base-nd).toFixed(1));
    crisisNodes.needText[i].textContent=ru(d.need[i],1)+' т';
    crisisNodes.needText[i].setAttribute('y',(base-nd-14).toFixed(1));
    /* уровень нормы, продлённый над фактическим запасом, и подпись под годом */
    var gapNode=crisisNodes.gap[i],tie=crisisNodes.tie[i];
    gapNode.style.transition='opacity .5s';
    tie.style.transition='opacity .5s,y1 .8s cubic-bezier(.2,.7,.2,1),y2 .8s cubic-bezier(.2,.7,.2,1)';
    tie.setAttribute('y1',(base-nd).toFixed(1));tie.setAttribute('y2',(base-nd).toFixed(1));
    if(short){
      tie.setAttribute('opacity',1);
      gapNode.textContent='не хватает '+ru(d.need[i]-d.have[i],1)+' т';
      gapNode.setAttribute('opacity',1);
    } else {tie.setAttribute('opacity',0);gapNode.setAttribute('opacity',0);}}
  var v=document.getElementById('crisisVerdict');
  v.textContent=d.verdict;v.className='verdict '+(d.ok?'good':'bad');
}
var mA=document.getElementById('mA'),mB=document.getElementById('mB');
function setMode(key){
  var isA=key==='A';
  mA.classList.toggle('on',isA);mB.classList.toggle('on',!isA);
  mA.setAttribute('aria-pressed',String(isA));mB.setAttribute('aria-pressed',String(!isA));
  drawCrisis(key);
}
if(mA&&mB){
  mA.addEventListener('click',function(){setMode('A');});
  mB.addEventListener('click',function(){setMode('B');});
  var crisisIO=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){drawCrisis('A');crisisIO.disconnect();}});},
    {threshold:.3});
  crisisIO.observe(document.getElementById('crisisChart'));
}

/* ---------- scroll loop ---------- */
var hdr=document.getElementById('hdr'),prog=document.getElementById('prog'),
    layers=[].slice.call(document.querySelectorAll('.starlayer')),
    earth=document.querySelector('.earth'),heroInner=document.querySelector('.heroInner'),
    calm=matchMedia('(prefers-reduced-motion: reduce)'),ticking=false;
function frame(){
  var y=window.scrollY||0,max=document.body.scrollHeight-window.innerHeight;
  prog.style.width=(max>0?y/max*100:0)+'%';
  hdr.classList.toggle('stuck',y>80);
  layers.forEach(function(l){l.style.transform='translateY('+(-y*parseFloat(l.dataset.par))+'px)';});
  if(earth&&!calm.matches){
    var p=Math.min(y/window.innerHeight,1);
    earth.style.transform='translateX(-50%) translateY('+(-p*230).toFixed(1)+'px) scale('+(1+p*0.10).toFixed(3)+')';
    heroInner.style.transform='translateY('+(p*72).toFixed(1)+'px)';
    heroInner.style.opacity=Math.max(0,1-p*1.15).toFixed(3);}
  ticking=false;
}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(frame);}},{passive:true});
addEventListener('resize',frame);
frame();
})();
