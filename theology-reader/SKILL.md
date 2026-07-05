---
name: theology-reader
description: >
  Fast document loader — bulk-reads PDF/MD/TXT/HTML files in a folder into
  the agent's context via PyMuPDF, with per-document truncation and a
  cache-first preference for pdf-extractor's healed Markdown. Use when the
  user asks to load, scan, or read a folder of theological documents.
  키워드: 문서 로드, 폴더 읽기, PDF 적재
version: 2.1.1
author: MS_Dev
triggers:
  - "신학 문서 로드"
  - "이 폴더 읽어줘"
  - "theology reader"
  - "문서 스캔"
capabilities:
  - fast_pdf_text_extraction
  - multi_format_directory_loading
  - context_limit_truncation
scripts_path: "./scripts"
status: active
---

# 📖 theology-reader: 고속 신학 문서 로더 스킬

신학 연구에 사용되는 다양한 형식의 문서들을 초고속으로 메모리에 적재하여 에이전트가 "볼 수 있도록" 피딩하는 텍스트/PDF 리더 스킬입니다.

## 🛠️ 주요 기능

1. **고속 텍스트 스캔**: `PyMuPDF (fitz)` 라이브러리를 활용해 PDF 문서를 즉시 파싱합니다.
2. **다중 포맷 자동 수확**: 지정된 디렉토리 내의 PDF, Markdown(`.md`), 일반 텍스트(`.txt`), Web HTML(`.html`) 파일을 통합 정렬하여 스캔합니다.
3. **컨텍스트 크기 관리**: 개별 문서 덤프 시 10만 자 한도를 두어 컨텍스트 오버플로우와 토큰 낭비를 자동으로 제어합니다.
4. **캐시 우선 매칭(협력 모델)**: 스캔 대상 폴더/경로에 `pdf-extractor`에 의해 가공 완료된 마크다운 결과물(`.md`, `_healed.md`)이 존재한다면, PDF를 새로 파싱하지 않고 정제 정본을 최우선적으로 읽어 들입니다.

---

## 🚀 사용법

에이전트에게 자연어로 문서 독서를 지시하면 자동으로 이 스킬이 호출됩니다.

### 1단계: 실행 명령 예시
```bash
# 로컬 공동 가상환경(shared_venv)의 python 인터프리터를 사용하여 실행합니다.
uv run python .skills/theology-reader/scripts/reader_tool.py --path <분석할_파일_또는_폴더_경로>
```

### 2단계: 에이전트 연동 (Triggers)
사용자가 아래와 같이 명령하면 에이전트가 이 스킬의 `reader_tool.py`를 가동하여 텍스트 컨텍스트를 수집합니다.
* "이 폴더 안에 있는 신학 논문들 다 로드해줘."
* "#theorizer 작동해줘."
* "신학 문서 리더 가동해서 이 폴더 스캔해."

---

## 🔧 의존성
- 이 스킬은 공동 가상환경 `shared_venv`를 기반으로 작동합니다.
- 패키지 의존성: `pymupdf`, `pydantic`. (이미 `shared_venv`에 구성 완료되어 있습니다.)
