# ⚙️ Git Workflow: Gotchas & Anti-Patterns

Git 워크플로우 수행 및 버전 관리 시 에이전트가 주의해야 할 사항입니다.

## 1. Branching Pitfalls (브랜칭의 함정)
- **Master Branch 사용**: 우리 시스템의 철칙은 `main` 브랜치입니다. `master`라는 이름을 보게 되면 즉시 `main`으로 전환하십시오.
- **Dangling Branches**: 작업이 끝난 `feature` 브랜치를 삭제하지 않고 방치하여 원격 저장소를 어지럽히지 마십시오.

## 2. Committing Failures (커밋 실패)
- **Huge Monolithic Commits**: 여러 개의 논리적 변경 사항을 하나의 커밋에 몰아넣지 마십시오. (Atomic Commits 준수)
- **Vague Messages**: "update code", "fix bug"와 같이 의미 없는 커밋 메시지를 쓰지 마십시오. 반드시 `feat(scope): description` 형식을 따르십시오.

## 3. Remote Errors (원격 오류)
- **Force Push to Main**: 대장의 명시적 승인 없이 `main` 브랜치에 강제 푸시(`-f`, `--force`)를 수행하여 동료들의 작업 내용을 날려버리지 마십시오.
- **Sync Neglect**: 푸시하기 전 `fetch/merge`를 통해 원격의 최신 상태와 동기화하지 않아 불필요한 충돌(Conflict)을 야기하지 마십시오.

---
*Created by MS_Dev Third Gen Standard*
