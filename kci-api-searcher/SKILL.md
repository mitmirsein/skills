---
name: kci-api-searcher
description: >
  Searches KCI (Korea Citation Index) via the official OpenAPI
  (open.kci.go.kr) and returns article metadata — abstract, authors,
  journal, DOI — in a single request. Use when the user asks for Korean
  academic papers, KCI search, or domestic journal lookup. This is the
  sole KCI skill (legacy kci-searcher removed 2026-06).
  키워드: KCI 검색, 한국 학술논문, 국내 저널, 초록 수집
triggers:
  - "KCI API 검색"
  - "kci-api-searcher"
  - "KCI OpenAPI 검색"
  - "KCI API 논문 찾아줘"
version: 1.0.0
status: active
---

# KCI OpenAPI Searcher Skill (kci-api-searcher)

KCI 직접 OpenAPI 서비스(`open.kci.go.kr/po/openapi/openApiSearch.kci`)를 **KCI 발급 직접 인증키(`KCI_OPEN_API_KEY`)**로 호출하는 에이전트 스킬. 공공데이터포털(data.go.kr) 우회 게이트웨이를 걷어내고, 초록 및 저자 정보를 1회의 단일 API 요청으로 고속 취합합니다.

## 핵심 특징
- **단일 요청 고속 취합:** 기존 data.go.kr의 4단계 보강 루프(M310 -> D214 -> D311)와 달리, 포털 직접 검색 API(`articleSearch`) 1회 호출로 저자명, 소속기관, 학술지명, UCI, DOI, 초록을 통합 반환합니다.
- **타임아웃 대폭 감소:** 공공 게이트웨이를 경유하지 않아 응답 딜레이 및 타임아웃 확률이 대폭 낮아집니다.
- **ForensicAudit 검증:** 입력 검색어가 부분 매칭되는 노이즈(예: "바르트" 검색 시 "헤르바르트" 매칭 등)를 지우기 위해 제목 텍스트 검증을 사후 수행합니다.

## 사용법

```bash
PY=~/Desktop/MS_Dev.nosync/.venv/bin/python

# 1) 기본 제목 검색 (JSON 출력)
$PY .skills/kci-api-searcher/scripts/search.py "구원론" --limit 5 --output json

# 2) 마크다운 리포트 출력
$PY .skills/kci-api-searcher/scripts/search.py "구원론" --limit 5 --output markdown
```

## 파라미터
- `query`: 검색할 논문 제목 키워드.
- `--page`: 페이지 번호 (기본 1).
- `--limit`: 출력 건수 (기본 10).
- `--output`: `json`(기본) | `markdown`.

## 에이전트 실행 패턴

```python
import json
import os
import subprocess

dev_root = os.path.expanduser("~/Desktop/MS_Dev.nosync")
result = subprocess.run(
    [os.path.join(dev_root, ".venv/bin/python"),
     ".skills/kci-api-searcher/scripts/search.py", "구원론", "--output", "json"],
    capture_output=True, text=True, cwd=dev_root,
)
data = json.loads(result.stdout)
```

(주의: `subprocess`는 `~`를 확장하지 않으므로 반드시 `expanduser`를 거친다.)

## 응답 필드
`title`, `title_eng`, `artiId`, `authors` (이름 배열), `affiliations` (소속기관 배열), `author_count`, `journal` (학술지명), `publisher` (발행학회/기관명), `pub_year`, `pub_mon`, `doi`, `uci`, `citation_kci`, `citation_wos`, `abstract`, `url`

## 💡 학회 홈페이지 및 JAMS 원문 획득 전략 (Society Archive Open Access)
- **KCI 직다운로드 차단 시 대안**: KCI 포털에서 직접 원문 다운로드가 막혀 있거나 상업 유통(DBpia/KISS)으로 유도되는 국내 학술지 논문은 `publisher`(발행학회)의 공식 홈페이지나 학회 전용 JAMS 포털(`*.jams.or.kr`)에서 무료 Open Access로 원문 PDF를 제공하는 경우가 많습니다.
- **실행 권장사항**: KCI 검색 결과에서 `journal` 및 `publisher` 정보를 확인한 뒤, 해당 학회 홈페이지(예: 한국신약학회 `ntsk.org`, 한국복음주의신학회 `kets.org` 등)의 '논문자료실'/'과월호'/'원문서비스' 또는 JAMS 시스템을 통해 무료 PDF를 직접 확보합니다.

