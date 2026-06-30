# Phase 1-2 — Generic Fetch Chain 상세 (정본)

> `python3 -m engine <URL>` / `from engine import fetch` 내부 동작과 격자·폴백·수동 개입 규격.

## 내부 단계 (디버깅용 노출)

`fetch()`는 단일 API이지만 내부는 phase로 나뉘어 있다. `result.trace`에서 각 시도를 확인할 수 있다.

```
probe      — curl_cffi + safari + self-referer로 첫 시도
validate   — 4-계층 검증 (marker / size / cookie / success_selectors)
detect     — WAF 제품 감지 ([(profile_id, confidence)] 랭킹)
plan       — 프로파일의 tls_candidates × url_transforms × referer 격자 구성
execute    — 격자 전수 시도 (첫 200에서 탈출하지 않음)
fallback   — capability 태그 기반 Playwright 라우팅 (MCP or local+chrome)
report     — FetchResult(ok, verdict, profile_used, trace, summary)
```

## 검증 원칙 (4-계층 AND)

- HTTP 200은 **검사 시작 조건**이지 성공이 아니다.
1. 챌린지 마커 없음 (`sec-if-cpt-container`, `Access Denied`, `Just a moment...`, `DataDome`)
2. 비정상 크기 아님 (< 3KB 또는 WAF fingerprint 크기)
3. 쿠키 센서 상태 정상 (`_abck=~-1~` 아님)
4. `success_selectors` 중 하나 이상 매칭 (caller 제공 시 → `strong_ok`, 미제공 시 → `weak_ok`)

## 격자 축 (profile이 우선순위 추천, 격자는 전수 시도)

| 축 | 값 | 비고 |
|----|-----|------|
| `url_transforms` | `original`, `mobile_subdomain` (`www.→m.`), `am_prefix`, `drop_www` | 사이트명 없음, 규칙만 |
| `tls_impersonate` | `safari`, `safari_ios`, `chrome99`, `chrome119`, `chrome131`, `chrome_android`, `firefox`... | 프로파일별 avoid 리스트 존재 |
| `referer_strategy` | `self_root`, `google_search`, `none` | |

**device_class**:
- `"auto"` (기본) — 프로파일 전략 따름
- `"desktop"` — TLS 데스크톱만 + `mobile_subdomain` 비활성
- `"mobile"` — TLS 모바일만 + `mobile_subdomain` 활성

## Playwright 폴백 (capability-matched)

`engine/executor.py`가 프로파일의 `capabilities_needed`를 읽고 실행기를 자동 선택:

| 태그 | 실행기 | 언제 |
|------|--------|------|
| `needs_real_tls_stack` + `needs_js_exec` | `playwright_real_chrome.js` (로컬 Node) | Akamai Bot Manager 등 — Chromium 번들 TLS는 탐지됨 |
| `needs_js_exec` only | Playwright MCP (`mcp__playwright__*`) | Cloudflare 기본 방어 등 |
| `needs_mobile_context` (+ real_tls) | `playwright_mobile_chrome.js` | 모바일 디바이스 에뮬레이션 필요 |

자세한 선택 기준: [playwright.md](playwright.md).

### Playwright MCP 호출 규칙

`fetch_chain`의 `needs_js_exec only` 케이스는 **Claude 세션에서 MCP 도구를 직접 호출**해야 한다. subprocess 경로 없음. 즉:
1. `result.summary`에 "Playwright MCP must be invoked from the Claude session"이 포함되면
2. `mcp__playwright__browser_navigate` → `browser_wait_for` → `browser_snapshot` 흐름으로 Claude가 직접 처리

## Phase 2 — 수동 개입 (옵션)

Phase 1이 `ok=False`를 반환하면 사용자 힌트를 받아 재시도:

```python
result = fetch(
    url,
    success_selectors=[...],
    user_hint={"impersonate_first": "safari_ios", "referer_strategy": "none"},
)
```

힌트는 **현재 호출 1회에만** 적용되며 저장되지 않는다.

## R7 보충 — 왜 API-first 병행 분기인가

SPA + WAF 사이트(쇼핑몰·커머스 다수)는 마케팅 페이지(HTML)만 WAF로 중투자하고 내부 API는
gateway 레벨 기본 방어만 쓰는 경우가 많다. HTML 격자 전수 낭비(50회 × 0.5s + Playwright
fallback 40s ≈ 65초)보다 **MCP 정찰 1회(5~10초) + API 재호출(0.5초)**가 훨씬 경제적이고
성공률 높다.

**MCP 정찰 루트 상세**:
1. `mcp__playwright__browser_navigate` → 대상 페이지 로드 (브라우저 렌더링)
2. `mcp__playwright__browser_network_requests` → XHR/fetch 호출 목록 수집, `/api/`·`/graphql`·`\.json` 필터로 내부 엔드포인트 식별
3. 식별된 JSON API URL을 `python3 -m engine <API_URL>`로 재호출 (백그라운드 engine과는 별개 호출). 대부분 API 레이어는 페이지 HTML보다 WAF 보호가 얕아 curl_cffi로 바로 수집됨
4. 응답 스키마 파악 후 pagination / query parameter 조합해 반복 수집

**"병렬"의 실행 의미** (Claude 도구 호출이 순차이므로 명확화):
- engine은 `run_in_background=true`로 Bash 툴에서 띄워둔다 — 격자는 그대로 돌되 블로킹하지 않음
- Claude는 그 사이 foreground에서 MCP Playwright 정찰 루트를 진행
- engine이 먼저 성공해도 좋고, MCP 정찰로 얻은 API가 먼저 성공해도 좋음. 빠른 쪽 결과 채택

**R7 편향 방지**: 내부 API URL·파라미터는 `engine/**`에 하드코딩 금지. 탐지된 URL은 런타임 호출에만 쓰고 저장소에 고정하지 않는다.
