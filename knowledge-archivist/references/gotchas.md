# 📚 Knowledge Archivist: Gotchas & Anti-Patterns

웹 자료 수집 및 지식 아카이빙 시 에이전트가 주의해야 할 사항입니다.

## 1. Archival Pitfalls (아카이빙의 함정)
- **분류의 게으름**: 모든 파일을 `000 System`이나 `010 Inbox`에 방치하지 마십시오. 아카이브의 핵심은 '흐름'과 '배치'입니다.
- **중복 문서 방치**: 동일한 내용의 URL이 이미 아카이브에 존재하는지 `grep`으로 확인하십시오. 중복 저장은 지식의 가독성을 떨어뜨립니다.

## 2. Formatting Failures (포맷팅 실패)
- **Defuddle 오용**: 웹 페이지의 광고, 메뉴, 댓글 등이 본문에 포함되지 않도록 `jina_reader`나 `defuddle` 엔진을 적절히 조절하십시오.
- **Frontmatter 유실**: 아카이빙된 마크다운 파일에 필수 메타데이터(source, created, tags)가 누락되면 나중에 검색이 불가능해집니다.

## 3. Zettelkasten Errors (제텔카스텐 오류)
- **고립된 노트 (Orphan Notes)**: 다른 노트와의 연결(`[[Link]]`)이 전혀 없는 섬 같은 노트를 만들지 마십시오. 최소한 하나의 상위 폴더나 관련 주제와 연결하십시오.
- **너무 긴 제목**: 파일명에 너무 많은 정보를 담으려 하지 마십시오. 제목은 명료해야 합니다.

---
*Created by MS_Dev Third Gen Standard*
