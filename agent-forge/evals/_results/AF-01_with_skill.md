# AF-01 · With-Skill 출력 (agent-forge v6.1.0 활성)

> 프롬프트: "신학 논문의 참고문헌 목록(BibTeX 또는 주석 형태)을 입력받아 SBL 규격으로 자동 변환해주는 에이전트 스킬을 설계해줘. #forge"
> 실행일: 2026-05-18 · 실행자: Claude (agent-forge SKILL.md 5-Phase 준수)

---

## Phase 1: Architecting & Ops Design
- **환경 스캔**: `.skills/` 확인 — `theology-translator`, `dictionary-editor` 존재하나 SBL **서지 변환** 전용 스킬은 없음 → 신규 생성 정당.
- **Source of Truth**: *The SBL Handbook of Style*, 2nd ed. (SBL Press); SBL Press 공개 스타일 가이드 PDF.
- **의도**: BibTeX/각주형 참고문헌 → SBL 각주(footnote) 및 참고문헌(bibliography) 양식 자동 변환.

## Phase 2: Precision Assembly (작성 교리 게이트 + 헌법 주입 통과)

### 생성 파일: `sbl-bibliography/SKILL.md`
```yaml
---
name: sbl-bibliography
description: BibTeX 또는 주석/각주 형태의 신학 논문 참고문헌을 SBL(Society of Biblical Literature) Handbook of Style 2판 규격의 각주·참고문헌 양식으로 변환한다. .bib 파일이나 "이 참고문헌 SBL로", "각주 SBL 양식" 요청 시 사용. 단순 인용 스타일 질문이 아닌 실제 변환·정규화가 필요할 때.
version: 1.0.0
author: MS_Dev
sources_of_truth:
  - "https://www.sblpress.org/files/SBLHSsupp2.pdf"
triggers:
  - "SBL 변환"
  - "참고문헌 SBL"
  - "SBL 각주 양식"
  - "convert to SBL"
capabilities:
  - bibtex_to_sbl_conversion
  - footnote_bibliography_dual_output
  - theological_series_abbreviation
references_path: "./references"
---
```
- **Why-First 적용**: "각주 첫 인용과 약식(ibid./저자-단축) 인용을 구분하라 — SBL은 첫 인용에 전체 서지, 재인용에 단축형을 요구하기 **때문**이다."
- **Progressive Disclosure**: 시리즈 약어표(WUNT/BZNW/AB 등 수백 개)는 본문이 아닌 `references/sbl-series-abbreviations.md`로 위임.
- **헌법 주입**: `references/gotchas.md`에 검증 정직성(불확실 서지정보 `[미확인]`), TRE 용어 앵커, 라틴 약어(ibid., idem.) 오용 함정 박제.

### 생성 파일: `sbl-bibliography/references/gotchas.md`
- 0. 헌법 기본 가드(검증 정직성·TRE 앵커·긴장 보존·환경 가드) — agent-forge 강제 주입.
- 1. BibTeX `@incollection` ↔ SBL "essay in a collection" 매핑 누락 함정.
- 2. 독일어 출판지(예: Tübingen) 로마자 보존 — 한글 음역 금지.

### 생성 파일: `sbl-bibliography/evals/evals.json`
- SB-01(basic): 단일 `@book` → SBL 각주+참고문헌 이중 출력 / assertion 4개.
- SB-02(advanced): 시리즈 약어 포함 `@incollection`, 재인용 단축형 / assertion 3개.

## Phase 3: Validation & FinOps Audit
- With-Skill vs Baseline 케이스(SB-01/02)를 `evals.json`에 등록. 배치 전 assertion 전수 통과 요구.

## Phase 4: Deployment & Governance
- 단일 표준 구조로 `.skills/sbl-bibliography/` 배치: `SKILL.md` + `references/{gotchas.md, sbl-series-abbreviations.md}` + `evals/evals.json`. config.json·scripts/ 불필요(순수 변환 규칙) → 생성 안 함(과잉 구성 회피).

## Phase 5: Meta-Harness (등록)
- 향후 변환 실패 사례는 대상 스킬 산출 로그/사용자 지정 경로에서 수집하여 `gotchas.md`에 명제화(존재 확인된 추적만).

---
**산출 요약**: SKILL.md(YAML frontmatter: name/description/triggers/capabilities 포함) + references/ 디렉토리(gotchas.md 포함) + evals.json. Why-Factor("때문이다") 본문 적용.
