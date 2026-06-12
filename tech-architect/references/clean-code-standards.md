# Tech Refactorer: Clean Code & Optimization Standards

코드의 가독성, 유지보수성, 성능을 최적화하기 위한 상세 리팩토링 지침입니다.

## 🌟 Refactoring Philosophy
- **"Leave the campground cleaner than you found it."**
- **Readability is King**: 코드는 읽히기 위해 존재하며, 지루하더라도 명시적인 코드가 '똑똑한' 트릭보다 훌륭합니다.
- **Behavior Preservation**: 리팩토링의 핵심은 기능(Behavior)을 변경하지 않고 구조(Structure)를 개선하는 것입니다.

## 🔍 Diagnostic Checklist (Analysis)
1. **DRY Violation**: 중복된 논리가 여러 곳에서 발견되는가?
2. **Cognitive Load**: 중첩된 루프/조건문이 많아 파악이 어려운가?
3. **Naming**: 변수와 함수명이 의도를 명확히 전달하고 있는가?
4. **Typing & Docs**: 타입 힌트와 Docstring이 누락되지 않았는가?

## 🛠️ Surgical Guidelines (Implementation)
- **Small Units**: 거대한 함수를 독립적인 작은 헬퍼 함수로 분해합니다.
- **Explicit Naming**: 한 글자 변수를 서술형 변수명으로 교체합니다.
- **Modernization**: 최신 언어 스펙(Python 3.12+, ESNext 등)을 활용하여 구문을 간소화합니다.
- **Docstrings**: 클래스와 함수에 목적, 파라미터, 반환값을 명시하는 주석을 추가합니다.

## ✅ Verification
변화된 깊이(Complexity), 개선된 타입 안전성, 중복 제거 효과 등을 수치나 명확한 문장으로 보고합니다.
