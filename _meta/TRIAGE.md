# 스킬 처분 분류 (TRIAGE)

작성: 2026-06-12 / 근거: `_meta/AUDIT.md` 베이스라인 감사 + 전수 탐색

처분 유형: **KEEP**(유지·소폭 개선) / **UPGRADE**(표준 재작성) / **SPLIT**(분할) /
**WRITE**(SKILL.md 신규 작성) / **MERGE?**(통합 후보 — **사용자 승인 필요**) /
**DEPRECATE?**(폐기 후보 — **사용자 승인 필요**) / **CLEANUP**(비문서 정리)

## 1. WRITE — SKILL.md 없음 (18개, F등급)

scripts/references는 있으나 본 지침이 없다. 배치에서 내용물 파악 후 SKILL.md 작성,
실질이 없으면 DEPRECATE? 로 전환.

| 스킬 | 분류 | 메모 |
|---|---|---|
| arc-librarian | vault | references+scripts 있음 |
| bible-meditation | theology | references+results 있음 |
| continuous-learner | utilities | |
| dictionary-editor | utilities | |
| journal-collector | academic-search | |
| knowledge-archivist | vault | references만 |
| langgraph-supervisor | dev-tools | |
| log-miner | dev-tools | |
| note-share | vault | references만 |
| notebooklm | academic-search | data만 — **MERGE? notebooklm-researcher로 흡수 검토** |
| ontology-builder | utilities | |
| rise-battleground-map | theology | |
| tech-architect | dev-tools | 구조 최소 |
| tech-reviewer | dev-tools | |
| tech-tdd | dev-tools | 구조 최소 |
| theology-chunker | theology | |
| theology-translator | theology | references 풍부 — 우선 작성 |
| visual-feedback | utilities | |

## 2. SPLIT — 모놀리스 분할 (200줄 상한 초과)

| 스킬 | 줄수 | 방침 |
|---|---|---|
| faith-compass | 356 | 상태 기계·4방향 매핑 정의를 references/로 분리, 본문은 라우팅+Phase만 |
| insane-search | 346 | 엔진 사양을 references/로, 타 스킬 스크립트 참조 경로 수정(W09 4건) |
| slide | 263 | React/테마 레퍼런스를 references/로, assets/hero.jpg 결손 해결 |

소프트캡(150줄) 초과: notebooklm-researcher(190), create-slide-from-markdown(162),
create-slide-image-prompts(158) — 배치에서 분리 검토.

## 3. MERGE? — 통합 후보 (사용자 승인 전 실행 금지)

| 후보 | 권고 |
|---|---|
| kci-searcher + kci-api-searcher | ✅ **결정 완료(2026-06-12, 사용자: "KCI는 API로만")** — kci-api-searcher 단일화, kci-searcher는 `status: deprecated` 처리(한 배치 주기 후 제거), 내부 .venv 삭제 완료 |
| ~~notebooklm → notebooklm-researcher~~ | ✅ 해소(2026-06-12) — 내용물이 .DS_Store뿐인 빈 폴더로 확인되어 제거. 흡수할 데이터 없음 |
| ~~theology-research vs theology-scholar~~ | ✅ 해소(배치 2) — 경계 명문화로 결정: research=서베이 래퍼, scholar=심층 연구·감사. 양쪽 description에 상호 참조 명시 |
| ~~nlk-biblio/subject/interlinker 3종~~ | ✅ 해소(배치 3) — 유지 확정, 파이프라인 순서(biblio→interlinker)를 description에 명문화 |
| ~~google-scholar-quick vs -semantic~~ | ✅ 해소(배치 3) — 유지 확정, 속도/심층 선택 기준을 양쪽 description에 명문화 |

## 4. CONTENT — 내용 신뢰성 문제

| 스킬 | 문제 | 방침 |
|---|---|---|
| prompt-engineer | references/가 유령 모델(GPT-5.5, Claude 4.7, Gemini 3.1) 기준으로 작성됨 (파일명 포함) | 배치에서 실존 모델 기준 전면 재작성·파일명 변경. SKILL.md 대표 문장은 수정 완료(2026-06-12) |
| insane-search | 참조 스크립트 4개가 타 스킬 폴더에 실재 — 경로 표기를 `.skills/<skill>/scripts/` 형식으로 수정 | 배치 처리 |

## 5. CLEANUP — 비문서 정리 (스킬 폴더 위생)

| 위치 | 문제 | 방침 |
|---|---|---|
| ~~riss-searcher/.venv~~ | 빈 껍데기(0B) | ✅ 배치 3에서 삭제 완료 |
| ~~kci-searcher/.venv~~ | 동기화 트리 안 venv | ✅ 삭제 완료 — 스킬 자체도 배치 7에서 최종 제거(참조 재지정 후) |
| ~~pdf-extractor/output (360MB)~~ | 작업 산출물 | ✅ 배치 7에서 삭제 (사용자 지시) |
| stealth-browser (62MB) | 브라우저 바이너리/캐시 추정 | 내용 확인 후 .stignore 또는 외부화 |
| theology-reviewer/.playwright-cli, google-scholar-quick/.playwright-cli | 브라우저 캐시 | .stignore 등록 확인 |

## 6. STUB — 골격만 존재 (정직하게 status: stub 표기 후 보강)

~~knowledge-gardener~~ → 실은 스텁이 아니라 wiki v4.0에 흡수된 **폐기 잔재**였음.
MS_Dev 심링크 제거 완료(2026-06-12). MS_Brain 본체 삭제 + 볼트 헌법 문서의 언급
제거는 사용자 승인 대기.
theology-terminology-linter(27줄), batch-operator(34줄), yt-subtitle-helper(35줄)

## 7. KEEP/UPGRADE — 나머지 전부 (B등급 65개)

공통 작업: description 하이브리드 형식(§3) 재작성 + gotchas.md 보강 + 체크리스트 통과.
세부 순서는 `_meta/PROGRESS.md` 배치 계획을 따른다.
