---
name: ixtheo-searcher
description: >
  Searches Tübingen's Index Theologicus (IxTheo) via OpenSearch/SRU and
  parses MARCXML for precise European and German-language theological
  bibliography. Use when the user asks for European or German theology
  literature beyond what KCI/Google Scholar cover.
  키워드: 튀빙엔 검색, 독일어권 신학 서지, IxTheo
version: 1.0.1
author: Antigravity
triggers:
  - "#ixtheo"
  - "#ixto"
  - "튀빙엔 검색"
  - "ixtheo search"
capabilities:
  - ixtheo_opensearch
  - ixtheo_sru_harvesting
  - marcxml_parsing
status: active
---

# 📚 Tübingen Index Theologicus Searcher (ixto)

## 1. Overview
튀빙엔 대학교 도서관(Universitätsbibliothek Tübingen)이 제공하는 세계 최대 규모의 신학 서지 데이터베이스 **Index Theologicus (IxTheo)**를 직접 연동하여, 사용자의 신학 주제에 맞는 유럽/독일어권 학술 데이터를 실시간으로 추출하고 검증하는 전문 서치 스킬이다.

## 2. Core Engine
이 스킬의 핵심 실행체는 **`scripts/ixtheo_searcher.py`**이다. 

### ⚙️ Usage
```bash
# 기본 키워드 검색 (JSON 결과 표준 출력)
python scripts/ixtheo_searcher.py --query "Amos 4:13"

# 검색 건수 한도 설정
python scripts/ixtheo_searcher.py --query "incarnation" --limit 10
```

## 3. Operations & Standards
- **2단계 하이브리드 검색**: 1차적으로 `OpenSearch` API를 이용하여 가볍고 빠르게 검색 목록을 확보한 뒤, 수집된 주요 논문들의 고유 식별자(DOI) 및 세부 권/호(Volume/Issue/Page) 검증을 위해 `SRU` API를 기동하여 MarcXML 포맷의 정밀 서지 정보를 상호 보완한다.
- **표준화된 출력**: 모든 결과물은 공통 서지 스키마(`title`, `authors`, `journal`, `year`, `volume`, `issue`, `doi`, `link`)로 정규화되어 JSON 형태로 출력된다.
