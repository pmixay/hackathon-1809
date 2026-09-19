(function(){
var cl=function(v,a,b){return v<a?a:(v>b?b:v)};
var seg=function(p,a,b){return cl((p-a)/(b-a),0,1)};
var ease=function(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};

/* stars */
var seed=20250919;function rnd(){seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296;}
[['s1',250,1.1,.05],['s2',175,1.7,.13],['s3',90,2.6,.25]].forEach(function(c){
  var h=document.getElementById(c[0]),f=document.createDocumentFragment();h.dataset.par=c[3];
  for(var i=0;i<c[1];i++){var d=document.createElement('div');d.className='star';
    d.style.width=c[2]+'px';d.style.height=c[2]+'px';
    d.style.left=(rnd()*100)+'vw';d.style.top=(rnd()*115)+'vh';
    d.style.opacity=(0.2+rnd()*0.7).toFixed(2);
    if(rnd()>0.88){d.style.background='#9ED2FF';d.style.boxShadow='0 0 7px 1px rgba(158,210,255,.85)';}
    if(rnd()>0.8){d.style.animation='tw '+(3+rnd()*5).toFixed(1)+'s ease-in-out '+(rnd()*5).toFixed(1)+'s infinite';}
    f.appendChild(d);}
  h.appendChild(f);});

/* hero subtitle */
var hs=document.getElementById('heroSub');
hs.innerHTML=hs.textContent.trim().split(' ').map(function(w,i){
  return '<span class="w" style="transition-delay:'+(160+i*70)+'ms">'+w+'</span>';}).join(' ');
setTimeout(function(){hs.classList.add('in');},160);

/* year strip */
var ys=['2035','2036','2037','2038','2039','2040'],pa=[];
for(var k=0;k<8;k++)ys.forEach(function(y){pa.push('<span>'+y+'</span><em>◆</em>');});
document.getElementById('track').innerHTML=pa.join('');

/* reveal + counters */
function fmt(v,dec,sep){var s=dec?v.toFixed(dec).replace('.',','):String(Math.round(v));
  if(sep)s=s.replace(/\B(?=(\d{3})+(?!\d))/g,' ');return s;}
function count(el){if(el.dataset.done)return;el.dataset.done=1;
  var to=parseFloat(el.dataset.to),dec=el.dataset.dec?+el.dataset.dec:0,sep=el.dataset.sep?1:0,t0=null,dur=1500;
  if(!to){el.textContent=fmt(0,dec,sep);return;}
  (function s(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1);
    el.textContent=fmt(to*(1-Math.pow(1-p,3)),dec,sep);if(p<1)requestAnimationFrame(s);})(performance.now());}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;
  var el=e.target,sib=el.parentNode.children,idx=0;
  for(var i=0;i<sib.length;i++){if(sib[i]===el){idx=i;break;}}
  el.style.transitionDelay=(Math.min(idx,7)*80)+'ms';el.classList.add('in');
  el.querySelectorAll('.cnt').forEach(count);io.unobserve(el);});},
  {threshold:.2,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv').forEach(function(e){io.observe(e);});

/* ---- demand chart ---- */
var YR=['2035','2036','2037','2038','2039','2040'];
var DEM=[100,140,190,250,320,390];
var SRC=[[109.9,0,0],[153.1,0,0],[190,13.2,0],[190,71.8,0],[190,130,12.6],[190,130,74.7]];
var CLR=['#4C8DFF','#3FE096','#59C8FF'];
var CW=1180,CH=470,PB=64,PT=40,BW=96,GAP=(CW-140-6*BW)/5,X0=70,MAXV=420,PH=CH-PB-PT;
var svg=document.getElementById('dChart'),parts=[];
parts.push('<line x1="40" y1="'+(CH-PB)+'" x2="'+(CW-40)+'" y2="'+(CH-PB)+'" stroke="rgba(125,175,235,.3)" stroke-width="1.5"/>');
for(var i=0;i<6;i++){var x=X0+i*(BW+GAP);
  parts.push('<rect class="dbar" data-i="'+i+'" x="'+x+'" y="'+(CH-PB)+'" width="'+BW+'" height="0" rx="7" fill="rgba(125,175,235,.42)"/>');
  for(var j=0;j<3;j++)parts.push('<rect class="sbar" data-i="'+i+'" data-j="'+j+'" x="'+x+'" y="'+(CH-PB)+'" width="'+BW+'" height="0" rx="4" fill="'+CLR[j]+'" opacity="0"/>');
  parts.push('<text class="dval" data-i="'+i+'" x="'+(x+BW/2)+'" y="'+(CH-PB-10)+'" text-anchor="middle" font-family="Benzin" font-weight="800" font-size="25" fill="#fff" opacity="0">0</text>');
  parts.push('<text x="'+(x+BW/2)+'" y="'+(CH-PB+34)+'" text-anchor="middle" font-family="Benzin" font-weight="600" font-size="20" fill="#B9D8F5">'+YR[i]+'</text>');}
svg.innerHTML=parts.join('');
var dbars=[].slice.call(svg.querySelectorAll('.dbar')),
    sbars=[].slice.call(svg.querySelectorAll('.sbar')),
    dvals=[].slice.call(svg.querySelectorAll('.dval'));

/* ---- chain: bezier helpers ---- */
var BA=[[255,150],[340,40],[440,40],[512,120]],BB=[[668,120],[745,40],[860,40],[930,150]];
function bez(b,t){var mt=1-t,a=mt*mt*mt,c=3*mt*mt*t,d=3*mt*t*t,e=t*t*t;
  return [a*b[0][0]+c*b[1][0]+d*b[2][0]+e*b[3][0], a*b[0][1]+c*b[1][1]+d*b[2][1]+e*b[3][1]];}
function ang(b,t){var p1=bez(b,Math.max(0,t-.01)),p2=bez(b,Math.min(1,t+.01));
  return Math.atan2(p2[1]-p1[1],p2[0]-p1[0])*180/Math.PI;}
var rocket=document.getElementById('rocket'),wrap=document.querySelector('.chainWrap');

/* ---- tank data ---- */
var TANK=[['2038',30.8,35.4],['2039',2.0,45.4],['2040',0,55.3]];
var TANK2=[['2038',35.4,35.4],['2039',45.4,45.4],['2040',55.3,55.3]];
var TMAX=62,TY0=420,TH=360,SVGH=460;
var liquid=document.getElementById('liquid'),liqTop=document.getElementById('liquidTop'),
    normIn=document.getElementById('normIn'),normTag=document.getElementById('normTag'),
    levelTag=document.getElementById('levelTag'),tYear=document.getElementById('tYear'),
    tState=document.getElementById('tState'),tDelta=document.getElementById('tDelta'),
    knob=document.getElementById('knob'),mA=document.getElementById('mA'),mB=document.getElementById('mB'),
    vsw=document.getElementById('vsw'),scaleEl=document.getElementById('scale');
/* ticks */
[0,20,40,60].forEach(function(v){var d=document.createElement('div');d.className='tk';
  d.style.top=(TY0-v/TMAX*TH)+'px';d.innerHTML='<span>'+v+' т</span><i></i>';scaleEl.appendChild(d);});

/* ---- pinned engine ---- */
var pins=[];function pin(id,fn){var el=document.getElementById(id);if(el)pins.push({el:el,fn:fn});}

pin('heroPin',function(p){
  var txt=document.getElementById('heroText'),pl=document.getElementById('planet'),
      at=document.getElementById('atmo'),ow=document.getElementById('orbitWrap'),
      sec=document.getElementById('heroSecond'),hint=document.getElementById('hint');
  var a=seg(p,0,.34);
  txt.style.transform='translateY('+(-a*150)+'px) scale('+(1-a*.14)+')';
  txt.style.opacity=(1-a*1.12).toFixed(3);
  hint.style.opacity=(1-seg(p,0,.1)).toFixed(3);
  var rise=seg(p,0,.66);
  pl.style.transform='translateX(-50%) translateY('+(-rise*420)+'px) scale('+(1+rise*.24)+')';
  at.style.transform='translateX(-50%) translateY('+(-rise*420)+'px) scale('+(1+rise*.24)+')';
  ow.style.transform='translateX(-50%) translateY('+(-rise*420)+'px) scale('+(1+rise*.24)+')';
  var b=seg(p,.28,.50);
  sec.style.opacity=b.toFixed(3);
  sec.style.transform='translateY('+(-50+(1-b)*7)+'%) scale('+(.95+b*.05)+')';
});

pin('chainPin',function(p){
  var caps=document.querySelectorAll('#chainCap div');
  var n1=document.getElementById('cn1'),n2=document.getElementById('cn2'),n3=document.getElementById('cn3');
  var a1=seg(p,.04,.18),fA=seg(p,.22,.46),a2=seg(p,.34,.50),fB=seg(p,.56,.80),a3=seg(p,.66,.84);
  n1.style.opacity=(.25+a1*.75).toFixed(2);n1.style.transform='scale('+(.9+a1*.1)+')';
  n2.style.opacity=(.25+a2*.75).toFixed(2);n2.style.transform='scale('+(.9+a2*.1)+')';
  n3.style.opacity=(.25+a3*.75).toFixed(2);n3.style.transform='scale('+(.9+a3*.1)+')';
  document.getElementById('pA').setAttribute('stroke-dashoffset',(230*(1-fA)).toFixed(1));
  document.getElementById('pB').setAttribute('stroke-dashoffset',(230*(1-fB)).toFixed(1));
  document.getElementById('ch1').classList.toggle('on',p>.16);
  document.getElementById('ch2').classList.toggle('on',p>.46);
  document.getElementById('ch3').classList.toggle('on',p>.74);
  var k=wrap.clientWidth/1180,pt,rot,vis=1;
  if(p<.20){vis=0;pt=bez(BA,0);rot=ang(BA,0);}
  else if(p<.50){var t=seg(p,.20,.48);pt=bez(BA,t);rot=ang(BA,t);}
  else if(p<.56){pt=bez(BA,1);rot=ang(BA,1);}
  else{var t2=seg(p,.56,.86);pt=bez(BB,t2);rot=ang(BB,t2);}
  rocket.style.opacity=vis;
  rocket.style.transform='translate('+(pt[0]*k)+'px,'+(pt[1]*k)+'px) rotate('+(rot+90)+'deg)';
  var idx=p<.34?0:(p<.64?1:2);
  caps.forEach(function(c,i){c.classList.toggle('on',i===idx);});
});

pin('demandPin',function(p){
  var phase=seg(p,.52,.72);
  dbars.forEach(function(b,i){
    var g=seg(p,.06+i*.035,.30+i*.035),h=DEM[i]/MAXV*PH*ease(g);
    b.setAttribute('height',h.toFixed(1));b.setAttribute('y',(CH-PB-h).toFixed(1));
    b.setAttribute('opacity',(1-phase).toFixed(2));
    var v=dvals[i];v.setAttribute('opacity',(g>.1?1:0));v.setAttribute('y',(CH-PB-h-14).toFixed(1));
    var tot=SRC[i][0]+SRC[i][1]+SRC[i][2];
    v.textContent=Math.round(phase>0?(DEM[i]+(tot-DEM[i])*phase):DEM[i]*ease(g));});
  sbars.forEach(function(b){var i=+b.dataset.i,j=+b.dataset.j,base=0;
    for(var q=0;q<j;q++)base+=SRC[i][q];
    var hh=SRC[i][j]/MAXV*PH*phase,bb=base/MAXV*PH*phase;
    b.setAttribute('height',hh.toFixed(1));b.setAttribute('y',(CH-PB-bb-hh).toFixed(1));
    b.setAttribute('opacity',phase.toFixed(2));});
  document.getElementById('dLegend').classList.toggle('on',phase>.35);
  var caps=document.querySelectorAll('#dCap div');
  caps[0].classList.toggle('on',phase<.4);caps[1].classList.toggle('on',phase>=.4);
});

pin('plansPin',function(p){
  var tr=document.getElementById('ptrack'),max=tr.scrollWidth-window.innerWidth+80;
  if(max<0)max=0;
  tr.style.transform='translateX('+(-ease(seg(p,.10,.94))*max)+'px)';
  if(p>.04)document.querySelectorAll('.pbar .fl').forEach(function(f){f.style.width=f.dataset.w+'%';});
});

pin('tankPin',function(p){
  var mode=p>=.55?1:0,lp=mode?seg(p,.58,1):seg(p,0,.52),set=mode?TANK2:TANK;
  var idx=Math.min(Math.floor(lp*3),2),loc=cl(lp*3-idx,0,1);
  var d=set[idx],nx=set[Math.min(idx+1,2)];
  var have=d[1]+(nx[1]-d[1])*ease(loc),need=d[2]+(nx[2]-d[2])*ease(loc);
  var yH=TY0-cl(have/TMAX,0,1)*TH, yN=TY0-cl(need/TMAX,0,1)*TH;
  liquid.setAttribute('height',(TY0-yH).toFixed(1));liquid.setAttribute('y',yH.toFixed(1));
  liqTop.setAttribute('cy',yH.toFixed(1));liqTop.setAttribute('opacity',(TY0-yH)>4?1:0);
  normIn.setAttribute('y1',yN.toFixed(1));normIn.setAttribute('y2',yN.toFixed(1));
  var ok=have>=need-0.05;
  liquid.setAttribute('fill',ok?'url(#lg)':'url(#lgBad)');
  normTag.style.top=(yN/SVGH*100)+'%';
  normTag.querySelector('b').textContent='норма '+need.toFixed(1).replace('.',',')+' т';
  levelTag.style.top=(yH/SVGH*100)+'%';
  var lb=levelTag.querySelector('b'),li=levelTag.querySelector('i');
  lb.textContent=have.toFixed(1).replace('.',',')+' т';
  lb.style.background=ok?'#3FE096':'#FF7D91';li.style.background=ok?'#3FE096':'#FF7D91';
  tYear.textContent=loc>.5?nx[0]:d[0];
  tState.textContent=ok?'Норма выполнена':'Запаса не хватает';
  tState.className='st '+(ok?'good':'bad');
  var diff=have-need;
  tDelta.textContent=ok?'запас в норме':(diff.toFixed(1).replace('.',',')+' т до нормы');
  tDelta.className='delta '+(ok?'good':'bad');
  document.getElementById('tNote').textContent=mode
    ? 'Заказы 2036 и 2037 годов подняли запас ровно до нормы каждого года.'
    : 'Запас на 1 января набирается заказами прошлых лет. Решать в этот момент уже поздно.';
  mA.classList.toggle('on',!mode);mB.classList.toggle('on',!!mode);
  knob.style.top=(mode?(vsw.clientHeight-21):6)+'px';
});

/* ---- scroll loop ---- */
var hdr=document.getElementById('hdr'),prog=document.getElementById('prog'),
    track=document.getElementById('track'),
    layers=[].slice.call(document.querySelectorAll('.starlayer')),
    glows=[].slice.call(document.querySelectorAll('.glow[data-par]')),tick=false;
function frame(){
  var y=window.scrollY||0,vh=window.innerHeight,max=document.body.scrollHeight-vh;
  prog.style.width=(max>0?y/max*100:0)+'%';
  hdr.classList.toggle('stuck',y>90);
  layers.forEach(function(l){l.style.transform='translateY('+(-y*parseFloat(l.dataset.par))+'px)';});
  glows.forEach(function(g){g.style.transform='translateY('+((vh-g.getBoundingClientRect().top)*parseFloat(g.dataset.par)*-0.4)+'px)';});
  track.style.transform='translateX('+(-((y*0.3)%1350))+'px)';
  pins.forEach(function(s){var r=s.el.getBoundingClientRect(),tot=s.el.offsetHeight-vh;
    s.fn(tot>0?cl(-r.top/tot,0,1):0);});
  tick=false;
}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(frame);}},{passive:true});
addEventListener('resize',frame);
frame();
})();

/* smooth anchor nav */
document.querySelectorAll('.nav a[href^="#"]').forEach(function(a){
  a.addEventListener('click',function(e){
    var el=document.querySelector(a.getAttribute('href'));
    if(el){e.preventDefault();window.scrollTo({top:el.offsetTop,behavior:'smooth'});}
  });
});
