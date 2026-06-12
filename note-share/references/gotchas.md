# 📤 Note Share: Gotchas & Anti-Patterns

노트 웹 공유 및 URL 갱신 시 에이전트가 주의해야 할 사항입니다.

## 1. Dispatch Pitfalls (발송의 함정)
- **인코딩 오류**: 파일 경로에 한글이나 특수문자가 포함될 때 Advanced URI 인코딩을 제대로 하지 않으면 Obsidian이 요청을 무시합니다.
- **앱 미실행**: Obsidian 앱이 켜져 있지 않은 상태에서 URI를 보내는 것은 무의미합니다. 앱 상태를 먼저 점검하십시오.

## 2. Capture Failures (캡처 실패)
- **pbpaste 타이밍**: 공유 명령을 보낸 직후 클립보드에 URL이 들어오기까지 시간이 걸립니다. 너무 빨리 `pbpaste`를 호출하여 이전 클립보드 내용을 가져오는 실수를 방지하십시오. (최소 1-2초 대기)
- **잘못된 URL 가로채기**: 클립보드에 담긴 내용이 실제 공유 URL인지 정규식으로 검증하십시오.

## 3. Metadata Errors (메타데이터 오류)
- **Property 덮어쓰기**: 기존에 존재하던 중요 메타데이터를 지우고 공유 URL만 남기는 파괴적 업데이트를 하지 마십시오.
- **비공개 정보 유출**: 민감한 태그나 노트를 무분별하게 웹에 올리지 않도록 공유 전 'Public' 태그 여부를 확인하십시오.

---
*Created by MS_Dev Third Gen Standard*
