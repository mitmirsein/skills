---
name: obsidian-cli
description: >
  Operates the Obsidian vault through the official Obsidian CLI (v1.12.x+) —
  note CRUD, search, backlinks, properties, tags, and link-safe refactoring
  at app level. Use when the user asks to create, move, or search notes, or
  to manipulate note metadata via Obsidian.
  키워드: 옵시디언 CLI, 노트 생성, 백링크 조회, 속성 조작
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#obsidian"
  - "#ob"
  - "노트 만들어줘"
  - "노트 검색해줘"
  - "백링크 조회해줘"
  - "파일 이동해줘 (obsidian)"
capabilities:
  - app_level_vault_management
  - automated_link_heavy_refactoring
  - property_metadata_caching
  - plugin_and_daily_note_automation
  - error_mining_and_gotcha_avoidance
references_path: "./references"
status: active
---

# 🖥️ Obsidian CLI 3.0

## 1. Overview
Obsidian 앱의 인덱스, 링크 그래프, 메타데이터 캐시를 직접 활용하여 볼트를 조작하는 고급 스킬입니다.

## 2. Dynamic Workflow
본 조작 전 **시스템 함정(Gotchas)**과 **앱 환경(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify CLI**: `which obsidian`으로 CLI 가용성을 확인하고, 대상 볼트는 `vault="MS_Thoughts.nosync" (또는 "MS_Library.nosync")` 파라미터로 명시합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 앱 세션 충돌 및 인덱스 지연 오류를 방지합니다.

### Phase 1: Target Identification
조작하거나 검색할 대상 노드를 위키링크 또는 경로 형식으로 식별합니다.

### Phase 2: Execute Command
`obsidian` 명령어를 사용하여 CRUD, 속성, 태그, 링크 분석 등을 수행합니다. 명령지는 [cli-commands.md](./references/cli-commands.md)를 참조하십시오.

### Phase 3: Reflect & Verify
변경 사항이 앱에 즉시 반영되었는지 확인하고 결과를 보고합니다. 실행 수칙은 [best-practices.md](./references/best-practices.md)를 참조하십시오.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 앱 세션 충돌 및 경로 오류 방지 가이드.
- [cli-commands.md](./references/cli-commands.md): 핵심 명령어 및 파이프라인 수칙.
- [best-practices.md](./references/best-practices.md): CLI 운영 수칙 및 GUI 프로토콜.

---
*Created by MS_Dev Third Gen Standard*
