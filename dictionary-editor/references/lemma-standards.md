# Dictionary Editor: Lemma Standards & YAML Schema

신학 사전 표제어(Lemma)의 다국어 표기 규약 및 YAML Frontmatter 스키마 명세입니다.

---

## 1. 다국어 표기 규약 (Multilingual Lemma)

| 필드 | 언어 | 예시 | 규칙 |
|---|---|---|---|
| `lemma_en` | 영어 | `"Justification"` | 학술 사전 표준 표기 |
| `lemma_de` | 독일어 | `"Rechtfertigung"` | TRE 항목 표기 우선 |
| `lemma_grc` | 고대 헬라어 | `"δικαίωσις"` | 원문 그대로 |
| `lemma_heb` | 히브리어 | `"צְדָקָה"` | 원문 그대로 |

- TRE(`~/Desktop/MS_Dev.nosync/data/tre_terms.csv`)에 존재하는 용어는 반드시 TRE ID와 독일어 표기를 포함해야 합니다.
- TRE에 없는 경우 `tre_id: ""` 비워둡니다.

---

## 2. YAML Frontmatter 전체 스키마 (ARC v4.0 표준)

```yaml
---
aliases: []
tags: [Dictionary, Concept]
zone: ""          # 100(신학) or 400(인문학)
lemma_en: ""
lemma_de: ""
lemma_grc: ""
lemma_heb: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft     # draft | review | wiki | canonical

# ── 의미론적 관계 (Semantic Relations) ─────────────────────────────────────
# 관계 유형: opposes | precedes | grounds | participates_in | exemplifies
#            is_about | depends_on | structural_ally | prescribes_solution
# 범주(scope): ontological | soteriological | ecclesiological | eschatological
relations:
  - target: "[[대상 표제어]]"   # 연결 대상
    type: ""                    # 관계 유형 (위 목록에서 선택)
    scope: ""                   # 신학적 범주 (위 목록에서 선택)
    note: ""                    # 선택적 한 줄 설명

# ── 신학적 긴장 (Aporia Guard — Tension Preservation) ──────────────────────
# ⚠️ AI의 Tension Flattening을 방지하는 가드레일.
# pole_a와 pole_b가 모두 존재해야 이 항목은 완전합니다.
tensions:
  - id: ""                      # 예: T1_믿음_vs_행위
    pole_a: ""                  # 긴장의 한 극단 (주장 A)
    pole_b: ""                  # 긴장의 반대 극단 (주장 B)
    status: "unresolved"        # unresolved | partial | resolved
    note: ""                    # 이 긴장이 왜 해소될 수 없는지 한 줄
---
```

---

## 3. 관계 유형 사전 (Relation Type Glossary)

| 유형 | 의미 | 예시 |
|---|---|---|
| `opposes` | 두 개념이 정면 충돌함 | 칭의 `opposes` 공로 교리 |
| `precedes` | A가 B의 선행 조건 | 회개 `precedes` 칭의 |
| `grounds` | A가 B의 논리적 근거 | 그리스도의 순종 `grounds` 칭의 |
| `participates_in` | A가 B의 일부분 | 칭의 `participates_in` 구원론 |
| `exemplifies` | A가 B의 구체적 사례 | 세례 `exemplifies` 언약 |
| `is_about` | A가 B를 주제로 삼음 | 갈라디아서 `is_about` 칭의 |
| `depends_on` | A가 B 없이 성립되지 않음 | 칭의 `depends_on` 그리스도의 대속 |
| `structural_ally` | 공통 위협을 가진 개념적 동맹 | 칭의 `structural_ally` 성화 |
| `prescribes_solution` | A가 B의 위협에 대한 해결책 제시 | 복음 `prescribes_solution` 율법의 정죄 |

---

## 4. 완결성 판별 기준 (Completion Gate)

에이전트가 `status: draft` → `status: review`로 승격하기 전 반드시 확인:

- [ ] `lemma_en` 또는 `lemma_de` 중 하나 이상 채워짐
- [ ] `relations` 블록에 최소 1개 항목 (type + target 필수)
- [ ] `tensions` 블록: `pole_a` + `pole_b` 모두 채워짐 (신학적 긴장이 없는 단순 서술 항목은 제외 가능)
- [ ] 본문 섹션 4 (Disputes/Aporia)에 Tension Zone 기술 완료

---
*Created for ARC v4.0 — Semantic Relations + Aporia Guard Protocol*
