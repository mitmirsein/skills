---
name: tech-architect
description: >
  Keeps a project's structure clean and its code maintainable — directory
  reorganization with before/after blueprints, hygiene sweeps (temp files,
  misplaced scripts), and behavior-preserving refactoring to clean-code
  standards. Use when the user asks to reorganize a project, clean up a
  folder, or refactor for readability.
  키워드: 구조 정리, 리팩토링, 프로젝트 청소, 클린 코드
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#architect"
  - "프로젝트 구조 정리해줘"
  - "리팩토링해줘"
references_path: ./references
---

# 🏗️ Tech Architect (구조·리팩토링 설계자)

프로젝트의 구조적 완성도(Hygiene)와 코드 품질을 지키는 스킬입니다.
"모든 파일에는 제자리가 있다" — 부유 파일이 시스템을 오염시키지 않게 합니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- **삭제·일괄 이동은 반드시 대상 목록(dry-run)을 먼저 제시하고 사용자 승인 후 실행**합니다.

## Phase 1 — 구조 정리 (정본: [structural-integrity.md](./references/structural-integrity.md))

1. 현재 트리를 스캔해 삭제 후보(임시 파일·`__pycache__`·빈 디렉토리·위치 오류 파일)와
   재배치 후보를 식별
2. **Blueprint**: 전/후 ASCII 트리를 제시 → 승인
3. 이동 시 영향받는 `import`/참조 경로를 함께 점검·수정

## Phase 2 — 리팩토링 (정본: [clean-code-standards.md](./references/clean-code-standards.md))

- **행동 보존(Behavior Preservation)**이 제1원칙 — 기능 변경 없이 구조만 개선
- 진단 체크: DRY 위반 / 인지 부하(중첩) / 명명 / 타입힌트·Docstring
- 수술 지침: 작은 단위 분해, 서술형 명명, 최신 구문 활용

## 검증·보고

- 구조 정리: 이동·삭제 파일 수, 전/후 트리, 수정한 참조 경로를 보고
- 리팩토링: 변경 전후 동작 동일성 확인 방법(테스트 실행 결과 등)을 함께 보고
- 검증하지 못한 부분은 명시한다
