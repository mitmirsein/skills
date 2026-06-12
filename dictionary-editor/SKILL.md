---
name: dictionary-editor
description: >
  Writes encyclopedic theological dictionary articles — multilingual lemma
  standards (EN/DE/Greek/Hebrew with TRE IDs), the 5-section article
  structure, tension-preserving debates (Aporia Guard), and typed semantic
  relations. Use when the user asks to write or revise a dictionary entry
  for the vault wiki. 키워드: 사전 아티클, 표제어 집필, 신학 사전
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#사전"
  - "사전 아티클 써줘"
  - "표제어 작성해줘"
references_path: ./references
---

# 📖 Dictionary Editor (신학 사전 집필자)

백과사전식 신학 아티클을 표준 규격으로 집필하는 스킬입니다.
분류·안치는 `.skills/wiki`의 영역 — 이 스킬은 **집필만** 담당합니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- **TRE 정책(워크스페이스 헌법)**: 집필 단계에서 TRE 용어를 강제 매핑하지 않되,
  표제어 frontmatter의 `tre_id`·독일어 표기는 [lemma-standards.md](./references/lemma-standards.md)
  규약을 따릅니다.

## Phase 1 — 표제어 규격 (정본: [lemma-standards.md](./references/lemma-standards.md))

- 다국어 표기: `lemma_en` / `lemma_de`(TRE 우선) / `lemma_grc` / `lemma_heb`
- TRE에 있는 용어는 TRE ID 필수, 없으면 `tre_id: ""` 공란.

## Phase 2 — 아티클 집필 (정본: [article-structure.md](./references/article-structure.md))

필수 5섹션: ① 정의 ② 역사·발전 ③ 교파별 관점 ④ 주요 논쟁 ⑤ 1차 근거 문헌(직접 인용 필수)

- **Tension Preservation (Aporia Guard)**: 논쟁 섹션에서 양극(pole_a/pole_b)을 타협적
  중간값으로 합치지 않는다. frontmatter `tensions` 블록이 모두 채워져야 완성.
- **Semantic Linking**: 관계는 9종 유형 어휘(`opposes`, `grounds`, ...)와 신학 범주로
  frontmatter `relations` 블록에 명시.
- 중립성·증거 기반 — 모든 단락은 1·2차 문헌에 근거.

## 검증·보고

- 5섹션 충족, tensions/relations 블록 완성, 1차 문헌 인용 존재를 점검표로 보고합니다.
- 안치(볼트 배치)는 wiki 스킬에 인계함을 명시합니다.
