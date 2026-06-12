---
name: theology-reviewer
description: >
  Reviews a specific theological paper across eight dimensions (structure,
  argument, comparison, history, paradigm, ecosystem, etc.) with agentic
  7-source evidence gathering and a dual-lens advocate/critic audit,
  producing an in-depth critique report. Use when the user asks to review
  or critique a particular paper. 키워드: 논문 비평, 리뷰, 심층 분석
version: 10.5.1
codename: Evidence Contract
author: MS_Dev
triggers:
  - "#review"
  - "#비평"
  - "review this paper"
  - "이 논문 비평해줘"
  - "Parrehsia v10 프로토콜 가동"
capabilities:
  - eight_dimensional_analysis        # 8섹션(I~VIII) + 섹션별 분석 질문 32개
  - agentic_evidence_gathering        # Phase 0: QuerySet → 7중 증거 수집 (S2 API + Labs + Quick + IxTheo + Crossref + KCI + RISS)
  - dual_lens_audit                   # Pass 1(Advocate) + Pass 2(Critic) 분리 실행
  - dialectical_verification          # Phase 2: 8축 검증 + 적대적 재구성 + 투명성 보고
  - semantic_scholar_api              # Semantic Scholar Graph API 자동 연동 (s2_runner.py)
  - google_scholar_labs_semantic      # Google Scholar Labs 자동 연동 (scholar_runner.py JSONL)
  - google_scholar_quick_integration  # CDP 기반 Google Scholar (토큰 0)
  - ixtheo_searcher_integration       # Tübingen Index Theologicus 연동 (ixtheo_searcher.py)
  - crossref_journal_integration      # Crossref Premium Theology Journal 연동 (crossref_journal_searcher.py)
  - kci_searcher_integration           # KCI (한국학술지인용색인) 연동 (search.py)
  - riss_searcher_integration          # RISS (학술연구정보서비스) 연동 (search.py)
  - theological_method_checklist      # 12개 방법론 체크리스트 자동 참조
  - phase2_compatible_annotation      # [TokenName] 형식 강제 → Phase 2 자동 파싱
project_engine: "projects/easy-review-system"
references_path: "./references"
status: active
---

# 🏛️ Theology Reviewer 10.5 (Unified + Evidence Contract)

## 1. 역할 정의 (Role Boundary)

> **스킬(Skill)**: ARC v4.0 오케스트레이터. 언제, 무엇을, 어떤 순서로 실행할지 결정.  
> **프로젝트(Project)**: 도메인 지식 엔진. 프롬프트·라이브러리·설정을 보유.
> **범위 제외**: `MS_Brain.nosync/500 Parrehsia/parrehsia` 프론트엔드는 자동 연결 대상이 아니다. 리뷰 산출물은 기본적으로 `MS_Brain.nosync/000 System/Inbox/Review_Reports`와 `Evidence`에 저장한다.

```
[theology-reviewer skill]          [easy-review-system project]
─────────────────────────          ──────────────────────────────
 오케스트레이션 로직          →    prompts/unified_review.json.md (v10.1)
 ARC v4.0 연동               →    prompts/dialectical_verification.json.md
 Google Scholar Labs 호출    →    configs/tool_registry.json.md
 google-scholar-quick 호출    →    configs/master_config.json.md
 출력 경로 결정              →    configs/theological_methods.json (신설)
                             →    configs/annotation_tokens.json
```

> ⚠️ **스킬은 프로젝트 내부 파일을 절대 경로로 하드링크하지 않는다.**  
> 모든 경로는 `config.json`의 `engine_root`를 통해 동적으로 해석한다.

---

## 2. Dynamic Workflow

본 비평 수행 전 **비평 함정(Gotchas)**과 **프로젝트 엔진 설정(Config)**을 먼저 점검합니다.

### Phase 0: Gather (Evidence Collection) — [선택적]
- **목적**: EvidencePack 확보
- **실행**: `scripts/review_engine.py [논문_파일] --phase 0`
- **자동**: QuerySet 생성 → Semantic Scholar API + Google Scholar Labs + google-scholar-quick + IxTheo + Crossref + KCI + RISS → EvidencePack 저장
- **Labs 규약**: `google-scholar-semantic`이 `tre_terms.csv` 기반 독일어/영어/고전어 쿼리 확장, 40초 Wait Protocol, 세션당 최대 4쿼리, `--citation-depth all`, JSONL 변환을 수행
- **KCI/RISS 규약**: 한국학술 검색 효율을 극대화하기 위해 문장형 의문문에서 의문사/조사 등의 불용어를 정제한 뒤 파편화된 키워드로 자동 우회 쿼리 수행
- **산출물**: `EvidencePack.json`, `QuerySet.json`, `ToolLog.json` → `MS_Brain.nosync/000 System/Inbox/Evidence/`

