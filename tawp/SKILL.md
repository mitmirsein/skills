---
name: tawp
description: >
  Runs the Theological Academic Writing Pipeline (TAWP) — from a one-line
  natural-language idea through research, source ingest, minimal ontology,
  adversarial red-team, SBL writing, Claim Ledger hard gate, and final
  PDF audit in 8 phases, producing journal-grade manuscripts. Use when the
  user wants to write a theological essay or paper end-to-end.
  키워드: 신학 글쓰기 파이프라인, 저널급 원고, 에세이 집필
version: 2.3.1
codename: local
author: MS_Dev
triggers:
  - "#tawp"
  - "@tawp"
  - "tawp"
  - "신학 학술 글쓰기 파이프라인"
capabilities:
  - natural_ideation_facilitator
  - trilingual_academic_literature_research
  - minimal_ontology_driven_design
  - adversarial_theological_redteam
  - sbl_chicago_writing_and_linting
  - claim_ledger_quality_gate
  - pre_pdf_unicode_and_typography_gate
  - final_submission_and_pdf_audit
references_path: "./references"
status: active
---

# ⛪ Theological Academic Writing Pipeline (TAWP) v2.3.0-local

## 1. Overview
**TAWP**는 신학도 및 목회자가 대화창에 던진 단 한 줄의 자연어 아이디어(예: *"칼 바르트의 칭의론에 대해 에세이를 쓰고 싶다"*)로부터 시작하여, 고품질 신학 에세이 및 아포리아(신학적 긴장) 명제망을 완성하는 통합 학술 글쓰기 파이프라인입니다. 

기계적인 파일 복사-붙여넣기식 데이터 분석을 지양하고, **글을 쓰기 전 사상의 대립과 핵심 아포리아를 명제망으로 정리하는 '최소 온톨로지(Minimal Ontology)'를 지적 뼈대로 활용하며, 집필 전 '적대적 레드팀(theology-redteam)' 검증을 통해 역사적·학술적 갭을 완벽하게 메운 뒤 집필에 진입**하여 학술성을 극대화합니다.

## 2. Pipeline Phase Gate Architecture
각 단계는 이전 단계의 산출물 및 명시적인 사용자 승인(HITL)을 거쳐 단계적으로 진행됩니다.

```
[START: 자연어 아이디어]
   │
   ▼
 Phase 1: 아이데이션 (Ideation) ───────── 대상 주제에 대한 핵심 질문 및 문제제기 수립
   │
   ▼
 Phase 2: 검색 및 리서치 (Research) ──── KCI/RISS 및 Scholar 등을 통한 문헌 탐색 (🔲 HITL 승인)
   │
   ▼
 Phase 3: 소스 인제스트 (Source Ingest) ─ PDF/원자료를 Markdown/Text와 page map으로 전처리 (선택)
   │
   ▼
 Phase 4: 최소 온톨로지 및 개요 설계 ─ 온톨로지(개념-관계-아포리아) 및 집필 TOC/개요 수립 (🔲 HITL 승인)
   │
   ▼
 Phase 5: 적대적 레드팀 검증 (Red-Team) ─ 뼈대의 신학적 갭, 비약, 아전인수 인용 탐지 및 리서치 보완 (🔲 HITL 승인)
   │
   ▼
 Phase 6: SBL 라이팅 & 린팅 ────────────── 최소 온톨로지와 개요를 뼈대 삼아 에세이 집필 및 각주 린팅
   │
   ▼
 Phase 7: Claim Ledger ──────────────── 핵심 주장과 출처·페이지·반대 근거 매핑
   │
   ▼
 Phase 8: 최종 감사 및 로컬 PDF 검수 ─── 용어, 각주, 문자권, Claim Ledger, PDF 조판 검출 (🔲 HITL 승인)
   │
   ▼
[DELIVER: 최종 에세이, 감사 산출물, 필요 시 로컬 PDF]
```

