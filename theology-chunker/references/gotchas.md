# 📦 Theology Chunker: Gotchas & Anti-Patterns

신학 문서 청킹 및 DB 인입 시 에이전트가 주의해야 할 사항입니다.

## 1. Extraction Pitfalls (추출의 함정)
- **바이너리 스타일 오염**: PDF에서 텍스트를 추출할 때 유니코드 특수 문자나 깨진 글꼴 정보가 JSONL에 그대로 들어가지 않도록 필터링하십시오.
- **Footnote Confusion**: 본문과 각주(Footnote)가 섞여서 청킹되면 문맥이 파괴됩니다. 각주 번호와 본문을 분리하거나 의미 있게 연결하십시오.

## 2. Chunking Failures (청킹 실패)
- **Incoherent Fragments**: 문장의 중간에서 기계적으로 잘라버려 앞뒤 문맥을 알 수 없는 청크를 만들지 마십시오. (Contextual Chunking 준수)
- **Metadata Mismatch**: 페이지 번호나 권(Volume) 정보가 실제 문헌과 어긋나면 RAG 검색 시 출처 신뢰도가 0이 됩니다.

## 3. Archiving Errors (아카이빙 오류)
- **JSONL 문법 파손**: 대량의 데이터를 인입할 때 쉼표(`,`) 하나가 빠져서 전체 DB 파일이 파싱되지 않는 대참사를 방지하십시오.
- **Duplicate Ingestion**: 이미 인입된 파일을 중복으로 넣어 검색 결과에 노이즈를 만들지 마십시오.

---
*Created by MS_Dev Third Gen Standard*
