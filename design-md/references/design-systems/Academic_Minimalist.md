# 📖 Academic Minimalist (개인 연구자/소개 표준 스타일)

> **"지적인 투명함과 정제된 미니멀리즘이 결합된 학술적 포트폴리오 스타일"**
> Reference: jinalee.org

이 문서는 개인 연구 성과, 논문, 프로젝트 등을 정갈하게 보여주기 위한 시각적 규성입니다. 텍스트의 권위와 가독성을 최우선으로 합니다.

---

## 1. Visual Theme & Atmosphere
- **Mood**: Airy · Intellectual · Transparent · Professional
- **Concept**: **"여백의 미(White Space)"**. 구성 요소들 사이의 충분한 거리를 두어 사용자가 정보의 흐름을 스트레스 없이 따라가도록 설계합니다.
- **Core Aesthetic**: 복잡한 장식(Shadow, Gradient)을 배제하고 타이포그래피와 미세한 보더(Border)만으로 정체성을 구축합니다.

---

## 2. Color Palette & Roles

| Token Name | Hex | Role |
| :--- | :--- | :--- |
| **Canvas Off-white** | `#FAFAFA` | 기본 배경색 (순백색보다 눈이 편안함) |
| **Ink Black** | `#1A1A1A` | 헤드라인 및 본문 텍스트 (고대비) |
| **Label Gray** | `#757575` | 메타 정보, 부가 라벨, 비활성 텍스트 |
| **Surface White** | `#FFFFFF` | 카드 내부, 강조 영역 배경 |
| **Border Light** | `#E5E7EB` | 카드 테두리, 구분선 |

### Semantic Badges (Status Labels)
- **Status Green**: `BG: #D1FAE5, Text: #065F46` (승인됨, 검토 완료)
- **Status Amber**: `BG: #FEF3C7, Text: #B45309` (진행 중, 주의 필요)
- **Status Neutral**: `BG: #F3F4F6, Text: #4B5563` (일반 정보)

---

## 3. Typography Rules

### Sans-serif (Main Stack)
- **Font**: `Inter`, `Pretendard`, `Segoe UI`, `Helvetica Neue`
- **Scale**:
    - **Name/Main Title**: `2.5rem (40px) / 700 (Bold)`
    - **Section Title**: `1.75rem (28px) / 600 (Semibold)`
    - **Body Lettering**: `1.125rem (18px) / 400 (Regular) / Line-height 1.6`
    - **Overline Label**: `0.875rem (14px) / 600 (Semibold) / UPPERCASE / Spacing 0.05em`

---

## 4. Component Stylings

### Project/Research Cards
- **Background**: `#FFFFFF`
- **Border**: `1px solid #E5E7EB`
- **Radius**: `8px`
- **Interaction**: 호버 시 테두리 색상을 `#D1D5DB`로 변경 (미세한 변화).

### Section Layout
- **Container**: `Max-width: 1050px`
- **Inner Padding**: `Top/Bottom: 4rem ~ 6rem`
- **Element Gap**: `Grid 24px` 또는 리스트 형태의 수직 나열.

---

## 5. Agent Prompt Guide

에이전트가 이 스타일을 구현할 때의 핵심 가이드:

- **배경 설정**: "`Canvas Off-white (#FAFAFA)` 배경을 사용하고, 섹션 간 패딩을 대담하게(6rem 이상) 배치하라."
- **타이포그래피**: "헤드라인은 `Ink Black (#1A1A1A)`으로 묵직하게 배치하고, 설명 텍스트는 `1.125rem` 크기에 행간을 1.6 이상으로 넉넉하게 주어라."
- **라벨링**: "날짜나 태그는 `UPPERCASE`와 자간 확장을 적용하여 `Label Gray (#757575)` 색상으로 작게 표시하라."
- **장식 배제**: "그림자(box-shadow)나 그라데이션을 절대 사용하지 말고, 오직 1px 보더로만 영역을 구분하라."

---

> **비고**: 이 스타일은 대장의 개인 연구 소개나 학술 논문 아카이브 페이지에 최적화되어 있습니다.
> 저장 위치: `.skills/design-md/references/design-systems/Academic_Minimalist.md`
