# -*- coding: utf-8 -*-
"""global-i18n 언어팩 패치버전 VER1.0 — 이 페이지용 도구 구현.
명령: roundtrip | extract | pending L | check L FILE | merge L | stats | cost
"""
import json, re, sys, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '02_models.html')
WORK = os.path.join(HERE, 'work')
HANGUL = re.compile(r'[가-힣ㄱ-ㆎ]')
INLINE = {'a','b','i','em','strong','sup','sub','code','small','br','span','u','s','mark','kbd'}
ATTRS = ('aria-label','alt','title','placeholder')
META_NAMES = ('description','citation_title','dc.title','dc.source')
CFG = {'layout':'suffix','page':'02_models','hintMaxLen':20,'bundleChars':14000,
       'langs':['en','zh','ja','ru','uz','vi'],
       'models':{'en':'haiku','zh':'haiku','ja':'haiku','ru':'sonnet','uz':'sonnet','vi':'sonnet'}}

def load(): return open(SRC, encoding='utf-8').read()

# ---------- 문서 영역 나누기 ----------
def regions(doc):
    """[(kind, start, end)] kind: html | js | data:<id> | style | rawscript"""
    out=[]; pos=0
    for m in re.finditer(r'<(script|style)\b([^>]*)>(.*?)</\1>', doc, re.S):
        out.append(('html',pos,m.start(3)))
        tag, attrs = m.group(1), m.group(2)
        if tag=='style': kind='style'
        else:
            idm=re.search(r'id="([^"]+)"', attrs)
            kind='data:'+idm.group(1) if idm else 'js'
        out.append((kind,m.start(3),m.end(3))); pos=m.end(3)
    out.append(('html',pos,len(doc)))
    return out

# ---------- HTML ----------
TAGRE = re.compile(r'<!--.*?-->|<[^>]+>', re.S)
def tagname(t):
    m=re.match(r'</?\s*([a-zA-Z0-9]+)', t); return m.group(1).lower() if m else ''

def html_units(doc, s, e, out):
    seg = doc[s:e]
    toks=[]; p=0
    for m in TAGRE.finditer(seg):
        if m.start()>p: toks.append(('t',s+p,s+m.start()))
        toks.append(('g',s+m.start(),s+m.end())); p=m.end()
    if p<len(seg): toks.append(('t',s+p,e))
    # 속성
    in_title=False
    for k,a,b in toks:
        if k!='g': continue
        t=doc[a:b]
        if t.startswith('<!--'): continue
        nm=tagname(t)
        if nm=='meta':
            mm=re.search(r'name="([^"]+)"',t); cm=re.search(r'content="([^"]*)"',t)
            if mm and cm and mm.group(1) in META_NAMES and HANGUL.search(cm.group(1)):
                out.append({'kind':'attr','start':a+cm.start(1),'end':a+cm.end(1),'text':cm.group(1),'ctx':'meta'})
            continue
        for at in ATTRS:
            for am in re.finditer(r'\s'+re.escape(at)+r'="([^"]*)"', t):
                if HANGUL.search(am.group(1)):
                    out.append({'kind':'attr','start':a+am.start(1),'end':a+am.end(1),'text':am.group(1),'ctx':at})
    # 글 덩어리(run): 글 + 인라인 태그
    i=0
    while i<len(toks):
        k,a,b=toks[i]
        if k=='g' and (doc[a:b].startswith('<!--') or tagname(doc[a:b]) not in INLINE):
            i+=1; continue
        j=i
        while j<len(toks):
            k2,a2,b2=toks[j]
            if k2=='g' and (doc[a2:b2].startswith('<!--') or tagname(doc[a2:b2]) not in INLINE): break
            j+=1
        ra,rb=toks[i][1],toks[j-1][2]
        run=doc[ra:rb]
        if HANGUL.search(re.sub(r'<[^>]+>','',run)):
            l=len(run)-len(run.lstrip()); r=len(run.rstrip())
            # 바깥쪽 태그 중 닫히지 않은 짝 정리: 앞쪽 여는 태그만 / 뒤쪽 닫는 태그만 있는 경우는 그대로 둔다
            out.append({'kind':'html','start':ra+l,'end':ra+r,'text':run[l:r],'ctx':''})
        i=j

# ---------- JS ----------
def js_units(doc, s, e, out):
    import subprocess
    r=subprocess.run(['node',os.path.join(HERE,'jslits.js')],input=doc[s:e].encode(),capture_output=True,check=True)
    for o in json.loads(r.stdout):
        o['start']+=s; o['end']+=s
        if o['kind']=='tpl':
            # 원문 표현식 위치를 그대로 보존: 원문 조각 = 템플릿 내부 전체
            o['raw']=doc[o['start']:o['end']]
        out.append(o)

