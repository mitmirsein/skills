---
name: paper-xray
description: >
  Extracts a PDF to high-fidelity Markdown, heals parsing noise, and
  reverse-engineers the core argument skeleton into an X-Ray briefing
  (thesis, logical topology, combat map) within 5 minutes — designed for
  theological and humanities papers. Use when the user asks to extract,
  parse, or x-ray a paper PDF. 키워드: 논문 투시, PDF 추출, 논문 뼈대, 엑스레이
version: 2.3.0
author: MS_Dev
triggers:
  - "PDF 추출"
  - "논문 파싱"
  - "비전 추출"
  - "extract pdf"
  - "논문 투시"
  - "X-Ray 브리핑"
  - "이 논문 핵심만"
  - "paper xray"
  - "논문 뼈대"
capabilities:
  - structural_hybrid_extraction
  - citation_safe_page_markers
  - elite_vision_ocr
  - intelligent_parenthesis_healing
  - footnote_separation
  - deletion_audit_report
  - original_language_protection
  - preflight_triage_routing
  - argument_skeleton_reverse_engineering
  - battleground_target_identification
  - one_sentence_thesis_distillation
  - scan_honesty_uncertainty_flagging
  - mechanical_qa_gate
  - release_hygiene_guard
  - untrusted_source_boundary
  - engine_single_source_mirror
scripts_path: "./scripts"
status: active
---

# 🩻 paper-xray: 고정밀 논문 추출 및 투시 분석 파이프라인 (Unified)

학술 PDF나 스캔본 문서로부터 텍스트를 고정밀로 추출하고, 불필요한 파싱 노이즈를 교정한 후, 논문의 뼈대(Skeleton)와 핵심 논지를 신속하게 추출하는 통합 분석 스킬입니다.

> ⚖️ **최상위 독해 헌법 준수 의무 (SSOT):**
> 에이전트는 본 스킬을 가동할 때 반드시 동일 폴더 루트의 **[GEMINI.md](./GEMINI.md)** (또는 **[CLAUDE.md](./CLAUDE.md)**, **[AGENTS.md](./AGENTS.md)**)에 명시된 최상위 헌법 규정과 '매의 눈 독해 휴리스틱'을 1순위 의사결정 및 가공 준거로 삼아야 합니다. (실제 알맹이 파일: [constitution.md](./constitution.md))

> 💾 **출력 형식 및 자동 저장 규약:**
> 최종 아웃풋의 시각적 양식과 작성 모범례는 **[templates.md](./references/templates.md)** 규격을 따르며, 최종 X-Ray 브리핑 결과물은 반드시 `output/{논문명}/{논문명}_xray.md` 파일로 디렉토리에 생성하여 디스크에 저장해야 합니다.

---

## 🛠️ 핵심 기능 (Capabilities)

1. **사전 진단 (Pre-flight Triage)**: PDF 텍스트 레이어의 상태와 노이즈 레벨을 사전에 진단하여 Core 또는 Elite Vision 경로를 결정합니다.
2. **하이브리드 추출 (Core - Structural)**: 텍스트 및 레이아웃 좌표 정보를 초고속으로 파싱합니다.
3. **시각 지능 추출 (Elite - Vision)**: 에이전트의 시각 정보 처리 성능을 극대화하여 스캔 이미지로부터 원전 언어와 각주 구조를 온전히 복원합니다.
4. **지능형 교정 (Healing Pipeline)**: 문자 단위 괄호 스택 매칭, 고아 각주 분리 블록화, 깨진 모음/자음 파편 정리를 통해 텍스트 완성도를 끌어올립니다.
5. **학술 삭제 감사 (Audit Report)**: 비가역적으로 제거되거나 재분류된 span을 보고서로 출력하여 학술 정보 손실을 사전에 예방합니다.
6. **논증 역설계 (X-Ray 브리핑)**: 논문의 서론·결론·소제목 위상을 토대로 1문장 요약(1-Sentence Thesis), 논증 구조, 학술적 대립 전선(Combat Map), 분석자 인사이트를 도출합니다.
7. **기계 검수 게이트 (Mechanical QA)**: 산출된 브리핑을 파싱해 유령 페이지 인용·미완성 흔적·섹션 누락을 `FAIL`로 차단하고, 정본 미확인 서지(제1조)·영혼 없는 찬사(제5조)를 `WARN`으로 띄워 독해 헌법을 기계로 강제합니다.
8. **공개 위생 게이트 (Release Guard)**: 외부 공유 전 공개 가능 산출물(`_xray.md`)만 화이트리스트로 분류하고, 원전 verbatim 누출을 `BLOCK`으로 차단합니다(제6조).

