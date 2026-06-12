# 스킬 개선 진행 추적 (PROGRESS)

목표: 모든 스킬을 `STANDARDS.md` 체크리스트(§8) 통과(A등급)로 끌어올린다.
세션이 바뀌어도 이 문서에서 이어서 작업한다.

## 배치별 스킬 업그레이드 절차 (플레이북)

스킬 하나당:

1. `python3 _meta/validate.py <skill>` — 현재 문제 확인
2. SKILL.md + references/ + scripts/ 정독, 스크립트 실행 가능성 점검
3. **구현안 작성**: `_meta/proposals/<skill>.md`에 개선안 기록 (변경 요지 5줄 이내 + 신규 description)
4. 적용: description 하이브리드화(§3) → 본문 한국어·Phase 골격(§4) → 150줄 초과분 references/ 분리
   → gotchas.md 보강 → 스크립트 docstring(§6) → 참조 무결성
5. version 마이너 범프, status 확정
6. `validate.py <skill>` 재실행 — A등급 확인 후 아래 표 갱신

MERGE?/DEPRECATE? 항목은 반드시 사용자 승인 후 실행 (`_meta/TRIAGE.md` §3).

## 배치 계획

| 배치 | 범위 | 개수 | 상태 |
|---|---|---|---|
| 0 | 기반 구축: 헌장·검증기·기계적 수정·거버넌스 문서 | — | ✅ 2026-06-12 완료 |
| 1 | vault: wiki, vault-query, knowledge-gardener, obsidian-cli, obsidian-web-clipper, zettel-capture, digital-curator (+WRITE: arc-librarian, knowledge-archivist, note-share) | 10 | ✅ 2026-06-12 완료 (9개 A등급, knowledge-gardener 심링크 제거) |
| 2 | theology: faith-compass(SPLIT) 외 17 (+WRITE: theology-translator, theology-chunker, bible-meditation, rise-battleground-map) | 18 | ✅ 2026-06-12 완료 (18/18 A등급) |
| 3 | academic-search: insane-search(SPLIT) 외 16 (+WRITE: journal-collector, notebooklm→MERGE?) | 17 | ✅ 2026-06-12 완료 (16/16 A — notebooklm은 빈 폴더로 제거, insane-search는 dev-tools로 재분류) |
| 4 | media: slide(SPLIT) 외 11 | 12 | ✅ 2026-06-12 완료 (12/12 A) |
| 5 | dev-tools: prompt-engineer(CONTENT) 외 13 (+WRITE: tech-architect/reviewer/tdd, langgraph-supervisor, log-miner) | 14 | ✅ 2026-06-12 완료 (14/14 A) |
| 6 | writing 5 + utilities 11 (+WRITE: continuous-learner, dictionary-editor, ontology-builder, visual-feedback) | 16 | ✅ 2026-06-12 완료 (16/16 A — **전 라이브러리 85/85 A등급**) |
| 7 | MERGE/DEPRECATE 승인 안건 일괄 처리 + CLEANUP(§5) + 부재 스크립트 4종 구현 | — | ✅ 2026-06-12 완료 — **프로젝트 완결: 84/84 A, 오류 0, 경고 0** |

## 배치 0 완료 기록 (2026-06-12)

- 백업: `~/skills-backup-2026-06-12.tar.gz` (20MB, venv/캐시/output 제외)
- `STANDARDS.md` 제정, `_meta/validate.py`·`fix_paths.py`·`fix_frontmatter.py` 작성
- 심링크 3개 상대경로화(`../../MS_Brain.nosync/.skills/...`), 죽은 `global` 심링크 제거
- 절대경로 `/Users/msn|msna-mba/` 118건(48개 파일) + MS_Brain 쪽 3개 파일 이식성 수정
  (md/json → `~/`, py → `os.path.expanduser`), 수정 py 18개 전부 구문 검사 통과
- frontmatter 정규화 68개 파일 (SemVer + codename 분리, status: active 기본)
- prompt-engineer SKILL.md 유령 모델명 1차 수정
- 감사 추이: 오류 104→22, 등급 C57/D2 → B65/C4

## 결정 기록

- 2026-06-12 사용자 결정: **KCI는 API로만** → kci-api-searcher 단일화(description 하이브리드 완료),
  kci-searcher `deprecated` + .venv 삭제. / **git 커밋 승인** → .skills 베이스라인 커밋.
- 발견 패턴: 따옴표 안 `~`는 셸/subprocess에서 확장 안 됨 → md 예시 2건 `$HOME`으로, subprocess 예시는
  `expanduser`로 교정. 배치 작업 시 동일 패턴 주의.

## 배치 1 완료 기록 (2026-06-12)

- 9개 스킬 A등급 달성. 구현안: `_meta/proposals/batch-1-vault.md`
- 신규 SKILL.md 3개 복원(arc-librarian, knowledge-archivist, note-share — references 기반)
- 결함 교정: obsidian-cli의 유령 config.json 참조, digital-curator `file://~` 표기,
  vault-query gotchas.md 신설(MS_Brain 쪽)
- knowledge-gardener: wiki v4.0에 흡수된 폐기 잔재 → MS_Dev 심링크 제거.
  **승인 대기**: MS_Brain 본체 폴더 삭제 + 볼트 CLAUDE/AGENTS/GEMINI.md의 언급 제거

## 메트릭 추이

| 일자 | A | B | C | D | F | 오류 | 경고 |
|---|---|---|---|---|---|---|---|
| 2026-06-12 (베이스라인) | 0 | 10 | 57 | 2 | 19 | 104 | 153 |
| 2026-06-12 (배치 0 후) | 0 | 65 | 4 | 0 | 18 | 22 | 86 |
| 2026-06-12 (배치 1 후) | 10 | 58 | 3 | 0 | 15 | 18 | 78 |
| 2026-06-12 (배치 2 후) | 28 | 45 | 2 | 0 | 11 | 13 | 64 |
| 2026-06-12 (배치 3 후) | 43 | 32 | 1 | 0 | 9 | 10 | 38 |
| 2026-06-12 (배치 4 후) | 55 | 21 | 0 | 0 | 9 | 9 | 24 |
| 2026-06-12 (배치 5 후) | 69 | 12 | 0 | 0 | 4 | 4 | 13 |
| 2026-06-12 (배치 6 후) | **85** | 0 | 0 | 0 | 0 | **0** | **0** |
| 2026-06-12 (배치 7 후) | **84** | 0 | 0 | 0 | 0 | **0** | **0** | ← kci-searcher 삭제로 모수 85→84

## 배치 7 완료 기록 (2026-06-12) — 프로젝트 완결

- 사용자 결정 4건 전부 집행: kci-searcher 삭제(런타임 참조 재지정), knowledge-gardener
  본체+헌법 5문서, pdf-extractor/output 360MB 삭제, 부재 스크립트 4종 **구현+실테스트**.
- 상세: `_meta/proposals/batch-7-cleanup-implementation.md`
- 이후 유지보수 모드: 새 스킬은 `_template` 복사 → `validate.py` A등급 통과 →
  `validate.py --index`로 INDEX 갱신.

## 배치 2 완료 기록 (2026-06-12)

- theology 18개 전부 A등급. 구현안: `_meta/proposals/batch-2-theology.md`
- faith-compass 356→112줄 분할(내용 불변), 신규 SKILL.md 4건 복원
- 부재 스크립트 정직 표기: theology-translator의 translator_audit.py,
  bible-meditation의 generate_tts.py → 배치 7(CLEANUP)에서 구현 여부 결정
