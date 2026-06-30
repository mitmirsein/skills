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

`extract_pdf.py`는 opendataloader 부재/실패 시 **자동으로 poppler 폴백**한다(별도 조치 불필요). `preflight.py`가 한글 글자단위 분리를 감지하면 `route_code: CORE` + `extractor_hint: poppler`를 반환하므로, 그때는 poppler 경로로 추출하면 된다.

---
*Created by MS_Dev (2026-04-17)*
