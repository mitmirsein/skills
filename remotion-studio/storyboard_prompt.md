# 🎬 Remotion Studio: Director's Storyboard Prompt

> 이 프롬프트는 텍스트를 단순 요약하는 것을 넘어, **'시청각적 연출(Directing)'**을 가미한 최적의 `video-config.json`을 자동 생성하기 위한 지침입니다.

## 1. 🔍 Phase 1: 입체적 분석 (Multi-dimensional Analysis)
원문 텍스트가 주어지면, 즉시 대본을 쓰지 말고 다음 3가지 렌즈로 텍스트를 해체하고 내부적으로 요약하십시오.
1. **Audience & Tone (청중과 톤)**: 이 영상의 타겟은 누구이며, 어떤 감정(위로, 도전, 정보)을 전달해야 하는가?
2. **Hook & Climax (서사 구조)**: 시청자를 사로잡을 단 하나의 질문(Hook)은 무엇이며, 결론에서 던질 가장 강력한 메시지(Climax)는 무엇인가?
3. **Visual Ingredients (시각적 재료)**: 텍스트 내에서 '리스트형 요약', '수치/통계', '가상 대화/대조'로 표현할 수 있는 요소를 남김없이 발굴하라.

## 2. ✍️ Phase 2: 시청각적 스토리보딩 (Audio-Visual Scripting)
분석된 재료를 바탕으로 JSON 대본을 짭니다. 이때 반드시 다음 **대본 작성의 3원칙**을 따르십시오.
1. **낭독 최적화 (Ear-reading)**: 문어체를 철저히 배제합니다. 문장을 짧게 끊고, 호흡을 조절하며, 단호한 입말(Spoken Word)로 변환합니다. (예: "~이므로 ~해야 한다" ➔ "~입니다. 그러므로 ~해야 합니다.")
2. **청각적 여백 (Pacing)**: 시청자가 숨 쉴 틈을 주십시오. 1개의 씬(`narration`)당 나레이션 길이는 절대 10~15초(한국어 기준 약 30~45자)를 넘지 않도록 제한합니다.
3. **지능형 템플릿 매핑 (Smart Scene Matching)**:
   - **`Hero`**: 도입부의 강력한 선언, 질문, 또는 영상 전체의 결론.
   - **`List`**: 3가지 핵심 요인, 행동 지침, 단계별 설명.
   - **`Stat`**: 충격적인 수치, 대비되는 데이터 포인트, 핵심 개념 키워드 부각.
   - **`Chat`**: A vs B의 대립 구도, 일반적인 오해와 진실, 가상의 질문과 답변.

## 3. 📤 Output Schema (video-config.json)
분석과 대본 작성이 완료되면, 반드시 아래 예시와 동일한 JSON 형식**코드 블록**으로만 결과를 반환하십시오.

```json
{
  "title": "[내부 식별용 짧은 영상 제목]",
  "version": "1.0.0",
  "scenes": [
    {
      "id": "scene_0_hero",
      "template": "Hero",
      "narration": "[10~15초 분량의 입말체 나레이션]",
      "data": {
        "title": "[화면에 크게 보일 압도적 키워드]",
        "subtitle": "[타이틀을 보조하는 서브 텍스트]"
      }
    },
    {
      "id": "scene_1_list",
      "template": "List",
      "narration": "[10~15초 분량의 입말체 나레이션]",
      "data": {
        "title": "[리스트의 주제]",
        "items": ["항목 1 (매우 짧게)", "항목 2", "항목 3"]
      }
    },
    {
      "id": "scene_2_stat",
      "template": "Stat",
      "narration": "[10~15초 분량의 입말체 나레이션]",
      "data": {
        "title": "[상단 제목]",
        "value": "[압도적으로 커질 텍스트/수치 (예: 99%, 필수, 파괴)]",
        "label": "[수치를 설명하는 하단 라벨]"
      }
    },
    {
      "id": "scene_3_chat",
      "template": "Chat",
      "narration": "[10~15초 분량의 입말체 나레이션]",
      "data": {
        "title": "[대화의 주제]",
        "messages": [
          { "author": "[화자1 (예: 세상)]", "text": "[대사]" },
          { "author": "[화자2 (예: 성경)]", "text": "[반박 대사]" }
        ]
      }
    }
  ]
}
```
* **제약사항**: `template` 값은 반드시 `Hero`, `List`, `Stat`, `Chat` 중 하나여야 합니다. `id`는 고유해야 합니다.
