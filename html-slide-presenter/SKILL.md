---
name: html-slide-presenter
description: >
  Generates a synchronized HTML presentation suite with on-screen QR code modal and mobile touch remote. Use when the user asks to create an interactive HTML presentation, dual slide deck, presenter view notes, or mobile remote slides.
  키워드: 발표자 모드 슬라이드, 듀얼 슬라이드, 모바일 리모컨, QR 코드 발표 리모컨, HTML 프레젠테이션, 발표 대본 슬라이드
version: 1.1.0
status: active
author: MS_Dev
triggers:
  - "/presenter-slide"
  - "/dual-slide"
  - "발표자 슬라이드 제작"
  - "모바일 리모컨 슬라이드"
  - "발표 대본 덱 생성"
---

# HTML Dual Slide & Mobile Presenter Deck Generator

Generate a synchronized 2-file HTML presentation suite with mobile touch remote and on-screen QR code connection:
1. **Main Slide Deck (`*_slides.html`)**: Fullscreen 100vw × 100vh canvas with live drawing tools (highlighter, pen, laser pointer), fullscreen toggle, and on-screen QR code modal (`Q` key).
2. **Mobile Presenter Remote (`*_presenter.html`)**: Mobile-first touch remote with real-time clock, stopwatch timer, slide-by-slide speaker notes, swipe gestures, haptic feedback, and jump buttons.
3. **Local Sync Server (`serve_deck.py`)**: Zero-cache, 100ms ultra-fast wireless sync server between MacBook projection screen and mobile devices.

Both windows communicate bi-directionally via HTTP Fast-Polling (with BroadcastChannel and localStorage fallbacks).

---

## Operating Contract

- Always extract or generate both **on-screen slide content** and **conversational speaker notes** for each slide.
- Generate two output HTML files in the target directory using the standard templates under `templates/`.
- Ensure keyboard shortcuts and mobile touch swipe work seamlessly across devices.
- Do not hardcode absolute paths in generated files.

---

## Slide Structure Contract

Each slide requires:
1. **Tag & Eyebrow**: Short section badge (e.g. `PROBLEM`, `ESSENCE`, `TOOL`, `DEMO`).
2. **Title & Heading**: Main slide title and punchy one-sentence headline.
3. **Body Content**: Visual cards (`.grid-2`, `.grid-3`), quote banners, or structured points.
4. **Speaker Notes (대본 품질 표준)**:
   - **형식 (완결된 액션 큐 & 블릿 기호)**: 미완성 어절(`~속에서.`, `~현실.` ❌) 금지. 공감 큐, 핵심 주장, 다음 전환 브릿지가 포함된 실전 스피치 큐로 작성
   - **서체 (고딕체)**: `Pretendard`, `Noto Sans KR` 등 가독성 높은 산세리프 고딕 적용
   - **문단형식 (내어쓰기)**: `text-indent: -1.35em; padding-left: 1.35em;` 적용으로 줄바꿈 시 블릿 뒷부분으로 정렬

---

## Keyboard & Remote Controls

### Main Presentation (`*_slides.html`)
- **Next / Prev**: `→` / `Space` / `Enter` / `PageDown` | `←` / `PageUp` / `Backspace`
- **Number Jump**: `1` ~ `9` (jump directly to slide)
- **QR Remote Modal**: `Q` (toggle on-screen mobile connection QR code)
- **Presenter Window**: `W` (open presenter popup on same machine)
- **Fullscreen**: `F` (toggle fullscreen)
- **Highlighter**: `H` (yellow highlighter mode)
- **Pen**: `P` (red ballpoint pen mode)
- **Laser**: `L` (glowing laser pointer dot)
- **Clear Canvas**: `C` (clear drawing on current slide)
- **Pointer Reset**: `ESC` (return to standard mouse cursor / close QR modal)

### Mobile Remote (`*_presenter.html`)
- **Touch Gestures**: Swipe Left (Next Slide) | Swipe Right (Prev Slide) with haptic vibration
- **Buttons**: Next (`▶`), Prev (`◀`), Direct Jump buttons (`1` ~ `N`)
- **Font Size**: `가+` / `가-` buttons
- **Timer Control**: `⏸️` (pause/resume) | `🔄` (reset to 00:00)

---

## Running & Serving Presentation

### 1. Launch Wireless Sync Server
Run the bundled sync runner inside the presentation directory:

```bash
python3 serve_deck.py
```

- **Projector Screen**: Opens `http://localhost:8080/slides` automatically on MacBook.
- **Mobile Remote**: Press `Q` on MacBook to show the QR code, or scan to open `http://<LOCAL_IP>:8080/presenter`.

### 2. Build via Python Builder
Generate `deck.json` and compile:

```bash
python3 scripts/build_dual_slides.py deck.json -o ./output -n my_lecture
```
