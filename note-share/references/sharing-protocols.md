# Note Share: Sharing Protocols & Command IDs

Obsidian 노트를 웹으로 공유하기 위한 플러그인 사양 및 명령 ID 모음입니다.

## 1️⃣ Share Note (1순위 - 기본값)
- **share**: `share-note:share-note` (현재 파일 공유)
- **force-upload**: `share-note:force-upload` (변경 여부와 상관없이 강제 업로드)
- **delete**: `share-note:delete-note` (공유 삭제)
- **copy-link**: `share-note:copy-link` (공유 URL 클립보드 복사)

## 2️⃣ Just Share Please (JSP) (2순위 - 폴백)
- **share**: `just-share-please:share` (현재 파일 공유, 클립보드에 URL 복사)
- **update**: `just-share-please:update` (공유된 파일의 변경 사항 업데이트)
- **delete**: `just-share-please:delete` (공유된 링크 삭제)
- **copy**: `just-share-please:copy` (공유된 URL 다시 클립보드에 복사)

## 🛡️ Pre-requisites
1. Obsidian 앱 실행 중이어야 합니다.
2. `Advanced URI` 플러그인이 설치/활성화되어 있어야 합니다.
3. 대상 공유 플러그인(JSP 또는 Share Note)이 설치/활성화되어 있어야 합니다.
