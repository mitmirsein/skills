---
name: theology-chunker
description: >
  Ingests theological PDFs and texts into the msn_th_db JSONL archive —
  pre-ingestion metadata matching (known_sources.yaml), page-offset
  calculation, OCR triage, then paragraph- or token-strategy chunking with
  overlap. Use when the user asks to add documents to the local theology
  corpus that theology-local-searcher queries.
  키워드: 청킹, 아카이브 인입, JSONL 변환, 코퍼스 추가
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#chunker"
  - "이 PDF 아카이브에 넣어줘"
  - "코퍼스에 인입해줘"
references_path: ./references
---

# 🧱 Theology Chunker (신학 코퍼스 인입기)

PDF/텍스트 문서를 `msn_th_db` JSONL 아카이브로 변환·인입합니다. 인입된 자료는
`.skills/theology-local-searcher`가 검색합니다.

## Phase 0 — 가드레일 (Pre-Ingestion)

- [gotchas.md](./references/gotchas.md)를 읽습니다.
- [ingestion-guide.md](./references/ingestion-guide.md)의 사전 점검 3종을 수행합니다:
  1. **Metadata**: 파일명 ↔ `known_sources.yaml` 매칭 (예: `RGG_Vol4.pdf` → abbr/vol)
  2. **Page Offset**: PDF 페이지 ↔ 인쇄 페이지 차이 계산
  3. **OCR 품질**: 텍스트 추출 불가(이미지 전용) PDF는 배제 — `pdf-extractor`로 우회

## Phase 1 — 설정 (Configuration)

- `projects/msn_th_db/temp/pre_chunk_config.json` 생성:
  - 전략 `paragraph`(번역·정독용, 300~6000자) 또는 `token`(임베딩·범용 검색용)
  - 청크 간 중첩(Overlap) 10% 내외

## Phase 2 — 실행 (Execution)

```bash
cd ~/Desktop/MS_Dev.nosync
uv run python projects/msn_th_db/src/chunker.py "/path/to/file.pdf" \
  --config projects/msn_th_db/temp/pre_chunk_config.json
```

## 검증·보고

- 인입된 총 청크 수를 확인하고, `temp/`의 JSONL을 표본 검사(필드 완전성·한글 깨짐)합니다.
- 보고: 소스 메타데이터, 청크 수, 전략/오버랩 설정, 표본 청크 1개.
- 실패(OCR 불가 등) 시 배제 사유를 명시합니다.
