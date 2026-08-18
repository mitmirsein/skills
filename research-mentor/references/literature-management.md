# Research Mentor: Literature & Action Protocol

선정된 주제를 실제 연구 데이터로 연결하기 위한 실행 프로토콜입니다.

## 🔎 Research Action (Phase 5a)
사용자가 선행 연구 검색을 요청할 시 다음 작업을 수행합니다.
1. **Local Search**: `theology-local-searcher`를 통해 로컬 JSONL 아카이브 검색.
2. **Scholar Search**: `scholar-semantic`을 통해 글로벌 최신 논문 검색.
3. **Bib Inventory**: 검색된 양질의 자료를 `references/core_literature.jsonl`에 추가하여 세션의 영속성을 보장합니다.

## 📝 Outline Design (Phase 5b)
- `theology-writer`의 개요 설계 기능을 연쇄 호출합니다.
- SBL 포맷(서론-본론-결론)의 논리적 목차를 제안합니다.

## 🏛️ Deep Dive (Phase 5c)
- `theology-council`을 소집하여 성서, 역사, 조직, 실천신학의 다각적 관점을 통합한 종합 리포트를 제공합니다.

## 💾 Session Archival
세션 종료 시 `MS_Thoughts.nosync/010 Inbox/`에 `research_session_{date}.md` 형식으로 대화 내용을 자동 저장합니다.
