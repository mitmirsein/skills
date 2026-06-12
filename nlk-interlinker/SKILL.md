---
name: nlk-interlinker
description: >
  Queries the National Library of Korea LOD SPARQL endpoint for a control
  number's owl:sameAs identifiers (VIAF/LoC/GND/BnF/DBpedia/NDL/ISNI/
  Wikidata) and injects them into a note's YAML frontmatter. No API key
  required. Use when the user asks to interlink a record with global
  authority identifiers — obtain a control number first via
  nlk-biblio-searcher. 키워드: 국립중앙도서관 LOD, 인터링킹, 전거 연계
triggers:
  - "국립중앙도서관 인터링킹"
  - "nlk-interlinker"
  - "LOD 링크 연계"
  - "국립중앙도서관 LOD"
version: 1.0.0
status: active
---

# 국립중앙도서관 인터링킹 LOD 스킬 (SPARQL)

국립중앙도서관 LOD SPARQL 엔드포인트(`https://lod.nl.go.kr/sparql`)를 직접 조회해 제어번호 기준 국내외 연계 식별자(LOD URI)를 수집하고 Obsidian 노트에 연동한다. **인증키가 필요 없다.**

> **전환 배경:** 기존 data.go.kr `InterlinkingInformationService` 게이트웨이는 기관 백엔드 장애로 무응답(타임아웃)이다. 동일 sameAs 데이터의 권위 원천인 LOD SPARQL로 전환했다.

> 이 스킬은 이름/제목 검색이 아니다. 먼저 제어번호(`controlNumber`)를 확보한 뒤 사용한다. 제어번호는 `lod.nl.go.kr/resource/{제어번호}` 리소스로 변환되어 조회된다(예: 저자 `KAC199600018`, 주제 `KSH…`, 서지 `CNTS-…`).

## 핵심 특징
- **시맨틱 연계 수집:** VIAF, 미국의회도서관(LoC), 독일국립도서관(GND/DNB), 프랑스국립도서관(BnF), 스페인국립도서관(BNE), DBpedia, 일본국립국회도서관(NDL), ISNI, IdRef, OCLC, Wikidata 등.
- **기관·식별자 자동 분류:** sameAs 대상 URI의 호스트로 기관명과 ID를 추출한다.
- **YAML 자동 인젝션:** `--file` 지정 시 노트의 `control_number`/`nlk_control_number`/`controlNumber`를 읽어 조회하고, `owl_same_as[]` 및 개별 식별자(`wikidata`/`lccn`/`dnb`/`bnf`/`viaf`/`isni`)를 프론트매터에 갱신·주입한다.

## 사용법
```bash
PY=~/Desktop/MS_Dev.nosync/.venv/bin/python

# 제어번호로 직접 조회
$PY .skills/nlk-interlinker/scripts/search.py KAC199600018 --output markdown
$PY .skills/nlk-interlinker/scripts/search.py --control-number KAC199600018 --output json

# 마크다운 노트 YAML에 LOD 식별자 자동 주입
$PY .skills/nlk-interlinker/scripts/search.py --file "/path/to/vault/notes/Karl_Barth.md"
```

## Output Contract
각 연계 항목: `institution`(기관명), `id`(식별자), `target_uri`(연계 URI), `source_uri`(NLK 리소스), `datatype`(기관 코드).

## 한계
- 제어번호에 sameAs가 없으면 빈 결과다. 외부 연계는 주로 전거(저자 KAC·주제 KSH) 자원에 풍부하고, 일반 서지(CNTS)엔 적을 수 있다.
- 제어번호 확보는 `nlk-biblio-searcher`(서지검색) 또는 `nlk-subject-searcher`(KSH)에서 한다.
