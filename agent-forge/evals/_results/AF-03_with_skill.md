# AF-03 · With-Skill 출력 (agent-forge v6.1.0 활성)

> 프롬프트: "여러 명의 신학자 에이전트가 협력하여 한 본문을 다양한 관점(역사비평, 조직신학, 목회적 적용)으로 분석하는 팀 스킬을 설계해줘. #forge"
> 실행일: 2026-05-18 · 실행자: Claude (agent-forge 5-Phase + harness-architecture-patterns 교리 준수)

---

## Phase 1: Architecting & Ops Design

- **환경 스캔**: `theology-scholar`(단일 학술 종합), `rise-exegesis-sermon`(석의→설교 파이프라인) 존재. 그러나 **동일 본문을 복수 관점으로 동시 분석 후 통합**하는 팀 스킬은 없음 → 신규 정당(경계 조건: "다관점 병렬 + 통합").
- **Source of Truth**: `references/harness-architecture-patterns.md`(6대 패턴), 워크스페이스 헌법(신학적 긴장 보존).

## Phase 2: Precision Assembly — 아키텍처 패턴 결정

### 패턴 선택 (harness-architecture-patterns.md 의사결정 트리 적용)
- 에이전트 2개 이상 + **실시간 교차 검증/발견 공유 필요** → **팀 모드(기본값)**.
- 동일 입력(본문)에 **서로 다른 전문 관점**을 **병렬 독립** 분석 → **패턴 2: 팬아웃/팬인 (Fan-out / Fan-in)**. 교리표상 ⭐⭐⭐ "반드시 팀으로 구성".

```
                  ┌→ [역사비평 신학자] ─┐
[본문 분배] ─────→ ├→ [조직신학자]      ─┼→ [통합 편집자 (Fan-in)]
                  └→ [목회적 적용가]    ─┘
```

### 에이전트 분리 (4축 판단표 적용)
| 축 | 판정 |
|---|---|
| 전문성 | ✅ 분리 — 역사비평/조직/목회는 상이한 전문 지식 |
| 병렬성 | ✅ 분리 — 세 관점은 동시 수행 가능(독립) |
| 컨텍스트 | ✅ 분리 — 각자 다른 1차/2차 자료 세트 |
| 재사용성 | ✅ 분리 — 각 전문가는 타 하네스에서도 재사용 |
→ **3 전문가 + 1 통합자** 구성 확정.

### 생성 파일: `multi-lens-exegete/SKILL.md` (frontmatter 발췌)
```yaml
name: multi-lens-exegete
description: 한 성서 본문을 역사비평·조직신학·목회적 적용 3개 전문가 에이전트가 병렬 분석한 뒤 통합 편집자가 신학적 긴장을 보존하며 종합하는 Fan-out/Fan-in 팀 스킬.
version: 1.0.0
triggers: ["#다관점석의", "본문 통합 분석", "multi-lens exegesis"]
capabilities: [parallel_multi_perspective_analysis, tension_preserving_synthesis]
```

### Fan-in(통합) 설계 — 품질 결정 단계
- 통합 편집자는 세 산출을 **merge**하되, harness 교리상 "통합 단계 품질이 전체를 결정".
- **헌법 주입**: 세 관점이 충돌할 때 **신학적 긴장을 단일 결론으로 평탄화 금지** — 긴장을 명시적으로 보존(예: "역사비평은 A, 조직신학은 B로 본다 — 이 긴장 자체가 본문의 신학적 깊이").
- 무한 루프 방지: 통합 재요청 최대 2회(Producer-Reviewer 교리 차용).

## Phase 3: Validation
- `evals/evals.json`에 ML-01(단일 본문 3관점 통합 출력), ML-02(관점 충돌 시 긴장 보존) 등록.

## Phase 4: Deployment
- 팀 모드 등록. 통합자 출력 스키마를 명시(경계면 교차 검증).

---
**산출 요약**: Fan-out/Fan-in 패턴 채택 · 4축 분리 기준(전문성·병렬성) 적용 · 통합(Fan-in/merge/synthesis) 단계가 긴장 보존과 함께 설계됨.
