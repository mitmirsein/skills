---
name: theology-evidence-writing
description: >
  Use when writing theology notes, doing biblical exegesis, or building a
  theological claim that should rest on evidence — before asserting anything
  you cannot yet cite. Guards against unsupported assertions and against
  premature flattening of theological tension.
  키워드: 문헌 증거 주도, 주해 주도, exegesis driven, EDD, 증거 없는 주장 방지, 아포리아 보존, 증거 우선 글쓰기
version: 2.0.0
author: MS_Dev
triggers:
  - "문헌 증거 주도"
  - "주해 주도"
  - "exegesis driven"
  - "edd 루프"
  - "EDD"
capabilities:
  - evidence_first_discipline
  - context_based_exegesis
  - hermeneutical_refactoring
  - terminology_consistency_advisory
status: active
---

# 🛡️ theology-evidence-writing (EDD): 증거-우선 주해 규율

신학·인문학의 독단적 주장과 비약을 막기 위해, 모든 논증을 문헌 증거에 정초시켜 전개하도록 강제하는 **자기완결(self-contained) 글쓰기 규율**. 소프트웨어 TDD의 Red-Green-Refactor 를 주해에 이식했다. 이 스킬은 외부 스크립트나 로컬 프로젝트에 의존하지 않는다(단일 노트용 경량 규율).

> ⚖️ 신학 텐션 보존: 논리적 모순·아포리아를 다수설로 평탄화하지 않는다.

**letter = spirit** — 규율의 문구를 우회하는 것은 규율의 정신을 위반하는 것이다. "이번 건은 예외"는 없다.

---

## 🔴 1단계: 증거 수집 (Red)

증거 없이는 어떤 신학 주장도 본문에 쓸 수 없다. 먼저 1차 사료(성경 구절·헬라어/히브리어 원어)와 2차 문헌(주석·논문)의 발췌를 증거 테이블로 선행 작성한다.

| ID | 출처·위치 | 발췌 Verbatim / 원어 분석 | 증명 요지 |
| :-- | :-- | :-- | :-- |
| `EV-01` | 요 1:1a | "In the beginning was the Word (Logos)" | 로고스의 영원한 선존성 |
| `EV-02` | Brown, Anchor Yale Bible (1966) p.4 | "Logos represents the creative power…" | 구약 다바르·지혜 전통과의 연계 |

통제 규칙: 테이블에 없는 주장을 본문에 쓰면 **Red 실패** — 되돌아가 증거부터 확보한다.

(see-also: TAWP 파이프라인으로 논문을 쓴다면 같은 규율을 CLI 하드게이트로 강제하는 `claim-ledger` (Phase 7)가 있다. EDD 는 그 경량 노트 버전이다.)

## 🟢 2단계: 주해 서술 (Green)

확보된 `EV-*` 범위 안에서만 서술한다. 원어의 어휘·역사 문맥을 반영해 주해하고, 각 주장에 증거 코드(`[EV-01]`)를 명시해 추적 가능하게 한다. 테이블 밖 지식으로 살을 붙이고 싶으면 먼저 Red 로 돌아가 새 `EV-*` 를 등록한다.

## 🔵 3단계: 해석학적 퇴고 (Refactor)

1. **텐션 복원** — 억지 봉합·다수설 평탄화가 있으면 긴장 관계로 재분리한다.
2. **용어 일관성 (자문)** — 한 개념의 한국어 표기 혼용(예: 언약/계약)을 하나로 통일(canonical)한다. 표준 참조로는 TRE(신학 용어 표준 사전)를 **폴백** 용도로만 참고하고, 의미·정의는 선행연구·1차문헌과의 정합으로 판단한다(단일 사전의 정의 권위를 강제하지 않는다). 이 단계는 발행을 막는 pass/fail 게이트가 아니라 **자문(경고)** 수준이다. (TAWP 에선 `theology-terminology-linter` 가 같은 검사를 수행한다.)
3. **서지 교정** — 각주·인용을 SBL 등 지정 포맷으로 정리한다.

---

## 🚩 Red Flags — 멈추고 Red 로 돌아가라

- "이 주장은 자명해서 증거가 필요 없다"
- "근거는 나중에 붙이면 된다"
- "이건 그냥 메모/초안이라서"
- "요지는 맞으니 출처는 대충"
- "letter 말고 spirit 만 지키면 된다"

## 합리화 차단표

| 합리화 | 실제 |
| :-- | :-- |
| "자명한 주장이라 증거 생략" | 자명해 보이는 주장이 가장 자주 날조된다. 근거 확인은 30초. |
| "나중에 근거 추가" | 근거 없는 초안은 이미 Red 실패. 지금 되돌아간다. |
| "메모/초안일 뿐" | 메모도 `EV-*` 없이는 본문 진입 금지. |
| "다수설이니 텐션 봉합" | 평탄화는 아포리아 삭제다. 긴장으로 재분리. |
| "TRE 에 없으니 아무 역어나" | 표기는 canonical 로 통일, TRE 는 폴백. 의미는 1차문헌 정합. |

## When NOT to use

- 완성 논문 **비평/리뷰** → `theology-reviewer`
- 집필 전 **적대적 갭·비약 공격** → `theology-redteam`
- **전체 논문 파이프라인** (검색→온톨로지→집필→감사) → `tawp`
- 논쟁 관계 **시각화** (RDF·Mermaid) → `theology-discourse-mapper`
