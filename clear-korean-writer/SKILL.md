---
name: clear-korean-writer
description: >
  Opt-in Korean prose polishing and AI-tell removal — reduces AI-generated
  patterns (translation-ese, structural tells, signature phrases) using a
  strict taxonomy while preserving facts, terminology, quotations,
  register, and intended uncertainty. Use when the user requests Korean
  editing, post-translation polishing, or humanizing AI text.
  키워드: 한국어 윤문, AI 말투 제거, 번역투 교정
version: 1.0.1
status: active
---

# Clear Korean Writer Protocol (v2.0)

## Objective
한국어 초안, 교정본, 번역 후 텍스트를 더 선명하고 자연스럽게 다듬으며, **LLM 특유의 AI 티(AI-Tell)를 수술적으로 제거**한다. 
단, 새 사실을 추가하지 않으며, 원문의 용어·인용·어조·불확실성은 엄격히 보존한다.

## References (SSOT)
윤문 작업 전, 아래의 두 단일 진실 원천(SSOT) 문서를 우선적으로 참조한다:
- **`references/ai-tell-taxonomy.md`**: 10대 분류(A~J) 40+ AI 티 탐지 패턴 및 심각도 기준
- **`references/rewriting-playbook.md`**: 카테고리별 구체적 치환 레시피 및 장르별 미세 조정 가이드

## Activation
- 기본값은 비활성이다.
- 사용자가 `clear-korean-writer`를 명시하거나, "한국어 문장 윤문", "교정", "AI 티 없애줘", "번역투 제거" 등을 직접 요청할 때만 사용한다.

## Guardrails (4대 철칙)
1. **의미 불변 (Fidelity First)**: 사실, 수치, 주장, 고유명사, 직접 인용, 법률/표준 문구는 100% 원문 보존한다.
2. **근거 기반 (Span-Grounded)**: 탐지된 패턴(finding) 구간에만 수술적으로 수정하며, 문제가 없는 구간은 건드리지 않는다.
3. **장르 유지 (Tone Match)**: 사용자가 요구한 어조와 장르를 우선 보존한다 (칼럼을 문학으로 바꾸지 않음). 신학/학술 문서의 경우 학술적 추상어나 독일어/영어 신학 용어는 예외적으로 보존한다.
4. **과윤문 금지 (No Over-Polish)**: 문장 전체를 새로 쓰는 것을 지양하며, 변경률이 30%를 초과하지 않도록 억제한다. 더 선명하게 쓸 수 있어도 의미나 뉘앙스가 달라지면 고치지 않는다.

## Core Style Priorities
세부 처방은 `rewriting-playbook.md`를 따르며, 핵심 원칙은 다음과 같다:

1. **A. 번역투 제거 (Translation-ese)**: `~에 대해`, `~를 통해`, `~에 있어`, `가지고 있다`, 기계적 피동태(`~되어진다`) 등을 자연스러운 조사와 능동태로 바꾼다.
2. **C. 구조적 AI 패턴 해체**: 기계적 병렬(`첫째/둘째/셋째`), 도식적 3단 공식(`먼저/반면/결국`), 불필요한 이모지 및 요약 박스를 해체하여 산문으로 녹인다.
3. **D. AI 관용구 삭제 (Signature Phrases)**: `결론적으로`, `시사하는 바가 크다`, `혁신적인`, 의인화된 추상 주어(`두 지능의 충돌이 질문을 던집니다`) 등 기계적 상투구를 구체적 서술로 치환하거나 삭제한다.
4. **E. 리듬 변주 (Rhythm Uniformity)**: 문장 길이와 종결 어미(`~이다`, `~한다` 반복)의 인공적인 균일성을 깨고 단문과 장문을 섞는다.
5. **F/H/I. 군더더기 및 명사화 축소**: 접속사 남발, 의존 명사 과다(`것이다`, `점`, `수`, `능력`), 의미 없는 진행형(`~고 있다`) 및 가능형(`~할 수 있다`)을 줄여 주어-동사 중심의 힘 있는 문장으로 만든다.

## Mode Selection
- **`humanize`**: **[New]** AI 티(AI-Tell) 제거 최우선 모드. 10대 카테고리 패턴을 적극 탐지하여 인간 필자의 리듬으로 재작성.
- **`minimal`**: 최소 개입, 원문 구조 및 의미 보존 최우선. 결정적(S1) 패턴만 제거.
- **`neutral`** *(기본값)*: 일반적인 명료화 및 가독성 개선.
- **`academic`**: 신학/학술 논지와 용어를 엄격히 보존하며, 학술적 완곡어는 허용하되 문장 밀도를 높이고 번역투를 제거.
- **`literary`**: 리듬과 어조를 살리되 과한 평준화 금지.

## Execution Workflow (3-Step Pipeline)
1. **[Intake]**: 텍스트와 장르(칼럼, 리포트, 신학 논문 등)를 파악한다.
2. **[Detect]**: `ai-tell-taxonomy.md`를 참조하여 보존 대상(인용문, 용어)과 AI 티 패턴(A~J) 및 심각도(S1/S2/S3)를 탐지한다.
3. **[Rewrite]**: `rewriting-playbook.md`의 레시피에 따라 탐지된 구간(Span)을 수술적으로 윤문한다. 
4. **[Audit]**: 사실, 용어, 양태가 보존되었는지(내용 훼손), 과도하게 문장이 바뀌지 않았는지(과윤문) 점검한다.
5. **[Output]**: 요청 형식에 맞춰 결과를 출력한다.

## Output Contract
- **기본값**: 최종 윤문본을 출력한다.
- **사용자 요청 시**: 핵심 수정 요약(Summary), 변경 전/후 비교(Diff), 탐지된 AI 티 패턴(Detection Report)을 덧붙인다.
