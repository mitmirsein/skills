# 동사: animate — 모션 12원칙 요약 + 성능 규칙

모션은 장식이 아니라 **상태 변화의 설명**이다. 과하면 양산형 "AI 데모" 룩이 된다.

## 디즈니 12원칙 중 UI에 직결되는 것
- **Slow in / Slow out (ease)**: 선형(linear) 금지. `cubic-bezier(.2,0,0,1)` 류로 자연 가속·감속.
- **Anticipation / Follow-through**: 등장은 살짝 늦게 시작해 끝에서 정착. 스프링이 적합한 경우 사용.
- **Staging**: 한 번에 한 가지에 시선. 동시다발 모션 금지.
- **Timing**: 마이크로(호버) 120–200ms, 전환(모달/페이지) 200–400ms. 그 이상은 느리게 느껴짐.
- **Secondary action**: 주 모션을 보조하는 미세 모션(아이콘 회전 등)만, 경쟁시키지 말 것.

## 성능·접근성 규칙 (hard)
- **`transition: all` 금지** — 변하는 속성만 나열.
- **compositor-safe만 애니메이트**: `transform`, `opacity` 우선. `width/height/top/left/margin` 애니메이트는 레이아웃 thrashing → 지양(필요 시 `transform: scale/translate`로 대체).
- `box-shadow`·`filter: blur` 애니메이트는 비싸다 — 가짜 레이어(pseudo + opacity) 기법 고려.
- 스크롤 연동 모션은 `IntersectionObserver`/`scroll-timeline`, rAF 사용. 스크롤 핸들러에서 동기 레이아웃 읽기 금지.
- **`@media (prefers-reduced-motion: reduce)`**에서 비필수 모션 제거/약화 — 필수 안전장치.

## 패턴
- 진입: opacity 0→1 + translateY(8px→0), 120–200ms, ease-out.
- 호버: `transform: translateY(-2px)` + 그림자 한 단계 상승.
- 모달: 백드롭 fade + 패널 scale(.96→1). 닫힘은 더 빠르게(역재생 아님).

## 함정
- 모든 것에 모션 = 아무것도 강조 못 함.
- 긴 ease-in-out로 "고급스럽게" 착각 → 실사용은 답답함.
