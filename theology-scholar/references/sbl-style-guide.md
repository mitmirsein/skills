title: SBL & Chicago Style Master Guide
---

# ✍️ SBL & Chicago Style Master Guide

신학 학술지의 표준인 **SBL Style Manual 2nd Edition**을 준수하며, 그 근간인 **Chicago Manual of Style (CMOS)**의 원칙을 철저히 따릅니다.

## 1. The Foundation: Chicago Manual of Style (CMOS)
SBL 스타일은 시카고 스타일(Notes-Bibliography System)의 변형입니다. 다음 기본 원칙을 유지하십시오:
- **각주(Notes)**: 첫 인용 시 전체 서지 정보를 제공하고, 이후 인용 시 '저자, 짧은 제목, 페이지' 형식을 사용합니다.
- **참고문헌(Bibliography)**: 저자 성(Last Name) 순으로 나열하며, 마침표(Period) 중심의 구두점 체계를 따릅니다.
- **인용구(Quotations)**: 5줄 이상의 인용구는 블록 인용(Block Quote)으로 처리하며, 따옴표 없이 들여쓰기합니다.

## 2. SBL Style Specification (2nd Edition)
신학 및 성서학 특유의 규정을 적용합니다:
- **성경 약어(Biblical Abbreviations)**: 각주나 괄호 안에서는 SBL 핸드북에서 정의한 약어를 사용합니다 (예: Gen 1:1, Matt 5:3). 본문에서는 약어를 쓰지 않습니다.
- **교부 및 고대 문헌(Ancient Sources)**: 저널별 특수 규격이 없다면 SBL 핸드북의 표준 인용 형식을 따릅니다.
- **비영어권 문헌(Non-English Sources)**: 독일어, 프랑스어 등 외국어 논문 제목은 원어 그대로 표기하되, 대문자 표기법(Capitalization)은 해당 언어의 규칙을 따릅니다.

## 3. Mandatory Checklist for #scholar
- [ ] 서지 정보의 점(.)과 쉼표(,) 위치가 CMOS 규격과 일치하는가?
- [ ] ISBN이나 DOI, S2, RISS ID가 존재할 경우 반드시 포함하며, 클릭 가능한 하이퍼링크 형식을 사용하였는가?
  - **DOI**: `[DOI:10.xxx/xxx](https://doi.org/10.xxx/xxx)`
  - **S2**: `[S2:paper_id](https://www.semanticscholar.org/paper/paper_id)`
  - **RISS**: `[RISS:control_no](https://www.riss.kr/search/detail/DetailView.do?p_mat_type=be1f68386aab600e&control_no=control_no)`
- [ ] 약어표(Abbreviations List)가 SBL 2nd Edition의 표준을 따르는가?
- [ ] '성경 구절' 인용 시 장(Chapter)과 절(Verse) 사이에 쌍점(:)을 사용하였는가?

---

## 🏷️ Metadata (YAML Front-matter)
최종 파일 상단에 다음 메타데이터를 포함합니다.
- `title`: 논문 또는 리포트 제목
- `date`: 작성일 (YYYY-MM-DD)
- `tags`: 주요 키워드 (#Theology, #Audit, #Scholarship 등)
- `type`: Theology-Scholar-Result
