# -*- coding: utf-8 -*-
"""시리즈 목차 index.html 만들기 (7개 언어, 한 파일). 제목·질문은 각 언어판 page-meta·본문에서 가져온다."""
import re, json, base64, html
LANGS=[('ko','한국어'),('en','English'),('zh','中文'),('ja','日本語'),('ru','Русский'),('uz','Oʻzbekcha'),('vi','Tiếng Việt')]
def f(L): return 'dist/02_models.html' if L=='ko' else 'dist/02_models.%s.html'%L
P={}
for L,_ in LANGS:
    s=open(f(L)).read()
    m=json.loads(re.search(r'id="page-meta">(.*?)</script>',s,re.S).group(1).replace('<\\/','</'))
    q=re.sub(r'<[^>]+>','',re.search(r'class="question">(.*?)</p>',s,re.S).group(1))
    P[L]={'title':m['title'],'series':m['series'],'q':q}
UI={
'ko':{'tag':'『Inference Engineering』(Philip Kiely, 2026)의 주제를 주차마다 한 편씩 다루는 인터랙티브 해설입니다. 각 주차는 따로 읽어도 됩니다. 박사·조수·초파리 연구원·주판봇이 실험과 대결로 안내합니다.','week':'{n}주차','read':'읽기 →','soon':'준비 중','plan':'예정','w1':'1주차 해설은 준비 중입니다.','w2b':'이어지는 내용: 2.3 이미지 생성 추론 · 2.4 추론 병목 계산 · 2.5 어텐션 최적화','steps':'다섯 칸: 행렬곱 · 활성화 함수 · 토큰과 샘플링 · 어텐션과 KV 캐시 · 전문가 혼합(MoE)','by':'글 · 안상선 ((주)M-Robo 대표)','src':'자료: Philip Kiely, 『Inference Engineering』, Baseten Books, 2026','lang':'언어','toc':'차례','note':'각 페이지 위쪽의 언어 선택으로 7개 언어를 오갈 수 있습니다.'},
'en':{'tag':'Interactive explainers on topics from Inference Engineering (Philip Kiely, 2026), one per week. Each week stands on its own. The Doctor, the Assistant, the Fruit Fly Researcher and AbaBot guide you through experiments and showdowns.','week':'Week {n}','read':'Read →','soon':'In preparation','plan':'Planned','w1':'The Week 1 explainer is in preparation.','w2b':'Coming next: 2.3 Image generation inference · 2.4 Calculating inference bottlenecks · 2.5 Optimizing attention','steps':'Five steps: matmul · activation functions · tokens and sampling · attention and the KV cache · Mixture of Experts (MoE)','by':'By Ahn Sangsun (CEO, M-Robo Inc.)','src':'Source: Philip Kiely, Inference Engineering, Baseten Books, 2026','lang':'Language','toc':'Contents','note':'Use the language menu at the top of each page to switch between the 7 languages.'},
'zh':{'tag':'每周一篇，讲解《Inference Engineering》（Philip Kiely，2026）中一个主题的互动讲解。每一周都可以单独阅读。博士、助手、果蝇研究员和算盘宝将通过实验和对决为你引路。','week':'第{n}周','read':'阅读 →','soon':'准备中','plan':'计划中','w1':'第1周的讲解正在准备中。','w2b':'后续内容：2.3 图像生成推理 · 2.4 推理瓶颈计算 · 2.5 注意力优化','steps':'五个阶梯：矩阵乘法 · 激活函数 · 词元与采样 · 注意力与 KV 缓存 · 混合专家（MoE）','by':'作者 · Ahn Sangsun（M-Robo 公司 CEO）','src':'资料：Philip Kiely，《Inference Engineering》，Baseten Books，2026','lang':'语言','toc':'目录','note':'在每页顶部的语言菜单中可以切换 7 种语言。'},
'ja':{'tag':'『Inference Engineering』（Philip Kiely, 2026）のテーマを週に1本ずつ扱うインタラクティブ解説です。どの週も単独で読めます。博士・助手・ショウジョウバエ研究員・アバボットが実験と対決でご案内します。','week':'{n}週目','read':'読む →','soon':'準備中です','plan':'予定','w1':'1週目の解説は準備中です。','w2b':'このあとの内容：2.3 画像生成の推論 · 2.4 推論のボトルネック計算 · 2.5 アテンションの最適化','steps':'5つの段：行列積 · 活性化関数 · トークンとサンプリング · アテンションとKVキャッシュ · 専門家混合（MoE）','by':'文 · Ahn Sangsun（M-Robo株式会社 代表）','src':'資料：Philip Kiely『Inference Engineering』Baseten Books, 2026','lang':'言語','toc':'目次','note':'各ページ上部の言語メニューで7つの言語を切り替えられます。'},
'ru':{'tag':'Интерактивные разборы тем из книги «Inference Engineering» (Philip Kiely, 2026), по одному на неделю. Каждую неделю можно читать отдельно. Доктор, Ассистентка, Исследователь-дрозофила и АбаБот проведут вас через эксперименты и поединки.','week':'Неделя {n}','read':'Читать →','soon':'Готовится','plan':'В планах','w1':'Разбор первой недели готовится.','w2b':'Далее: 2.3 Инференс генерации изображений · 2.4 Расчёт узких мест инференса · 2.5 Оптимизация внимания','steps':'Пять ступеней: матричное умножение · функции активации · токены и сэмплинг · внимание и KV-кэш · смесь экспертов (MoE)','by':'Автор · Ahn Sangsun (генеральный директор M-Robo Inc.)','src':'Источник: Philip Kiely, «Inference Engineering», Baseten Books, 2026','lang':'Язык','toc':'Содержание','note':'Переключайтесь между 7 языками в меню вверху каждой страницы.'},
'uz':{'tag':'«Inference Engineering» (Philip Kiely, 2026) kitobidagi mavzular boʻyicha har haftaga bitta interaktiv izoh. Har bir haftani alohida oʻqish mumkin. Doktor, Yordamchi, Meva pashshasi tadqiqotchi va AbaBot sizni tajribalar va bellashuvlar orqali boshlab boradi.','week':'{n}-hafta','read':'Oʻqish →','soon':'Tayyorlanmoqda','plan':'Rejada','w1':'1-hafta izohi tayyorlanmoqda.','w2b':'Keyingi mavzular: 2.3 Tasvir yaratishda inferens · 2.4 Inferensdagi tor joylarni hisoblash · 2.5 Diqqatni optimallashtirish','steps':'Besh pogʻona: matritsa koʻpaytmasi · faollashtirish funksiyalari · tokenlar va tanlash · diqqat va KV kesh · ekspertlar aralashmasi (MoE)','by':'Muallif · Ahn Sangsun (M-Robo Inc. rahbari)','src':'Manba: Philip Kiely, «Inference Engineering», Baseten Books, 2026','lang':'Til','toc':'Mundarija','note':'Har bir sahifaning yuqorisidagi til menyusi orqali 7 til oʻrtasida oʻtishingiz mumkin.'},
'vi':{'tag':'Mỗi tuần một bài giải thích tương tác về một chủ đề trong cuốn Inference Engineering (Philip Kiely, 2026). Có thể đọc riêng từng tuần. Tiến sĩ, Trợ lý, Nhà nghiên cứu Ruồi giấm và AbaBot sẽ dẫn bạn qua các thí nghiệm và màn đối đầu.','week':'Tuần {n}','read':'Đọc →','soon':'Đang chuẩn bị','plan':'Dự kiến','w1':'Bài giải thích tuần 1 đang được chuẩn bị.','w2b':'Phần tiếp theo: 2.3 Suy luận tạo ảnh · 2.4 Tính toán nút thắt suy luận · 2.5 Tối ưu cơ chế chú ý','steps':'Năm bậc: phép nhân ma trận · hàm kích hoạt · token và lấy mẫu · cơ chế chú ý và bộ nhớ đệm KV · hỗn hợp chuyên gia (MoE)','by':'Tác giả · Ahn Sangsun (CEO, M-Robo Inc.)','src':'Tư liệu: Philip Kiely, Inference Engineering, Baseten Books, 2026','lang':'Ngôn ngữ','toc':'Mục lục','note':'Dùng menu ngôn ngữ ở đầu mỗi trang để chuyển giữa 7 ngôn ngữ.'}}
for L in UI: UI[L].update(P[L])
b64=lambda p:'data:image/webp;base64,'+base64.b64encode(open(p,'rb').read()).decode()
COVER=b64('assets/img/cover_ch2_960.webp'); THUMB=b64('assets/img/thumb_02.webp')
DATA=json.dumps({'ui':UI,'langs':LANGS},ensure_ascii=False).replace('</','<\\/')
page='''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>인퍼런스 엔지니어링 해설</title>
<meta name="description" content="『Inference Engineering』(Philip Kiely, 2026)을 주차별로 읽는 인터랙티브 해설 시리즈 — 한국어·English·中文·日本語·Русский·Oʻzbekcha·Tiếng Việt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;700&display=swap">
<style>
/* 시리즈 목차 · 02 페이지와 같은 밤의 연구실 토큰 */
:root{--bg:#13141f;--panel:#1c1e2d;--panel2:#25283a;--rule:#363a52;--text:#eceaf3;--muted:#9d9bb8;--gfp:#5ee39c;--stain:#d672d6;--amber:#f1b646;--info:#82b8ff;--accent:#9ab8ff;
  --font:"IBM Plex Sans","IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans SC","Noto Sans JP",system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:16px;line-height:1.7}
h1,h2,h3,p{word-break:keep-all;overflow-wrap:break-word}
:lang(zh) h1,:lang(zh) h2,:lang(zh) h3,:lang(zh) p,:lang(ja) h1,:lang(ja) h2,:lang(ja) h3,:lang(ja) p{word-break:normal;line-break:strict}
.wrap{max-width:1000px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
nav{position:sticky;top:0;z-index:5;background:rgba(19,20,31,.85);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--rule)}
nav .wrap{display:flex;align-items:center;gap:12px;height:54px}
.logo{font-weight:700;display:flex;gap:8px;align-items:center;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.logo i{flex:0 0 18px;width:18px;height:20px;background:var(--gfp);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
select{font:inherit;font-size:13px;color:var(--text);background:var(--panel2);border:1px solid var(--rule);border-radius:8px;padding:4px 6px}
.cover{position:relative;width:100%;height:min(31.25vw,46vh);min-height:150px;overflow:hidden;background:#1b1533}
.cover img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 45%}
.cover::after{content:"";position:absolute;inset:auto 0 0 0;height:40%;background:linear-gradient(0deg,var(--bg),rgba(19,20,31,0))}
header.top{padding-block:28px 8px}
h1{font-size:clamp(28px,4.4vw,46px);line-height:1.2;margin:0 0 10px;text-wrap:balance}
.tag{color:#cfcde0;max-width:760px;margin:0}
h2{font-size:20px;margin:34px 0 12px;color:var(--accent)}
.list{display:grid;gap:14px}
.card{display:grid;grid-template-columns:240px 1fr;gap:16px;background:var(--panel);border:1px solid var(--rule);border-radius:14px;padding:14px;color:inherit;text-decoration:none;min-width:0}
a.card:hover,a.card:focus-visible{border-color:var(--gfp)}
a.card:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.card img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:10px;display:block;max-width:100%}
.card .ph{aspect-ratio:3/2;border-radius:10px;background:repeating-linear-gradient(135deg,var(--panel2) 0 12px,#20222f 12px 24px);border:1px dashed var(--rule)}
.card>div{min-width:0}
.wk{font-size:13px;color:var(--gfp);font-weight:500;letter-spacing:.03em}
.card h3{font-size:19px;margin:2px 0 6px;line-height:1.35}
.card p{margin:0 0 6px;color:#cfcde0;font-size:15px}
.chip{display:inline-block;font-size:12.5px;padding:2px 10px;border-radius:999px;border:1px solid var(--rule);color:var(--muted)}
.chip.go{border-color:var(--gfp);color:#c9f7de;background:rgba(94,227,156,.12)}
.card.off{opacity:.72}
footer{border-top:1px solid var(--rule);margin-top:40px;padding-block:24px 48px;color:var(--muted);font-size:14px}
footer p{margin:4px 0}
@media (max-width:640px){.card{grid-template-columns:1fr}.card.off .ph{display:none}}
</style>
</head>
<body>
<nav aria-label="series"><div class="wrap"><span class="logo"><i aria-hidden="true"></i><span id="series"></span></span><label for="lang" id="langlabel" class="chip" style="border:0;padding:0 2px"></label><select id="lang"></select></div></nav>
<div class="cover"><img src="__COVER__" width="960" height="540" alt="" fetchpriority="high" decoding="async"></div>
<main class="wrap">
  <header class="top"><h1 id="h1"></h1><p class="tag" id="tag"></p></header>
  <h2 id="toc"></h2>
  <div class="list">
    <a class="card" id="c2" href="02_models.html"><img src="__THUMB__" width="600" height="400" alt="" loading="lazy"><div><div class="wk" id="w2k"></div><h3 id="w2t"></h3><p id="w2q"></p><p id="w2s" style="font-size:14px;color:var(--muted)"></p><span class="chip go" id="w2r"></span></div></a>
  </div>
  <p style="color:var(--muted);font-size:14px;margin-top:16px" id="note"></p>
</main>
<footer><div class="wrap"><p id="by"></p><p id="src"></p></div></footer>
<script type="application/json" id="data">__DATA__</script>
<script>
(function(){var D=JSON.parse(document.getElementById('data').textContent), codes=D.langs.map(function(a){return a[0]});
  function $(i){return document.getElementById(i)}
  function file(l){return l==='ko'?'02_models.html':'02_models.'+l+'.html'}
  function pick(){var q=null; try{q=new URLSearchParams(location.search).get('lang');}catch(e){}
    if(q&&codes.indexOf(q)>=0) return q; var n=((navigator.languages&&navigator.languages[0])||navigator.language||'ko').slice(0,2).toLowerCase(); return codes.indexOf(n)>=0?n:'ko';}
  function render(L){var u=D.ui[L]; document.documentElement.lang=L; document.title=u.series;
    $('series').textContent=u.series; $('langlabel').textContent=u.lang; $('h1').textContent=u.series; $('tag').textContent=u.tag; $('toc').textContent=u.toc;
    $('w2k').textContent=u.week.replace('{n}','2')+' · Ch.2 Models · §2.1–2.2'; $('w2t').textContent=u.title; $('w2q').textContent=u.q; $('w2s').textContent=u.steps; $('w2r').textContent=u.read;
    $('c2').href=file(L)+'?lang='+L;
    $('note').textContent=u.note; $('by').textContent=u.by; $('src').textContent=u.src;}
  var sel=$('lang'); sel.innerHTML=D.langs.map(function(a){return '<option value="'+a[0]+'">'+a[1]+'</option>'}).join('');
  var L=pick(); sel.value=L; render(L);
  sel.addEventListener('change',function(){render(sel.value); try{history.replaceState(null,'','?lang='+sel.value);}catch(e){}});
})();
</script>
</body>
</html>
'''
page=page.replace('__COVER__',COVER).replace('__THUMB__',THUMB).replace('__DATA__',DATA)
open('dist/index.html','w').write(page)
print('index.html %.0f KB'%(len(page.encode())/1024))
