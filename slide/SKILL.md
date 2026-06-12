---
name: slide
description: >
  Turns a Markdown/Obsidian document into a Master Of Slide deck and edits
  existing decks — workflow, theme selection, and the technical contract for
  React pages under slides/<id>/index.tsx. Use when the user invokes /slide
  <markdown-path>, asks to create slides from a note, or wants to tweak a
  deck's layout, palette, or pages.
  키워드: 슬라이드 생성, 슬라이드 수정, 덱 제작, 마크다운 슬라이드
version: 4.0.1
codename: Unified
author: MS_Dev
triggers:
  - "/slide"
  - "slide [path]"
  - "Create slides from [path]"
  - "edit slide"
  - "tweak this page"
  - "fix the layout"
  - "change the palette"
references_path: ./references
status: active
---

# 🛝 Unified Slide & Authoring Skill

`/slide <markdown-path>` is the one-command workflow for creating or editing a Master Of Slide deck from a local Markdown/Obsidian note.

You only write files under `slides/<id>/`. Never modify the source Markdown note.

## 1. High-Level Invocation & Scoping

### User Commands
*   `/slide /absolute/path/to/source.md` · `slide <path>` · `Create slides from <path>`
*   If no Markdown path is present, ask for one. Resolve relative paths from the current workspace root.

### Pre-Creation Questions
Before writing files, ask for missing decisions:
*   **Page Count**: "몇 장짜리 슬라이드로 만들까요?"
*   **Image Count**: "생성 이미지는 몇 개 넣을까요?"
*   **Visual Theme**: "어떤 테마로 만들까요?"

If the user wants speed or says to decide automatically, default to **8 pages, 2 generated images, and `auto` theme**.
If image generation is unavailable, still ask for the intended image count, then create that many precise `ImagePlaceholder` hints instead of bitmap assets.

### Theme Selection Guide
If ask-user-question UI is available, ask the theme question as a choice picker with these Korean options:

*   `auto (자동 추천)` — 문서 장르, 청중, 이미지 성격을 보고 가장 맞는 테마를 고른다.
*   `editorial-noir (다크 매거진)` — 뉴스 인사이트, 에세이, 실사/시네마틱 덱. Canva 이식성 높음.
*   `paper-press (종이 리포트)` — 리포트, 강의안, 긴 한국어 설명에 맞는 밝은 인쇄물 스타일.
*   `neon-terminal (터미널)` — 개발자 데모, CLI/툴링, 코드 설명에 맞는 어두운 터미널 스타일.
*   `neo-brutalism (네오 브루탈리즘)` — 굵은 검정 테두리, 강한 그림자, 선명한 색의 강한 스타일.
*   `research-brief (연구 브리프)` — 절제된 선, 표, 차트, 설명형 레이아웃의 연구/교육 스타일.
*   `vercel-minimal (미니멀 제품)` — 흰 배경, 얇은 선, 시스템 다이어그램 중심 미니멀 스타일.
*   `raycast-dark-product (다크 제품)` — 어두운 SaaS/제품 런칭 느낌, UI 패널 + 붉은 accent.
*   `photo-editorial-tech (실사 테크 매거진)` — 실사 PNG와 절제된 텍스트의 테크 매거진 스타일.

## 2. Technical Reference & File Contract

### Hard Rules
*   Slide folder: `slides/<kebab-case-id>/`. Entrypoint: `slides/<id>/index.tsx`. Assets under `slides/<id>/assets/`.
*   Do **not** touch `package.json`, `open-slide.config.ts`, or other slide folders.
*   Do not add dependencies — only `react` and standard web APIs.
*   Do not create `README.md` or other prose files inside the slide folder.

### File Contract
```tsx
// slides/<id>/index.tsx
import type { Page, SlideMeta } from '@open-slide/core';

const Cover: Page = () => <div>…</div>;
const Body: Page = () => <div>…</div>;

export const meta: SlideMeta = { title: 'My slide' };
export default [Cover, Body] satisfies Page[];
```
*   `export default` must be a **non-empty array of zero-prop React components**, one per page.
*   The slide id is the kebab-case folder name (`q2-roadmap`, `amos-chapter-4`).

## 3. 기술 정본 (References)

| 문서 | 내용 |
|---|---|
| [canvas-and-budget.md](./references/canvas-and-budget.md) | **1080px 수직 예산 규율** — 절대 픽셀 규칙, 타입 스케일, 예산 계산식·예시 |
| [design-and-template.md](./references/design-and-template.md) | DesignSystem 토큰, `var(--osd-X)` 바인딩, React 스타터 템플릿 전문, 에셋·ImagePlaceholder 규칙 |

JSX를 쓰기 전에 두 문서를 반드시 읽는다. 수직 예산 계산 없이 페이지를 쓰지 않는다.

## 4. Self-Review Checklist

- [ ] `slides/<id>/index.tsx` exports a non-empty `Page[]` default array.
- [ ] Every page root fills `100% × 100%`.
- [ ] Content respects the 100–160px padding margins.
- [ ] Every page satisfies the height budget: `(font_size × line_height × lines) + gaps + 2×padding ≤ 1080px`.
- [ ] Bullets do not wrap to a second line.
- [ ] One coherent visual direction (palette + typography).
- [ ] The `design: DesignSystem` constant is exported and values are bound via `var(--osd-X)`.
- [ ] All imported assets exist under `slides/<id>/assets/`.
- [ ] No files outside `slides/<id>/` were edited.

## 5. Anti-Patterns to Avoid

*   ❌ Walls of text (split the page if body contains >40 words).
*   ❌ Vertically overflowing 1080px canvas limits.
*   ❌ Shrinking fonts below 28px or padding below 100px to squeeze content.
*   ❌ `overflow: auto/scroll` wrappers (hides layout bugs instead of fixing them).
*   ❌ Inconsistent palettes or mixed typography families between pages.
*   ❌ Installing custom npm packages (only core React/Browser APIs are allowed).
*   ❌ Writing prose or `README.md` files inside the slide folder.

## 6. 검증·보고

완료 시 보고: 슬라이드 id·경로, 페이지 수, 선택 테마, 에셋 처리 내역(생성/복사/플레이스홀더),
프리뷰 URL `http://127.0.0.1:5173/s/<id>`. 체크리스트(§4) 통과 여부를 명시한다.
