# 🎬 Media Factory: Gotchas & Anti-Patterns

이미지 생성 및 영상 제작 시 에이전트가 주의해야 할 사항입니다.

## 1. Visual Pitfalls (비주얼의 함정)
- **키치(Kitsch)한 디자인**: 너무 원색적이거나 저렴해 보이는 디자인을 지양하십시오. 우리 브랜드의 핵심은 'Premium'과 'Holy Aesthetic'입니다.
- **비율(Aspect Ratio) 불일치**: 유튜브용 영상 제작 시 16:9 비율이 아닌 이미지를 사용하여 검은 여백(Letterbox)이 생기지 않도록 주의하십시오.

## 2. Audio/Video Sync Failures (싱크 실패)
- **오디오 잘림**: FFmpeg 명령 실행 시 영상 길이가 오디오보다 짧아서 뒷부분이 잘리지 않도록 `-shortest` 옵션이나 지속시간 계산에 주의하십시오.
- **자막 폰트 가독성**: 배경 이미지와 자막 색상이 겹쳐 글자가 보이지 않는 상황을 방지하십시오. 그림자(Shadow)나 아웃라인을 활용하십시오.

## 3. Resource Errors (자원 오류)
- **임시 파일 적체**: 렌더링 과정에서 생성된 수많은 중간 `.png`나 `.wav` 파일들을 작업 완료 후 삭제하지 않으면 디스크 용량이 낭비됩니다.
- **경로 공백**: 파일명이나 경로에 공백이 포함되어 FFmpeg 명령이 깨지는 것을 방지하기 위해 항상 따옴표(`" "`)로 감싸십시오.

---
*Created by MS_Dev Third Gen Standard*
