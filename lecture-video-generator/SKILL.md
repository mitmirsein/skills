---
name: lecture-video-generator
description: >
  Orchestrates the existing lecture_video_generator project pipeline to turn
  a theology lecture Markdown/DOCX into outline, slides, TTS, and final
  video — fixing the generate → tts → assemble order per the project's
  GEMINI.md and pipeline.py and auditing output contracts. Use when the
  user asks to produce a lecture video from a script.
  키워드: 강의 영상 생성, 강의안 영상화, TTS 영상
version: 1.0.1
status: active
---

# Lecture Video Generator

## 역할

이 스킬은 자유형 영상 생성기가 아니라, `projects/lecture_video_generator`의 기존 파이프라인을 안전하게 호출하고 검수하는 운영 스킬이다.

## 먼저 읽을 것

1. `projects/lecture_video_generator/GEMINI.md`
2. `projects/lecture_video_generator/README.md`
3. 필요 시 [workflow.md](./references/workflow.md)
4. 실패나 품질 이슈가 있으면 [gotchas.md](./references/gotchas.md)

## 기본 워크플로

1. 입력 파일이 `.md` 또는 `.docx`인지 확인한다.
2. 테마가 불명확하면 자동화 상황에서는 명시적으로 `--design`을 준다.
3. `generate`를 실행하고 산출물 계약을 확인한다.
4. `tts`를 실행하고 `audio_*.wav` 산출물을 확인한다.
5. `assemble`를 실행하고 `final.mp4` 생성 여부를 확인한다.
6. 실패 시 전체 재실행보다 깨진 단계만 다시 수행한다.

## 절대 규칙

- 이미지 생성 시 배경 이미지만 허용한다.
- 이미지 안의 텍스트, 숫자, 로고, 표지형 레이아웃은 실패다.
- `assemble` 단계의 입력 계약은 `slide_*.png`와 `audio_*.wav`다.
- 새 런타임을 임의로 도입하지 말고, 기존 `pipeline.py`와 `modules/`를 우선 사용한다.

## 출력 계약

- `outline.json`
- `slide_*.svg`
- `slide_*.png`
- `tts_*.txt`
- `audio_*.wav`
- `final.mp4`

## 검수 포인트

- 섹션 수와 산출물 수가 일치하는지
- 시네마틱 배경 이미지가 텍스트를 포함하지 않는지
- `all` 경로가 실제 출력 디렉터리를 기준으로 조립되는지
- FFmpeg 조립 실패 시 어느 세그먼트에서 깨지는지 로그를 우선 확인하는지
