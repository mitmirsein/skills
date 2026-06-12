# 🇨🇭 Swiss Design Gráfico (DESIGN.md Reference)

> "Strong grid system, sans-serif typography, asymmetrical layout, and clean lines. The pinnacle of modern functional minimalism."

## 1. Visual Theme & Atmosphere
- **Core Concept**: Modern trend in UI/UX web design focused on clarity, objectivity, and readability.
- **Mood**: Precise · Objective · Minimalist · Dynamic
- **Density**: 3/10 — Airy (High negative space usage)
- **Variance**: 7/10 — Dynamic (Asymmetrical balance)
- **Motion**: 4/10 — Subtle (Ease-out transitions, 200-300ms)

---

## 2. Color Palette & Roles
- **Signal Red** (#D82C2C): Error states, destructive actions, primary accent.
- **Black** (#1A1A1A): Primary background, dark surfaces.
- **White** (#FFFFFF): Primary text (on dark), card surfaces (on light).
- **Cool Grey** (#A9B2B1): Secondary text, borders, muted elements.
- **Deep Blue** (#0033A0): Secondary accent.
- **Light Grey** (#F2F2F2): Muted backgrounds, secondary text.

---

## 3. Typography Rules
- **Primary Typeface**: `Helvetica Neue`, `Helvetica`, `Arial`, `sans-serif`
- **Hero/Display**: Helvetica Neue (700), tight tracking. `clamp(2.5rem, 5vw, 4rem)`
- **Body**: Helvetica Neue (400), 16px, 1.6 line-height, max 72ch.
- **UI Labels**: Helvetica Neue (500), 0.875rem, slight letter-spacing.
- **Monospace**: `JetBrains Mono` for metadata and technical values.

---

## 4. Layout Principles (Grid System)
- **Grid**: 12-column CSS Grid (`grid-template-columns: repeat(12, 1fr)`).
- **Gap**: 20px (`--grid-gap-swiss: 20px`).
- **Composition**: Asymmetrical layout focusing on negative space. No 3-equal-column layouts.
- **Content Alignment**: Flush left, rag right (align: left).
- **Containment**: Max-width 1280px with 1.5rem side padding.

---

## 5. Component Stylings
- **Buttons**: Subtly rounded (0.5rem). Accent fill (#D82C2C). Hover: 8% darken + subtle lift shadow. Active: -1px translate.
- **Cards**: 0.5rem corners. Subtle shadow (`0 2px 12px rgba(0,0,0,0.06)`). 1px border stroke.
- **Inputs**: Label above. 1px border. Focus ring: 2px accent color offset 2px.

---

## 6. Anti-Patterns (Banned)
- 🚫 **No emojis** in UI — use Lucide or Heroicons only.
- 🚫 **No decorative gradients** — use flat color only.
- 🚫 **No pure black (#000000)** — use off-black (#1A1A1A).
- 🚫 **No heavy shadows** — maximum `0 2px 8px rgba(0,0,0,0.08)`.
- 🚫 **No AI clichés** in copywriting ("Elevate", "Seamless", "Unleash").

---
*Source: https://designmd.app/en/library/swiss-design-grafico*
