---
name: insane-search
description: >
  Auto-bypass for blocked websites — tries every method until one works.
  Use when WebFetch returns 402/403/blocked, or when accessing X/Twitter, Reddit,
  YouTube, GitHub, Mastodon, Medium, Substack, Stack Overflow, Threads, Naver,
  Coupang, LinkedIn, or any platform with WAF/bot protection. Leverages yt-dlp
  (1,858 media sites), Jina Reader, public APIs (HN, Bluesky, arXiv), and a
  generic WAF-profile-driven fetch chain (curl_cffi TLS impersonation, mobile
  URL transforms, Playwright real-Chrome) with auto dependency install.
  Do NOT trigger for simple web searches that WebSearch can handle directly.
  키워드: 사이트 차단됨, 트위터/X 못 열어, 레딧 안 읽혀, 유튜브 자막, 깃헙 검색,
  네이버 블로그, 페이월 우회, WAF 차단
version: 1.1.0
status: active
---

# Insane Search

> URL 접근이 차단될 때, **사이트 무관한** 우회 전략을 자동 선택한다.

## 하네스 규칙 (Claude에게 강제되는 지침)

이 규칙은 Claude가 즉흥 판단으로 엇나가지 못하게 하기 위한 **고삐**다. 위반 시 "chrome 200에서 break → safari 미시도 → Playwright 미설치라 포기" 식의 오판이 재현된다.

**R1 — 일반 웹 URL 차단/403/402 감지 시**:
1. WebFetch, 즉흥 curl, 수동 헤더 조합 **시도 금지**
2. 즉시 다음을 실행:
   ```bash
   python3 -m engine "<URL>" [--selector "<CSS>"] [--device auto|desktop|mobile] [--trace]
   ```
3. 종료코드 0(ok) 또는 1(fail) 받은 뒤 판단. trace를 먼저 읽고 재시도 결정.
4. 실패 시에만 `--trace --json`으로 재호출해서 원인 진단 후 `--device` 또는 `user_hint` 조정.

**R2 — 첫 200에서 탈출 금지**: HTTP 200은 **검사 시작 조건**이지 성공이 아니다. 4-계층 검증(챌린지 마커/크기/쿠키 센서/success_selectors)을 통과해야 성공 선언. CLI는 이미 강제한다.

**R3 — 편향 금지**: `engine/**`, `waf_profiles.yaml`에 특정 사이트 도메인·셀렉터·브랜드명 하드코딩 금지. `python3 engine/bias_check.py`가 CI 게이트. 전체 규칙: [no-site-name-rule.md](references/no-site-name-rule.md)

**R4 — 힌트는 런타임에만**: 사이트 고유 정보(성공 셀렉터, 우선 Referer)는 CLI 인자 또는 `user_hint`로만 전달, 저장소에 고정 금지.

**R5 — Phase 0 공식 API 우선**: X/Reddit/YouTube/HN/arXiv 등 **공식 공개 엔드포인트**가 있는 플랫폼은 [phase0-api-index.md](references/phase0-api-index.md)를 먼저 확인하고 해당 API를 쓴다. 이건 편향이 아니라 합의된 접근 경로.

**R6 — 실패 선언은 전수 시도 후에만**: 격자(URL 변환 × TLS impersonate × Referer × Playwright fallback)를 **모두** 돌린 뒤에만 "뚫을 수 없음" 결론. CLI의 `max_attempts` 기본 12가 이를 보장. 단, R7 성립 시 engine은 계속 돌되 Claude가 병렬로 MCP 정찰 루트를 시도할 수 있다 — 빠른 쪽이 이긴다.

**R7 — WAF 조기 감지 시 API-first 병행 분기**. 발동 조건 (AND):
1. engine 초기 2~3회 attempt가 모두 `verdict=challenge`
2. `profile_used`가 `akamai_bot_manager`/`cloudflare_turnstile`/`datadome_probable`/`perimeterx_human`/`f5_big_ip`/`aws_waf` 중 하나로 확정
3. 사용자 요청이 **리스트/수집/반복 의도** (단건 본문 조회는 해당 없음)

세 조건 모두 참이면: engine을 `run_in_background=true`로 돌려둔 채, foreground에서 MCP
Playwright 정찰(네트워크 요청에서 내부 API 식별 → `python3 -m engine <API_URL>` 재호출)을
병행한다. 실행 상세·근거: [fetch-chain-guide.md](references/fetch-chain-guide.md) §R7 보충.

핵심 불변식: **단일 진입점**(`python3 -m engine <URL>` / `from engine import fetch`) ·
**편향 금지** · **힌트는 런타임에만**.

## 의도 분류 (Phase 0 진입 전)

| 사용자 입력 | 경로 |
|------------|------|
| URL 제공 (`https://...`) | → Phase 0 검사 후 없으면 Phase 1 (generic fetch chain) |
| 핸들 제공 (`@username`) | → Phase 0 syndication/API |
| 키워드만 ("X에서 AI 검색") | → WebSearch(`site:{domain} {keyword}`) 먼저 → URL 확보 후 재진입 |

> **한국어 신규 콘텐츠 한계**: 네이버/다음/한국 커뮤니티의 키워드 검색은 WebSearch 경유가 유일하며, 신규 콘텐츠 인덱싱이 지연될 수 있다.

## Phase 0 — 플랫폼 공식 API (정본: [phase0-api-index.md](references/phase0-api-index.md))

소셜(X/Reddit/Bluesky/Mastodon/HN/SO) · 미디어(yt-dlp 1,858 사이트) · 학술(KCI/S2/IxTheo/
CrossRef/arXiv + Theology Scholar Sweep) · 한국(네이버) 공식 엔드포인트 색인과 빠른 참조
명령어는 위 정본 문서를 본다. **그 외 모든 사이트는 Phase 1이 자동 처리한다.**

## Phase 1 — Generic Fetch Chain

```python
from insane_search.engine import fetch

result = fetch(
    "https://example.com/path",
    success_selectors=["article", "[class*='product-card']"],  # 포지티브 프루프 (선택)
    device_class="auto",      # "auto" | "desktop" | "mobile"
    user_hint=None,           # {"referer_strategy": "self_root", "impersonate_first": "safari"}
    timeout=25,
)
# result.ok → verdict: strong_ok | weak_ok / 실패 시 result.trace로 원인 진단
```

내부 단계(probe→validate→detect→plan→execute→fallback→report), 격자 축, Playwright
폴백(capability-matched), MCP 직접 호출 규칙, Phase 2 수동 개입(user_hint)의 정본:
**[fetch-chain-guide.md](references/fetch-chain-guide.md)**

## 의존성 자동 설치

```bash
python3 -c "import curl_cffi, bs4, yaml" 2>/dev/null || pip install curl_cffi beautifulsoup4 pyyaml -q
```

로컬 워크스페이스에서는 상위 `AGENTS.md`의 패키지 설치 guardrail이 우선한다. Playwright
로컬 경로 사용 시 Node 필요 (`npm i -g playwright playwright-extra puppeteer-extra-plugin-stealth`).

## 참조 문서 내비게이션

어떤 상황에 어떤 `references/*.md`를 읽을지는 **[reading-guide.md](references/reading-guide.md)**가
정본이다 (engine 진단 A / 경량 대안 B / 플랫폼별 API C / engine 코드 D). 선제적으로 전부
읽지 말고 필요할 때만 연다.
