---
name: langgraph-supervisor
description: >
  Orchestrates large multi-step jobs as a Supervisor-Worker state machine —
  plan, delegate to specialized workers (OCR, sanitizer, theologian, draft
  editor, quality auditor), review with feedback loops, and finalize, with
  human-interrupt checkpoints for costly or ambiguous steps. Use when a task
  is too large for one pass and needs a coordinated worker pipeline.
  키워드: 멀티에이전트 오케스트레이션, 감독관 파이프라인, 작업 분해
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#supervisor"
  - "팀으로 처리해줘"
  - "파이프라인으로 진행해줘"
references_path: ./references
---

# 👑 LangGraph Supervisor (감독관-작업자 오케스트레이션)

대규모 지령을 전문 작업자에게 분배하고 검수 루프로 품질을 보증하는 상태 기계 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- **Human Interrupt**: 모호하거나 비용이 큰 단계에서는 멈추고 사용자 결재를 받습니다.

## Phase 1 — 팀 구성 (정본: [team-topology.md](./references/team-topology.md))

- **Supervisor**: 계획 수립·작업 분해·검수(Critic)·승인 획득. 전체 컨텍스트 유지.
- **Workers**: OCR Specialist / Sanitizer / Theologian / Draft Editor / Quality Auditor —
  과업 성격에 맞게 필요한 역할만 기동.

## Phase 2 — 5단계 상태 루프 (정본: [state-machine-logic.md](./references/state-machine-logic.md))

```
[Init 계획] → [Delegate 위임] → [Execute 수행] → [Review 검수] → [Finalize 산출]
                      ↑__________________ Fail: 구체적 결함 명시 후 재작업 _____|
```

- 위임 시 작업자에게 현재 상태(State)와 임무를 명확히 정의해 전달합니다.
- Review에서 Pass면 다음 단계, Fail이면 결함을 명시해 피드백 루프를 돕니다.

## 검증·보고

- 최종 보고에 작업 분해 구조, 각 작업자의 산출물 검수 결과(Pass/Fail 이력),
  사용자 개입 지점을 명시합니다.
- Quality Auditor의 최종 레드팀 결과를 포함해야 완료를 선언할 수 있습니다.
