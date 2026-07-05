# references/ 읽기 가이드 + Phase 0 공식 API 인덱스

이 문서는 **참조 파일 선택 가이드**다. 문제가 생겼을 때 어떤 `references/*.md`를 열어야 할지 결정하는 기준으로 쓴다. Claude는 필요할 때만 해당 파일을 `Read`하고, 선제적으로 전부 읽지 않는다.

## Phase 0 — 플랫폼 공식 API 인덱스

> 플랫폼이 **공식 공개한** 전용 API/CLI만 여기에 둔다. 이건 편향이 아니라 합의된 엔드포인트 사용이다.
> **그 외 모든 사이트는 Phase 1(generic fetch chain)이 자동 처리한다.** `python3 -m engine <URL>` 하나면 phase0 라우터가 격자보다 먼저 아래 경로를 시도한다.

### 소셜/커뮤니티 전용 API

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| X/Twitter | syndication (타임라인) + oEmbed (개별 트윗) + 키워드 검색: WebSearch → oEmbed | [twitter.md](twitter.md) |
| Reddit | Atom/RSS 피드(`.rss`) — 비인증 `.json`은 WAF 차단(403), score·댓글수는 OAuth | [json-api.md](json-api.md) |
| Bluesky | AT Protocol (`public.api.bsky.app/xrpc/...`) | [public-api.md](public-api.md) |
| Mastodon | 인스턴스별 공개 API | [public-api.md](public-api.md) |
| Hacker News | Firebase API + Algolia Search | [json-api.md](json-api.md) |
| Stack Overflow | SE API v2.3 | [public-api.md](public-api.md) |
| Lobste.rs / V2EX / dev.to | 공개 JSON API | [json-api.md](json-api.md) |

### 미디어 (CLI 도구 필수)

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| YouTube/Vimeo/Twitch/TikTok/SoundCloud 등 1,858개 | `yt-dlp --dump-json` | [media.md](media.md) |

### 학술/레지스트리

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| arXiv | Atom API | [public-api.md](public-api.md) |
| CrossRef | REST API | [public-api.md](public-api.md) |
| Wikipedia | REST API | [json-api.md](json-api.md) |
| OpenLibrary | JSON API | [public-api.md](public-api.md) |
| GitHub | gh CLI / REST API | [public-api.md](public-api.md) |
| npm / PyPI | Registry API | [json-api.md](json-api.md) |
| Wayback Machine | CDX API | [public-api.md](public-api.md) |

### 한국 전용 공식 API

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| 네이버 검색 | `search.naver.com` (통합/블로그/뉴스탭) | [naver.md](naver.md) |
| 네이버 금융 시세 | `api.finance.naver.com/siseJson.naver` (비공식 JSON) | [naver.md](naver.md) |

## A. Engine 확장·진단 (하네스 내부)

| 파일 | 언제 읽는가 | 무엇을 다루는가 |
|------|-------------|-----------------|
| [tls-impersonate.md](tls-impersonate.md) | curl_cffi 격자가 전부 `challenge`/`blocked`로 끝날 때, 새 impersonate 타겟을 `waf_profiles.yaml`에 추가할 때 | curl_cffi로 Safari/Chrome/Firefox TLS(JA3/JA4) 지문 복제하는 방법, WAF(Akamai/Cloudflare/F5 등)별 최적 타겟 조합, 임퍼소네이션 타겟 버전 목록, `tls_impersonate_avoid`의 실증 근거 |
| [playwright.md](playwright.md) | engine이 Playwright fallback으로 넘어가는데 MCP/Local Chrome 중 어디로 갈지 확인 필요할 때 | Approach 1 (`mcp__playwright__*` — Cloudflare급 챌린지), Approach 2 (Local Node + `channel:'chrome'` + stealth — Akamai Bot Manager급), 템플릿 파라미터 규격 |
| [fallback.md](fallback.md) | `verdict`가 애매하거나 Phase 전환 타이밍 결정 필요할 때 | engine의 Phase 0→1→2→3 에스컬레이션 원칙, 응답 성공/실패 판정 기준 세부, 각 Phase 종료 조건 |
| [metadata.md](metadata.md) | 본문 전체를 못 가져왔지만 제목·요약·가격·저자 같은 핵심만이라도 필요할 때 | OGP 메타 태그, JSON-LD (Schema.org), Twitter Card 파싱, 구조화 데이터 추출 패턴 |

