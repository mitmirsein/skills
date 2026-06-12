---
name: continuous-learner
description: >
  Learns durable user preferences from session behavior — scaffolding
  questions, discovery of corrections and implicit preferences, then
  user-verified atomic instincts persisted to instincts.md with conflict
  resolution. Use when the user asks to capture lessons from a session or
  update working instincts. 키워드: 본능 학습, 선호 기록, 세션 회고
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#learn"
  - "이번 세션에서 배운 것 기록해줘"
  - "본능 업데이트해줘"
references_path: ./references
---

# 🌱 Continuous Learner (지속 학습기)

사용자의 교정·암시적 선호를 원자적 본능(Atomic Instinct)으로 정제해 영구 보존하는 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- **추측 본능 금지**: 사용자 확인 없이 본능을 확정·저장하지 않습니다.

## Phase 1 — SDE 루프 (정본: [sde-framework.md](./references/sde-framework.md))

1. **Scaffolding**: 메타인지 질문으로 의도 명확화 ("가장 효율적이었던 지점은?")
2. **Discovery**: 최근 대화에서 교정(Corrections)·암시적 선호 추출 → 신뢰도 점수를 단
   원자적 본능 공식화 → 사용자에게 가볍게 확인
3. **Evaluation & Persistence**: 확정 본능을 `projects/msn_th_db/instincts.md`에 저장.
   기존 본능과 충돌 시 사용자에게 우선순위를 묻고 갱신

## 연동

- `.skills/log-miner`가 채굴한 Tactical Instincts(🦁)를 이 스킬이 받아 정제·보존합니다.

## 검증·보고

- 새로 저장/갱신된 본능 목록과 신뢰도, instincts.md 변경 디프 요지를 보고합니다.
