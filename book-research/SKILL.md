---
name: book-research
description: >
  Compares evidence-backed claims from multiple book skills and produces a
  source-traceable research packet. Use when the user asks to compare authors,
  synthesize books, verify a claim against locators, or find counterarguments.
  키워드: 도서 비교 연구, 저자별 주장 비교, 근거 추적, 반론 검색, 연구 패킷
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "/book-research"
capabilities:
  - evidence_backed_claim_retrieval
  - cross_book_comparison
  - counterargument_search
references_path: ./references
---

# book-research

여러 도서 스킬의 근거 연결 claim을 질의별로 비교하고, 저자 진술과 연구자의 종합을 분리함.

## Phase 0 — 가드레일

- 시작 전 [gotchas.md](references/gotchas.md)를 읽음.
- `book-index.json`과 `claim-index.json`은 책별 정본이며, `claim-catalog.json`은 재생성 가능한 파생 파일임.
- `generated` claim을 확정 근거로 쓰지 않음. 최소 `source-checked`를 기본 기준으로 삼음.
- 태그의 일치만으로 저자 간 찬성·영향·비판 관계를 단정하지 않음.

## Phase 1 — 질문을 검색 축으로 변환

질문에서 다음 축을 분리함: 개념·성경 본문·locus·인물·시대·방법·저자 범위. 모호한 질문은 가장 적은 축으로 먼저 검색하고, 선택한 해석 범위를 결과에 명시함.

관련 장을 찾을 때는 기존 book catalog를, claim을 찾을 때는 claim catalog를 사용함. converter 저장소는 사용자명 없는 경로 또는 현재 작업공간에서 발견하고, 다음 형식으로 조회함.

```bash
python3 tools/query_claim_catalog.py \
  --catalog <books-root>/claim-catalog.json \
  --term "성육신" --scripture "John 1:14" \
  --verification source-checked --match all --limit 20 --format json
```

catalog 또는 claim index가 없으면 이를 숨기지 않고 기존 chapter catalog로 범위를 좁힌 뒤, 원문 재확인이 필요하다고 보고함.

## Phase 2 — 근거와 범위를 검증

1. 결과의 claim ID, attribution, chapter path, verification, evidence locator를 확인함.
2. 각 저자별로 직접 진술을 분리해 기록함.
3. 질문의 핵심 claim은 locator가 가리키는 원문 segment를 다시 읽음.
4. claim이 한 권만 나오면 횡단 종합이 불가능하다고 명시함. 관련성이 낮은 책을 수량 맞추기로 추가하지 않음.
5. `basis=inferred` 관계는 저자의 직접 관계가 아니라 연구 과정의 비교 연결로 표시함.

## Phase 3 — 비교와 counter-query

비교 축은 질문에 맞게 정하되, 최소한 논지·근거 본문·방법·범위/한계를 대조함. 같은 조건으로 반대 방향 용어, 인접 locus, 비판 유형을 한 번 더 조회해 침묵·긴장·반론을 찾음.

`quick`은 source-checked claim의 짧은 비교, `standard`는 관련 chapter 재독해와 비교 행렬, `deep`은 locator 재검증과 counter-query·미해결 질문까지 포함함.

## Phase 4 — Research Packet 작성

아래 순서를 유지하고, 저자의 주장과 종합을 섞지 않음.

```markdown
# Research Packet

## 질문과 범위
## 선택된 책과 선택 이유
## 저자별 핵심 주장
## 비교 행렬
## 일치점
## 긴장·반론·소수 의견
## 종합
## 종합 중 inferred인 연결
## 출처 locator
## 미해결 질문
```

각 종합 문장에는 사용한 claim ID를 연결하고, locator 재확인 여부와 `generated` 포함 여부를 밝혀야 함. 장문의 원문 인용을 축적하지 않음.

## 검증·보고

- 결과 claim의 source·chapter·locator가 실제 index에서 해석되는지 확인함.
- 최소 두 책 비교를 요청받았으나 근거가 한 책뿐이면 그 제한을 첫 문단에 보고함.
- inferred 연결, 반론 검색 결과, 미해결 질문을 별도 표기함.
- source-checked 비율과 검증하지 못한 locator를 간결히 보고함.
