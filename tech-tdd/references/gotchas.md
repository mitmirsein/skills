# 🚦 Technical TDD: Gotchas & Anti-Patterns

테스트 주도 개발(TDD) 수행 시 에이전트가 주의해야 할 사항입니다.

## 1. Red Phase Pitfalls (Red 단계의 함정)
- **False Positive**: 테스트 코드가 잘못 작성되어, 구현 코드가 없는데도 성공(`PASS`)해버리는 상황을 경계하십시오. 반드시 '실패하는 것'을 먼저 눈으로 확인해야 합니다.
- **Brittle Tests**: 구현 세부 사항(Private method 등)에 너무 결합된 테스트를 작성하지 마십시오. 인터페이스와 결과(Behavior) 위주로 테스트하십시오.

## 2. Green Phase Failures (Green 단계 실패)
- **과잉 구현**: 테스트를 통과하기 위한 '최소한의 코드'가 아니라, 나중에 필요할 것 같은 기능까지 미리 구현(YAGNI 위반)하지 마십시오.
- **Dirty Hacks**: 테스트만 통과하면 된다는 생각으로 유지보수가 불가능한 스파게티 코드를 양산하지 마십시오. (이는 Refactor 단계에서 해결해야 합니다)

## 3. Refactor Errors (Refactor 오류)
- **Refactoring without Tests**: 테스트가 깨진 상태에서 코드를 고치려 하지 마십시오. 반드시 Green 상태에서 리팩토링을 시작하십시오.
- **Coverage Obsession**: 100% 커버리지라는 숫자에 집착하여 무의미한 테스트(예: 단순 Get/Set 테스트)를 양산하지 마십시오. 비즈니스 로직과 에지 케이스 보호가 우선입니다.

---
*Created by MS_Dev Third Gen Standard*
