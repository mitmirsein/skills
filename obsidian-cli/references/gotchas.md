# 🖥️ Obsidian CLI: Gotchas & Anti-Patterns

Obsidian CLI를 이용한 볼트 조작 및 노트 관리 시 에이전트가 주의해야 할 사항입니다.

## 1. Sync Pitfalls (동기화의 함정)
- **앱 세션 무시**: Obsidian 앱이 켜져 있는 상태에서 파일을 직접 수정(Direct I/O)하면 앱의 내부 캐시와 충돌하여 데이터가 유실되거나 덮어씌워질 수 있습니다. 반드시 CLI(`obsidian` 명령)를 통해 앱에 변경 사항을 알리십시오.
- **색인 지연 (Index Lag)**: 대량의 파일을 생성하거나 이동한 직후에는 Obsidian의 검색(Search)이나 백링크 인덱싱이 완료되지 않았을 수 있습니다.

## 2. Path Errors (경로 오류)
- **위키링크(WikiLink) 해석**: Obsidian은 파일명이 유일할 경우 폴더 경로 없이 `[[Note Name]]`만으로 연결을 허용합니다. 하지만 CLI 작업 시에는 모호성 방지를 위해 항상 '전체 상대 경로'를 사용하거나 고유 ID를 확인하십시오.
- **대소문자 민감도**: macOS/Windows 등 OS에 따라 파일명의 대소문자 구분이 다를 수 있으나, Obsidian 내부 링크는 대소문자를 구분합니다.

## 3. Metadata Failures (메타데이터 실패)
- **YAML 구조 파손**: 속성(Properties) 업데이트 시 YAML 문법을 깨뜨리지 마십시오. 특히 콜론(`:`) 뒤의 공백과 리스트(`-`) 들여쓰기를 철저히 준수하십시오.
- **이미지/첨부파일 실종**: 노트를 이동할 때 해당 노트가 참조하는 이미지 파일(`999-Attachments/`)을 함께 옮기지 않으면 링크가 깨집니다.

---
*Created by MS_Dev Third Gen Standard*
