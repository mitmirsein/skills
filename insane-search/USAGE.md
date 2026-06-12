# Insane Search 사용 가이드

`insane-search`는 일반 웹 접근이 막혔을 때 포기하지 않고, 공개 API, RSS/JSON 엔드포인트, Jina Reader, `yt-dlp`, KCI 전용 CLI, 그리고 `engine/` 기반 fetch chain을 순서 있게 선택하도록 돕는 스킬이다.

이 로컬 버전은 원본 v0.4.1의 `engine/` 하네스를 포함한다. 일반 URL 접근 실패는 문서에 적힌 헤더 조합을 즉흥적으로 반복하기보다 `python3 -m engine` 단일 진입점으로 trace를 남기며 판단하는 것이 기본이다.

## 기본 원칙

1. **Phase 0 우선**: X/Twitter, Reddit, HN, arXiv, 신학 학술 sweep, KCI, GitHub, YouTube처럼 공개 API나 전용 CLI가 있는 플랫폼은 그 경로를 먼저 쓴다.
2. **일반 URL은 engine 우선**: 차단/403/빈 SPA/WAF 신호가 있으면 `.skills/insane-search/engine`에서 `python3 -m engine "<URL>" --trace`를 실행해 결과와 trace를 확인한다.
3. **HTTP 200은 성공이 아니다**: `engine`의 validator가 챌린지 마커, body size, 쿠키 센서, selector 매칭을 확인한 뒤 `strong_ok` 또는 `weak_ok`를 낼 때 성공으로 본다.
4. **힌트는 런타임에만**: 사이트별 selector, referer, impersonate 우선순위는 명령 인자나 `user_hint`로만 넘기고, `engine/` 코드에는 특정 사이트를 하드코딩하지 않는다.
5. **설치 guardrail 준수**: 원본은 자동 설치를 전제하지만, 이 워크스페이스에서는 상위 `AGENTS.md`의 패키지 정책, 승인 흐름, 격리 환경 규칙이 우선한다.

## 일반 URL 요청

사용자는 보통 이렇게 요청하면 된다.

```text
insane-search로 이 URL 본문 읽고 핵심만 3줄 요약해줘: URL
```

에이전트가 직접 진단할 때의 기본 명령은 다음과 같다.

```bash
cd ~/Desktop/MS_Dev.nosync/.skills/insane-search
python3 -m engine "URL" --trace
```

본문 위치가 명확하면 selector를 함께 준다.

```bash
python3 -m engine "URL" --selector "article" --selector ".content" --trace
```

결과 해석:

- `strong_ok`: selector 같은 포지티브 증거가 맞았으므로 가장 신뢰한다.
- `weak_ok`: 챌린지/차단 신호는 없지만 selector 증거는 없다. 본문 샘플을 확인한다.
- `challenge`, `blocked`, `unknown`: trace를 보고 profile, transform, impersonate, fallback 필요성을 판단한다.

## 플랫폼별 요청 패턴

### 소셜/커뮤니티

```text
최근 X에서 "키워드" 관련 공개 포스트 5개를 찾아서 작성자, 요약, 링크를 표로 정리해줘.
r/LocalLLaMA에서 "Codex CLI" 관련 반응을 찾아서 주요 논점만 요약해줘.
Hacker News에서 오늘 AI 관련 상위 스레드 3개와 베스트 댓글을 요약해줘.
```

기본 경로:

- X/Twitter: WebSearch로 URL 확보 후 oEmbed, 또는 공개 syndication 타임라인.
- Reddit: `.json` 엔드포인트 + mobile UA.
- Hacker News: Firebase API 또는 Algolia Search.
- Bluesky/Mastodon/Stack Overflow: 공개 API.

### 미디어/동영상

```text
이 YouTube 영상 자막 추출해서 핵심 논점 3가지를 정리해줘: URL
이 영상의 제목, 업로드 날짜, 설명란 링크를 리스트업해줘: URL
```

기본 경로는 `yt-dlp --dump-json` 또는 자막 추출이다. 미설치 시 바로 설치하지 말고, 로컬 패키지 정책과 승인 흐름을 따른다.

