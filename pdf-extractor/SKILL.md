---
name: pdf-extractor
description: >
  Extracts PDFs to high-fidelity Markdown using structural engines, an opt-in
  agent-guided Vision transcription contract, and a 5-pass healing pipeline —
  designed for theological papers. Use when the user asks to extract or
  convert a PDF to Markdown; for argument-skeleton briefing on top of
  extraction use paper-xray. 키워드: PDF 추출, 마크다운 변환, 비전 전사
version: 2.3.0
author: MS_Dev
triggers:
  - "PDF 추출"
  - "논문 파싱"
  - "비전 추출"
  - "extract pdf"
capabilities:
  - structural_hybrid_extraction
  - vision_transcription_contract
  - intelligent_parenthesis_healing
  - footnote_separation
  - deletion_audit_report
  - original_language_protection
  - preflight_triage_routing
scripts_path: "./scripts"
status: active
---

# 📄 pdf-extractor: 고정밀 신학 논문 추출 스킬

PDF를 신학 연구에 최적화된 마크다운으로 추출하고 교정하는 전문 스킬입니다.

## 🛠️ 주요 기능

1. **기본 Core**: `opendataloader`가 기본 엔진이며 일반/Hybrid 모드를 지원합니다.
2. **opt-in fast lane**: `pdf-inspector`는 단순 native-text PDF에만 사용합니다. 스캔·Mixed·인코딩 이상·다단/복잡 레이아웃은 안전 게이트에서 완료 처리하지 않습니다.
3. **Vision 계약**: `vision_*` 스크립트는 에이전트가 이미지를 읽어 결과를 작성할 경로와 JSON 골격만 제공합니다. 내장 OCR 엔진이 아닙니다.
4. **Healing Pipeline**: 추출 후 괄호 노이즈, 각주 혼입, 깨진 외래어를 좁은 휴리스틱으로 교정합니다.

---

## 🚀 사용법

### 0단계: 사전 분류 (Pre-flight Triage) — 권장 진입점
현재 preflight는 pypdf로 첫 3페이지를 고속 스캔하여 기존 `CORE` / `VISION` 경로를 제안합니다. `pdf-inspector` 자동 라우팅은 아직 활성화하지 않습니다.
```bash
# 사람용 판정 리포트
uv run python scripts/preflight.py <PDF_PATH>

# 에이전트 자동 라우팅용 JSON (stdout=순수 JSON, 진단=stderr)
uv run python scripts/preflight.py <PDF_PATH> --json
```
→ `route_code`가 `CORE`면 1단계로, `VISION`이면 3단계로 분기하십시오.

### 1단계: 텍스트 추출 (Core)

기본 동작은 `opendataloader`입니다.
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH>
uv run python scripts/extract_pdf.py --input <PDF_PATH> --hybrid
```
> ⚠️ `--hybrid`는 별도 서버가 필요합니다. **먼저 다른 터미널에서**
> `uv run opendataloader-pdf-hybrid`를 기동하십시오 (미기동 시 "Hybrid server" 에러).
> 텍스트 PDF는 `--hybrid` 없이 일반 모드로 충분합니다. (gotchas.md 참조)

단순 native-text PDF를 명시적으로 fast lane에 넣을 때만 다음을 사용합니다.
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --engine pdf-inspector
```
안전 게이트가 `pdf_type`, OCR 필요 페이지, 인코딩, 다단/복잡 레이아웃을 검사합니다. 실패 시 Poppler로 조용히 바꾸지 않고 실패 메시지를 반환합니다. Poppler를 직접 선택하려면 다음을 사용합니다.
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --engine poppler
```
`--hybrid`는 `opendataloader`에서만 유효합니다.

연구 인용용 페이지 마커가 필요하면 다음처럼 생성합니다.
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --page-markers
uv run python scripts/extract_pdf.py --input <PDF_PATH> --engine pdf-inspector --page-markers
```
OpenDataLoader는 JSON의 1-based `page number`를 사용하고, `pdf-inspector`는 0-based `page.page`에 `--start-page`를 더합니다. 출력은 `<파일명>_paged.md`이며, 후속 `post_cleaner.py`는 페이지 마커와 표·목록·코드 블록을 구조 라인으로 보존합니다.

