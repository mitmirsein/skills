# 📎 Citation Mapping Spec: 인용 정규화 규격

> **목적**: NotebookLM 답변의 인용 정보를 일관되고 추적 가능한 형식으로 정규화하는 규격.

---

## 1. 원칙

1. **모든 답변에는 인용이 포함되어야 한다**: 질문 시 항상 "근거와 출처를 포함하여 답변해 주세요"를 추가합니다.
2. **인용 번호는 소스 제목과 매핑되어야 한다**: 독자가 `[3]`만 보고는 의미를 알 수 없습니다.
3. **인용 표기는 답변 본문 아래에 별도 블록으로 분리한다**.

---

## 2. 정규화 형식

### 답변 내 인용 (Inline Citation)
답변 본문에서는 번호만 표기합니다.
```
전통적 RAG는 텍스트 청크를 벡터 DB에 저장합니다 [1]. 
반면 GraphRAG는 엔티티와 관계를 추가로 추출합니다 [2].
```

### 인용 목록 (Citation Block)
답변 아래에 아래 형식으로 소스 매핑을 추가합니다.
```markdown
> **Citations**:
> - [1] GraphRAG vs. Traditional RAG (URL/PDF)
> - [2] GraphRAG vs. Traditional RAG (URL/PDF)
> - [3] 온톨로지 AI 에이전트 구축 완전 분석 (YouTube)
```

---

## 3. 소스 유형별 표기

| 소스 유형 | 표기 형식 | 예시 |
| :--- | :--- | :--- |
| **URL/웹페이지** | `{제목} (URL)` | GraphRAG Overview (URL) |
| **YouTube** | `{제목} (YouTube)` | 온톨로지 AI 구축 (YouTube) |
| **PDF** | `{제목} (PDF)` | Barth KD §59 (PDF) |
| **Pasted Text** | `{제목} (Text)` | 연구 노트 (Text) |
| **Google Docs** | `{제목} (GDoc)` | 프로젝트 기획서 (GDoc) |

---

## 4. 비정상 케이스 처리

| 상황 | 처리 |
| :--- | :--- |
| 답변에 인용 번호가 없음 | "출처를 포함하여 다시 답변해 주세요"로 재질의 |
| 동일 인용 번호가 다른 소스를 가리킴 | `source_describe`로 실제 소스 확인 후 수동 매핑 |
| "소스에 관련 정보 없음" 답변 | `미해결 과제(Open Questions)` 섹션에 기록 |

---
*NotebookLM Researcher 3.0 | Citation Mapping Reference*