### Phase 1: Unified Review (Analysis)
- **실행**: `scripts/review_engine.py [논문_파일] --phase 1`
- **프롬프트**: `unified_review.json.md` v10.1 (PRIMARY)
  - 8섹션 × 분석 질문 최대 5개
  - `theological_methods.json`의 12개 방법론 체크리스트 자동 적용
  - `[TokenName]` 형식 강제 — Phase 2 파싱 호환
- **산출물**: 핸드오프 패킷 → 에이전트가 최종 리뷰 마크다운 생성

### Phase 2: Dialectical Verification ⚡ NEW
- **실행**: `scripts/review_engine.py [논문_파일] --phase 2 --review [리뷰.md]`
- **5단계 파이프라인**:
  1. **Claim Extraction** — 리뷰 내 모든 사실적 주장(citation/assertion/interpretation) 파싱
  2. **Triangulated Verify** — 원본 논문 역참조 + google-scholar-quick(CDP) + EvidencePack(보너스)
  3. **Adversarial Recon** — `[Critique]` 토큰별 저자 진영 반격 문헌 검색 → `Critique-Validated` / `Critique-Under-Review` 판정
  4. **Confidence Calibrate** — `✅ Anchored` / `⚠️ Unverified` / `❌ Contradicted` 자동 라벨링
  5. **Selective Regen** — `❌` 섹션만 외과적 재작성 + 투명성 보고서 생성
- **산출물**: `verified_claims.json`, `transparency_report.md`, `p2_handoff_packet.json`

### 전체 파이프라인 일괄 실행
```bash
uv run python \
  .skills/theology-reviewer/scripts/review_engine.py \
  [논문_파일_경로] --phase all

# Phase 2만 단독 실행 (기존 리뷰에 적용)
uv run python \
  .skills/theology-reviewer/scripts/review_engine.py \
  [논문_파일] --phase 2 --review [기존_리뷰.md]

# 브라우저/네트워크 없이 설정과 EvidencePack 계약 점검
uv run python .skills/theology-reviewer/scripts/review_engine.py --self-test
```

---

## 3. Verification Triangle (검증 Heptad-Engine + 8축)

Phase 2에서 사용하는 실전 검증 수단:

| 검증 축 | 도구 | 상태 | 커버리지 |
| :--- | :--- | :---: | :--- |
| Axis 1: 원본 논문 역참조 | 첨부 파일 직접 비교 | ✅ 항상 | 내부 인용 정합성 |
| Axis 2: Google Scholar Labs | google-scholar-semantic JSONL | ✅ **v10.5 계약 반영** | 질적 맥락·최신 논쟁 지형 |
| Axis 3: google-scholar-quick | CDP · Google Scholar (일반 검색) | ✅ 실전 | 외부 문헌 실존 검증 |
| Axis 4: Semantic Scholar API | s2_runner.py (S2 Graph API) | ✅ | 구조화 메타데이터·인용 보강 |
| Axis 5: Tübingen IxTheo | ixtheo_searcher.py | ✅ **v10.5 추가** | 유럽·독일어권 정밀 신학 문헌 |
| Axis 6: Crossref Journal | crossref_journal_searcher.py | ✅ **v10.5 추가** | 58종 프리미엄 신학 저널 검색 |
| Axis 7: KCI 한국학술지 | kci-api-searcher (`search.py`) | ✅ **v10.5 추가** | 국내 신학 문헌 및 신학자 논지 검증 |
| Axis 8: RISS 학술정보 | riss-searcher (`search.py`) | ✅ **v10.5 추가** | 국내 학위논문, 학술지, 단행본 추적 |
| Axis Bonus: EvidencePack | Phase 0 산출물 (7중 검색기 수집분) | ⚪ 선택적 | 교차검증 보너스 |

---

## 4. Configuration (config.json)

경로·모델·출력 설정은 `./config.json`에서 관리합니다.  
프로젝트 엔진 경로가 변경되면 **config.json만 수정**하면 됩니다.
구조는 `config.schema.json`을 따릅니다.

---

## 5. Reference Links

- [gotchas.md](./references/gotchas.md): 용어 혼선 및 ARC v4.0 규격 함정 목록
- [config.json](./config.json): 엔진 경로·출력 경로·S2/Labs/google-scholar-quick 설정 및 KCI/RISS 설정
- [config.schema.json](./config.schema.json): 스킬 설정 스키마
- [evidencepack-schema.md](./references/evidencepack-schema.md): Phase 0 → Phase 1/2 EvidencePack 계약
- [review_engine.py](./scripts/review_engine.py): Phase 0/1/2 파이프라인 구현체 (22 메서드)

**프로젝트 엔진 참조 (engine_root 기준)**:
- `prompts/unified_review.json.md` → v10.1, 분석 질문 32개, Phase 2 호환
- `prompts/dialectical_verification.json.md` → Phase 2 전용 검증 프롬프트
- `configs/theological_methods.json` → 12개 방법론 체크리스트
- `configs/annotation_tokens.json` → 13개 토큰 단일 진실 출처(SoT)

---
*MS_Dev Unified Standard — v10.5.0 (KCI/RISS Integrated) | 2026-05-21*
