---
name: google-scholar-quick
description: >
  Fast Google Scholar scrape via Playwright CLI (CDP) — grabs paper lists
  and URLs with near-zero token cost, no deep parsing. Use when the user
  wants a quick paper list; for citation-depth semantic recon use
  google-scholar-semantic instead.
  키워드: 스콜라 빠른 검색, 논문 리스트, 구글 스콜라
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "논문 리스트 뽑아줘"
  - "scholar 빠른 검색"
  - "find papers quickly"
  - "#google-scholar-quick"
capabilities:
  - fast_academic_indexing
  - low_token_search_engine
  - cdp_accelerated_scraping
  - scraping_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# ⚡ Google Scholar Quick 3.0

## 1. Overview
Playwright CDP를 활용하여 구글 스콜라에서 논문 목록과 URL을 초고속으로 확보하는 연구 지원 도구입니다.

## 2. Dynamic Workflow
본 검색 전 **시스템 함정(Gotchas)**과 **스크래핑 환경(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 엔진 대기 시간(Wait) 및 결과 노출 제한(Limit)을 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 캡차 유발 및 잘못된 링크 확보를 방지합니다.

### Phase 1: Search & Exploration
입력된 쿼리를 CDP 엔진을 통해 스콜라에 전달합니다. 엔진 사양은 [engine-specs.md](./references/engine-specs.md)를 참조하십시오.

### Phase 2: Collect & Filter
제목, 저자, 링크를 정제하여 대장(User)의 의도에 부합하는 리스트를 선별합니다.

### Phase 3: Reporting & Handoff
수집된 결과를 보고하고 심층 연구(Semantic Search) 연동 여부를 확인합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 캡차 방지 및 결과 리스트 정제 가이드.
- [engine-specs.md](./references/engine-specs.md): CDP 가속 기술 명세 및 실행 가이드.

---
*Created by MS_Dev Third Gen Standard*
