# Dictionary Editor: Standard Article Structure

신학 백과사전식 아티클(Dictionary Entry)을 작성하기 위한 표준 목차와 집필 가이드입니다.

## 📝 Required Sections
1. **정의 (Definition)**: 해당 용어에 대한 가장 간결하고 명확한 신학적 정의 기술.
2. **역사 및 발전 (History)**: 개념의 성서적 기원, 교회사적 변천 및 근현대적 재발견 과정.
3. **교파/전통별 관점 (Confessional Perspectives)**: 가톨릭, 루터교, 개혁주의, 성공회 등 주요 교파 간의 강조점 차이.
4. **주요 신학 논쟁 (Key Debates)**: 과거 및 현대 신학계에서 벌어지는 주요 쟁점과 긴장 관계.
   > ⚠️ **Tension Preservation Rule**: 이 섹션에서 AI는 양 극단(pole_a / pole_b)을 타협적 중간값으로 합치면 안 된다. 해소되지 않은 역설은 역설 그대로 기술하며, 이것이 frontmatter `tensions` 블록의 본문 확장이 된다.
5. **1차 근거 문헌 (Primary Sources)**: 성경 구절, 공의회 결정문, 케리그마적 신조 등의 직접 인용 (필수).

## ⚖️ Drafting Principles
- **Neutrality**: 특정 교파의 입장에 편향되지 않고, 학술적 객관성을 유지하며 기술합니다.
- **Evidence-Based**: 모든 기술적 단락은 신뢰할 수 있는 1차 또는 2차 문헌에 근거해야 합니다.
- **Tension Preservation (Aporia Guard)**: 신학적 역설과 긴장은 해소하지 않는다. frontmatter `tensions` 블록의 `pole_a` / `pole_b`가 모두 채워져야 아티클이 완성된 것으로 간주한다.
- **Semantic Linking (의미론적 링크)**: 본문 내 다른 신학 용어 출현 시 단순 `[[Link]]` 대신, 가능한 경우 frontmatter `relations` 블록에 관계 유형(type)과 신학적 범주(scope)를 명시한다.
  - 관계 유형 어휘: `opposes` | `precedes` | `grounds` | `participates_in` | `exemplifies` | `depends_on` | `structural_ally` | `prescribes_solution`
  - 신학적 범주: `ontological` | `soteriological` | `ecclesiological` | `eschatological`

---
*Updated for ARC v4.0 — Semantic Relations + Aporia Guard Protocol*
