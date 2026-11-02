import sys, os, json, glob, re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import i18n
DIST=os.path.join(i18n.HERE,'..','dist'); os.makedirs(DIST,exist_ok=True)
mode=sys.argv[1] if len(sys.argv)>1 else 'check'
langs=sys.argv[2:] or i18n.CFG['langs']
rep={}
if mode=='check':
    for L in langs:
        outs=sorted(glob.glob(os.path.join(i18n.WORK,L,'*.out.json')))
        tot_ok=tot=0; fails={}
        for fn in outs:
            ok,n,f=i18n.check(L,fn); tot_ok+=ok; tot+=n; fails.update(f)
        rep[L]={'pass':tot_ok,'total':tot,'fail':fails}
        print(L,'통과',tot_ok,'/',tot, '실패',len(fails))
        for k,v in list(fails.items())[:40]: print('   ',k,v)
    json.dump(rep,open(os.path.join(i18n.WORK,'check_report.json'),'w'),ensure_ascii=False,indent=1)
elif mode=='retry':
    # 실패 id만 모아 언어별 retry 묶음
    rep=json.load(open(os.path.join(i18n.WORK,'check_report.json')))
    for L in langs:
        ids=set(rep.get(L,{}).get('fail',{}).keys())
        if ids:
            for fn,n,ch in i18n.pending(L,retry_ids=ids,name=L+'_r1'): print(fn,n,ch)
elif mode=='merge':
    src=i18n.load()
    open(os.path.join(DIST,'02_models.html'),'w').write(i18n.add_hreflang(src))
    for L in langs:
        html,miss=i18n.merge(L)
        html=i18n.add_hreflang(html)
        open(os.path.join(DIST,'02_models.%s.html'%L),'w').write(html)
        print(L,'번역 없음',len(miss),miss[:10],'· 크기 %.0f KB'%(len(html.encode())/1024))
