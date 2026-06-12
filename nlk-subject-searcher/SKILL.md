---
name: nlk-subject-searcher
description: >
  Expands a subject term through the National Library of Korea LOD SPARQL —
  preferred/non-preferred terms, broader/narrower terms, and definitions
  from KSH (subject headings) and KDC (decimal classification). No API key
  required. Use when the user wants controlled-vocabulary expansion before
  an NLK/KCI search or theology/humanities query broadening.
  키워드: 주제어 확장, 통제어휘, KSH, KDC
version: 1.0.1
status: active
---

# 국립중앙도서관 주제 검색 스킬 (LOD SPARQL)

국립중앙도서관 LOD SPARQL 엔드포인트(`https://lod.nl.go.kr/sparql`)를 직접 조회해 주제어의 SKOS 관계를 확장한다. **인증키가 필요 없다.**

> **전환 배경:** 기존 data.go.kr `SubjectInformationService` 게이트웨이는 기관 백엔드 장애로 무응답(타임아웃) 상태다. 동일 NLSH/SKOS 데이터의 권위 원천인 LOD SPARQL로 전환했다.

## 두 개의 주제 어휘를 함께 검색
- **KSH(주제명표목표)** — 진짜 주제 시소러스. 우선어·비우선어(영문 포함)·상위어·하위어 제공. 예: `구원론[救援論]` → 하위어 `보편 구원론[普遍救援論]`(비우선어 `universalism`).
- **KDC(한국십진분류)** — 분류 표목을 SKOS로 표현. 상위/하위 분류 + 범위주기(정의, 상호참조 `→231.6`) 제공. 분류 표목명에 한해 매칭.

## 매칭 방식 (중요)
- **KSH**: 라벨이 `삼위일체[三位一體]`처럼 한자 병기·공백을 포함하므로 **부분일치(CONTAINS)** 로 검색한다(주제명 스킴에 한정해 빠름).
- **KDC**: 분류 표목명 **정확매칭**(`prefLabel`). 분류명이 아닌 일반 개념어는 KDC에선 안 잡히고 KSH에서 잡힌다.
- 검색어가 짧을수록 후보가 많아진다. 정확한 표제어를 권장한다.

## Quick Start
```bash
PY=~/Desktop/MS_Dev.nosync/.venv/bin/python
$PY .skills/nlk-subject-searcher/scripts/search.py "종말론" --output markdown
$PY .skills/nlk-subject-searcher/scripts/search.py "구원론" --limit 5 --output json
$PY .skills/nlk-subject-searcher/scripts/search.py "삼위일체" --output markdown
```

## Output Contract
각 결과는 다음 필드로 정규화된다(기존 계약 유지).
- `source`: `KSH` | `KDC`
- `preferred_label`: 우선어
- `alt_labels[]`: 비우선어(동의어, 영문 포함)
- `broader[]` / `narrower[]` / `related[]`: 상위어 / 하위어 / 관련어(라벨)
- `scope_note`: 정의·범위주기(KDC 상호참조 포함)
- `notation`: KDC 분류기호 (KSH는 빈 값)
- `uri`, `id`, `same_as`

## 한계
- `related`(연관어, RT)는 KDC엔 거의 없다(분류체계 특성). KSH엔 일부 존재.
- 라벨에 한자 병기·공백·외국어가 섞여 있을 수 있다(LOD 원본 포맷). 스크립트가 꼬리 아티팩트(`~`, 정렬접두 `N-`, 외국어 lang 꼬리)를 정리하지만 완벽하진 않다.
- KSH 개념은 `nlon:isSubjectOf`로 해당 주제의 서지 제어번호(CNTS-…)와 연결된다 → `nlk-interlinker`/서지 파이프라인의 잠재 브리지(현재 미노출).

## Workflow
1. 질의어를 `scripts/search.py`로 조회한다.
2. `preferred_label`·`alt_labels`·`broader`·`narrower`로 검색어를 확장한다.
3. 확장어를 `kci-api-searcher`, `nlk-biblio-searcher`, `theology-research` 쿼리로 넘긴다.
4. 자료가 특정되면 `nlk-interlinker`로 외부 식별자를 보강한다.
