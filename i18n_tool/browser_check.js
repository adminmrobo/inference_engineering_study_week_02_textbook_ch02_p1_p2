const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const files=process.argv.slice(2);const res={};
for(const f of files){const L=(f.match(/\.([a-z]{2})\.html$/)||[,'ko'])[1];res[L]={};
 for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:900}});const errs=[];
  p.on('pageerror',e=>errs.push('PE '+e.message));p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|fonts/.test(m.text()))errs.push(m.text())});
  await p.goto('file://'+f);await p.waitForTimeout(1200);
  const r=await p.evaluate(()=>{const H=/[가-힣]/g;const clone=document.body.cloneNode(true);clone.querySelectorAll('select,script,style').forEach(e=>e.remove());
    const t=clone.textContent;const m=t.match(H)||[];let ctx=[];let i=0;const re=/[가-힣]+/g;let mm;while((mm=re.exec(t))&&ctx.length<8)ctx.push(t.slice(Math.max(0,mm.index-20),mm.index+20).replace(/\s+/g,' '));
    const attrs=[...document.querySelectorAll('[aria-label],[alt],[title],[placeholder]')].filter(e=>/[가-힣]/.test((e.getAttribute('aria-label')||'')+(e.getAttribute('alt')||'')+(e.getAttribute('placeholder')||''))&&e.tagName!=='SELECT').length;
    return {sw:document.documentElement.scrollWidth,hangul:m.length,ctx,attrs,quiz:document.querySelectorAll('.qitem').length,kg:document.querySelectorAll('.kgitem').length,lang:document.documentElement.lang,title:document.title}});
  if(w===1280){await p.click('#duelbox .reveal');await p.waitForTimeout(500);r.verdict=await p.$eval('#duelbox .verdict p',e=>e.textContent);r.asst=await p.$eval('#duelbox .asst p',e=>e.textContent);
    await p.$eval('#kg',e=>e.scrollIntoView());await p.waitForTimeout(300);await p.screenshot({path:'/home/claude/build/i18n/shots/'+L+'_kg.png'});
    await p.$eval('#lv4',e=>e.scrollIntoView());await p.waitForTimeout(600);await p.screenshot({path:'/home/claude/build/i18n/shots/'+L+'_lv4.png'});
    const H=/[가-힣]/g; const t2=await p.evaluate(()=>document.body.innerText); r.hangulAfter=(t2.match(H)||[]).length;}
  r.errs=errs;res[L][w]=r;await p.close();}}
console.log(JSON.stringify(res,null,1));await b.close();})();
