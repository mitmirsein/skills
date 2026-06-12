# 배치 5 구현안 — dev-tools 카테고리 (2026-06-12)

14개 전부 A등급 달성 (insane-search는 배치 3에서 선처리).

## 신규 SKILL.md 5건 (references 기반 복원, 각 1.0.0)
- **tech-architect**: 구조 정리(전/후 트리 Blueprint, 삭제는 dry-run→승인) + 행동 보존 리팩토링.
- **tech-reviewer**: 그림자 경로 추적(성공/빈/오류/지연), Boil the Lake, 보안 감사,
  Zero Hallucination 출처 의무. 비밀값 발견 시 즉시 중단 규칙.
- **tech-tdd**: RGR 사이클(RED 실패를 실제 확인), 공개 행동만 테스트, 안티패턴 명문화.
- **langgraph-supervisor**: Supervisor-Worker 5단계 상태 루프 + Human Interrupt 결재.
- **log-miner**: 4종 광물(아이디어/스니펫/본능/할일) 채굴 + PII 차단 + 원본 처리 사용자 확인.

## 유령 참조 2건 실증 기반 보수
- **react-components**: 실재하지 않던 references/qa-validation.md를 scripts/validate.js
  실제 동작(@swc AST 파싱·인터페이스·Tailwind 검사) + architecture-checklist 기반으로 작성.
  Phase 0의 유령 config.json 참조 → npm install/validate 점검으로 교체.
- **agent-forge**: 자체 gotchas.md 부재 → 스킬 공장 함정(표준 미준수 생성, 유령 참조 양산,
  트레이스 없는 재작성, 중복 양산) 작성. STANDARDS/validate.py 준수를 description에 내장.

## prompt-engineer (1.0.0 → 1.1.0) — 모델명 재평가 및 버전 중립화
- **판정 변경**: GPT-5.5/Claude 4.7/Gemini 3.1은 "유령"이 아니라 지식 컷오프(2026-01) 이후
  실재 가능 모델로 재평가. 삭제 대신 **파일명·헤더를 버전 중립화**(claude-/gpt-/gemini-
  prompt-strategies.md)하고, 현재 확정 앵커(Fable 5/Opus 4.8/Sonnet 4.6/Haiku 4.5)와
  "버전 진화 — 단정 전 공식 문서 확인" 원칙을 명기. validate.py의 유령 모델 검사 목록 철회.

## description 하이브리드화 9건 (패치 범프)
git-workflow, github-ops, code-simplifier, tech-strategist, agent-forge, stealth-browser
(insane-search 에스컬레이션 관계 명시), react-components, lightpanda-recon(150줄 초과분
푸터 정리), prompt-engineer.
