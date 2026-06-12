# ⚠️ Gotchas & Anti-Patterns

에이전트가 이 스킬을 사용할 때 저지르기 쉬운 실수와 반드시 피해야 할 안티 패턴 모음입니다.

## 0. 헌법 기본 가드 (agent-forge 강제 주입 — 삭제 금지)
- **검증 정직성**: 출력을 직접 확인한 것만 "통과/완료"로 보고한다. 불확실은 `[미확인]`, 인용·수치 날조 금지.
- **TRE 용어 앵커**: 신학 용어는 `data/tre_terms.csv` TRE 정의를 우선한다. 이탈 시 `[⚠️ TRE-외 정의]`로 명시.
- **신학적 긴장 보존**: 의도된 아포리아를 단일 결론으로 평탄화하지 않는다.
- **환경 가드(Python)**: venv는 machine-local(`.venv-m1`/`.venv-intel`), Syncthing 동기 경로 금지. release-age·lifecycle-script 비활성 정책 전제.
- *(이 스킬에 해당 없는 항목은 삭제하지 말고 "비해당: 사유" 로 표기한다.)*

## 1. 흔한 실패 포인트 (Typical Failures)
- **과도한 설명**: [Why it fails] -> [How to fix]
- **데이터 유실**: [Context] -> [Prevention]

## 2. 에이전트 전용 함정 (Agent-Specific Pitfalls)
- **Default Assumption**: 클로드는 기본적으로 [X]라고 생각하지만, 이 스킬에서는 반드시 [Y]여야 합니다.
- **Tool Selection**: [Tool A]보다 [Tool B]가 이 작업에 더 안전합니다.

## 3. 실전 사례 (Real-world Bad Examples)
- "과거 [X] 작업 시 [Y] 문제가 발생하여 [Z] 해결책을 적용함." -> 이를 위해 항상 [Rule]을 준수하십시오.

---
*Created by MS_Dev Third Gen Standard*
