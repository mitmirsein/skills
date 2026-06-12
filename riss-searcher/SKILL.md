---
name: riss-searcher
description: >
  Searches RISS (Korean academic research service) for journal articles,
  theses, and books — bypassing TLS-fingerprint WAF blocks via curl_cffi
  (InsaneRecon) and filtering noise with ForensicAudit; supports language
  filters. Use when the user asks for Korean theses/dissertations or RISS
  lookup. 키워드: RISS 검색, 학위논문, 국내 학술 검색
triggers:
  - "RISS 검색"
  - "riss-searcher"
  - "학술연구정보서비스"
  - "RISS 논문 찾아줘"
  - "학위논문 검색"
version: 1.0.1
status: active
---

# RISS Searcher Skill

RISS(학술연구정보서비스, `riss.kr`)에서 논문·학위논문·단행본을 검색하는 에이전트 네이티브 스킬.  
TLS 핑거프린트 차단을 `curl_cffi` 기반 `InsaneRecon` 모듈로 우회한다.

## 핵심 아키텍처

```
[Step 1] InsaneRecon(curl_cffi) GET 검색 → ForensicAudit 필터링
[Step 2] (선택) 상세 조회 → 초록 + 메타데이터 수확
[Fallback] httpx 표준 클라이언트 재시도
```

## ⚠️ 필수 주의사항

### 1. TLS 핑거프린트 우회 필수
RISS는 일반 `httpx`/`requests` 라이브러리의 TLS 핑거프린트를 감지하여 차단한다.  
반드시 `curl_cffi` 라이브러리의 `safari15_5` 프로파일로 요청해야 한다.

```python
from curl_cffi import requests
response = requests.get(url, impersonate="safari15_5", timeout=30)
```

### 2. ForensicAudit 필터 의무 적용
검색 결과 제목에 쿼리 키워드가 실제로 포함되어 있는지 띄어쓰기를 무시하고 검증한다.  
RISS는 관련도 낮은 결과를 포함하는 경향이 있으므로 필터링이 특히 중요하다.

### 3. 의존 패키지

```toml
# curl_cffi는 시스템 libcurl에 의존 — uv 설치 시 자동 처리
curl-cffi>=0.7.0
httpx>=0.28.1
beautifulsoup4>=4.14.2
```

## 사용법

### 기본 검색

```bash
# scripts/ 디렉토리에서 실행
uv run python search.py "바르트 계시론" --output json
uv run python search.py "구원론" --category re_a_over --lang kor
uv run python search.py "하나님 나라" --output markdown --page 2
```

### 고급 검색 (언어 필터 + 이전 키워드 조합)

```bash
# 한국어 논문만
uv run python search.py "성령론" --lang kor --output json

# 영어 논문 포함
uv run python search.py "pneumatology" --lang eng --output json

# 독일어 논문
uv run python search.py "Offenbarung" --lang ger --output json

# 학위논문만
uv run python search.py "종말론" --category re_d_kor --output json
```

### 상세 조회

```bash
uv run python search.py --detail --control-no 012345678 --mat-type 1 --output json
```

### 출력 형식

**JSON** (`--output json`): 에이전트 파싱 최적화
```json
{
  "query": "바르트 계시론",
  "total": 5,
  "results": [
    { "rank": 1, "title": "칼 바르트의 계시 이해 ...", "control_no": "RBIB0000123456",
      "p_mat_type": "1", "info": "저자 | 학술지명 | 발행년도",
      "url": "https://www.riss.kr/search/detail/...", "download_links": [] }
  ],
  "forensic_audit": { "total_fetched": 10, "passed": 5, "rejected": 5 }
}
```

## 검색 카테고리 (category) 옵션

| 코드 | 의미 |
|---|---|
| `re_a_over` | 학술지 논문 (기본값) |
| `re_d_kor` | 국내 학위논문 |
| `re_d_for` | 해외 학위논문 |
| `re_b_over` | 단행본 |
| `re_r_kor` | 연구보고서 |

## 언어 필터 옵션

| 코드 | 의미 |
|---|---|
| `kor` | 한국어 |
| `eng` | 영어 |
| `ger` | 독일어 |
| `fre` | 프랑스어 |
| `jpn` | 일본어 |

## 에이전트 실행 패턴

```python
import subprocess, json

SKILL_DIR = ".skills/riss-searcher"

result = subprocess.run(
    ["uv", "run", "python", "scripts/search.py", keyword, "--output", "json"],
    capture_output=True, text=True, cwd=SKILL_DIR
)
data = json.loads(result.stdout)
```

## 한계 및 주의

- RISS 원문 PDF 다운로드는 기관 인증이 필요하므로 스킬 범위 외.
- curl_cffi 미설치 시 httpx fallback으로 자동 전환 (차단 가능성 높음).
- 페이지당 최대 10건 반환 (`--limit`로 조정 가능).
