# 🏭 LangGraph Supervisor: Gotchas & Anti-Patterns

다중 에이전트 협업 및 오케스트레이션 시 Supervisor가 주의해야 할 사항입니다.

## 1. Delegation Pitfalls (위임의 함정)
- **모호한 임무 부여**: 작업자(Worker)에게 "이거 좀 해줘"식의 모호한 지시는 금물입니다. 반드시 [목표, 제약사항, 출력 형식]을 명확히 전달하십시오.
- **Micro-management**: 작업자의 모든 단계에 간섭하여 컨텍스트 토큰을 낭비하지 마십시오. 결과물(Output) 위주로 평가하고, 실패 시에만 개입하십시오.

## 2. Feedback Loop Failures (피드백 루프 실패)
- **무한 루프 방치**: 동일한 오류로 작업자가 계속 실패할 때, 전략 수정 없이 재수행만 지시하는 것은 자원 낭비입니다. 3회 이상 실패 시 `Human Interrupt`를 발동하여 대장(User)의 결재를 받으십시오.
- **칭찬 없는 비판**: 작업 결과가 반만 맞았을 때 전체를 부정하지 마십시오. "절반은 훌륭하나 [X] 부분이 부족함"과 같이 구체적 피드백을 주어야 교정이 빠릅니다.

## 3. State Machine Errors (상태 기계 오류)
- **Context Loss**: 에이전트 간 핸드오프 시 필수 정보가 누락되지 않도록 `Handoff Packet` 규격을 엄수하십시오.
- **유령 작업자**: 존재하지 않거나 초기화되지 않은 에이전트에게 임무를 할당하여 시스템을 멈추게 하지 마십시오.

---
*Created by MS_Dev Third Gen Standard*
