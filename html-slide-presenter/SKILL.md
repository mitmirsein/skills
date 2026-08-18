---
name: html-slide-presenter
description: >
  Generates a synchronized dual-window HTML presentation deck (fullscreen main slides with canvas drawing tools + presenter view with real-time timer, clock, speaker notes, and jump navigation). Use when the user asks to create an interactive HTML presentation, dual slide deck, or presenter view notes.
  키워드: 발표자 모드 슬라이드, 듀얼 슬라이드, HTML 프레젠테이션, 발표 대본 슬라이드
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "/presenter-slide"
  - "/dual-slide"
  - "발표자 슬라이드 제작"
  - "발표 대본 덱 생성"
---

# HTML Dual Slide & Presenter Deck Generator

Generate a synchronized 2-file HTML presentation suite:
1. **Main Slide Deck (`*_slides.html`)**: Fullscreen 100vw × 100vh canvas with live drawing tools (highlighter, pen, laser pointer) and fullscreen toggle.
2. **Presenter View (`*_presenter.html`)**: Independent popup window with real-time clock, stopwatch timer, slide-by-slide speaker notes, next slide preview, and jump buttons.

Both windows communicate bi-directionally in real-time via `BroadcastChannel` (with `localStorage` sync fallback).

---

## Operating Contract

- Always extract or generate both **on-screen slide content** and **conversational speaker notes** for each slide.
- Generate two output HTML files in the target directory using the standard templates under `templates/`.
- Ensure keyboard shortcuts work seamlessly across both windows (Arrow keys, Space, PageUp/PageDown, number jump keys).
- Do not hardcode absolute paths in generated files.

---

## Slide Structure Contract

Each slide requires:
1. **Tag & Eyebrow**: Short section badge (e.g. `PROBLEM`, `ESSENCE`, `TOOL`, `DEMO`).
2. **Title & Heading**: Main slide title and punchy one-sentence headline.
3. **Body Content**: Visual cards (`.grid-2`, `.grid-3`), quote banners, or structured points.
4. **Speaker Notes (대본)**: Natural, spoken-language script for the presenter.

---

## Keyboard Shortcuts

### Main Presentation (`*_slides.html`)
- **Next / Prev**: `→` / `Space` / `Enter` / `PageDown` | `←` / `PageUp` / `Backspace`
- **Number Jump**: `1` ~ `9` (jump directly to slide)
- **Presenter Window**: `W` (open presenter popup)
- **Fullscreen**: `F` (toggle fullscreen)
- **Highlighter**: `H` (yellow highlighter mode)
- **Pen**: `P` (red ballpoint pen mode)
- **Laser**: `L` (glowing laser pointer dot)
- **Clear Canvas**: `C` (clear drawing on current slide)
- **Pointer Reset**: `ESC` (return to standard mouse cursor)

### Presenter View (`*_presenter.html`)
- **Next / Prev**: `→` / `Space` / `Enter` | `←` / `Backspace`
- **Font Size**: `가+` / `가-` buttons
- **Timer Control**: `⏸️` (pause/resume) | `🔄` (reset to 00:00)

---

## Build Methods

### Method A: Automated via Python Builder
Generate `deck.json` and compile via builder script:

```bash
python3 scripts/build_dual_slides.py deck.json -o ./output -n my_lecture
```

### Method B: Direct HTML Generation
Use the standard templates located in `templates/` and inject the computed slide elements, titles array, and speaker notes JSON.
