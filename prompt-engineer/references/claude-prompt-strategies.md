# Claude Prompt Strategies

> 기준 모델(2026-06 현재): **Claude Fable 5** (`claude-fable-5`), **Opus 4.8**, **Sonnet 4.6**, **Haiku 4.5**.
> 모델 버전은 계속 진화한다 — 특정 버전의 능력을 단정하기 전에 공식 문서(claude-api 스킬 또는 docs.claude.com)로 확인한다.

## 추론·자원 제어
- **Thinking Mode**: `adaptive` 설정으로 모델이 스스로 사고 깊이를 결정하게 함.
- **Effort Control**: 복잡한 문제는 `effort="xhigh"`로 최대 자원 투입, 단순 작업은 낮춰 비용 절감.
- **Pre-fill**: 최신 상위 모델(Opus 4.7+/Fable 5)에서는 pre-fill보다 명확한 지시가 더 효과적인 경우가 많음. 구세대(4.6 이하)에서는 여전히 유효.

## 구조화 (XML Tags — Claude 표준)
- `<context>`, `<task>`, `<constraints>`, `<example>`, `<output_format>` 태그로 구획.
- 긴 컨텍스트는 문서를 먼저, 지시를 마지막에 배치.

## 경량 모델 (Haiku 4.5)
- 깊은 추론 기대 대신 명확한 패턴 매칭 지시와 예시 제공이 유리.
