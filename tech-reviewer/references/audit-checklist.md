# Tech Reviewer: Logic & Security Audit Checklist

코드의 무결성과 안전성을 보장하기 위한 정밀 검수 항목입니다.

## 🕵️ Logic Audit (논리 검증)
- **Edge Cases**: 입력값이 `None`, `0`, 음수, 혹은 빈 리스트일 때의 동작은 정의되었는가?
- **Race Conditions**: 공유 리소스에 대한 접근이 안전한가 (Lock, Thread-safe)?
- **Resource Leaks**: 파일이나 소켓이 사용 후 명확히 닫히는가 (`with` 구문 사용 등)?
- **Logic Integrity**: `if/else` 조건문의 분기가 실제 기획된 의도와 일치하는가?

## 🛡️ Security Audit (보안 검증)
- **Hardcoded Secrets**: API 키, 비밀번호 등이 평문으로 하드코딩되어 있지 않은가?
- **Injection Risks**: SQL 인젝션 또는 위험한 쉘 실행(`shell=True`)이 포함되어 있는가?
- **PII Exposure**: 개인정보나 민감한 데이터가 로그에 기록되고 있지 않은가?
- **Secret Detection**: 비밀값이 발견되면 즉시 중단하고 사용자에게 경고(Warn)를 보냅니다.

## 🤖 AI Era Verification (AI 검증)
- **Zero Hallucination Audit**: 제안된 로직이나 지배적인 정보가 실존하는 라이브러리 및 데이터에 근거하는가?
- **Source Tracing Validation**: 에이전트가 어떤 데이터(파일, 로그, 웹)를 참조하여 결론을 도출했는지 출처가 명확히 명시되었는가?
