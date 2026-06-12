# 🕵️‍♂️ Stealth Browser: Gotchas & Anti-Patterns

스텔스 브라우징 및 자동화 수행 시 에이전트가 주의해야 할 사항입니다.

## 1. Interaction Pitfalls (상호작용의 함정)
- **비정상적 속도**: 인간이 할 수 없는 속도로 클릭이나 타이핑을 수행하여 봇 탐지 시스템(Cloudflare 등)을 자극하지 마십시오. 적절한 `delay`와 `jitter`를 사용하십시오.
- **Selector Fragility**: 웹사이트의 구조는 수시로 변경됩니다. 깨지기 쉬운 절대 경로(XPath) 대신, 텍스트나 의미론적 식별자를 사용하십시오.

## 2. Identity Failures (신원 실패)
- **세션 오염**: 하나의 프로필로 여러 사이트를 동시에 넘나들며 추적 가능한 패턴을 남기지 마십시오. 목적에 맞는 프로필 격리(Isolation)를 준수하십시오.
- **로그인 상태 오판**: 실제 Chrome 프로필을 가져왔더라도 세션이 만료되었을 수 있습니다. 작업을 시작하기 전 '로그인 필요' 화면인지 먼저 확인하십시오.

## 3. Engine Errors (엔진 오류)
- **리소스 과다**: 병렬 군집(Swarm) 모드 사용 시 시스템의 CPU/RAM 상태를 고려하십시오. 너무 많은 브라우저 창을 띄우면 시스템 전체가 멈출 수 있습니다.
- **Headless Detection**: 일부 사이트는 Headless 모드를 감지합니다. 필요에 따라 `headless: false` 또는 `stealth-plugin`을 활성화하십시오.

---
*Created by MS_Dev Third Gen Standard*
