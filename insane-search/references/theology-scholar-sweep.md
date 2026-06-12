# Theology Scholar Sweep

> 신학 학술 탐색 전용 Phase 0. 범용 웹 우회 전에 Google Scholar Semantic, Semantic Scholar, IxTheo, CrossRef, KCI를 다축으로 돌려 문헌 후보를 발견하고 교차검증한다.

## 역할 분담

| 축 | 접근 유형 | 주 역할 | 강점 | 산출 |
|----|-----------|---------|------|------|
| KCI | API | 국내 논문 축 | 한국어 신학 논문, KCI 초록/인용 | KCI `artiId`, DOI, abstract |
| CrossRef / CrossRef Journal | API | DOI/저널 검증 | DOI, 권호, 저널, 출판 메타데이터 | normalized CrossRef records |
| Semantic Scholar (S2) | API | 구조화 메타데이터 | 초록, 인용 수, OA PDF, 빠른 API | JSON/Markdown paper records |
| IxTheo | Web search / site API hybrid | 신학 특화 보강 | 독일어권/유럽권 신학 서지 | JSON/Markdown bibliographic records |
| Google Scholar | Web search | 넓은 발견망 | Scholar 색인, 인용망, 회색지대 서지 발견 | search result candidates |
| Google Scholar Semantic | Web search / browser | 시맨틱 발견망 | Scholar Labs, 인용 버튼, 비정형 학술 결과 | `scholar_labs.jsonl`, citation variants |

## 기본 순서

1. **QuerySet 생성**: 한국어, 영어, 독일어 질문형 쿼리를 만든다. 성서학/조직신학 주제는 필요 시 히브리어/헬라어/TRE headword를 추가한다.
2. **API 축 먼저**: KCI, CrossRef, S2를 먼저 돌려 안정적인 구조화 메타데이터를 확보한다.
3. **웹 검색 축 보강**: IxTheo, Google Scholar, Google Scholar Semantic으로 API 축이 놓치는 신학 전문/인용망 결과를 찾는다.
4. **API 재검증**: 웹 검색에서 발견한 제목/저자/DOI 후보를 S2/CrossRef/KCI로 다시 확인한다.
5. **중복 병합**: DOI, title normalized key, author/year로 중복을 묶고 각 축의 evidence tag를 남긴다.

## 접근 유형 구분

### API 축

API 축은 빠르고 구조화되어 있으며, 우선 실행한다.

- **KCI**: dev `.env`의 `KCI_OPEN_API_KEY` / `KCI_API_KEY` 사용.
- **CrossRef / CrossRef Journal**: 공개 API. DOI/저널 메타데이터 검증용.
- **Semantic Scholar (S2)**: dev `.env`의 `SEMANTIC_SCHOLAR_API_KEY` 사용. 초록/인용 수/OA PDF 확인용.

### 웹 검색 축

웹 검색 축은 발견력이 크지만 느리고 환경 의존성이 있다. 결과는 후보로 태깅하고 API 축으로 재검증한다.

- **IxTheo**: 신학 특화 웹 검색/SRU 계열. 독일어권·유럽권 신학 서지 보강.
- **Google Scholar**: 일반 Scholar 검색. 웹 검색 축으로 취급.
- **Google Scholar Semantic**: Scholar Labs/browser 기반. 시맨틱 발견과 citation extraction에 특화.

## QuerySet 규칙

Google Scholar Semantic은 키워드 나열보다 자연어 질문을 선호한다.

```text
Bad: Barth election doctrine modern scholarship
Good: What does recent scholarship say about Karl Barth's doctrine of election?
Good: How has recent German-language theology interpreted Barth's doctrine of election?
Good: 칼 바르트 예정론에 관한 최근 국내 신학 논문은 어떤 논점을 다루는가?
```

신학 도메인에서는 다음 언어 축을 권장한다.

- 한국어: KCI/RISS/국내 논쟁.
- 영어: S2, Scholar, CrossRef.
- 독일어: IxTheo, 독일어권 신학 서지.
- 원어/고전어: 성서학 주제에서만 opt-in.

## 실행 예시

### Google Scholar Semantic