### 한국 플랫폼

```text
네이버에서 "키워드" 관련 최신 뉴스와 블로그 글을 나눠서 찾아줘.
이 네이버 블로그 글 본문을 읽고 요약해줘: URL
클리앙/에펨코리아/디시인사이드에서 "제품명" 실사용 후기만 모아줘.
```

기본 경로:

- 네이버 검색: `references/naver.md`의 검색/뉴스/블로그 경로.
- 네이버 블로그: 모바일 URL 또는 RSS.
- 네이버 뉴스/증권: Jina Reader 또는 네이버 금융 JSON.
- 커뮤니티/쇼핑/동적 페이지: Phase 0 경로가 없으면 `engine`으로 trace 기반 접근.

### 신학 학술 탐색

```text
신학 학술 sweep으로 "칼 바르트 예정론" 관련 핵심 문헌을 찾아줘.
Google Scholar Semantic, S2, IxTheo, CrossRef, KCI를 돌려서 "삼위일체와 perichoresis" 논문 후보를 교차검증해줘.
국내외 신학 논문 검색에서 "아모스 4:13" 관련 최근 논쟁축을 정리해줘.
```

신학 학술 검색은 Phase 0에서 API 축과 웹 검색 축을 구분한다. API 축은 KCI, CrossRef, Semantic Scholar(S2)이고, 웹 검색 축은 IxTheo, Google Scholar, Google Scholar Semantic이다. API 축은 빠르고 구조화되어 우선 실행하며, 웹 검색 축은 발견력이 크지만 환경 의존성이 있으므로 후보를 찾은 뒤 API 축으로 재검증한다.

기본 실행 흐름:

```text
QuerySet 생성
  -> API 축: KCI + CrossRef/CrossRef Journal + Semantic Scholar API
  -> 웹 검색 축: IxTheo + Google Scholar + Google Scholar Semantic
  -> 웹 검색 후보를 API 축으로 재검증
  -> DOI/title/author/year 기준 병합
```

API 축:

```bash
cd ~/Desktop/MS_Dev.nosync
python .skills/semantic-scholar/scripts/s2_runner.py --query "Karl Barth doctrine of election" --limit 10 --format json --fields "Philosophy,Religious Studies"
python .skills/crossref-journal-searcher/scripts/crossref_journal_searcher.py --query "Karl Barth election" --limit 10 --format json
```

웹 검색 축:

```bash
cd ~/Desktop/MS_Dev.nosync
python .skills/ixtheo-searcher/scripts/ixtheo_searcher.py --query "Karl Barth Erwählungslehre" --limit 10 --format json
~/Desktop/MS_Dev.nosync/shared_venv/bin/python .skills/google-scholar-semantic/scripts/scholar_runner.py \
  --query "What does recent scholarship say about Karl Barth's doctrine of election?" \
  --domain theology \
  --tre-expand \
  --output-dir /tmp/theology_scholar_sweep/google_scholar_labs \
  --jsonl /tmp/theology_scholar_sweep/google_scholar_labs/scholar_labs.jsonl \
  --max-queries-per-session 5 \
  --wait-seconds 40 \
  --browser-channel chrome \
  --citation-depth all \
  --max-results 10
```

KCI:

```bash
cd ~/Desktop/MS_Dev.nosync
uv run python .skills/kci-api-searcher/scripts/search.py "검색어" --limit 10 --output markdown
# (구 --detail 2단계 조회는 폐기 — 검색 1회가 초록까지 반환)
```

개발 워크스페이스 `.env`에는 S2/KCI API 키가 설정되어 있다. 키 값은 절대 출력하지 않는다. 자세한 운용은 `references/theology-scholar-sweep.md`와 `references/kci.md`를 본다.
Google Scholar Semantic은 API 키가 아니라 로그인된 브라우저 세션이 필요한 웹 검색 축이다. 한 세션은 최대 5개 쿼리까지만 사용하고, 세션 내 각 쿼리는 Scholar Labs가 약 100개 후보를 찾아 10개 추천 결과를 렌더링할 수 있도록 최소 40초 대기한다. Headless smoke에서 `accounts.google.com`으로 리다이렉트되면 저장 HTML 파싱 또는 `--browser-channel chrome`을 붙인 로그인된 Chrome 세션 경로를 사용한다.

