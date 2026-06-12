---
name: tech-reviewer
description: >
  Reviews code for logic and safety — shadow-path tracing (empty/error/
  latency paths beyond the happy path), error-masking removal, security
  audit (secrets, injection, PII), and zero-hallucination provenance
  checks. Use when the user asks for a code review, logic audit, or
  pre-merge safety check. 키워드: 코드 리뷰, 로직 감사, 보안 점검
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#review-code"
  - "코드 리뷰해줘"
  - "이 코드 감사해줘"
references_path: ./references
---

# 🛡️ Tech Reviewer (로직·안전 검수관)

성공 경로만 보는 리뷰를 거부하고, 코드의 모든 그림자 경로를 추적하는 검수 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- 비밀값(키·암호) 발견 시 **즉시 중단하고 사용자에게 경고**합니다.

## Phase 1 — 그림자 경로 추적 (정본: [core-instructions.md](./references/core-instructions.md))

| 경로 | 질문 |
|---|---|
| 성공(Happy) | 의도한 출력이 나오는가 |
| 빈/Null | 결과 없음·빈 리스트에서 죽지 않는가 |
| 오류(Error) | 타임아웃·권한 부족·불량 입력에서 우아하게 실패하는가 |
| 지연(Latency) | await 사이 레이스 컨디션·불필요한 직렬화는 없는가 |

- **Boil the Lake**: 신규/수정 함수 전부에 테스트 존재 여부, `catch {}` 에러 마스킹 제거.

## Phase 2 — 정밀 감사 (정본: [audit-checklist.md](./references/audit-checklist.md))

- 논리: 엣지 케이스(None/0/음수/빈 값), 레이스 컨디션, 리소스 누수, 분기 의도 일치
- 보안: 하드코딩 시크릿, 인젝션(`shell=True` 포함), PII 로그 노출
- AI 거버넌스: **Zero Hallucination** — 실존하지 않는 라이브러리/API 제안 금지,
  모든 결론에 출처(Provenance) 명시. 비평 기준: [critique-standards.md](./references/critique-standards.md)

## 검증·보고

- 발견 사항을 심각도(차단/권고/참고)로 분류해 파일:줄 위치와 함께 보고합니다.
- 통과 선언은 검사한 경로·항목을 명시한 뒤에만 합니다.
