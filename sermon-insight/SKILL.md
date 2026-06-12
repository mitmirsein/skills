---
name: sermon-insight
description: >
  Converts a theological paper's argument into a sermon insight package —
  decompiling the exegesis, mapping a lightweight ontology and aporia, and
  building three hermeneutical bridges toward a paradoxical proclamation.
  Use when the user asks to extract sermon insights from an academic paper.
  키워드: 설교 인사이트, 논문에서 설교, 케리그마 변환
version: 2.0.1
codename: Second Gen
author: MS_Dev
triggers:
  - "#sermon-insight"
  - "#설교인사이트"
  - "논문에서 설교 인사이트 추출해줘"
capabilities:
  - thesis_exegesis_decompilation
  - lightweight_ontology_and_aporia_mapping
  - three_hermeneutical_bridges
  - paradoxical_proposition_synthesis
  - forensic_sermon_auditing
references_path: "./references"
status: active
---

# 🛠️ sermon-insight

## 1. Overview
`sermon-insight` 스킬은 학술적 신학 논증(Exegesis)을 설교적 선포(Kerygma)로 변환하기 위해 고안되었다. 이 스킬은 텍스트의 추상적 표현을 명사화 해체 기법으로 복원하고, TOSK(Theology Ontology Starter Kit)를 참조한 경량 신학 온톨로지 및 신학적 아포리아(Aporia)를 도출한다. 최종적으로 3중 해석학적 교량과 청중 반론 제어가 결합한 역설적 도발 명제 설교 패키지를 생성한다.

## 2. Core Workflow
본 스킬은 다음 5단계의 파이프라인을 순차적으로 수행한다.

1. **Ingest (수집)**: 대상 신학 논문 원문과 신학적 필터(`theological_filter`), 청중 수준(`audience_level`)을 수집한다.
2. **Analyze (구조 분석)**: 논증 구조를 분석하고, 추상적인 복합명사를 `[행위자 + 동사]`의 동적 구조로 해체한다.
3. **Mine (신학 채굴 및 온톨로지 맵)**:
   * 4개 층위(`[CONTEXT]`, `[THEME]`, `[REDEEMPTIVE_TRAJECTORY]`, `[KERYGMA]`)를 태깅 및 추출한다.
   * TOSK 참조 경량 온톨로지(Continuant 분류, 주장-근거 매핑, 신학적 아포리아 구조)를 도출한다.
4. **Synthesize (설교 합성)**: 3중 해석학적 교량과 [도발 명제 → 예상 반론 선제 수용 → 긴장 유지 → 그리스도 중심적 해소]의 4단계 텍스트 블록을 합성한다.
5. **Validate (신학적 감사)**: 4대 신학 검증 필터(해석학적 정직성, 본문 우위성, 그리스도 중심성, 아포리아의 긴장 유지성)를 수행하여 품질 기준을 충족하는지 검사한다.

상세 실행 지침 및 입출력 규격은 `references/` 디렉터리의 문서를 참조한다.

## 3. Reference Links
- [schema.md](./references/schema.md): 입출력 데이터 규격 및 Markdown 저장 경로 정의
- [core-instructions.md](./references/core-instructions.md): 단계별 프롬프트 및 온톨로지/아포리아 구조화 상세 지침
- [best-practices.md](./references/best-practices.md): 신학적 비약 방지(Gotchas) 및 예외 처리, TRE 용어 준수 규칙

---
*Created by MS_Dev Second Gen Skill Forge*
