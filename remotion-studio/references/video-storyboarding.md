# Remotion Studio: Video Storyboarding & Layouts

입력 텍스트를 최상의 시각적 연출(Pacing, Layout)로 변환하기 위한 스토리보드 알고리즘입니다.

## 🎞️ Storyboarding Logic (The Director Phase)

1. **Content Ingestion**: 마크다운, 요점 요약 텍스트, 혹은 유튜브 스크립트를 입력으로 받습니다.
2. **Analysis (video-config.json)**: `storyboard_prompt.md`의 지침에 따라 씬(Scene) 정보가 담긴 JSON 설정을 생성합니다.
   - **Audience Profiling**: 대상 독자(학생, 신학자 등)를 설정하여 무드와 속도를 결정합니다.
   - **Pacing & Transitions**: 음악과 음성 길이에 맞춰 씬 전환 시점을 계산합니다.

## 🖼️ Standard Templates (Scene Elements)
- **Hero**: 대제목과 소제목의 강력한 시각적 효과.
- **List**: 애니메이션 블렛 포인트를 사용한 핵심 요약.
- **Stat**: 숫자 중심의 통계 성과 가시화.
- **Chat**: 대화형 말풍선 연출.
- **Code**: 코드 윈도우 지원 (확장 예정).

## 🛠️ video-config.json Structure
```json
{
  "scenes": [
    {
      "template": "Hero",
      "props": { "title": "...", "subtitle": "..." },
      "duration_ms": 5000
    }
  ],
  "audio_config": { "voice": "ko-KR-SunHiNeural", "bgm": "ambient" }
}
```
- **Validation**: 렌더링 시작 전 사용자에게 설정을 선보고하고 승인받습니다.
