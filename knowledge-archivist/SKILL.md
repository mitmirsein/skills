---
name: knowledge-archivist
description: >
  Collects web articles and documents into the vault with /collect
  (defuddle-first extraction, full frontmatter, standard naming) and sorts
  inbox material into the ARC folder structure with /organize. Use when the
  user asks to save web sources in bulk, archive research material, or sort
  the inbox into folders. For a single-page clip use obsidian-web-clipper.
  키워드: 자료 수집, 아카이빙, 인박스 분류, defuddle
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "/collect [url]"
  - "/organize"
  - "자료 수집해줘"
  - "인박스 정리해서 분류해줘"
references_path: ./references
---

# 🗄️ Knowledge Archivist (자료 수집·배치 아키비스트)

외부 자료(웹/문서)를 표준 규격으로 수집하고, 인박스의 자료를 ARC 구조로 배치하는 스킬입니다.

### Negative Scope (이 스킬이 하지 않는 것)
- ❌ 단일 페이지 클리핑(Web Clipper 템플릿 규격) → `obsidian-web-clipper`
- ❌ 노트 메타데이터 규격화·점수화 → `arc-librarian`
- ❌ 위키 편찬·병합 → `wiki`

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 분류 방치, 중복 저장, frontmatter 유실,
  고아 노트 생성을 방지합니다.
- 수집 전 동일 URL/제목이 이미 볼트에 있는지 `rg`로 확인합니다.

## Phase 1 — /collect (수집)

- [archival-standards.md](./references/archival-standards.md)의 수집 표준을 따릅니다:
  1. `defuddle parse <url> --md` 우선 사용 (노이즈 제거 본문 추출)
  2. YAML frontmatter 필수 생성: `created`, `source`, `tags`, `summary`, `author`
  3. 파일명: `YYYYMMDD-Title` 또는 학술 자료는 `Author-Year-Title`
- 저장 위치: 기본 `~/Desktop/MS_Brain.nosync/000 System/Inbox/Raw/`
  (사용자 지정 시 해당 경로).

## Phase 2 — /organize (배치)

- 인박스 자료의 내용·맥락을 분석해 ARC 구조(100 Theology / 200 Ministry /
  300 Tech / 900 Archive)로 이동을 **제안**합니다.
- 이동은 대상 파일 목록(dry-run)을 먼저 보여주고 사용자 승인 후 실행합니다
  (볼트 헌법: 일괄 이동 사전 승인).
- 이동 시 `obsidian move`를 사용해 위키링크가 깨지지 않게 합니다.

## 검증·보고

- 수집: 생성 파일 경로, frontmatter 필수 5필드 충족 여부, 본문 표본을 보고합니다.
- 배치: 이동 파일 수와 목적지 분포를 보고하고, 깨진 링크가 없는지 표본 확인합니다.
