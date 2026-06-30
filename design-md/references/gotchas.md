# 🚨 UI Architect Gotchas (감각적·기술적 회피 함정)

AI가 흔히 저지르는 **"양산형 템플릿(Generic MVP Look)"**과 기술적 안티패턴을 깨부수는 안전장치. 모든 렌더링 전·Phase 4 critique에서 반드시 확인한다.

## 1. 원색·하드코딩 색상 (Primitive / Hardcoded Color)
- **증상**: `red`, `blue`, `#ff0000` 같은 브라우저 순색, 또는 **컴포넌트마다 흩뿌린 임의 hex**.
- **해결책**: 색은 반드시 [tokens/oklch-base.md](./tokens/oklch-base.md)의 OKLCH 토큰(`var(--color-…)`)을 거친다. brand canon의 hex조차 그대로 박지 말고 토큰으로 승격해 라이트/다크·대비를 파생한다.
- **주의**: 과거 버전이 권한 `색상명 #fbbf24` 식 **직접 hex 박기는 이제 금지**다. canon hex는 토큰의 *시드*일 뿐 최종 값이 아니다.

## 2. 일관성 없는 깊이감 (Inconsistent Shadows)
- **증상**: `box-shadow: 2px 2px 5px gray` 같은 구형 단일 섀도우로 플랫·촌스러움.
- **해결책**: 다중 레이어 섀도우(`0 1px 2px / 0 8px 24px rgba(...)`)나 canon의 Elevation 시스템을 따르고, 토큰화(`--shadow-1..3`)한다.

## 3. 죽은 인터페이스 (Lack of Micro-interactions)
- **증상**: 버튼·카드에 호버/포커스/액티브 반응이 없음.
- **해결책**: 상호작용 요소에 상태 변화를 명시하되 **`transition: all` 금지**(리플로우·예측불가 애니메이션 유발). 변하는 속성만 명시하고 compositor-safe 속성(`transform`, `opacity`)을 우선한다. 예: `transition: transform .18s ease, background-color .18s ease`. 상세는 [operations/animate.md](./operations/animate.md).

## 4. 가독성 파괴 (Typography Hierarchy Collapse)
- **증상**: 전부 동일 `sans-serif`, 위계 크기차 미미, 한글에 영문 폰트만 지정.
- **해결책**: 제목/본문 폰트 이분화 + Size·Weight 극명 대비. 한글은 [operations/typeset.md](./operations/typeset.md)의 Pretendard/Noto Serif KR + `word-break: keep-all` 규칙 강제.

## 5. 여백 부족 (Over-Crowding)
- **증상**: 요소가 다닥다닥 붙어 숨 쉴 틈 없음.
- **해결책**: `8px Base Grid` 준수, 컨테이너 패딩 최소 `24px`. 본문 측정폭은 45–75자(자세히는 typeset).

## 6. 접근성 무시 (Accessibility Blindness) — v5 신설
- **증상**: 본문 대비 4.5:1 미만, 포커스 링 제거(`outline:none`만), 키보드 도달 불가, 아이콘 버튼에 레이블 없음, `prefers-reduced-motion` 무시.
- **해결책**: 텍스트 대비 ≥ 4.5:1(큰 글자 3:1), 포커스는 `:focus-visible`로 *대체 표시* 제공, 모든 인터랙션은 키보드 도달 가능, 아이콘 전용 버튼에 `aria-label`, 모션은 `@media (prefers-reduced-motion: reduce)`로 약화. 상세 검수는 [operations/critique.md](./operations/critique.md).

## 7. 의미 평탄화 (Semantic Flattening) — v5 신설, 워크스페이스 헌법 직결
- **증상**: 신학·에디토리얼 콘텐츠에서 대립·아포리아·긴장을 시각적으로 한 결론처럼 정렬해 버림.
- **해결책**: 대립 항은 시각 위계에서도 **대등하게(병렬 컬럼·대조 블록)** 두고, 종합을 강요하지 않는다. 사용자가 명시적으로 종합을 요청한 경우만 단일화한다.
