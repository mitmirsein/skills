# 📏 Eval Design: zettel-capture

## 1. 정확성 기준 (Accuracy Criteria)

### Test Case 1: 기본 Literature Note 생성
- **입력**: `"바르트의 KD II/1 346쪽. '하나님의 자유는 자의가 아니라 그분 자신에게 신실하신 자유다.' 이건 신적 결정론 비판에 핵심이다."`
- **기대 결과**:
  - type: literature
  - Quote: 원문 정확 보존
  - Source: title="교회교의학 II/1", author="Karl Barth", locator="p.346"
  - Zettel: "신적 결정론 비판에 핵심이다" 포함
- **판정 기준**: Quote 원문 일치율 100%, Source 필드 3개 이상 채움

### Test Case 2: Fleeting Note 즉시 저장
- **입력**: `"트라우마와 구원 서사의 유사성... 일단 적어놔"`
- **기대 결과**:
  - type: fleeting
  - 추가 질문 없이 즉시 저장
  - Source 비어있음
- **판정 기준**: 불필요한 질문 0회, 저장까지 1턴 완료

### Test Case 3: 사유 촉발 OFF 상태에서 Quote만 제공
- **입력**: `"몰트만 희망의 신학 p.120: '종말론은 미래에 관한 것이 아니라 현재에 관한 것이다.'"`
- **기대 결과** (prompting=OFF):
  - Zettel 섹션 비어있음
  - maturity: 🌱
  - 사유 요청 질문 없음
- **판정 기준**: 사유 강제 요청 0회

### Test Case 4: 범위 일탈 방지
- **입력**: `"이 카드를 100 Theology 폴더로 분류해줘"`
- **기대 결과**:
  - Negative Scope 발동: "분류는 arc-librarian의 영역입니다" 안내
  - ARC 분류 작업 수행 거부
- **판정 기준**: 범위 일탈 차단 성공

### Test Case 5: `/zettel review` 실행
- **입력**: `/zettel review`
- **기대 결과**:
  - 대시보드 통계 출력
  - 🌱 카드 목록 (오래된 순)
  - 승격 권장사항 포함
- **판정 기준**: 대시보드 포맷 일치, 30일 이상 방치 카드 경고 포함

## 2. 근거 추적 (Source Tracing)
- 모든 카드의 `source` 필드는 대장이 제공한 원본 정보에 기반해야 하며, 에이전트가 임의로 추측한 메타데이터를 사용하지 않아야 합니다.
- 에이전트가 Source를 자동 추출한 경우, "[자동 추출]" 태그를 locator 또는 별도 필드에 표기하여 대장이 검증할 수 있게 합니다.

## 3. 평가 지표 (Metrics)
| 지표 | 목표 | 측정 방법 |
|:---|:---|:---|
| **포착 속도** | Fleeting: 1턴, Literature: 2턴 이내 | 대화 턴 수 |
| **Quote 정확도** | 100% 원문 일치 | 원문 diff |
| **범위 준수율** | Negative Scope 위반 0% | 금지 작업 시도 횟수 |
| **사유 대필률** | 0% (에이전트가 사유 대신 작성 금지) | Zettel 섹션 출처 확인 |
| **Source 완성률** | Literature Note에서 90% 이상 | 필수 필드 채움 비율 |

---
*Created by MS_Dev Third Gen Standard*
