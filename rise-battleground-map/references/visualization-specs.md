# Battleground Map: Visualization Specifications

신학적 지형 분석 결과를 시각화하기 위한 형식 및 우선순위 규격입니다.

## 🥇 Standard: HTML Interactive Chart
- **Engine**: Chart.js + Tailwind CSS.
- **Output**: 단일 HTML 파일로 생성하여 브라우저에서 인터랙티브하게 탐색 가능하게 합니다.
- **Style**: Dark Academia 또는 시스템의 Visual Stylist 테마를 적용합니다.

## 🥈 Markdown: Mermaid Diagram
- **Type**: `radar` 또는 `poly` 형식을 활용하여 마크다운 문서 내에 즉시 렌더링합니다.
- **Syntax**:
```mermaid
radar
    title "칭의론 지형 분석"
    axes
        "법정적 칭의" : 8
        "실질적 변화" : 5
        ...
    "칼빈" : [8, 5, ...]
    "바르트" : [4, 9, ...]
```

## 🥉 Legacy: ASCII Radar Chart
- 텍스트 전용 환경이나 빠른 확인이 필요한 경우 사용합니다. 기호를 사용하여 대략적인 구도를 표현합니다.

## 📜 Footer Requirement
모든 시각화 출력물 하단에는 반드시 다음 문구를 포함합니다:
`powered by 케리그마출판사 | [Visit Website](https://kerygma.co.kr)`
