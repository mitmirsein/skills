# TDD: Testing Patterns & Templates

다양한 언어와 프레임워크에서의 표준 테스트 패턴입니다.

## 🐍 Python (`pytest`)
```python
def test_should_return_correct_value():
    # Arrange (준비)
    input_val = 5
    # Act (실행)
    result = calculate(input_val)
    # Assert (검증)
    assert result == 10
```

## 📜 TypeScript (`jest` / `vitest`)
```typescript
describe('Calculator', () => {
    it('should add numbers correctly', () => {
        // expect(add(1, 2)).toBe(3);
    });
});
```

## 🛠️ Mocking Strategy
- **Python**: `unittest.mock` 또는 `pytest-mock` 사용.
- **Node.js**: `jest.spyOn()` 또는 `msw` (API 가상화) 사용.
- **Core Rule**: 외부 시스템(Network, File System, DB)과의 상호작용은 반드시 Mocking 처리하여 테스트 속도와 결정성을 확보합니다.
