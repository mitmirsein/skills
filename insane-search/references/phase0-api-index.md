# Phase 0 — 플랫폼 공식 API 인덱스 (정본)

> 플랫폼이 **공식 공개한** 전용 API/CLI만 여기에 둔다. 이건 편향이 아니라 합의된 엔드포인트 사용이다.

## 소셜/커뮤니티 전용 API

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| X/Twitter | syndication (타임라인) + oEmbed (개별 트윗) + 키워드 검색: WebSearch → oEmbed | [twitter.md](twitter.md) |
| Reddit | URL + `.json` + Mobile UA | [json-api.md](json-api.md) |
| Bluesky | AT Protocol (`public.api.bsky.app/xrpc/...`) | [public-api.md](public-api.md) |
| Mastodon | 인스턴스별 공개 API | [public-api.md](public-api.md) |
| Hacker News | Firebase API + Algolia Search | [json-api.md](json-api.md) |
| Stack Overflow | SE API v2.3 | [public-api.md](public-api.md) |
| Lobste.rs / V2EX / dev.to | 공개 JSON API | [json-api.md](json-api.md) |

## 미디어 (CLI 도구 필수)

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| YouTube/Vimeo/Twitch/TikTok/SoundCloud 등 1,858개 | `yt-dlp --dump-json` | [media.md](media.md) |

## 학술/레지스트리

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| Theology Scholar Sweep | API 축(KCI/CrossRef/S2) + 웹 검색 축(IxTheo/Google Scholar/Google Scholar Semantic) | [theology-scholar-sweep.md](theology-scholar-sweep.md) |
| Google Scholar Semantic | 웹 검색/browser: `.skills/google-scholar-semantic/scripts/scholar_runner.py` (Labs, citation extraction) | [theology-scholar-sweep.md](theology-scholar-sweep.md) |
| Semantic Scholar (S2) | API: `.skills/semantic-scholar/scripts/s2_runner.py` + `SEMANTIC_SCHOLAR_API_KEY` from dev `.env` | [theology-scholar-sweep.md](theology-scholar-sweep.md) |
| IxTheo | 웹 검색/site API hybrid: `.skills/ixtheo-searcher/scripts/ixtheo_searcher.py` | [theology-scholar-sweep.md](theology-scholar-sweep.md) |
| CrossRef Journal | API: `.skills/crossref-journal-searcher/scripts/crossref_journal_searcher.py` | [theology-scholar-sweep.md](theology-scholar-sweep.md) |
| arXiv | Atom API | [public-api.md](public-api.md) |
| CrossRef | REST API | [public-api.md](public-api.md) |
| KCI (한국학술지인용색인) | `.skills/kci-api-searcher` CLI + `KCI_OPEN_API_KEY`/`KCI_API_KEY` from dev `.env` | [kci.md](kci.md) |
| Wikipedia | REST API | [json-api.md](json-api.md) |
| OpenLibrary | JSON API | [public-api.md](public-api.md) |
| GitHub | gh CLI / REST API | [public-api.md](public-api.md) |
| npm / PyPI | Registry API | [json-api.md](json-api.md) |
| Wayback Machine | CDX API | [public-api.md](public-api.md) |

## 한국 전용 공식 API

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| 네이버 검색 | `search.naver.com` (통합/블로그/뉴스탭) | [naver.md](naver.md) |
| 네이버 금융 시세 | `api.finance.naver.com/siseJson.naver` (비공식 JSON) | [naver.md](naver.md) |

**그 외 모든 사이트는 Phase 1(generic fetch chain)이 자동 처리한다.**

## 빠른 참조 — Phase 0 명령어

```bash
# 범용 웹 (Jina Reader — 일반 HTML만, WAF 사이트엔 무효)
curl -s "https://r.jina.ai/{URL}"

# yt-dlp — 1,858 사이트 미디어 메타데이터
yt-dlp --dump-json "URL"

# Reddit
curl -sL -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" \
  "https://www.reddit.com/r/{sub}/hot.json?limit=10"

# X/Twitter 타임라인
curl -sL "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"

# Hacker News
curl -sL "https://hacker-news.firebaseio.com/v0/topstories.json?limitToFirst=10&orderBy=%22%24key%22"

# YouTube 자막
yt-dlp --write-sub --write-auto-sub --sub-lang "en,ko" --skip-download -o "/tmp/%(id)s" "URL"
```
