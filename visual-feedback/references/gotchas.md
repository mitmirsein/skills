# 👁️ Visual Feedback: Gotchas & Anti-Patterns

시각적 피드백 처리 및 소스 코드 매핑 시 에이전트가 주의해야 할 사항입니다.

## 1. Mapping Pitfalls (매핑의 함정)
- **Selector Over-reliance**: CSS 셀렉터(`div > p:nth-child(2)`)는 구조가 조금만 바뀌어도 깨집니다. 텍스트 내용이나 고유 ID를 함께 사용하여 매핑의 정확도를 높이십시오.
- **Wrong File Localization**: 비슷한 클래스명을 가진 다른 컴포넌트 파일을 수정하지 않도록, `grep` 검색 시 컨텍스트를 충분히 확인하십시오.

## 2. Sync Failures (동기화 실패)
- **Daemon Lag**: `agent-picker` 데몬의 정보가 실시간이 아닐 수 있습니다. 현재 브라우저에 표시된 화면과 소스 코드가 일치하는지 먼저 확인하십시오.
- **State Mismatch**: 사용자가 'Hover'나 'Click' 등으로 변화시킨 동적 상태의 UI를 정적 소스 코드의 기본값과 혼동하지 마십시오.

## 3. Action Errors (수행 오류)
- **Destructive Style Changes**: 특정 요소를 고치려다 전역 스타일(Global CSS)을 건드려 다른 페이지의 레이아웃을 망가뜨리지 마십시오.
- **Blind Refactoring**: 시각적 결과만 보고 내부 로직을 추측하여 리팩토링하지 마십시오. 실제 함수 구현부를 먼저 읽어야 합니다.

---
*Created by MS_Dev Third Gen Standard*
