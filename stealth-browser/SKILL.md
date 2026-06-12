---
name: stealth-browser
description: >
  Playwright browser automation with isolated local profiles and optional
  CDP providers — targeted browsing, extraction, and interaction where a
  real browser session is required. Use when the user asks for stealth
  browsing or when insane-search's engine escalates to a manual browser
  session. 키워드: 스텔스 브라우징, 브라우저 자동화, CDP
version: 3.1.1
author: MS_Dev
triggers:
  - "#stealth"
  - "#브라우징"
  - "/stealth [url]"
  - "/stealth-parallel [urls]"
capabilities:
  - playwright_browser_automation
  - local_profile_isolation
  - optional_cdp_provider_connection
  - parallel_web_automation
  - text_extraction
  - stealth_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# Stealth Browser

## 1. Overview
Playwright 기반 브라우저 자동화 헬퍼입니다. 로컬 격리 프로필을 사용하고, 필요할 때 Lightpanda/Browserbase/Kernel 같은 CDP provider에 연결합니다.

## 2. Dynamic Workflow
본 브라우징 전 **세션 함정(Gotchas)**과 **엔진 세팅(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: 현재 타겟 사이트의 봇 탐지 정책과 로그인 요구 여부를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 비정상적 속도 및 세션 오염을 방지합니다.

### Phase 1: Browser Session
`agents/stealth_browser.py`로 로컬 격리 프로필 또는 CDP provider 세션을 시작합니다.

### Phase 2: Parallel Sessions
여러 브라우저를 동시에 구동하여 대규모 작업을 병렬 처리합니다. 명령어 옵션은 [cli-usage.md](./references/cli-usage.md)를 참조하십시오.

### Phase 3: Extraction & Reporting
웹 데이터를 확보하고 결과를 정제하여 보고합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 봇 탐지 회피 전략 및 프로필 격리 가이드.
- [cli-usage.md](./references/cli-usage.md): `/stealth`, `/stealth-parallel` 명령어 및 운영 수칙.

---
*Updated by MS_Dev — legacy extension bridge removed*
