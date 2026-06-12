# Gemini & Veo Prompt Strategies

> 기준 모델: **Gemini 3 계열**, 영상은 **Veo 3 계열**.
> 마이너 버전별 차이는 공식 문서로 확인한다.

## System Instructions
- **Constraint-First**: 제약 사항을 가장 먼저 언급하여 무시되지 않도록 함.
- **Few-shot Examples**: 복잡한 논리 구조는 예시를 통해 학습시킴.
- 다국어·멀티모달(이미지/비디오) 통합 지시 활용.

## Video & Image (Veo)
- JSON 구조화된 동영상 지시문 활용.
- (Emotion Descriptor) + "Dialogue" 패턴 사용.
