---
name: theology-discourse-mapper
description: >
  Extracts scholars (Actors), claims, and concepts from a theological text
  using the omni-academic-framework ontology and renders the debate
  landscape as RDF triples and Mermaid diagrams. Use when the user asks to
  map a scholarly debate or visualize discourse structure.
  키워드: 담론 분석, 학자 논쟁 맵, 온톨로지 추출
version: 1.0.1
author: MS_Dev
triggers:
  - "#theology-discourse-mapper"
  - "#담론분석"
  - "담론분석해줘"
  - "학자논쟁맵 그려줘"
capabilities:
  - theological_discourse_ontology_extraction
  - actor_claim_conflict_mapping
  - rdf_triples_generation
  - mermaid_visualization_export
status: active
---

# 🕸️ Theology Discourse Mapper 1.0

## 1. 개요
신학 학술 연구 및 텍스트 작성 과정에서 여러 학자들의 학설 대립과 논쟁 지형을 파악하는 것은 매우 중요하다. `theology-discourse-mapper`는 입력 텍스트를 정밀 분석하여 학자(`Actor`), 학설 및 주장(`Claim`), 핵심 용어 및 사상(`Concept`) 등을 추출하고, 이들 간의 지지(`supports`), 비판/대립(`conflicts_with`), 계승(`builds_on`) 등의 10대 관계 술어로 이루어진 온톨로지 데이터(RDF Triples) 및 시각화 다이어그램(Mermaid)을 자동으로 산출한다.

## 2. 온톨로지 스키마
`projects/omni-academic-framework` 프로젝트의 범용 온톨로지 정의와 100% 호환되도록 다음 모델을 상속 및 확장하여 작동한다.

### 7대 엔티티 클래스 (EntityClass)
- **Concept (개념)**: 신학적 주제, 교리, 사상적 핵심 단어 (예: Covenantal Nomism)
- **Actor (행위자/학자)**: 신학자, 학파, 역사적 인물 (예: E. P. Sanders)
- **Method (방법론)**: 텍스트 석의 방법, 분석 틀, 해석학적 렌즈 (예: Redaction Criticism)
- **Claim/Data (주장/데이터)**: 텍스트 내 명제, 학설적 판단 (예: Paul was not reacting against legalistic Judaism)
- **Artifact/System (저작/체계)**: 경전, 신학서적, 역사적 법전 (예: Covenant Code)
- **Context/Setting (해석학적 정황)**: 역사적 배경, 문화적 지평 (예: Post-Exilic Judah)
- **Limitation/Gap (해계/한계)**: 선행 연구의 한계, 해석학적 아포리아 (예: Lack of textual evidence in Amos 4:1)

### 10대 관계 술어 (RelationPredicate)
- `is_a`: 상위 개념-하위 개념 관계
- `part_of`: 전체-부분 관계
- `builds_on`: 이론이나 해석학적 기반 계승
- `is_derived_from`: 텍스트적/기록학적 기원
- `causes`: 인과 관계
- `correlates_with`: 상호 연관성
- `supports`: 다른 학설이나 주장을 동조/지지
- `conflicts_with`: 다른 학설이나 주장과 비판/대립
- `addresses`: 문제를 제기하고 해결책을 제시
- `uses_method`: 방법론 차용

## 3. 작동 프로토콜 (Execution Protocol)
1. 대상 신학 마크다운 파일 또는 직접 텍스트를 입력받는다.
2. 텍스트를 문단 단위로 슬라이싱하여 각 부분에서 지식 노드(`Node`)와 엣지(`Edge`) 구조를 탐색한다.
3. LLM API(Structured Output)를 기동하여 `OntologyMap` 형태의 JSON 구조를 추출한다. 이때 환각(Hallucination) 방지를 위해 각 노드와 엣지는 반드시 원문의 구체적인 인용(`source_quote`)과 문단 번호(`paragraph_id`)를 꼬리표로 보존한다.
4. 추출된 데이터를 결합하여 다음과 같은 3대 최종 자산(Assets)을 출력한다.
   - **온톨로지 메타데이터**: JSON 형식의 데이터
   - **담론 지형 보고서**: 학자들의 대립 쟁점을 요약 기술한 보고서
   - **Mermaid Graph**: 마크다운 렌더링용 관계 다이어그램 코드
5. 생성된 시각화 코드와 보고서를 대상 마크다운 파일에 추가하거나 독립된 분석 리포트(`.md`) 파일로 볼트에 수록한다.
