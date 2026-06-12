# React Components: Architectural Rules (Modular, Logic, Types)

Stitch 디자인을 유지보수가 용이하고 확장 가능한 리액트 컴포넌트로 변환하기 위한 아키텍처 원칙입니다.

## 🧱 Modular Architecture
- **Independence**: 거대한 하나의 파일(Monolithic)이 아닌, 의미론적으로 독립된 단위의 파일들로 분리합니다.
- **Hook Isolation**: 모든 비즈니스 로직과 이벤트 핸들러는 `src/hooks/` 하위의 커스텀 훅으로 격리하여 뷰(View)와 로직(Logic)을 분리합니다.

## 📦 Data Decoupling
- **Mock Data**: 모든 하드코딩된 텍스트, 이미지 URL, 리스트 데이터는 `src/data/mockData.ts`로 추출하여 중앙 집중식으로 관리합니다.

## 🛡️ Type Safety (TypeScript)
- **Props**: 모든 컴포넌트는 반드시 `Readonly` 속성이 적용된 `[ComponentName]Props` 인터페이스를 포함해야 합니다.
- **Consistency**: 테마별 Tailwind 설정(`tailwind.config`)을 파싱하여 스타일 일관성을 확보하고, `resources/style-guide.json`과 동기화합니다.

## 🧹 Optimization
- **Clean Code**: 구글 라이선스 헤더 등 불필요한 메타데이터를 제거하고 깔끔한 코드만 산출합니다.
- **Theme Focus**: 정적으로 하드코딩된 HEX 코드 대신 테마에 매핑된 Tailwind 유틸리티 클래스를 사용합니다.
