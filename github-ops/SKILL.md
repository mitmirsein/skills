---
name: github-ops
description: >
  Automates GitHub operations via the gh CLI — repo creation, remote
  wiring, issues, and PRs. Use when the user asks to publish a project to
  GitHub, create a repository, or manage issues/PRs from the terminal.
  키워드: 깃헙 올리기, 레포 생성, 이슈 관리, gh CLI
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "이거 깃헙에 올려줘"
  - "새 레포 만들어줘"
  - "#git-init"
  - "커밋해줘"
  - "푸시해줘"
  - "#git-push"
  - "PR 날려줘"
  - "#pr"
capabilities:
  - repo_init_and_sync
  - issue_management_automation
  - pr_lifecycle_control
  - github_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# 🐙 GitHub Operations 3.0

## 1. Overview
로컬 Git 저장소와 GitHub 클라우드를 `gh` CLI를 통해 완벽하게 동기화하고 관리하여 생산성을 극대화하는 스킬입니다.

## 2. Dynamic Workflow
본 관리 작업 전 **운영 함정(Gotchas)**과 **인증 상태(Config)**를 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Auth**: `gh auth status`로 로그인 여부를 확인하고, 레포의 `Private` 설정을 기본으로 점검합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 브라인드 머지(Blind Merge) 및 잘못된 레포 공개 설정을 방지합니다.

### Phase 1: Init & Ship (초기화)
레포지토리를 생성하고 `main` 브랜치를 강제로 설정하여 최초 배포를 수행합니다.

### Phase 2: Code Sync (동기화)
변경사항을 요약하여 지능적 커밋과 명시적 푸시를 실행합니다.

### Phase 3: Issue & PR Ops (이슈/PR)
이슈 등록 및 PR 생성을 통해 협업 및 작업 관리를 자동화합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 토큰 스코프 부족 및 낚시성 이슈 등록 방지 가이드.

---
*Created by MS_Dev Third Gen Standard*