---

## 🚀 입력 포맷별 파이프라인 분기 (Routing)

에이전트는 입력받은 논문 파일의 확장자에 따라 다음과 같이 처리 경로를 분기합니다.

| 입력 포맷 | 단계별 처리 경로 | 설명 |
| :--- | :--- | :--- |
| **PDF** | `[1단계 Triage]` ➡️ `[2단계 Extraction]` ➡️ `[3단계 Healing]` ➡️ `[4단계 X-Ray]` ➡️ `[5단계 QA]` | 표준 프로세스 전체. 브리핑 저장 후 QA 게이트 필수. 외부 공유 시 `[6단계 공개점검]` 추가. |
| **DOCX** | `[Pandoc/CLI 변환]` ➡️ `[4단계 X-Ray]` | `.md` 확보 후 곧바로 4단계로 진입하며, **최종 브리핑 결과물을 `{논문명}_xray.md`로 물리 저장**합니다. |
| **MD / TXT** | `[4단계 X-Ray]` (즉시 분석 ➡️ 파일 저장) | 1~3단계를 생략하고 즉시 4단계 분석을 가동하며, **최종 브리핑 결과물을 `{논문명}_xray.md`로 물리 저장**합니다. |

---

## 🚀 파이프라인 표준 프로세스 (4-Steps)

에이전트는 각 포맷별 분기 경로에 맞춰 아래 지침을 실행합니다.

### 0단계: 진입 전 준비
- 워크스페이스 내에서는 `uv run`이 의존성을 자동 처리합니다. 워크스페이스 외부의 경우, `pip install -r requirements.txt`로 의존성을 먼저 설정하십시오.
- **엔진 정본 주의 (SSOT):** 추출 엔진 6스크립트(`preflight`·`extract_pdf`·`post_cleaner`·`healer`·`vision_*`)의 정본은 형제 스킬 **`pdf-extractor`**입니다. paper-xray는 검증된 미러를 보유합니다. 엔진을 고칠 일이 있으면 **반드시 정본에서 수정한 뒤** `pdf-extractor/scripts/sync_engine.py`로 전파하십시오. 미러 무결성은 `tests/test_engine_parity.py`가 강제합니다(불일치 시 FAIL).

### [1단계] 사전 진단 (Pre-flight Triage)
추출 전 PDF 파일의 첫 3페이지를 초고속 진단하여 최적의 파싱 경로를 결정합니다.
```bash
# 에이전트 자동 라우팅용 JSON (stdout=순수 JSON)
uv run python scripts/preflight.py <PDF_PATH> --json
```
- `route_code` 결과가 `CORE`일 경우 **[2단계 Core 경로]**로, `VISION`일 경우 **[2단계 Vision 경로]**로 진행하십시오.

### [2단계] 추출 경로 실행 (Core vs Vision)

