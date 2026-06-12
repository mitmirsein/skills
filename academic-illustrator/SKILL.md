---
name: academic-illustrator
description: >
  Transforms theological/humanities text into publication-quality academic
  diagrams via a visualization pipeline with archetype banks and
  high-resolution rendering. Use when the user asks to diagram a concept,
  visualize a doctrine's structure, or illustrate an argument.
  키워드: 다이어그램, 개념 시각화, 학술 일러스트
version: 4.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#다이어그램"
  - "#일러스트"
  - "#시각화"
  - "이 개념을 그려줘"
  - "칭의론 체계도로 만들어줘"
capabilities:
  - scholarly_concept_schematization
  - visualization_pipeline_execution
  - high_resolution_image_rendering
  - mermaid_fallback_automation
  - error_mining_and_gotcha_avoidance
references_path: "./references"
status: active
---

# 🎨 Academic Illustrator 4.0

## 1. Overview
텍스트 속의 복잡한 논증과 추상적 개념을 학술 원형(Archetypes)에 따라 해체하고, 정교한 다이어그램으로 시각화하는 전문 일러스트레이션 스킬입니다.

## 2. Dynamic Workflow
본 스킬은 시각화 전 **함정(Gotchas)**과 **환경(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 선호하는 이미지 엔진 사양과 출력 경로를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 텍스트 렌더링 붕괴 및 시각적 노이즈를 방지합니다.

### Phase 1: Architect (Architect & Design)
텍스트의 논리 관계를 분석하여 가장 적합한 도식 원형을 선정합니다. 상세 정의는 [archetype-bank.md](./references/archetype-bank.md)를 참조하십시오.

### Phase 2: Stylist (Prompting)
학술 미학(Academic Aesthetic) 가이드를 적용하여 고해상도 이미지 및 Mermaid 코드를 설계합니다. 지침은 [visualization-protocol.md](./references/visualization-protocol.md)를 참조하십시오.

### Phase 3: Visualizer (Emission)
`generate_image`로 생성하거나, 복잡한 인덱스 중심 도표는 Mermaid 코드로 산출합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 시각적 노이즈 방지 및 Mermaid 폴백 타이밍 가이드.
- [archetype-bank.md](./references/archetype-bank.md): 동심원, 축, 페리코레시스 등 11개 도식 원형.
- [visualization-protocol.md](./references/visualization-protocol.md): 학술 미학 가이드 및 이미지 사양.

---
*Created by MS_Dev Third Gen Standard*
