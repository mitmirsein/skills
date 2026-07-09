# 배선 경계 — 누가 무엇을 공격하는가

omni-academic-framework 안에는 "적대적 검증"이라는 같은 교리를 따르는 층위가 셋 있다. 서로를 호출하지 않으며, 각자의 대상과 실행 평면이 다르다. 이 경계를 흐리면 세 곳이 같은 말을 따로 유지하다 drift한다.

## 세 층위

| 층위 | 무엇을 공격하는가 | 실행 평면 | 위치 |
|---|---|---|---|
| `--llm-critic` | 렌즈 **분석 리포트** (자기 자신의 산출) | 파이썬 자동 패스 | `omni_academic/analyze/lens_analyzer.py` `build_llm_critic()` |
| review_panel의 Devil's Advocate | **초안(draft)** | 파이썬 peer-review 패스 | `lenses/review_panel.yaml` |
| **econ-redteam** (이 스킬) | **대상 문서 자체** — 정책안 또는 실증 논문 | 에이전트가 적용하는 프로토콜 | `.skills/econ-redteam` |

`--llm-critic`은 도메인 중립이며 자기 분석을 red-team한다. 이 스킬은 도메인 특화이며 **원본 텍스트의 경제학적 논증**을 공격한다. 둘은 대상이 다르므로 중복이 아니다.

## 파이프라인 상의 위치

omni의 실제 단계는 **Phase A(정찰) → B(HITL) → C(온톨로지) → D(렌즈별 정밀 타격)** 이다. 모듈 수준으로는 `recon → ontology → analyze → draft → review`.

econ-redteam은 이 코드 파이프라인의 **자동 단계가 아니다.** Phase D에서 economics 렌즈가 산출한 분석을 앞에 두고, 에이전트가 대상 문서에 직접 적용하는 적대 프로토콜이다. omni 코드는 이 스킬을 import하지도 호출하지도 않는다.

> 과거 SKILL.md에 있던 `Phase 3.5` 표기는 theology-redteam(TAWP Phase 3.5)에서 복사되며 딸려온 유령 표기였다. omni에는 그런 단계가 없다. v2.0.0에서 제거했다.

## economics 렌즈와의 역할 분리

`lenses/economics.yaml`의 `focus_areas` + `analysis_prompt`가 식별전략 분류, 핵심 가정 명시, 인과/상관 태깅, 외적타당성, 강건성 신호를 이미 지시한다.

- **렌즈** = 1차 분석 프롬프트. 무엇을 볼 것인가.
- **이 스킬** = 적대 프로토콜 + 결정론 게이트. 무엇을 공격하고, 무엇이 차단되는가.

`references/ex_post_axes.md`는 렌즈의 `focus_areas`를 커버리지 척추로 **상속**하고, 렌즈에 없는 항목(군집 표준오차·SUTVA·측정오차·표본선택·HTE·출판편향, 그리고 ex-ante 전 축)만 델타로 추가한다. 렌즈가 이미 지시하는 것을 이 스킬이 재나열하면 두 곳이 각자 낡는다.

렌즈를 고칠 때는 `ex_post_axes.md`의 델타 목록을 함께 본다. 렌즈에 항목이 추가되면 이 스킬에서는 델타에서 빼고 상속으로 옮긴다.

## 범위 경계 (omni ARCHITECTURE.md 상속)

grounding은 **산문 논증에만** 작동한다. 회귀표의 숫자 셀에는 작동하지 않는다. omni는 결과 검증기(results verifier)가 아니라 논증 분석기(argument analyzer)이며, 표값 추출과 리플리케이션은 의도적으로 범위 밖이다.

`scripts/econ_gate.py`의 grounding 검사는 대상 문서에서 마크다운 표 행과 코드 블록을 제거한 뒤 인용을 대조함으로써 이 경계를 **기계적으로** 강제한다. 계수를 공격하고 싶으면 그 계수를 해석하는 산문 문장을 인용하라.

## 정본과 미러

- 정본(canonical): `.skills/econ-redteam` — 여기서만 고친다.
- 미러: `projects/omni-academic-framework/skills/econ-redteam` — 복사만 받는다. 독립 개발하지 않는다.

정본을 고친 뒤 `python3 scripts/econ_gate.py sync`로 전파하고, `sync --check`로 drift를 확인한다. `tests/test_mirror_parity.py`가 sha256 바이트 동일을 강제한다(미러 부재 시 skip). 상세는 `CANONICAL_NOTICE.md`.
