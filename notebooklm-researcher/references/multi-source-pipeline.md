# 🌐 멀티소스 학술 파이프라인 (Multi-Source Academic Pipeline)

> **목적**: 국내(KCI/RISS) + 해외(Google Scholar / Semantic Scholar / NotebookLM research_start)  
> 5개 채널에서 학술 소스를 발굴하여 NotebookLM으로 통합하는 완전 자원 확보 파이프라인.  
>  
> **버전**: 1.0.0 | notebooklm-researcher v3.1 Integrated Edition

---

## 1. 파이프라인 맵 (Pipeline Map)

```
                    🎯 연구 주제 입력
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    🇰🇷 국내 채널         │          🌐 해외 채널
         │                │                │
    ┌────┴────┐      ┌────┴────┐    ┌──────┼──────┐
    │  KCI    │      │NLM      │    │Google│Seman-│
    │  RISS   │      │research_│    │Schol-│tic   │
    │  MCP    │      │_start   │    │ar    │Schol-│
    └────┬────┘      └────┬────┘    │(×2)  │ar    │
         │                │         └──┬───┴──┬───┘
         │                │            │      │
         └───────────┬────┘            │      │
                     │        ─────────┘      │
                     │       │                │
                     └───────┼────────────────┘
                             │
                    📥 URL / 메타데이터 수집
                             │
                    ✅ 소스 선별 & 중복 제거
                             │
                    📚 NotebookLM source_add
                             │
                    🔬 Dive / Plan Mode 연구
```

---

## 2. 채널별 도구 상세

### 🇰🇷 채널 1: KCI (한국학술지인용색인)
- **도구**: `kci-api-searcher` 스킬 → `.skills/kci-api-searcher/scripts/search.py`
- **강점**: 국내 학술지 논문, 피어리뷰 학술지 전문
- **약점**: 원문 URL 없는 경우 많음 → KCI 상세 페이지 URL 사용
- **출력**: 제목, 저자, 초록, artiId, 원문 링크

```bash
uv run python .skills/kci-api-searcher/scripts/search.py "칼 바르트 은혜론" --limit 10 --output markdown
# URL 선별 후 source_add
```

### 🇰🇷 채널 2: RISS (학술연구정보서비스)
- **도구**: `riss-searcher` 스킬 → `.skills/riss-searcher/scripts/search.py`
- **강점**: 국내 학위논문(석·박사) + 해외 학술논문 포함
- **약점**: 원문 접근 제한 많음 → 초록을 텍스트로 추가
- **카테고리**: `"re_a_over"` (해외학술), `"bib_t"` (학위논문)

```bash
uv run python .skills/riss-searcher/scripts/search.py "<keyword>" --category domestic --limit 10 --output markdown
uv run python .skills/riss-searcher/scripts/search.py "<keyword>" --category journal_over --limit 10 --output markdown
# URL / 텍스트로 source_add
```

### 🌐 채널 3: Semantic Scholar (Graph API)
- **도구**: `.skills/semantic-scholar/scripts/s2_runner.py`
- **강점**: ✅ API Key 보유 (`SEMANTIC_SCHOLAR_API_KEY`), Open Access PDF 링크, 인용 수
- **약점**: 신학 특화 자료 다소 부족
- **출력**: 논문 메타데이터 + PDF URL (Open Access인 경우)

```bash
# 실행 (MS_Dev에서)
uv run python .skills/semantic-scholar/scripts/s2_runner.py \
  --query "Karl Barth doctrine of grace" \
  --limit 10

# PDF URL이 있는 논문만 → source_add(url=pdf_url)
# PDF URL 없는 논문 → 초록을 텍스트로 source_add
```

**에이전트 호출 방식:**
```
s2_runner.py 결과에서:
- openAccessPdf.url 있음 → mcp_notebooklm_source_add(url=pdf_url)
- 없음 → mcp_notebooklm_source_add(text=abstract, title=title)
```

### 🌐 채널 4: Google Scholar Quick (빠른 목록)
- **도구**: `.skills/google-scholar-quick/` → Playwright CDP
- **강점**: 빠른 URL 확보, 최신 논문 포함
- **약점**: 캡차 위험, 직접 PDF URL 획득 어려움
- **용도**: URL 목록을 먼저 확보 → 개별 확인 후 import

```
google_scholar_quick_search.sh "Karl Barth grace"
→ URL 리스트 확보
→ source_add(url) 시도 (크롤링 성공 여부 NLM 의존)
```

