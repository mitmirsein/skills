---
name: notebooklm-researcher
description: >
  Operates NotebookLM as a consolidated research library — multi-source
  acquisition over 5 channels (KCI/RISS + Semantic Scholar + Google Scholar
  ×2 + NLM research_start), Plan-mode batch questioning, recursive Dive
  reasoning, and audio/slide generation. Use when the user asks to research
  with NotebookLM, build a notebook, or consolidate sources into one
  library. 키워드: 노트북LM 연구, 단권화, 소스루프, 리서치 플랜
version: 3.2.1
codename: Third Gen — Multi-Source Edition
triggers:
  - "#nlm"
  - "NotebookLM 연구해줘"
  - "내 노트북에서 찾아줘"
  - "소스루프"
  - "리서치 플랜"
capabilities:
  - plan_mode_batch_questions
  - smart_discovery
  - recursive_follow_up
  - deep_research_expansion
  - citation_mapping
  - notebook_library_indexing
  - error_mining_and_gotcha_avoidance
references_path: "./references"
status: active
---

# 🧠 NotebookLM Researcher 3.2 (Multi-Source Edition)

국내(KCI/RISS) + 해외(S2 API / Google Scholar ×2 / NLM research_start) **5채널 멀티소스
파이프라인**으로 자원을 확보하고(세션당 15~25건 목표), Plan/Dive/Scout + 오디오/슬라이드
생성을 통합한 연구 런타임.

## 1. 연구 모드

| 모드 | 목적 | 최적 시나리오 |
| :--- | :--- | :--- |
| **Plan Mode** ⚡ | 다각도 질문 세트 사전 생성 후 일괄 질의 | 새 도메인의 빠른 전방위 이해 |
| **Dive Mode** 🔬 | 재귀적 꼬리물기 심층 탐구 | 신학적 논쟁, 학술 배경의 뿌리 추적 |
| **Scout Mode** 🌐 | 외부 웹/드라이브에서 신규 소스 발굴·추가 | 연구 초기 문헌 탐색, 주제 확장 |
| **KCI/RISS Pipe** 📡 | 국내 학술 DB 발굴 → 노트북 임포트 | 국내 논문 단권화 — [kci-riss-pipeline.md](./references/kci-riss-pipeline.md) |
| **Multi-Source** 🌐² | 5채널 동시 발굴 | 국내+해외 완전 자원 확보 — [multi-source-pipeline.md](./references/multi-source-pipeline.md) |
| **Create Mode** 🎙️ | 소스를 오디오/슬라이드로 변환 | 설교·강의 준비 — [nlm-content-creation.md](./references/nlm-content-creation.md) |

## 2. Dynamic Workflow

### Phase 0: Setup & Guardrail
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 반드시 읽고 연구 함정을 점검.
- **Auth Verify**: NotebookLM MCP 인증 확인. 401/403 시 `mcp_notebooklm_refresh_auth`.
- **Notebook Identify**: 대상 노트북 ID 확인 — 없으면 `notebook_list` 검색 또는 신규 생성.
- **Source Inventory**: `notebook_get`으로 소스 목록 파악 후 연구 범위 결정.

### Phase 1: Plan Mode ⚡ (사전 질문 설계)
1. 연구 주제(Topic)·목표(Goal) 수신
2. 6축(정의·역사·구조·논쟁·적용·연결)으로 질문 세트 8~15개 자동 생성
   — 축별 정의·예시 정본: [plan-mode-guide.md](./references/plan-mode-guide.md)
3. `mcp_notebooklm_notebook_query`로 일괄 실행
4. Citation을 `[소스명][인용번호]` 형식으로 정규화 ([citation-mapping-spec.md](./references/citation-mapping-spec.md))
5. 전체 Q&A를 구조화 마크다운으로 종합

### Phase 2: Dive Mode 🔬 (재귀적 심층 추론)
1. **Smart Discovery**: `notebook_describe`로 전체 맥락·제안 토픽 확보
   ([smart-discovery-guide.md](./references/smart-discovery-guide.md))
2. **Recursive Follow-up**: 답변의 정보 공백(Gap) 식별 → 꼬리 질문
   - Gap 규칙: 불확실성 마커("~일 수 있다") / 미정의 신규 용어 / 단일 관점 서술 → 후속 질문
   - **탈출 조건**: 3회 연속 동일 소스만 인용되거나 정보 증분이 무시 가능할 때 종료
   - 꼬리 질문 패턴 정본: [recursive-query-patterns.md](./references/recursive-query-patterns.md)
3. 추론 경로(Chain of Thought)를 시각화하여 보고

### Phase 3: Scout Mode 🌐 (외부 소스 발굴)
1. `mcp_notebooklm_research_start` — `mode: fast`(~30초, ~10개) / `mode: deep`(~5분, ~40개)
2. `mcp_notebooklm_research_status`로 진행 모니터링
3. 유관 소스 선별 → `mcp_notebooklm_research_import`로 노트북 추가
4. 새 소스 포함 Plan/Dive Mode 재가동

### Phase 4: Synthesis & Report
최종 결과를 [research-report-template.md](./templates/research-report-template.md) 규격
(연구 개요 / 핵심 발견 / Q&A 아카이브 / 미해결 과제 / 소스 인벤토리)으로 종합 보고한다.

## 3. Mode Selection Decision Tree

```
사용자 요구 수신
│
├─ "전반적으로 파악해줘" / "빠르게 정리" / "전방위 분석"   → ⚡ Plan Mode
├─ "이 논점을 깊이 파줘" / "근거를 추적해"                → 🔬 Dive Mode
├─ "관련 자료 더 찾아줘" / "웹에서 검색해"                → 🌐 Scout Mode
└─ "완전히 연구해줘" / "단권화해줘" / 복합 요청           → Scout → Plan → Dive (Full Pipeline)
```

## 4. 검증·보고

- 보고서에 사용 모드, 소스 수, 질문 수를 명시하고, 모든 핵심 주장에 Citation을 단다.
- 인용이 확인되지 않는 진술은 보고서에 넣지 않거나 [미확인]으로 표기한다 (gotchas 참조).

---
*MCP Runtime: notebooklm-mcp-cli v0.6.10 | 소스 채널: KCI · RISS · S2 API · Google Scholar ×2 · NLM research_start*
