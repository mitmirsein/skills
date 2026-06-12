---
name: theology-citation-linker
description: >
  Parses temporary citation anchors ([Ref: ...]) in a Markdown draft, maps
  them to EvidencePack.json via fuzzy matching, and generates SBL-style
  footnotes and a bibliography with dynamic re-indexing. Use when the user
  asks to link citations, build footnotes, or finalize references in a
  theological manuscript. 키워드: 각주 연결, 인용 매핑, 참고문헌 생성
version: 1.0.1
author: MS_Dev
triggers:
  - "#theology-citation-linker"
  - "#각주연결"
  - "각주 연결해줘"
  - "인용 매핑해줘"
capabilities:
  - markdown_citation_anchor_extraction
  - fuzzy_evidence_mapping
  - sbl_style_citation_formatting
  - dynamic_footnote_indexing
  - markdown_footnote_structure_audit
status: active
---

# 🔗 Theology Citation Linker 1.0

## 1. 개요
신학 학술 문서 초안에 작성된 임시 인용 표기(예: `[Ref: Waltke 2007, 45]`)를 추출하고, Phase 2 문헌 수집 단계에서 수집된 서지 정보 데이터베이스(`EvidencePack.json`)와 대조/매핑한다. 매핑 결과를 바탕으로 SBL(Society of Biblical Literature) 포맷의 정밀한 주석(각주) 및 참고문헌 목록을 마크다운 문서 최하단에 자동 생성하고 본문 각주 인덱스를 동적으로 연결한다.

## 2. 핵심 기능
- **임시 앵커 파싱**: 본문의 `[Ref: 저자명 연도, 페이지]` 혹은 `[Ref: 저자명, 페이지]` 패턴을 정규 표현식으로 추출한다.
- **퍼지 매핑 (Fuzzy Mapping)**: Levenshtein Distance 유사도 분석 알고리즘을 활용하여 저자명, 출판 연도 등을 비교한다. 매핑 신뢰도(Confidence)가 60% 이상인 최적의 서지 정보를 후보로 자동 결정한다. 만약 신뢰도가 60% 미만이거나 불명확할 경우 경고를 표시하고 매핑을 보류하여 수동 조정을 유도한다.
- **SBL 스타일 포맷팅**:
  - 도서 (Book): 저자명, *도서명* (출판지: 출판사, 출판연도), 인용페이지.
  - 논문 (Journal Article): 저자명, "논문제목," *저널명* 권호 (연도): 인용페이지.
  - 사전/백과사전 (Dictionary/Lexicon): 저자명, "항목명," in *사전명* 권호, ed. 편집자명 (출판지: 출판사, 연도), 페이지.
- **동적 각주 재색인 (Dynamic Re-indexing)**:
  - 본문에서 인용이 등장한 순서대로 `[^1]`, `[^2]` 형태로 순차적인 각주 기호를 치환한다.
  - 마크다운 문서 최하단에 각주 번호와 SBL 인용이 결합된 각주 정의 리스트를 삽입한다.
  - 동일한 문헌을 반복해서 인용하는 경우, SBL 규정에 따라 이전 각주와 비교하여 잇따름(Ibid.) 표기를 적용하거나 단축형 인용(Short Title: 저자 성, *단축 서명*, 페이지.)으로 압축 변환한다.
  - 최하단에는 인용된 모든 문헌 목록을 정렬(영어는 알파벳순, 한국어는 가나다순)하여 종합 참고문헌(Bibliography) 섹션을 추가로 작성한다.
- **각주 구조 감사 (Footnote Structure Audit)**:
  - 본문 각주 호출 수, 고유 각주 ID 수, 하단 각주 정의 수를 대조한다.
  - 같은 위치의 연속 각주(`[^34][^35]`)를 병합 후보로 경고한다. 같은 문장 위치의 복수 출처는 하나의 각주 안에 함께 처리해야 한다.
  - 서로 다른 위치에서 같은 각주 ID가 반복 호출되는 경우를 경고한다. Pandoc/XeLaTeX는 반복 호출을 PDF에서 새 각주로 다시 찍으므로, 별도 short note로 분리해야 한다.
  - 본문 호출 누락 정의, 미사용 정의, 중복 정의를 감지한다.
  - `--fail-on-footnote-issues`와 함께 실행하면 구조 결함 발견 시 비정상 종료하여 PDF 단계로 넘어가지 않게 한다.

## 3. 작동 프로토콜 (Execution Protocol)
1. Target Markdown 파일과 `EvidencePack.json`의 경로를 입력받아 작업을 시작한다.
2. 스크립트(`cite_linker.py`)를 기동하여 본문의 임시 앵커 목록을 수집한다.
3. 수집된 앵커별로 `EvidencePack.json` 내부의 서지 데이터와 매핑을 진행하고 신뢰도 스코어를 도출한다.
4. 매핑 리포트를 출력하여 자동 매핑 성공 항목과 보류(경고) 항목을 구분 보고한다.
5. 임시 앵커들을 `[^N]` 각주 번호로 치환하고, 문서 최하단에 SBL 스타일의 각주 정의 목록 및 Bibliography를 통합 생성하여 덮어쓴다.
6. 작업 후 각주 구조 감사를 실행하여 PDF 예상 각주 수와 Markdown 정의 수가 일치하는지 보고한다.

## 3.1 각주 구조 감사 단독 실행

기존 원고의 각주만 점검할 때는 `EvidencePack.json` 없이 실행할 수 있다.

```bash
python3 ~/Desktop/MS_Dev.nosync/.skills/theology-citation-linker/scripts/cite_linker.py \
  --file path/to/manuscript.md \
  --audit-footnotes \
  --fail-on-footnote-issues
```

감사 기준:
- PASS: 본문 각주 호출, 고유 각주 ID, 하단 각주 정의가 1:1로 대응하고 연속/반복 호출 문제가 없다.
- FAIL: 같은 위치의 연속 각주, 다른 위치의 반복 각주 호출, 누락 정의, 미사용 정의, 중복 정의 중 하나라도 발견된다.

## 4. 인용 예시
* **본문 임시 표기**: `Amos's prophecy reflects a deep covenantal transformation [Ref: Waltke 2007, 145].`
* **치환된 본문**: `Amos's prophecy reflects a deep covenantal transformation[^1].`
* **생성된 각주**: `[^1]: Bruce K. Waltke, *An Old Testament Theology* (Grand Rapids: Zondervan, 2007), 145.`
