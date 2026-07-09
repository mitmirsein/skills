# econ-redteam — Canonical 고지

작성: 2026-07-09

이 스킬은 두 곳에 존재한다. 개발 정본(canonical)은 **`.skills/econ-redteam`** 이다.

| 위치 | 지위 |
|---|---|
| `~/Desktop/MS_Dev.nosync/.skills/econ-redteam` | **정본** — 여기서만 고친다 |
| `~/Desktop/MS_Dev.nosync/projects/omni-academic-framework/skills/econ-redteam` | 미러 — 복사만 받는다 |

## 규칙

- 버그 수정·기능 개선은 **정본에서 먼저** 한다. 미러를 독립적으로 개발하지 않는다.
- 정본을 고친 뒤 `python3 scripts/econ_gate.py sync`로 전파하고, `sync --check`로 drift가 0인지 확인한다.
- 두 사본은 **바이트 동일**을 유지한다. omni 사본이 분기해야 할 이유가 생기면 이 고지를 먼저 갱신하고, parity 규약을 "헤더 1블록 제외 content parity"로 완화한다.
- `tests/`는 정본 전용이며 미러에 복사하지 않는다. 미러의 `scripts/econ_gate.py sync`는 정본이 아닌 위치임을 감지하고 skip한다.

## 동기화 대상

`SKILL.md` · `CANONICAL_NOTICE.md` · `references/**` · `scripts/**` · `evals/**`
(`__pycache__`와 `.pyc`는 제외. 단일 진실은 `scripts/econ_gate.py`의 `SYNC_FILES`·`SYNC_DIRS` 상수다.)

## 강제 장치

- `python3 scripts/econ_gate.py sync --check` — drift 시 exit 1 (`pdf-extractor/scripts/sync_engine.py` 선례).
- `tests/test_mirror_parity.py` — sha256 바이트 동일을 강제하고 미러 전용 잔여 파일도 잡는다. 미러가 없으면 skip.

## 최근 sync

- 2026-07-09: v2.0.0 — 이중 모드(ex-ante/ex-post) 재편, 결정론 게이트(`econ_gate.py`) 신설, gotchas 대칭화, 죽은 `Phase 3.5` 표기 제거. 정본에서 작성 후 미러에 최초 전파.
