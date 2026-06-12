# Design System Inspiration of Notion

## 1. Visual Theme & Atmosphere
Notion's website embodies the philosophy of the tool itself: a blank canvas that gets out of your way. The design system is built on warm neutrals rather than cold grays, creating a distinctly approachable minimalism that feels like quality paper rather than sterile glass.

**Key Characteristics:**
- NotionInter (modified Inter) with negative letter-spacing
- Warm neutral palette: grays carry yellow-brown undertones
- Near-black text via `rgba(0,0,0,0.95)` -- micro-warmth
- Ultra-thin borders: `1px solid rgba(0,0,0,0.1)` throughout

## 2. Color Palette & Roles
| Token Name | Hex Code | Role |
| :--- | :--- | :--- |
| **Warm White** | `#f6f5f4` | Secondary Background |
| **Pure White** | `#ffffff` | Main Page/Card Background |
| **Notion Black** | `rgba(0,0,0,0.95)` | Primary Text |
| **Notion Blue** | `#0075de` | Link/Interactive Accent |
| **Soft Gray** | `#f1f1ef` | Hover Backgrounds/Badges |
| **Whisper Border** | `rgba(0,0,0,0.1)` | Subtle Borders |

## 3. Typography Rules
- **Font**: `Inter` (or NotionInter)
- **H1**: Weight 700, Letter-spacing -0.02em
- **Body**: Weight 400, Line-height 1.55, Letter-spacing -0.01em

## 4. Component Stylings
- **Cards**: Minimalist, often without padding or borders, using whitespace to define boundaries.
- **Elevation**: Multi-layered soft shadows for shallow depth.

## 5. Agent Prompt Guide
- **Atmosphere**: "Create an approachable minimalist interface using warm neutrals and near-black text."
- **Borders**: "Use whisper-thin borders (rgba(0,0,0,0.1)) for subtle section separation."
- **Typography**: "Apply Inter font with slightly negative letter-spacing for a professional, documentation-style look."
