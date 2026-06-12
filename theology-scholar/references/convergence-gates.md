# ⚡ Convergence Gates: Phase Gate 조건 명세 및 Arena 수렴 알고리즘

본 문서는 'Theology Scholar' v6.0의 Phase Gate Architecture를 상세 규정한다.
설계 원칙: **"명확해질 때까지 만들지 않고, 안정될 때까지 진화를 계속한다."**

---

## 1. Phase Gate 조건 일람

모든 Phase는 **Entry Gate**(진입 조건)와 **Exit Gate**(종료 조건)를 가진다.
Gate를 충족하지 못하면 다음 Phase로 진행할 수 없다.

| Phase | Entry Gate | Exit Gate | HITL |
|:------|:-----------|:----------|:----:|
| **0 (PAF)** | 텍스트 존재 + Verification Harness PASS | Skeleton 문서 + Fissure ≥ 1건 | — |
| **1 (Aporetics)** | Skeleton 문서 존재 | 비평적 가설 ≥ 1건 수립 | 🔲 가설 방향 승인 |
| **2 (TDD Arena)** | 승인된 가설 존재 | Convergence ≥ 0.90 또는 Hard Cap | — |
| **3 (Writing)** | TDD 통과 논증 세트 | SBL 규격 초안 완성 | — |
| **4 (Audit)** | 초안 문서 존재 | 7-Stage 전 항목 PASS | 🔲 감사 결과 수용 |
| **5 (Red Team)** | Audit PASS + 사용자 결재 | Anti-Bluffing PASS | — |

### Gate 미충족 시 행동 규정
- **Entry Gate 미충족**: 이전 Phase로 되돌아가 Exit 조건을 재달성한다.
- **Exit Gate 미충족**: 현재 Phase 내에서 반복 시도하되, 3회 연속 실패 시 사용자에게 상황을 보고하고 결재를 요청한다.
- **HITL 결재 거부**: 사용자의 수정 지시에 따라 해당 Phase의 산출물을 교정한 뒤 Exit Gate를 재시도한다.

---

## 2. Arena 수렴 종료 알고리즘 (Phase 2 전용)

### 2.1 목적
Arena Mode(Track B)의 공격/방어 릴레이 논박이 **무한 반복**되거나,
반대로 AI의 합의 편향으로 **1라운드 만에 성급한 합의**에 도달하는 것을 방지한다.

### 2.2 수렴 측정 공식

```
Convergence = 0.5 × thesis_stability + 0.3 × evidence_novelty + 0.2 × concession_delta
```

| 측정 축 | 가중치 | 정의 | 점수 산정 |
|:--------|:------:|:-----|:---------|
| **Thesis Stability** | 50% | 핵심 테제(주장)가 이전 라운드와 동일한가? | 변경 없음 = 1.0, 부분 수정 = 0.5, 전면 교체 = 0.0 |
| **Evidence Novelty** | 30% | 새로운 텍스트 근거가 추가되었는가? | 추가 없음 = 1.0, 1건 추가 = 0.7, 2건+ = 0.3 |
| **Concession Delta** | 20% | 양보(인정) 사항이 이전 라운드와 동일한가? | 동일 = 1.0, 1건 변경 = 0.5, 전면 변경 = 0.0 |

### 2.3 종료 조건

| 조건 | 임계값 | 결과 |
|:-----|:------:|:-----|
| **수렴(Convergence)** | ≥ 0.90 | "논증 포화" → Phase 3으로 이행 |
| **Hard Cap** | 5라운드 | 수렴 미달이라도 강제 종료, 최선의 논증 세트 채택 |
| **조기 합의 차단** | 1라운드 종료 시 Convergence = 1.0 | ⚠️ 경고: "합의 편향 의심" → 최소 2라운드 강제 수행 |

### 2.4 병리적 패턴 감지

| 패턴 | 감지 조건 | 대응 |
|:-----|:---------|:-----|
| **정체(Stagnation)** | 2라운드 연속 Convergence ≥ 0.95 | 정상 수렴으로 간주, 종료 |
| **진동(Oscillation)** | Round N의 테제 ≈ Round N-2의 테제 (교대 반복) | "논박이 두 입장 사이를 왕복 중" 경고 → 제3의 관점 도입 시도 |
| **무한 발산** | 3라운드 연속 Convergence < 0.5 | "수렴 불가" 판정 → Hard Cap 대기 없이 즉시 종료, 양극 병렬 보존 |

### 2.5 라운드 기록 형식

각 Arena 라운드 종료 시, 다음 형식으로 내부 상태를 기록한다:

```
Round {N}:
  Thesis: {현재 핵심 테제 1문장 요약}
  New Evidence: {추가된 근거 목록 또는 "없음"}
  Concessions: {인정한 반론 목록 또는 "없음"}
  Convergence: {0.00 ~ 1.00}
  Status: CONTINUE | CONVERGED | HARD_CAP | OSCILLATION | DIVERGENT
```

---

## 3. Aporia 보호 원칙 (절대 지침)

> **수렴(Convergence)은 양극의 타협이나 중간값 합성을 의미하지 않는다.**

- 신학적 긴장(Aporia)이 발견되면, 그것을 해소하는 것이 아니라 **구조화**하는 것이 목표다.
- Phase 3(Writing)에서 양극을 `## 3b. ⚡ 신학적 긴장 (Aporia Zone)` 섹션에 병렬 기술한다.
- Convergence 판정 시 양측이 "서로의 존재를 인정하되 합치하지 않는 상태"도 정당한 수렴이다.

---
*Created for Theology Scholar v6.0 (Gated Cathedral) — Ouroboros convergence pattern adapted for theological domain*
