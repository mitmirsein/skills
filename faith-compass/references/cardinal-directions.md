# Faith Compass: Cardinal Directions & Core Questions

신앙의 나침반이 탐험하는 네 가지 본질적 방향과 질문의 지도입니다.

## 🗺️ The Map of Truth
- **북 (NORTH): 계시 — 성경, 교리, 고백**
  - 핵심 질문: "신앙은 무엇을 **고백**하는가?"
  - 소스: 성경 본문, 신조, 교리적 정의.
- **동 (EAST): 전통 — 역사, 교부, 공의회**
  - 핵심 질문: "역사와 세계는 무엇을 **가르쳤**는가?"
  - 소스: 교회사, 성인들의 전승, 신학 사조의 변천.
- **서 (WEST): 이성 — 철학, 변증, 논리**
  - 핵심 질문: "논리는 무엇을 **묻고 설명**하는가?"
  - 소스: 신학적 변증론, 관련 철학적 질문, 현대 과학/논리와의 상호작용.
- **남 (SOUTH): 삶 — 윤리, 실천, 성화**
  - 핵심 질문: "이것은 어떤 **성품을 빚어내**는가?"
  - 소스: 그리스도인의 실천, 윤리적 판단, 영성 형성 및 공동체적 영향.

## ⚙️ Navigation State Machine
에이전트는 다음 상태를 내부적으로 추적해야 합니다.
- `Current_Phase`: Phase 0 (Calibration) ~ Phase 5 (Center).
- `Current_Direction`: 현재 탐험 방향 (N, E, W, S, CENTER).
- `Context_Mode`: 탐험의 톤 (Academic, Pastoral, Homiletic, Contemplative).
- `Explored`: 각 방향의 탐험 완료 여부.
