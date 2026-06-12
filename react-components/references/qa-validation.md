# QA Validation — AST 검증기 연동 및 최종 심사 규정

## 실행

```bash
cd .skills/react-components && npm run validate   # node scripts/validate.js
```

`scripts/validate.js`가 `@swc/core`로 TSX를 파싱해 AST 수준에서 검사한다:
- TypeScript/TSX 구문 유효성 (파싱 실패 = 즉시 불합격)
- Props 인터페이스 존재 여부 (`Readonly<T>` 권장)
- Tailwind 사용 이슈 스캔

## 최종 심사 체크리스트

AST 통과 후 [../resources/architecture-checklist.md](../resources/architecture-checklist.md)
(Architecture Quality Gate)를 항목별로 확인한다:
- 로직은 `src/hooks/` 커스텀 훅으로 분리되었는가
- Atomic/Composite 모듈성 — 모놀리식 파일 금지
- 정적 텍스트/URL은 `src/data/mockData.ts`로 이동했는가
- Props `Readonly<T>`, 템플릿 플레이스홀더(`StitchComponent` 등) 실명 교체

## 합격 기준

AST 검사 0 오류 + 체크리스트 전 항목 충족 시에만 변환 완료를 선언한다.
불합격 항목은 파일·줄 위치와 함께 보고하고 수정 후 재검증한다.
