# 🏛️ Technical Architect (Unified): Gotchas & Anti-Patterns

프로젝트 구조 설계, 정리 및 코드 리팩토링 수행 시 에이전트가 주의해야 할 사항입니다.

## 1. Structural Pitfalls (구조의 함정)
- **과잉 엔지니어링 (Over-engineering)**: 파일 5개짜리 작은 프로젝트에 복잡한 Monorepo나 Microservices 구조를 강제하지 마십시오. 규모에 맞는(Scalable but Simple) 구조를 지향하십시오.
- **Deep Nesting**: 폴더 깊이가 너무 깊어지면 경로 관리가 힘들어지고 개발 경험이 저하됩니다 (Max Depth 3~4 권장).
- **Hidden Dependencies**: 특정 폴더의 이름에 의존하는 스크립트(예: hardcoded path)가 있는지 전역 검색을 통해 확인 후 이동하십시오.

## 2. Refactoring & Logic Pitfalls (리팩토링 및 논리의 함정)
- **기능 변경 (Feature Creep)**: 리팩토링의 목적은 '구조 개선'이지 '기능 추가'가 아닙니다. 코드를 다듬다가 새로운 기능을 슬쩍 끼워넣지 마십시오.
- **추상화 중독 (Abstraction Abuse)**: 모든 중복을 제거하려고 너무 복잡한 인터페이스나 제네릭을 도입하지 마십시오. 때로는 '약간의 중복'이 '나쁜 추상화'보다 낫습니다.
- **Side Effects 간과**: 전역 변수나 싱글톤 객체를 건드릴 때 발생하는 부수 효과를 철저히 계산하십시오.
- **Edge Case 유실**: 간결한 코드를 위해 복잡한 조건문을 단순화하다가 특수한 경우(Null, Empty list 등)의 처리를 누락하지 마십시오.

## 3. Hygiene & Implementation Failures (위생 및 구현 실패)
- **무분별한 삭제**: '임시 파일'처럼 보여도 중요한 데이터일 수 있습니다. 삭제 전 반드시 파일 내용을 미리보기(View)하고 대장의 승인을 받으십시오.
- **Broken Paths**: 파일을 이동시킨 후 해당 파일을 참조하던 `import` 경로들을 업데이트하지 않으면 전체 시스템이 붕괴됩니다.
- **Backup/TDD 누락**: 대규모 재편 전에는 `git commit`이나 임시 백업을 생성하고, 테스트 코드가 없는 상태에서 리팩토링하지 마십시오. 반드시 `tech-tdd` 등과 연계하여 기존 기능 보존을 확인하십시오.
- **가독성 저하**: "한 줄 코딩"이나 "천재적인 기법"을 쓴답시고 동료가 읽기 힘든 암호같은 코드를 만들지 마십시오.

---
*Unified Architect & Refactorer by MS_Dev Third Gen Standard*
