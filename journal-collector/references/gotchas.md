# 📚 Journal Collector: Gotchas & Anti-Patterns

학술지 수집 및 스크래핑 시 에이전트가 주의해야 할 사항입니다.

## 1. Collection Pitfalls (수집의 함정)
- **차단 트리거**: 단시간에 너무 많은 요청을 보내 서버로부터 봇으로 감지되어 IP가 차단되지 않도록 주의하십시오. 지연(Delay)을 적절히 사용하십시오.
- **잘못된 권/호 매핑**: 저널마다 권(Volume)과 호(Issue)를 표기하는 방식이 다릅니다. (예: 115. Jg. vs Vol. 115) 이를 혼동하여 엉뚱한 파일을 받지 마십시오.

## 2. Refining Failures (정제 실패)
- **OCR Garbage**: 수집된 PDF에서 텍스트를 추출할 때 하이더(Header), 푸터(Footer), 페이지 번호 등이 본문에 섞여 들어가지 않도록 정밀하게 클리닝하십시오.
- **비구조화된 요약**: 논문의 핵심 논지(Thesis Statement)를 놓치고 목차만 나열하는 요약은 피하십시오.

## 3. Librarian CLI Errors (도구 오류)
- **파라미터 누락**: `librarian.py` 실행 시 필수 인자(저널 코드, 밴드 번호 등)가 누락되면 작업이 비정상 종료됩니다.
- **저장 경로 이탈**: 수집된 파일이 `010 Inbox`가 아닌 임시 폴더에서 미아가 되지 않도록 경로를 절대적으로 확인하십시오.

---
*Created by MS_Dev Third Gen Standard*
