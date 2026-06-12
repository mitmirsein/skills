---
name: log-miner
description: >
  Mines unstructured conversation logs (.logs/) for reusable knowledge —
  flash ideas, code snippets, tactical instincts (forwarded to
  continuous-learner), and unfinished todos — then routes refined output
  into knowledge bases. Use when the user asks to mine, sift, or distill
  past session logs. 키워드: 로그 채굴, 대화 로그 정리, 인사이트 추출
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#log-miner"
  - "로그 채굴해줘"
  - "지난 대화에서 건질 것 찾아줘"
references_path: ./references
---

# ⛏️ Log Miner (대화 로그 채굴기)

비정형 대화 로그에서 핵심 지식을 발굴해 지식 베이스로 환류하는 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- 로그에 포함된 개인정보·비밀값은 추출물에 옮기지 않습니다.

## Phase 1 — 채굴 (정본: [extraction-protocol.md](./references/extraction-protocol.md))

대상: `.logs/tech/`, `.logs/theology/`, `.logs/misc/`

| 광물 | 추출 대상 | 목적지 |
|---|---|---|
| 💡 Flash Ideas | "만약 X를 한다면?" 류 발상 | `ideas.md` |
| 💾 Code Snippets | 재사용 가능한 함수·설정 | `snippets.md` |
| 🦁 Tactical Instincts | 사용자 취향·교정 사항 | `continuous-learner` → `instincts.md` |
| ✅ Todos | 미완성 작업 언급 | `todo.md` |

## Phase 2 — 정련·보존

- 추출 지식을 `data/` 또는 관련 프로젝트 지식 베이스에 통합합니다.
- **Retention**: 작업 완료 후 원본 로그의 아카이브/삭제 여부를 **반드시 사용자에게 확인**
  (임의 삭제 금지).

## 검증·보고

- 카테고리별 추출 건수와 기록 위치, 표본 1~2개를 보고합니다.
- 원본 로그 처리(보존/아카이브/삭제) 결정을 사용자 확인과 함께 기록합니다.
