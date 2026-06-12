# 📺 YouTube Digest: Gotchas & Anti-Patterns

유튜브 요약 및 자막 추출 수행 시 에이전트가 주의해야 할 사항입니다.

## 1. Extraction Pitfalls (추출의 함정)
- **Auto-gen Noise**: 유튜브 자동 생성 자막(Auto-generated)은 오타와 문맥 오류가 매우 많습니다. 이를 그대로 요약하지 말고, 반드시 '지능형 정제(Cleanup)' 과정을 거치십시오.
- **Wait Time Neglect**: 긴 영상의 자막을 추출하거나 요약할 때 타임아웃이 발생할 수 있습니다. 진행 상황을 사용자에게 알리십시오.

## 2. Content Failures (내용 실패)
- **Clickbait Bias**: 영상의 제목이나 썸네일의 자극적인 내용에 휘둘리지 마십시오. 오직 실제 '자막(Transcript)'의 텍스트 데이터에 기반하여 요약하십시오.
- **Missing Nuance**: 화자의 어조나 농담, 반어법을 놓쳐서 실제 의도와 반대되는 요약을 내놓지 않도록 주의하십시오.

## 3. Storage Errors (저장 오류)
- **Inbox Pollution**: 요약 결과물이 너무 짧거나 무성의하여 인박스(`010 Inbox`)에 실질적인 가치가 없는 파일을 쌓지 마십시오.
- **Link Missing**: 요약 문서 상단에 반드시 원본 유튜브 URL을 기록하여 출처를 확인할 수 있게 하십시오.

---
*Created by MS_Dev Third Gen Standard*
