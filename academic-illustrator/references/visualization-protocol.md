# Academic Illustrator: Visualization & Fallback Protocol

신학/인문학 도식을 출판물 수준의 시각적 언어로 번역하기 위한 3단계 파이프라인과 폴백 지침입니다.

## 🌈 Visualization Pipeline (RICE Track)

### 1. Architect (뼈대 설계)
- 텍스트 분석 후 11가지 도식 원형을 매핑한 노드(Node)와 엣지(Edge) 구조를 사용자에게 공개합니다.
- 반드시 체크포인트에서 사용자 승인이 떨어질 때까지 렌더링하지 않습니다.

### 2. Stylist (미학 지시어)
- **Academic Aesthetic**: 카툰/유아적 스타일을 배제하고, 벡터 스타일의 깨끗하고 정밀한 형태를 지향합니다.
- **Composition**: `[원형 형태] + [학술적 배경/톤] + [레이아웃 비율 16:9] + [선/도형 스타일] + [텍스트 최소화 지시]`
- **Palette**: 차분한 파스텔톤, 슬레이트 블루, 소프트 그레이 등 학술적 색조를 사용합니다.

### 3. Visualizer (렌더링 & 폴백)
- `generate_image`를 통해 이미지를 렌더링합니다.
- **Image Spec**: 1920×1080 (16:9), PNG 포맷.

## 🔄 Mermaid Fallback (신뢰 중심)
- **Trigger**: `generate_image` 호출 실패, 또는 렌더링된 이미지 내 문자가 뭉개지는 현상이 발생할 경우 즉시 발동합니다.
- **Action**: 즉시 Mermaid 코드로 전환하여 명확한 구조를 제공합니다.
```mermaid
graph TD / flowchart / ...
```
- 사용자에게 이미지 생성 실패 사실과 대체 도식을 제공했음을 고지합니다.
