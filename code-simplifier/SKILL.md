---
name: code-simplifier
description: >
  Simplifies code — token diet, complexity reduction, and abstraction
  flattening while preserving behavior (an /simplify-style pass). Use when
  the user asks to simplify, shrink, or flatten over-engineered code.
  키워드: 코드 간소화, 토큰 다이어트, 추상화 평탄화
version: 2.0.1
codename: Second Gen
author: MS_Dev
triggers:
  - "#simplify"
  - "코드 간소화해줘"
  - "토큰 다이어트 시켜줘"
  - "추상화 평탄화해줘"
  - "flatten this code"
capabilities:
  - context_window_optimization_diet
  - redundant_abstraction_removal
  - control_flow_flattening_logic
  - code_complexity_reduction_metrics
references_path: "./references"
status: active
---

# 🪄 Code Simplifier 2.0

## 1. Overview
복잡한 코드 구조를 해체하고, 과도한 추상화를 제거하여 인지 부하와 LLM 토큰 소모를 극적으로 줄이는 '복잡도 스트리핑(Complexity Stripping)' 전문 스킬입니다.

## 2. Core Workflow
1. **Analyze**: 대상 파일의 로직 트리와 추상화 깊이를 스캔하여 간소화 지점을 식별합니다.
2. **Flatten**: 깊은 루프나 복잡한 조건문을 Early Return과 Guard Clause를 사용하여 1~2 Depth로 평탄화합니다.
   - 평탄화 기법 및 상세 파이프라인은 [flattening-protocol.md](./references/flattening-protocol.md)를 참조하십시오.
3. **Strip**: 쓰이지 않는 변수, 중복된 장황한 로직, 불필요한 반복문을 짧고 투명한 구조로 교체합니다.
   - 핵심 목표 및 실행 원칙(No Functional Changes)은 [simplification-principles.md](./references/simplification-principles.md)를 참조하십시오.
4. **Report**: 간소화 전/후의 라인 수 축소 및 복잡성 지표의 변화를 요약하여 보고합니다.

## 3. Reference Links
- [simplification-principles.md](./references/simplification-principles.md): "Less is More" 철학, 토큰 다이어트 목표 및 동작 보존 원칙.
- [flattening-protocol.md](./references/flattening-protocol.md): Early Return, Guard Clause 패턴 및 Simplifier 4단계 파이프라인 가이드.

---
*Created by MS_Dev Second Gen Skill Forge*
