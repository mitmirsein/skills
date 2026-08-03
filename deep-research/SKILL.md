---
name: deep-research
description: >
  Runs a resumable, tool-agnostic deep-research pipeline with query planning,
  parallel-or-sequential retrieval, source triangulation, claim-ledger gates,
  citation-audited reports, and claim-to-footnote conversion. Use when the user
  asks for comprehensive research, a source-backed investigation, landscape
  analysis, fact-checking, footnoted research output, or a Deep Research
  session that may need to resume across turns.
  키워드: 딥리서치, 심층 연구, 종합 조사, 출처 검증, 팩트체크, 각주 변환
version: 1.1.0
status: active
author: mitmirsein
triggers:
  - "/deep-research"
  - "deep research"
  - "딥리서치"
  - "심층 연구"
capabilities:
  - resumable_research_sessions
  - adaptive_multi_agent_retrieval
  - source_triangulation
  - deterministic_claim_validation
  - citation_audit
  - markdown_footnote_conversion
references_path: ./references
---

# Deep Research

질문 하나를 재개 가능한 증거 묶음과 검증된 보고서로 전환한다.

## Phase 0 — 가드레일과 라우팅

1. `references/gotchas.md`와 `references/evidence-policy.md`를 먼저 읽는다.
2. 사용 가능한 검색·브라우징·학술검색·서브에이전트 능력을 확인한다. 도구명은 가정하지 말고 `references/orchestration-adapters.md`에 따라 능력으로 선택한다.
3. 사용자가 특정 출력 위치를 지정하지 않으면 현재 작업 디렉터리의 `RESEARCH/`를 사용한다. 스킬 디렉터리 안에는 연구 산출물을 만들지 않는다.
4. 종합 조사, 출처 검증, 팩트체크 및 재개 가능한 딥리서치 세션 관리는 이 스킬로 처리한다.
5. 고위험 주제(의료·법률·재무·규제)는 `strict=true`로 설정하고 최신 1차 자료를 우선한다. 이 스킬의 검증은 전문가 자문을 대체하지 않는다.

## Phase 1 — 질문 정제와 세션 생성

1. 이미 구체적인 요청이면 질문을 늘리지 말고 합리적 기본값을 기록한다. 범위·독자·시점·산출물이 결과를 크게 바꿀 때만 한 번에 묻는다.
2. `references/query-schema.json`에 맞는 쿼리 JSON을 만든다.
3. 스킬 디렉터리에서 다음을 실행하고 출력된 세션 경로를 보존한다.

```bash
python3 scripts/research_session.py init \
  --root <output-root> --topic "<topic>" --query <query.json>
```

4. `resume` 요청은 기존 `state.json`을 읽어 마지막 미완료 단계부터 계속한다. `status` 요청은 `research_session.py status` 또는 `list`만 실행하고 새 조사를 시작하지 않는다.

## Phase 2 — 검색 계획

1. 질문을 겹침이 적은 3~5개 하위 문제로 분해한다.
2. 각 하위 문제에 발견·확인·반증 쿼리를 만든다. 최신성은 필요한 주장에만 현재 날짜를 반영한다.
3. 단계별 입력·산출물 계약은 `references/phase-contracts.md`를 따른다.
4. 계획 승인이 결과 방향을 실질적으로 바꿀 때만 사용자 확인을 받고, 아니면 바로 조사한다.

## Phase 3 — 적응형 조사

1. 서브에이전트가 있으면 역할을 분리해 사용 가능한 동시성 범위에서 최대 2~3개씩 배치 실행한다. 없거나 실패하면 메인 에이전트가 같은 하위 문제를 순차 조사한다.
2. 최신 사실은 웹·공식 문서, 학술 주장은 논문·학술 DB, 기술 주장은 공식 명세·원저장소를 우선한다.
3. 모든 조사 반환값을 `orchestration-adapters.md`의 공통 계약으로 정규화한다.
4. 원자료를 직접 읽지 못했으면 검색 스니펫을 원문 확인으로 표현하지 않는다.
5. 반환 파일을 다음 명령으로 `sources/sources.jsonl`에 병합한다.

```bash
python3 scripts/merge_findings.py \
  --output <session>/sources/sources.jsonl <finding-files...>
```

## Phase 4 — 삼각검증과 Claim Ledger

1. 핵심 수치·날짜·법률·의학·재무·규제·인과 주장을 `artifacts/claim_ledger.jsonl`에 기록한다.
2. 핵심 주장마다 독립 출처 두 개 이상을 찾고 반증 검색을 한 번 수행한다.
3. 출처 독립성, 등급, 1차 자료 여부는 `references/evidence-policy.md`로 판단한다.
4. 충돌·근거 부족·원문 미확인은 숨기지 말고 `unresolved`로 둔다.
5. 검증 게이트를 실행한다. 종료 코드 1은 반증 검색 누락, 2는 스키마·참조 오류다.

```bash
python3 scripts/validate_ledger.py --session <session>
```

## Phase 5 — 합성

1. `outputs/verified_claims.json`만 핵심 사실의 단정형 근거로 사용한다.
2. `unresolved_claims.json`과 `refuted_claims.json`은 본문 근거로 쓰지 말고 해당 부록에 분리한다.
3. 사용자 요구에 맞춰 `templates/research-report.md` 또는 `templates/executive-summary.md`를 적용한다.
4. 검증 가능한 사실에는 `[src_001]` 형식의 출처 ID를 붙이고, 핵심 주장에는 `[clm_001]`도 함께 표시한다.
5. 출처 링크는 참고문헌에 직접 URL 또는 DOI로 제공한다.

## Phase 6 — 품질 감사 및 각주 변환

1. 인용이 실제 문장을 지지하는지 원문과 대조한다.
2. 보고서에 `Confidence`, `Refuted`, `Unresolved` 절을 둔다.
3. 검증 게이트를 다시 실행한 뒤 보고서 평가를 실행한다.

```bash
python3 scripts/evaluate_report.py \
  --session <session> --report <report.md>
```

4. `FAIL`이면 알 수 없는 출처 ID, 잘못 배치된 미확정 주장, 누락 섹션을 고치고 재실행한다.
5. 본문의 `[clm_XXX]`, `[src_XXX]` 인용을 표준 마크다운 각주(`[^1]`, `[^2]`) 및 `## 각주 (Footnotes)` 섹션으로 자동 치환하려면 다음 스크립트를 실행한다.

```bash
python3 scripts/convert_footnotes.py \
  --session <session> --report <report.md> --output <report_footnotes.md>
```

## Phase 7 — 패키징과 보고

1. `state.json`을 마지막 단계로 갱신한다.
2. 최종 보고서, 출처 레지스트리, Claim Ledger, 검증·평가 결과의 경로를 제시한다.
3. 확인한 출처 수, 검증·미확정·반박 주장 수, 남은 한계를 간결히 보고한다.
4. 실제로 실행한 검사만 통과했다고 말한다.
