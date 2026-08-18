# 템플릿 (Templates) 규격

Obsidian Web Clipper가 사용하는 기본 Frontmatter 구조와 본문 템플릿을 정의합니다. `read_url_content`를 통해 추출한 데이터를 이 템플릿에 맞춰 합성하십시오.

## 1. Default Clipping Template

```markdown
---
title: "{page_title}"
source: "{page_url}"
author: "{author_if_available}"
published: "{publish_date_if_available}"
created: {current_date_YYYY-MM-DD}
description: "{page_description_or_summary}"
tags:
  - clippings
---

# {page_title}

{cleaned_markdown_content}
```

## 2. 변수 매핑 가이드 (Variable Mapping)

- `{page_title}`: 웹페이지의 `<title>` 또는 첫 번째 `<h1>` 헤딩. 쌍따옴표(`"`)를 이스케이프 처리하거나 제거해야 합니다.
- `{page_url}`: 사용자가 스크랩을 요청한 원본 URL.
- `{author_if_available}`: 본문이나 메타데이터에서 식별된 작성자. 없으면 필드 생략 가능.
- `{publish_date_if_available}`: 본문이나 메타데이터에서 식별된 발행일. 없으면 필드 생략 가능.
- `{current_date_YYYY-MM-DD}`: 이 스크랩 작업이 수행된 현재 날짜 (예: `2026-04-24`).
- `{page_description_or_summary}`: 본문의 첫 단락, 메타 Description, 또는 에이전트가 생성한 1~2줄의 간략한 요약.
- `{cleaned_markdown_content}`: `gotchas.md`의 규칙에 따라 정제된 깨끗한 마크다운 본문.

## 3. 파일 생성 규칙
- **File Name**: `{page_title}.md` (Windows/macOS 파일 시스템에서 금지된 특수문자 `\/:*?"<>|`는 반드시 공백이나 언더스코어로 치환).
- **Directory**: 대장이 특별히 지정하지 않으면 기본적으로 `~/Desktop/MS_Library.nosync/Clippings/` 또는 작업 지시에 명시된 폴더를 사용합니다.
