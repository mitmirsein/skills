---
name: skill-name
description: >
  Does one thing well (third-person, present tense). Use when the user asks
  for X, Y, or Z. 키워드: 한국어 트리거1, 트리거2, 트리거3
version: 0.1.0
status: stub
author: MS_Dev
triggers:
  - "/skill-name"
references_path: ./references
---

# Skill Name (한 줄 요약)

이 스킬이 무엇을 하는지 한 문장으로.

## Phase 0 — 가드레일

- 시작 전 `references/gotchas.md`를 읽고 알려진 함정을 확인한다.
- (필요 시) 입력·전제 조건 점검 항목.

## Phase 1 — 실행

1. 사용자의 요청을 분석하여 필요한 작업 단계를 파악한다.
2. `scripts/` 도구가 필요하면 실행한다. (경로는 `~/` 표기 — 절대경로 금지, STANDARDS.md §5)
3. 150줄을 넘길 상세 지식은 본문에 두지 말고 `references/`로 분리한다.

## 검증·보고

- 무엇을 확인해야 "성공"인지 명시한다 (출력 파일, 개수, 표본 확인 등).
- 결과를 사용자에게 간결히 보고하고, 검증하지 못한 부분은 그렇다고 말한다.

---

새 스킬 만들기: 이 폴더를 복사 → frontmatter 채우기 → `python3 _meta/validate.py <skill-name>` 통과 확인.
규범 전문은 `.skills/STANDARDS.md`.
