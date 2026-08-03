# 증거와 Claim Ledger 정책

## 출처 등급

| 등급 | 일반 기준 | 예 |
|---|---|---|
| A | 직접성이 높고 엄격한 검토를 거친 1차·종합 근거 | 체계적 문헌고찰, 공식 법령·통계, 감사된 공시 |
| B | 신뢰할 수 있는 원자료 또는 전문기관 자료 | 피어리뷰 원논문, 표준, 공식 제품 문서 |
| C | 편집 책임이 있는 전문 2차 자료 | 주요 언론 분석, 전문기관 해설, 학회 발표 |
| D | 유용하지만 검토·이해관계 한계가 큰 자료 | 프리프린트, 기업 블로그, 보도자료 |
| E | 검증되지 않은 단서 | 포럼, 소셜 미디어, 익명 주장 |

등급은 분야에 맞게 적용한다. 법률은 현행 공식 법령, 의료는 최신 임상지침·체계적 근거, 제품 동작은 해당 버전 공식 문서가 직접성이 높다. E 등급은 발견 단서로만 사용하고 검증 근거로 세지 않는다.

## 독립 출처

독립성은 도메인 수가 아니라 정보 생산 계보로 판단한다. 다음은 하나의 `independence_group`으로 묶는다.

- 같은 보도자료를 전재한 기사
- 같은 연구나 데이터셋을 재인용한 보고서
- 같은 조직의 지역 사이트·자회사
- 원문을 확인하지 않은 요약 서비스

## 출처 레코드

`sources/sources.jsonl`은 한 줄에 하나의 JSON 객체를 둔다.

```json
{
  "id": "src_001",
  "url": "https://example.org/source",
  "title": "Source title",
  "author": "Author or organization",
  "published_at": "2026-01-31",
  "domain": "example.org",
  "source_type": "official",
  "quality_rating": "B",
  "primary": true,
  "independence_group": "example.org",
  "claims": ["직접 지지하는 내용"]
}
```

## Claim Ledger 레코드

`artifacts/claim_ledger.jsonl`은 핵심 주장만 기록한다.

```json
{
  "claim_id": "clm_001",
  "text": "검증할 핵심 주장",
  "risk": "high",
  "claim_type": "numeric",
  "source_ids": ["src_001", "src_002"],
  "counter_search": "반증 검색 결과와 사용한 쿼리",
  "counter_refuted": false,
  "conflicting": false
}
```

## 판정 규칙

- `refuted`: 신뢰할 만한 반증으로 주장이 기각됨.
- `unresolved`: 독립 근거가 두 개 미만, 출처 충돌, E 등급만 존재, 또는 고위험 주장에 1차 자료가 없음.
- `verified`: A–D 등급의 독립 근거가 두 개 이상이며, 고위험 주장은 반증 검색과 1차 자료까지 갖춤.
- 고위험 유형은 `numeric`, `legal`, `causal`, `medical`, `financial`, `regulatory`다.
- 반증 검색이 빠진 고위험 주장은 검증 스크립트의 프로세스 오류로 처리한다.

## 인용 규칙

- 보고서의 검증 가능한 사실에는 `[src_001]` 형식의 ID를 붙인다.
- 핵심 주장에는 감사 추적을 위해 `[clm_001]`도 붙인다.
- 참고문헌에는 저자·기관, 날짜, 제목, 직접 URL 또는 DOI를 제공한다.
- 긴 PDF나 책은 확인한 페이지를 기록한다.
- 인용이 문장을 부분적으로만 지지하면 문장의 강도를 낮추거나 미확정으로 이동한다.
