# 🧠 Thoughtbox Patterns Cookbook

> **Progressive Disclosure**: 이 파일은 SKILL.md에서 "Mental Models가 필요하면 참조하라"고 지시할 때만 로드한다.
> 평소에는 로드하지 않아 컨텍스트를 절약한다.

---

## Mental Models (15종)

각 모델은 **이름 | 언제 쓰나 | 핵심 질문** 형태로 압축되어 있다.

| # | 모델명 | 적합 상황 | 핵심 질문 |
| :---: | :--- | :--- | :--- |
| 1 | **Five Whys** | 근본 원인 분석 | "왜?" 를 5번 반복 |
| 2 | **Pre-mortem** | 계획 실패 예측 | "이 계획이 실패했다고 가정하면, 원인은?" |
| 3 | **Steelmanning** | 반대 입장 강화 | "상대방의 가장 강력한 논변은?" |
| 4 | **Trade-off Matrix** | 대안 비교 | "각 옵션의 비용/이익을 2x2 매트릭스로" |
| 5 | **Decomposition** | 복잡한 문제 분할 | "이 문제를 독립된 하위 문제 3개로 나누면?" |
| 6 | **First Principles** | 가정 제거 | "우리가 당연시하는 전제를 제거하면?" |
| 7 | **Inversion** | 역발상 | "이것을 최악으로 만들려면 무엇을 해야 하나?" |
| 8 | **Second-order Effects** | 파급 효과 분석 | "이 결정의 2차, 3차 결과는?" |
| 9 | **Occam's Razor** | 가설 선택 | "가장 적은 가정으로 설명하는 가설은?" |
| 10 | **Falsification** | 가설 검증 | "이 가설이 틀렸음을 증명할 반례는?" |
| 11 | **Analogy Mapping** | 낯선 문제 해결 | "비슷한 구조를 가진 이미 해결된 문제는?" |
| 12 | **Constraint Analysis** | 자원 제한 최적화 | "가장 큰 병목(bottleneck)은 어디인가?" |
| 13 | **Dialectic** | 종합적 결론 도출 | "정(Thesis) ↔ 반(Antithesis) → 합(Synthesis)" |
| 14 | **Scenario Planning** | 불확실성 대비 | "최선/최악/가장 가능성 높은 시나리오는?" |
| 15 | **Red Team** | 보안/품질 검증 | "내가 이것을 공격/파괴한다면 어디를 노리겠나?" |

---

## 복합 패턴 (Compound Patterns)

여러 모델을 연쇄하는 고급 패턴:

### 패턴 A: 탐색→수렴 (Diverge-Converge)
```
[순방향 + Decomposition] → [분기 + Trade-off Matrix] → [수렴 + Occam's Razor]
```
복잡한 열린 문제를 분해 → 대안 탐색 → 최적 해 선택

### 패턴 B: 역공학 (Reverse Engineering)
```
[역방향 + First Principles] → [순방향 + Constraint Analysis]
```
목표에서 출발점까지 역추적 → 현실 제약조건으로 실행 가능성 검증

### 패턴 C: 적대적 검증 (Adversarial Validation)
```
[순방향으로 가설 생성] → [분기 + Red Team + Falsification] → [수정(Revision)]
```
가설을 세운 뒤 적극적으로 파괴 시도 → 살아남은 가설만 채택

### 패턴 D: 신학적 변증 (Theological Dialectic)
```
[순방향 + Steelmanning 양 진영] → [Dialectic 종합] → [역방향으로 설교/논문 구조화]
```
신학 논쟁의 양 입장을 최강으로 강화 → 변증적 종합 → 목표 산출물로 역구조화
