#!/usr/bin/env python3
# Builds the IMALOO multi-page website. Each page is one Custom HTML block.
import json, re, sys, os
U = '/wp-content/uploads/2026/11/'
SP = json.load(open('/tmp/claude-0/site/sprites.json'))
SONGS = json.load(open('/tmp/claude-0/site/songs-compact.json'))
LANDS = open('/tmp/claude-0/site/lands.txt').read().split()

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap">'

CSS = r"""
/* IMALOO website. Each page keeps everything in one block: styles, page and scripts.
   WordPress wrapper reset: the page fills the whole window, with no theme header, footer or side gaps. */
.wp-site-blocks{padding:0!important}.wp-site-blocks>*,.wp-block-post-content>*{margin-block-start:0!important;margin-block-end:0!important;max-width:none!important}.wp-block-post-content,.entry-content{max-width:none!important;margin:0!important;padding:0!important}.imaloo-page h1,.imaloo-page h2,.imaloo-page h3{color:inherit;letter-spacing:normal;font-weight:700}.imaloo-page a{text-decoration:none}.imaloo-page footer a,.imaloo-page .ul a{text-decoration:underline}
/* Colours: bright pinks, purples and sky blue. No green. */
:root{--sun:#FFC94D;--berry:#FF5FA2;--sky:#4FB8FF;--grape:#8B5CF6;--bg:#FFF8FD;--band:#F4EEFF;--card:#FFFFFF;--ink:#3B2357;--muted:#76628F;--line:#EBDDFB;--display:"Fredoka","Baloo 2","Trebuchet MS",system-ui,sans-serif;--body:"Nunito","Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.6;overflow-x:hidden}img{max-width:100%}[hidden]{display:none!important}
.wrap{max-width:1100px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--display);line-height:1.15;text-wrap:balance;margin:0}h2{font-size:clamp(28px,4vw,40px)}p{margin:0}a{color:inherit}
.btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--display);font-weight:600;font-size:19px;text-decoration:none;border-radius:999px;padding:14px 28px;border:0;cursor:pointer}
.btn-main{background:linear-gradient(135deg,#FF5FA2,#FF8A5B);color:#fff;box-shadow:0 5px 0 #C2367A}.btn-main:hover{transform:translateY(-1px)}.btn-soft{background:rgba(255,255,255,.94);color:#3B2357}.btn:focus-visible,button:focus-visible,a:focus-visible{outline:3px solid var(--sky);outline-offset:3px}
/* Top menu: on every page */
.top{position:sticky;top:0;z-index:30;background:linear-gradient(90deg,#8B5CF6,#C86BFF 50%,#FF7EB6);box-shadow:0 4px 18px rgba(139,92,246,.25)}
.top .wrap{display:flex;align-items:center;gap:14px;padding-block:10px}
.logo{font-family:var(--display);font-weight:700;font-size:26px;color:#fff;letter-spacing:.04em;text-shadow:0 2px 8px rgba(0,0,0,.25);flex:none}
.menu{display:flex;gap:6px;flex:1;min-width:0;overflow-x:auto;scrollbar-width:none;justify-content:center}.menu::-webkit-scrollbar{display:none}
.menu a{flex:none;font-family:var(--display);font-weight:600;font-size:16px;color:#fff;padding:7px 13px;border-radius:999px;white-space:nowrap;transition:background .2s,transform .2s}
.menu a:hover{background:rgba(255,255,255,.2);transform:translateY(-2px)}.menu a[aria-current="page"]{background:#fff;color:var(--grape)}
.menu a .e{display:inline-block}.menu a:hover .e{animation:bob .6s ease}
.top .signin{flex:none;font-size:15px;padding:8px 16px}
@keyframes bob{0%,100%{transform:translateY(0)}40%{transform:translateY(-5px) rotate(-8deg)}70%{transform:translateY(1px) rotate(5deg)}}
@media (max-width:820px){.top .wrap{flex-wrap:wrap;gap:6px 10px;padding-block:8px}.logo{font-size:22px}.top .signin{margin-left:auto}.menu{order:3;flex-basis:100%;justify-content:flex-start;margin:0 -4px}.menu a{font-size:15px;padding:6px 11px}}
/* Page header band for inner pages */
.band{position:relative;overflow:hidden;color:#fff;background:linear-gradient(135deg,#8B5CF6 0%,#C86BFF 45%,#FF7EB6 100%);padding-block:56px 72px;text-align:center}
.band h1{font-size:clamp(34px,5vw,58px);text-shadow:0 3px 14px rgba(60,20,110,.35)}.band p{max-width:34em;margin:14px auto 0;font-size:clamp(17px,1.6vw,20px)}
.band::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:40px;background:var(--bg);clip-path:ellipse(60% 100% at 50% 100%)}
.band .floaty{position:absolute;font-size:clamp(28px,4vw,48px);animation:floaty 5s ease-in-out infinite;pointer-events:none}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(-6deg)}50%{transform:translateY(-16px) rotate(6deg)}}
section{scroll-margin-top:80px}.sec{padding-block:64px}.sec h2{text-align:center}.sec .sub{text-align:center;color:var(--muted);margin:10px auto 30px;max-width:36em}
.tint{background:linear-gradient(180deg,#F4EEFF,#FFEFF7)}
.cta{text-align:center;display:grid;gap:14px;justify-items:center;padding-block:56px}.cta p{color:var(--muted)}
.card{background:var(--card);border:2px solid var(--line);border-radius:24px;padding:24px;box-shadow:0 8px 24px rgba(139,92,246,.08)}
footer{background:linear-gradient(180deg,#F4EEFF,#FFE7F3);padding-block:36px;color:var(--muted);font-size:15px}footer .wrap{display:flex;flex-wrap:wrap;gap:12px 28px;justify-content:space-between}footer nav{display:flex;flex-wrap:wrap;gap:8px 20px}
/* Fairy sprinkles drifting over the page */
#sprinkles{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:40}
/* Confetti for the little games */
.conf{position:absolute;width:10px;height:14px;border-radius:3px;pointer-events:none;z-index:6;animation:conf 1.3s ease-out forwards}
@keyframes conf{from{transform:translate(0,0) rotate(0);opacity:1}to{transform:translate(var(--x),var(--y)) rotate(var(--r));opacity:0}}
@media (max-width:820px){.band .floaty{display:none}.band{padding-block:40px 60px}}
@media (prefers-reduced-motion:reduce){.band .floaty,.menu a:hover .e{animation:none}}
"""

def nav(cur):
    items = [('/', '🏠', 'Home'), ('/games/', '🎮', 'Games'), ('/books/', '📚', 'Books'), ('/fantasy-lands/', '🏰', 'Fantasy Lands'),
             ('/prices/', '⭐', 'Prices'), ('/how-it-works/', '🧸', 'How it works'), ('/safety/', '🛡️', 'Safety')]
    links = ''.join('<a href="%s"%s><span class="e" aria-hidden="true">%s</span> %s</a>' % (h, ' aria-current="page"' if h == cur else '', e, t) for h, e, t in items)
    return ('<canvas id="sprinkles" aria-hidden="true"></canvas>\n<header class="top"><div class="wrap">\n  <a class="logo" href="/">IMALOO</a>\n'
            '  <nav class="menu" aria-label="Pages">%s</nav>\n  <a class="btn btn-soft signin" href="https://app.imaloo.com.au">Sign in</a>\n</div></header>\n' % links)

FOOTER = """
<footer><div class="wrap">
  <span>© 2026 IMALOO, by Ambience Care WA Pty Ltd</span>
  <nav>
    <a href="/how-it-works/">How it works</a>
    <a href="/prices/">Prices</a>
    <a href="/safety/">Safety</a>
    <a href="https://app.imaloo.com.au/privacy">Privacy</a>
    <span>Help: <a href="mailto:support@imaloo.com.au">support@imaloo.com.au</a></span>
  </nav>
</div></footer>
"""

TRIAL = """
<div class="cta wrap">
  <a class="btn btn-main" href="https://app.imaloo.com.au">Start your 7-day free trial</a>
  <p>No card needed for the trial. Made in Australia.</p>
</div>
"""

RULE = """// IMPORTANT for anyone editing this script inside WordPress: never type two ampersands, and never put a
// "less than" sign straight before a letter. WordPress rewrites those and the whole script stops working.
// Use nested ifs and write comparisons the other way round (pages.length-1 > i).
"""

JS_SPRINKLES = r"""
// Fairy sprinkles: little golden, pink and white sparkles drifting gently down the page.
(function(){
  var c=document.getElementById('sprinkles');if(!c)return;if(!c.getContext)return;
  var g=c.getContext('2d'),W=0,H=0,dpr=Math.min(window.devicePixelRatio||1,2),bits=[];
  var calm=false;if(window.matchMedia){calm=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}
  var colours=['#FFD86B','#FF8FC7','#FFFFFF','#C9A8FF','#8FE3FF'];
  function size(){W=c.clientWidth;H=c.clientHeight;c.width=W*dpr;c.height=H*dpr;g.setTransform(dpr,0,0,dpr,0,0);}
  function make(top){return {x:Math.random()*W,y:top?-10:Math.random()*H,r:1+Math.random()*2.6,vy:.25+Math.random()*.6,vx:(Math.random()-.5)*.35,t:Math.random()*6.28,col:colours[Math.floor(Math.random()*colours.length)],star:(.35>Math.random())};}
  function star(x,y,r){g.beginPath();for(var k=0;8>k;k++){var a=k*Math.PI/4,rr=k%2?r*.4:r*1.9;g.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr);}g.closePath();g.fill();}
  size();window.addEventListener('resize',size);
  var count=Math.round(Math.min(70,W/18));for(var k=0;count>k;k++)bits.push(make(false));
  function frame(){
    g.clearRect(0,0,W,H);
    for(var k=0;bits.length>k;k++){var b=bits[k];
      if(!calm){b.y+=b.vy;b.x+=b.vx+Math.sin(b.t)*.2;b.t+=.03;}
      if(b.y>H+10||-10>b.x||b.x>W+10)bits[k]=b=make(true);
      g.globalAlpha=.55+.45*Math.sin(b.t*2);g.fillStyle=b.col;g.shadowColor=b.col;g.shadowBlur=6;
      if(b.star)star(b.x,b.y,b.r);else{g.beginPath();g.arc(b.x,b.y,b.r,0,6.283);g.fill();}
    }
    g.globalAlpha=1;g.shadowBlur=0;
    if(!calm)requestAnimationFrame(frame);
  }
  frame();
})();
"""

JS_CONFETTI = r"""
// Confetti burst inside a game box (used when a child gets it right).
function imalooConfetti(box,x,y){
  var cols=['#FF5FA2','#FFD23F','#4FB8FF','#B07CFF','#FF8A3D','#FFFFFF'];
  for(var k=0;28>k;k++){
    var p=document.createElement('i');p.className='conf';
    var a=Math.random()*6.283,d=60+Math.random()*140;
    p.style.left=x+'px';p.style.top=y+'px';p.style.background=cols[k%cols.length];
    p.style.setProperty('--x',(Math.cos(a)*d)+'px');p.style.setProperty('--y',(Math.sin(a)*d-40)+'px');p.style.setProperty('--r',(Math.random()*720-360)+'deg');
    box.appendChild(p);
    (function(el){setTimeout(function(){el.remove();},1400);})(p);
  }
}
"""

STORYBOOK_CSS = r"""
.book{padding-block:72px;background:linear-gradient(180deg,#FFF8FD,#FFF3D6)}.book h2{text-align:center}.book .sub{text-align:center;color:var(--muted);margin:10px auto 28px;max-width:34em}.reader{max-width:860px;margin:0 auto;background:#fff;border-radius:28px;box-shadow:0 18px 50px rgba(139,92,246,.18);overflow:hidden;border:3px solid #fff}.reader .pic{position:relative;aspect-ratio:16/9;background:#F4EEFF}.reader .pic img{width:100%;height:100%;object-fit:cover;display:block;animation:turn .45s ease}.reader .cover-title{position:absolute;inset:auto 0 0;padding:28px 20px 18px;text-align:center;color:#fff;background:linear-gradient(0deg,rgba(80,40,140,.85),rgba(80,40,140,0));font-family:var(--display)}.reader .cover-title b{display:block;font-size:clamp(26px,4.5vw,44px);line-height:1.1}.reader .cover-title span{font-size:clamp(15px,2vw,19px);opacity:.95}.reader .words{padding:20px 26px 6px;font-family:var(--display);font-size:clamp(18px,2.3vw,23px);line-height:1.5;min-height:6.2em;color:var(--ink)}.reader .bar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 18px 18px}.reader .bar button{font-family:var(--display);font-weight:600;font-size:17px;border:0;border-radius:999px;padding:10px 18px;cursor:pointer;background:#F4EEFF;color:var(--ink)}.reader .bar button.go{background:linear-gradient(135deg,#FF5FA2,#FF8A5B);color:#fff}.reader .bar button:disabled{opacity:.35;cursor:default}.reader .dots{display:flex;gap:7px}.reader .dots i{width:10px;height:10px;border-radius:50%;background:#E3D6FA}.reader .dots i.on{background:var(--berry)}@keyframes turn{from{opacity:0;transform:translateX(24px) scale(.98)}to{opacity:1;transform:none}}.book .after{text-align:center;margin-top:22px;color:var(--muted)}
@media (max-width:820px){.reader .words{padding:16px 18px 4px}.reader .bar button{font-size:15px;padding:9px 14px}}
"""

