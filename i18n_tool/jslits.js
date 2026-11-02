// stdin: JS source → stdout: JSON [{kind:'js'|'tpl', start, end, q, text, exprs[], ctx}]  (offsets relative to source)
const acorn=require('acorn'); const src=require('fs').readFileSync(0,'utf8');
const H=/[가-힣]/; const out=[]; const comments=[];
const ast=acorn.parse(src,{ecmaVersion:2022,onComment:(b,t,s,e)=>{if(b&&t.startsWith('i18n:'))comments.push({ctx:t.slice(5),end:e});}});
function ctxFor(start){const c=comments.filter(c=>c.end<=start && /^\s*$/.test(src.slice(c.end,start))); return c.length?c[c.length-1].ctx:'';}
(function walk(n){ if(!n||typeof n.type!=='string')return;
  if(n.type==='Literal'&&typeof n.value==='string'&&H.test(n.value)){const ctx=ctxFor(n.start); if(ctx!=='skip') out.push({kind:'js',start:n.start+1,end:n.end-1,q:src[n.start],text:src.slice(n.start+1,n.end-1),exprs:[],ctx});}
  if(n.type==='TemplateLiteral'){let text='',exprs=[];n.quasis.forEach((q,i)=>{text+=src.slice(q.start,q.end);if(i<n.expressions.length){const ex=n.expressions[i];exprs.push('${'+src.slice(ex.start,ex.end)+'}');text+='{'+i+'}';}});
    if(H.test(text.replace(/\{\d+\}/g,''))){const ctx=ctxFor(n.start); if(ctx!=='skip') out.push({kind:'tpl',start:n.start+1,end:n.end-1,text,exprs,ctx,tplExact:true});}}
  for(const k in n){const v=n[k]; if(Array.isArray(v))v.forEach(walk); else if(v&&typeof v.type==='string')walk(v);} })(ast);
process.stdout.write(JSON.stringify(out));
