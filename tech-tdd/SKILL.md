---
name: tech-tdd
description: >
  Drives development through the Red-Green-Refactor cycle — acceptance
  criteria first, failing test, minimal passing code, then refactor —
  with strict test isolation and public-behavior-only testing. Use when
  the user asks to build a feature test-first or add a disciplined test
  suite. 키워드: TDD, 테스트 주도 개발, 레드그린리팩터
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#tdd"
  - "TDD로 만들어줘"
  - "테스트 먼저 작성해줘"
references_path: ./references
---

# 🚦 Tech TDD (테스트 주도 개발)

코드보다 테스트를 먼저 쓰는 규율 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- 수용 기준을 먼저 정의합니다: `사용자(역할)는 [기능]을 원한다. [이유] 때문이다.`

## Phase 1 — RGR 사이클 (정본: [rgr-cycle.md](./references/rgr-cycle.md))

1. 🔴 **RED**: 요구사항을 만족하는 최소한의 **실패하는** 테스트 작성 — 실패를 실제로 확인
2. 🟢 **GREEN**: 테스트를 통과하는 **최소한의** 코드 작성 (그 이상 구현 금지)
3. 🔵 **REFACTOR**: 기능 유지한 채 가독성·중복·복잡도 개선 — 테스트 재실행으로 보증

테스트 벡터는 정상 경로·경계값·오류 상황을 포함하고, 각 테스트는 실행 순서와 무관하게
독립적이어야 합니다. 패턴 카탈로그: [testing-patterns.md](./references/testing-patterns.md)

## 안티패턴 (금지)

- 내부 상태·private 메서드 테스트 — **공개 행동만** 테스트
- 외부 API/DB 직접 의존 느린 테스트 — Mock 사용, 유닛은 밀리초 단위
- 테스트 통과를 위한 테스트 수정(요구사항 변경 없이)

## 검증·보고

- 각 사이클의 RED 실패 출력과 GREEN 통과 출력을 실제 실행 결과로 보여줍니다.
- 최종 보고: 테스트 수, 커버한 시나리오(정상/경계/오류), 남은 위험.
