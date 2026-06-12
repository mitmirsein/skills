---
name: remotion-studio
description: >
  Generates videos programmatically with Remotion (code-as-video), edge-tts
  narration, and JSON scene configurations — shorts, lecture summaries, and
  algorithmic storyboards. Use when the user asks to turn text/content into
  a rendered video or shorts clip.
  키워드: 영상 제작, 쇼츠 생성, 리모션, 코드 비디오
version: 3.1.1
codename: PRO - Official Rules Integrated
author: MS_Dev / Remotion Team (Rules)
triggers:
  - "#영상제작"
  - "#remotion"
  - "#studio"
  - "이 내용을 쇼츠 영상으로 만들어줘"
  - "강의 요약 비디오 제작해"
  - "generate video from text"
capabilities:
  - algorithmic_storyboard_generation
  - programmatic_video_rendering_automation
  - multi_voice_edge_tts_integration
  - react_based_motion_graphic_templates
  - media_error_mining_gotcha_avoidance
  - official_remotion_best_practices_compliance
references_path: "./references"
status: active
---

# 🏗️ Remotion Studio 3.1 (PRO)

## 1. Overview
텍스트를 바탕으로 React 기반 Remotion 템플릿과 음성을 결합하여 고품질 비디오를 자동 생성하는 비디오 공장 스킬입니다. 공식 Remotion 팀의 개발 규칙(Official Rules)이 통합되어 더욱 정교한 코드 생성이 가능합니다.

## 2. Dynamic Workflow
본 제작 전 **제작 함정(Gotchas)**과 **공식 개발 규칙(Official Rules)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 타겟 해상도(숏폼/롱폼) 및 음성 엔진 설정을 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 공통 함정을 피합니다.
- **Official Rules Compliance**: 작업 내용에 따라 [official-rules](./references/official-rules/) 폴더 내 관련 규칙(예: `animations.md`, `audio.md`)을 읽고 코드를 검증합니다.

### Phase 1: Storyboarding (The Director)
입력 콘텐츠를 분석하여 `video-config.json`을 생성합니다. 전략은 [video-storyboarding.md](./references/video-storyboarding.md)를 참조하십시오.

### Phase 2: Asset Production (Asset)
음성(edge-tts)과 자막 데이터를 생성합니다. 명령지는 [rendering-production.md](./references/rendering-production.md)를 참조하십시오.

### Phase 3: Rendering & Export (Output)
최종 비디오를 렌더링하고 `public/video.mp4`로 납품합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 정보 과잉 방지 및 자막 가독성 보장 가이드.
- [Official Rules Directory](./references/official-rules/): Remotion 공식 개발 가이드 (3D, Audio, Fonts, Lottie 등 세부 규칙 포함).
- [video-storyboarding.md](./references/video-storyboarding.md): 스토리보드 구조 및 페이싱 전략.
- [rendering-production.md](./references/rendering-production.md): Voiceover 생성 CLI 및 Remotion 파이프라인.

---
*Upgraded to MS_Dev v3.1 with Official Remotion Rules Synthesis*
