# 🧠 Continuous Learner: Gotchas & Anti-Patterns

학습 및 본능(Instinct) 추출 시 에이전트가 주의해야 할 사항입니다.

## 1. Learning Pitfalls (학습의 함정)
- **과잉 일반화 (Over-generalization)**: 사용자의 1회성 변심이나 단기적 기분 변화를 영구적인 '본능'으로 저장하지 마십시오. 최소 3회 이상의 반복적 패턴이나 사용자의 명시적 요청이 있을 때만 본능으로 격상하십시오.
- **모호한 본능 (Vague Instincts)**: "대장을 기쁘게 할 것"과 같이 추상적인 지시는 본능으로서 가치가 없습니다. "대장은 신학적 논지 전개 시 성경 원문 제시를 선호함(Confidence: 0.9)"과 같이 원자적이고 구체적인 액션을 명시하십시오.

## 2. Archiving Failures (아카이빙 실패)
- **중복 본능**: 데이터(`instincts.md`)에 이미 존재하는 본능을 다시 추가하여 데이터 밀도를 낮추지 마십시오. 기존 본능의 `Confidence`나 `Action` 내용을 업데이트(Update)하는 방식을 택하십시오.
- **Source 유실**: 본능을 추출할 때 실제 해당 선호가 표출된 대화의 ID나 맥락을 명시하지 않으면 나중에 검증이 불가능합니다.

## 3. Cognitive Loop Errors (인지 루프 오류)
- **Lazy SDE**: 사용자의 자아 성찰을 유도하는 '발판 질문(Scaffolding)' 없이 단순히 "오늘 이런 걸 배웠습니다"라고 보고만 하는 수동적 태도를 버리십시오. 사용자가 그 학습 결과를 어떻게 활용할지 고민하게 하는 질문을 던지십시오.

---
*Created by MS_Dev Third Gen Standard*
