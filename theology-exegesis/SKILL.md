---
name: theology-exegesis
description: >
  Performs scholarly exegesis of a biblical or theological text through four
  academic lenses — biblical, systematic, historical, and practical theology
  — with original-language and grammatical-historical analysis. Use when the
  user asks to exegete a passage or analyze a theological text academically.
  키워드: 신학 석의, 본문 주해, 신학 렌즈 분석
version: 4.0.1
author: MS_Dev
triggers:
  - "#theology-exegesis"
  - "#신학석의"
  - "#신학해석"
  - "신학 렌즈 분석해줘"
  - "본문 주해해줘"
capabilities:
  - four_theological_lenses_exegesis
  - original_languages_syntactic_analysis
  - historical_dogmatics_reconstruction
  - systematic_logical_formalization
  - practical_theological_contextualization
references_path: "./references"
status: active
---

# 📖 Theology Exegesis 4.0

## 1. 개요
신학 학술 문서 및 성경 본문을 다차원적으로 석의하고 평가하기 위한 프레임워크이다. 본 스킬은 기존의 설교학적/적용 중심의 설계를 배제하고, 순수 학술 석의와 해석학적 분석에 집중한다. 신학의 4대 대분류(성서학, 조직신학, 역사신학, 실천신학) 렌즈를 제공하며, 각 렌즈에 맞춰 학술적 타당성, 개념적 타당성, 문법-역사적 본의를 추적한다.

## 2. 4대 신학 렌즈 스키마

### 1) 성서학 렌즈 (Biblical Studies)
- **목표**: 텍스트의 언어적 본의와 역사·문학적 맥락을 드러낸다.
- **핵심 명세**:
  - **원어(히브리어/헬라어) 통사론 및 형태론 분석**: 핵심 어휘(예: 헤세드, 디카이오쉬네)의 의미 영역(Semantic Field)과 구문적 기능(Syntactic Relation)을 해부한다.
  - **역사-문학 비평**: 자료비평, 양식비평, 편집비평, 수사비평 등을 통해 본문이 형성된 삶의 정황(Sitz im Leben)과 정경적(Canonical) 최종 형태의 메시지를 분석한다.

### 2) 조직신학 렌즈 (Systematic Theology)
- **목표**: 신학적 개념들의 일관성, 논리적 추론 구조 및 교의적 정밀성을 평가한다.
- **핵심 명세**:
  - **논증 형식화**: 신학적 주장을 전제와 결론의 형태로 재구성하여 타당성을 점검한다.
  - **분석신학적 명료화**: 교의의 내적 일관성을 확보하고, 논리적 모순이나 아포리아를 비판적으로 진단한다.

### 3) 역사신학 렌즈 (Historical Theology)
- **목표**: 역사적 교의와 신학 사상의 발달 및 사상사적 지형을 규명한다.
- **핵심 명세**:
  - **역사적 정황 및 신조 검토**: 교부 시대, 중세 스콜라학, 종교개혁기 등 특정 역사적 맥락과 주요 신조(Creeds) 및 신앙고백서(Confessions)와의 부합성을 확인한다.
  - **사상사적 연속성/불연속성**: 신학 이론의 역사적 기원과 발전, 변형 경로를 고찰한다.

### 4) 실천신학 렌즈 (Practical Theology)
- **목표**: 텍스트와 사상의 현대적 실천성, 윤리적 영향력 및 선교학적 정황화를 분석한다.
- **핵심 명세**:
  - **선교적/목회적 정황성(Contextualization)**: 사상이 현대 사회의 구체적인 사회·문화적 정황 속에서 가지는 의의를 탐색한다.
  - **학제간 통섭**: 사회과학적, 철학적 분석과의 유기적 연계를 통하여 실천주의적/윤리적 방향성을 도출한다. (단, 단순 설교 양식이나 적용 가이드 생성은 배제한다.)

## 3. 분석 프로토콜 (Exegesis Protocol)
1. **렌즈 선택**: 분석을 시작하기 전, 분석 대상을 규정할 핵심 신학 렌즈를 1개 이상 지정한다. (예: `성서학` 및 `역사신학` 렌즈)
2. **함정 감지 (Gotcha Check)**: [gotchas.md](./references/gotchas.md)를 참고하여, 자의적 성경 해석(Eisegesis)이나 현대 사상의 시대착오적 투영을 사전 차단한다.
3. **학술 석의 (Exegesis Process)**: [exegesis-protocol.md](./references/exegesis-protocol.md)의 가이드라인에 따라 형태론, 통사론, 역사 비평 또는 논리 분석을 순차적으로 수행한다.
4. **학술적 타당성 검토 (Orthodoxy Audit)**: [academic-orthodoxy.md](./references/academic-orthodoxy.md)에 의거하여 역사적 정통 신조와 논리적 타당성 검수를 실행한다.
5. **보고서 산출**: 최종적으로 '신학 학술 석의 보고서(Theological Exegesis Report)'를 한국어 평서문으로 발행하여 볼트에 저장한다.
