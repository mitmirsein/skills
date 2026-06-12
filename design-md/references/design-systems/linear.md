# 🌑 Linear (DESIGN.md Reference)

> "어둠 속에서 피어나는 정교한 엔지니어링 미학"

## 1. Visual Theme & Atmosphere
- **Core Concept**: Dark-mode-native Precision.
- **Mood**: Dark · Tech-driven · Focused · Luminous
- **Density**: 7/10 — High information density managed through luminance.
- **Backgrounds**: Marketing Black (#08090a), Panel Dark (#0f1011), Level 3 Surface (#191a1b).

---

## 2. Color Palette & Roles
- **Brand Indigo** (#5e6ad2): Primary brand color. Primary CTAs.
- **Accent Violet** (#7170ff): Interactive accents, active states, links.
- **Primary White** (#f7f8f8): Primary text (not pure white to prevent strain).
- **Silver Gray** (#d0d6e0): Body text, secondary content.
- **Tertiary Gray** (#8a8f98): Muted metadata, placeholders.

---

## 3. Typography Rules
- **Font Family**: 
  - **Preferred (KR)**: `Pretendard, "Noto Sans KR", -apple-system, sans-serif`
  - **Standard**: `Inter Variable`, "SF Pro Display", sans-serif
  - **Monospace**: `Berkeley Mono`, ui-monospace, Menlo
- **Hierarchy**:
  - Display XL: 72px, weight 510 (Signature), tight line-height (1.0).
  - Heading 3 (Card): 20px, weight 590.
  - Body (Reading): 16px, weight 400, 1.5 line-height.
- **OpenType**: cv01, ss03 (Geometric alternates) enabled globally for Inter.

---

## 4. Layout Principles
- **Luminance Stacking**: 깊이는 배경색의 불투명도(0.02 → 0.05)로 표현하며, 검은색일수록 더 깊은 레이어를 의미합니다.
- **Borders**: 반투명 흰색 테두리 사용 (`rgba(255,255,255,0.05)`).
- **Spacing**: Base unit 8px.
- **Whitespace**: 어둠 그 자체를 여백으로 활용하여 콘텐츠를 돋보이게 함.

---

## 5. Component Stylings
- **Buttons**:
  - Ghost: `rgba(255,255,255,0.02)` background, #e2e4e7 text, 6px radius.
  - Primary: Brand Indigo (#5e6ad2) background, white text.
- **Cards**: Translucent background (`rgba(255,255,255,0.02)`), whisper-thin border.
- **Status Dots**: Success Green (#10b981) small circular badges.

---

## 6. Do & Don't
- ✅ **Do**: 텍스트에는 `Pretendard` 또는 `Inter`의 Geometric alternate 기능을 활성화하십시오.
- ✅ **Do**: 그림자 대신 배경색의 명도 단계(Luminance Stepping)를 통해 계층을 구분하십시오.
- 🚫 **Don't**: 순수 흰색(#ffffff) 본문 텍스트 지양 (#f7f8f8 사용 권장).
- 🚫 **Don't**: 고체(Solid) 색상 버튼 지양. 다크 모드 특유의 투명도 계층을 유지하십시오.

---
*Derived from oh-my-design / linear.app*
