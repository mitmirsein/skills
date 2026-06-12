# Canvas & Vertical Budget — 1080px Discipline (정본)

Every page renders into a fixed **1920 × 1080** canvas. The framework scales it automatically.

## Absolute Metric Rule
*   Use **absolute pixel values** for `font-size`, padding, positioning. No `rem`, `em`, `vw`, `vh`, or `%` for type.
*   Root element must fill canvas: `width: '100%', height: '100%'`.
*   Prefer inline `style={{ ... }}`. Scope classnames carefully as CSS imports are global.

## Type Scale & Spacing
*   **Hero Title**: 140–200px
*   **Section Heading**: 80–120px
*   **Page Heading**: 56–80px
*   **Body Text**: 32–44px
*   **Caption/Label**: 22–28px
*   **Content Padding**: 100–160px from canvas edges.
*   **Breathing Room**: 32–64px gap between elements.

## Vertical Budget Calculation
The canvas does **not** scroll. Anything below 1080px is silently cropped. Design within the usable vertical budget:
*   **Usable Height** = `1080 − top_padding − bottom_padding`. (e.g., 120px padding on each side = **840px** budget).
*   **Element Height** = `font_size × line_height × number_of_lines`.
*   A bullet wrapping to 2 lines counts as 2 lines. Add gaps (32–64px) between elements.

**Vertical Height Budget Example (Usable: 840px):**
*   Heading: 80px × 1.2 × 1 line = **96px**
*   Gap = **64px**
*   Body: 40px × 1.6 × 3 lines = **192px**
*   Gap = **48px**
*   5 bullets: 40px × 1.6 × 1 line each = **320px**
*   4 gaps between bullets: 24px each = **96px**
*   **Total = 816px** (Fits within 840px budget ✅)

If the content exceeds the budget, **split it into two pages**.
