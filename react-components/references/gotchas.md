# ⚛️ Stitch to React Components: Gotchas & Anti-Patterns

Stitch 디자인 변환 및 리액트 컴포넌트 구현 시 에이전트가 주의해야 할 사항입니다.

## 1. Conversion Pitfalls (변환의 함정)
- **Hard-coded Data**: 디자인에 포함된 임시 텍스트를 컴포넌트에 직접 하드코딩하지 마십시오. 반드시 `mockData`나 `props`로 분리하여 데이터 주입이 가능한 구조를 만드십시오.
- **Inline Style 남용**: Stitch에서 가져온 스타일을 모두 인라인 스타일로 박지 마십시오. 공통 스타일은 CSS 변수나 테마 시스템으로 추상화하십시오.

## 2. Architecture Failures (아키텍처 실패)
- **비즈니스 로직 혼재**: 컴포넌트 파일 내부에 복잡한 데이터 처리(fetching, sorting) 로직을 넣지 마십시오. 반드시 커스텀 훅(`useXxx`)으로 격리하십시오.
- **Prop Drilling**: 컴포넌트 계층이 깊어질 때 props를 무분별하게 전달하지 마십시오. Context API나 상태 관리 라이브러리 사용을 검토하십시오.

## 3. Validation Errors (검증 오류)
- **Lint 무시**: `npm run validate` 결과로 나온 린트 에러를 무시하고 제출하지 마십시오. 코드 품질은 곧 시스템의 안정성입니다.
- **타입 정의 부재**: `any` 타입을 남용하여 TypeScript의 이점을 죽이지 마십시오. 인터페이스(Interface)를 명확히 정의하십시오.

---
*Created by MS_Dev Third Gen Standard*