STORYBOOK_HTML = """
<section class="book" id="storybook"><div class="wrap">
  <h2>📚 Peek inside a storybook</h2>
  <p class="sub">Your child's toys become the stars of their very own book. Here's one we made with Teddy, Dolly and Pony. Read it on screen, hear it read aloud, print it at home, or order a real printed book.</p>
  <div class="reader" id="reader" aria-live="polite">
    <div class="pic" id="bk-pic"></div>
    <div class="words" id="bk-words"></div>
    <div class="bar">
      <button type="button" id="bk-prev" aria-label="Previous page">◀ Back</button>
      <div class="dots" id="bk-dots" aria-hidden="true"></div>
      <button type="button" id="bk-say" aria-label="Read this page to me">🔊 Read to me</button>
      <button type="button" class="go" id="bk-next" aria-label="Next page">Next ▶</button>
    </div>
  </div>
  <p class="after">Made in IMALOO from three toy photos. Your book stars <b>your</b> child's toys.</p>
</div></section>
"""

JS_STORYBOOK = r"""
// A storybook to peek inside: Teddy, Dolly and Pony's Big Sparkle Party.
// Each page has a real storyteller recording (book-voice-0.mp3 to book-voice-5.mp3). Never use a robot voice.
(function(){
  var U='/wp-content/uploads/2026/11/';
  var pages=[
    {img:U+'book-1-fairy.jpg',cover:true,text:'Tap Next to start the story!'},
    {img:U+'book-1-fairy.jpg',text:'Once upon a time, Teddy, Dolly and Pony found a tiny glowing invitation in the fairy garden. "The Big Sparkle Party is tonight!" whispered Dolly. "We need sprinkles, balloons and a cake!" Off we go, hip hip hooray, we\'re getting ready for the party today!'},
    {img:U+'book-2-candy.jpg',text:'Whoosh! A rainbow slide took them all the way to Candy Land. Pony scooped rainbow sprinkles into the basket while Teddy waved to the gumdrops. "Sprinkles, check!" giggled Dolly.'},
    {img:U+'book-3-balloons.jpg',text:'Next, a magic bubble floated them to the carnival. Pop, pop, hooray! They found the biggest, brightest bunch of balloons, and danced all the way home. Off we go, hip hip hooray, we\'re getting ready for the party today!'},
    {img:U+'book-4-sneak.jpg',text:'Back in the playroom, the friends hung bunting and twinkly fairy lights. Dolly put the candles on a big pink cake. "Shh, it\'s nearly time!" smiled Pony.'},
    {img:U+'book-5-surprise.jpg',text:'Then, SURPRISE! Confetti sparkled everywhere and everyone jumped for joy. It was the happiest Sparkle Party ever, and the friends danced until bedtime. Hip hip hooray! The End.'}
  ];
  pages.forEach(function(p,k){p.voice=U+'book-voice-'+k+'.mp3';});
  var last=pages.length-1;
  var voice=new Audio(),reading=false;voice.preload='none';
  var i=0,pic=document.getElementById('bk-pic'),words=document.getElementById('bk-words'),dots=document.getElementById('bk-dots'),
      prev=document.getElementById('bk-prev'),next=document.getElementById('bk-next'),sayBtn=document.getElementById('bk-say');
  if(!pic)return;
  pages.forEach(function(){dots.appendChild(document.createElement('i'));});
  function hush(){try{voice.pause();}catch(e){}}
  function readPage(){hush();voice.src=pages[i].voice;voice.currentTime=0;voice.play().catch(function(){});sayBtn.textContent='⏸ Stop reading';reading=true;}
  // When the reader finishes a page, turn to the next one by itself and keep reading to the end.
  voice.addEventListener('ended',function(){
    if(reading){
      if(last>i){setTimeout(function(){if(reading){if(voice.ended){i++;draw();}}},900);return;}
    }
    reading=false;sayBtn.textContent='🔊 Read to me';
  });
  function draw(){
    hush();
    var p=pages[i];
    pic.textContent='';
    var im=document.createElement('img');im.src=p.img;im.alt=p.cover?'Storybook cover: Teddy, Dolly and Pony':'Story page '+i;pic.appendChild(im);
    if(p.cover){var t=document.createElement('div');t.className='cover-title';var bb=document.createElement('b');bb.textContent='The Big Sparkle Party';var sp=document.createElement('span');sp.textContent='Starring Teddy, Dolly and Pony';t.appendChild(bb);t.appendChild(sp);pic.appendChild(t);}
    words.textContent=p.text;
    prev.disabled=(i===0);next.textContent=(i===last)?'Read again ↺':'Next ▶';
    [].forEach.call(dots.children,function(d,k){d.className=(k===i)?'on':'';});
    if(reading)readPage();else sayBtn.textContent='🔊 Read to me';
  }
  prev.addEventListener('click',function(){if(i>0){i--;draw();}});
  next.addEventListener('click',function(){i=(i===last)?0:i+1;draw();});
  sayBtn.addEventListener('click',function(){
    if(reading){if(!voice.paused){hush();reading=false;sayBtn.textContent='🔊 Read to me';return;}}
    readPage();
  });
  var x0=null;pic.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  pic.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;x0=null;if(Math.abs(dx)>50){if(0>dx)next.click();else prev.click();}});
  draw();
})();
"""

# ---------------- HOME ----------------
HOME_CSS = r"""
.hero{position:relative;color:#fff;background:linear-gradient(135deg,#8B5CF6 0%,#C86BFF 45%,#FF7EB6 100%)}.stage{position:relative;overflow:hidden}.scene{position:relative;width:100%;aspect-ratio:16/9;max-height:calc(100vh - 60px);background:url(/wp-content/uploads/2026/11/hero-forest.jpg) center/cover no-repeat;overflow:hidden}.scene::before{content:"";position:absolute;inset:auto 0 0;height:14%;background:linear-gradient(0deg,rgba(139,92,246,.55),rgba(139,92,246,0));z-index:2;pointer-events:none}
.hero-copy{max-width:1100px;margin:0 auto;padding-block:36px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:16px;justify-items:center;text-align:center;min-width:0}.hero h1{font-size:clamp(34px,4.6vw,60px);text-shadow:0 3px 14px rgba(0,0,0,.4)}.hero h1 span{color:#FFE45C}.hero p{font-size:clamp(17px,1.5vw,20px);max-width:30em;text-shadow:0 1px 6px rgba(0,0,0,.5)}.hero .ctas{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}.hero small{opacity:.92;text-shadow:0 1px 4px rgba(0,0,0,.5)}
.teddy-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 50%;display:block;transition:opacity .6s ease}#teddy-wake{z-index:2}#teddy-play{z-index:1}.teddy-video.fade{opacity:0}
.zzz{position:absolute;z-index:3;left:53%;top:46%;pointer-events:none;font-family:var(--display);font-weight:700;color:#fff;text-shadow:0 2px 8px rgba(80,40,140,.6)}.zzz span{position:absolute;opacity:0;font-size:clamp(16px,2.2vw,30px);animation:snooze 3s ease-in-out infinite}.zzz span:nth-child(2){animation-delay:1s;font-size:clamp(20px,2.8vw,38px)}.zzz span:nth-child(3){animation-delay:2s;font-size:clamp(24px,3.4vw,46px)}@keyframes snooze{0%{opacity:0;transform:translate(0,0) rotate(-8deg)}20%{opacity:1}100%{opacity:0;transform:translate(2.4em,-2.6em) rotate(12deg)}}
.wake-hint{position:absolute;z-index:3;left:50%;bottom:9%;transform:translateX(-50%);font-family:var(--display);font-weight:600;font-size:clamp(15px,1.8vw,21px);color:#fff;padding:.45em 1.1em;border-radius:999px;background:linear-gradient(135deg,rgba(255,95,162,.85),rgba(139,92,246,.85));white-space:nowrap;pointer-events:none;animation:hintglow 2.2s ease-in-out infinite}@keyframes hintglow{0%,100%{box-shadow:0 0 0 0 rgba(255,216,107,.55);transform:translateX(-50%) scale(1)}50%{box-shadow:0 0 22px 6px rgba(255,216,107,.55);transform:translateX(-50%) scale(1.05)}}@media (prefers-reduced-motion:reduce){.zzz span,.wake-hint{animation:none}.zzz span{opacity:1}}
.replay{position:absolute;z-index:3;right:max(16px,env(safe-area-inset-right,0px));bottom:16px;font-size:16px;padding:10px 18px}@media (max-width:820px){.replay{bottom:10px;font-size:14px;padding:8px 14px}}
.how{padding-block:72px}.how h2{text-align:center;margin-bottom:36px}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.step{background:var(--card);border:2px solid var(--line);border-radius:24px;padding:24px;display:grid;gap:10px;align-content:start;box-shadow:0 8px 24px rgba(139,92,246,.08)}.step .n{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-family:var(--display);font-weight:700;font-size:22px;color:#fff}.step:nth-child(1) .n{background:var(--sky)}.step:nth-child(2) .n{background:var(--grape)}.step:nth-child(3) .n{background:var(--berry)}.step h3{font-size:24px}.step p{color:var(--muted)}
/* Big doors to the other pages */
.doors{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.door{position:relative;display:block;border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 14px 34px rgba(139,92,246,.18);transition:transform .25s}
.door:hover{transform:translateY(-6px) rotate(-1deg)}.door:nth-child(2):hover{transform:translateY(-6px) rotate(1deg)}
.door .pic{aspect-ratio:4/3;background-size:cover;background-position:center;position:relative}
.door .pic video{width:100%;height:100%;object-fit:cover;display:block}
.door .lbl{padding:16px 20px 20px}.door h3{font-size:26px}.door p{color:var(--muted);margin-top:4px}
.door .go{display:inline-block;margin-top:10px;font-family:var(--display);font-weight:600;color:var(--berry)}
.door .badge{position:absolute;top:12px;left:12px;font-size:34px;filter:drop-shadow(0 3px 6px rgba(0,0,0,.25));animation:floaty 4s ease-in-out infinite}
.minis{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:24px}
.mini{display:flex;align-items:center;gap:14px;background:#fff;border:2px solid var(--line);border-radius:20px;padding:14px 18px;transition:transform .2s}.mini:hover{transform:translateY(-3px)}
.mini .ic{font-size:30px}.mini b{font-family:var(--display);font-size:19px;display:block}.mini span{color:var(--muted);font-size:15px}
.safe{background:linear-gradient(135deg,#4FB8FF,#8B5CF6);color:#fff;padding-block:56px}.safe .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}.safe blockquote{margin:0;font-family:var(--display);font-size:clamp(24px,3vw,32px);line-height:1.25}.safe ul{margin:0;padding-left:22px;display:grid;gap:8px}.safe a{font-weight:700;text-decoration:underline}
@media (max-width:820px){.steps,.doors,.minis,.safe .wrap{grid-template-columns:1fr}}
"""

