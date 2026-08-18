---
name: media-factory
description: >
  Creative studio — generates high-quality AI images ("holy aesthetic"
  presets) and converts audio plus images into videos (audiograms) with
  ffmpeg. Use when the user asks to generate an image, make an audiogram,
  or convert audio into a simple video.
  키워드: 이미지 생성, 오디오그램, 영상 변환
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#media"
  - "#video"
  - "#image"
  - "영상 만들어줘"
  - "이미지 생성해줘"
  - "오디오 비디오로 변환해줘"
capabilities:
  - ai_image_generation_holy_aesthetic
  - ffmpeg_audiogram_production
  - multi_mode_video_rendering
  - media_asset_management
  - visual_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# 🎬 Media Factory 3.0

## 1. Overview
묵상이나 연구 리포트를 시청각 자료로 전환하는 크리에이티브 스튜디오입니다. AI 이미지 생성과 FFmpeg 영상 제작 엔진을 관리합니다.

## 2. Dynamic Workflow
본 스킬은 배출 전 **심미적 함정(Gotchas)**과 **제작 환경(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 비디오 해상도, 프레임 레이트 및 프리셋 옵션을 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 키치한 디자인 및 오디오 싱크 오류를 방지합니다.

### Phase 1: Visual Generation (AI)
주제에 부합하는 장엄한(Holy Aesthetic) 이미지를 생성합니다. 비주얼 가이드는 [visual-direction.md](./references/visual-direction.md) 및 사령부 템플릿 [nano_banana_prompt_frame.md](file://~/Desktop/MS_Thoughts.nosync/000%20System/Templates/nano_banana_prompt_frame.md)를 참조하십시오.

### Phase 2: Video Production (FFmpeg)
오디오와 이미지를 결합하여 MP4 영상을 제작합니다. 명령지는 [video-production.md](./references/video-production.md)를 참조하십시오.

### Phase 3: Delivery (Check)
에셋 무결성을 확인하고 지정된 폴더에 납품합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 비주얼 품질 기준 및 자원 적체 방지 가이드.
- [visual-direction.md](./references/visual-direction.md): 프롬프트 공학 및 심미적 기준.
- [video-production.md](./references/video-production.md): `video_factory.py` 엔진 사용법.
- [nano_banana_prompt_frame.md](file://~/Desktop/MS_Thoughts.nosync/000%20System/Templates/nano_banana_prompt_frame.md): **(Global Standard)** 나노 바나나 이미지 프롬프트 프레임워크.

---
*Created by MS_Dev Third Gen Standard*
