---
title: Theological Writing & Research Methodology
version: 6.0 (Gated Cathedral)
---

# 🖋️ Theological Writing & Research Methodology

'Theology Scholar'는 단순 집필을 넘어 1차 분석(PAF)부터 가설 발견, 논증 검정, 최종 감사 및 자가 비판까지의 전 과정을 통합된 방식으로 수행합니다.

## ⛪ Phase 0: Primary Analysis First (PAF)
> **Entry Gate**: 텍스트 존재 + Verification Harness PASS | **Exit Gate**: Skeleton 문서 + Fissure ≥ 1건

모든 분석의 출발점은 텍스트 자체에 대한 심층적 침잠입니다.
- **Skeletal Mapping**: 외부 학설을 배제하고 오직 저자의 내부 논리와 용어 사용의 일관성, 그리고 의도적 침묵(Silence)을 추적합니다.
- **NotebookLM Offloading (HITL)**: 수백 쪽에 달하는 대규모 단행본이나 주석서를 조우할 경우, 사용자의 승인을 거쳐 텍스트 분석을 방대하고 정확한 RAG 엔진인 `NotebookLM MCP`로 오프로딩(Offloading)하여 압축된 핵심 아포리아(Aporia)만을 1차 인계받습니다.

## 🏗️ Phase 1: Aporetics & Discovery (Aporetics)
> **Entry Gate**: Skeleton 문서 존재 | **Exit Gate**: 비평적 가설 ≥ 1건 + 🔲 HITL 승인

신학적 '발견'은 지식의 공백(Aporia)을 찾는 것에서 시작합니다.
- **Contextual Search**: RGG, TRE, EKL 등 거대 전문 문헌을 횡단하여 기존 학설의 '긴장'을 탐색합니다.
- **Hypothesizing**: 발견된 난제에 대해 현 상황(Status Quaestionis)을 돌파할 비평적 가설을 세웁니다.

## 🧱 Phase 2: Logic Hardening (Theology TDD - Dual Track)
> **Entry Gate**: 승인된 가설 존재 | **Exit Gate**: Convergence ≥ 0.90 또는 Hard Cap (5라운드)

세워진 가설을 학술적 요새(Fortress)로 구축합니다. 목적에 따라 두 가지 모드로 분리 작동합니다.

### Track A: Standard Mode (Sequential Thinking MCP)
일상적인 신학 개념의 비교 및 정리에 사용되며, 강제 구획된 인지를 통해 빠르게 레드팀과 그린팀을 오갑니다.
- **Red Team (Critique)**: 가설의 취약점을 선제적으로 공격하여 논리의 허점을 노출시킵니다.
- **Green Patch (Verification)**: 다중 사전(BDB, HALOT, BDAG) 및 독일어권 신학백과사전(RGG, TRE, EKL), 그리고 1차 문헌을 활용하여 반론을 격파하고 논거를 요새화합니다.

### Track B: Arena Mode (File System Handoff / 문서 릴레이 방식)
기존 학설의 전복이나 첨예한 대립이 필요한 최상위 난제에만 가동합니다.
- **Physical Wall**: AI의 합의 편향(Consensus Bias)을 강제로 절단하기 위해, Red Team의 논박을 `/tmp/` 등의 물리적 마크다운 파일로 저장한 뒤 프로세스를 일시 정지합니다.
- **Cold Reboot**: 이후 정반대의 페르소나(Green Team)로 다시 기동하여, 자신의 이전 생각을 지운 채 물리적 파일의 내용만을 100%의 적대감으로 반박하여 극한의 논리적 긴장감을 도출합니다.

### 🔁 Arena 수렴 종료 조건
논박 라운드의 종료 시점은 정량적으로 판정한다. 상세 알고리즘과 병리 패턴 감지 규칙은 [convergence-gates.md](./convergence-gates.md)를 참조.
- **Convergence ≥ 0.90** → 논증 포화 → Phase 3 이행
- **5라운드 Hard Cap** → 안전장치
- **1라운드 즉시 합의(Convergence = 1.0)** → ⚠️ 합의 편향 의심 → 최소 2라운드 강제

## ✍️ Phase 3: Synthesis & Drafting (Writing)
> **Entry Gate**: TDD 통과 논증 세트 | **Exit Gate**: SBL 규격 초안 완성

검색과 검증을 마친 재료들을 서사적으로 엮습니다.
- **Dialectical Design**: 상반된 입장들을 정-반-합의 논리로 대조하여 고유한 통찰을 도출합니다.
- **SBL/CMOS Standard**: 시카고 스타일 기반의 SBL 2판 규격으로 문장과 각주를 정밀하게 구성합니다.

## 👓 Phase 4: Merciless Audit (The Editor)
> **Entry Gate**: 초안 문서 존재 | **Exit Gate**: 7-Stage PASS + 🔲 HITL 수용

독설적 에디터 페르소나를 투영하여 결과물을 파괴적으로 검증합니다.
- [audit-protocol.md](./audit-protocol.md)의 7단계 체크리스트(Audit 0~7)를 엄격하게 적용합니다.

## 🛡️ Phase 5: Cathedral Red Team (Self-Critique)
> **Entry Gate**: Audit PASS + 사용자 결재 | **Exit Gate**: Anti-Bluffing PASS → [DELIVER]

감사 결과 자체를 다시 한번 검증하여 AI 블러핑과 편향을 제거합니다.
- 비평의 근거가 실존하는지, 시대적 맥락에 부합하는지 최종 필터링합니다.

---
