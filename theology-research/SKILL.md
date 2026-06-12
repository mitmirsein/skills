---
name: theology-research
description: >
  Orchestrates the full theological research survey pipeline — multilingual
  query expansion, 7-engine literature search (KCI/RISS/Google Scholar ×2/
  Semantic Scholar/IxTheo/Crossref), forensic DOI verification, and Mosaic
  schema reporting. Use when the user asks for a theological literature
  survey or broad academic research on a theology topic.
  키워드: 신학 연구, 논문 서베이, 문헌 조사
version: 2.0.1
codename: Mosaic Spec
author: MS_Dev
triggers:
  - "#theology-research"
  - "#신학연구"
  - "신학 연구해줘"
  - "theology-research 실행"
capabilities:
  - query_expansion                    # 다국어(EN/DE) 학술 용어 확장 (Theology-Translator 연동)
  - hexa_engine_search                 # 7대 엔진(KCI/RISS/GS/GS Semantic/S2/IxTheo/Crossref) 활용 수집 가이드
  - forensic_gate                      # 수집 문헌 적합성 감사 및 DOI 실존 검증
  - paf_aporetics                      # 1차 텍스트 분석 및 TRE 용어 정합성 점검
  - mosaic_schema_output               # Appendix 및 Forensic Audit Log를 포함한 표준 출력
status: active
---

# 🏛️ Theology Research 2.0 (Mosaic Standard Wrapper)

본 스킬은 신학 학술 연구 및 논문 서베이 워크플로우를 에이전트가 완벽하게 자각하여 실행할 수 있도록 하는 통합 래퍼(Wrapper) 명세서이다.

---

## 1. 실행 파이프라인 (Execution Pipeline)

에이전트는 `#theology-research` 호출을 인지했을 때, 다음 5단계 과정을 순차적으로 수행한다.

### 1단계: [QUERY EXPANSION] (질의 확장)
- 입력된 한국어 주제 또는 연구 대상을 기반으로 하여 학술적으로 검증된 영어(EN) 및 독일어(DE) 전문 용어 세트를 설계한다.
- 이 과정에서 `theology-translator` 스킬의 번역 및 스타일 가이드를 참조하여 고전어(히브리어/그리스어) 전사 표기를 함께 확보한다.

### 2단계: [HEXA-ENGINE SEARCH] (7중 증거 수집 가이드)
자료 탐색의 누락을 방지하고 교차 검증 신뢰성을 극대화하기 위해 다음 7대 데이터베이스를 활용한다.
1. **KCI**: `kci-api-searcher` 스킬 활용 (`search.py` CLI). 공식 OpenAPI 기반 검색 기동.
2. **RISS**: `riss-searcher` 스킬 활용 (`search.py` CLI). InsaneRecon TLS 우회 방식.
3. **Google Scholar**: `search_web` 및 `google-scholar-quick`을 통해 상위 인용 논문을 발굴한다.
4. **Google Scholar Semantic**: `google-scholar-semantic` 스킬의 `scholar_runner.py`를 통해 Google Scholar Labs 시맨틱 정찰 데이터를 확보한다.
5. **Semantic Scholar**: `semantic-scholar` 스킬의 `s2_runner.py`를 호출하여 API 기반 정밀 메타데이터를 수집한다.
6. **IxTheo (ixto)**: `ixtheo-searcher` 스킬을 기동하여 유럽/독일어권 학술 서지 데이터를 2차 획득한다.
7. **Crossref Journal**: `crossref-journal-searcher` 스킬로 58대 피어 리뷰 신학 저널 대상 타겟 필터링을 수행한다.

### 3단계: [FORENSIC GATE] (포렌식 감사)
- 수집된 모든 문헌의 신학적 관련성을 감사한다.
- DOI 및 URL 실존 여부를 엄격히 확인하여 '유령 인용(Ghost Refs)' 및 주제 불합치 노이즈를 원천 배제한다.
- **LOD 식별자 연계**: 수집된 주요 인물 및 문헌 노드에 대해 `nlk-interlinker` 스킬을 구동하여 Wikidata, 미국의회도서관(LoC), 독일국립도서관(DNB) 등 글로벌 LOD URI를 조회하고 로컬 지식베이스에 연계한다.

### 4단계: [PAF & APORETICS] (본문 분석)
- Cathedral Engine의 1차 텍스트 분석 프로토콜을 수행한다.
- `MS_Brain.nosync` 사령부의 로컬 규칙(예: `tre_terms.csv` 용어 정의)을 조회하여 신학적 개념의 정합성을 확인한다.

### 5단계: [OUTPUT: MOSAIC SCHEMA] (산출물 구조화)
최종 결과물은 다음 표준 구조를 강제한다.
- **Body**: 신학적 통찰, 논증 TDD 및 변증적 전개를 중심으로 한국어 평서문(~한다) 어조로 기술한다.
- **Appendix: Research Inventory**: 검증을 통과한 모든 문헌 목록을 본문 최하단에 수록한다. (프론트매터 수록은 엄격히 차단한다.)
- **Forensic Audit Log**: 사용한 검색 엔진 목록, 구체적 쿼리 전략, 필터링 내역 및 제외 사유를 명시한다.

---

## 2. 통합 및 우선순위 규칙 (Prioritization Rules)

- **Scholar Labs Dynamic Option**: 자연어 연구 질문 쿼리 시 `google-scholar-semantic`을 가동하여 Scholar Labs 데이터를 수집하고, EvidencePack 계약을 강화한다.
- **S2 API Priority**: 일반 웹 검색을 통한 수집보다 API 메타데이터(`semantic-scholar`) 사용을 항상 우선한다.
- **IxTheo & Crossref Integration**: 유럽/독일어권 및 58종 프리미엄 학술지 타겟 팩트체크 시 두 스킬을 반드시 병행 기동하여 서지 목록을 정규화한다.

---
*MS_Dev Unified Standard — v2.0.0 (Research Wrapper) | 2026-05-21*
