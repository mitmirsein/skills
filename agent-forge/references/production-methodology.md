# Agent Forge: Production Line & Methodology

에이전트 제작소의 고정밀 공정(High-Precision Production Line) 매뉴얼이다.
**이 문서는 SKILL.md의 5-Phase 워크플로우를 상술할 뿐, 표준의 권위는 SKILL.md에 있다**
(충돌 시 SKILL.md 우선). 공정은 SKILL.md의 Phase 1~5와 1:1 대응한다.

## 제 1공정: 아키텍트 및 테스트 설계 (Architect & Eval Design)
에이전트 배포 전 성공 지표를 정의한다.
1. **환경 스캔**: 스킬 루트(`.skills/` — 정본 `~/Desktop/MS_Dev.nosync/.skills/`)를 `ls`하여 중복·유사 기능 스킬을 확인한다. 프로젝트 공유본은 `projects/*/skills`, `projects/*/.skills`, `projects/*/.agents/skills`를 별도 포크로 본다.
2. **의도 정의**: 에이전트의 핵심 임무와 트리거 상황을 구체화한다.
3. **테스트 케이스(Evals) 작성**: `evals/evals.json`에 실전 테스트 프롬프트를 미리 구상한다.

## 제 2공정: 정밀 조립 및 작법 (Precision Assembly)
검증된 작법(Writing Patterns)을 적용한다.
- **Source of Truth Identification**: 에이전트가 참조해야 할 공식 문서 URL을 발굴하여 `sources_of_truth` 메타데이터에 명시한다. (Knowledge Gap 해소)
- **Knowledge DNA**: 모델의 기본 지식 이후 변경된 최신 사양을 'Overview & DNA' 섹션에 우선 배치한다.
- **Why Factor**: 모델에게 강압적 지시보다 이론적 배경과 논리를 설명하여 행동을 유도한다.
- **Gotcha Mining**: 과거 유사 작업 로그를 분석하여 AI가 흔히 범하는 '지식 함정'을 찾아 `gotchas.md`에 명제화한다.
- **Dynamic Knowledge Workflow**: `SKILL.md` 1단계에 반드시 'Fetch & Verify'(sources_of_truth 대조) 단계를 포함시켜 지능의 최신성을 강제한다.
- **Config-Driven (선택)**: 사용자 개인화가 *실제로 필요한 경우에만* `config.json`을 둔다. 불필요한 config는 안티패턴(과잉 구성)이다.

## 제 3공정: 실전 검증 루프 (Validation Loop)
- **성능 측정**: 생성된 스킬을 실제로 적용하여 소요 시간, 토큰 사용량, 성능을 Baseline과 대조한다.
- **반복 개선**: 피드백에 따라 프롬프트 문구와 논리를 미세 조정(Refactoring)한다.

## 제 4공정: 오케스트레이션 및 배치 (Phase 4 — Deployment)
- **물리적 배치**: 단일 표준(SKILL.md 표) 폴더 구조를 준수하여 파일을 생성한다.
- **Reflection Setup (선택)**: 장기 맥락 재사용이 실제로 필요한 스킬에 한해 `history.log` 참조 프로토콜을 둔다.

## 제 5공정: 메타-하네스 최적화 (Phase 5 — Outer Loop)
배치로 끝나지 않는다. 기존 스킬의 실행 추적(Raw Execution Traces)을 분석하여 자율 재작성한다.
상세는 [meta-harness-optimization-loop.md](./meta-harness-optimization-loop.md)를 따른다.

---
*SKILL.md 단일 표준의 구현 매뉴얼. 버전·표준은 SKILL.md를 따른다.*