# ---------- 데이터 블록 (시리즈 2) ----------
def data_units(doc, kind, s, e, out):
    if kind=='data:kg-raw':
        kg=json.loads(doc[s:e].replace('<\\/','</'))
        for n in kg['nodes']:
            if n['type'] in ('QuizItem',): continue
            out.append({'kind':'kg','node':n['id'],'field':'label','text':n['label']['ko'],'ctx':'kg-label'})
            if 'definition' in n: out.append({'kind':'kg','node':n['id'],'field':'definition','text':n['definition']['ko'],'ctx':'kg-def'})
    elif kind=='data:page-meta':
        m=json.loads(doc[s:e].replace('<\\/','</'))
        for f in ('title','series','suggestedCitation','educationalLevel'):
            out.append({'kind':'meta','field':f,'text':m[f],'ctx':'page-meta'})

def extract(doc=None):
    doc=doc or load(); occ=[]
    for kind,s,e in regions(doc):
        if kind=='html': html_units(doc,s,e,occ)
        elif kind=='js': js_units(doc,s,e,occ)
        elif kind.startswith('data:'): data_units(doc,kind,s,e,occ)

    for kind,s,e in regions(doc):
        if kind=='style':
            for m in re.finditer(r'content:"([^"]*)"',doc[s:e]):
                if HANGUL.search(m.group(1)):
                    occ.append({'kind':'js','q':'"','start':s+m.start(1),'end':s+m.end(1),'text':m.group(1),'ctx':'css-content','exprs':[]})
    units={}; order=[]
    for o in occ:
        key=o['text']+'␟'+o['ctx']
        if key not in units:
            units[key]={'id':'u%04d'%(len(order)+1),'text':o['text'],'ctx':o['ctx']}; order.append(key)
        o['id']=units[key]['id']
    # 짧은 단위에만 hint (패치 2)
    for o in occ:
        u=units[o['text']+'␟'+o['ctx']]
        if 'hint' in u or 'start' not in o: continue
        if len(o['text'])<CFG['hintMaxLen'] or o['text']!=o['text'].strip():
            u['hint']=doc[max(0,o['start']-40):o['start']]+'⟦…⟧'+doc[o['end']:o['end']+40]
    return doc,occ,[units[k] for k in order]

# ---------- 번역 메모리 ----------
def tm_path(L): return os.path.join(WORK,L,'tm.json')
def tm_load(L):
    p=tm_path(L); return json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {}
def tm_key(u): return hashlib.sha1((u['text']+'␟'+u['ctx']).encode()).hexdigest()[:16]

GLOSS=json.load(open(os.path.join(HERE,'glossary.json'),encoding='utf-8'))
def gloss_for(L, text):
    return {k:v[L] for k,v in GLOSS.items() if k in text and L in v}