HOME_HTML = """
<section class="hero">
  <div class="stage"><div class="scene">
    <video class="teddy-video" id="teddy-wake" src="https://videos.files.wordpress.com/n1vJuENw/teddy-wake-v2.mp4" poster="/wp-content/uploads/2026/11/teddy-walk-poster.jpg" playsinline preload="auto" aria-label="A teddy bear asleep on the forest path. Tap to wake him: he walks up waving and calling Hi! Hi!, then says Hello! Good to see you! Come and play in our magic worlds on Imaloo!"></video>
    <video class="teddy-video" id="teddy-play" src="https://videos.files.wordpress.com/uRcCmUWU/teddy-play.mp4" muted playsinline loop preload="auto" hidden aria-label="The teddy bear waves, dances and claps in the forest"></video>
    <div class="zzz" id="zzz" aria-hidden="true"><span>z</span><span>z</span><span>z</span></div>
    <div class="wake-hint" id="wake-hint" role="note">Tap to wake Teddy ✨</div>
    <button class="btn btn-soft replay" type="button" id="replay" hidden>▶ Watch again</button>
  </div></div>
  <div class="hero-copy">
    <h1>Your child's toys <span>come to life</span></h1>
    <p>Take a photo of a real teddy, doll or pony, and watch it wake up in bright, magical worlds. Make pictures, storybooks and little movies starring your child's very own toy.</p>
    <div class="ctas">
      <a class="btn btn-main" href="https://app.imaloo.com.au">Start your 7-day free trial</a>
    </div>
    <small>No card needed for the trial. Made in Australia.</small>
  </div>
</section>

<section class="how"><div class="wrap">
  <h2>As easy as one, two, three</h2>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Snap a toy</h3><p>A grown-up takes a photo of a real toy, front and back. Every photo is checked to make sure it's a toy.</p></div>
    <div class="step"><div class="n">2</div><h3>Pick a world</h3><p>A sunny Aussie beach, a castle, outer space or a deep forest. Big picture buttons, so little ones can choose on their own.</p></div>
    <div class="step"><div class="n">3</div><h3>Watch it come alive</h3><p>IMALOO makes a picture or a short movie with a story read aloud. Watch it big on the TV with the whole family.</p></div>
  </div>
  <p style="text-align:center;margin-top:24px"><a class="btn btn-soft" style="border:2px solid var(--line)" href="/how-it-works/">🧸 See how it works, step by step</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
  <h2>Come and explore ✨</h2>
  <p class="sub">Tap a door to step inside.</p>
  <div class="doors">
    <a class="door" href="/games/"><div class="pic" style="background-image:url(/wp-content/uploads/2026/11/imaloo-fruit-garden.jpg)"><span class="badge" aria-hidden="true">🎮</span></div><div class="lbl"><h3>Games</h3><p>Catch Party bubbles, Fruit Maths, Read &amp; Spell and sing-along songs. Try them right here!</p><span class="go">Play now ▶</span></div></a>
    <a class="door" href="/books/"><div class="pic" style="background-image:url(/wp-content/uploads/2026/11/book-5-surprise.jpg)"><span class="badge" aria-hidden="true">📚</span></div><div class="lbl"><h3>Books</h3><p>Storybooks starring your child's own toys, read aloud by a bubbly storyteller.</p><span class="go">Open the books ▶</span></div></a>
    <a class="door" href="/fantasy-lands/"><div class="pic"><video src="https://videos.files.wordpress.com/B3Ra78yb/w-castle.mp4" poster="/wp-content/uploads/2026/11/w-castle.jpg" autoplay muted loop playsinline preload="metadata" aria-label="A fairytale castle"></video><span class="badge" aria-hidden="true">🏰</span></div><div class="lbl"><h3>Fantasy Lands</h3><p>54 bright, magical places, from the Aussie bush to a castle in the clouds.</p><span class="go">Explore ▶</span></div></a>
  </div>
  <div class="minis">
    <a class="mini" href="/prices/"><span class="ic" aria-hidden="true">⭐</span><div><b>Prices</b><span>From $12.99 a month. 7 days free.</span></div></a>
    <a class="mini" href="/how-it-works/"><span class="ic" aria-hidden="true">🧸</span><div><b>How it works</b><span>Easy steps for grown-ups.</span></div></a>
    <a class="mini" href="/safety/"><span class="ic" aria-hidden="true">🛡️</span><div><b>Safety</b><span>Toys only. Private to your family.</span></div></a>
  </div>
</div></section>
""" + STORYBOOK_HTML + """
<section class="safe"><div class="wrap">
  <blockquote>Imaloo — where toys come to life and childhood stays innocent.</blockquote>
  <div>
    <ul>
      <li>Only photos of toys are allowed. Photos of people, screens and magazines are refused.</li>
      <li>Every picture and movie is checked before your child sees it.</li>
      <li>No ads. Your family's toys, photos and movies are private to your family.</li>
    </ul>
    <p style="margin-top:16px"><a href="/safety/">How we keep children safe</a></p>
  </div>
</div></section>
""" + TRIAL

JS_TEDDY = r"""
// The teddy sleeps on the path until the visitor taps anywhere. Then the whole
// wake-up (walk, "Hi! Hi!", hello) plays from the start with his voice, and he
// fades gently into playing. Browsers only allow sound after that first tap.
(function(){
  var wake=document.getElementById('teddy-wake'),play=document.getElementById('teddy-play'),
      hint=document.getElementById('wake-hint'),zzz=document.getElementById('zzz'),replay=document.getElementById('replay'),asleep=true;
  try{play.load();}catch(e){}
  function start(){
    asleep=false;hint.hidden=true;zzz.hidden=true;replay.hidden=true;
    play.pause();wake.hidden=false;wake.classList.remove('fade');wake.currentTime=0;wake.muted=false;
    var p=wake.play();
    if(p){if(p.catch){p.catch(function(){wake.muted=true;wake.play().catch(function(){});});}}
  }
  // Phones only allow sound after a finished tap (a click, on finger lift), not when a finger first touches the screen.
  // If Teddy still had to start without sound, the next tap turns his voice on.
  function tapped(e){
    // Taps on links, buttons and the storybook don't wake Teddy, so they keep working normally.
    if(e){if(e.target){if(e.target.closest){if(e.target.closest('a,button,#reader')){if(!e.target.closest('.scene'))return;}}}}
    if(asleep){start();return;}
    if(wake.muted){if(!wake.hidden){if(!wake.ended){wake.muted=false;}}}
  }
  document.addEventListener('click',tapped);
  document.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' ')tapped();});
  wake.addEventListener('ended',function(){
    // Teddy keeps playing underneath while the wake-up fades away, so there is no jump.
    play.hidden=false;play.currentTime=0;play.play().catch(function(){});
    wake.classList.add('fade');
    setTimeout(function(){wake.hidden=true;},650);
    replay.hidden=false;
  });
  replay.addEventListener('click',function(e){e.stopPropagation();start();});
})();
"""

# ---------------- GAMES ----------------
GAMES_CSS = r"""
.game{display:grid;grid-template-columns:260px 1fr;gap:40px;align-items:center;padding-block:56px}
.game.alt{grid-template-columns:1fr 260px}.game.alt .phone{order:2}
.phone{position:relative;border-radius:38px;background:#2b1d40;padding:10px;box-shadow:0 20px 50px rgba(59,35,87,.3);transform:rotate(-3deg);transition:transform .3s}
.phone:hover{transform:rotate(0) scale(1.03)}.game.alt .phone{transform:rotate(3deg)}
.phone img{display:block;border-radius:30px;width:100%;aspect-ratio:1/2;object-fit:cover}
.gtext h2{text-align:left;font-size:clamp(28px,3.6vw,40px)}.gtext .lead{color:var(--muted);margin:8px 0 16px}
.gtext ul{margin:0 0 18px;padding-left:22px;color:var(--muted)}
.chip{display:inline-block;font-family:var(--display);font-weight:600;font-size:14px;border-radius:999px;padding:3px 12px;margin:0 6px 6px 0;color:#fff}
.chip.a{background:#FFB703}.chip.b{background:var(--sky)}.chip.c{background:var(--berry)}
.play{position:relative;border-radius:26px;overflow:hidden;box-shadow:0 14px 36px rgba(139,92,246,.22);border:4px solid #fff;min-height:330px;user-select:none;-webkit-user-select:none}
.play .start{position:absolute;inset:0;display:grid;place-items:center;align-content:center;gap:10px;background:rgba(59,35,87,.35);z-index:5;color:#fff;text-align:center;padding:16px;font-family:var(--display)}
.play .start b{font-size:clamp(22px,3vw,30px);text-shadow:0 2px 10px rgba(0,0,0,.4)}
.play .start .btn{animation:pulse 1.8s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}
.say{position:relative;z-index:2;margin:14px auto 0;width:max-content;max-width:calc(100% - 28px);background:rgba(255,255,255,.95);border-radius:999px;padding:8px 18px;font-family:var(--display);font-weight:600;font-size:clamp(17px,2.2vw,21px);color:var(--ink);box-shadow:0 4px 14px rgba(0,0,0,.12);text-align:center}

/* Catch Party */
.cp-sec{padding-block:56px 24px}
.cp-head{display:grid;grid-template-columns:1fr auto;gap:20px;align-items:end;margin-bottom:18px}
.cp-head h2{text-align:left;font-size:clamp(30px,4vw,44px)}.cp-head .lead{color:var(--muted);margin-top:8px;max-width:40em}
.new{display:inline-block;background:linear-gradient(135deg,#FFD23F,#FF8A3D);color:#fff;font-family:var(--display);font-weight:700;font-size:15px;border-radius:999px;padding:4px 12px;margin-left:8px;vertical-align:middle;animation:pulse 1.6s ease-in-out infinite}
#cp{aspect-ratio:16/9;min-height:420px;max-height:640px;background:#bfe6ff center/cover no-repeat;transition:background-image .6s}
#cp-layer{position:absolute;inset:0;z-index:2;overflow:hidden}
.f{position:absolute;bottom:-120px;border:0;padding:0;background:none;cursor:pointer;animation:rise linear forwards;-webkit-tap-highlight-color:transparent;touch-action:manipulation}
.f i{display:block;width:100%;height:100%}
.bub i{border-radius:50%;border:2px solid #ffffffcc;background:radial-gradient(circle at 30% 28%,#fffffff0 0 8%,#bfe6ffaa 20%,#9fd8ff55 45%,#c9a2ff55 72%,#ffffff88 100%);box-shadow:inset -6px -8px 14px #ffffff55}
.itm i{background-image:url(/wp-content/uploads/2026/11/imaloo-catch-items.webp);background-size:800% 100%;filter:drop-shadow(0 6px 6px rgba(0,0,0,.35));animation:sway 1.3s ease-in-out infinite}
.itm.flut i{animation:flut .35s ease-in-out infinite alternate}
@keyframes rise{to{transform:translateY(calc(-1 * var(--h,500px) - 160px)) translateX(var(--dx,20px))}}
@keyframes sway{50%{transform:translateX(10px) rotate(8deg)}}
@keyframes flut{to{transform:scaleX(.82) rotate(-6deg)}}
.drop{position:absolute;z-index:6;pointer-events:none;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 18%,#d8f1ffdd 40%,#a9d8ffaa 70%,#c9a2ff88 100%);animation:conf .7s ease-out forwards}
.flyer{position:absolute;z-index:7;pointer-events:none;background-image:url(/wp-content/uploads/2026/11/imaloo-catch-items.webp);background-size:800% 100%;transition:all .65s cubic-bezier(.5,-.3,.6,1)}
.jar{position:absolute;z-index:4;right:14px;bottom:14px;display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.92);border-radius:999px;padding:6px 16px 6px 8px;box-shadow:0 6px 16px rgba(0,0,0,.18);font-family:var(--display);font-weight:700;font-size:28px;color:var(--ink)}
.jar i{width:46px;height:46px;background-image:url(/wp-content/uploads/2026/11/imaloo-catch-items.webp);background-size:800% 100%}
.jar.bump{animation:hop .4s ease}
.cp-top{position:absolute;z-index:4;left:0;right:0;top:12px;display:flex;justify-content:center;pointer-events:none}
.cp-top .say{margin:0;pointer-events:none}
.banner{position:absolute;z-index:5;left:50%;top:40%;transform:translate(-50%,-50%) scale(.6);opacity:0;pointer-events:none;font-family:var(--display);font-weight:700;font-size:clamp(34px,6vw,64px);color:#fff;text-shadow:0 4px 18px rgba(80,20,120,.6);transition:all .35s;white-space:nowrap}
.banner.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
.cp-btns{position:absolute;z-index:4;left:14px;bottom:14px;display:flex;gap:8px}
.cp-btns .btn{font-size:15px;padding:8px 14px}
.cp-end{position:absolute;inset:0;z-index:6;display:grid;place-items:center;align-content:center;gap:14px;text-align:center;padding:16px;background:rgba(59,35,87,.45);color:#fff;font-family:var(--display)}
.cp-end b{font-size:clamp(24px,3.4vw,36px);text-shadow:0 2px 10px rgba(0,0,0,.4);max-width:20em}
.cp-start .rounds{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
.cp-start .rounds i{width:54px;height:54px;border-radius:16px;background-color:rgba(255,255,255,.85);background-image:url(/wp-content/uploads/2026/11/imaloo-catch-items.webp);background-size:800% 100%}
@media (max-width:820px){.cp-head{grid-template-columns:1fr}#cp{aspect-ratio:auto;height:520px;min-height:0}.jar{font-size:22px}.jar i{width:36px;height:36px}}
/* Fruit Maths */
#fm{background:url(/wp-content/uploads/2026/11/imaloo-fruit-garden.jpg) center/cover}
.rug{position:relative;z-index:2;margin:18px auto 0;width:min(92%,560px);min-height:130px;border-radius:24px;background:repeating-linear-gradient(45deg,#ff6b81 0 18px,#fff 18px 36px);box-shadow:0 8px 20px rgba(0,0,0,.18);display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px;padding:12px}
.fruit{position:relative;width:clamp(64px,13vw,92px);aspect-ratio:1;border:0;padding:0;cursor:pointer;background-color:transparent;background-image:url(/wp-content/uploads/2026/11/imaloo-fruit-sprite.webp);background-size:800% 100%;filter:drop-shadow(0 4px 4px rgba(0,0,0,.25));transition:transform .2s}
.fruit:hover{transform:scale(1.08)}.fruit.counted{animation:hop .45s ease}
.fruit .num{position:absolute;top:-10px;right:-6px;width:34px;height:34px;border-radius:50%;background:var(--grape);color:#fff;font-family:var(--display);font-weight:700;font-size:20px;display:grid;place-items:center;box-shadow:0 3px 8px rgba(0,0,0,.25)}
@keyframes hop{0%{transform:translateY(0)}40%{transform:translateY(-22px) scale(1.12)}100%{transform:translateY(0)}}
.answers{position:relative;z-index:2;display:flex;justify-content:center;gap:14px;margin:16px 0 18px}
.answers button{width:clamp(64px,12vw,82px);aspect-ratio:1;border-radius:22px;border:0;cursor:pointer;font-family:var(--display);font-weight:700;font-size:clamp(30px,5vw,40px);color:#fff;box-shadow:0 5px 0 rgba(0,0,0,.18)}
.answers button:nth-child(1){background:var(--sky)}.answers button:nth-child(2){background:var(--berry)}.answers button:nth-child(3){background:#FFB703}
.answers button.no{animation:nope .4s}.answers button.yes{transform:scale(1.15)}
@keyframes nope{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
.again{position:relative;z-index:2;display:block;margin:0 auto 16px}
/* Read & Spell */
#rs{background:linear-gradient(160deg,#FFE3F1,#E9DDFF 55%,#D7F0FF)}
.picks{position:relative;z-index:2;display:flex;justify-content:center;flex-wrap:wrap;gap:8px;padding:14px 10px 0}
.pick{width:62px;height:62px;border-radius:18px;border:3px solid #fff;cursor:pointer;background-color:#fff;background-image:url(/wp-content/uploads/2026/11/imaloo-spell-toys.webp);background-size:600% 100%;box-shadow:0 4px 10px rgba(0,0,0,.12);transition:transform .2s}
.pick:hover{transform:translateY(-3px)}.pick[aria-pressed="true"]{border-color:var(--grape);transform:scale(1.1)}
.word{position:relative;z-index:2;display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;padding:12px}
.toy{width:clamp(110px,20vw,150px);aspect-ratio:1;background-image:url(/wp-content/uploads/2026/11/imaloo-spell-toys.webp);background-size:600% 100%;filter:drop-shadow(0 8px 10px rgba(0,0,0,.2))}
.toy.won{animation:hop .6s ease 2}
.slots{display:flex;gap:8px}.slot{width:clamp(48px,9vw,64px);height:clamp(58px,10vw,74px);border-radius:16px;border:3px dashed #B9A3E8;display:grid;place-items:center;font-family:var(--display);font-weight:700;font-size:clamp(30px,5vw,42px);color:#fff;background:rgba(255,255,255,.5)}
.slot.full{border:0;background:var(--grape);animation:hop .4s ease}.slot.next{border-color:var(--berry);background:rgba(255,95,162,.15)}
.tiles{position:relative;z-index:2;display:flex;justify-content:center;flex-wrap:wrap;gap:10px;padding:4px 10px 18px}
.tile{width:clamp(56px,10vw,70px);height:clamp(56px,10vw,70px);border-radius:18px;border:0;cursor:pointer;font-family:var(--display);font-weight:700;font-size:clamp(30px,5vw,40px);color:#fff;box-shadow:0 5px 0 rgba(0,0,0,.18);touch-action:manipulation}
.tile:nth-child(4n+1){background:#FF5FA2}.tile:nth-child(4n+2){background:#4FB8FF}.tile:nth-child(4n+3){background:#FFB703}.tile:nth-child(4n+4){background:#8B5CF6}
.tile.glow{box-shadow:0 0 0 4px #FFE45C,0 0 18px 6px rgba(255,228,92,.8)}.tile.used{opacity:0;pointer-events:none;transition:opacity .3s}.tile.no{animation:nope .4s}
.story{position:relative;z-index:2;text-align:center;font-family:var(--display);font-size:clamp(18px,2.4vw,22px);padding:0 14px 16px;color:var(--ink)}
/* Songs */
#sg{background:linear-gradient(135deg,#8B5CF6,#FF5FA2 60%,#FFB36B);color:#fff}
.songs{position:relative;z-index:2;display:flex;justify-content:center;flex-wrap:wrap;gap:10px;padding:16px 10px 4px}
.songs button{font-family:var(--display);font-weight:600;font-size:17px;border:0;border-radius:999px;padding:10px 16px;cursor:pointer;background:rgba(255,255,255,.92);color:var(--ink)}
.songs button[aria-pressed="true"]{background:#FFE45C}
.lyric{position:relative;z-index:2;min-height:150px;display:grid;place-items:center;text-align:center;padding:18px 16px 26px;font-family:var(--display);font-weight:700;font-size:clamp(24px,4vw,40px);line-height:1.3;text-shadow:0 2px 10px rgba(80,20,90,.35)}
.lyric .w{display:inline-block;margin:0 .14em;transition:color .15s,transform .15s}.lyric .w.on{color:#FFE45C;transform:translateY(-4px) scale(1.08)}
.lyric .nextline{display:block;font-size:.55em;opacity:.75;margin-top:10px}
.note{position:absolute;z-index:1;bottom:-30px;font-size:30px;animation:rise 4s linear forwards;pointer-events:none}
@keyframes rise{to{transform:translateY(-420px) rotate(30deg);opacity:0}}
.stopbar{position:relative;z-index:2;text-align:center;padding-bottom:16px}
@media (max-width:820px){.game,.game.alt{grid-template-columns:1fr;gap:24px;padding-block:40px}.game.alt .phone{order:0}.phone{width:200px;margin:0 auto}.gtext h2{text-align:center}.gtext .lead{text-align:center}}
"""

