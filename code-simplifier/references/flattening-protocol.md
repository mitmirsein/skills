# Code Simplifier: Flattening Protocol (Early Return)

복잡한 조건문과 루프 구조를 해체하여 인지 부하(Cognitive Load)를 최소화하기 위한 4단계 평탄화 파이프라인입니다.

## 🚀 4-Phase Pipeline

### 1. Analyze (스캔)
- 대상 파일의 로직 트리와 추상화 깊이를 분석합니다.
- 중첩된 `if` 블록, 거대한 `switch`, 깊은 루프 등 간소화 타겟을 식별합니다.

### 2. Flatten (평탄화)
- **Early Return**: `if (!condition) return;` 형식을 사용하여 조건이 만족되지 않는 경우를 먼저 처리함으로써 코드의 중첩 레벨을 1~2단계로 축소합니다.
- **Guard Clause**: 본 로직 시작 전 방어 코드를 최상단에 배치하여 본문의 인덴트(Indent)를 걷어냅니다.

### 3. Strip (정리)
- 사용되지 않는 변수(`unused`), 과도하게 중복된 장황한 표현, 불필요한 일시 로직을 제거합니다.
- 복잡한 정규식이나 난해한 원라이너 대신 명확하고 투명한 선언적 코드로 교체합니다.

### 4. Report (지표 보고)
- 작업 전/후의 간소화 성과를 정량적으로 보고합니다.
- 예: "7단계 중첩 → 1단계 평탄화 완료. 코드 라인 45% 축소."

## 🎨 Pattern: Before vs After
```javascript
// BEFORE (Nested)
function processRequest(req) {
  if (req) {
    if (req.user) {
      if (req.user.isActive) {
        // 본 로직 (4단계 중첩)
      }
    }
  }
}

// AFTER (Flattened)
function processRequest(req) {
  if (!req || !req.user || !req.user.isActive) return;
  // 본 로직 (1단계 중첩)
}
```
