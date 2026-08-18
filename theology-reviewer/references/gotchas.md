# ⚠️ Theology Reviewer Gotchas (ARC v4.0)

> **"신학적 정밀함은 부주의한 용어 선택에서 무너진다."**

`theology-reviewer`를 수행하거나 비평을 작성할 때 반드시 피해야 할 '신학적 함정'과 '시스템 규격 위반' 목록입니다.

## 1. Terminology Pitfalls (용어 혼선 금지)
개신교 학술 신학(Academic Theology) 표준에 어긋나는 법적/일상적 용어 사용을 경계합니다.

| ❌ 피해야 할 용어 | ✅ 권장하는 용어 | 사유 |
| :--- | :--- | :--- |
| **계약 (Contract)** | **언약 (Covenant)** | 성경적 '베리트'는 일방적/상호적 인격 관계지, 법적 거래가 아님. |
| **법정적 (Legal)** | **법정적 (Forensic)** | 칭의론에서 'Forensic'은 법률 절차보다 하나님의 선언적 성격을 강조. |
| **도덕 (Morality)** | **윤리 (Ethics)** | 신학에서는 원칙적인 '윤리'를 개인의 '도덕'보다 학술적으로 선호. |
| **구원 (Save)** | **구원 (Salvation/Soteriology)** | 동사형보다는 명사형 체계로 기술 권장. |

## 2. ARC v4.0 Constitution Compliance
헌법(ARC v4.0)에 명시된 '물리 법칙'을 위반하지 않도록 주의합니다.

- **[No Hallmark Design]**: 비평 리포트의 디자인이 '기본'이어서는 안 됩니다. 명확한 가독성과 프리미엄한 구성(Mermaid 다이어그램, 꼼꼼한 테이블)을 갖추어야 합니다.
- **[Evidence Stewardship]**: 주석의 출처를 위조(Hallucination)하는 행위는 비평 시스템 전체의 파멸을 의미합니다. 모르는 출처는 모른다고 명시하고 `[Evidence_Missing]` 태그를 붙입니다.
- **[Tone]**: 비평의 어조는 단호하되 학자적 예의(Irenic)를 유지해야 합니다. 비난이 아닌 비평(Critique)을 지향합니다.

## 3. Structural Pitfalls (구조적 함정)
- **[No Numeric Scoring Only]**: 단순한 점수(1~5점)는 비평이 아닙니다. 왜 그 점수가 도출되었는지에 대한 '이중 관점(Dual Lens)'의 근거가 누락되면 안 됩니다.
- **[Boundary Violation]**: `210 Meditation` 구역의 개인적 고백을 학술 비평의 '공격 대상'으로 삼지 마십시오. 해당 구역은 절대적 격리 구역입니다.
- **[Terminology Standard]**: 한국 찬송가/성경 인용 시 개역개정(KRV/NKRV)을 기본으로 하되, 원문 비평 시에는 히브리어/헬라어 원어를 반드시 병기합니다.

## 4. Verification Guardrails
- **[Pass 0 Missing]**: `scholar-semantic`을 통한 외부 증거 수집 없이 자의적 분석만으로 비평을 종결하는 것은 'Half-Review'로 간주됩니다.
- **[Echo Chamber]**: 저자의 주장만을 반복하는 것은 '비평'이 아닌 '리뷰'입니다. 반드시 저자의 논증을 해체하고(Pass 1) 재구성(Pass 2)하는 과정을 거쳐야 합니다.

## 5. Dialectical Anti-patterns (변증법적 함정)
(출처: vibe-coding-skills/debate — Antigravity 선별 흡수 2026-05-01)

- **[Straw Man 금지]**: 저자의 주장을 비판하기 전에, **저자 자신이 100% 동의할 수준으로** 해당 주장을 한 문장으로 먼저 요약해야 합니다. 요약 없이 곧바로 반박에 들어가면 허수아비 논증(Straw Man)으로 간주하여 해당 비평 항목을 무효 처리합니다.
- **[Analysis Paralysis 탈출]**: 비평 과정에서 판정을 회피하며 무한 검토에 빠지는 것을 금지합니다. 모든 쟁점은 아래 두 범주 중 하나로 반드시 분류합니다:
  - **판정 가능**: 증거 기반으로 `✅ Anchored` / `❌ Contradicted` 판정을 즉시 내린다.
  - **판정 유보**: 현재 증거로 결론이 불가하면 `⚠️ Unverified — [구체적 사유]`로 명기하고 다음 쟁점으로 이동한다. 동일 쟁점에서 3회 이상 재검토 반복을 금지한다.

## 6. Logic Trap: Identifier Confusion (표면적 식별자 혼동 금지)
(출처: Karpathy의 "이메일 vs User ID" 역설 — 볼트 에이전트 헌장)

에이전트는 서로 다른 시스템(신학파)에 속한 '표면적으로 동일한 단어'를 '동일한 개념'으로 연결하려는 강한 본능(Vibe-matching)이 있습니다. Phase 2 검증 시 이 논리적 비약을 엄격히 통제해야 합니다.

- **[단어는 User ID가 아니다]**: Stripe의 이메일과 Google의 이메일이 같다고 같은 결제자가 아니듯, **신학에서 "단어가 같다고 같은 개념이 아닙니다."**
- **[Architectural Mismatch 방지]**: 논문에서 `시간(Time)`이나 `말씀(Word)`이라는 단어를 썼다고 해서, 그것이 `H 학파의 시간`이나 `바르트의 말씀`과 동일한 아키텍처를 가졌다고 자동 판정(`✅ Anchored`)해서는 안 됩니다.
- **행동 지침**: 서로 다른 학자의 텍스트를 교차 검증할 때, 단어(표면적 식별자)가 일치하더라도 그 배후의 **신학적 전제(Theological Architecture)**가 다르면 명시적으로 `❌ Contradicted` 또는 `⚠️ Unverified (Architecture Mismatch)` 처리를 해야 합니다.

---
*Verified for ARC v4.0 Policy — Updated 2026-05-01*
