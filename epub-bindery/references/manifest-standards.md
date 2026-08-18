# EPUB Bindery: Manifest & Metadata Standards

전자책의 품질과 유지가능성을 위한 `book_manifest.yaml` 규격 및 메타데이터 관리 규정입니다.

## 📄 `book_manifest.yaml` Schema
```yaml
title: "도서 제목"
author: "저자명"
creator: "MS_Dev"
date: "YYYY-MM-DD"
language: "ko-KR"
identifier: "urn:uuid:..." # 선택 사항
rights: "ⓒ 2026. All rights reserved."
publisher: "MS_Library.nosync Publishing"
tags: ["Theology", "Meditation"]
cover-image: "cover.jpg"
stylesheet: "epub_style.css"
order:
  - 00_Introduction.md
  - 01_Chapter.md
  - 99_Conclusion.md
```

## 📜 Metadata Guidelines
- **Title & Author**: 책의 얼굴이 되는 정보를 Manifest 최상단에 배치합니다.
- **Language**: 다국어 폰트 렌더링에 영향을 주므로 `ko-KR`, `en-US`, `de-DE` 등을 정확히 명시합니다.
- **TOC Depth**: 기본값은 2로 설정하여 세부 목차까지 탐색 가능하게 합니다.
- **Identifier**: 고유 ID가 필요한 경우 자동으로 UUID를 생성하여 부여할 수 있습니다.
