---
name: create-slide-image-prompts
description: >
  Builds image-generation prompts for Master Of Slide decks from a distilled
  GPT Image 2 cheat-sheet — hero artwork, infographics, posters, thumbnails,
  UI mockups, avatars, and storyboards. Use when a slide needs bitmap
  visuals or the user asks for slide image prompts.
  키워드: 슬라이드 이미지 프롬프트, 이미지 생성, 히어로 이미지
version: 1.0.1
references_path: ./references
status: active
---

# Create Slide Image Prompts

This skill turns a short visual request or slide outline into image-generation
prompts suitable for slide assets. Use it inside `create-slide`,
`create-slide-from-markdown`, and `slide` whenever bitmap visuals would improve
the deck.

Only write generated or copied assets under `slides/<id>/assets/`. Do not modify
the source Markdown note.

When invoked from `/slide`, respect the user's requested image count. If the
count is missing, ask for it before planning assets. If the user delegates the
choice, default to 2 generated images.

## Prompt Assembly

Use this structure:

```text
[subject] + [composition] + [style] + [environment] + [lighting] + [typography/layout] + [details] + [aspect_ratio]
```

Fill these variables:

- `subject`: what the image shows
- `composition`: framing, focal subject, hierarchy
- `style`: visual aesthetic
- `environment`: background or setting
- `lighting`: lighting mood
- `typography`: text-safe area, labels, callouts, or no text
- `details`: materials, props, texture, atmosphere
- `aspect_ratio`: landscape, portrait, or square

Default ratios:

- Slide hero, cover, thumbnail, banner, UI mockup: `landscape`
- Poster, profile, vertical campaign: `portrait`
- Logo experiment, product cutout, general asset: `square`

## Category Recipes

레시피 전문(프롬프트 원형 7종)은 **[category-recipes.md](./references/category-recipes.md)**가
정본이다. 에셋을 계획한 뒤, 해당 카테고리의 레시피를 읽고 프롬프트를 조립한다.

| 카테고리 | 용도 |
|---|---|
| Profile / Avatar | 프로필, 캐릭터 아바타, 호스트 초상, 페르소나 카드 |
| YouTube Thumbnail / Cover | 강렬한 커버 슬라이드, 섹션 오프너, 고대비 타이틀 |
| Infographic / Diagram | 설명 슬라이드, 워크플로우, 비교, 단계별 시각화 |
| Product / Brand Poster | 제품·서비스·브랜드·캠페인 비주얼 |
| E-Commerce Hero | 판매 덱, 랜딩 목업, 제품 상세 비주얼 |
| UI Mockup / App Screen | 앱 컨셉, 대시보드, SaaS 인터페이스 슬라이드 |
| Storyboard / Character Sheet | 시나리오, 여정, 캐릭터 기반 설명 |

## Slide Asset Rules

- Generate the requested number of images. If fewer images would be better,
  explain briefly and ask only if reducing the count would materially change the
  user's requested deck.
- Prefer one strong hero image over decorative filler.
- Keep Korean text out of generated images unless the user explicitly needs it;
  add Korean text as React text for editability.
- Ask for or use real screenshots, logos, and private photos instead of
  hallucinating them.
- Avoid fake charts and fake documents. Use diagram-style abstractions instead.
- Save generated images under `slides/<id>/assets/`.
- Import assets with `import hero from './assets/hero.png';` and render with
  `<img src={hero} alt="..." />`.

## When Image Generation Is Available

If the current agent environment can generate images, create the bitmap asset
after writing the final prompt. Save it under `slides/<id>/assets/` with a
descriptive filename.

If image generation is not available, write precise `ImagePlaceholder` hints or
include an `imagePrompts` section in your final handoff so the user can generate
assets later.

## Output

For each planned asset, produce:

- page number or page role
- category recipe used
- final prompt
- target filename under `slides/<id>/assets/`
- whether the asset was generated, copied, or left as a placeholder
