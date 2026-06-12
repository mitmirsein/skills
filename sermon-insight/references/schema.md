# sermon-insight 입출력 스키마 명세

## 1. 입력 사양 (Input Specification)
스킬이 실행될 때 LLM은 다음 규격에 부합하는 입력을 전달받는다.

```yaml
meta:
  name: sermon-insight
  version: 2.0-integrated
inputs:
  - name: source_document
    type: markdown / pdf_text
    required: true
    description: "학술 신학 논문 또는 에세이의 원문 텍스트"
  - name: theological_filter
    type: enum [REDEEMPTIVE_CHRIST, PROPHETIC_JUSTICE, PASTORAL_COMFORT]
    default: REDEEMPTIVE_CHRIST
    description: "인사이트 추출에 적용할 주요 신학적 관점 성향"
  - name: audience_level
    type: enum [SUNDAY_SERMON, BIBLE_STUDY, DEVOTIONAL]
    default: SUNDAY_SERMON
    description: "최종 아웃라인 및 설교적 적용의 형식 지향점"
```

---

## 2. 경량 온톨로지 및 아포리아 메타데이터 규격
스킬은 논증 구조에서 핵심이 되는 개념과 신학적 긴장 상태를 다음과 같은 구조화된 온톨로지 메타데이터(JSON/YAML)로 본문 헤더에 박아 출력한다.

* **Continuants (핵심 개념 분류)**:
  * `Person`: 텍스트 내에서 신학적 논지를 펼치는 인물 (예: "아모스", "예수")
  * `Scripture`: 본문과 직접 연계된 성경적 출처 (예: "Amos 4:12")
  * `Place`: 역사적/신학적 의미를 담은 장소 (예: "베델", "길갈")
  * `Creed`: 신학적 배경이 되는 공식 고백문 (예: "Nicaea 325")
  * `Concept`: 텍스트 내의 주요 추상적 개념 (예: "성육신", "심판")
* **Arguments (주장-근거 매핑)**:
  * `Claims`: 논문이 제기하는 논리적 명제
  * `Evidences`: 해당 주장을 지지하는 주석적, 역사비평적 근거
* **Structured Aporia (구조화된 아포리아)**:
  * `Tension_Nodes`: 해소되지 않고 보존되어야 하는 신학적 역설이나 긴장점 (예: "하나님의 전능성과 신적 패배의 역설")
  * `Interpretive_Poles`: 서로 긴장 관계를 이루는 두 신학적 해석의 극한 대립점 (예: "심판자 하나님 vs 패배하는 하나님")

---

## 3. 출력 사양 (Output Specification)
최종 결과물은 다음 구조의 마크다운 파일로 작성되어 지정된 경로인 `~/Desktop/MS_Brain.nosync/000 System/Inbox/sermon-insight/` 디렉터리 하위에 자동 저장된다. 파일명은 `SI-[년월일]-[논문식별자].md`로 구성한다.

```markdown
---
sermon_insight_id: "SI-20260520-[SOURCE_ID]"
source_paper: "[논문 제목 및 출처]"
filter_applied: "REDEEMPTIVE_CHRIST | PROPHETIC_JUSTICE | PASTORAL_COMFORT"
audience_level: "SUNDAY_SERMON | BIBLE_STUDY | DEVOTIONAL"
ontology_metadata:
  continuants:
    - type: "Person | Scripture | Place | Creed | Concept"
      name: "개념명"
      description: "간략한 정의"
  arguments:
    - claim: "추출된 핵심 주장 명제"
      evidence:
        - "텍스트 내의 구체적인 본문/주석적 근거 구절"
  structured_aporia:
    - tension_node: "해소 불가능한 신학적 역설 지점"
      pole_a: "해석 극점 A"
      pole_b: "해석 극점 B"
      hermeneutical_tension: "두 극점 사이의 긴장 관계에 대한 기술"
---

# [Sermon Insight] 본문 중심 설교 인사이트 패키지

## 1. 신학적 뼈대 (Theological Framework)
* **주해적 명제 (Exegesis):** 논문이 도출한 핵심 성경 주해의 학술적 결론을 제시한다.
* **설교적 명제 (Kerygma):** 본 주해적 명제가 현대 성도에게 선포될 수 있는 케리그마적 원형으로 가공된 문장이다.

## 2. 3중 해석학적 교량 (Hermeneutical Bridges)
1. **역사적 교량 (Historical Bridge):** 본문이 기록된 당시의 역사비평적 배경을 설교적 맥락으로 연결한다.
2. **정경적 교량 (Canonical Bridge):** 성경 전체 정경의 지평 속에서 본문의 위치를 조망하고 타 장르/구절과의 상호텍스트성을 규명한다.
3. **구속사적 교량 (Redemptive Bridge):** 지정된 `theological_filter`에 맞춘 구속사적 지평(예: 그리스도 중심적 구속의 성취)으로 나아가는 가교 역할을 제시한다.

## 3. 역설적 명제 프로토콜 (Sermon Delivery Path)
아포리아의 긴장을 보존하며 청중에게 다가가는 4단계 전개 경로를 구축한다.
* **[1단계: 도발 (Provocation)]** 청중의 통념을 깨는 역설적인 도발적 명제를 선포한다.
* **[2단계: 반론 선제 수용 (Anticipating Objection)]** 청중이 가질 법한 상식적 의문이나 신학적 반론을 선제적으로 수용하여 공감대를 형성한다.
* **[3단계: 긴장 유지 (Sustaining Tension)]** 아포리아의 긴장 상태를 쉽게 해소하지 않고, 텍스트가 지닌 모순과 한계를 드러내며 긴장을 고조시킨다.
* **[4단계: 해소 (Resolution)]** 복음(특히 십자가와 그리스도 중심적 은혜)을 통해 신학적 긴장을 신비적 방식으로 수렴하여 선포한다.

## 4. 용도별 변환 사양 (Tailored Formats)
지정된 `audience_level` 양식에 맞추어 구성된 상세 아웃라인, 핵심 본문 및 적용 예화를 제시한다.
* **SUNDAY_SERMON**: 3대지 중심의 20분 설교 아웃라인과 현대적 일상 예화 매칭.
* **BIBLE_STUDY**: 깊이 있는 성경 공부를 위한 문답 구조식 아웃라인 및 주석적 질문 설계.
* **DEVOTIONAL**: 매일의 묵상과 인격적 적용을 돕는 묵상 질문 및 기도 방향 제시.
```