```bash
~/Desktop/MS_Dev.nosync/shared_venv/bin/python \
  .skills/google-scholar-semantic/scripts/scholar_runner.py \
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

Notes:
- Labs 실행은 브라우저 기반이며 느리다. 쿼리 실행 후 결과 렌더링까지 대기한다.
- 한 세션당 `--max-queries-per-session`은 5 이하로 유지한다. 5개를 넘으면 새 브라우저 세션으로 회전한다.
- 세션 내 각 쿼리 뒤에는 최소 `--wait-seconds 40`을 둔다. Scholar Labs가 쿼리 후 약 100개 후보를 찾고 그중 10개를 추천하는 렌더링 시간을 확보하기 위함이다.
- `citation_status != ok`인 레코드는 최종 참고문헌에서 재시도/불완전 후보로 표시한다.
- 로컬 기준 Python은 `~/Desktop/MS_Dev.nosync/shared_venv/bin/python` (Python 3.12)이다.
- Google Scholar Labs는 API 키가 아니라 로그인된 브라우저 세션이 필요하다. headless 실행은 `accounts.google.com` 로그인으로 리다이렉트될 수 있다.
- Playwright 패키지와 Chromium 브라우저 바이너리가 `shared_venv`/Playwright cache에 준비되어 있어야 한다.
- 라이브 브라우저 경로는 시스템 Chrome 채널(`--browser-channel chrome`)이 가장 안정적으로 검증되었다.
- 라이브 실행이 막히면 Chrome/브라우저 세션에서 HTML을 확보한 뒤 `--html` 파서 모드로 주입한다.

Headless 진단 예시:

```bash
PYTHONUNBUFFERED=1 ~/Desktop/MS_Dev.nosync/shared_venv/bin/python \
  .skills/google-scholar-semantic/scripts/scholar_runner.py \
  --query "What does recent scholarship say about Sabbath theology?" \
  --domain theology \
  --max-results 1 \
  --max-queries 1 \
  --max-queries-per-session 1 \
  --citation-depth none \
  --wait-seconds 5 \
  --browser-channel chrome \
  --login-timeout-seconds 10 \
  --headless \
  --output-dir /tmp/theology_scholar_sweep/google_scholar_labs \
  --jsonl /tmp/theology_scholar_sweep/google_scholar_labs/scholar_labs.jsonl
```

저장 HTML 파싱 예시:

```bash
~/Desktop/MS_Dev.nosync/shared_venv/bin/python \
  .skills/google-scholar-semantic/scripts/scholar_runner.py \
  --html scholar_result_1.html \
  --output-dir /tmp/theology_scholar_sweep/google_scholar_labs_parse \
  --jsonl /tmp/theology_scholar_sweep/google_scholar_labs_parse/scholar_labs.jsonl
```

### Semantic Scholar (S2)

```bash
python .skills/semantic-scholar/scripts/s2_runner.py \
  --query "Karl Barth doctrine of election" \
  --limit 10 \
  --format json \
  --fields "Philosophy,Religious Studies"
```

Notes:
- dev `.env`의 `SEMANTIC_SCHOLAR_API_KEY`를 사용한다. 키 값은 출력하지 않는다.
- S2는 발견보다는 구조화, 초록, citation count, OA PDF 확인에 강하다.

### IxTheo

```bash
python .skills/ixtheo-searcher/scripts/ixtheo_searcher.py \
  --query "Karl Barth Erwählungslehre" \
  --limit 10 \
  --format json
```

Notes:
- 독일어권/유럽권 신학 서지 보강에 우선 사용한다.
- 영어 쿼리와 독일어 쿼리를 모두 시도하면 누락을 줄일 수 있다.

### CrossRef Journal

```bash
python .skills/crossref-journal-searcher/scripts/crossref_journal_searcher.py \
  --query "Karl Barth election" \
  --limit 10 \
  --format json
```

Notes:
- DOI, 저널, 권호, 페이지, 출판사 검증에 사용한다.
- 신학 저널 필터가 적용된 결과는 일반 CrossRef보다 정밀할 수 있다.

### KCI

```bash
uv run python .skills/kci-api-searcher/scripts/search.py \
  "칼 바르트 예정론" \
  --limit 10 \
  --output markdown
```

또는 KCI 직접 OpenAPI 환경이 준비된 경우:

```bash
uv run python .skills/kci-api-searcher/scripts/search.py \
  "칼 바르트 예정론" \
  --limit 10 \
  --output markdown
```

Notes:
- dev `.env`의 `KCI_OPEN_API_KEY`와 `KCI_API_KEY`를 사용한다. 키 값은 출력하지 않는다.
- 현재 Python 환경에 의존성이 없으면 설치를 바로 시도하지 말고 상위 패키지 guardrail을 따른다.

## 병합 기준

각 결과는 다음 필드 중심으로 정규화한다.

```text
title
authors
year
venue / journal
publisher
doi
url
abstract / snippet
citation_count
source_axis: google_scholar_semantic | s2 | ixtheo | crossref | kci
source_id: paperId | IxTheo record id | DOI | KCI artiId
```

중복 판단 우선순위:

1. DOI 완전 일치.
2. 정규화 제목 + 출판연도 일치.
3. 정규화 제목 + 대표 저자 일치.
4. Scholar citation text와 CrossRef/S2 제목의 높은 유사도.

## 보고 원칙

- 어떤 축을 실제로 실행했는지 명시한다.
- 각 축의 결과 수와 실패 사유를 분리한다.
- DOI/S2/IxTheo/KCI ID가 있으면 클릭 가능한 링크 또는 식별자를 남긴다.
- Scholar Semantic 단독 결과는 "발견 후보"로 태깅하고, S2/CrossRef/IxTheo/KCI 검증 여부를 따로 표시한다.
- 신학적 쟁점은 합성으로 납작하게 만들지 말고 논쟁축과 해석 진영을 보존한다.
