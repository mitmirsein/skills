# 단계별 계약

## Phase 1 — 질문 정제

입력:

- 사용자 질문
- 독자, 시점, 지역, 깊이, 산출물 제약

산출물:

- `artifacts/query.json`
- `state.json`

종료 조건:

- 조사 질문과 제외 범위가 한 문장으로 설명 가능하다.
- 성공 기준과 최신성 기준이 기록됐다.

## Phase 2 — 검색 계획

산출물 `artifacts/research_plan.json`:

```json
{
  "subtopics": [
    {
      "id": "sub_01",
      "question": "검증할 하위 문제",
      "discovery_queries": [],
      "confirmation_queries": [],
      "counter_queries": [],
      "preferred_sources": []
    }
  ]
}
```

종료 조건:

- 하위 문제는 3~5개이며 상호 중복이 설명 가능할 정도로 낮다.
- 핵심 주장 후보마다 1차 자료 경로와 반증 검색이 계획됐다.

## Phase 3 — 조사

산출물:

- `artifacts/agent-results/*.json` 또는 `*.jsonl`
- `sources/sources.jsonl`
- `sources/failed_access.jsonl`

종료 조건:

- 각 하위 문제에 직접 관련된 출처가 있다.
- 핵심 주장 후보는 독립 출처 두 개 또는 명시적 공백을 가진다.

## Phase 4 — 검증

산출물:

- `artifacts/claim_ledger.jsonl`
- `outputs/verified_claims.json`
- `outputs/unresolved_claims.json`
- `outputs/refuted_claims.json`

종료 조건:

- `validate_ledger.py`가 종료 코드 0으로 끝난다.
- `state.json.verification.passed`가 `true`다.

## Phase 5 — 합성

산출물:

- 요청된 최종 Markdown 보고서
- `sources/bibliography.md`

종료 조건:

- 핵심 단정은 verified claim에 연결된다.
- 모든 `[src_NNN]`가 출처 레지스트리에 존재한다.
- 반박·미확정 주장은 전용 절에만 있다.

## Phase 6 — 감사

산출물:

- `outputs/eval_report.json`

종료 조건:

- 평가 verdict가 `PASS`다.
- 의미론적 인용 대조를 직접 수행했다.

## Phase 7 — 전달

산출물:

- 최종 보고서
- 세션 상태와 감사 파일
- 한계 및 추가 조사 목록

종료 조건:

- `state.json`의 phase 7이 `completed`다.
- 사용자가 재개에 필요한 세션 경로를 받았다.