### 🌐 채널 5: Google Scholar Semantic (RISE Protocol 심층)
- **도구**: `.skills/google-scholar-semantic/scripts/scholar_runner.py`
- **강점**: Scholar Labs AI 결과, 인용 네트워크, BibTeX 추출
- **약점**: 세션당 4쿼리 제한, 40초 대기
- **용도**: 심층 연구 시 최종 확인 단계 (Plan Mode 이후)

```bash
python .skills/google-scholar-semantic/scripts/scholar_runner.py \
  --query-file Evidence/SESSION/QuerySet.json \
  --output-dir Evidence/SESSION/google_scholar_labs \
  --citation-depth all --max-results 10
→ JSONL → source_add(text=abstract)
```

### 🌐 채널 6: NotebookLM research_start (NLM 내장 웹 검색)
- **도구**: `mcp_notebooklm_research_start`
- **강점**: NLM이 자체 판단으로 적합한 소스 발굴, 완전 자동화
- **약점**: 소스 선택 기준 불투명, 신학 특화 자료 제한적

```python
mcp_notebooklm_research_start(
    query="Karl Barth doctrine of grace ecumenical dialogue",
    mode="fast",    # ~30초, ~10개 소스
    notebook_id=<id>
)
→ mcp_notebooklm_research_status(notebook_id, max_wait=60)
→ mcp_notebooklm_research_import(notebook_id, task_id, cited_only=True)
```

---

## 3. 표준 실행 순서 (Standard Run Order)

### 🔴 1단계: 빠른 국내+해외 스캔 (5~10분)
```
병렬 실행:
├── KCI: kci-api-searcher search.py --limit 5
├── RISS: riss-searcher search.py --limit 5
├── S2: s2_runner.py --query <eng_query> --limit 10
└── NLM research_start(mode="fast")
```

### 🟡 2단계: 소스 선별 및 NotebookLM 임포트 (2~5분)
```
수집된 URL/텍스트 중:
- Open Access PDF → source_add(url=pdf)  [우선순위 1]
- 논문 상세 페이지 URL → source_add(url=detail)  [우선순위 2]
- URL 없음 → source_add(text=abstract, title=title)  [우선순위 3]
```

### 🟢 3단계: 심층 확장 (필요 시, 10~30분)
```
└── Google Scholar Semantic: scholar_runner.py (Scholar Labs)
    → BibTeX / 인용 네트워크 추가 발굴
    → 추가 소스 source_add
```

### 🔵 4단계: 연구 실행
```
Plan Mode 또는 Dive Mode 가동
→ 최종 보고서 생성
```

---

## 4. 쿼리 전략 (Query Translation)

| 한국어 주제 | KCI/RISS 쿼리 (한국어) | 해외 채널 쿼리 (영어) |
|:---|:---|:---|
| 칼 바르트 은혜론 | `칼 바르트 은혜` | `Karl Barth doctrine of grace` |
| 바울 칭의론 | `바울 칭의` | `Pauline justification sola fide` |
| 디트리히 본회퍼 제자도 | `본회퍼 제자도` | `Bonhoeffer cost of discipleship` |
| 불트만 비신화화 | `불트만 실존론적 해석` | `Bultmann demythologization existential` |

> **규칙**: KCI/RISS는 한국어로, Semantic Scholar / Google Scholar는 영어로 쿼리.  
> 독일어 신학 주제는 독어 쿼리도 병행 (Scholar Labs 지원).

---

## 5. 소스 커버리지 목표

```
이상적 1회 리서치 세션:
├── KCI:        3~5건 (국내 학술지)
├── RISS:       3~5건 (학위논문 + 해외학술)
├── S2:         5~8건 (Open Access PDF 우선)
├── NLM Fast:   5~10건 (자동 웹 검색)
└── Scholar:    (선택) 추가 심층 확인
────────────────────────────────────
총 목표:        15~25건 / 세션
```

---

## 6. 알려진 제한사항

| 채널 | 제한 | 해결책 |
|:---|:---|:---|
| KCI/RISS | 원문 URL 없는 경우 多 | KCI 상세 페이지 URL 또는 초록 텍스트 사용 |
| Semantic Scholar | Open Access 아닌 경우 PDF 불가 | 초록을 텍스트로 추가 |
| Google Scholar Quick | 캡차 위험 | 세션당 10건 이하, 쿼리 간 딜레이 |
| Google Scholar Semantic | 세션당 4쿼리 제한 | 쿼리 설계 신중히, `--max-queries-per-session 4` |
| NLM research_start | 소스 투명성 낮음 | `cited_only=True`로 임포트 선별 |
| NotebookLM | URL 크롤링 실패 가능 | DOI 직접 링크 > PDF 직접 링크 > 상세 페이지 순으로 시도 |

---

*Multi-Source Academic Pipeline | notebooklm-researcher v3.1 | MS_Dev 2026-05-16*
