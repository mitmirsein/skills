# ⚠️ Zettel Capture: Gotchas & Anti-Patterns

에이전트가 이 스킬을 사용할 때 저지르기 쉬운 실수와 반드시 피해야 할 함정 모음입니다.

## 1. 포착 단계의 함정 (Capture Pitfalls)
- **과잉 카드 생성 (Card Spam)**: 대장이 하나의 문단을 주었을 때 문장마다 별도 카드를 만들지 마십시오. 하나의 핵심 인사이트 = 하나의 카드 원칙을 지키십시오.
- **원문 왜곡 금지 (Quote Fidelity)**: Quote 섹션은 대장이 제공한 원문을 정확히 보존해야 합니다. AI가 "더 나은 표현"으로 바꾸려는 유혹을 차단하십시오.
- **출처 누락 (Source Amnesia)**: 카드 생성 시 `source` 메타데이터가 불완전하면 나중에 검증이 불가합니다. 최소한 `title`과 `author`(또는 `url`)는 반드시 기입하십시오. 대장이 출처를 제공하지 않았다면, 반드시 물어보십시오.

## 2. 분류 단계의 함정 (Classification Pitfalls)
- **Permanent 남발 (Premature Permanence)**: 처음 포착한 생각을 바로 💎 Permanent로 분류하는 것은 위험합니다. 대부분의 신규 포착은 📖 Literature 또는 💭 Fleeting입니다. Permanent는 성숙 과정을 거쳐 승격되어야 합니다.
- **Fleeting 방치 (Fleeting Graveyard)**: 💭 Fleeting 카드가 30일 이상 방치되면 정보 부패가 시작됩니다. `/zettel review`를 통한 주기적 리뷰를 촉구하십시오.

## 3. 사유 촉발의 함정 (Prompting Pitfalls)
- **강제 사유 요구 금지**: 대장이 "일단 적어놔"라고 했을 때 "사유를 덧붙이시겠습니까?"라고 묻지 마십시오. 이 경우 즉시 💭 Fleeting으로 저장하고 끝내십시오.
- **대장의 사유 대필 금지 (No Ghost-Writing)**: Zettel(사유) 섹션을 에이전트가 대신 작성하지 마십시오. 에이전트는 질문이나 연결 제안만 할 수 있으며, 사유 자체는 반드시 대장의 입력이어야 합니다.

## 4. 범위 일탈의 함정 (Scope Creep)
- **분류 작업 침범 금지**: ARC 카테고리(100~900) 분류나 폴더 이동은 `arc-librarian`의 영역입니다. 이 스킬은 Inbox에 저장하는 것까지만 합니다.
- **온톨로지 추출 금지**: 카드에서 엔티티/관계를 추출하여 DB에 저장하는 것은 `ontology-builder`의 영역입니다.

---
*Created by MS_Dev Third Gen Standard*
