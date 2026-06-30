---
name: design-md
description: >
  Designs and renders UI/UX from a single source of truth (design.md SSOT)
  by composing focused design operations — route intent, load brand canon
  and OKLCH tokens, run verb-passes, then score the result. Use when the
  user asks to design a UI, render a screen, polish or redesign an existing
  interface, or typeset editorial/print output.
  키워드: UI 설계, 디자인 SSOT, 화면 명세, 다듬어줘, 인쇄 조판, 프리미엄 스타일
version: 5.0.0
codename: ARC v5 Composable Oracle
author: MS_Dev
triggers:
  - "UI 만들어줘"
  - "세련된 스타일 적용해줘"
  - "다듬어줘 / polish"
  - "이 화면 개선해줘"
  - "인쇄용으로 조판해줘"
  - "#ui"
  - "#스타일"
  - "make it look premium"
capabilities:
  - intent_routing_to_design_operations
  - design_system_ssot_parsing
  - oklch_token_system
  - composable_premium_ui_ux_rendering
  - editorial_print_grade_typesetting
  - scored_design_critique
references_path: "./references"
status: active
---

# 🎨 Design-MD (v5 · Composable Oracle)

브랜드 정전(canon)과 OKLCH 토큰을 진실 공급원으로 삼아, **작은 디자인 동사(operation)들을 의도에 맞게 합성**하여 렌더링하고 점수로 검수하는 스킬. 절대 "상상해서" 디자인하지 않는다.

v4의 일괄 1패스를 버리고, 재호출·부분개선이 가능한 **동사 파이프라인**으로 전환했다. 모든 동사는 워크스페이스 전역(UI/문서/인쇄/Obsidian)에서 상시 사용 가능하다.

## Phase 0 — 가드레일

- 모든 렌더링 전 [references/gotchas.md](./references/gotchas.md)를 읽고 양산형(Generic) 함정·접근성·모션 안티패턴을 확인한다.
- 한글이 등장하면 [typeset](./references/operations/typeset.md)의 타이포 규칙(Pretendard / Noto Serif KR, `word-break: keep-all`)이 **무조건** 적용된다.

## Phase 1 — Route (의도→동사 체인 선택)

사용자 의도를 분류하고, 아래 기본 체인 중 하나를 고른 뒤 불필요한 동사는 건너뛴다. 각 동사 파일은 **그 단계를 실행할 때만** 읽는다(progressive disclosure).

| 의도 | 기본 동사 체인 |
|---|---|
| 새 화면/컴포넌트 생성 | shape → layout → typeset → colorize → animate → harden → critique |
| 다듬기/마감 (polish) | critique → (layout·typeset·colorize 중 지적된 것) → critique |
| 기존 UI 개선 (redesign) | critique → 타겟 동사 → harden → critique |
| 에디토리얼·설교·저널 인쇄 | shape → typeset → print-grade → critique |
| 색/팔레트 작업 | colorize (→ oklch-base 토큰) |
| 반응형/멀티타깃 | adapt |

동사 카탈로그 (`references/operations/`):
- [shape.md](./references/operations/shape.md) — 코드 전 설계 인터뷰 → 디자인 브리프
- [layout.md](./references/operations/layout.md) — 8px 그리드·리듬·여백·위계
- [typeset.md](./references/operations/typeset.md) — 한·영 타이포 시스템, 측정폭, 마이크로 타이포
- [colorize.md](./references/operations/colorize.md) — 브랜드 색 → OKLCH 팔레트 적용
- [animate.md](./references/operations/animate.md) — 모션 12원칙 요약 + compositor-safe 규칙
- [harden.md](./references/operations/harden.md) — empty/error/loading/긴 한글/i18n/edge
- [adapt.md](./references/operations/adapt.md) — 반응형·인쇄·Obsidian-native 출력 타깃
- [print-grade.md](./references/operations/print-grade.md) — 인쇄급 조판(@page·금칙·각주·성구)
- [critique.md](./references/operations/critique.md) — 0–100 점수 루브릭 + 페르소나 + 신학적 긴장 체크

## Phase 2 — Oracle (정전·토큰 적재)

- `references/design-systems/`에서 타겟 브랜드 `.md`를 로드해 무드·색·폰트 스펙을 적재한다. (예: apple, toss, stripe, linear, notion, Claude_Editorial, Academic_Minimalist, sermon-framework …)
- 색은 hex로 끝내지 말고 [references/tokens/oklch-base.md](./references/tokens/oklch-base.md)로 OKLCH 토큰화하여 라이트/다크·대비·계절(전례) 변주를 파생한다.
- 브랜드 미지정 시: 콘텐츠 성격으로 추정(SaaS→linear/stripe, 에디토리얼/신학→Claude_Editorial/Academic_Minimalist)하고 사용자에게 한 줄로 확인한다.

## Phase 3 — Compose (동사 순차 실행)

1. 선택한 체인을 순서대로 실행한다. 각 동사 파일을 그 시점에 읽고 규칙을 적용한다.
2. 스타일 주입은 **추출된 OKLCH 토큰(var)** 에 의존한다. 임의 hex·원색 금지(gotchas §1).
3. 출력 포맷(HTML/React/SVG/Obsidian)은 [adapt.md](./references/operations/adapt.md)가 정한 타깃 규약을 따른다. 모든 화면 출력은 Mobile-First 반응형 필수.

## Phase 4 — Critique (무자비한 점수 심사)

- [critique.md](./references/operations/critique.md)의 루브릭으로 0–100 점수화하고, 70점 미만 항목은 해당 동사로 되돌아가 1회 이상 보정한다.
- gotchas.md 전 항목 + 접근성(대비·포커스·키보드) 통과 여부를 명시한다.
- **신학/에디토리얼 콘텐츠**: 대립·아포리아가 시각 위계에서 단일 결론으로 평탄화되지 않았는지 반드시 점검(워크스페이스 헌법 직결).

## 검증·보고

- 보고 시: 선택한 동사 체인, 적용 브랜드 canon, critique 총점과 미달 항목, 사용한 OKLCH 토큰을 명시한다.
- 실제로 렌더 결과를 추론·검수하지 않았다면 그렇다고 정직하게 말한다. 임의 가정으로 통과 처리 금지.

---
*Commanded by Peppone, MS_Brain.nosync Chief of Staff*
