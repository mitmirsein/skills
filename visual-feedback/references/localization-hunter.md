# Visual Feedback: Localization & Selection Hunter

사용자의 시능적 피드백(CSS Selector, Text)을 바탕으로 실제 소스 코드 파일(Component)을 찾아내는 전략입니다.

## 🎯 The "Hunter" Strategy (Localization)

1. **Selector Parsing**: `agent-pickerd`가 제공하는 CSS 셀렉터를 소스 트리에서 `grep`합니다.
   - **Unique IDs**: `#hero`, `#cta-button` 등 유일한 ID가 포함된 경우 가장 높은 정확도로 검색 가능합니다.
   - **Tailwind/Modules**: 해시화된 클래스명 보다는 구조적 태그(`nav > ul > li`)와 속성(`data-name`)을 조합하여 검색 범위를 좁힙니다.

2. **Text-Content Search**: 셀렉터가 모호하거나 해시된 경우, 선택된 요소의 `text_content`를 기반으로 검색합니다.
   - `grep -rI "About Us" src/`
   - 주의: 공용 텍스트나 다국어 키값일 경우 여러 파일이 검색될 수 있으므로 셀렉터와 대조가 필요합니다.

3. **Hierarchy Traversal**: 선택된 노드를 포함하는 최상위 React/Vite 컴포넌트 파일을 특정합니다.
   - 선택된 요소의 부모 노드들을 거슬러 올라가며 컴포넌트 경계(Component Boundary)를 탐지합니다.

## 🔄 Interaction Protocol (Feedback Loop)
- **Acknowledge**: 픽커 정보를 확인한 뒤 즉시 사용자에게 "AboutUs.tsx의 2번째 항목을 수정하겠습니다"라고 보고합니다.
- **Set Status**: `agent-pickerd:set-agent-note`를 통해 실시간 처리 상태를 브라우저에 표시하여 신뢰를 확보합니다.
- **Fixed & Verify**: 작업 완료 후 상태를 `fixed`로 변경하고 사용자에게 눈으로 확인(Visual QA)할 것을 요청합니다.
