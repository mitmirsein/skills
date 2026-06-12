---
name: ontology-builder
description: >
  Extracts knowledge-graph elements from text — entities, evidence-backed
  relations, and aporia (negative ontology for what resists decomposition)
  — in micro or macro-hybrid modes, with human-in-the-loop commit approval.
  Use when the user asks to build an ontology, extract entities/relations,
  or map a text into the knowledge graph.
  키워드: 온톨로지 추출, 지식 그래프, 엔티티 관계, 아포리아 기록
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#온톨로지"
  - "온톨로지 추출해줘"
  - "지식 그래프 만들어줘"
references_path: ./references
---

# 🕸️ Ontology Builder (지식 그래프 구축기)

텍스트에서 Entity·Relation·Aporia를 추출해 지식 그래프로 구축하는 스킬입니다.
볼트 수준 관리(`wiki`)·담론 시각화(`theology-discourse-mapper`)와 역할이 다릅니다 —
이 스킬은 **추출과 DB 주입**을 담당합니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- **HITL 필수**: 추출 결과를 바로 저장하지 않는다 — 목록을 보여주고 최종 승인(Commit)
  후에만 주입.

## Phase 1 — 전략 선택 (정본: [extraction-strategies.md](./references/extraction-strategies.md))

- **Micro-Mode**: 단일 챕터 정밀 분석 → 즉시 주입
- **Macro-Hybrid**: 전역 구축 — 챕터 반복 분석으로 충돌·중복 조정 후 `add-bulk` 일괄 주입

## Phase 2 — 추출 (정본: [knowledge-schema.md](./references/knowledge-schema.md))

- **Entity**: `id`(PascalCase)·`type`·`names`·**`key_chunks`(증거 필수)**
- **Relation**: `source`·`target`·`relation` 술어·**`evidence`(증거 청크 필수)**
- 증거 없는 엔티티/관계는 생성 금지.

## Phase 3 — 부정 온톨로지 (Negative Ontology)

"분해되지 않는 것들의 지도" — 사용자가 "말로 표현이 안 돼", "분해하면 상실됨",
역설/신비/침묵을 표현하면: 분해 불가능 영역임을 확인하는 인터뷰(시도한 분해,
상실되는 가치) 후 `add_aporia`로 기록합니다. 긴장을 해소하지 않고 보존합니다.

## 검증·보고

- 주입 전 승인 목록(엔티티/관계/아포리아 수), 주입 후 DB 반영 확인 결과를 보고합니다.
