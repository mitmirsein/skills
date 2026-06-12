---
name: obsidian-web-clipper
description: >
  Clips a single web page into clean Markdown with official Obsidian Web
  Clipper-compatible frontmatter and saves it into the vault (insane-search
  for paywalled/blocked pages, yt-dlp transcripts for YouTube links). Use
  when the user gives a URL to clip or scrap into Obsidian. For bulk
  collection-plus-filing use knowledge-archivist instead.
  키워드: 웹 클리핑, 스크랩, 클리퍼, URL 저장
version: 1.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "/clip [url]"
  - "#clipper"
  - "이 페이지 스크랩해줘"
  - "웹 클리핑"
capabilities:
  - url_content_fetching
  - youtube_transcript_extraction
  - markdown_cleanup_and_formatting
  - frontmatter_metadata_injection
  - obsidian_vault_direct_save
references_path: "./references"
status: active
---

# ✂️ Obsidian Web Clipper 1.0

## 1. Overview
사용자가 제공한 URL의 웹페이지 콘텐츠를 `read_url_content` (또는 기타 스크래핑 도구)를 통해 추출하고, 불필요한 UI 요소를 제거한 뒤 깨끗한 마크다운(Markdown)으로 정제하여 로컬 Obsidian Vault(예: `MS_Brain.nosync`의 Inbox 또는 지정된 Clippings 폴더)에 바로 저장하는 스킬입니다.

이 스킬은 **공식 Obsidian Web Clipper Extension**의 로컬 에이전트 버전(Local Agent Edition) 역할을 수행하며, 브라우저 확장 프로그램 없이도 대화형 에이전트가 직접 웹 스크랩 및 파일 생성을 처리할 수 있게 합니다.

### Negative Scope (이 스킬이 하지 않는 것)
- ❌ PDF/이미지 파일 처리 → `pdf-extractor`
- ❌ 노트 분류 및 ARC 안치 → `arc-librarian`
- ❌ 온톨로지/엔티티 추출 → `ontology-builder`
- ❌ Obsidian 앱 레벨 조작 → `obsidian-cli`

## 2. Dynamic Workflow

### Phase 0: Setup & Guardrail
- **Verify Config**: [config.json](./references/config.json)에서 기본 저장 경로, 태그 프리셋을 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 노이즈 혼입 및 Frontmatter 구문 오류를 방지합니다.

### Phase 1: INTAKE (URL 수용 및 파싱)
- 대장(User)이 제공한 URL(`[url]`)을 확인합니다.
- (선택) 태그(Tags)나 저장 위치(Folder path)가 함께 제공되었는지 파악합니다.

### Phase 2: FETCH & CLEAN (콘텐츠 추출 및 정제)
- 단순 스크래핑(`read_url_content`)에 의존하지 않고, **`insane-search` 스킬을 호출**하여 대상 웹페이지를 타격합니다. `insane-search`가 페이월(구독 장벽)과 봇 차단(Cloudflare 등)을 모두 뚫고 확보한 깨끗한 원본 텍스트/마크다운을 전달받습니다.
- **YouTube 링크의 경우**: `run_command` 도구를 사용하여 `yt-dlp` 등으로 상세 자막(Transcript)을 추출하고 본문에 포함시킵니다.
- [gotchas.md](./references/gotchas.md)를 참조하여 내비게이션 바, 푸터, 광고 등 본문과 무관한 요소를 제거합니다.
- HTML 테이블이나 이미지 캡션 등을 Obsidian에서 잘 렌더링되도록 교정합니다.

### Phase 3: FORMATTING (메타데이터 템플릿 적용)
- [templates.md](./references/templates.md)에 정의된 YAML Frontmatter 규격에 맞춰 제목, 출처(URL), 클리핑 날짜, 태그 등을 주입합니다.
- 파일명(Note name)은 보통 `{Page_Title}.md` 형식으로 안전하게 생성합니다(특수문자 제거).

### Phase 4: SAVE TO VAULT (볼트에 저장)
- 대장이 별도로 지정하지 않은 경우, 기본 저장소(예: `~/Desktop/MS_Brain.nosync/Clippings/` 또는 대장이 지정한 Clipping 디렉토리)에 `write_to_file` 도구를 사용해 `.md` 파일을 생성합니다.
- 작업 완료 시 생성된 파일 경로와 추출 요약본을 대장에게 보고합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): 깨끗한 마크다운 정제를 위한 주의사항 및 예외 처리 로직
- [templates.md](./references/templates.md): 공식 Web Clipper와 호환되는 Frontmatter 템플릿 구조

---
*Created by MS_Dev Third Gen Skill Forge*