### 2단계: 구조 정제 및 지능형 교정 (Healing)
```bash
# 기본 정제 (Spalte, Literatur 처리)
uv run python scripts/post_cleaner.py output/논문.md

# 지능형 교정 (문자 단위 괄호 매칭, 각주 분리, 외래어 파편 제거)
uv run python scripts/healer.py output/논문_cleaned.md

# 감사 모드: healer 내부의 삭제·재분류 span을 _healed.report.md로 기록
uv run python scripts/healer.py output/논문_cleaned.md --report
```

> ⚠️ healer는 비가역 삭제를 수행합니다. 신학 원전(원어·인용·각주)이 섞인 문서는
> **`--report`로 감사 로그를 생성하여 손실분을 반드시 확인**하십시오.

### 3단계: 비전 기반 대안 추출 (Elite)
텍스트 추출 품질이 낮을 때(독일어 깨짐, 괄호 붕괴 등) 이미지 디렉토리를 대상으로 실행합니다.
두 스크립트는 OCR을 직접 하지 않고 **에이전트 작성 계약(입력/출력 경로)을 명시**합니다.
```bash
# 마크다운 산출 경로·계약 출력 → 에이전트가 _vision_raw.md 작성
uv run python scripts/vision_extractor.py output/논문_images/

# 시맨틱 JSON 골격 생성 → 에이전트가 _vision.json 채움
uv run python scripts/vision_to_json.py output/논문_images/
```

---

## 🏥 Healer v2.1 파이프라인 (5-Pass)

| Pass | 대상 | 조치 |
| :---: | :--- | :--- |
| 1 | 페이지 잔해 | 단독 숫자(페이지 번호), 반복 헤더 제거 |
| 2 | 각주 분리 | 본문에 섞인 서지 파편을 `> [각주]` 블록으로 격리 |
| 3 | 외래어 잔해 | 역전(`s i e h t o n o M`) 또는 깨진 라틴 자음 파편 제거 |
| 4 | 괄호 정규화 | **문자 단위 스택 매칭**으로 고아 `(`만 정교하게 삭제 |
| 5 | 정규화 | 다중 공백, 연속 빈 줄, 문단 끝 공백 정리 |

---

## 🔗 엔진 정본 (SSOT)

이 스킬은 추출 엔진 6스크립트(`preflight`·`extract_pdf`·`post_cleaner`·`healer`·`vision_*`)의 **정본(Single Source of Truth)**입니다. `paper-xray` 스킬이 동일 엔진의 검증된 미러를 보유하므로, **엔진 수정은 반드시 이 정본에서** 한 뒤 전파하십시오.

```bash
python3 scripts/sync_engine.py          # 미러(paper-xray)에 전파
python3 scripts/sync_engine.py --check  # drift 검사만 (커밋/CI 전, 불일치 시 exit 1)
```

미러 무결성은 `paper-xray/tests/test_engine_parity.py`가 강제합니다(1바이트라도 어긋나면 FAIL).

## 🔧 의존성
- 정본: 이 스킬의 `requirements.txt` (`opendataloader-pdf`, `pdf-inspector`, `pypdf`). 존재하지 않는 루트 `pyproject.toml`을 전제로 하지 않습니다.
- 설치: `uv pip install -r requirements.txt` (두 Mac에서 각자 architecture에 맞는 wheel을 설치)
- Intel Mac은 PyTorch 충돌 가능 — `gotchas.md §2` 참조.
- `extract_pdf.py`의 `--hybrid`는 API/CLI 기본값이 **False로 일치**(서버 선행 필요).

## 📁 디렉토리 구조
- `scripts/preflight.py`: 사전 분류 라우터 (Core/Vision 판정, `--json`)
- `scripts/extract_pdf.py`: 메인 추출 엔진
- `scripts/post_cleaner.py`: 구조 정제기
- `scripts/healer.py`: 지능형 교정기 (v2.1, `--report` 감사)
- `scripts/vision_extractor.py`: 비전 추출 컨트롤러 (마크다운 계약)
- `scripts/vision_to_json.py`: 비전 시맨틱 JSON 골격 생성기
- `scripts/sync_engine.py`: 엔진 정본 → 미러(paper-xray) 동기화기 (`--check`로 drift 검사)
- `tests/test_healer.py`: healer 회귀·멱등·불변식 테스트 (`python3 -m unittest discover tests`)
- `references/gotchas.md`: 함정·안티패턴 가이드
