---
name: theology-local-searcher
description: >
  Searches the local Theology AI Lab JSONL archive (msn_th_db) with 3-way
  multilingual lexical expansion and grep, returning source-grounded
  passages. Use when the user asks to find material in the local theology
  corpus (e.g., Barth-related sources) without going online.
  키워드: 로컬 검색, 신학 아카이브, 자료 찾기
version: 4.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#rag"
  - "#검색"
  - "find theology documents"
  - "search for [topic]"
  - "바르트 [주제] 관련 자료 찾아줘"
capabilities:
  - multi_language_expansion
  - lexical_search_grep
  - semantic_filtering
  - rdlo_verification
  - search_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# 🔎 Theology Local Searcher 4.0

## 1. Overview
로컬 JSONL 아카이브를 직접 검색하여 신학적 질문에 대한 원전 기반의 정밀한 답변을 생성하는 고속 검색 스킬입니다.

## 2. Dynamic Workflow
본 검색 수행 전 **데이터 함정(Gotchas)**과 **검색 설정(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 검색 티어(Tier) 범위 및 결과물 필터링 강도를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 인용 정보 위조(Hallucination) 및 문맥 상실을 방지합니다.

### Phase 1: Search Strategy
질문을 분석하고 쿼리를 **한/영/독**으로 확장합니다. 방법론은 [search-strategy.md](./references/search-strategy.md)를 참조하십시오.

### Phase 2: Execute & Verify
검색을 실행하고 결과의 신뢰성을 RDLO 프레임워크 기반으로 검증합니다. 지침은 [logic-verification.md](./references/logic-verification.md)를 참조하십시오.

### Phase 3: Synthesis (Output)
필터링된 정보를 정규 인용 형식과 함께 종합하여 답변합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** RDLO 논리 위반 방지 및 단일 키워드 검색 지양 가이드.
- [search-strategy.md](./references/search-strategy.md): 다국어 확장 및 데이터 티어링 지침.
- [logic-verification.md](./references/logic-verification.md): 검증 및 안전 규정.

---
*Created by MS_Dev Third Gen Standard*
