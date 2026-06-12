# LangGraph Supervisor: State Machine & Execution Logic

복잡한 작업을 파이프라인으로 구성하여 자동화하기 위한 5단계 상태 천이(State Transition) 로직입니다.

## 🔄 The 5-Step Loop

### 1. [Init] - 작업 계획 수립 (Planning)
- 사용자의 대규모 지령을 분석합니다.
- 필요한 전문가(Worker) 목록과 작업 순서를 설계합니다.

### 2. [Delegate] - 작업 위임 (Delegating)
- 특정 작업자에게 현재 상태(State)와 임무를 명확히 정의하여 전달합니다.

### 3. [Execute] - 작업 수행 (Work)
- 작업자(에이전트)가 할당된 코드 작성, 분석, 번역을 수행하고 결과 보고서를 제출합니다.

### 4. [Review] - 검수 및 피드백 (Reviewing)
- 감독관(Supervisor)이 결과물을 평가합니다.
- **Pass**: 다음 작업자로 넘어가거나 가공(Drafting) 단계로 진입합니다.
- **Fail**: 작업자에게 구체적 결함(Refactor)을 명시하며 수정을 지시합니다. (Feedback Loop)

### 5. [Finalize] - 최종 산출 (Reporting)
- 모든 공판이 끝나면 종합 산출물을 사용자(대장)에게 최종 보고합니다.

## 🚦 Decision Thresholds (결재 기준)
- **Critical Failure**: 두 번 이상의 수정 시도에도 실패할 경우.
- **High Risk**: 아키텍처나 데이터가 크게 변하는 결정적 분기점.
- **Ambiguity**: 사용자의 초기 의도와 충돌하는 새로운 정보 발견 시.
