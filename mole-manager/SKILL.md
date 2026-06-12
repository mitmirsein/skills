---
name: mole-manager
description: >
  Automates macOS diagnostics, cleanup, optimization, and monitoring with
  the Mole CLI (tw93/Mole) — a free replacement workflow for CleanMyMac,
  DaisyDisk, iStat Menus, and AppCleaner. Use when the user asks to clean,
  diagnose, or monitor their Mac.
  키워드: 맥 청소, 시스템 진단, 디스크 정리
version: 1.0.1
codename: First Gen
author: MS_Dev
triggers:
  - "#mole"
  - "#mac-clean"
  - "청소해줘"
  - "시스템 최적화해줘"
  - "디스크 분석해줘"
  - "시스템 상태 확인해줘"
  - "앱 삭제해줘"
  - "프로젝트 정리해줘"
capabilities:
  - disk_cleanup
  - app_uninstall
  - system_optimization
  - disk_analysis
  - realtime_monitoring
  - project_artifact_purge
  - installer_cleanup
references_path: "./references"
status: active
---

# 🧹 Mole System Manager

## 1. Overview
[Mole](https://github.com/tw93/Mole)은 macOS용 올인원 시스템 유틸리티로, Go + 셸 스크립트 기반의 초경량 CLI 도구입니다.
CleanMyMac, DaisyDisk, iStat Menus, AppCleaner 등 유료 앱의 핵심 기능을 단일 바이너리(`mo`)로 제공합니다.

> **바이너리**: `/opt/homebrew/bin/mole` → 명령어: `mo`
> **설치 여부 확인**: `which mo`

## 2. Core Workflow

### Phase 0: Intent Classification
사용자 요청을 분석하여 아래 6가지 작업 유형 중 하나로 분류합니다.

| 사용자 발화 예시 | 실행 명령 |
|---|---|
| "청소해줘", "용량 확보해줘" | `mo clean` |
| "앱 삭제해줘 [앱명]" | `mo uninstall` |
| "시스템 느려졌어", "최적화해줘" | `mo optimize` |
| "디스크 용량 분석해줘" | `mo analyze` |
| "CPU/메모리 상태 봐줘" | `mo status` |
| "프로젝트 빌드 파일 정리해줘" | `mo purge` |

### Phase 1: Dry-Run 우선 실행
**파괴적 작업(clean, uninstall, optimize, purge)은 반드시 `--dry-run` 플래그로 미리보기 후 사용자 확인을 받습니다.**

```bash
# 예시: 청소 전 미리보기
mo clean --dry-run

# 예시: 앱 제거 전 미리보기
mo uninstall --dry-run
```

### Phase 2: Execute
사용자 승인 후 실제 명령을 실행합니다. 상세 명령어는 [cli-commands.md](./references/cli-commands.md)를 참조하십시오.

### Phase 3: Verify & Report
실행 결과(확보 용량, 삭제 파일 목록 등)를 사용자에게 명확히 보고합니다.

## 3. Reference Links
- [cli-commands.md](./references/cli-commands.md): 전체 명령어 레퍼런스 및 플래그
- [best-practices.md](./references/best-practices.md): 안전 운영 수칙 및 주의사항
- [gotchas.md](./references/gotchas.md): 알려진 함정 및 에러 대응

---
*Created by MS_Dev · Source: https://devopslog.tistory.com/207 · https://github.com/tw93/Mole*
