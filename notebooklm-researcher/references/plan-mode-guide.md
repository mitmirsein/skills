# ⚡ Plan Mode Guide: 사전 질문 설계 심화 가이드

> **Origin**: SourceLoop의 'Plan-first' 접근법을 MS_Dev 환경에 맞게 재설계.
> NotebookLM MCP를 통해 질문-답변을 일괄 수행하는 전략 문서.

---

## 1. 언제 Plan Mode를 사용하는가?

- 사용자가 **낯선 도메인**에 대한 포괄적 이해를 요구할 때
- **긴 영상/논문**의 핵심을 빠르게 추출할 때
- 단일 질문으로는 포착 불가능한 **다면적 주제**를 분석할 때
- 콘텐츠 생산(강의, 블로그, 카드뉴스)을 위한 **원재료 확보** 목적

---

## 2. 질문 설계 프로토콜

### Step 1: 주제와 목표 수신
대장에게 아래 두 가지를 반드시 확인합니다.
- **주제 (Topic)**: 연구할 대상 (예: "온톨로지 기반 AI 에이전트 구축")
- **목표 (Goal)**: 연구의 최종 용도 (예: "강의자료 제작", "논문 석의", "블로그 포스팅")

### Step 2: 6축 질문 생성
Sequential Thinking MCP를 활용하여 아래 6개 축에 따라 질문을 분배합니다.

```
총 질문 수: 8~15개 (주제 복잡도에 따라 조절)

축별 최소 배분:
- 정의(Definition): 1~2개
- 역사(History): 1~2개
- 구조(Structure): 2~3개
- 논쟁(Controversy): 1~2개
- 적용(Application): 1~2개
- 연결(Connection): 1~2개
```

### Step 3: 질문 품질 검증
생성된 질문이 아래 기준을 충족하는지 자기 검증합니다.

| 기준 | 통과 조건 |
| :--- | :--- |
| **구체성** | "더 알려줘"가 아닌, 특정 개념/인물/사건을 지목하는가? |
| **독립성** | 각 질문이 서로 중복되지 않고 독립적 정보를 추출하는가? |
| **인용 유도** | "근거를 포함하여" 또는 "출처와 함께"라는 지시가 포함되어 있는가? |
| **목표 정합** | 질문의 답변이 최종 목표(강의/논문/블로그)에 직접 활용 가능한가? |

### Step 4: 일괄 실행
```
for each question in question_set:
    response = mcp_notebooklm_notebook_query(notebook_id, question)
    normalize_citations(response)
    append_to_report(question, response)
```

- **실행 간격**: 각 질문 사이 2~3초의 의미적 간격을 두어 NotebookLM의 문맥 혼동을 방지합니다.
- **오류 처리**: 답변이 "소스에 관련 정보가 없습니다"로 오면, 해당 질문을 `미해결 과제`로 분류합니다.

---

## 3. 인용 정규화 규칙 (Citation Mapping)

NotebookLM 답변의 인용을 아래 형식으로 정규화합니다.

**입력 (Raw)**:
```
면역학자는 의학 연구와 깊게 연결되어 있고 [2], [3]
```

**출력 (Normalized)**:
```
면역학자는 의학 연구와 깊게 연결되어 있고 
**Citations**: [GraphRAG vs. Traditional RAG][2], [GraphRAG vs. Traditional RAG][3]
```

---

## 4. 실전 예시: "온톨로지 구성방법" 연구

**주제**: 온톨로지 구성방법
**목표**: 학습 자료 제작

**생성된 질문 세트**:
1. [정의] 온톨로지(Ontology)의 학술적 정의와 지식 표현에서의 역할은 무엇인가?
2. [역사] 온톨로지 개념은 철학에서 컴퓨터 과학으로 어떻게 전이되었는가?
3. [구조] 온톨로지의 핵심 구성요소(Class, Property, Instance, Axiom)는 각각 무엇인가?
4. [구조] 온톨로지와 단순 Taxonomy의 구조적 차이는 무엇인가?
5. [논쟁] 전통적 RAG와 GraphRAG의 핵심 트레이드오프는 무엇인가?
6. [논쟁] 온톨로지 구축의 진입장벽과 그 극복 전략은?
7. [적용] 기업 환경에서 온톨로지를 AI 에이전트 구축에 적용하는 구체적 단계는?
8. [적용] Syntax과 Semantics 접근의 실무적 차이와 선택 기준은?
9. [연결] 온톨로지는 Knowledge Graph, Linked Data와 어떤 관계인가?
10. [연결] 온톨로지 설계가 LLM 기반 AI의 성능에 미치는 영향은?

---
*NotebookLM Researcher 3.0 | Plan Mode Reference*
