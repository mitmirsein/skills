# Theology Searcher: Strategy & Expansion

로컬 JSONL 아카이브 검색의 정확도를 높이기 위한 데이터 확장 및 티어링 전략입니다.

## 📈 Search Expansion
사용자가 입력한 한국어 쿼리를 다국어로 확장하여 검색 범위를 넓힙니다.
1. **Korean**: 기존 검색어
2. **English**: 학술적 표준 번역어
3. **German**: 신학 원전(예: Barth, Jungel)에 사용된 핵심 전문 용어

## 🏗️ Data Tiering
검색 결과의 권위를 위해 데이터를 계층화합니다.
- **Tier 1 (Primary)**: 원전 텍스트 (예: Karl Barth's Church Dogmatics 등).
- **Tier 2 (Secondary)**: 주석서, 한국어 논문, 학술적 해설서.

## 🧠 Scratchpad Implementation
검색 실행 전, 어떤 경로가 가장 최적일지 `thought` 블록에서 먼저 설계합니다. 예: "바르트의 칭의론은 CD IV/1을 먼저 스캔한 뒤, 국내 논문에서 그 수용사를 추적한다."
