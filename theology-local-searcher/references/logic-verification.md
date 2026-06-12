# Theology Searcher: Logic & Safety (RDLO)

검색 결과의 논리적 완결성을 보장하기 위한 안전장치 및 검증 로직입니다.

## 🛡️ Safety Guards
- **데이터 부재 (Data Absence)**: 검색 결과가 전혀 없는 경우, 억지로 지어내지 말고 "데이터 부재"를 명시하고 범위를 넓히도록 제안합니다.
- **데이터 충돌 (Data Conflict)**: 검색된 청크들이 서로 상충할 경우, `thought` 블록에서 논리적 대립 지점을 분석하여 사용자에게 보고합니다.

## ✅ Output Verification
- **Semantic Filtering**: 질문과 무관한 청크는 LLM의 판단으로 제거합니다.
- **Citation Protocol**: 인용 시 반드시 `{abbr}, {volume}, {page}` 형식을 준수합니다.
- **Result Capping**: 검색 결과가 50개 이상이면 사용자에게 키워드 추가를 요청합니다.

## 🛠️ Execution
기본적으로 MCP 도구(`msn_th_db:search`)를 사용하되, 실패 시 직접 프로젝트 서버 스크립트를 호출합니다.
