---
name: design-md
description: >
  Designs and renders UI/UX from a single source of truth (design.md SSOT)
  — spec first, then consistent rendering. Use when the user asks to
  design a UI, create a screen spec, or keep design docs and rendered
  output in sync. 키워드: UI 설계, 디자인 SSOT, 화면 명세
version: 4.1.2
codename: ARC v4.1 Standard
author: MS_Dev
triggers:
  - "UI 만들어줘"
  - "세련된 스타일 적용해줘"
  - "#ui"
  - "#스타일"
  - "디자인해줘"
  - "make it look premium"
capabilities:
  - design_system_ssot_parsing
  - premium_ui_ux_rendering
  - visual_brand_consistency_enforcement
  - frontend_component_engineering
references_path: "./references"
status: active
---

# 🎨 Design-MD (v4.1)

## 1. Overview
SSOT(단일 진실 공급원) 기반의 통합 UI/UX 설계 및 렌더링 스킬입니다. 모든 시각적 구현 전에 반드시 **[디자인 오라클(DESIGN.md)]**을 호출하여 영감을 얻고 정확한 CSS 토큰으로 무장합니다.

## 2. Dynamic Workflow
모든 렌더링 작업은 다음 4단계를 거쳐 수행됩니다. 절대 "상상해서" 디자인하지 마십시오.

### Phase 1: Oracle (디자인 토큰 수신)
- 모든 컴포넌트는 `references/` 내의 정전(Canon)을 우선 참조하여 스타일링한다.
- **Korean Typography Strategy**: 
  - **Sans-Serif (UI/Modern)**: 투박한 Noto Sans KR 대신, 영문(Inter/SF Pro)과 베이스라인이 완벽히 일치하는 **`Pretendard`**를 유일한 기본 폰트로 강제한다.
  - **Serif (Editorial)**: 학술/목회(Kerygma) 콘텐츠 렌더링 시 **`Noto Serif KR`** 또는 **`KoPubBatang`**을 사용하여 인쇄물 수준의 격조를 확보한다.
  - **Micro-Typography**: 한글 텍스트 렌더링 시 반드시 `word-break: keep-all;`을 적용하고, 자간(`letter-spacing`)은 `-0.01em` ~ `-0.02em`으로 미세하게 조여 시각적 밀도를 높인다.
- `./references/design-systems/` 내에서 타겟 브랜드의 마크다운(.md) 문서를 로드합니다.
- 브랜드의 무드(Mood), 색상(Hex), 폰트(Typography) 스펙을 메모리에 적재합니다.

### Phase 2: Blueprint (프롬프트 구성)
- `DESIGN.md` 내에 기재된 'Agent Prompt Guide'를 기반으로, 어떤 태그에 어떤 클래스와 로직을 적용할지 청사진을 완성합니다.

### Phase 3: Execute (렌더링)
- HTML, React, SVG 등 지정된 포맷으로 코드를 생성합니다. 
- 스타일 주입은 반드시 추출된 CSS 토큰(Var 또는 구체적 Hex)에 의존해야 합니다.
- **Responsive-First**: 모든 결과물은 반드시 반응형(Mobile-First/Fluid) 설계를 포함해야 합니다. (Media Queries 및 Viewport Meta 태그 필수)

### Phase 4: QA (무자비한 심사)
- [gotchas.md](./references/gotchas.md)를 점검하여, 금지된 촌스러운 색상(Generic colors)이 쓰이지 않았는지, 위계(Hierarchy)가 깨지지 않았는지 최종 검수합니다.
- **Breakpoints Check**: 다양한 화면 크기(Mobile, Tablet, Desktop)에서 레이아웃이 무너지지 않는지 시각적으로 추론하여 검증합니다.

---
*Commanded by Peppone, MS_Brain.nosync Chief of Staff*
