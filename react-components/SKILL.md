---
name: react-components
description: >
  Converts Stitch design screens into modular Vite/React components —
  logic isolated into hooks, data externalized, then AST-validated via
  npm run validate. Use when the user asks to turn a Stitch design into
  React components. 키워드: 스티치 변환, 리액트 컴포넌트, 디자인 투 코드
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "Stitch 디자인을 리액트로 변환해줘"
  - "Stitch 화면 가져와서 컴포넌트로 만들어줘"
  - "convert stitch design [url]"
  - "#stitch-react"
capabilities:
  - stitch_design_to_react_conversion
  - ast_based_code_validation
  - logic_hook_isolation
  - modular_component_bundling
  - structural_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# ⚛️ Stitch to React Components 3.0

## 1. Overview
Stitch MCP를 통해 시각적 디자인 데이터를 확보하고, 이를 모듈화된 Vite 및 React 컴포넌트로 변환하는 프론트엔드 전문 스킬입니다.

## 2. Dynamic Workflow
본 변환 전 **구현 함정(Gotchas)**과 **개발 환경(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Env**: 대상 프로젝트 최상위 경로를 확인하고, 이 스킬 폴더에서 `npm install`이
  완료되어 `npm run validate`가 동작하는지 점검합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 하드코딩된 데이터 및 비즈니스 로직 혼재를 방지합니다.

### Phase 1: Retrieval & Intake
Stitch MCP를 통해 디자인 데이터(`get_screen`)를 확보합니다. 네트워킹 전략은 [stitch-integration.md](./references/stitch-integration.md)를 참조하십시오.

### Phase 2: Modular Assembly
컴포넌트, 훅, 데이터를 분리하여 작성합니다. 아키텍처 규칙은 [architecture-rules.md](./references/architecture-rules.md)를 참조하십시오.

### Phase 3: AST Validation
`npm run validate`를 통해 코드 품질을 검증합니다. 품질 체크리스트는 [qa-validation.md](./references/qa-validation.md)를 참조하십시오.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 인라인 스타일 남용 방지 및 타입 안정성 보장 가이드.
- [stitch-integration.md](./references/stitch-integration.md): Stitch MCP 호출 규약 및 `fetch-stitch.sh`.
- [architecture-rules.md](./references/architecture-rules.md): 모듈화 아키텍처 및 로직 격리(Hooks) 원칙.
- [qa-validation.md](./references/qa-validation.md): AST 검증기 연동 및 최종 심사 규정.

---
*Created by MS_Dev Third Gen Standard*