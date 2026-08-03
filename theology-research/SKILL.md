---
name: theology-research
description: >
  Orchestrates the full theological research survey pipeline — multilingual
  query expansion, 7-engine literature search (KCI/RISS/Google Scholar ×2/
  Semantic Scholar/IxTheo/Crossref), forensic DOI verification, Red Team Challenge
  (Adversarial Rationality), and Nash Equilibrium Mosaic schema reporting.
  Use when the user asks for a theological literature survey or broad academic
  research on a theology topic.
  키워드: 신학 연구, 논문 서베이, 문헌 조사, 내쉬 균형 신학, 적대적 검증
version: 2.1.0
codename: Mosaic Nash Spec
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
  - paf_aporetics_redteam              # 텍스트 분석, TRE 용어 점검 및 Red Team 공격 시뮬레이션
  - steelmanning_nash_synthesis        # 반대 입장 강철 인간화(Steel-manning) 및 파훼 불가능한 내쉬 균형 합성
  - mosaic_schema_output               # Appendix, Red Team Audit Log를 포함한 표준 출력
status: active
---

# 🏛️ Theology Research 2.1 (Mosaic & Nash Equilibrium Standard)

본 스킬은 7대 데이터베이스 서베이와 **v1.3 적대적 이성 게임**(Adversarial Rationality Protocol) 및 **신학적 내쉬 균형**(Theological Nash Equilibrium)을 결합하여, 파훼 불가능한 고정밀 학술 결과물을 생성하는 통합 워크플로우 명세서이다.

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

### 4단계: [PAF & RED TEAM CHALLENGE] (적대적 텍스트 비평 및 반론 시뮬레이션)
- Cathedral Engine의 텍스트 분석 프로토콜 및 로컬 규칙(`tre_terms.csv` 용어 정의)을 적용한다.
- **Red Team Simulator 기동**: 논리적 오류, 안일한 인용(Lazy Citation), 문맥 이탈 인용, 교파적 편향 및 시대착오적 투영을 사정없이 공격한다.
- **Steel-manning**(강철 인간 만들기): 대립하는 반대 입장을 약화시키지 않고 가장 강력하고 설득력 있는 논거 형태로 재구성한다.

### 5단계: [OUTPUT: MOSAIC & NASH EQUILIBRIUM SCHEMA] (내쉬 균형 산출물 구조화)
최종 결과물은 다음 표준 구조를 강제한다.
- **Body**: 주요 기독교 전통(개혁주의, 가톨릭, 정교회 등)의 어떤 비판에도 무너지지 않는 파훼 불가능한 논제(**Theological Nash Equilibrium Thesis**)를 중심으로 작성하며, 한국어 평서문(~한다) 어조로 기술한다.
- **Argument Traceability Map**: 각 주요 주장(Claim)별 성경/학술 근거 및 Red Team 공격에 대한 방어 논리를 맵핑한다.
- **Appendix: Research Inventory**: 검증을 통과한 모든 문헌 목록을 본문 최하단에 수록한다. (프론트매터 수록은 엄격히 차단한다.)
- **Red Team Challenge & Forensic Audit Log**: Red Team의 공격과 이에 대한 방어/보강 내역, 사용 검색 엔진 및 쿼리 전략 내역을 명시한다.

---

## 2. 통합 및 우선순위 규칙 (Prioritization Rules)

- **Adversarial Invincibility Principle**: 단지 자료를 요약 나열하는 교과서적 서술에 그치지 않고, 적대적 검증(Red Team Attack)을 거쳐 논리적 결함이 0인 내쉬 균형 상태의 논제를 도출한다.
- **Scholar Labs Dynamic Option**: 자연어 연구 질문 쿼리 시 `google-scholar-semantic`을 가동하여 Scholar Labs 데이터를 수집하고, EvidencePack 계약을 강화한다.
- **S2 API Priority**: 일반 웹 검색을 통한 수집보다 API 메타데이터(`semantic-scholar`) 사용을 항상 우선한다.
- **IxTheo & Crossref Integration**: 유럽/독일어권 및 58종 프리미엄 학술지 타겟 팩트체크 시 두 스킬을 반드시 병행 기동하여 서지 목록을 정규화한다.

---
*MS_Dev Unified Standard — v2.1.0 (Mosaic & Nash Equilibrium) | 2026-07-28*

