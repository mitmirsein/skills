---
name: thoughtbox-lite
description: >
  Cookbook of thinking strategies for the Sequential Thinking MCP —
  efficient reasoning patterns, when to branch/revise, and budget control.
  Use when a problem needs structured multi-step reasoning or the user
  invokes #사고. 키워드: 사고 전략, 순차 추론, 추론 가이드
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#사고"
  - "#분석"
  - "#thinking"
  - "복합 문제 해결해줘"
capabilities:
  - sequential_thinking_optimization
  - backward_thinking_strategy
  - logical_branching_evaluation
  - token_optimized_reasoning
  - logic_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# 🧠 Thoughtbox Lite 3.0

## 1. Overview
복잡한 추론 시 MCP를 고도로 효율적으로 사용하기 위한 사고 전략 매뉴얼입니다.

## 2. Dynamic Thinking
본 사고 수행 전 **논리 함정(Gotchas)**과 **사고 제약(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 사고 단계 수(Step limits) 및 토큰 절약 필터 강도를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 직선적 사고의 늪 및 무의미한 단계 반복을 방지합니다.

### Phase 1: Directional Routing
문제의 성격에 따라 순방향, 역방향, 분기 경로 중 최적의 경로를 선택합니다. 지침은 [thinking-router.md](./references/thinking-router.md)를 참조하십시오.

### Phase 2: Token Economy & Proof
사고 단계를 최소화하면서도 논리적 완결성을 확보합니다. 운영 가이드 및 모범 사례는 [best-practices.md](./references/best-practices.md)를 참조하십시오.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 확증 편향 및 논리적 비약(Gap) 주의 가이드.
- [thinking-router.md](./references/thinking-router.md): 역방향 사고 프로토콜 및 문제 유형별 라우팅.
- [best-practices.md](./references/best-practices.md): 토큰 절약 규칙 및 검증 지침.

---
*Created by MS_Dev Third Gen Standard*
