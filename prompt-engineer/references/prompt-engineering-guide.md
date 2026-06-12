# Prompt Engineering Guide

[...내용 생략 - 원본 저장소의 prompt-engineering-guide.md 내용이 들어감...]
*(이 파일은 treylom/prompt-engineering-skills의 핵심 가이드를 포함함)*

## 핵심 모델별 전략 요약

### GPT-5 계열 (Outcome-first)
1. **Role**: 구체적인 페르소나 설정.
2. **Personality**: 말투와 태도 정의.
3. **Goal**: 달성하고자 하는 궁극적 목표.
4. **Success Criteria**: 결과물 평가 기준.
5. **Constraints**: 금지 사항 및 제약 조건.
6. **Output**: 원하는 출력 형식.

### Claude — Fable 5 / Opus 4.8 (Adaptive Thinking)
- `thinking={"type":"adaptive"}` 설정 권장.
- `effort="xhigh"`로 깊은 추론 유도.
- XML 태그를 사용하여 구조화된 컨텍스트 제공.

### Gemini 3 계열 (Constraints First)
- 제약 조건을 프롬프트 상단에 배치하여 주의력 집중.
- 다국어 및 멀티모달(이미지/비디오) 통합 지시 활용.
