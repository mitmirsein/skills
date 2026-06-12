---
name: git-workflow
description: >
  Standardized Git workflow — Conventional Commits, branch strategy, and
  pull-request flow. Use when the user asks to commit, push, branch, or
  open a PR in a repository.
  키워드: 커밋, 푸시, 브랜치, PR 생성
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#git"
  - "#커밋"
  - "#푸시"
  - "커밋해줘"
  - "푸시해줘"
  - "PR 만들어줘"
capabilities:
  - conventional_commits_automation
  - branch_strategy_management
  - remote_sync_alignment
  - git_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# ⚙️ Git Workflow 3.0

## 1. Overview
커밋, 브랜치 관리, PR 생성 등 모든 버전 관리 공정을 표준화하고 `main` 브랜치 중심의 무결성을 유지하는 스킬입니다.

## 2. Dynamic Workflow
본 명령 수행 전 **관리 함정(Gotchas)**과 **로컬 상태(Config)**를 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Status**: 현재 브랜치가 `main`인지, 커밋되지 않은 민감한 파일이 있는지 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 `master` 브랜치 사용 및 불완속한 커밋 메시지 작성을 방지합니다.

### Phase 1: Status & Survey (파악)
현황을 파악하고 작업 범위를 확정합니다.

### Phase 2: Commit & Message (기록)
Conventional Commits 규격에 맞춰 원자적 커밋(Atomic Commit)을 수행합니다.

### Phase 3: Push & Sync (동기화)
원격 저장소와 최신 상태를 동기화하고 명시적으로 푸시합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 강제 푸시 금지 및 브랜치 오동작 주의 가이드.

---
*Created by MS_Dev Third Gen Standard*
