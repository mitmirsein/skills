# GPT Prompt Strategies

> 기준 모델: **GPT-5 계열** (5.x — 버전은 빠르게 갱신됨).
> 특정 마이너 버전(5.2/5.4/5.5 등)의 능력을 단정하기 전에 공식 문서로 확인한다.

## Outcome-First Architecture
1. **Role & Personality**: 전문가 역할과 페르소나.
2. **Success Criteria**: "어떻게 하면 성공인가?"를 명시.
3. **Stop Rules**: 모델이 멈춰야 할 지점이나 금지 영역.

## Reasoning Effort
- "Step-by-step을 외워라" 식 구버전 기법보다 reasoning effort 파라미터 활용이 효율적.

## XML Legacy Support
- 하위 모델 호환이 필요하면 `<design_constraints>`, `<tool_rules>` 등 태그 구조 사용 가능.
