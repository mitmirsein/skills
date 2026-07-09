# 출력 계약 v2 — 비평 패킷 스키마

레드팀 리포트는 사람이 읽는 마크다운 4개 섹션과, 게이트가 읽는 JSON 비평 패킷 **두 형태로 동시에** 산출한다. 마크다운은 서술이고, JSON은 판정 대상이다.

## 1. 패킷 스키마

```json
{
  "schema_version": 1,
  "mode": "ex-ante | ex-post | mixed",
  "target_ref": "<대상 파일 경로 또는 omni run 식별자>",
  "critiques": [
    {
      "id": "C1",
      "section": "Leap-Alert | Evidence-Check | Concept-Tension",
      "axis": "A1|A2|A3|A4|A5|E1|E2|E3",
      "part": "proposal | empirical | null",
      "severity": "blocking | major | minor",
      "paragraph_id": "P_0007",
      "source_quote": "대상 산문에서 글자 그대로 복사한 앵커",
      "critique": "공격 본문",
      "steelman": "때리는 주장의 최강 버전",
      "falsification_condition": "이 지적을 해소할 증거 또는 분석",
      "engaged_by_target": "UNJUDGED",
      "is_strongest": "UNJUDGED",
      "verdict": "UNJUDGED"
    },
    {
      "id": "D1",
      "section": "Policy-Directives",
      "refs": ["C1", "C3"],
      "critique": "이 지적들을 판가름할 추가 분석·데이터·변수"
    }
  ],
  "aporia": [
    {
      "name": "단기 부양 대 장기 구조 전환",
      "poles": ["즉각적 총수요 보전", "지대 고착 없는 산업 재편"],
      "critique_id": "C4",
      "verdict": "UNJUDGED"
    }
  ]
}
```

## 2. 필드 정의

| 필드 | 의미 | 누가 채우는가 |
|---|---|---|
| `mode` | 대상 문서 유형 선언 | 에이전트 (코드는 자문만) |
| `axis` | 어느 축의 공격인가 | 에이전트 |
| `part` | mixed에서 제안부/실증부 중 어디를 때리는가 | 에이전트 |
| `severity` | 정책 결정에 미치는 무게 | 에이전트 |
| `paragraph_id` | omni `paragraphs.json`의 키 (`P_0001` 형식) | 에이전트, 게이트가 실존 검증 |
| `source_quote` | 원문 산문의 verbatim 앵커 | 에이전트, 게이트가 포함 검증 |
| `steelman` | 때리기 전 대상 주장의 최강 버전 | 에이전트 |
| `falsification_condition` | 무엇이 나오면 이 지적이 철회되는가 | 에이전트 |
| `engaged_by_target` | 대상이 이 반론을 대면했는가 (`대면`/`미대면`/`무관`) | 판정 슬롯 |
| `is_strongest` | 이것이 그 지점의 최강 반론인가 (`true`/`false`) | 판정 슬롯 |
| `verdict` | `valid` / `strawman` / `moot` | 판정 슬롯 |
| `aporia[].verdict` | `보존` / `평탄화` / `의도된 종합` | 판정 슬롯 |

**판정 슬롯은 `UNJUDGED`로 산출한다.** 코드도 최초 산출 시점의 에이전트도 채우지 않는다. `prepare`가 worklist로 뽑아내고, 별도의 판정 패스(에이전트 또는 사람)가 증거에서 채우며, `decide`가 집계한다.

## 3. `[Policy-Directives]` 격리 규칙

레드팀의 임무는 결함을 드러내는 것이지 처방하는 것이 아니다. 처방을 같은 무게로 요구하면 **처방 가능한 결함만 지적하게 되어** 공격이 무뎌진다(gotcha ⑦).

1. Policy-Directives는 공격 섹션 **뒤에만** 오는 비점수 부록이다.
2. 각 directive는 `refs`로 자신이 다루는 `critique.id`를 참조해야 한다. 참조 없는 처방은 형식 오류다.
3. Directive는 어떤 지적도 완화·철회하지 못한다. `severity`를 낮추는 서술은 계약 위반이다.
4. 게이트의 커버리지·심각도 집계에서 **제외된다.** 옹호가 방어율을 희석하지 못하게 한다.
5. 성격은 "차선책 정책 처방"이 아니라 **hand-off 지침**이다. 즉 "어떤 추가 분석·데이터·미시패널 변수가 이 지적을 판가름하는가"라는 리서치 쿼리이지, 정책에 대한 지지 표명이 아니다.

Policy-Directives 항목은 `axis`·`severity`·`source_quote`·`steelman`·`falsification_condition`을 요구받지 않으며, grounding 검사 대상도 아니다.

## 4. Grounding 규칙

- `source_quote`는 대상 문서의 **산문**에 정규화(NFKC + 공백 축약) 후 부분문자열로 존재해야 한다.
- **표의 셀과 코드 블록은 산문이 아니다.** 게이트는 마크다운 표 행(`|`로 시작)과 펜스 코드 블록을 제거한 뒤 대조한다. 회귀표의 계수를 인용하면 ungrounded로 차단된다.
- 이것은 omni `ARCHITECTURE.md`의 범위 경계를 기계적으로 강제한 것이다. omni는 결과 검증기가 아니라 **논증 분석기**다. 계수의 재계산·리플리케이션은 의도적으로 범위 밖이다. 계수를 문제 삼고 싶다면 그 계수를 **해석하는 산문 문장**을 인용하라.
- `--paragraphs`로 omni `paragraphs.json`(`{"P_0001": "본문..."}` 평면 매핑)을 주면 `paragraph_id` 실존과 해당 문단 내 인용 포함까지 검증한다. 문단 번호는 omni가 발급한 것을 **소비할 뿐 재발명하지 않는다.**

## 5. 마크다운 리포트

동일한 내용을 사람이 읽는 4개 섹션으로 낸다. 순서는 고정이다.

1. `[Leap-Alert]` — 인과 입증이 붕괴한 지점 (ex-post: 식별 전략 / ex-ante: 기준선·가정)
2. `[Evidence-Check]` — 아전인수 인용, 넓은 신뢰구간, 추론·강건성 결함
3. `[Concept-Tension]` — 목표 충돌과 트레이드오프. 여기 오는 항목은 `aporia[]`에도 등록한다
4. `[Policy-Directives]` — hand-off 지침 (비점수 부록)
