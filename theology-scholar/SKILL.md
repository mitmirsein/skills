---
name: theology-scholar
description: >
  Top-tier theological research engine ('Cathedral') — primary-text analysis
  (PAF), hypothesis generation, argumentation TDD, SBL-standard writing, and
  a 7-stage merciless audit under phase gates with convergence criteria. Use
  when the user asks for deep theological scholarship, thesis construction,
  or rigorous critique (heavier than theology-research's survey wrapper).
  키워드: 신학 심층 연구, 논증 감사, 학술 집필
version: 6.0.1
codename: Gated Cathedral
triggers:
  - "#scholar"
  - "#audit-th"
  - "신학 연구 및 감사 수행해줘"
  - "theological research & audit"
  - "perform thorough scholarship on [topic]"
capabilities:
  - primary_text_internal_logic_mapping
  - notebooklm_mcp_delegation
  - aporia_identification_concilium
  - red_green_refactor_argumentation
  - merciless_cathedral_audit
  - sbl_chicago_master_formatting
  - rgg_tre_ekl_contextual_verification
  - recursive_self_critique_protocol
  - anti_bluffing_verification
  - verification_harness
references_path: "./references"
status: active
---

# ⛪ Theology Scholar (The Cathedral Engine) 6.0

## 1. Overview
'Theology Scholar'는 신학적 사유의 발견(Discovery)부터 무자비한 감사(Audit)까지의 전 과정을 관장합니다. 연구 프로세스는 반드시 **Verification Harness**를 통한 데이터 검증을 선행합니다. 특히 **Phase 0: Primary Analysis First(PAF)**를 통해 외부 학설과의 대조 전, **'텍스트 자체의 내적 논리'**를 완벽하게 해부하여 비평의 기초를 다집니다. 방대한 문헌 조우 시 **NotebookLM MCP**로 1차 분석을 위임하는 결속력을 갖추고 있습니다.

## 1.1 Pipeline State Diagram (Phase Gate Architecture)
각 Phase는 명시적 **진입 조건(Entry Gate)**과 **종료 조건(Exit Gate)**을 가진다. Gate를 통과하지 못하면 다음 Phase로 진행할 수 없다.

```
[START]
  │
  ▼
 Phase 0 (PAF)  ──Entry: 텍스트 존재 + Verification Harness PASS
  │                Exit: 뼈대(Skeleton) + 내적 균열(Fissure) ≥ 1건 식별
  ▼
 Phase 1 (Aporetics)  ──Entry: PAF 뼈대 문서 존재
  │                      Exit: 비평적 가설 ≥ 1건 수립 + 🔲 HITL 승인
  ▼
 Phase 2 (TDD Arena)  ──Entry: 승인된 가설 존재
  │                      Exit: 수렴 판정(Convergence ≥ 0.90) 또는 Hard Cap
  ▼
 Phase 3 (Writing)  ──Entry: TDD 통과 논증 세트
  │                    Exit: SBL 규격 초안 완성
  ▼
 Phase 4 (Audit)  ──Entry: 초안 문서 존재
  │                  Exit: 7-Stage 전 항목 PASS + 🔲 HITL 감사 결과 수용
  ▼
 Phase 5 (Red Team)  ──Entry: Audit PASS
  │                     Exit: Anti-Bluffing PASS
  ▼
[DELIVER]
```

> 🔲 = 사용자 결재(HITL) 필수 지점. 에이전트가 자동으로 넘기지 않는다.

## 2. Dynamic Workflow: The Cathedral Protocol
본 스킬 가동 시 **사유의 함정(Gotchas)**과 **위원회 규모(Config)**를 즉시 필터링합니다.

### Phase 0: Primary Analysis First (PAF: 1차 분석)
- **Entry Gate**: 분석 대상 텍스트가 물리적으로 존재하며, `Verification Harness`가 인용/메타데이터 정확성을 PASS 판정.
- **Mandatory Verification**: 모든 문헌 분석 시작 전 `Verification Harness`를 가동하여 인용 및 메타데이터의 정확성을 강제 검증합니다.
- **Standard PAF**: 텍스트 전반의 핵심 용어와 논리적 뼈대(Skeletal Structure), 내적 모순(Internal Fissure)을 추출합니다.
- **NotebookLM Routing (HITL)**: 대규모 문헌(단행본, 주석서 등) 분석 요청 시, 사용자의 명시적 승인(Human-in-the-Loop)을 거쳐 문헌 전체를 `NotebookLM MCP`로 오프로딩(Offloading)하여 1차 구조 해체 및 아포리아 심문을 외부 지능에 위임합니다.
- **Exit Gate**: 논리적 뼈대(Skeleton) 문서 생성 완료 + 내적 균열(Fissure) 최소 1건 식별. 미달 시 텍스트 재독 또는 분석 범위 조정.

### Phase 1: Aporetics & Discovery (Aporetics)
- **Entry Gate**: Phase 0의 뼈대(Skeleton) 문서가 존재.
- **Identify Gaps**: 분석된 텍스트를 RGG, TRE, EKL과 대조하여 연구사(Forschung)의 공백을 식별합니다.
- **Hypothesis**: 기존 학설과의 긴장을 유발하는 비평적 가설을 제안합니다.
- **Exit Gate + 🔲 HITL**: 비평적 가설 최소 1건 수립. **사용자가 가설의 방향성을 승인**해야 Phase 2로 진입. 사용자는 가설을 수정·기각·추가할 수 있다.

### Phase 2: Logic Hardening (Argumentation TDD)
- **Entry Gate**: 사용자 승인(🔲 HITL)을 받은 비평적 가설이 존재.

단일 AI의 합의 편향(Consensus Bias)을 깨기 위해 두 가지 트랙으로 분리 가동합니다.
- **Track A (Standard Mode)**: Sequential Thinking MCP의 인지 구획화를 이용해 일상적 논증을 빠르게 공격(Red)하고 방어(Green)합니다.
- **Track B (Arena Mode)**: 논리적 텐션을 극대화하기 위해, 공격 파일(`.md`)을 출력 후 즉시 사고를 끊어내고(Cold Reboot) 전혀 다른 페르소나로 재접근하여 물리적으로 격리된 문서 릴레이 논박을 수행합니다.

#### 🔁 Arena 수렴 종료 조건 (Convergence Gate)
논박 라운드가 무한히 계속되거나, 반대로 성급하게 합의에 도달하는 것을 방지합니다. 상세 알고리즘은 [convergence-gates.md](./references/convergence-gates.md)를 참조.

| 측정 축 | 가중치 | 의미 |
|:---|:---:|:---|
| **Thesis Stability** | 50% | 핵심 테제가 이전 라운드와 변경 없으면 1.0 |
| **Evidence Novelty** | 30% | 새로운 근거가 추가되지 않으면 1.0 |
| **Concession Delta** | 20% | 양보 사항이 이전 라운드와 동일하면 1.0 |

- **Convergence ≥ 0.90** → "논증 포화(Saturation)" → Phase 3으로 이행.
- **5라운드 Hard Cap** → 안전장치. 수렴 미달이라도 강제 종료 후 현재까지의 최선 논증 채택.
- ⚠️ **Aporia 보호**: 수렴이 양극의 타협/중간값을 의미하지 않는다. Phase 3에서 양극을 병렬 기술하는 것이 올바른 수렴이다.

- **Exit Gate**: Convergence ≥ 0.90 판정 또는 Hard Cap 도달. TDD를 통과한 논증 세트가 존재.

### Phase 3: Synthesis & Style (Writing)
- **Entry Gate**: Phase 2의 TDD 통과 논증 세트가 존재.
- **Organization**: 시카고 기반 SBL 2판 규격에 맞춰 논문을 설계합니다.
- **Drafting**: 학술적 경외와 정밀함이 조화된 문체로 초안을 작성합니다.
- **Exit Gate**: SBL 규격 초안 문서 완성 (제목, 초록, 본문, 각주, 참고문헌 구비).

### Phase 4: Merciless Audit (The Cathedral Editor)
- **Entry Gate**: Phase 3의 SBL 규격 초안 문서가 존재.
- **7-Stage Audit**: 초록, 서론, 논증, 문법, 인용 등 7개 영역에 대해 무자비한 감사를 수행합니다.
- **Exit Gate + 🔲 HITL**: 7-Stage 전 항목 PASS. **감사 결과 보고서를 사용자에게 제시하고, 수정 지시 또는 수용을 결재**받은 후 Phase 5로 진입.

### Phase 5: Cathedral Red Team (Self-Red Team)
- **Entry Gate**: Phase 4 Audit PASS + 사용자 결재(🔲 HITL) 완료.
- **Recursive Critique**: 감사 결과 자체의 AI 편향 및 블러핑 여부를 `#criticalthink` 로직으로 최종 검열합니다.
- **Exit Gate**: Anti-Bluffing Check PASS → **[DELIVER]** 최종 산출물 제출.
  *   **⚠️ 산출물 보존 위치 원칙**: 최종 산출물을 포함한 모든 중간 문서(Skeleton, Hypothesis, Arena_Log, Draft 등)는 기본적으로 작업을 수행하는 로컬 개발 공간(예: `MS_Dev.nosync/scratch/` 또는 호출된 작업 디렉토리) 내에 생성 및 통합 보존해야 한다. Obsidian 볼트(`MS_Library.nosync` 또는 `MS_Thoughts.nosync`)로 직접 발행하거나 이관하는 행위는 사용자의 명시적 지시가 있는 경우에만 수행하며, 임의로 볼트 경로에 파일을 생성하지 않는다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): 학술적 타협 및 환각 방지 가이드.
- [verification-harness.md](./references/verification-harness.md): 인용 및 데이터 검증 필수 프로토콜.
- [audit-protocol.md](./references/audit-protocol.md): (v6.0) 1차 분석(Phase 0) 및 7단계 감사 프로토콜.
- [sbl-style-guide.md](./references/sbl-style-guide.md): 시카고 기반 SBL 스타일 및 메타데이터 규격.
- [writing-methodology.md](./references/writing-methodology.md): 변증법적 종합 및 신학 TDD 공정 설계 가이드.
- [convergence-gates.md](./references/convergence-gates.md): ⚡ Phase Gate 조건 명세 및 Arena 수렴 종료 알고리즘.

---