def games_html():
    return """
<section class="band">
  <span class="floaty" style="left:6%;top:24%" aria-hidden="true">🍓</span><span class="floaty" style="right:7%;top:20%;animation-delay:1s" aria-hidden="true">🔤</span><span class="floaty" style="left:16%;bottom:22%;animation-delay:2s" aria-hidden="true">🫧</span><span class="floaty" style="right:16%;bottom:26%;animation-delay:3s" aria-hidden="true">⭐</span>
  <h1>🎮 Games kids love</h1>
  <p>Learning that feels like play. Every game is in the IMALOO app, and you can try a little taste of each one right here. Turn your sound on!</p>
</section>

<div class="wrap">
<section class="cp-sec" id="catch-party">
  <div class="cp-head"><div>
    <h2>🎉 Catch Party <span class="new">NEW!</span></h2>
    <p class="lead">Bubbles float up through bright, magical worlds. Catch the butterflies, trucks, puppies, fairies, candy and bees, and pop the bubbles! A bubbly storyteller tells children what to catch next. In the app, it's also the fun little game to play while their movie is being made.</p>
  </div></div>
  <div class="play" id="cp">
    <div id="cp-layer"></div>
    <div class="cp-top"><div class="say" id="cp-say">Catch the butterflies!</div></div>
    <div class="banner" id="cp-banner"></div>
    <div class="jar" id="cp-jar" aria-live="polite"><i id="cp-jar-img"></i><span id="cp-count">0</span></div>
    <div class="cp-btns" id="cp-btns" hidden><button class="btn btn-soft" type="button" id="cp-next">Next ▶</button><button class="btn btn-soft" type="button" id="cp-stop">⏹ Stop</button></div>
    <div class="start cp-start" id="cp-start"><b>Catch what the storyteller asks for!</b><div class="rounds" aria-hidden="true"><i style="background-position:0 0"></i><i style="background-position:14.286% 0"></i><i style="background-position:28.571% 0"></i><i style="background-position:42.857% 0"></i><i style="background-position:57.143% 0"></i><i style="background-position:71.429% 0"></i><i style="background-position:85.714% 0"></i></div><button class="btn btn-main" type="button">🔊 Tap to play</button></div>
    <div class="cp-end" id="cp-end" hidden><b id="cp-msg"></b><button class="btn btn-main" type="button" id="cp-again">🎉 Play again</button></div>
  </div>
</section>

<section class="game" id="fruit-maths">
  <div class="phone"><img src="/wp-content/uploads/2026/11/imaloo-shot-fruit-maths.jpg" alt="Fruit Maths Party in the IMALOO app" loading="lazy"></div>
  <div class="gtext">
    <h2>🍎 Fruit Maths Party</h2>
    <p class="lead">Real-looking fruit on a picnic rug in a sunny garden. Children count, add and take away, with a bubbly storyteller cheering them on.</p>
    <p><span class="chip a">🐣 1-3 count to 10</span><span class="chip b">🐥 3-4 add to 20</span><span class="chip c">🦁 4-5 up to 50</span></p>
    <ul><li>Starts small and grows as your child gets it right</li><li>Confetti, stars and a Fruit Party for five in a row</li><li>A gentle count-along when an answer is wrong</li></ul>
    <div class="play" id="fm">
      <div class="start" id="fm-start"><b>Can you count the fruit?</b><button class="btn btn-main" type="button">🔊 Tap to play</button></div>
      <div class="say" id="fm-say">Let's count the fruit!</div>
      <div class="rug" id="fm-rug" aria-live="polite"></div>
      <div class="answers" id="fm-ans" hidden></div>
      <button class="btn btn-soft again" type="button" id="fm-again" hidden>🍓 Play again</button>
    </div>
  </div>
</section>

<section class="game alt" id="read-and-spell">
  <div class="phone"><img src="/wp-content/uploads/2026/11/imaloo-shot-read-and-spell.jpg" alt="Read and Spell in the IMALOO app" loading="lazy"></div>
  <div class="gtext">
    <h2>🔤 Read &amp; Spell</h2>
    <p class="lead">Life-like animals and things to spell, with letters that light up. The storyteller spells along, then reads a little story about each word.</p>
    <p><span class="chip a">🐣 1-3 first letter</span><span class="chip b">🐥 3-4 spell together</span><span class="chip c">🦁 4-5 spell alone</span></p>
    <ul><li>45 words, 15 for each age</li><li>Every word won goes into My Toy Box</li><li>A little picture story for every word</li></ul>
    <div class="play" id="rs">
      <div class="start" id="rs-start"><b>Pick an animal and spell it!</b><button class="btn btn-main" type="button">🔊 Tap to play</button></div>
      <div class="picks" id="rs-picks"></div>
      <div class="say" id="rs-say">Pick one to spell!</div>
      <div class="word"><div class="toy" id="rs-toy" role="img" aria-label=""></div><div class="slots" id="rs-slots"></div></div>
      <div class="tiles" id="rs-tiles"></div>
      <div class="story" id="rs-story"></div>
    </div>
  </div>
</section>

<section class="game" id="songs">
  <div class="phone"><img src="/wp-content/uploads/2026/11/imaloo-shot-songs.jpg" alt="Sing-along songs in the IMALOO app" loading="lazy"></div>
  <div class="gtext">
    <h2>🎵 Sing-along songs</h2>
    <p class="lead">12 happy IMALOO songs. The words light up as they are sung, and in party mode your child's own toys dance on the screen.</p>
    <ul><li>Twinkle Twinkle Little Toy, Down on the Farm, Little Blue Dolphin and more</li><li>Big karaoke words, perfect for little readers</li><li>Party mode with confetti and dancing toys</li></ul>
    <div class="play" id="sg">
      <div class="songs" id="sg-list"></div>
      <div class="lyric" id="sg-lyric" aria-live="off">Pick a song and sing along! 🎤</div>
      <div class="stopbar"><button class="btn btn-soft" type="button" id="sg-stop" hidden>⏹ Stop</button></div>
    </div>
  </div>
</section>
</div>

<section class="sec tint"><div class="wrap" style="text-align:center">
  <h2>All the games are in every plan</h2>
  <p class="sub">Catch Party, Fruit Maths, Read &amp; Spell and Songs are unlimited, with no ads. Little ones choose with big picture buttons, so there's hardly any reading needed.</p>
  <a class="btn btn-main" href="https://app.imaloo.com.au">Start your 7-day free trial</a>
</div></section>
"""

