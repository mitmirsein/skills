# Meta-Harness Optimization Loop (Outer-Loop Optimization)

## 🎯 개요 (Overview)
Meta-Harness는 단일 에이전트의 프롬프트나 가중치를 수정하는 것을 넘어, **"에이전트를 감싸고 있는 실행 환경과 논리 구조(Harness) 자체를 탐색하고 최적화하는 기법"**입니다.
`agent-forge` v6.0부터 도입된 이 기능은, 단순한 스킬 1회성 생성을 넘어 **기존 스킬이 실행되며 남긴 날것의 로그(Raw Execution Traces)를 파일시스템 레벨에서 수집·분석하여, 스킬의 본체(`SKILL.md` 및 하위 스크립트)를 자율적으로 재작성(Self-Correction via Traces)하는 메타 에이전트(Outer-Loop Agent)** 역할을 수행합니다.

## 🧠 기본 철학 (Core Philosophy)
- **요약본에 의존하지 않는다 (No Compressed Feedback)**: 단일 점수(Scalar Score)나 요약된 평가 결과만으로는 하네스 레벨의 원인 추적이 불가능합니다. 항상 **원시 실행 추적**(도구 호출 내역, JSON 파싱 내역, 내부 사고 과정, 에러 메시지)을 있는 그대로 확인해야 합니다. 단, 추적 로그의 위치는 **런타임에 따라 다르며 보장되지 않습니다** — Claude Code 환경에는 고정된 `brain/<conversation-id>/logs` 경로가 없습니다. 따라서 추적 출처는 (a) 사용자가 명시한 로그/트랜스크립트 경로, (b) 대상 스킬이 직접 남긴 산출 로그(예: `evals/_results/`, 스킬별 `*.report.md`), (c) 현재 대화 맥락 중 실제 존재가 확인된 것만 사용합니다. 경로를 추측해 지어내지 마십시오.
- **코드 공간에서의 탐색 (Search in Code-Space)**: 프롬프트뿐만 아니라, `SKILL.md` 내부의 제약 조건, Workflow 로직, 자원 검색 방식(Retrieval Strategy) 등을 구조적으로 수정합니다.
- **인과적 디버깅 (Causal Reasoning Over Failures)**: 실패 사례를 단순히 보완하는 문구를 추가하는 것에 그치지 않고, "왜 이 단계에서 에이전트가 헤매었는가?"라는 구조적 병목(예: 불필요한 확인 루프, 불명확한 검색어 지정, 초기 컨텍스트 부족)을 찾아 제거합니다.

## 🔄 워크플로우 (Phase 5: Meta-Harness Optimization)

### 1단계: Data Gathering (파일시스템 스캔)
- 추적 가능한 출처를 **존재 확인 후** 식별합니다: 사용자가 지정한 로그/트랜스크립트 경로, 대상 스킬이 남긴 산출물(`evals/_results/`, `*.report.md` 등), 또는 현재 대화 맥락. 경로가 확인되지 않으면 추측하지 말고 사용자에게 추적 소스를 요청합니다.
- `grep`, `cat`, `Read` 등으로 실패 지점(에러 메시지, 반복된 도구 호출, Audit 실패 등)의 흔적(Execution Traces)을 수집합니다.

### 2단계: Causal Diagnosis (인과적 진단)
- 성공한 Trace와 실패한 Trace를 비교 분석합니다.
- **어디서 문제가 발생했는가?**
  - 프롬프트 템플릿의 모호성?
  - 도구(Tool) 호출 시 파라미터 전달의 한계?
  - 컨텍스트 오버플로우(너무 많은 정보)?
  - 과도한/부족한 Retrieval 로직?

### 3단계: Code-Space Evolution (하네스 재작성)
- 진단 결과를 바탕으로 대상 스킬의 `SKILL.md` 또는 관련 스크립트, `config.json`, `references/` 파일들을 직접 수정(Patch)합니다.
- 수정 사항은 "구조적이고 명시적인 해결책"이어야 합니다.
  - 예: 단순히 "주의해라"라고 쓰는 것이 아니라, "질문하기 전에 항상 `check_files` 도구를 먼저 호출하라"와 같이 행동(Action) 레벨의 제약을 부여.

### 4단계: Validation & Archiving
- 최적화된 하네스가 정상적으로 작동하는지 검증(Validation)하거나 사용자의 승인을 받습니다.
- 변경된 내용은 버전 업그레이드와 함께 `history.log` 또는 커밋 메시지에 구체적인 Trace 기반 이유를 포함하여 기록합니다.

---
*Reference: Lee et al., "Meta-Harness: End-to-End Optimization of Model Harnesses" (2026)*
