# 📚 ARC Librarian: Gotchas & Anti-Patterns

노트 규격화 및 ARC 분류 시 에이전트가 주의해야 할 사항입니다.

## 1. Categorization Pitfalls (분류의 함정)
- **모호한 분류 (Loose Mapping)**: 내용이 조금이라도 신학적이라 해서 무조건 100(Theology)으로 몰아넣지 마십시오. 개인적 묵상은 200(Ministry), 학술적 연구는 100으로 정교하게 구분하십시오.
- **Top-heavy 태그**: 너무 많은 태그를 달아 지식 그래프를 어지럽히지 마십시오. 핵심 키워드 3~5개면 충분합니다.

## 2. Metadata Failures (메타데이터 실패)
- **기존 데이터 유실**: 사용자가 직접 작성한 소중한 프론트매터 필드를 무시하고 덮어쓰지 마십시오. 기존 필드는 보존(Preserve)하며 표준 필드만 추가하거나 업데이트하십시오.
- **잘못된 날짜 형식**: 반드시 `YYYY-MM-DD` 형식을 엄수하십시오.

## 3. Link Discovery Errors (링크 탐색 오류)
- **환상적 링크 (Hallucinated Links)**: 존재하지 않는 파일명을 `[[Link]]` 형식으로 연결하지 마십시오. 반드시 `list_dir`이나 `grep_search`로 실존 여부를 확인한 후 연결하십시오.

---
*Created by MS_Dev Third Gen Standard*
