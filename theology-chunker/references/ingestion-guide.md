# Theology Chunker: Ingestion & Configuration Guide

PDF 및 텍스트 문서를 `msn_th_db` 아카이브(JSONL)로 변환하기 위한 상세 가이드라인입니다.

## 1. Pre-Ingestion Analysis
청킹 전 에이전트는 다음 사항을 반드시 확인해야 합니다.
- **Metadata Extraction**: 파일명을 분석하여 `known_sources.yaml`과의 매칭 여부를 확인합니다. (예: `RGG_Vol4.pdf` → `abbr: RGG`, `vol: 4`)
- **Page Offset**: PDF 페이지 번호와 실제 인쇄 페이지 번호의 차이를 계산해야 합니다.
- **OCR Quality Check**: 텍스트 추출이 불가능한 이미지만 있는 PDF는 배제합니다.

## 2. Configuration Settings
`temp/pre_chunk_config.json` 생성 시 권장되는 파라미터입니다.
- **Strategy**: 
    - `paragraph`: 신학적 번역 목적 시 권장 (최소 300자, 최대 6000자).
    - `token`: 임베딩 및 범용 검색 목적.
- **Overlap**: 청크 간 컨텍스트 유지를 위해 10% 내외의 중첩 권장.

## 3. Execution Commands
```bash
uv run python projects/msn_th_db/src/chunker.py "/path/to/file.pdf" --config projects/msn_th_db/temp/pre_chunk_config.json
```

## 4. Post-processing Verification
- 인입된 총 청크(Chunk) 수 확인.
- `temp/` 디렉토리에 생성된 JSONL 파일의 유효성 검사.