### 개발/연구

```text
arXiv에서 최근 7일간 "LLM Agent" 관련 논문을 찾아서 제목, 저자, 링크를 정리해줘.
GitHub에서 "agent memory graph" 관련 저장소를 별점순으로 찾아줘.
npm/PyPI에서 특정 패키지의 최신 버전과 메타데이터를 확인해줘.
```

기본 경로:

- arXiv: Atom API.
- CrossRef/OpenLibrary/GitHub/npm/PyPI: 공개 API 또는 registry API.
- GitHub는 가능하면 `gh` CLI를 우선하되, 인증/설치 상태를 먼저 확인한다.

### 긴 글/뉴스레터/아카이브

```text
이 Medium/Substack/브런치 글을 읽고 저자의 핵심 주장과 근거를 정리해줘: URL
원본 페이지가 안 열리는데 Wayback Machine이나 archive.today에서 공개 스냅샷이 있는지 확인해줘: URL
```

Jina Reader, OGP/JSON-LD, RSS, Wayback/CDX, archive.today를 차례로 검토한다. 로그인/구독/페이월 신호가 명확하면 인증 필요 여부와 사용 가능한 공개 메타데이터 범위를 구분해 보고한다.

## 고급 진단

### trace 기반 재시도

`engine` 실패 시 `--json --trace`로 재호출해 profile과 verdict를 확인한다.

```bash
python3 -m engine "URL" --trace --json
```

유용한 판단 포인트:

- `profile_used`: 감지된 WAF/챌린지 유형.
- `trace[].verdict`: `challenge`가 반복되는지, 특정 transform만 실패하는지.
- `trace[].body_size`: 200 OK지만 비정상적으로 작은 차단 페이지인지.
- `summary`: R7 API-first 힌트가 나오는지.

### R7 API-first

리스트/수집/반복 요청에서 WAF 챌린지가 반복되면, 브라우저로 HTML을 억지로 읽기보다 네트워크 요청에서 공개 JSON/API 엔드포인트를 찾는 경로가 빠를 수 있다.

```text
브라우저로 대상 페이지를 열고 network requests에서 /api/, /graphql, .json 호출을 찾아줘.
찾은 API URL을 insane-search engine으로 다시 호출해서 구조를 확인해줘.
```

탐지한 API URL과 파라미터는 런타임 결과로만 사용한다. `engine/` 코드에 사이트별 API를 저장하지 않는다.

## 참고 문서 선택

- 일반 fetch 실패/trace 해석: `references/fallback.md`
- Jina Reader: `references/jina.md`
- 공개 JSON/API: `references/json-api.md`, `references/public-api.md`
- X/Twitter: `references/twitter.md`
- 네이버: `references/naver.md`
- 미디어/자막: `references/media.md`
- 신학 학술 sweep: `references/theology-scholar-sweep.md`
- KCI: `references/kci.md`
- RSS/Google News RSS: `references/rss.md`
- 아카이브: `references/cache-archive.md`
- 메타데이터/JSON-LD: `references/metadata.md`
- TLS/Playwright engine 진단: `references/tls-impersonate.md`, `references/playwright.md`
- 페이월 감지/로컬 확장: `references/paywall.md`

## 마지막 점검

작업 완료 전에는 무엇을 실제로 검증했는지 분명히 말한다.

- URL을 직접 열었는지, API만 확인했는지, 캐시/아카이브만 확인했는지 구분한다.
- `engine`을 썼다면 verdict, profile, 시도 수, trace상 핵심 실패 신호를 보고한다.
- 신학 학술 sweep을 썼다면 Google Scholar Semantic, S2, IxTheo, CrossRef, KCI 중 실제 실행한 축과 각 결과 수/실패 사유를 보고한다.
- 설치가 필요했지만 수행하지 않았다면 그 이유와 남은 리스크를 말한다.