#### ■ 경로 A: Core 일반/하이브리드 추출
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --page-markers
```
- *참고: 복잡한 레이아웃이나 표가 많은 스캔본의 경우, 터미널 A에서 `uv run opendataloader-pdf-hybrid` 서버를 선행 구동한 후 `--hybrid` 플래그를 추가해 실행하십시오.*
- `--page-markers`는 opendataloader JSON의 `page number`를 사용해 `===== p.N =====` 마커가 박힌 `<논문명>_paged.md`를 생성합니다. 연구 인용, TKG `Evidence.canonical_ref`, X-Ray page-grounded claim에는 이 파일을 표준 입력으로 삼으십시오.

#### ■ 경로 B: Elite Vision 시각 지능 추출
텍스트 추출 품질이 극히 낮거나 희랍어/히브리어/독일어 원전 등 텍스트가 심하게 깨질 때 작동합니다.
```bash
# 에이전트 마크다운 계약서 생성 → 에이전트가 직접 _vision_raw.md 작성
uv run python scripts/vision_extractor.py output/<논문명>/
```
- 에이전트는 출력된 계약 경로에 맞춰 이미지 파일들을 보며 마크다운 본문을 직접 구축합니다.

### [3단계] 지능형 구조 교정 (Healing Pipeline)
추출 도중 발생한 노이즈와 서지 혼입 파편들을 5단계 파이프라인으로 정제합니다.
```bash
# 1. Spalte(단 번호), Literatur(참고문헌) 1차 정제
uv run python scripts/post_cleaner.py output/<논문명>/<논문명>_paged.md

# 2. 지능형 교정 및 학술 삭제 감사 보고서 자동 생성
uv run python scripts/healer.py output/<논문명>/<논문명>_paged_cleaned.md --report
```
- `_healed.report.md` 감사 리포트를 반드시 검토하여 고유 명사나 핵심 각주가 오폭 삭제되지 않았는지 에이전트 스스로와 사용자가 교차 검증합니다.
- 최종 X-Ray 및 TKG 전달용 정본은 `output/<논문명>/<논문명>_paged_healed.md`입니다. 이 파일은 `===== p.N =====` 페이지 마커를 보존해야 합니다.

### [4단계] X-Ray 분석 및 브리핑 (최종 아웃풋)
정제 완료된 `{논문}_paged_healed.md` 문서를 바탕으로, 전체를 정독하지 않고도 논문의 핵심 뼈대를 볼 수 있는 **X-Ray 브리핑**을 최종 출력하고 파일로 저장합니다. 핵심 주장과 전선도 항목에는 가능한 한 보존된 페이지 마커를 근거로 붙입니다.
* **중요 (강조 규칙)**: 최종 브리핑 마크다운 문서 작성 시 **이탤릭체(`*텍스트*` 및 `_텍스트_`) 사용은 전면 금지**됩니다. 강조가 필요하다면 오직 볼드(`**텍스트**`)만 사용해 작성해야 합니다.

### [5단계] 기계 검수 게이트 (Mechanical QA) — 필수
브리핑을 `{논문명}_xray.md`로 저장한 뒤, constitution의 독해 헌법을 기계적으로 강제하는 QA 게이트를 통과시킵니다.
```bash
uv run python scripts/xray_qa.py output/<논문명>/<논문명>_xray.md --source output/<논문명>/<논문명>_paged_healed.md
```
- **유령 페이지**(정본 마커 밖 인용)·**미완성 흔적**(TODO·빈 섹션·템플릿 잔재)·**섹션 누락**은 `FAIL`(exit 1)로 차단됩니다. 수정 후 재실행하십시오.
- **정본 미확인 연도**(제1조 위반 의심)·**영혼 없는 찬사**(제5조)는 `WARN`으로 표기되며 검토가 필요합니다.
- `--source`로 정본을 함께 주면 페이지 마커 교차검증이 활성화됩니다(강력 권장). 정본 없이 돌리면 페이지 검증은 `WARN`으로 건너뜁니다.

### [6단계] 공개 전 위생 점검 (Release Guard) — 외부 공유 시
저작권 있는 원전의 추출 전문이 작업 폴더에 평문으로 남으므로, 외부 공유·발행 전 반드시 점검합니다.
```bash
uv run python scripts/release_guard.py output/<논문명>/
```
- 공개 가능 화이트리스트는 `_xray.md`(분석 산출물)와 자작 도식(`assets/`)뿐입니다. 원전 파생물(`_paged*.md`·`.json`·렌더 이미지)은 **공개 금지**입니다.
- `_xray.md`에 원전 장문이 verbatim으로 복제되면 `BLOCK`(exit 2)됩니다 (제6조 4항).
