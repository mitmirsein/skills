---
name: arc-librarian
description: >
  Standardizes vault notes into the ARC architecture — assigns category
  codes (100 Theology / 200 Ministry / 300 Tech / 400 Humanities /
  900 Archive), applies the standard YAML frontmatter schema, scores
  quality (arc_score 1–10), and links related notes. Use when the user
  asks to classify, file, or normalize notes into the ARC structure.
  키워드: ARC 분류, 노트 규격화, 메타데이터 표준화, 안치
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#arc"
  - "ARC 분류해줘"
  - "노트 규격화해줘"
  - "안치해줘"
references_path: ./references
---

# 📚 ARC Librarian (ARC 분류·규격화 사서)

볼트 노트에 ARC 분류 코드와 표준 메타데이터를 부여하고, 품질 점수(arc_score)와
관련 노트 링크를 채워 지식 자산으로 규격화하는 스킬입니다.

### Negative Scope (이 스킬이 하지 않는 것)
- ❌ 웹 자료 수집 → `knowledge-archivist`
- ❌ 위키 편찬·병합·린트 → `wiki`
- ❌ 제텔 카드 포착 → `zettel-capture`

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 느슨한 분류, 메타데이터 덮어쓰기,
  환상 링크를 방지합니다.
- 대상 노트의 **기존 frontmatter를 먼저 읽고 보존**합니다. 표준 필드만 추가/갱신합니다.

## Phase 1 — 분류 (Categorize)

- [arc-categorization.md](./references/arc-categorization.md)의 ARC 맵에 따라
  카테고리 코드를 판정합니다. 신학적 내용이라도 개인 묵상이면 200, 학술 연구면 100.
- 판정 근거를 한 줄로 남깁니다 (모호하면 사용자에게 확인).

## Phase 2 — 규격화 (Standardize)

- [metadata-schema.md](./references/metadata-schema.md)의 표준 YAML 스키마를 적용합니다.
  (tags 계층형 3~5개, created/updated, category, arc_score, themes, references)
- `arc_score`는 점수 기준표(1–3 Stub / 4–6 Developing / 7–9 Polished / 10 Masterpiece)에
  따라 자가 평가합니다.

## Phase 3 — 연결 (Link)

- `related:` 필드에 실존하는 노트만 연결합니다 — 연결 전 `rg` 또는 `obsidian search`로
  파일 실재를 반드시 확인 (환상 링크 금지).

## 검증·보고

- 변경된 노트 수, 카테고리별 분포, arc_score 분포를 보고합니다.
- 표본 1~2개 노트의 frontmatter를 보여주고, 기존 필드가 보존되었음을 확인합니다.
- `210 Meditation`은 읽기 전용 — 분류 대상에서 제외합니다.
