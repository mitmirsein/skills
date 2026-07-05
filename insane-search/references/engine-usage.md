# Engine 사용법 상세 (Phase 1/2 · 검증 · 격자 · 폴백 · 의존성 · 빠른 참조)

SKILL.md의 단일 진입점(`python3 -m engine <URL>` / `from engine import fetch`) 사용법 세부. 디버깅·튜닝·의존성 문제 시 읽는다.

## Phase 1 — Generic Fetch Chain

### 단일 진입점

```python
from engine import fetch

result = fetch(
    "https://example.com/path",
    success_selectors=["article", "[class*='product-card']"],  # 포지티브 프루프 (선택)
    device_class="auto",      # "auto" | "desktop" | "mobile"
    user_hint=None,           # {"referer_strategy": "self_root", "impersonate_first": "safari"}
    timeout=25,
)

if result.ok:
    print(result.verdict)     # strong_ok | weak_ok
    html = result.content     # raw fetched text for parsers/storage
    agent_text = result.to_untrusted_text()  # pass this to LLM/agent context
else:
    # Phase 2 수동 개입 (Playwright MCP) 필요 — result.trace로 원인 진단
    pass
```

### 내부 단계 (디버깅용 노출)

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

### 검증 원칙

- HTTP 200은 **검사 시작 조건**이지 성공이 아니다.
- 성공 판정은 **4-계층 AND**:
  1. 챌린지 마커 없음 (`sec-if-cpt-container`, `Access Denied`, `Just a moment...`, `DataDome`)
  2. 비정상 크기 아님 (< 3KB 또는 WAF fingerprint 크기)
  3. 쿠키 센서 상태 정상 (`_abck=~-1~` 아님)
  4. `success_selectors` 중 하나 이상 매칭 (caller 제공 시 → `strong_ok`, 미제공 시 → `weak_ok`)

### 격자 축 (profile이 우선순위 추천, 격자는 전수 시도)

| 축 | 값 | 비고 |
|----|-----|------|
| `url_transforms` | `original`, `mobile_subdomain` (`www.→m.`), `am_prefix`, `drop_www` | 사이트명 없음, 규칙만 |
| `tls_impersonate` | `safari`, `safari_ios`, `chrome99`, `chrome119`, `chrome131`, `chrome_android`, `firefox`... | 프로파일별 avoid 리스트 존재 |
| `referer_strategy` | `self_root`, `google_search`, `none` | |

**device_class**:
- `"auto"` (기본) — 프로파일 전략 따름
- `"desktop"` — TLS 데스크톱만 + `mobile_subdomain` 비활성
- `"mobile"` — TLS 모바일만 + `mobile_subdomain` 활성

### Playwright 폴백 (capability-matched)

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

## 의존성 자동 설치

최초 호출 시 필요 패키지를 자동 설치한다. **curl_cffi는 0.15.0 이상**을 요구한다 — 0.15부터
`impersonate="chrome"`이 최신 Chrome(146+) 지문으로 갱신되고(0.14는 chrome142에 고정), HTTP/3 지문과
SSRF-safe redirect 기본값이 추가됐다. 아래 가드는 **미설치뿐 아니라 0.15 미만이면 업그레이드**한다:
```bash
python3 -c "import curl_cffi,bs4,yaml; v=curl_cffi.__version__.split('.'); assert (int(v[0]),int(v[1]))>=(0,15)" 2>/dev/null \
  || pip install -U "curl_cffi>=0.15.0" beautifulsoup4 pyyaml -q
```

Playwright 로컬 경로 사용 시 Node가 필요. 로컬 의존성은 `engine/templates/`의 package.json으로 관리한다 (executor가 그 디렉토리를 cwd로 실행). **Patchright**는 Playwright drop-in 포크로, Cloudflare/DataDome이 감지하는 CDP `Runtime.enable` 누출을 막아준다 — 템플릿이 설치돼 있으면 최우선 사용하고, 없으면 playwright-extra+stealth → plain playwright로 폴백한다:
```bash
cd "${CLAUDE_PLUGIN_ROOT}/skills/insane-search/engine/templates" && npm install
npx patchright install chrome   # 시스템 Chrome 채널 (channel:'chrome' 사용)
```

## 빠른 참조 — Phase 0 명령어

> **먼저 이걸 기억하라: Reddit/X/YouTube는 이제 engine이 자동 처리한다.**
> `python3 -m engine "<URL>"` 하나면 Phase 0 라우터(`engine/phase0.py`)가 **격자보다 먼저** 공식 경로를 시도한다 —
> Reddit→`.rss`, X 트윗→`tweet-result`/oEmbed, X 프로필→syndication, YouTube→`yt-dlp`.
> 아래 수동 스니펫은 디버그/참조용이며 trace에 `phase=phase0`로 기록된다.
> (실측 주의: Reddit `.json`+모바일UA·`syndication-timeline`은 흔히 403/429라 plain `curl`은 신뢰 불가 — engine이 curl_cffi 지문으로 접근한다.)

```bash
# ★ 거의 모든 경우 이거면 됨 (Phase 0 자동 + 실패 시 격자→Playwright 에스컬레이션)
python3 -m engine "<URL>"

# 범용 웹 (Jina Reader — 일반 HTML만, WAF 사이트엔 무효)
curl -s "https://r.jina.ai/{URL}"

# yt-dlp — 1,858 사이트 미디어 메타데이터 / 자막
yt-dlp --dump-json "URL"
yt-dlp --write-sub --write-auto-sub --sub-lang "en,ko" --skip-download -o "/tmp/%(id)s" "URL"

# Reddit — .rss (curl_cffi 지문 필요; plain curl은 TLS로 403)
python3 -c "from curl_cffi import requests as r; print(r.get('https://www.reddit.com/r/{sub}/.rss', impersonate='safari').text[:2000])"

# X/Twitter — 개별 트윗(가장 안정적): tweet-result / oEmbed
python3 -c "from curl_cffi import requests as r; print(r.get('https://cdn.syndication.twimg.com/tweet-result?id={TWEET_ID}&token=a', impersonate='safari').text)"
# X 프로필 타임라인 (rate-limit 변동 — engine이 재시도) / 키워드: WebSearch(site:x.com {kw})→tweet-result
curl -sL "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"

# Hacker News
curl -sL "https://hacker-news.firebaseio.com/v0/topstories.json?limitToFirst=10&orderBy=%22%24key%22"
```

> 커버리지 회귀 점검: `python3 tests/coverage_battery.py` — 플랫폼별 전수 경로 pass/fail + 썩은 예시 자동 적발.
