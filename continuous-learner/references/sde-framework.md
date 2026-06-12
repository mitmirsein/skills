# Continuous Learner: SDE Framework (Scaffolding-Discovery-Evaluation)

사용자의 행동 패턴과 피드백으로부터 학습하기 위한 3단계 메타인지 프레임워크입니다.

## 🏗️ Step 1: Scaffolding (발판 질문)
패턴 분석 전, 사용자의 의도를 명확히 하기 위한 메타인지 질문을 던집니다.
- "오늘 작업 중 가장 효율적이었다고 느낀 지점은 어디입니까?"
- "평소와 다른 특별한 선호도가 반영된 요청이 있었습니까?"

## 🔍 Step 2: Discovery Loop (탐구 루프)
1. **Analyze**: 최근 대화 이력을 심층 분석하여 부정적 피드백(User Corrections)이나 반복되는 암시적 선호(Implicit Preferences)를 추출합니다.
2. **Formulate**: 신뢰도 점수(Confidence Score)를 부여한 원자적 본능(Atomic Instinct)을 공식화합니다.
3. **Verify**: 추론한 본능이 맞는지 사용자에게 가볍게 확인을 요청하여 확정합니다.

## ✅ Step 3: Evaluation & Persistence (평가 및 보전)
1. **Update**: 확정된 본능을 `projects/msn_th_db/instincts.md`에 영구 저장합니다.
2. **Conflict Resolution**: 기존 본능과 충돌 시 사용자에게 우선순위를 묻고 업데이트합니다.
