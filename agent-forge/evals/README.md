# Agent Forge: Skill Evaluation Framework

> **"작동한다고 느끼는 것"과 "실제로 더 낫다는 것"은 다르다.**
> With-Skill vs Baseline 비교로만 스킬의 효과를 증명할 수 있다.

---

## 개요

이 프레임워크는 **Harness Testing Doctrine**을 기반으로,
`agent-forge`가 생성한 스킬이 실제로 Baseline(스킬 미사용)보다 더 나은지 검증한다.

### 현재 등록된 테스트 케이스

| 스킬 | 케이스 수 | 난이도 커버리지 |
|---|---|---|
| `agent-forge` | 3케이스 (AF-01~03) | Basic / Advanced / Expert |
| `theology-searcher` | 2케이스 (TS-01~02) | Basic / Advanced |
| `bible-meditation` | 2케이스 (BM-01~02) | Basic / Advanced |

---

## 테스트 실행 절차

### Step 1: 테스트 케이스 선택

```bash
# evals.json에서 실행할 케이스 ID 확인
cat evals/evals.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for skill in d['skills']:
    print(f\"\\n[{skill['skill_id']}]\")
    for tc in skill['test_cases']:
        print(f\"  {tc['id']}: {tc['label']}\")
"
```

### Step 2: With-Skill 실행

선택한 테스트 케이스의 `with_skill_prompt`를 에이전트에 입력한다.

```
# 예시 — AF-01 실행
프롬프트: "신학 논문의 참고문헌 목록(BibTeX 또는 주석 형태)을 입력받아 
SBL 규격으로 자동 변환해주는 에이전트 스킬을 설계해줘. #forge"

출력을 evals/_results/{케이스ID}_with_skill.md 에 저장
```

### Step 3: Baseline 실행

**동일한 세션에서 스킬을 비활성화한 후**, `baseline_prompt`를 입력한다.

```
# 예시 — AF-01 Baseline
프롬프트: "신학 논문의 참고문헌 목록(BibTeX 또는 주석 형태)을 입력받아 
SBL 규격으로 자동 변환해주는 에이전트 스킬을 설계해줘."
(#forge 트리거 없이 실행)

출력을 evals/_results/{케이스ID}_baseline.md 에 저장
```

### Step 4: Assertion 채점

`evals.json`의 `assertions` 목록을 하나씩 체크한다.

```
각 Assertion에 대해:
  ✅ PASS: 출력에 조건이 충족됨
  ❌ FAIL: 조건 미충족

3개 이상 FAIL → 스킬 수정 필요
0 FAIL → 배치 승인
```

### Step 5: 결과 기록

```bash
# 수동으로 evals/_results/summary.md 에 기록
Date: YYYY-MM-DD
Skill: agent-forge v5.2.0
Case: AF-01
With-Skill Assertions: 5/5 PASS
Baseline Assertions:   2/5 PASS
Delta: +3 assertions → 스킬 효과 확인됨
```

---

## 새 스킬 배치 시 체크리스트

`agent-forge`가 새 스킬을 생성할 때, 배치 전 반드시 다음을 확인한다.

```
[ ] evals.json에 해당 스킬의 테스트 케이스 2개 이상 추가됨
[ ] 핵심 사용 사례(Basic) 1개 포함
[ ] 엣지 케이스(Advanced) 1개 포함
[ ] 각 케이스에 최소 3개의 Assertion 정의됨
[ ] With-Skill 실행 결과 모든 Assertion 통과
[ ] Baseline 대비 최소 2개 이상의 Assertion에서 우위 확인
[ ] _results/summary.md에 결과 기록됨
```

---

## 디렉토리 구조

```
evals/
├── README.md           ← 이 파일 (테스트 실행 절차)
├── evals.json          ← 테스트 케이스 정의 (핵심)
└── _results/           ← 실행 결과 저장소 (자동 생성)
    ├── AF-01_with_skill.md
    ├── AF-01_baseline.md
    └── summary.md
```

---

## Assertion 작성 규칙

새 스킬의 테스트 케이스를 `evals.json`에 추가할 때 따를 원칙:

1. **존재 확인이 아닌 의미 확인**: `"SKILL.md가 있는가?"`가 아니라 `"YAML frontmatter가 올바르게 작성되었는가?"`
2. **부정 Assertion 포함**: With-Skill이 하면 안 되는 것(Hallucination 방지, 무한 루프 등)도 정의
3. **측정 가능한 조건**: `len(output) > 500` 같은 정량 기준 혼합
4. **도메인 특화**: 스킬의 전문 용어나 고유 산출물(예: SBL 형식, 묵상 아티클)을 assertion에 포함

---

*MS_Dev Agent Forge Eval Framework v1.0 — Harness Testing Doctrine 기반*
*2026.03.29 구축*
