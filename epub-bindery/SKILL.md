---
name: epub-bindery
description: >
  Compiles Markdown files into a publication-grade EPUB ebook via pandoc —
  chapters, metadata manifest, embedded fonts, and theme templates. Use
  when the user asks to bind notes or a folder into an ebook or publish
  as EPUB. 키워드: 전자책 제작, EPUB 변환, 제본소, 출판
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#출판"
  - "#epub"
  - "제본소 가동"
  - "이 폴더 epub으로 만들어줘"
  - "publish these notes as ebook"
capabilities:
  - pandoc_epub_compilation
  - font_embedding_typography
  - automatic_manifest_generation
  - chapter_level_segmentation
  - error_mining_and_gotcha_avoidance
references_path: "./references"
status: active
---

# 📚 EPUB Bindery 3.0

## 1. Overview
마크다운 문서들을 조립하여 정밀한 타이포그래피와 챕터 분리가 적용된 출판물 수준의 EPUB 전자책을 생산하는 전문 제본소 도구입니다.

## 2. Dynamic Workflow
본 스킬은 제본 전 **기술적 함정(Gotchas)**과 **제본 설정(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 책의 제목, 작가, 폰트 임베딩 옵션을 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 폰트 미포함 및 내부 링크 파손을 방지합니다.

### Phase 1: Intake & Planning
대상 문서를 분석하고 제본 순서(`book_manifest.yaml`)를 제안합니다. 규격은 [manifest-standards.md](./references/manifest-standards.md)를 참조하십시오.

### Phase 2: Pre-processing (Smilzo)
Smilzo 에이전트가 내부 링크를 정제하고 애셋 경로를 매핑합니다.

### Phase 3: Compile (Pandoc)
Pandoc 엔진으로 스타일을 적용하여 컴파일합니다. 상세 옵션은 [compilation-guide.md](./references/compilation-guide.md)를 참조하십시오.

### Phase 4: Archive (Quality Gate)
최종 파일을 검수하고 `900 Archive/` 폴더로 영구 보전합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 타이포그래피 붕괴 및 경로 오류 방지 가이드.
- [compilation-guide.md](./references/compilation-guide.md): Pandoc CLI 옵션 및 실행 지침.
- [manifest-standards.md](./references/manifest-standards.md): 매니페스트 YAML 규격 및 메타데이터 작성 표준.

---
*Created by MS_Dev Third Gen Standard*