def games_js():
    fm = SP['fm']; rs = SP['rs']
    songs = {'twinkle-toy': ['⭐ Twinkle Twinkle Little Toy', SONGS['twinkle-toy']],
             'toy-parade': ['🥁 The Toy Parade', SONGS['toy-parade']],
             'counting-fruit': ['🍎 Counting Fruit', SONGS['counting-fruit']]}
    return (r"""
// A tiny voice player for the games. Each game's real recorded storyteller lines are joined in one
// sound file, and each line is played from its start time for its length. Never use a robot voice.
function imalooVoice(src,lines){
  var a=new Audio(src),queue=[],timer=null,busy=false,unlocked=false;a.preload='auto';
  function stop(){queue=[];clearTimeout(timer);busy=false;try{a.pause();}catch(e){}}
  function nextLine(){
    clearTimeout(timer);
    if(queue.length===0){busy=false;try{a.pause();}catch(e){}return;}
    var item=queue.shift(),seg=lines[item.k];
    if(!seg){if(item.cb)item.cb();nextLine();return;}
    busy=true;
    try{a.currentTime=seg[0];}catch(e){}
    var p=a.play();if(p){if(p.catch){p.catch(function(){});}}
    timer=setTimeout(function(){try{a.pause();}catch(e){}if(item.cb)item.cb();nextLine();},seg[1]*1000+80);
  }
  return {
    unlock:function(){if(unlocked)return;unlocked=true;var p=a.play();if(p){if(p.then){p.then(function(){if(!busy)a.pause();}).catch(function(){});}}},
    say:function(keys,done){stop();keys.forEach(function(k,n){queue.push({k:k,cb:(n===keys.length-1)?done:null});});nextLine();},
    stop:stop,
    idle:function(){return !busy;}
  };
}
function imalooShuffle(arr){for(var k=arr.length-1;k>0;k--){var j=Math.floor(Math.random()*(k+1));var t=arr[k];arr[k]=arr[j];arr[j]=t;}return arr;}

// Catch Party: tap the things the storyteller asks for, and pop the bubbles.
(function(){
  var box=document.getElementById('cp');if(!box)return;
  var V=imalooVoice('/wp-content/uploads/2026/11/imaloo-catch-voice.mp3',""" + json.dumps(SP['cp'], separators=(',', ':')) + r""");
  var S=imalooVoice('/wp-content/uploads/2026/11/imaloo-catch-sfx.mp3',""" + json.dumps(SP['cps'], separators=(',', ':')) + r""");
  var U='/wp-content/uploads/2026/11/imaloo-catch-';
  var T=[
    {id:'butterfly',many:'butterflies',word:'Butterflies!',img:[0],flut:true},
    {id:'truck',many:'trucks',word:'Trucks!',img:[1]},
    {id:'puppy',many:'puppies',word:'Puppies!',img:[2]},
    {id:'fairy',many:'fairies',word:'Fairies!',img:[3]},
    {id:'candy',many:'candy',word:'Candy!',img:[4,7]},
    {id:'bubble',many:'bubbles',word:'Bubbles!',img:[5],only:true},
    {id:'bee',many:'bees',word:'Bees!',img:[6],flut:true}
  ];
  T.forEach(function(t){var im=new Image();im.src=U+t.id+'.jpg';});
  var layer=document.getElementById('cp-layer'),say=document.getElementById('cp-say'),banner=document.getElementById('cp-banner'),jarImg=document.getElementById('cp-jar-img'),countEl=document.getElementById('cp-count'),jar=document.getElementById('cp-jar'),btns=document.getElementById('cp-btns'),start=document.getElementById('cp-start'),end=document.getElementById('cp-end'),msg=document.getElementById('cp-msg');
  var cur=0,caught={},spawnT=null,roundT=null,playing=false;
  function pos(k){return (k*100/7)+'% 0';}
  function setTheme(i){cur=i;var t=T[i];box.style.backgroundImage='url('+U+t.id+'.jpg)';jarImg.style.backgroundPosition=pos(t.img[0]);countEl.textContent=caught[t.id]||0;}
  setTheme(0);
  function add(){
    if(!playing)return;if(layer.childElementCount>11)return;
    var t=T[cur],item=t.only?false:(0.42>Math.random()),W=box.clientWidth,H=box.clientHeight;
    var size=item?W*(0.13+Math.random()*0.05):W*(0.1+Math.random()*0.07);
    size=Math.max(item?70:56,Math.min(size,item?150:130));
    var b=document.createElement('button');b.type='button';b.className='f '+(item?('itm'+(t.flut?' flut':'')):'bub');
    b.setAttribute('aria-label',item?('Catch the '+t.many):'Bubble');
    b.style.width=size+'px';b.style.height=size+'px';b.style.left=(2+Math.random()*(96-size/W*100-2))+'%';
    b.style.animationDuration=(7+Math.random()*3)+'s';b.style.setProperty('--h',H+'px');b.style.setProperty('--dx',(Math.random()*40-20).toFixed(0)+'px');
    var k=t.img[Math.floor(Math.random()*t.img.length)];b.setAttribute('data-k',k);
    var ic=document.createElement('i');if(item)ic.style.backgroundPosition=pos(k);b.appendChild(ic);
    b.addEventListener('pointerdown',function(e){e.preventDefault();hit(b,item,t);});
    b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();hit(b,item,t);}});
    b.addEventListener('animationend',function(e){if(e.target===b)b.remove();});
    layer.appendChild(b);
  }
  function bump(t){caught[t.id]=(caught[t.id]||0)+1;countEl.textContent=caught[t.id];jar.classList.remove('bump');void jar.offsetWidth;jar.classList.add('bump');}
  function hit(b,item,t){
    if(b.getAttribute('data-done'))return;b.setAttribute('data-done','1');
    var r=b.getBoundingClientRect(),q=box.getBoundingClientRect(),x=r.left-q.left+r.width/2,y=r.top-q.top+r.height/2;
    b.remove();
    if(!item){
      for(var n=0;14>n;n++){var d=document.createElement('i');d.className='drop';var a=Math.random()*6.283,dist=r.width*0.3+Math.random()*r.width*0.5,sz=4+Math.random()*8;
        d.style.left=(x-sz/2)+'px';d.style.top=(y-sz/2)+'px';d.style.width=sz+'px';d.style.height=sz+'px';d.style.setProperty('--x',(Math.cos(a)*dist)+'px');d.style.setProperty('--y',(Math.sin(a)*dist)+'px');d.style.setProperty('--r','0deg');
        box.appendChild(d);(function(el){setTimeout(function(){el.remove();},750);})(d);}
      S.say(['pop']);
      if(t.only)bump(t);
      if(V.idle()){if(0.25>Math.random())V.say(['pop-'+(1+Math.floor(Math.random()*3))]);}
      return;
    }
    imalooConfetti(box,x,y);
    var f=document.createElement('div');f.className='flyer';f.style.left=(x-r.width/2)+'px';f.style.top=(y-r.height/2)+'px';f.style.width=r.width+'px';f.style.height=r.height+'px';f.style.backgroundPosition=pos(+b.getAttribute('data-k'));box.appendChild(f);
    var j=jarImg.getBoundingClientRect();
    requestAnimationFrame(function(){requestAnimationFrame(function(){f.style.left=(j.left-q.left)+'px';f.style.top=(j.top-q.top)+'px';f.style.width=j.width+'px';f.style.height=j.height+'px';f.style.opacity='.4';});});
    setTimeout(function(){f.remove();bump(t);},650);
    S.say([t.id]);
    if(V.idle()){if(0.5>Math.random())V.say(['catch-'+t.id]);else if(0.3>Math.random())V.say(['yay-'+(1+Math.floor(Math.random()*4))]);}
  }
  function switchTo(i){
    [].forEach.call(layer.querySelectorAll('.itm'),function(x){x.setAttribute('data-done','1');x.style.transition='opacity .4s';x.style.opacity='0';setTimeout(function(){x.remove();},400);});
    setTheme(i);var t=T[i];V.say(['now-'+t.id]);
    banner.textContent='Now… '+t.many+'!';banner.classList.add('on');setTimeout(function(){banner.classList.remove('on');},2400);
    say.textContent='Ooh! Catch the '+t.many+'!';
    clearTimeout(roundT);roundT=setTimeout(function(){switchTo((cur+1)%T.length);},20000);
  }
  function go(){
    playing=true;end.hidden=true;btns.hidden=false;
    var t=T[cur];say.textContent=t.word+' Collect as many '+t.many+' as you can!';
    V.say(['start-'+t.id]);
    clearInterval(spawnT);spawnT=setInterval(add,750);add();
    clearTimeout(roundT);roundT=setTimeout(function(){switchTo((cur+1)%T.length);},20000);
  }
  function stop(){
    playing=false;clearInterval(spawnT);clearTimeout(roundT);layer.textContent='';btns.hidden=true;
    var parts=T.filter(function(t){return caught[t.id];}).map(function(t){return caught[t.id]+' '+(t.id==='candy'?'sweet treats':t.many);});
    var text='What a great game!';
    if(parts.length){text='You caught '+(parts.length>1?parts.slice(0,-1).join(', ')+' and '+parts[parts.length-1]:parts[0])+'!';}
    msg.textContent=text+' 🎉';end.hidden=false;V.say(['yay-'+(1+Math.floor(Math.random()*4))]);
    var q=box.getBoundingClientRect();imalooConfetti(box,q.width/2,q.height/2);
  }
  document.getElementById('cp-next').addEventListener('click',function(){switchTo((cur+1)%T.length);});
  document.getElementById('cp-stop').addEventListener('click',stop);
  document.getElementById('cp-again').addEventListener('click',function(){caught={};setTheme(Math.floor(Math.random()*T.length));go();});
  start.querySelector('button').addEventListener('click',function(){V.unlock();S.unlock();start.hidden=true;setTheme(Math.floor(Math.random()*T.length));go();});
  document.addEventListener('visibilitychange',function(){if(document.hidden){if(playing)stop();}});
})();

// Fruit Maths: count the fruit, then pick the right number.
(function(){
  var box=document.getElementById('fm');if(!box)return;
  var V=imalooVoice('/wp-content/uploads/2026/11/imaloo-fruit-voice.mp3',""" + json.dumps(fm, separators=(',', ':')) + r""");
  var FRUIT=[['apple','apples'],['banana','bananas'],['grapes','bunches of grapes'],['lemon','lemons'],['orange','oranges'],['pear','pears'],['strawberry','strawberries'],['watermelon','watermelon slices']];
  var YES=['Yes!','Hooray!','Well done!','You got it!','Super counting!','Fantastic!'];
  var rug=document.getElementById('fm-rug'),ans=document.getElementById('fm-ans'),say=document.getElementById('fm-say'),again=document.getElementById('fm-again'),start=document.getElementById('fm-start');
  var n=0,counted=0,f=0,lastF=-1,done=false;
  function round(first){
    done=false;counted=0;n=1+Math.floor(Math.random()*5);
    f=Math.floor(Math.random()*FRUIT.length);if(f===lastF)f=(f+1)%FRUIT.length;lastF=f;
    rug.textContent='';ans.hidden=true;again.hidden=true;
    for(var k=0;n>k;k++){
      var b=document.createElement('button');b.type='button';b.className='fruit';
      b.style.backgroundPosition=(f*100/7)+'% 0';b.setAttribute('aria-label',FRUIT[f][0]);
      b.addEventListener('click',tapFruit);rug.appendChild(b);
    }
    say.textContent='How many '+FRUIT[f][1]+' can you see? Tap each one!';
    V.say(first?['start-count','count-'+FRUIT[f][0]]:['count-'+FRUIT[f][0]]);
  }
  function tapFruit(e){
    var b=e.currentTarget;if(b.classList.contains('counted'))return;
    counted++;b.classList.add('counted');
    var s=document.createElement('span');s.className='num';s.textContent=counted;b.appendChild(s);
    if(counted===n){V.say(['n'+counted,'pick'],function(){});showAnswers();}
    else V.say(['n'+counted]);
  }
  function showAnswers(){
    say.textContent='Now pick the right number!';
    var opts=[n];while(3>opts.length){var o=1+Math.floor(Math.random()*6);if(opts.indexOf(o)===-1)opts.push(o);}
    imalooShuffle(opts);ans.textContent='';
    opts.forEach(function(o){var b=document.createElement('button');b.type='button';b.textContent=o;b.addEventListener('click',function(){pick(b,o);});ans.appendChild(b);});
    ans.hidden=false;
  }
  function pick(b,o){
    if(done)return;
    if(o===n){
      done=true;b.classList.add('yes');var y=Math.floor(Math.random()*6);
      say.textContent=YES[y]+' '+n+'!';V.say(['yes-'+(y+1),'n'+n]);
      var r=b.getBoundingClientRect(),q=box.getBoundingClientRect();imalooConfetti(box,r.left-q.left+r.width/2,r.top-q.top);
      again.hidden=false;
    }else{
      b.classList.remove('no');void b.offsetWidth;b.classList.add('no');
      say.textContent="Let's count again!";
      [].forEach.call(rug.children,function(x){x.classList.remove('counted');x.textContent='';});counted=0;ans.hidden=true;
    }
  }
  again.addEventListener('click',function(){round(false);});
  start.querySelector('button').addEventListener('click',function(){V.unlock();start.hidden=true;round(true);});
})();

// Read & Spell: pick an animal, then tap the letters in order.
(function(){
  var box=document.getElementById('rs');if(!box)return;
  var V=imalooVoice('/wp-content/uploads/2026/11/imaloo-spell-voice.mp3',""" + json.dumps(rs, separators=(',', ':')) + r""");
  var WORDS=[['cat','The cat chased the mouse!'],['dog','The dog dug a big hole.'],['pig','The pig played in the mud.'],['cow','The cow said moo to the moon.'],['sun','The sun is hot and bright.'],['bee','The bee buzzed by the flower.']];
  var EXTRA='abcdegnopstuw';
  var picks=document.getElementById('rs-picks'),say=document.getElementById('rs-say'),toy=document.getElementById('rs-toy'),slots=document.getElementById('rs-slots'),tiles=document.getElementById('rs-tiles'),story=document.getElementById('rs-story'),start=document.getElementById('rs-start');
  var w='',at=0,busy=false;
  WORDS.forEach(function(x,k){
    var b=document.createElement('button');b.type='button';b.className='pick';b.style.backgroundPosition=(k*20)+'% 0';
    b.setAttribute('aria-label','Spell '+x[0].toUpperCase());b.setAttribute('aria-pressed','false');
    b.addEventListener('click',function(){choose(k);});picks.appendChild(b);
  });
  function choose(k){
    w=WORDS[k][0];at=0;busy=false;story.textContent='';
    [].forEach.call(picks.children,function(p,j){p.setAttribute('aria-pressed',j===k?'true':'false');});
    toy.style.backgroundPosition=(k*20)+'% 0';toy.setAttribute('aria-label',w);toy.classList.remove('won');
    slots.textContent='';
    for(var j=0;w.length>j;j++){var s=document.createElement('div');s.className='slot'+(j===0?' next':'');slots.appendChild(s);}
    var letters=w.split('');var spare=EXTRA.replace(new RegExp('['+w+']','g'),'');
    letters.push(spare.charAt(Math.floor(Math.random()*spare.length)));
    imalooShuffle(letters);tiles.textContent='';
    letters.forEach(function(c){var t=document.createElement('button');t.type='button';t.className='tile';t.textContent=c.toUpperCase();t.setAttribute('data-c',c);
      t.addEventListener('pointerdown',function(e){e.preventDefault();tap(t);});t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();tap(t);}});tiles.appendChild(t);});
    say.textContent='Can you spell '+w.toUpperCase()+'? Find the '+w.charAt(0).toUpperCase()+'!';
    V.say(['ask-'+w,'together','find-'+w.charAt(0)]);
    glow();
  }
  function glow(){[].forEach.call(tiles.children,function(t){t.classList.remove('glow');});}
  function tap(t){
    if(busy)return;if(!w)return;if(t.classList.contains('used'))return;
    var c=t.getAttribute('data-c');
    if(c===w.charAt(at)){
      t.classList.add('used');var s=slots.children[at];s.textContent=c.toUpperCase();s.className='slot full';at++;
      if(w.length>at){slots.children[at].className='slot next';say.textContent='Yes! Now find the '+w.charAt(at).toUpperCase()+'!';V.say(['letter-'+c,'find-'+w.charAt(at)]);}
      else{
        busy=true;say.textContent=w.split('').join(', ').toUpperCase()+'. That spells '+w.toUpperCase()+'!';
        toy.classList.add('won');var q=box.getBoundingClientRect(),r=toy.getBoundingClientRect();imalooConfetti(box,r.left-q.left+r.width/2,r.top-q.top+r.height/2);
        [].forEach.call(tiles.children,function(x){x.classList.add('used');});
        var st=WORDS.filter(function(x){return x[0]===w;})[0][1];
        V.say(['letter-'+c,'spelled-'+w,'story-'+w],function(){busy=false;});
        setTimeout(function(){story.textContent='📖 '+st;},2600);
      }
    }else{
      t.classList.remove('no');void t.offsetWidth;t.classList.add('no');
      say.textContent='Oops! Try another letter! Find the '+w.charAt(at).toUpperCase()+'!';
      V.say(['try','find-'+w.charAt(at)]);
      [].forEach.call(tiles.children,function(x){if(x.getAttribute('data-c')===w.charAt(at)){if(!x.classList.contains('used'))x.classList.add('glow');}});
    }
  }
  start.querySelector('button').addEventListener('click',function(){V.unlock();start.hidden=true;choose(Math.floor(Math.random()*WORDS.length));});
})();

// Sing-along: real IMALOO songs with each word lighting up as it is sung.
(function(){
  var box=document.getElementById('sg');if(!box)return;
  var SONGS=""" + json.dumps(songs, separators=(',', ':'), ensure_ascii=False) + r""";
  var list=document.getElementById('sg-list'),lyric=document.getElementById('sg-lyric'),stopBtn=document.getElementById('sg-stop');
  var a=new Audio(),cur=null,line=-1,raf=null,noteT=null;a.preload='none';
  Object.keys(SONGS).forEach(function(id){
    var b=document.createElement('button');b.type='button';b.textContent=SONGS[id][0];b.setAttribute('aria-pressed','false');
    b.addEventListener('click',function(){play(id);});list.appendChild(b);
  });
  function mark(){[].forEach.call(list.children,function(b,k){b.setAttribute('aria-pressed',Object.keys(SONGS)[k]===cur?'true':'false');});}
  function showLine(k){
    var L=SONGS[cur][1].l;line=k;lyric.textContent='';
    var holder=document.createElement('div');
    L[k][1].forEach(function(w){var s=document.createElement('span');s.className='w';s.textContent=w[0];holder.appendChild(s);});
    if(L[k+1]){var nx=document.createElement('span');nx.className='nextline';nx.textContent=L[k+1][1].map(function(w){return w[0];}).join(' ');holder.appendChild(nx);}
    lyric.appendChild(holder);
  }
  function tick(){
    if(!cur)return;
    var t=a.currentTime,L=SONGS[cur][1].l,k=-1;
    for(var j=0;L.length>j;j++){if(t+0.05>=L[j][0])k=j;}
    if(k>=0){
      if(k!==line)showLine(k);
      var words=lyric.querySelectorAll('.w');
      L[k][1].forEach(function(w,n){if(words[n]){if(t+0.05>=w[1])words[n].classList.add('on');}});
    }
    raf=requestAnimationFrame(tick);
  }
  function note(){
    var n=document.createElement('span');n.className='note';n.textContent=['🎵','🎶','⭐','💖','✨'][Math.floor(Math.random()*5)];
    n.style.left=(5+Math.random()*90)+'%';box.appendChild(n);setTimeout(function(){n.remove();},4100);
  }
  function play(id){
    stop();cur=id;mark();a.src='/wp-content/uploads/2026/11/imaloo-song-'+id+'.mp3';a.currentTime=0;
    lyric.textContent='🎤 Get ready to sing!';
    var p=a.play();if(p){if(p.catch){p.catch(function(){});}}
    stopBtn.hidden=false;raf=requestAnimationFrame(tick);noteT=setInterval(note,700);
  }
  function stop(){
    try{a.pause();}catch(e){}cancelAnimationFrame(raf);clearInterval(noteT);
    if(cur){cur=null;line=-1;mark();lyric.textContent='Pick a song and sing along! 🎤';stopBtn.hidden=true;}
  }
  a.addEventListener('ended',function(){stop();lyric.textContent='Hooray! Great singing! 🎉';var q=box.getBoundingClientRect();imalooConfetti(box,q.width/2,q.height/2);});
  stopBtn.addEventListener('click',stop);
})();
""")

