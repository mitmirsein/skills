---
name: lightpanda-recon
description: >
  Headless browser recon via the Lightpanda binary — faster and lighter
  than Playwright for GitHub, docs, and JS-rendered pages. Use when a page
  needs JS rendering but no login/interaction (fall back to Playwright for
  those). 키워드: 라이트판다, 가벼운 정찰, 깃헙 분석, JS 렌더링 읽기
version: 1.0.1
author: MS_Dev
triggers:
  - "라이트판다로 읽어줘"
  - "가볍게 정찰해줘"
  - "깃헙 레포 분석해줘"
  - "웹페이지 내용 파악해줘"
  - "/lp [url]"
  - "/recon [url]"
capabilities:
  - js_rendered_html_extraction
  - markdown_dump
  - semantic_tree_text_dump
  - lightweight_fast_fetch
  - multi_url_parallel_recon
binary: ~/Desktop/MS_Dev.nosync/bin/lightpanda
version_confirmed: 0.2.9
status: active
---

# 🐼 Lightpanda Recon

> **핵심 원칙**: 웹 페이지를 읽어야 할 때 **항상 이 스킬을 1순위로 실행**한다.
> Lightpanda는 AI 에이전트를 위해 설계된 초경량 헤드리스 브라우저(Zig 기반 단일 바이너리, Chromium 불필요)이며, Playwright 대비 빠르고 메모리 효율이 압도적이다.

## 0. 웹 접근 삼각 체계 (교통정리)

```
🐼 1단계: Lightpanda (기본값, 항상 먼저)
    ↓ 빈 결과 / WAF 탐지
🔥 2단계: insane-search (차단 우회 전문)
    ↓ 로그인 / 실제 상호작용 필요
🎭 3단계: Playwright / browser_subagent (최후 수단)
```

| 도구 | 독점 영역 | 포기 기준 |
| :--- | :--- | :--- |
| **🐼 Lightpanda** | GitHub, 학술, 문서, 일반 웹 (JS 렌더링 포함) | 빈 결과 또는 WAF 탐지 |
| **🔥 insane-search** | Twitter/X, Reddit, YouTube 자막, 클라우드플레어, 네이버, 한국 커뮤니티 | 로그인 벽, 실제 상호작용 필요 |
| **🎭 Playwright** | 로그인 세션, 버튼 클릭, 폼 입력, 스크린샷 | 없음 (최후 수단) |

> **참고**: `insane-search`는 내부적으로 Playwright(Phase 3)를 포함한다. Lightpanda 실패 시 `insane-search`만 호출해도 Playwright까지 자동 에스컬레이션된다.

## 1. 언제 사용하는가 (사용 기준)

| 상황 | 도구 선택 |
| :--- | :--- |
| GitHub 레포 분석, README 읽기 | ✅ **Lightpanda** |
| 문서 사이트, 뉴스, 블로그 읽기 | ✅ **Lightpanda** |
| JS 렌더링이 필요한 일반 웹페이지 | ✅ **Lightpanda** |
| WAF/클라우드플레어 차단, 소셜 플랫폼 | 🔥 **insane-search** |
| 로그인, 버튼 클릭, 폼 입력, 스크린샷 | 🎭 **browser_subagent(Playwright)** |

## 2. 명령어 레퍼런스

### 기본 사용법

```bash
# AI 친화적 텍스트 추출 (권장 - 토큰 효율 최고)
~/Desktop/MS_Dev.nosync/bin/lightpanda fetch \
  --dump semantic_tree_text \
  --strip-mode full \
  --wait-ms 5000 \
  <URL>

# 마크다운 추출 (링크 보존이 필요할 때)
~/Desktop/MS_Dev.nosync/bin/lightpanda fetch \
  --dump markdown \
  --strip-mode full \
  --wait-ms 5000 \
  <URL>

# HTML 원본 추출 (구조 분석이 필요할 때)
~/Desktop/MS_Dev.nosync/bin/lightpanda fetch \
  --dump html \
  --strip-mode full \
  <URL>
```

### 옵션 상세

| 옵션 | 설명 | 권장값 |
| :--- | :--- | :--- |
| `--dump` | 출력 형식 | `semantic_tree_text` (AI 분석) / `markdown` (링크 필요) |
| `--strip-mode` | 제거할 태그 그룹 | `full` (JS+CSS+이미지 모두 제거, 텍스트만) |
| `--wait-ms` | 렌더링 대기 시간(ms) | `5000` (일반) / `8000` (SPA) |
| `--wait-until` | 대기 이벤트 | `done` (기본값) / `networkidle` (Ajax 사이트) |
| `--log-level` | 로그 수준 | 기본 warn (stderr로 출력되어 stdout 결과에 간섭 없음) |

### 병렬 다중 URL 정찰

```bash
# 여러 URL을 순차적으로 빠르게 스캔 (병렬 처리)
for url in <URL1> <URL2> <URL3>; do
  ~/Desktop/MS_Dev.nosync/bin/lightpanda fetch \
    --dump semantic_tree_text --strip-mode full "$url" &
done
wait
```

## 3. 실행 워크플로우

```
[요청 수신]
    ↓
🐼 Step 1: Lightpanda fetch --dump semantic_tree_text --strip-mode full
    ↓ 성공(텍스트 1줄 이상) → 분석 및 보고
    ↓ 실패(빈 결과 / WAF 감지)
🔥 Step 2: insane-search 스킬 호출 (Phase 0~3 자동 에스컬레이션)
    ↓ 로그인 벽 / 실제 상호작용 필요
🎭 Step 3: browser_subagent(Playwright) 직접 호출
```

> **원칙**: 각 단계 실패 시 반드시 실패 사유를 대장에게 명시하고 다음 단계로 이동.

## 4. 결과 검증 기준

- **성공**: stdout에 텍스트가 1줄 이상 출력된 경우.
- **실패**: 빈 결과(`---END---` 전 아무것도 없음), 또는 오류 메시지가 나온 경우.
- **주의**: stderr로 `$level=warn` 메시지가 나오는 것은 정상(stdout 결과에 영향 없음).

## 5. 알려진 한계 (Gotchas) → 삼각 체계 핸드오프 기준

| 한계 상황 | 증상 | 핸드오프 대상 |
| :--- | :--- | :--- |
| **클라우드플레어 WAF** | 빈 결과 또는 챌린지 페이지 | 🔥 insane-search Phase 2 |
| **소셜 플랫폼** (Twitter, Reddit 등) | 로그인 리다이렉트 | 🔥 insane-search Phase 0 (전용 API) |
| **SPA (React/Vue)** | 빈 결과 | `--wait-until networkidle --wait-ms 8000` 재시도 → 실패 시 🔥 insane-search |
| **로그인 필요 페이지** | 로그인 폼 노출 | 🎭 browser_subagent 직접 |
| **버튼 클릭 / 폼 입력** | 구조적 불가 | 🎭 browser_subagent 직접 |
| **User-Agent 제약** | Mozilla 포함 불가 → 일부 봇 탐지 | 🔥 insane-search Phase 2 (curl_cffi TLS 임퍼소네이션) |

## 6. 바이너리 정보

| 항목 | 값 |
| :--- | :--- |
| **경로** | `~/Desktop/MS_Dev.nosync/bin/lightpanda` |
| **버전** | v0.2.9 (확인: 2026-04-28) |
| **개발사** | lightpanda-io (GitHub: `lightpanda-io/browser`) |
| **아키텍처** | Zig 기반 단일 바이너리, Chromium 불필요 |
| **MCP 지원** | `lightpanda mcp` 서브커맨드 내장 |
