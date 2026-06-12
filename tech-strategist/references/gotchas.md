# ♟️ Tech Strategist (Unified): Gotchas & Anti-Patterns

기획 의도 재정의와 외부 저장소 정찰 및 지능 이식 시 에이전트가 주의해야 할 사항입니다.

## 1. Strategic & Planning Pitfalls (기획의 함정)
- **해결하려는 '특정 고통'을 놓치지 마세요**: "사용자를 위한 달력 앱"보다는 "계정이 엉킨 사용자의 개인 비서"처럼 대상의 구체적인 고통이 특정되어야 합니다.
- **"Narrowest Wedge"를 반드시 명시하세요**: 당장 내일 보여줄 수 있는 '가장 작고 날카로운 조각(MVP)'이 무엇인지 정의하지 못하면 기획 실패입니다.
- **Complexity is the Enemy of Taste**: 핵심 가치 하나를 위해 나머지 9개를 쳐내십시오. 1년 뒤에 봐도 명쾌한 설계를 지향하십시오.
- **"Boil the Lake" (완결성)**: 10가지 기능을 대충 50%씩 구현하지 말고, 1가지라도 100% 테스트와 예외 처리가 끝난 상태로 배포하십시오.

## 2. Infiltration & Scouting Pitfalls (정찰 및 정찰의 함정)
- **Blind Cloning**: 저장소 크기나 신뢰도를 확인하지 않고 무분별하게 클론하여 자원을 낭비하거나 보안 리스크를 초래하지 마십시오.
- **Dependency Hell**: 외부의 복잡한 패키지 의존성이 필요한 도구를 우리 시스템 환경(uv)을 고려하지 않고 무리하게 이식하려 하지 마십시오.
- **껍데기 정찰**: 파일 목록만 보고 '고가치 자산'이라 판단하지 마십시오. 파일 내용을 읽어보고(View) 우리 시스템 규격(RISE/ARC)에 맞게 변용 가능한지 깊이 있게 분석하십시오.

## 3. Implementation & Looting Failures (구현 및 이식의 함정)
- **흔적 유실**: 정찰한 저장소의 출처(URL, Author) 정보를 기록하지 않아 나중에 참고할 수 없게 되는 상황을 방지하십시오.
- **Loot Overload**: 너무 많은 정보를 가져오려다 정작 중요한 '핵심 통찰(Tactical Instinct)'을 놓치지 마십시오.
- **Clean-up 실패**: 정찰이 끝난 후 임시로 클론했던 폴더를 즉시 삭제하여 작업 공간을 어지럽히지 마십시오.

---
*Unified Strategist & Scout by MS_Dev Third Gen Standard*