# ---------------- BOOKS ----------------
BOOKS_CSS = r"""
.ways{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.way{display:grid;gap:10px;align-content:start}.way .ic{font-size:40px;line-height:1}.way h3{font-size:23px}.way p{color:var(--muted)}
.gallery{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:8px}
.gallery img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:16px;box-shadow:0 8px 20px rgba(139,92,246,.15);transition:transform .25s}
.gallery img:hover{transform:scale(1.06) rotate(-1deg)}
.prints{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.prints h3{font-size:24px;margin-bottom:8px}.prints table{width:100%;border-collapse:collapse}.prints td{padding:8px 0;border-bottom:1px dashed var(--line)}.prints td:last-child{text-align:right;font-family:var(--display);font-weight:700;font-variant-numeric:tabular-nums}
.prints .note{color:var(--muted);font-size:15px;margin-top:10px}
@media (max-width:820px){.ways,.prints{grid-template-columns:1fr}.gallery{grid-template-columns:repeat(2,1fr)}}
"""

BOOKS_HTML = """
<section class="band">
  <span class="floaty" style="left:7%;top:26%" aria-hidden="true">📖</span><span class="floaty" style="right:8%;top:22%;animation-delay:1.2s" aria-hidden="true">🧸</span><span class="floaty" style="left:15%;bottom:24%;animation-delay:2.4s" aria-hidden="true">✨</span><span class="floaty" style="right:15%;bottom:26%;animation-delay:3.2s" aria-hidden="true">🦄</span>
  <h1>📚 Storybooks starring your toys</h1>
  <p>Once upon a time, your child's teddy went on an adventure... IMALOO writes the story, paints every page with your own toys, and reads it aloud.</p>
</section>
""" + STORYBOOK_HTML + """
<section class="sec"><div class="wrap">
  <h2>Three ways to make a book</h2>
  <p class="sub">Every book has a proper beginning, a little adventure and a happy ending.</p>
  <div class="ways">
    <div class="card way"><span class="ic" aria-hidden="true">🗺️</span><h3>A storybook adventure</h3><p>Pick up to four toys, a world and how many pages (4, 6 or 8). IMALOO writes a whole story, then paints every page with your toys in it.</p></div>
    <div class="card way"><span class="ic" aria-hidden="true">🖼️</span><h3>A story for my pictures</h3><p>Already made some pictures? Turn them into one whole story, or a little story for each picture.</p></div>
    <div class="card way"><span class="ic" aria-hidden="true">🔊</span><h3>Read to me</h3><p>A bubbly storyteller reads every page, with fun join-in moments, and turns the pages by herself.</p></div>
  </div>
</div></section>

<section class="sec tint"><div class="wrap">
  <h2>Pages from our sample book</h2>
  <p class="sub">The Big Sparkle Party, starring Teddy, Dolly and Pony.</p>
  <div class="gallery">
    <img src="/wp-content/uploads/2026/11/book-1-fairy.jpg" alt="Teddy, Dolly and Pony in the fairy garden" loading="lazy">
    <img src="/wp-content/uploads/2026/11/book-2-candy.jpg" alt="The friends in Candy Land" loading="lazy">
    <img src="/wp-content/uploads/2026/11/book-3-balloons.jpg" alt="A big bunch of balloons at the carnival" loading="lazy">
    <img src="/wp-content/uploads/2026/11/book-4-sneak.jpg" alt="Getting the playroom ready for the party" loading="lazy">
    <img src="/wp-content/uploads/2026/11/book-5-surprise.jpg" alt="Surprise! The Sparkle Party" loading="lazy">
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Print it and keep it forever</h2>
  <p class="sub">Print at home for free, or order a real printed book or poster, posted to your door.</p>
  <div class="prints">
    <div class="card"><h3>📕 Printed books</h3><table>
      <tr><td>Softcover book</td><td>$34.95</td></tr>
      <tr><td>Hardcover book</td><td>$45.95</td></tr>
      <tr><td>Print at home (A5 or A4)</td><td>Free</td></tr>
    </table><p class="note">Printed books need 8 to 10 pictures, so choose an 8-page adventure.</p></div>
    <div class="card"><h3>🖼️ Posters</h3><table>
      <tr><td>A5 poster</td><td>$34.95</td></tr>
      <tr><td>A4 poster</td><td>$36.95</td></tr>
      <tr><td>A3 poster</td><td>$44.95</td></tr>
    </table><p class="note">Choose a Rainbow, Starry night, Gold or Simple frame.</p></div>
  </div>
  <p class="sub" style="margin-top:20px;margin-bottom:0">Prices in Australian dollars, with delivery and GST included. Printed and posted in Australia only.</p>
</div></section>
""" + TRIAL

# ---------------- FANTASY LANDS ----------------
NAMES = {'aus-beach': 'Aussie Beach', 'aus-bush': 'Aussie Bush', 'cubby': 'Cubby House', 'home': 'Family Home', 'construction': 'Construction Site',
         'ocean': 'Underwater', 'dino-valley': 'Dinosaur Valley', 'moon-base': 'Moon Base', 'ice-cream-shop': 'Ice Cream Shop', 'hot-air-balloons': 'Hot Air Balloons',
         'night-backyard': 'Night Backyard', 'toy-shop': 'Toy Shop', 'theatre-stage': 'Theatre Stage', 'sports-oval': 'Sports Oval', 'wild-west': 'Wild West',
         'water-park': 'Water Park', 'race-track': 'Race Track', 'rock-pools': 'Rock Pools', 'secret-island': 'Secret Island', 'little-town': 'Little Town',
         'fire-station': 'Fire Station', 'mermaid-lagoon': 'Mermaid Lagoon', 'cloud-kingdom': 'Cloud Kingdom', 'christmas-village': 'Christmas Village',
         'cherry-blossom': 'Cherry Blossom Garden', 'birthday-party': 'Birthday Party', 'autumn-woods': 'Autumn Woods', 'desert-oasis': 'Desert Oasis',
         'dragon-valley': 'Dragon Valley', 'fairy-garden': 'Fairy Garden', 'deep-forest': 'Deep Forest', 'candy-land': 'Candy Land', 'pirate-island': 'Pirate Island',
         'rainbow-meadow': 'Rainbow Meadow', 'snow': 'Snowy Land'}
def pretty(s):
    return NAMES.get(s, s.replace('-', ' ').title())

