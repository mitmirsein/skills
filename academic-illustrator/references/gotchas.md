# 🎨 Academic Illustrator: Gotchas & Anti-Patterns

학술 다이어그램 생성 및 개념 시각화 시 에이전트가 주의해야 할 사항입니다.

## 1. Visualization Pitfalls (시각화의 함정)
- **과도한 장식 (Chartjunk)**: 학술 다이어그램의 핵심은 '명료함'입니다. 불필요한 그림자, 그라데이션, 화려한 3D 효과 대신 깔끔한 벡터 스타일을 유지하십시오.
- **논리적 부정확성**: 화살표의 방향이나 도형의 겹침(Overlapping)이 실제 신학적 개념의 선후 관계나 상호 침투(Perichoresis)와 일치하는지 엄밀히 검토하십시오.

## 2. Technical Failures (기술적 실패)
- **텍스트 붕괴 (Text Corruption)**: DALL-E와 같은 이미지 생성 도구는 상세한 텍스트 렌더링에 취약합니다. 긴 문장을 이미지에 넣으려 하지 말고, 핵심 키워드만 사용하거나 Mermaid로 전환하십시오.
- **Archetype 오용**: 단순히 멋져 보인다고 동심원 구조를 쓰지 마십시오. 개념이 층위(Layer)를 가질 때만 동심원을 사용하십시오.

## 3. Agentic Errors (에이전트적 오류)
- **Mermaid 폴백 지연**: 이미지 생성이 계속 실패하거나 텍스트가 심하게 깨지는데도 계속 `generate_image`를 시도하지 마십시오. 2회 실패 시 즉시 Mermaid 코드로 전환하여 논리적 구조를 보여주십시오.

---
*Created by MS_Dev Third Gen Standard*
