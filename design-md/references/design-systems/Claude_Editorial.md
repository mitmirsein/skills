# Design System Inspiration of Claude (Anthropic)

## 1. Visual Theme & Atmosphere
Claude's interface is a literary salon reimagined as a product page — warm, unhurried, and quietly intellectual. The entire experience is built on a parchment-toned canvas (`#f5f4ed`) that deliberately evokes the feeling of high-quality paper rather than a digital surface.

**Key Characteristics:**
- Warm parchment canvas (`#f5f4ed`) evoking premium paper, not screens
- Custom Anthropic type family: Serif for headlines, Sans for UI, Mono for code
- Terracotta brand accent (`#c96442`) — warm, earthy, deliberately un-tech
- Exclusively warm-toned neutrals — every gray has a yellow-brown undertone

## 2. Color Palette & Roles
| Token Name | Hex Code | Role |
| :--- | :--- | :--- |
| **Parchment** | `#f5f4ed` | Main Page Background |
| **Ivory** | `#faf9f5` | Card/Surface Background |
| **Anthropic Near Black** | `#141413` | Primary Text |
| **Olive Gray** | `#5e5d59` | Secondary/Muted Text |
| **Terracotta** | `#c96442` | Brand Accent (CTA/Links) |
| **Border Warm** | `#e8e6dc` | Subtle Borders |

## 3. Typography Rules
- **Headline**: `Anthropic Serif`, Weight 500, Letter-spacing -0.01em
- **Body**: `Anthropic Sans`, Weight 400, Line-height 1.6
- **Code**: `Anthropic Mono`, Weight 400

## 4. Component Stylings
- **Cards**: Surface `Ivory (#faf9f5)`, Border `1px solid Border Warm (#e8e6dc)`, Radius `8px`
- **Buttons**: Background `Terracotta (#c96442)`, Text `#FFFFFF`, Radius `6px`

## 5. Agent Prompt Guide
- **Atmosphere**: "Use a warm, parchment-toned (#f5f4ed) background to create a literary and intellectual atmosphere."
- **Typography**: "Use Serif fonts for headlines with a Weight of 500 and near-black (#141413) color."
- **Accents**: "Use Terracotta (#c96442) for all active links and call-to-action buttons."
