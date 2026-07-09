---
name: econ-redteam
description: >
  Adversarially attacks economic policy proposals (ex-ante) and empirical econometric work (ex-post),
  targeting financing, incidence, and behavioral response for the former, identification and inference
  for the latter, and grounding every critique in a verbatim quote from the source prose.
  Use when the user asks to red-team a policy proposal or budget bill, critique public spending,
  or audit econometric identification in an empirical paper.
  키워드: 경제학 레드팀, 경제 정책 비평, 계량경제학 검증, 인과관계 식별, 적대적 정책 검증
version: 2.0.0
status: active
author: MS_Dev
triggers:
  - "/econ-redteam"
  - "@econ-redteam"
  - "경제 정책 레드팀"
  - "경제학 비평"
  - "계량 검증"
references_path: ./references
---

# 📈 econ-redteam — 경제 정책 적대적 검증

경제 정책 제안과 실증 연구의 논증을 공격한다. 모든 지적은 원문 산문의 인용에 정박해야 하며, 형식·정박·커버리지는 결정론 게이트가 판정한다.

파이프라인 위치: omni `recon → ontology → analyze[economics 렌즈]` 뒤에 에이전트가 적용하는 적대 프로토콜이다. 코드 자동 단계가 아니다(`references/wiring.md`).

---

## Phase 0 — 가드레일

분석 시작 전 `references/gotchas.md`를 반드시 읽는다. 함정은 양방향이다 — 과잉 비판(루카스 남용·RCT 강요)과 과소 비판(허수아비·낙관 기준선 수용·옹호로의 미끄러짐) 둘 다 실패다.

세 원칙을 지킨다.

1. **코드는 형식의 판사, 에이전트는 실질의 판사.** 게이트는 존재·정박·enum·커버리지만 차단한다. 지적이 참인가, 반론이 최강인가, 대상이 그것을 대면했는가는 코드가 선언하지 않는다.
2. **산문 논증만 공격한다.** 회귀표의 숫자 셀을 재계산하거나 리플리케이션하지 않는다. 계수를 문제 삼으려면 그 계수를 해석하는 산문 문장을 인용한다.
3. **아포리아를 평탄화하지 않는다.** 목표 충돌은 단일 결론으로 뭉개지 않고 `aporia[]`에 보존한다.

---

## Phase 1 — 모드 판별

```bash
python3 scripts/econ_gate.py classify --target <문서>
```

코드는 어휘 tally로 **자문 신호만** 낸다(항상 exit 0). 판별은 에이전트가 선언한다.

- 실현된 산출 데이터에 묶인 인과 추정이 있으면 → **ex-post**
- 미래 개입 제안이고 실현 outcome 데이터가 없으면 → **ex-ante**
- 제안부와 실증부를 함께 가지면(정책 평가 논문) → **mixed**

ex-ante 문서에는 공격할 식별 전략이 애초에 없다. 거기에 평행 추세 침해를 들이대는 것이 이 스킬이 고친 가장 큰 결함이다(gotcha ⑧). 게이트가 `mode=ex-ante` + `axis=E*`를 형식 오류로 차단한다.

---

## Phase 2 — 축 가동

선언한 모드의 축만 가동한다. 각 축마다 최소 1건의 지적이 필요하다.

| 모드 | 축 | 참조 |
|---|---|---|
| ex-ante | A1 재원·기회비용·반사실 기준선 · A2 분배·조세귀착 · A3 행태반응(굿하트) · A4 정치경제·집행·시간비일관성 · A5 불확실성·꼬리위험 | `references/ex_ante_axes.md` |
| ex-post | E1 식별·내생성 · E2 추론·강건성 · E3 외적타당성·이질성·일반균형 | `references/ex_post_axes.md` |
| mixed | 양쪽 모두. A축은 `part=proposal`, E축은 `part=empirical`로 태깅 | 두 파일 모두 |

ex-post 축은 `lenses/economics.yaml`의 `focus_areas`를 커버리지 척추로 상속하고, 렌즈에 없는 항목만 델타로 더한다. 렌즈는 분석 렌즈이고 이 스킬은 적대 프로토콜이다. 같은 항목을 두 곳에서 유지하지 않는다.

