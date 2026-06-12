---
name: note-share
description: >
  Publishes an Obsidian note to the web via Advanced URI and the Share Note
  plugin (Just Share Please as fallback), captures the public URL from the
  clipboard, and writes it back into the note's share_url property. Use when
  the user asks to share a note, get a public link, or update or delete a
  shared link. 키워드: 노트 공유, 공유 링크, 웹 발행, share url
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "/share [노트명]"
  - "노트 공유해줘"
  - "공유 링크 만들어줘"
references_path: ./references
---

# 📤 Note Share (노트 웹 공유)

Obsidian 노트를 Share Note(1순위)/JSP(폴백) 플러그인으로 웹에 발행하고,
공유 URL을 노트 속성에 기록하는 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 인코딩 오류, pbpaste 타이밍,
  속성 덮어쓰기, 비공개 정보 유출을 방지합니다.
- 사전 조건 점검: Obsidian 앱 실행 중 + `Advanced URI` 플러그인 + 공유 플러그인
  (Share Note 또는 JSP) 활성. 민감한 노트인지(공개 가능 여부) 먼저 확인합니다.

## Phase 1 — 발행 (4-Step Pipeline)

[execution-workflow.md](./references/execution-workflow.md)의 절차를 따릅니다:

1. **URI Encoding**: 파일 경로를 URL 인코딩 (한글·공백 필수 처리)
2. **Advanced URI Call**: `open "obsidian://advanced-uri?...&commandid=share-note:share-note"`
   — 명령 ID는 [sharing-protocols.md](./references/sharing-protocols.md) 참조.
   Share Note 실패 시 JSP(`just-share-please:share`)로 폴백.
3. **Wait & Capture**: 3~5초 대기 후 `pbpaste`로 URL 확보, **정규식으로 URL 형식 검증**
4. **Metadata Update**: `obsidian property:set`으로 `share_url` 속성 기록
   (기존 속성 보존 — 파괴적 갱신 금지)

주의: 이 스킬에서는 공식 CLI의 `command` 서브커맨드를 사용하지 않습니다
(Electron Trace/BPT trap 오류 — gotchas 참조).

## 검증·보고

- 확보한 URL이 실제 공유 페이지인지(정규식 + 필요시 접속 확인) 검증합니다.
- 노트의 `share_url` 속성이 기록되었는지 `obsidian read`로 확인 후,
  공유 URL과 함께 보고합니다.
