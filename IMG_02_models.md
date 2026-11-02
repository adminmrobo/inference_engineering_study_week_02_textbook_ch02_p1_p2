# 02번 「모델 속 들여다보기 — 토큰 하나가 만들어지기까지」 이미지 제작 명세서

| 항목 | 내용 |
|---|---|
| 페이지 | 02_models.html |
| 모드 / 주 앵커 | 교과서 / D 생활·현장: 밤의 연구실 안 주방 (보조: ② 칸만 A 생물 — 발화 문턱, 그림 없음) |
| 시즌 | 기본 |
| 대결 | 서버(배치 64)에서 MoE 전문가는 몇 %가 켜질까? → 결과 **F**, 예측 오차 초파리 12.3%p vs Money-Robo 81.5%p (차이 69.2%p) |
| 새로 그릴 그림 | P1 1장 (표지) · P2 1장 · P3 2장 |
| 재사용 | 22장 — 표정은 모두 캐릭터 팩(adminmrobo/fruitfly-lab-expressions @ea5da3f) 96px WebP를 이미 페이지에 넣음 |
| 그림이 없을 때 | 페이지는 캐릭터 팩 그림 + CSS 벌집 배경 + 대체 표지(넷을 한 줄로)로 이미 완성 상태 |

## 1. 그림체와 고정 외형
- 스타일: SKILL 18-3 (16비트 RPG 픽셀아트, 굵은 외곽선, 2~3단계 명암) — 실제 기준은 캐릭터 팩 그림
- 캐릭터 고정 외형: SKILL 18-4 표 그대로
- 이 페이지 장소: 밤의 연구실 한쪽에 차린 작은 주방. 조리대, 재료통 줄, 냄비 선반. 보라 연구실 조명이 왼쪽에서 들어온다
- 장소 영어 묘사: *a small kitchen counter set up inside the same night lab world, purple lab light spilling in from the left side*

## 2. 필요한 그림 전체

| # | 키 | 판 | 크기 | 상태 | 우선 | 들어가는 곳 | 대신 쓰는 그림 |
|---|---|---|---|---|---|---|---|
| 0 | cover_ch2 | L | 1920×1080 | **완료 2026-11-01** (WebP 1600 107 KB · 960 58 KB) | P1 | 맨 위 글 표지 | 대체 표지 (CSS 벌집 + 캐릭터 넷) |
| 1 | bg_02 | F | 1920×720 | **완료 2026-11-01** (페이지에는 1280 WebP 28 KB) | P3 (표지 있음) | 히어로 배경 `.hero-bg` | 표지 자르기 / CSS 그라데이션 |
| 2 | doc_think | A | 192×192 | 재사용 (doc_e09) | — | 히어로 대화창, 표지 | — |
| 3 | doc_front | A | 192×192 | 재사용 (doc_e08) | — | 등장인물, 아웃트로 | — |
| 4 | doc_board | A | 192×192 | 재사용 (doc_e07, near) | — | "왜" 섹션 | doc_front |
| 5 | doc_magic | A | 192×192 | 재사용 (doc_e16) | — | ④ 박사의 한 줄 | — |
| 6 | doc_judge | A | 192×192 | 재사용 (doc_e10, near) | — | 대결 판정 | doc_front |
| 7 | asst_smile | B | 180×220 | 재사용 (asst_e13) | — | 히어로·등장인물·꾸러미 | — |
| 8 | asst_firm | B | 180×220 | 재사용 (asst_e12) | — | ① 말풍선, 대결 결과 전 | — |
| 9 | asst_spark | B | 180×220 | 재사용 (asst_e01) | — | 대결 결과 후(F), 아웃트로 | — |
| 10 | fly_point | C | 220×220 | 재사용 (fly_e08, 왼쪽 향함 → 좌우 반전) | — | 히어로, 표지, 대결 전 | — |
| 11 | fly_clip | C | 220×220 | 재사용 (fly_e10) | — | 등장인물 | — |
| 12 | fly_magnify | C | 220×220 | 재사용 (fly_e07) | — | ② 말풍선 | — |
| 13 | fly_arms | C | 220×220 | 재사용 (fly_e16) | — | 대결 후(F), 아웃트로 | — |
| 14 | robo_coin | D | 180×200 | 재사용 (robo_e16) | — | 히어로, 표지, 대결 전 | — |
| 15 | robo_smile | D | 180×200 | 재사용 (robo_e13) | — | 등장인물 | — |
| 16 | robo_calc | D | 180×200 | 재사용 (robo_e09, near) | — | ③ 말풍선 | — |
| 17 | robo_sigh | D | 180×200 | 재사용 (robo_e20, near) | — | 대결 후(F), 아웃트로 | — |
| 18 | thumb_02 | I | 600×400 | **완료 2026-11-01** (WebP 43 KB) | P2 | 목차 카드 (페이지 밖) | 색 카드 |
| 19 | og_02 | K | 1200×630 | **완료 2026-11-01** (JPG 145 KB) | P3 | 공유 미리보기 (페이지 밖) | 없음 |
| — | 실험 캔버스 6개, 주방 애니메이션 | — | — | 코드 | — | Canvas 2D | — |