## B. 경량 대안 (engine 말고 다른 도구가 나은 상황)

| 파일 | 언제 읽는가 | 무엇을 다루는가 |
|------|-------------|-----------------|
| [jina.md](jina.md) | WAF 없는 일반 웹(블로그·뉴스·Wiki)의 깨끗한 마크다운 추출 필요할 때 | `r.jina.ai/URL` 한 줄로 Puppeteer 기반 JS SPA 렌더링, 마크다운 변환, 무료 500 RPM, API 키 불필요 |
| [cache-archive.md](cache-archive.md) | 원본 사이트가 차단됐지만 과거 스냅샷으로라도 접근 필요할 때 | Wayback Machine CDX API, archive.today, AMP Cache (Google Cache는 2024-07 종료됨) |
| [rss.md](rss.md) | 뉴스·블로그·커뮤니티의 시계열 업데이트를 구조화해 받고 싶을 때 | RSS/Atom 자동 발견, 피드 파싱, 인증 불필요 — 가장 깔끔한 시계열 데이터 소스 |

## C. 플랫폼별 공식/공개 API (Phase 0 인덱스와 연결)

| 파일 | 언제 읽는가 | 무엇을 다루는가 |
|------|-------------|-----------------|
| [json-api.md](json-api.md) | Reddit/Wikipedia/HN/npm/PyPI 등 **URL 변형만으로** JSON/피드를 주는 사이트 | Reddit Atom/RSS(`.rss`) 대체 경로 + score·댓글용 OAuth(`.json`은 WAF 차단), HN Firebase, Algolia Search, Wikipedia REST, npm/PyPI Registry API |
| [public-api.md](public-api.md) | Bluesky/Mastodon/arXiv/Stack Overflow/CrossRef/GitHub/OpenLibrary/Wayback 공식 API 사용 시 | 인증 없이 쓰는 공식 공개 REST/AT/Atom API 엔드포인트, 요청 형식, 공통 파라미터 |
| [twitter.md](twitter.md) | X/Twitter 접근 — 프로필 타임라인, 특정 트윗, 키워드 검색 | `syndication.twitter.com` 타임라인, oEmbed 개별 트윗, 검색은 WebSearch로 URL 확보 후 oEmbed |
| [naver.md](naver.md) | 네이버 블로그·뉴스·증권·검색 접근 | 서비스별 대체 접근(블로그는 `m.blog.naver.com` 변환, 증권은 비공식 JSON, 검색은 `search.naver.com`), 한글 검색 쿼리 패턴 |
| [media.md](media.md) | YouTube/Vimeo/Twitch/TikTok/SoundCloud 등 미디어 메타·자막·오디오 필요 시 | `yt-dlp --dump-json` 기반 1,858개 사이트 커버, 자막 다운로드(`--write-sub`), 포맷 선택, 라이브/팟캐스트 |

## D. Engine 코드 직접 읽을 때

| 파일 | 언제 읽는가 |
|------|-------------|
| `engine/phase0.py` | Phase 0 공식-API 라우터 (Reddit/X/YouTube 자동 경로). 플랫폼·경로 추가 시. bias_check 면제 파일(R5 sanctioned) |
| `engine/fetch_chain.py` | 체인 단계 로직·`Attempt`/`FetchResult` schema·`untried_routes`/`must_invoke_playwright_mcp` 실패게이트 |
| `engine/validators.py` | 4-계층 검증 세부 (Verdict 분류, 챌린지 마커 목록) |
| `engine/waf_detector.py` | WAF 랭킹 감지 알고리즘, `_LAST_LOAD_ERROR` 처리 |
| `engine/waf_profiles.yaml` | 프로파일별 detectors·tls_candidates·capabilities_needed |
| `engine/url_transforms.py` | URL 변환 규칙 추가할 때 |
| `engine/executor.py` | Playwright MCP vs local capability 매칭 로직 |
| `engine/templates/*.js` | Playwright 템플릿 튜닝 (warmup, reload, devices) |
| `engine/bias_check.py` | 편향 린터 규칙 — brand denylist, URL_PATTERN, excluded dirs |