---

## Phase 3 — 출력 계약 v2

마크다운 4개 섹션과 JSON 비평 패킷을 **함께** 낸다. 전체 스키마는 `references/output_contract.md`.

1. `[Leap-Alert]` — 인과 입증이 붕괴한 지점
2. `[Evidence-Check]` — 아전인수 인용, 넓은 신뢰구간, 추론·강건성 결함
3. `[Concept-Tension]` — 목표 충돌. 여기 오는 항목은 `aporia[]`에도 등록한다
4. `[Policy-Directives]` — hand-off 지침 (비점수 부록)

각 공격 지적은 다음을 필수로 갖는다.

- `source_quote` — 원문 산문의 verbatim 앵커 (없으면 유령 비판)
- `steelman` — 때리기 전 그 주장의 최강 버전 (없으면 허수아비)
- `falsification_condition` — 무엇이 나오면 이 지적이 철회되는가
- `axis` · `severity` · (mixed면) `part`

판정 슬롯(`verdict` · `is_strongest` · `engaged_by_target` · `aporia[].verdict`)은 `UNJUDGED`로 남긴다. 채우는 것은 별도의 판정 패스다.

**Policy-Directives 격리**: 처방은 발견을 철회할 수 없다. 각 directive는 `refs`로 다루는 `critique.id`를 참조하며, 커버리지·심각도 집계에서 제외된다. 성격은 정책 지지가 아니라 리서치 쿼리다.

---

## Phase 4 — 결정론 게이트

```bash
# 필수 — 형식·정박·커버리지 (단발 판정)
python3 scripts/econ_gate.py check --critiques packet.json --target <문서> \
    [--paragraphs paragraphs.json] [--fail-on-schema --fail-on-ungrounded \
     --fail-on-missing-axis --fail-on-mode-unset]

# 선택 — 실질 판정 (판정 패킷 이디엄)
python3 scripts/econ_gate.py prepare --critiques packet.json --out worklist.json
# → 판정 슬롯을 증거에서 채운 뒤
python3 scripts/econ_gate.py decide --worklist worklist.json \
    [--fail-on-strawman --fail-on-unengaged --fail-on-flattened]
```

종료 코드: `0` 통과 또는 자문 · `1` 스크립트 내부 오류 · `2` 입력 오류 또는 hard 게이트 실패.

**도입 곡선**: 처음에는 `--fail-on-*` 없이 리포트-only로 운용한다. 게이트가 무엇을 잡는지 확인한 뒤 하나씩 차단으로 격상한다. 모든 게이트를 처음부터 exit 2로 강제하면 게이트 피로가 스킬을 죽인다.

---

## 배선 경계

omni 안에 적대적 검증 층위가 셋 있고, 서로를 호출하지 않는다.

- `--llm-critic`(`build_llm_critic()`)은 **렌즈 분석 리포트**를 red-team하는 도메인 중립 자동 패스다.
- review_panel의 Devil's Advocate는 **초안**을 공격한다.
- econ-redteam은 **대상 문서 자체**를 공격한다.

대상이 다르므로 중복이 아니다. 상세와 정본·미러 규약은 `references/wiring.md`.

---

## 검증·보고

성공 조건: `check`가 exit 0이고, 모든 공격 지적이 grounding을 통과했으며, 모드가 선언됐고, 선언된 모드의 모든 축에 최소 1건의 지적이 있다.

스킬 자체의 건강성은 아래로 확인한다.

```bash
python3 scripts/econ_gate.py sync --check     # 정본↔미러 drift 0 (미러에서 실행하면 skip)
python3 -m unittest discover -s tests         # 게이트 단위 테스트 (정본 전용, 미러엔 없음)
```

행동 회귀는 `evals/evals.json`이 다룬다(모드 선언·축 커버·앵커·steelman).

보고 시 실제로 실행한 게이트의 출력만 인용한다. 체크리스트 자기보고를 게이트 통과로 보고하지 않는다.
