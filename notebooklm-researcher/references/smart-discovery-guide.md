# 🔍 Smart Discovery Guide: 메타데이터 자동 추출 기법

> **목적**: 새로운 노트북을 수신했을 때, 소스의 전체 맥락을 빠르게 파악하고 색인하는 가이드.

---

## 1. Discovery 절차

### Step 1: 노트북 메타데이터 확보
```
notebook_info = mcp_notebooklm_notebook_get(notebook_id)
```
- 노트북 제목, 소스 목록, 생성일을 확인합니다.

### Step 2: AI 요약 및 토픽 추출
```
description = mcp_notebooklm_notebook_describe(notebook_id)
```
- `summary`: 노트북 전체에 대한 AI 요약 (마크다운)
- `suggested_topics`: AI가 제안하는 탐구 주제 목록

### Step 3: 소스별 키워드 칩 수집
```
for each source in notebook_info.sources:
    source_desc = mcp_notebooklm_source_describe(source.id)
    # source_desc.keywords → 핵심 키워드 목록
    # source_desc.summary → 소스별 요약
```

### Step 4: 색인 카드 생성
수집된 정보를 아래 형식의 '색인 카드'로 종합합니다.

```markdown
## 📇 노트북 색인 카드
- **제목**: {notebook_title}
- **ID**: {notebook_id}
- **소스 수**: {count}
- **AI 요약**: {summary (첫 3문장)}
- **핵심 토픽**: {suggested_topics (쉼표 구분)}
- **소스 목록**:
  | # | 제목 | 유형 | 키워드 |
  | --- | --- | --- | --- |
  | 1 | ... | PDF | ontology, graph |
  | 2 | ... | URL | RAG, vector |
```

---

## 2. 발견의 깊이 기준 (Discovery Depth)

| 수준 | 설명 | 사용 시점 |
| :--- | :--- | :--- |
| **Quick** | `notebook_describe`만 실행 | 노트북의 대략적 주제만 필요할 때 |
| **Standard** | + 소스별 `source_describe` | Plan/Dive 모드 진입 전 기본 점검 |
| **Full** | + 소스별 `source_get_content` | 소스 원문까지 필요한 정밀 연구 |

---
*NotebookLM Researcher 3.0 | Discovery Reference*
