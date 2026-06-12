# Code Simplifier: Key Objectives & Principles

"Less is More. 코드는 짧고 투명해야 한다."

## 🎯 Core Objectives
1. **Token Diet (토큰 다이어트)**: 장황한(Verbose) 코드를 압축하여 LLM 컨텍스트 윈도우 점유율을 극적으로 낮춥니다.
2. **Abstraction Flattening (추상화 평탄화)**: 불필요하게 깊은 상속, 복잡한 클래스 메서드, 중첩된 인터페이스를 제거하여 구조를 단순화합니다.
3. **Cognitive Load Reduction (인지 부하 감소)**: 무의미한 주석을 제거하고, 직관적인 변수명과 제어 흐름을 도입하여 가독성을 극대화합니다.

## ⚙️ Execution Principles
- **No Functional Changes**: 기존 비즈니스 로직과 시스템 동작은 **절대** 변경하지 않습니다. 오직 '표현'의 무게만 덜어냅니다.
- **Complexity Stripping**: 기술적 아키텍처 개선(`tech-refactorer`)과 달리, 이 스킬은 철저히 '복잡도 제거'와 '경량화'에만 집중합니다.
- **Indicator Reporting**: 작업 완료 후 "약 XX 라인 축소, 중첩 단계 YY에서 1단계로 평탄화"와 같은 지표를 보고합니다.
