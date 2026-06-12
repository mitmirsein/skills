# 🔎 Theology Searcher: Gotchas & Anti-Patterns

신학 아카이브 검색 및 답변 생성 수행 시 에이전트가 주의해야 할 사항입니다.

## 1. Search Pitfalls (검색의 함정)
- **Keyword Isolation**: 한국어 쿼리만 사용하여 검색하지 마십시오. 신학적 개념은 원어(독/영/희/히)로 검색할 때 훨씬 정밀한 결과를 얻을 수 있습니다.
- **Grep Exhaustion**: 너무 넓은 범위에 대해 `grep`을 남발하여 검색 속도를 저하시키지 마십시오. 적절한 티어(Tier)와 디렉토리 범위를 설정하십시오.

## 2. Verification Failures (검증 실패)
- **Context Loss**: 검색된 짧은 청크(Chunk) 하나만 보고 전체 문맥을 오해하지 마십시오. 앞뒤 페이지를 확인하거나 `theology-chunker`의 메타데이터를 신뢰하십시오.
- **Citation Hallucination**: {abbr}, {volume}, {vage} 인용 정보를 임의로 지어내지 마십시오. 검색 결과에 포함된 데이터만 사용하십시오.

## 3. Logical Errors (논리 오류)
- **RDLO 위반**: 검색된 자료가 대장의 질문에 대한 직접적인 근거(Direct Logic)가 되는지 엄격히 따지십시오. '비슷한 주제'라고 해서 '답변의 근거'가 되는 것은 아닙니다.
- **Over-synthesis**: 자료가 부족함에도 불구하고 마치 완벽한 답변인 것처럼 '지어낸 논리'를 섞지 마십시오. 모르면 모른다고 하거나 추가 검색을 제안하십시오.

---
*Created by MS_Dev Third Gen Standard*
