# 🚨 UI Architect Gotchas (감각적/기술적 회피 함정)

이 문서는 프리미엄 웹 디자인을 구현함에 있어 AI가 흔히 저지르는 **"양산형 템플릿(Generic MVP Look)"**의 한계를 깨부수기 위한 안전장치입니다. 모든 렌더링 전 반드시 확인하십시오.

## 1. Color Hardcoding & Primitive Colors (원색 금지)
- **증상**: `red`, `blue`, `#ff0000`, `#0000ff` 등 브라우저 기본 색상이나 순색을 그대로 사용하는 행위.
- **해결책**: 반드시 `DESIGN.md` 에 정의된 브랜드 컬러 스펙(예: `Amber Gold #fbbf24`, `Parchment #f5f4ed`)을 사용하라.

## 2. Inconsistent Shadows (일관성 없는 깊이감)
- **증상**: 구형 박스 섀도우(`box-shadow: 2px 2px 5px gray`)를 사용하여 인터페이스가 플랫하고 촌스러워짐.
- **해결책**: 현대적인 다중 레이어 섀도우(예: `0 4px 24px rgba(0,0,0,0.1)`)를 사용하거나, `DESIGN.md`에 명시된 Elevation 시스템을 따르라.

## 3. Lack of Micro-interactions (죽은 인터페이스)
- **증상**: 버튼이나 카드에 마우스를 올려도 아무 반응이 없는 상태.
- **해결책**: 모든 상호작용 가능한 요소(버튼, 링크, 카드)에는 `transition: all 0.2s ease`와 `hover` 상태의 색상/그림자/크기 변화를 반드시 명시하라.

## 4. Typography Hierarchy Collapse (가독성 파괴)
- **증상**: 모든 텍스트가 `sans-serif`로 도배되거나, 위계에 따른 크기 차이가 미미함.
- **해결책**: 제목은 권위 있는 폰트(Serif 계열 등), 본문은 가독성 위주(Inter, Pretendard)로 정확히 이분화하고, Size와 Weight에 극명한 대비를 두라.

## 5. Over-Crowding (여백 부족)
- **증상**: 요소들이 너무 다닥다닥 붙어 있어 숨쉴 틈이 없음.
- **해결책**: `8px Base Grid`를 준수하고, 컨테이너 내부 패딩은 최소 `24px` 이상을 주어 고급스러운 면모(Negative Space)를 확보하라.
