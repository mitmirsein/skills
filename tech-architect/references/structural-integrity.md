# Tech Architect: Structural Integrity & Hygiene

프로젝트의 구조적 완성도와 청결함(Hygiene)을 유지하기 위한 상세 지침입니다.

## 🌟 Architectural Philosophy
- **"A place for everything, and everything in its place."**
- 모든 파일은 그 용도에 맞는 명확한 위치가 있어야 하며, 부유하는 파일이 시스템을 오염시키지 않도록 합니다.

## 🧹 Cleanup & Hygiene Standards
- **Candidate for Deletion**:
    - 임시 파일: `.tmp`, `*.log`, `debug_*.py`, `temp_*.md`.
    - 도구 생성물: `.DS_Store`, `__pycache__`, `.venv` (루트 외 개별 생성 시).
    - 빈 디렉토리 및 위치가 잘못된 파일 (예: `docs/`에 있는 `.py` 스크립트).
- **Naming Conventions**: 
    - 파일명은 일관된 규칙(kebab-case 또는 snake_case)을 따라야 합니다.

## 🏗️ Reorganization Protocol
1. **Blueprint**: reorganization 전/후의 트리(ASCII Tree)를 사용자에게 제시합니다.
2. **Safety First**: 삭제 명령(`rm`)은 실행 전 반드시 대상 목록을 명시하고 사용자의 최종 승인을 받아야 합니다.
3. **Implicit Update**: 파일 이동 시 영향받는 `import` 경로를 함께 점검하고 수정을 제안합니다.