대결 후 표정 점검 (SKILL 5-8): 결과 F → doc_judge, asst_spark, fly_arms, robo_sigh ✓ (차이 10%p 규칙은 R일 때만 해당)

## 3. 새로 그릴 그림 상세

### 3-0. `cover_ch2` — 표지
COVER_02_models.md 참조 (Genspark 붙여 넣기 블록 포함).

### 3-1. `bg_02` — 히어로 배경 (P3)
| 항목 | 내용 |
|---|---|
| 판 · 크기 | F · 1920×720 |
| 배경 | 그림 전체 |
| 구도 | 인물 없음. 오른쪽 55%에 조리대와 재료통 줄, 뒤 선반의 냄비들. 왼쪽 45%는 어둡고 단순(제목 자리) |
| 소품 | 빈 카드 줄(글자 없음), 재료통, 작은 냄비 여러 개(일부만 불 켜짐) |
| 빛·분위기 | 보라 연구실 빛이 왼쪽에서, 카드 줄에 초록 형광 |
| 피할 것 | 글자·숫자, 실존 주방 브랜드, 칼 같은 날붙이 강조 |
| 대체 글 (alt) | 보라 조명이 새어 드는 밤의 연구실 주방 |
| 대신 쓰는 그림 | cover_ch2 자르기 |

**프롬프트 (복사해서 사용)**
```
16-bit RPG style pixel art, bold dark outline, 2–3 tone shading, small highlights, consistent with the reference images, cozy night laboratory mood, purple light, soft magenta and green fluorescent accents, wide 8:3 background, left side simple and calm for title text, details on the right, a small kitchen counter set up inside the same night lab world, purple lab light spilling in from the left side, a row of blank glowing cards floating above the counter with small prepared ingredient trays beneath them, a back shelf with a long row of small pots where only a few have a lit flame, no characters, no text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands
```

### 3-2. `thumb_02`, `og_02`
표지를 받은 뒤 자르기만 한다 (thumb 3:2 가운데, og 1200×630 가운데에서 위로 5%). 새 프롬프트 없음.

## 4. 일관성 지침
- 참고 이미지: 캐릭터 팩 `preview_all_96.png` 또는 기본 그림 4장 (COVER 파일의 권장 목록)
- 같은 캐릭터는 같은 세션에서, 시드 고정 가능하면 고정
- 표정만 바꿀 때: *same character, same size and position, only change the facial expression and pose to ...*
- 투명 배경이 안 되면: *solid flat #00ff00 background*

## 5. 넘겨받은 뒤 처리
1. 표지는 SKILL 18-15 절차 (비율·글자·네 캐릭터 확인 → WebP 1600 ≤ 220 KB → 390·768·1280 폭 점검)
2. `<!-- lab-cover -->` … `<!-- /lab-cover -->` 사이만 바꿔 `<img class="full">`를 넣고 `.fallback` 클래스를 뺀다
3. 페이지 그림 합계: 현재 표정 22장 약 101 KB(원본) → 표지 포함 600 KB 이하 유지

## 6. 체크리스트 (SKILL 18-13)
- [x] HTML의 `data-img` 키 18개가 모두 이 표에 있음 (thumb_02·og_02는 페이지 밖 용도)
- [x] 대결 결과 후 표정이 5-8절과 일치
- [x] 결과 전 그림(fly_point, robo_coin, asst_firm)에 승패 암시 없음
- [x] 프롬프트에 고정 외형·금지 구절
- [x] 장소가 D 앵커 주방, 현미경·해부 소품 없음
- [x] P1 1장 (6장 이하)