## 3. Core Workflow
1. **아이디어 포착**: 사용자가 대화창에 던진 주제를 바탕으로 `research-mentor` 스킬을 기동하여 기초 방향성과 핵심 문제를 설계합니다.
2. **리서치 및 수집**: 한국어, 영어, 독일어(한·영·독) 3개 언어 쿼리 자동 확장 및 번역을 거쳐 국내외 신학 학술지 DB(KCI, RISS, Scholar, IxTheo 등)를 교차 검색하고 문헌 목록을 사용자와 최종 승인(HITL)합니다.
3. **소스 인제스트**: `pdf-extractor`가 설치된 경우 논문 PDF, 단행본 발췌, 스캔 자료를 Markdown/Text와 page map으로 추출합니다. PDF 추출은 원고 근거 확보를 위한 전처리이며, 로컬 PDF 조판은 Phase 8에서 별도로 수행합니다.
4. **최소 온톨로지 및 집필 설계**: 글을 집필하기 전, `ontology-builder`와 `theology-discourse-mapper` 가이드를 기반으로 글의 뼈대가 될 개념(Concept), 관계(Relation), 그리고 타협 불가능한 아포리아(Aporia)를 명제(RDF Triples) 형태로 도출하고, 이를 실제 장/절 구조로 매핑한 **라이팅 TOC(목차) 및 상세 개요(Outline)**를 구성하여 사용자의 승인(HITL)을 획득합니다.
5. **적대적 레드팀 검증**: 집필 전 설계된 뼈대(온톨로지 & 개요)에 대해 `theology-redteam` 스킬을 작동시켜 **역사적·교리적 간극(Gap), 학술적 비약(Leap), 아전인수적 사료 대조(Vibe-interpretation)**를 공격하고, 갭 메꿈 지침(Gap-Filling Directives)에 따라 추가 표적 리서치 및 개요 보완을 수행하여 사용자의 최종 승인(HITL)을 얻습니다.
6. **SBL 라이팅**: 승인된 온톨로지와 개요 구조를 따라 흐트러짐 없이 논지를 전개하며 SBL 2nd 규격에 맞춰 에세이를 집필하고, `theology-citation-linker`를 구동해 각주와 레퍼런스를 정교하게 매핑 및 복원합니다.
7. **Claim Ledger**: 로컬에 별도 `claim-ledger` 스킬이 없어도 배포판 스크립트 `~/Desktop/MS_Dev.nosync/projects/tawp/skills/claim-ledger/scripts/claim_ledger.py`를 호출하여 본문 핵심 주장마다 `claim_id`, 출처, 페이지, support type, counterevidence, confidence를 매핑하고 unsupported claim을 제출 전 hard gate로 차단합니다.
8. **최종 감사 및 로컬 PDF 검수**: `theology-terminology-linter`, `tawp_quality_gate.py`, `theology-citation-linker --audit-footnotes`, Claim Ledger audit, `theology-pdf` 감사를 순차 실행하여 용어 혼용, 각주 구조, 비허용 문자권 혼입, Claim Ledger 정합성, PDF 타이포그래피 위험, 환각(Bluffing)을 잡아냅니다.

### 3.1 Claim Ledger Quality Gate

로컬 `.skills` 안에 `claim-ledger` 스킬을 중복 설치하지 않습니다. 대신 공유용 프로젝트의 Claim Ledger CLI를 Phase 7에서 직접 호출합니다.

```bash
python3 ~/Desktop/MS_Dev.nosync/projects/tawp/skills/claim-ledger/scripts/claim_ledger.py build \
  --file path/to/manuscript.md \
  --output path/to/ClaimLedger.json

python3 ~/Desktop/MS_Dev.nosync/projects/tawp/skills/claim-ledger/scripts/claim_ledger.py audit \
  --file path/to/manuscript.md \
  --ledger path/to/ClaimLedger.json \
  --evidence path/to/EvidencePack.json \
  --report path/to/ClaimLedger_Audit.md \
  --fail-on-unsupported \
  --fail-on-missing-counterevidence
```

## 3.2 Pre-PDF Quality Gate

PDF 컴파일 전에는 반드시 TAWP 품질 게이트를 실행합니다. 이 게이트는 의미 검토가 아니라 조판 전 원고 위생 검사입니다.

```bash
python3 ~/Desktop/MS_Dev.nosync/.skills/tawp/scripts/tawp_quality_gate.py \
  --file path/to/manuscript.md \
  --halt-on-fail
```

필수 차단 항목:
- Thai/Cyrillic 등 비허용 문자권 문자가 한국어·히브리어·그리스어·라틴 문자 원고 안에 섞인 경우. 예: `στεναγμός` 안에 태국 문자 또는 키릴 문자가 혼입된 케이스.
- 라틴 문자 음역어가 백틱 코드로 감싸진 경우. 예: `` `peirasmos` ``는 PDF에서 모노스페이스로 렌더링되므로 `peirasmos` 또는 `*peirasmos*`로 교정해야 합니다.

## 4. Reference Links
- [core-instructions.md](./references/core-instructions.md): TAWP 단계별 에이전트 상세 실행 매뉴얼 및 개별 스킬 연동 지침
- [ontology-driven-writing.md](./references/ontology-driven-writing.md): 문서의 학술적 완성도를 높이기 위한 "최소 온톨로지 기반 신학 집필론" 가이드
