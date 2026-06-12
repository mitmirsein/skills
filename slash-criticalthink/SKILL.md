---
name: slash-criticalthink
description: >
  Self red-teams the AI's own just-produced answer (code, architecture,
  paper outline) — dismantling it against a critique framework and pitfall
  checklist to counter confirmation and authority bias. Use when the user
  invokes #criticalthink or asks the AI to attack its own proposal.
  키워드: 비판적 검증, 자가 레드팀, 답변 해체
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#criticalthink"
  - "#비판"
  - "#검증"
  - "#레드팀"
  - "방금 답변을 비판적으로 검토해줘"
  - "/criticalthink"
capabilities:
  - self_red_teaming_analysis
  - logical_fallacy_detection
  - ai_hallucination_evasion_audit
  - risk_and_mitigation_scenario_planning
  - self_critique_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# 🕵️ Critical Think 3.0 (Red Team)

## 1. Overview
자신이 내놓은 답변에 대해 비판적 분석가(Red Team)로 돌변하여 약점과 숨겨진 가정을 폭로하는 자가 검증 스킬입니다.

## 2. Dynamic Workflow
본 비판 수행 전 **분석 함정(Gotchas)**과 **비판 심도(Config)**를 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 비판 대상의 영역(코드/신학/전략) 및 비판 강도를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 형식적 비판(알랑방귀) 및 대안 없는 파괴를 방지합니다.

### Phase 1: Thesis Deconstruction
핵심 논지를 요약하고 해결책이 무너질 수 있는 치명적 가정을 식별합니다. 프레임워크는 [critique-framework.md](./references/critique-framework.md)를 참조하십시오.

### Phase 2: Multi-Layer Audit
논리적 비약과 AI 특유의 실패 모델을 점검합니다. 체크리스트는 [ai-pitfall-checklist.md](./references/ai-pitfall-checklist.md)를 참조하십시오.

### Phase 3: Synthesis & Action
리스크를 분석하고 수정된 확신도와 근본적 대안을 제시합니다. 비판 모드 해제 안내문과 함께 종료합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 형식적 비판 방지 및 건설적 대안 제시 가이드.
- [critique-framework.md](./references/critique-framework.md): 비판 7단계 표준 구조 명세.
- [ai-pitfall-checklist.md](./references/ai-pitfall-checklist.md): 문제 회피, 과잉 엔지니어링 및 사실 정확성 평가 기준.

---
*Created by MS_Dev Third Gen Standard*
