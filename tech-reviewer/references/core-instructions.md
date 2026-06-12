# 🛡️ Tech Reviewer: Logic & Safety Core Instructions

## 1. Shadow Path Tracing (그림자 경로 추적)
단순 성공 케이스(Happy Path)를 넘어, 코드의 모든 분기점이 야기할 수 있는 부수 효과를 사냥합니다.

- **성공 경로(Success Path)**: 데이터가 예상대로 처리되는가? 의도한 출력이 나오는가?
- **빈 경로(Empty/Null Path)**: DB 조회 결과가 없거나, 리스트가 비어있을 때 코드가 죽지 않는가?
- **오류 경로(Error Path)**: 외부 API 타임아웃, 권한 부족, 올바르지 않은 JSON 데이터 입력 시 우아하게 실패(Graceful Failure)하는가?
- **지연 경로(Latency Path)**: 비동기 처리(`await`) 간에 레이스 컨디션이나 불필요한 직렬화가 없는가?

## 2. Boil the Lake (완결성 원칙)
- **100% Logic Coverage**: 신규/수정된 모든 함수에 대해 유닛 테스트가 존재하는가?
- **Try/Catch Audit**: `catch (e) { }` 같은 에러 마스킹(Masking)을 100% 제거하고, 필수 로깅을 강제하십시오.
- **SQL / API Security**: 모든 외부 입력값에 대해 Sanitizing이 수행되었는지, 파라미터 바인딩을 사용하는지 눈을 떼지 마십시오.

## 3. Zero Hallucination Audit (AI 거버넌스)
코드 생성이나 문서화 과정에서 실존하지 않는 상상의 라이브러리나 API를 사용하는 것을 '절대로' 허용하지 마십시오.
모든 제안은 **증거(Provenance)**가 있어야 합니다.

---
*Staff Engineering Reference for MS_Dev*
