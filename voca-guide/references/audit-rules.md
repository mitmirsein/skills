# Voca Guide Quality Audit Rules

이 문서는 `voca-guide` 스킬을 통해 생성되는 단어 카드뉴스 교재의 품질을 보장하기 위한 공식 룰셋(Rule Book)입니다. 모든 어휘 데이터셋(`vocab_data.json`)은 빌드 전에 본 룰셋에 부합하는지 `audit_harness.py`를 통해 자동으로 검증되어야 합니다.

---

## 1. Schema & Completeness (데이터 정합성)

각 단어 데이터는 다음 13단계 스토리라인에 필요한 모든 필드를 완벽하게 포함해야 합니다.

* **필수 필드 구성**:
  * `word` (str): 표제어 (예: `incident`)
  * `pronunciation` (str): 발음 기호 (예: `IN-suh-duhnt`)
  * `meaning1` (str): 물리적/1차 의미
  * `meaning2` (str): 추상적/2차 의미
  * `intro` (str): 질문형 도입부
  * `etymology` (dict): 어원 정보 (아래 상세 스키마 참고)
  * `examples1` (list): 1차 의미 예문 (정확히 2개 원소)
  * `transition_question` (str): 2차 의미 연결 질문
  * `logic_flow` (list): 의미 변화 징검다리 흐름 (3~7개 원소)
  * `logic_desc` (str): 변화의 논리적 이유 설명
  * `examples2` (list): 2차 의미 예문 (정확히 2개 원소)
  * `feeling` (str): 단어의 핵심 이미지/뉘앙스 요약
  * `real_tip` (str): 실전 시험 및 독해 팁
  * `summary_flow` (list): 꼬리에 꼬리를 무는 핵심 요약 (3~5개 원소)
  * `quiz` (list): 2문항 빈칸 퀴즈 (정확히 2개 원소)

* **상세 스키마 제한**:
  * `etymology` 내부는 `root1` (str), `root2` (str), `flow` (list) 키를 반드시 가져야 합니다.
  * `examples1`, `examples2` 내부 원소는 `en` (str), `ko` (str) 키를 정확히 가져야 합니다.
  * `quiz` 내부 원소는 `question` (str), `translation` (str), `answer` (str) 키를 정확히 가져야 합니다.

---

## 2. Pedagogical Style & Tone (학습 친화성 및 문체)

학생들이 강사의 과외를 받듯 친근하고 직관적으로 이해할 수 있도록 문체와 콘텐츠를 제한합니다.

* **친근한 구어체 의무화**:
  * **금지 문체**: 딱딱하고 기계적인 격식체 (`~입니다`, `~했습니다`, `~합니다`, `~됩니다` 등)
  * **권장 문체**: 친근하고 대화 지향적인 구어체 반말/반격식체 (`~이지`, `~했어`, `~잖아`, `~지`, `~이야` 등)
  * 검증 범위: `intro`, `logic_desc`, `feeling`, `real_tip` 등 한글 설명 필드 전체
* **어원 표기 표준 규격**:
  * `etymology`의 `root1`, `root2` 등은 반드시 라틴어(`L.`), 그리스어(`Gk.`), 고대 영어(`OE.`) 원어 형태와 한글 의미 대역을 명시해야 합니다.
  * 예시: `L. cadere : to fall / 떨어지다` (언어 기호 + 원형 단어 + 뜻)
* **어원 연결성 시각화**:
  * `logic_flow` 배열은 변화의 역동성을 보여주기 위해 단계 사이의 인과 화살표(`↓`)를 요소에 포함하거나 인과가 명확하게 구성되어야 합니다.
* **퀴즈 정합성**:
  * `quiz` 내 각 문항의 `answer`는 표제어(`word`)와 완벽히 일치하거나, 혹은 문장 내 시제/단복수/파생형 변화(예: `incident` -> `incidents`, `compromise` -> `compromised`) 형태여야 합니다. 엉뚱한 타 단어가 정답으로 들어가선 안 됩니다.

---

## 3. Privacy & Security (개인정보 및 보안)

특정 강사나 학원의 실명이 노출되지 않도록 데이터 청결을 유지합니다.

* **금지어 매칭**:
  * 강사명: `minkyoo`, `cho`, `minkyoo_cho`, `조민규` 등
  * 브랜드/학원명: `대치동`, `개별맞춤`, `대치동 개별맞춤 영어` 등
  * 기타 개인 SNS 또는 계정 정보 노출 금지

---

## 4. Layout & Overflow Guard (레이아웃 오버플로우 방지)

A4 1페이지 내에 13개의 카드뉴스 타일이 격자형으로 배치되므로, 텍스트가 지정된 글자 수를 초과하면 물리적인 겹침이나 잘림 현상이 발생합니다.

* **글자 수 제한 기준 (한국어 공백 포함)**:
  * `logic_desc`: 최대 **150자** 이내
  * `real_tip`: 최대 **200자** 이내
  * 예문 한 문장당 (`examples1`, `examples2` 내의 `en` 및 `ko`): 최대 **100자** 이내
  * `intro` 및 `transition_question`: 최대 **100자** 이내