def pending(L, retry_ids=None, name=None):
    doc,occ,units=extract(); tm=tm_load(L)
    todo=[u for u in units if tm_key(u) not in tm and (retry_ids is None or u['id'] in retry_ids)]
    os.makedirs(os.path.join(WORK,L),exist_ok=True)
    bundles=[]; cur=[]; size=0
    for u in todo:
        if cur and size+len(u['text'])>CFG['bundleChars']: bundles.append(cur); cur=[]; size=0
        cur.append(u); size+=len(u['text'])
    if cur: bundles.append(cur)
    names=[]
    for bi,b in enumerate(bundles,1):
        allt=''.join(u['text'] for u in b)
        payload={'lang':L,'bundle':name or '%s_%03d'%(L,bi),
                 'glossary':gloss_for(L,allt),
                 'units':{u['id']:u['text'] for u in b},
                 'hints':{u['id']:u['hint'] for u in b if 'hint' in u},
                 'context':{u['id']:u['ctx'] for u in b if u['ctx']}}
        fn=os.path.join(WORK,L,payload['bundle']+'.json')
        json.dump(payload,open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
        names.append((fn,len(b),len(allt)))
    return names

# ---------- 검사 ----------
TAGS=re.compile(r'<[^>]+>')
NUM=re.compile(r'\d+(?:[.,]\d+)*')
def norm_tags(t):
    return sorted(HANGUL.sub('*',re.sub(r'="[^"]*[가-힣][^"]*"','="*"',x)) for x in TAGS.findall(t))
def nums_src(t):
    t=re.sub(r'\{\d+\}','',TAGS.sub(' ',t)); out=[]
    for m in NUM.finditer(t):
        v=m.group(0); after=t[m.end():m.end()+2]
        if after[:1] in ('억','차','등','위') or after.startswith('번째'): continue
        if t[max(0,m.start()-3):m.start()].endswith('분의 '): continue
        n=v.replace(',','')
        if after[:1]=='만':
            try: out.append({n, str(int(float(n)*10000)), str(int(float(n)*10))}); continue
            except: pass
        if after[:1]=='천':
            try: out.append({n, str(int(float(n)*1000))}); continue
            except: pass
        out.append({n})
    return out
def nums_tgt(t):
    t=re.sub(r'\{\d+\}','',TAGS.sub(' ',t))
    t=re.sub(r'(?<=\d)[    ](?=\d{3}\b)','',t)
    return {m.group(0).replace(',','') for m in NUM.finditer(t)}
WORDNUM={'0':['zero','零','ноль','нул','nol','không'],'16':['sixteenth','十六','шестнадцат','oʻn olti','mười sáu','16分の1'],'1':['one','一','một','bir','один'],'2':['two','二','hai','ikki','два'],'3':['three','三','ba','uch','три'],'4':['four','四','bốn','tört','четыр'],'5':['five','五','năm','besh','пят'],'8':['eight','八','tám','sakkiz','восем']}
def check_unit(L,src,tgt):
    errs=[]
    if not isinstance(tgt,str) or not tgt.strip(): return ['빈 번역']
    if HANGUL.search(tgt): errs.append('한글 남음')
    if sorted(re.findall(r'\{\d+\}',src))!=sorted(re.findall(r'\{\d+\}',tgt)): errs.append('자리표시')
    if norm_tags(src)!=norm_tags(tgt): errs.append('태그')
    if sorted(re.findall(r'&[a-z#0-9]+;',src))!=sorted(re.findall(r'&[a-z#0-9]+;',tgt)): errs.append('엔티티')
    if L not in ('zh','ja'):
        if (src[:1]==' ')!=(tgt[:1]==' ') or (src[-1:]==' ')!=(tgt[-1:]==' '): errs.append('앞뒤 공백')
    tn=nums_tgt(tgt); low=tgt.lower()
    for alts in nums_src(src):
        if not (alts & tn) and not any(w in low for a in alts for w in WORDNUM.get(a,[])):
            errs.append('숫자 '+'/'.join(sorted(alts))); break
    return errs

def check(L, fn):
    doc,occ,units=extract(); byid={u['id']:u for u in units}
    raw=open(fn,encoding='utf-8').read().strip()
    raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw)
    try: out=json.loads(raw)
    except Exception:
        out={}
        for m in re.finditer(r'"(u\d{4})"\s*:\s*("(?:[^"\\]|\\.)*")',raw):
            try: out[m.group(1)]=json.loads(m.group(2))
            except Exception: pass
    bundle=json.load(open(fn.replace('.out.json','.json'),encoding='utf-8'))
    ids=list(bundle['units'].keys())
    tm=tm_load(L); ok=0; fails={}
    for i in ids:
        u=byid[i]
        if i not in out: fails[i]=['빠짐']; continue
        e=check_unit(L,u['text'],out[i])
        if e: fails[i]=e
        else: tm[tm_key(u)]=out[i]; ok+=1
    json.dump(tm,open(tm_path(L),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    return ok,len(ids),fails

# ---------- 조립 ----------
FONTS={'zh':('Noto+Sans+SC','"Noto Sans SC","PingFang SC","Microsoft YaHei"'),
       'ja':('Noto+Sans+JP','"Noto Sans JP","Hiragino Sans","Yu Gothic"'),
       'ru':('IBM+Plex+Sans','"IBM Plex Sans"'),'uz':('IBM+Plex+Sans','"IBM Plex Sans"'),
       'vi':('IBM+Plex+Sans','"IBM Plex Sans"'),'en':('IBM+Plex+Sans','"IBM Plex Sans"')}
def esc_js(t,q):
    t=t.replace('\r','').replace('\n','\\n')
    return re.sub(r'(?<!\\)'+re.escape(q),'\\'+q,t)
def esc_tpl(t):
    t=re.sub(r'(?<!\\)`','\\`',t); return t.replace('${','\\${')
def esc_attr(t): return t.replace('"','&quot;')

def hreflang_block():
    p=CFG['page']; L=['<link rel="alternate" hreflang="ko" href="%s.html">'%p]
    L+=['<link rel="alternate" hreflang="%s" href="%s.%s.html">'%(l,p,l) for l in CFG['langs']]
    return '\n'.join(L)+'\n'

def merge(L, doc=None, allow_missing=False):
    doc,occ,units=extract(doc); tm=tm_load(L); miss=[]
    def tr(o):
        u={'text':o['text'],'ctx':o['ctx']}; k=tm_key(u)
        if k not in tm: miss.append(o['id']); return None
        return tm[k]
    reps=[]
    datas={}
    for o in occ:
        t=tr(o)
        if t is None: continue
        if o['kind'] in ('html',): reps.append((o['start'],o['end'],t))
        elif o['kind']=='attr': reps.append((o['start'],o['end'],esc_attr(t)))
        elif o['kind']=='js': reps.append((o['start'],o['end'],esc_js(t,o['q'])))
        elif o['kind']=='tpl':
            tt=esc_tpl(t)
            for n,ex in enumerate(o['exprs']): tt=tt.replace('{%d}'%n,ex)
            reps.append((o['start'],o['end'],tt))
        else: datas.setdefault(o['kind'],[]).append((o,t))
    # 데이터 블록
    for kind,s,e in regions(doc):
        if kind=='data:kg-raw':
            kg=json.loads(doc[s:e].replace('<\\/','</')); by={n['id']:n for n in kg['nodes']}
            for o,t in datas.get('kg',[]):
                n=by[o['node']]
                if o['field']=='label':
                    if L!='en': n['label'][L]=t
                else: n['definition'][L]=t
            reps.append((s,e,json.dumps(kg,ensure_ascii=False).replace('</','<\\/')))
        elif kind=='data:page-meta':
            m=json.loads(doc[s:e].replace('<\\/','</'))
            for o,t in datas.get('meta',[]): m[o['field']]=t
            m['language']=[L]; m['translatedFrom']='ko'
            for c in m['creator']: c['name']='Ahn Sangsun'; c['affiliation']='M-Robo Inc.'
            reps.append((s,e,json.dumps(m,ensure_ascii=False).replace('</','<\\/')))
    reps.sort(key=lambda x:x[0])
    out=[]; p=0
    for a,b,t in reps:
        assert a>=p, ('겹침',a,p)
        out.append(doc[p:a]); out.append(t); p=b
    out.append(doc[p:]); html=''.join(out)
    # 페이지 단위 바꾸기 (postReplace)
    html=html.replace('<html lang="ko">','<html lang="%s">'%L,1)
    html=html.replace('<meta name="page-lang" content="ko">','<meta name="page-lang" content="%s">'%L,1)
    html=html.replace('content="안상선"','content="Ahn Sangsun"')
    html=html.replace("var AUTHOR='안상선';","var AUTHOR='Ahn Sangsun';") if "var AUTHOR='안상선';" in html else html
    fam,stack=FONTS[L]
    html=html.replace('family=IBM+Plex+Sans+KR:wght@400;500;700','family=%s:wght@400;500;700'%fam,1)
    html=html.replace('--font:"IBM Plex Sans KR",','--font:%s,"IBM Plex Sans KR",'%stack,1)
    if L in ('zh','ja'):
        html=html.replace('</style>','h1,h2,h3,h4,p,li,td,th{word-break:normal;line-break:strict}\n</style>',1)
        html=html.replace("o.lesson+'. '+who","o.lesson+'。'+who")
    if L=='en':
        pass
    return html, sorted(set(miss))

def add_hreflang(html):
    if 'hreflang=' in html: return html
    return html.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', hreflang_block()+'<link rel="preconnect" href="https://fonts.googleapis.com">',1)

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='roundtrip':
        doc,occ,units=extract()
        # 번역 = 원문으로 끼워서 같은지
        reps=sorted([(o['start'],o['end'],o['text'] if o['kind']!='tpl' else o['text']) for o in occ if 'start' in o])
        out=[];p=0
        for a,b,t in reps:
            if '{0}' in t:
                o=[x for x in occ if x.get('start')==a][0]
                for n,ex in enumerate(o['exprs']): t=t.replace('{%d}'%n,ex)
            out.append(doc[p:a]); out.append(t); p=b
        out.append(doc[p:]); print('roundtrip 일치:', ''.join(out)==doc, '· 출현', len(occ), '· 단위', len(units))
    elif cmd=='stats':
        doc,occ,units=extract(); from collections import Counter
        c=Counter(o['kind'] for o in occ); print(c, '단위', len(units), '글자', sum(len(u['text']) for u in units), 'hint', sum(1 for u in units if 'hint' in u))
    elif cmd=='pending':
        for fn,n,ch in pending(sys.argv[2]): print(fn,n,'단위',ch,'자')
    elif cmd=='check':
        ok,tot,f=check(sys.argv[2],sys.argv[3]); print('통과',ok,'/',tot); [print(' ',k,v) for k,v in f.items()]
