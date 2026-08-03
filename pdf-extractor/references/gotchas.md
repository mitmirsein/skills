# 📄 PDF Extractor: Gotchas & Anti-Patterns

신학 논문 PDF 추출 시 에이전트가 반드시 확인해야 할 주의사항입니다.

---

## 1. Hybrid 모드 서버 미기동 오류

Hybrid(Docling) 모드 사용 시 별도 서버가 필요합니다.

```bash
# 터미널 A: 서버 기동
uv run opendataloader-pdf-hybrid

# 터미널 B: 추출 실행
uv run python scripts/extract_pdf.py --input paper.pdf --hybrid
```

`"Hybrid server"` 관련 에러 발생 시 → 서버가 구동되지 않은 것입니다.

---

## 2. Intel Mac (2017 iMac) 호환성

- **문제**: PyTorch 의존성이 Intel Mac 환경에서 충돌할 수 있음
- **해결**: CPU 전용 버전으로 설치하거나, 일반 모드(`--hybrid` 없이)로 실행

---

## 3. 스캔본 PDF vs 텍스트 PDF 구분

- **텍스트 PDF**: 일반 모드로도 충분. Hybrid 불필요
- **스캔본 PDF**: 반드시 Hybrid 모드 또는 `pdf-phantom-scanner` → ABBYY OCR 선처리 후 입력
- **확인 방법**: Adobe Acrobat이나 Preview에서 텍스트 선택이 되면 텍스트 PDF

---

## 4. Spalte(단 번호) 누락 문제

독일어 신학 사전(TRE, RGG, RGG4)의 단(Spalte) 번호는 종종 추출 시 노이즈로 처리됩니다.
- `post_cleaner.py`의 Spalte 패턴이 자동 복원하지만, 누락된 경우 수동 확인 필요
- 패턴: `Sp. 123` 형태

---

## 5. 출력 파일명 불일치

`opendataloader-pdf`는 버전에 따라 출력 파일명이 다를 수 있습니다.
- 기대: `{입력파일명}.md`
- 실제 확인: `extract_pdf.py`가 자동으로 출력 디렉토리를 스캔하여 대체 경로를 찾습니다.

---

## 6. theology-chunker 연계 시 주의

`_cleaned.md` 파일을 `theology-chunker`로 넘길 때:
- `known_sources.yaml`에 해당 문서가 등록되어 있어야 메타데이터 매칭 가능
- 미등록 문서는 `temp/pre_chunk_config.json`에 수동 메타데이터 입력 필요

---

## 7. 한글 PDF 추출기 선택 (pypdf 자간 분해 함정)

한글 학술 PDF는 추출기에 따라 텍스트 품질이 크게 갈린다.

- **pypdf**: 한글 자간을 공백으로 분해(`오 늘 날`) → 띄어쓰기 소실, 사실상 복구 불가
- **poppler `pdftotext -layout`**: 한글 띄어쓰기를 정상 보존. ★권장
- **opendataloader**: Intel Mac에서 PyTorch 충돌(§2), 미설치도 흔함

기본 `opendataloader` 경로는 미설치·실패 시 **자동으로 poppler 폴백**한다. `preflight.py`가 한글 글자단위 분리를 감지하면 `route_code: CORE` + `extractor_hint: poppler`를 반환하므로, 다음처럼 명시할 수 있다.

```bash
uv run python scripts/extract_pdf.py --input paper.pdf --engine poppler
```

---

## 8. pdf-inspector 0.2.6 fast lane의 범위

`pdf-inspector`는 `--engine pdf-inspector`를 명시했을 때만 실행되는 선택형 경량 엔진입니다. 기본 엔진을 바꾸지 않았습니다.

- 공식 패키지명은 `pdf-inspector`, Python import명은 `pdf_inspector`입니다.
- `process_pdf()`의 `pdf_type`이 `text_based`가 아니거나 `pages_needing_ocr`가 있으면 완료 처리하지 않습니다.
- `has_encoding_issues`, `pages_with_columns`, `pages_with_tables`, `is_complex_layout` 중 하나라도 감지되면 완료 처리하지 않습니다. 다단·각주·주변주가 섞일 수 있으므로 OpenDataLoader Hybrid 또는 Poppler를 검토합니다.
- `process_pdf()`의 진단 페이지 신호는 1-based입니다. `extract_pages_markdown()`의 `page.page`는 0-based이며, 출력 마커는 `start_page + page.page`로 계산합니다.
- `extract_pages_markdown()` 결과의 페이지 수·순서·중복을 검증합니다. 빠진 페이지가 있으면 파일을 성공으로 쓰지 않습니다.

관련 위험: [다단 순서 이슈](https://github.com/firecrawl/pdf-inspector/issues/219), [본문·각주·헤더 혼합 이슈](https://github.com/firecrawl/pdf-inspector/issues/215), [복잡 레이아웃 누락 이슈](https://github.com/firecrawl/pdf-inspector/issues/210), [CIDFont 문자 오인식 이슈](https://github.com/firecrawl/pdf-inspector/issues/208).

---

## 9. Mixed PDF와 OCR 계약

`pdf-inspector`는 OCR 엔진이 아닙니다. Mixed PDF에서 `pages_needing_ocr`를 보고할 수는 있지만, 첫 릴리스는 선택 페이지 OCR 실행이나 native/OCR 결과 병합을 하지 않습니다. 스캔·Mixed 결과를 완전 추출로 표시하지 말고 Vision/OCR 계약 또는 별도 OCR 파이프라인으로 넘깁니다.

`vision_extractor.py`와 `vision_to_json.py`도 실제 OCR을 수행하지 않습니다. 이미지 입력과 에이전트가 채울 Markdown/JSON 출력 계약만 생성합니다.

---

## 10. 엔진별 실패·fallback 정책

- 엔진을 생략하면 `opendataloader`가 기본이며, 그 엔진 내부의 import/실행 실패만 기존 Poppler 폴백 대상입니다.
- `--engine pdf-inspector`를 명시했는데 패키지가 없거나 안전 게이트에 걸리면 조용히 Poppler로 바꾸지 않고 실패합니다.
- `--engine poppler`는 `opendataloader_pdf`를 import하지 않고 바로 `pdftotext -layout`을 실행합니다.
- `--hybrid`는 `opendataloader`에서만 유효합니다.

---

## 11. 의존성·두 Mac 설치

`requirements.txt`가 이 스킬의 의존성 정본입니다. 존재하지 않는 루트 `pyproject.toml`을 전제로 하지 않습니다. `pdf-inspector`는 0.2.6 API를 기준으로 하되 `>=0.2.5,<0.3.0`으로 선언되어 있어, 7-day release-age 가드가 0.2.6을 아직 허용하지 않을 때 0.2.5를 선택할 수 있습니다. Intel x86_64와 Apple Silicon용 wheel은 각 Mac에서 별도로 설치하며 venv/native wheel을 Syncthing으로 공유하지 않습니다.

---
Created by MS_Dev (2026-08-03)
