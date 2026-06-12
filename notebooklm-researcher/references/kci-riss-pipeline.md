# 📡 KCI/RISS → NotebookLM 소스 파이프라인

> **목적**: 한국 학술 데이터베이스(KCI/RISS)에서 발굴한 논문을 NotebookLM 노트북으로 자동 임포트하여  
> 국내 학술 자료를 연구 런타임에 통합하는 파이프라인.

---

## 1. 전제 조건

| 도구 | 역할 | 확인 방법 |
|:---|:---|:---|
| `kci-api-searcher` 스킬 | KCI 검색 및 메타데이터 수집 | `.skills/kci-api-searcher/scripts/search.py` |
| `riss-searcher` 스킬 | RISS 검색 및 메타데이터 수집 | `.skills/riss-searcher/scripts/search.py` |
| `notebooklm-mcp` MCP 서버 | NotebookLM 소스 추가 및 쿼리 | `nlm setup list` → ✓ 확인 |

---

## 2. 표준 파이프라인 (3단계)

### Stage 1: KCI/RISS Discovery (학술 소스 발굴)

에이전트가 `kci-api-searcher`와 `riss-searcher` 스킬을 실행하여 논문 목록과 메타데이터를 수집합니다.

**KCI 경로:**
1. `uv run python .skills/kci-api-searcher/scripts/search.py "<keyword>" --limit 10 --output markdown`
2. 필요한 경우 `--detail <artiId>`로 초록 + 원문 링크 확보
3. 출력된 URL과 초록을 선별

**RISS 경로:**
1. `uv run python .skills/riss-searcher/scripts/search.py "<keyword>" --category journal_over --output markdown`
2. `uv run python .skills/riss-searcher/scripts/search.py "<keyword>" --category domestic --output markdown`
3. 출력된 URL과 초록을 선별

---

### Stage 2: Source Qualification (소스 선별)

발굴된 논문에서 NotebookLM에 추가할 가치가 있는 것을 선별합니다:

```markdown
## 선별 기준 (에이전트 판단)
- 초록이 연구 주제와 직접 관련 있는가?
- 원문 URL이 존재하는가? (URL 없으면 NotebookLM 추가 불가)
- 중복 소스가 아닌가?
```

**원문 URL 우선순위:**
1. DOI 직접 링크 (`doi.org/...`)
2. PDF 직접 링크
3. KCI/RISS 상세 페이지 URL (최소한 이것이라도)

---

### Stage 3: NotebookLM Import (노트북에 소스 추가)

```
선별된 URL을 notebooklm-mcp의 source_add로 일괄 추가
```

**MCP 도구 호출:**
```python
# 단일 소스 추가
mcp_notebooklm_source_add(
    notebook_id="<대상 노트북 ID>",
    url="https://doi.org/10.xxxx/xxxx",
    title="논문 제목 (선택)"
)

# 소스 추가 후 즉시 쿼리 가능
mcp_notebooklm_notebook_query(
    notebook_id="<노트북 ID>",
    query="방금 추가된 논문의 핵심 주장은?"
)
```

---

## 3. 빠른 파이프라인 명령 예시

### 신학 논문 단권화 예시:
```
에이전트에게:
"KCI에서 '칼 바르트 은혜론' 관련 논문 5편을 찾아서, 
 원문 URL을 내 [신학연구] 노트북에 추가하고, 
 각 논문의 핵심 주장을 인용과 함께 정리해줘."
```

### 하이브리드 검색 예시:
```
1. `uv run python .skills/kci-api-searcher/scripts/search.py "칼 바르트 은혜론" --limit 10 --output markdown`
2. 관련 논문의 초록+URL 확보
3. source_add(notebook_id, url) × N건
4. notebook_query("추가된 논문들의 바르트 은혜론 해석 비교")
```

---

## 4. 알려진 제한사항 (Gotchas)

| 상황 | 해결책 |
|:---|:---|
| KCI 논문에 URL 없음 | 상세 페이지 URL 직접 사용 (KCI 링크로 대체) |
| RISS 학위논문 원문 제한 | 초록만 텍스트로 복사해서 `source_add`에 `text` 파라미터로 추가 |
| NotebookLM URL 크롤링 실패 | DOI → PDF 링크로 대체 시도 |
| 한국어 논문 쿼리 정확도 저하 | 영어 번역 제목도 함께 소스로 추가 권장 |

---

*KCI-RISS Pipeline Guide | notebooklm-researcher v3.1 | MS_Dev*