LANDS_CSS = r"""
.lhero{position:relative;color:#fff;text-align:center;overflow:hidden}
.lhero video{width:100%;aspect-ratio:21/9;max-height:62vh;object-fit:cover;display:block}
.lhero .over{position:absolute;inset:0;display:grid;place-items:center;align-content:center;gap:12px;padding:16px;background:linear-gradient(0deg,rgba(80,40,140,.6),rgba(80,40,140,.05) 60%)}
.lhero h1{font-size:clamp(34px,5vw,60px);text-shadow:0 3px 14px rgba(0,0,0,.45)}.lhero p{max-width:32em;font-size:clamp(16px,1.6vw,20px);text-shadow:0 1px 6px rgba(0,0,0,.5)}
.wgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.wgrid figure{margin:0;border-radius:18px;overflow:hidden;position:relative;aspect-ratio:16/9;box-shadow:0 8px 20px rgba(139,92,246,.15)}.wgrid video{width:100%;height:100%;object-fit:cover;display:block}.wgrid figcaption{position:absolute;left:10px;bottom:8px;font-family:var(--display);font-weight:600;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.7)}
.lands{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.land{position:relative;border:0;padding:0;cursor:pointer;border-radius:16px;overflow:hidden;aspect-ratio:16/9;background-image:url(/wp-content/uploads/2026/11/imaloo-lands-sheet.jpg);background-size:600% 900%;box-shadow:0 6px 16px rgba(139,92,246,.15);transition:transform .25s,box-shadow .25s}
.land:hover{transform:translateY(-4px) scale(1.04);box-shadow:0 12px 26px rgba(139,92,246,.3)}
.land span{position:absolute;left:0;right:0;bottom:0;padding:14px 8px 6px;font-family:var(--display);font-weight:600;font-size:15px;color:#fff;text-align:left;background:linear-gradient(0deg,rgba(40,20,70,.75),rgba(40,20,70,0));text-shadow:0 1px 4px rgba(0,0,0,.5)}
.zoom{position:fixed;inset:0;z-index:60;display:grid;place-items:center;padding:16px;background:rgba(40,20,70,.75)}
.zoom .big{position:relative;width:min(960px,100%);aspect-ratio:16/9;border-radius:24px;border:5px solid #fff;background-image:url(/wp-content/uploads/2026/11/imaloo-lands-sheet.jpg);background-size:600% 900%;box-shadow:0 20px 60px rgba(0,0,0,.4);animation:pop .4s ease}
.zoom .big b{position:absolute;left:0;right:0;bottom:0;padding:30px 16px 14px;text-align:center;font-family:var(--display);font-size:clamp(24px,4vw,38px);color:#fff;background:linear-gradient(0deg,rgba(80,40,140,.8),rgba(80,40,140,0))}
.zoom .x{position:absolute;top:18px;right:18px}
@keyframes pop{from{transform:scale(.6) rotate(-4deg);opacity:0}to{transform:none;opacity:1}}
.spark{position:fixed;z-index:61;pointer-events:none;font-size:22px;animation:conf 1.1s ease-out forwards}
@media (max-width:1000px){.lands{grid-template-columns:repeat(4,1fr)}}
@media (max-width:820px){.wgrid{grid-template-columns:repeat(2,1fr)}.lands{grid-template-columns:repeat(2,1fr)}.lhero video{aspect-ratio:4/3}}
"""

def lands_html():
    vids = [('B3Ra78yb/w-castle.mp4', 'w-castle.jpg', 'Castle', 'A fairytale castle'), ('DUb3UnSl/w-space.mp4', 'w-space.jpg', 'Space', 'Outer space with planets'),
            ('D343k1NL/w-aus-beach.mp4', 'w-aus-beach.jpg', 'Aussie Beach', 'A sunny Australian beach'), ('nV0Kpy45/w-dino-valley.mp4', 'w-dino-valley.jpg', 'Dinosaur Valley', 'A friendly dinosaur valley'),
            ('16FIpymC/w-ocean.mp4', 'w-ocean.jpg', 'Underwater', 'Under the sea'), ('zR492uOF/w-snow.mp4', 'w-snow.jpg', 'Snow', 'A snowy land'),
            ('CKm6it07/w-farm.mp4', 'w-farm.jpg', 'Farm', 'A farm with a red barn'), ('ioEMoa1J/w-pirate-island.mp4', 'w-pirate-island.jpg', 'Pirate Island', 'A pirate island')]
    vh = '\n'.join('    <figure><video src="https://videos.files.wordpress.com/%s" poster="/wp-content/uploads/2026/11/%s" autoplay muted loop playsinline preload="metadata" aria-label="%s"></video><figcaption>%s</figcaption></figure>' % (v, p, al, c) for v, p, c, al in vids)
    tiles = []
    for i, s in enumerate(LANDS):
        col, row = i % 6, i // 6
        tiles.append('<button class="land" type="button" style="background-position:%s%% %s%%" data-pos="%s%% %s%%"><span>%s</span></button>' % (
            round(col * 20, 3), round(row * 12.5, 3), round(col * 20, 3), round(row * 12.5, 3), pretty(s)))
    return """
<section class="lhero">
  <video src="https://videos.files.wordpress.com/B3Ra78yb/w-castle.mp4" poster="/wp-content/uploads/2026/11/w-castle.jpg" autoplay muted loop playsinline preload="auto" aria-label="A fairytale castle on a sunny hill"></video>
  <div class="over"><h1>🏰 Fantasy Lands</h1><p>54 bright, warm and magical places for your child's toys to explore. Nothing scary, just sunshine, sparkles and little surprises.</p></div>
</section>

<section class="sec"><div class="wrap">
  <h2>Watch the lands come alive</h2>
  <p class="sub">Every land has gentle movement and little details to spot: waves, butterflies, twinkling stars and more.</p>
  <div class="wgrid">
""" + vh + """
  </div>
</div></section>

<section class="sec tint"><div class="wrap">
  <h2>Explore all 54 lands ✨</h2>
  <p class="sub">Tap a land to see it big. In the app, your child picks one with a big picture button, then their toy wakes up inside it.</p>
  <div class="lands" id="lands">
""" + '\n'.join(tiles) + """
  </div>
</div></section>
<div class="zoom" id="zoom" hidden role="dialog" aria-modal="true" aria-label="Fantasy land"><div class="big" id="zoom-big"><b id="zoom-name"></b></div><button class="btn btn-soft x" type="button" id="zoom-x">✕ Close</button></div>
""" + TRIAL

JS_LANDS = r"""
// Fantasy Lands: tap a land to see it big, with a little burst of sparkles.
(function(){
  var grid=document.getElementById('lands'),zoom=document.getElementById('zoom'),big=document.getElementById('zoom-big'),nm=document.getElementById('zoom-name'),x=document.getElementById('zoom-x');
  if(!grid)return;
  function sparkle(cx,cy){
    for(var k=0;14>k;k++){var s=document.createElement('span');s.className='spark';s.textContent=['✨','⭐','💖','🌟'][k%4];
      var a=Math.random()*6.283,d=50+Math.random()*120;s.style.left=cx+'px';s.style.top=cy+'px';
      s.style.setProperty('--x',(Math.cos(a)*d)+'px');s.style.setProperty('--y',(Math.sin(a)*d)+'px');s.style.setProperty('--r',(Math.random()*360)+'deg');
      document.body.appendChild(s);(function(el){setTimeout(function(){el.remove();},1200);})(s);}
  }
  function close(){zoom.hidden=true;}
  [].forEach.call(grid.querySelectorAll('.land'),function(b){
    b.addEventListener('click',function(){
      big.style.backgroundPosition=b.getAttribute('data-pos');nm.textContent=b.textContent;zoom.hidden=false;x.focus();
      sparkle(window.innerWidth/2,window.innerHeight/2);
    });
  });
  x.addEventListener('click',close);
  zoom.addEventListener('click',function(e){if(e.target===zoom)close();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
})();
"""

# ---------------- PRICES ----------------
PRICES_CSS = r"""
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.plan{background:var(--card);border:2px solid var(--line);border-radius:24px;padding:26px;display:grid;gap:12px;align-content:start;transition:transform .25s}.plan:hover{transform:translateY(-5px)}.plan.pop{border-color:var(--berry);box-shadow:0 10px 30px rgba(255,95,162,.18)}.plan .tag{justify-self:start;background:var(--sun);color:#3B2357;font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:3px 10px}.plan h3{font-size:24px}.plan .em{font-size:40px;line-height:1}.price{font-family:var(--display);font-size:40px;font-weight:700;font-variant-numeric:tabular-nums}.price small{font-size:16px;font-weight:500;color:var(--muted)}.plan ul{margin:0;padding-left:20px;color:var(--muted)}
.incl{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.incl div{background:#fff;border:2px solid var(--line);border-radius:20px;padding:16px;text-align:center}.incl .ic{font-size:32px;display:block}.incl b{font-family:var(--display);font-size:18px}
.extras{display:grid;grid-template-columns:1fr 1fr;gap:20px}.extras h3{font-size:22px;margin-bottom:8px}.extras table{width:100%;border-collapse:collapse}.extras td{padding:8px 0;border-bottom:1px dashed var(--line)}.extras td:last-child{text-align:right;font-family:var(--display);font-weight:700;font-variant-numeric:tabular-nums}
.faq{max-width:800px;margin:0 auto;display:grid;gap:12px}.faq details{background:#fff;border:2px solid var(--line);border-radius:18px;padding:14px 18px}.faq summary{cursor:pointer;font-family:var(--display);font-weight:600;font-size:19px}.faq p{color:var(--muted);margin-top:8px}
@media (max-width:820px){.pgrid,.extras{grid-template-columns:1fr}.incl{grid-template-columns:repeat(2,1fr)}}
"""

PRICES_HTML = """
<section class="band">
  <span class="floaty" style="left:7%;top:28%" aria-hidden="true">⭐</span><span class="floaty" style="right:8%;top:24%;animation-delay:1.4s" aria-hidden="true">🎁</span><span class="floaty" style="left:16%;bottom:24%;animation-delay:2.6s" aria-hidden="true">🧸</span>
  <h1>⭐ Simple family plans</h1>
  <p>Try everything free for 7 days. Prices in Australian dollars, GST included. Cancel any time.</p>
</section>

<section class="sec"><div class="wrap">
  <div class="pgrid">
    <div class="plan"><span class="em" aria-hidden="true">🧸</span><h3>One child</h3><div class="price">$12.99<small> / month</small></div><ul><li>10 movies a month</li><li>60 pictures a month</li><li>Or $129 a year</li></ul></div>
    <div class="plan pop"><span class="tag">Most popular</span><span class="em" aria-hidden="true">🧸🦄</span><h3>Two children</h3><div class="price">$19.99<small> / month</small></div><ul><li>16 movies a month</li><li>100 pictures a month</li><li>Or $199 a year</li></ul></div>
    <div class="plan"><span class="em" aria-hidden="true">🧸🦄🐶</span><h3>Family</h3><div class="price">$24.99<small> / month</small></div><ul><li>Up to 4 children</li><li>25 movies a month</li><li>150 pictures a month</li><li>Or $249 a year</li></ul></div>
  </div>
  <div class="cta" style="padding-bottom:0">
    <a class="btn btn-main" href="https://app.imaloo.com.au">Start your 7-day free trial</a>
    <p>The free trial includes 3 movies and 20 pictures. No card needed.</p>
  </div>
</div></section>

<section class="sec tint"><div class="wrap">
  <h2>Every plan includes</h2>
  <p class="sub">Games, songs, spelling and maths are unlimited. There are never any ads.</p>
  <div class="incl">
    <div><span class="ic" aria-hidden="true">🎉</span><b>Catch Party</b></div>
    <div><span class="ic" aria-hidden="true">🍎</span><b>Fruit Maths</b></div>
    <div><span class="ic" aria-hidden="true">🔤</span><b>Read &amp; Spell</b></div>
    <div><span class="ic" aria-hidden="true">🎵</span><b>12 songs</b></div>
    <div><span class="ic" aria-hidden="true">📚</span><b>Storybooks</b></div>
    <div><span class="ic" aria-hidden="true">🏰</span><b>54 lands</b></div>
    <div><span class="ic" aria-hidden="true">📺</span><b>Watch on TV</b></div>
    <div><span class="ic" aria-hidden="true">🛡️</span><b>Grown-up settings</b></div>
    <div><span class="ic" aria-hidden="true">🔒</span><b>Private to your family</b></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Extras</h2>
  <p class="sub">Only if you want them.</p>
  <div class="extras">
    <div class="card"><h3>🎬 More movies</h3><table><tr><td>10 extra movies</td><td>$6.99</td></tr></table></div>
    <div class="card"><h3>📕 Printed books and posters</h3><table>
      <tr><td>Softcover book</td><td>$34.95</td></tr><tr><td>Hardcover book</td><td>$45.95</td></tr>
      <tr><td>Posters A5 / A4 / A3</td><td>$34.95 / $36.95 / $44.95</td></tr>
    </table><p style="color:var(--muted);font-size:15px;margin-top:8px">Delivery and GST included. Australia only.</p></div>
  </div>
</div></section>

<section class="sec tint"><div class="wrap">
  <h2>Questions</h2>
  <div class="faq" style="margin-top:24px">
    <details><summary>What counts as a movie or a picture?</summary><p>Each short movie or picture IMALOO makes counts once. A long movie counts as two. Each page painted for a storybook adventure counts as one picture. Games, songs, spelling and maths never count.</p></details>
    <details><summary>How do I change or cancel my plan?</summary><p>Open the Parents page in the app (behind a grown-ups question) and choose Manage plan. You can change or cancel any time.</p></details>
    <details><summary>What happens after the free trial?</summary><p>New families get 7 days free with 3 movies and 20 pictures. To keep going, choose a plan on the Parents page.</p></details>
    <details><summary>Is GST included?</summary><p>Yes. All prices are in Australian dollars and include GST, and your receipt shows the GST.</p></details>
  </div>
</div></section>
""" + TRIAL

