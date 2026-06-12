# TDD: Red-Green-Refactor Cycle & Checklist

표준 TDD(테스트 주도 개발)의 핵심 사이클과 품질 체크리스트입니다.

## 🚦 The RGR Cycle
1. 🔴 **RED (실패)**: 요구사항을 만족하는 최소한의 실패하는 테스트 코드를 먼저 작성합니다.
2. 🟢 **GREEN (성공)**: 테스트를 통과할 수 있는 최소한의 실제 코드를 작성합니다. (우선 순위는 구현의 미려함보다 '성공'에 둠)
3. 🔵 **REFACTOR (정제)**: 기능을 유지한 채 코드의 가독성, 중복, 복잡도를 개선합니다.

## ✅ Development Checklist
- [ ] **Acceptance Criteria**: `사용자(역할)는 [기능]을 원한다. [이유] 때문이다.` 형식으로 목표 정의.
- [ ] **Test Vectors**: 정상 경로(Happy path), 경계값(Edge cases), 오류 상황(Error states)을 포함한 테스트 케이스 설계.
- [ ] **Strict Minimal**: 테스트 통과에 필요한 것 '이상'으로 코딩하지 않기.
- [ ] **Complete Isolation**: 각 테스트는 독립적이어야 하며 실행 순서에 영향을 받지 않아야 함.

## 🚫 Critical Anti-Patterns
- **구현 상세 테스트**: 내부 상태나 private 메서드가 아닌 '공개된 행동(Public Behavior)'을 테스트하십시오.
- **느린 테스트**: 유닛 테스트는 밀리초 단위로 실행되어야 합니다. 외부 API나 DB 의존성은 Mock을 활용하십시오.
