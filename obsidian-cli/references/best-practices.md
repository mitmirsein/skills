# Obsidian CLI: Best Practices & Rules

Obsidian CLI와 파일 시스템 직접 조작 사이의 균형 및 안전 운영 수칙입니다.

## 🎯 CLI vs Direct File Access
| 상황 | 추천 방식 | 이유 |
| :--- | :--- | :--- |
| **이동/이름 변경** | ✅ **CLI** | 링크 및 백링크 자동 업데이트 보장. |
| **내용 추가/수정** | ✅ **CLI** | 앱 내 인덱스 및 캐시 즉시 반영. |
| **전체 내용 교체** | ⚡ **직접 조작** | CLI가 전체 교체를 지원하지 않을 때 유용. |
| **검색/관계 분석** | ✅ **CLI** | 백그라운드 인덱스 활용으로 매우 빠름. |
| **대용량 파일 읽기** | ⚡ **직접 조작** | 특정 라인 범위만 읽기 가능 (`view_file`). |

## 🛡️ Operational Rules
1. **GUI Focus Prohibition**: 백그라운드 환경에서 `open`, `command` 등 GUI 포커스를 요구하는 명령은 충돌(Exit 133)을 일으키므로 절대 사용하지 마십시오.
2. **Path & Vault**: 항상 절대 경로(`~/bin/obsidian`)와 `vault="MS_Thoughts.nosync"`를 명시하십시오.
3. **JSON Parsing**: 검색 및 목록 조회 시 `format=json` 플래그를 사용하여 결과의 가독성과 처리 용이성을 확보하십시오.
4. **Stderr Suppression**: `2>/dev/null`을 사용하여 불필요한 로딩 메시지나 경고가 출력되지 않도록 하십시오.