# ---------------- HOW IT WORKS ----------------
HOW_CSS = r"""
.steps2{display:grid;gap:28px;max-width:960px;margin:0 auto}
.s2{display:grid;grid-template-columns:90px 1fr;gap:22px;align-items:start;background:#fff;border:2px solid var(--line);border-radius:28px;padding:24px;box-shadow:0 8px 24px rgba(139,92,246,.08)}
.s2 .n{width:76px;height:76px;border-radius:24px;display:grid;place-items:center;font-size:38px;color:#fff;transform:rotate(-6deg);transition:transform .3s}
.s2:hover .n{transform:rotate(6deg) scale(1.08)}
.s2:nth-child(4n+1) .n{background:var(--sky)}.s2:nth-child(4n+2) .n{background:var(--grape)}.s2:nth-child(4n+3) .n{background:var(--berry)}.s2:nth-child(4n+4) .n{background:#FFB703}
.s2 h3{font-size:25px;margin-bottom:6px}.s2 p{color:var(--muted)}.s2 ul{margin:8px 0 0;padding-left:20px;color:var(--muted)}
.s2 .shot{display:flex;gap:14px;margin-top:14px;flex-wrap:wrap}.s2 .shot img{width:150px;border-radius:20px;border:5px solid #2b1d40;box-shadow:0 8px 20px rgba(59,35,87,.2)}
.faq{max-width:800px;margin:0 auto;display:grid;gap:12px}.faq details{background:#fff;border:2px solid var(--line);border-radius:18px;padding:14px 18px}.faq summary{cursor:pointer;font-family:var(--display);font-weight:600;font-size:19px}.faq p{color:var(--muted);margin-top:8px}
@media (max-width:820px){.s2{grid-template-columns:1fr;gap:12px}.s2 .n{width:60px;height:60px;font-size:30px}.s2 .shot img{width:120px}}
"""

HOW_HTML = """
<section class="band">
  <span class="floaty" style="left:7%;top:28%" aria-hidden="true">🧸</span><span class="floaty" style="right:8%;top:24%;animation-delay:1.3s" aria-hidden="true">📷</span><span class="floaty" style="left:15%;bottom:24%;animation-delay:2.5s" aria-hidden="true">✨</span><span class="floaty" style="right:15%;bottom:26%;animation-delay:3.4s" aria-hidden="true">📺</span>
  <h1>🧸 How IMALOO works</h1>
  <p>Easy steps for grown-ups. Set it up once, then little ones can play on their own with big picture buttons.</p>
</section>

<section class="sec"><div class="wrap"><div class="steps2">
  <div class="s2"><div class="n" aria-hidden="true">👋</div><div><h3>1. Make your family account</h3><p>Go to <a href="https://app.imaloo.com.au" style="text-decoration:underline">app.imaloo.com.au</a> and start your 7-day free trial. No card needed. Add your children's names and ages, so the games start at the right level.</p></div></div>
  <div class="s2"><div class="n" aria-hidden="true">📷</div><div><h3>2. Add a toy</h3><p>Tap Toys, then take two photos of a real toy: one of the front and one of the back. IMALOO checks every photo to make sure it's a toy. Photos of people, screens and magazines are refused.</p></div></div>
  <div class="s2"><div class="n" aria-hidden="true">✨</div><div><h3>3. Make something magical</h3><p>Tap Make and choose what to make:</p><ul><li><b>Wake-up movie</b>: one toy comes to life and its room turns magical.</li><li><b>Adventure picture</b>: up to four toys together in a world.</li><li><b>Storybook adventure</b>: in Library, then Books.</li></ul>
    <div class="shot"><img src="/wp-content/uploads/2026/11/imaloo-shot-make-choose-toy.jpg" alt="Choosing a toy in the Make screen" loading="lazy"></div></div></div>
  <div class="s2"><div class="n" aria-hidden="true">🏰</div><div><h3>4. Pick a land</h3><p>Choose one of <a href="/fantasy-lands/" style="text-decoration:underline">54 fantasy lands</a>, from a sunny Aussie beach to outer space. Then watch your toy wake up inside it.</p>
    <div class="shot"><img src="/wp-content/uploads/2026/11/imaloo-shot-dolphin-underwater.jpg" alt="A toy dolphin underwater" loading="lazy"><img src="/wp-content/uploads/2026/11/imaloo-shot-cow-farm.jpg" alt="A toy cow on the farm" loading="lazy"></div></div></div>
  <div class="s2"><div class="n" aria-hidden="true">📺</div><div><h3>5. Watch it on the TV</h3><p>Everything you make is kept in the Library. Open a movie and send it to your TV to watch together on the big screen.</p></div></div>
  <div class="s2"><div class="n" aria-hidden="true">🎮</div><div><h3>6. Play and learn</h3><p>Tap Catch Party, Maths, Spell or Songs. Children pick their age (🐣 1-3, 🐥 3-4 or 🦁 4-5) and the games grow with them. <a href="/games/" style="text-decoration:underline">Try the games here</a>.</p></div></div>
  <div class="s2"><div class="n" aria-hidden="true">👪</div><div><h3>7. The Parents page</h3><p>Behind a grown-ups question, so little fingers can't get in. Here you can:</p><ul><li>See your plan and how many movies and pictures are left</li><li>Choose who can add toys, make movies or delete things</li><li>Set a daily play time</li><li>Change or cancel your plan, or delete your account</li></ul></div></div>
</div></div></section>

<section class="sec tint"><div class="wrap">
  <h2>Questions</h2>
  <div class="faq" style="margin-top:24px">
    <details><summary>What age is IMALOO for?</summary><p>IMALOO is made for children aged about 1 to 5, with a grown-up setting things up. The games have three age levels.</p></details>
    <details><summary>Can more than one child use it?</summary><p>Yes. The Two children and Family plans let each child have their own name and age. Tap "Who's playing?" to switch.</p></details>
    <details><summary>Which devices does it work on?</summary><p>IMALOO works in the web browser on phones, tablets and computers. Apps for the App Store and Google Play are coming soon.</p></details>
    <details><summary>I need help</summary><p>Email us at <a href="mailto:support@imaloo.com.au" style="text-decoration:underline">support@imaloo.com.au</a> and we'll help.</p></details>
  </div>
</div></section>
""" + TRIAL

# ---------------- SAFETY ----------------
SAFE_CSS = r"""
.promise{max-width:860px;margin:0 auto;background:linear-gradient(135deg,#4FB8FF,#8B5CF6);color:#fff;border-radius:30px;padding:clamp(24px,4vw,44px);box-shadow:0 18px 50px rgba(79,184,255,.25)}
.promise blockquote{margin:0 0 14px;font-family:var(--display);font-size:clamp(24px,3.4vw,34px);line-height:1.25}.promise p{margin-top:12px}
.keeps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.keep{display:grid;gap:8px;align-content:start}.keep .ic{font-size:38px;line-height:1}.keep h3{font-size:21px}.keep p{color:var(--muted)}
.links{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:28px}
@media (max-width:820px){.keeps{grid-template-columns:1fr}}
"""

SAFE_HTML = """
<section class="band">
  <span class="floaty" style="left:8%;top:28%" aria-hidden="true">🛡️</span><span class="floaty" style="right:8%;top:24%;animation-delay:1.5s" aria-hidden="true">💖</span><span class="floaty" style="left:16%;bottom:24%;animation-delay:2.8s" aria-hidden="true">🧸</span>
  <h1>🛡️ Safe, private and kind</h1>
  <p>IMALOO is made for little children, so safety is built into every part of it.</p>
</section>

<section class="sec"><div class="wrap">
  <div class="promise">
    <blockquote>Imaloo — where toys come to life and childhood stays innocent.</blockquote>
    <p>Imaloo is designed for children to enjoy imaginative, age-appropriate adventures with their favourite toys. Our content rules strictly prohibit pornography, nudity, sexual content, violence, gore, and abusive or disturbing scenes.</p>
    <p>Only photographs of toys are permitted. Photos of real people, magazine pictures, screenshots, and other non-toy images are not allowed. Attempts to bring these images to life or create sexual, violent, or harmful content are prohibited.</p>
    <p>Our commitment is to keep Imaloo a place for playful storytelling, creativity, and childhood wonder.</p>
  </div>
</div></section>

<section class="sec tint"><div class="wrap">
  <h2>How we keep children safe</h2>
  <p class="sub">Nothing scary, no weapons, and toys only ever share hugs and high-fives.</p>
  <div class="keeps">
    <div class="card keep"><span class="ic" aria-hidden="true">🧸</span><h3>Toy photos only</h3><p>Every photo is checked before it is saved. Photos of people, screens and magazines are refused and never kept.</p></div>
    <div class="card keep"><span class="ic" aria-hidden="true">🔍</span><h3>Everything is checked</h3><p>Every picture and movie is checked again before your child sees it. If something isn't right, it's thrown away.</p></div>
    <div class="card keep"><span class="ic" aria-hidden="true">⌨️</span><h3>Children never type</h3><p>Little ones choose with picture buttons, so they can't type anything into IMALOO.</p></div>
    <div class="card keep"><span class="ic" aria-hidden="true">🔒</span><h3>Private to your family</h3><p>Nobody else can see your family's toys, photos, pictures or movies.</p></div>
    <div class="card keep"><span class="ic" aria-hidden="true">🚫</span><h3>No ads, ever</h3><p>IMALOO never shows ads to children.</p></div>
    <div class="card keep"><span class="ic" aria-hidden="true">👪</span><h3>Grown-ups in charge</h3><p>Choose who can add toys, make movies or delete things, set a daily play time, and delete your account whenever you like.</p></div>
  </div>
  <div class="links">
    <a class="btn btn-soft" style="border:2px solid var(--line)" href="https://app.imaloo.com.au/safety">Read our full Safety Promise</a>
    <a class="btn btn-soft" style="border:2px solid var(--line)" href="https://app.imaloo.com.au/privacy">Privacy policy</a>
  </div>
  <p class="sub" style="margin-top:20px;margin-bottom:0">Questions about safety or privacy? Email <a href="mailto:support@imaloo.com.au" style="text-decoration:underline">support@imaloo.com.au</a>.</p>
</div></section>
""" + TRIAL

def page(cur, css, body, js):
    html = FONTS + '\n<style>' + CSS + css + '</style>\n<div class="imaloo-page">\n' + nav(cur) + body + FOOTER + '</div>\n<script>\n' + RULE + js + JS_SPRINKLES + '</script>'
    # Safety check for the WordPress script rule
    for m in re.finditer(r'<script>(.*?)</script>', html, re.S):
        sc = m.group(1)
        if '&&' in sc: sys.exit('&& found in script for ' + cur)
        bad = re.findall(r'.{0,30}<[A-Za-z/!].{0,30}', sc)
        if bad: sys.exit('< before letter in script for %s: %r' % (cur, bad[:3]))
    return '<!-- wp:html -->\n' + html + '\n<!-- /wp:html -->'

PAGES = {
    'home': page('/', HOME_CSS + STORYBOOK_CSS, HOME_HTML, JS_TEDDY + JS_STORYBOOK),
    'games': page('/games/', GAMES_CSS, games_html(), JS_CONFETTI + games_js()),
    'books': page('/books/', STORYBOOK_CSS + BOOKS_CSS, BOOKS_HTML, JS_STORYBOOK),
    'fantasy-lands': page('/fantasy-lands/', LANDS_CSS, lands_html(), JS_LANDS),
    'prices': page('/prices/', PRICES_CSS, PRICES_HTML, ''),
    'how-it-works': page('/how-it-works/', HOW_CSS, HOW_HTML, ''),
    'safety': page('/safety/', SAFE_CSS, SAFE_HTML, ''),
}
os.makedirs('/tmp/claude-0/site/out', exist_ok=True)
for k, v in PAGES.items():
    open('/tmp/claude-0/site/out/%s.html' % k, 'w').write(v)
    print(k, len(v))