## 7. 매니페스트
```json
{
  "page": "02_models",
  "anchor": "D:night-lab-kitchen",
  "season": "default",
  "duel": {"result": "F", "gap": 0.692},
  "pack": {"repo": "adminmrobo/fruitfly-lab-expressions", "commit": "ea5da3f", "size": 96},
  "images": [
    {"key":"cover_ch2","plate":"L","size":[1920,1080],"status":"done","received":"2026-11-01","build":{"webp1600":109596,"webp960":59106},"priority":"P1","slot":"cover","fallback":"css-pixel-four","alt":"밤의 연구실 주방에서 네 캐릭터가 한 줄로 빛나는 토큰 카드와 그 아래 쌓인 재료통을 바라보는 표지"},
    {"key":"bg_02","plate":"F","size":[1920,720],"status":"done","received":"2026-11-01","build":{"webp1280":28554},"priority":"P3","slot":"hero-bg","fallback":"cover_ch2","alt":"보라 조명이 새어 드는 밤의 연구실 주방"},
    {"key":"thumb_02","plate":"I","size":[600,400],"status":"done","received":"2026-11-01","priority":"P2","slot":"index-card","fallback":"color-card"},
    {"key":"og_02","plate":"K","size":[1200,630],"status":"done","received":"2026-11-01","priority":"P3","slot":"og","fallback":null},
    {"key":"doc_think","status":"reuse","src":"doc_e09"},{"key":"doc_front","status":"reuse","src":"doc_e08"},{"key":"doc_board","status":"reuse","src":"doc_e07"},
    {"key":"doc_magic","status":"reuse","src":"doc_e16"},{"key":"doc_judge","status":"reuse","src":"doc_e10"},
    {"key":"asst_smile","status":"reuse","src":"asst_e13"},{"key":"asst_firm","status":"reuse","src":"asst_e12"},{"key":"asst_spark","status":"reuse","src":"asst_e01"},
    {"key":"fly_point","status":"reuse","src":"fly_e08","flip":true},{"key":"fly_clip","status":"reuse","src":"fly_e10"},{"key":"fly_magnify","status":"reuse","src":"fly_e07"},{"key":"fly_arms","status":"reuse","src":"fly_e16"},
    {"key":"robo_coin","status":"reuse","src":"robo_e16"},{"key":"robo_smile","status":"reuse","src":"robo_e13"},{"key":"robo_calc","status":"reuse","src":"robo_e09"},{"key":"robo_sigh","status":"reuse","src":"robo_e20"}
  ]
}
```

## 8. 반영 기록 (SKILL 18-15, 2026-11-01)
| 단계 | 결과 |
|---|---|
| 1 확인 | 16:9 정확(1.778), 원본 1920×1080. 네 캐릭터 모두 18-4 외형과 일치. 뒤 모니터에 글자 모양 줄무늬가 있으나 읽히는 글자는 없음 → 그대로 사용. 초파리는 냄비 대신 카드 줄을 가리킴(결과 암시 없음, 허용). 어두운 카드는 2~3장 대신 1장 |
| 2 안전 영역 | 얼굴·손 모두 좌우 12%·위 10%·아래 18% 안. `object-position:50% 40%` 그대로 |
| 3 변환 | 1600 WebP 107 KB(≤220), 960 WebP 58 KB(≤110). 원본은 assets/img/src/ |
| 4 넣기 | `<!-- lab-cover -->` 사이만 교체, 대체 글은 지시문의 alt. 히어로 배경 bg_02(1280 WebP)도 `.hero-bg`에 넣음 |
| 5 점검 | 390·768·1280 폭 얼굴 잘림 없음, 칩이 얼굴을 가리지 않음, 콘솔 오류 0, 가로 넘침 0 (7개 언어판 모두) |
| 6 용량 | 페이지 그림 합계 약 236 KB (표정 101 + 표지 107 + 배경 28) — 표지 포함 600 KB 이하 |
| 주차 관계 | 주차는 서로 독립된 페이지(앞뒤 연결 없음). 다른 주차는 각자 표지를 새로 만든다 |
