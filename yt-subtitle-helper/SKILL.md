---
name: yt-subtitle-helper
description: >
  Coordinates the YouTube subtitle workflow — download via yt-dlp, LLM
  spelling correction and multilingual translation, then batch upload via
  the YouTube API. Use when the user asks to fix, translate, or publish
  subtitles for their own videos.
  키워드: 유튜브 자막 교정, 자막 번역, 자막 업로드
version: 2.0.1
author: MS_Dev
triggers:
  - "#yt-subtitle"
  - "#유튜브자막"
  - "유튜브 자막 번역 및 업로드"
capabilities:
  - download_subtitles
  - heal_subtitles_llm
  - translate_subtitles_llm
  - upload_subtitles_api
references_path: "./references"
status: active
---

# 📺 YouTube Subtitle Helper 2.0

## 1. Overview
유튜브 영상의 자막을 다운로드하여, 언어 모델(LLM)을 통해 음성 인식 오탈자를 교정하고, 다국어(영어, 일본어, 중국어 등) 자막을 일괄 생성한 후 유튜브 채널에 API를 통해 최종 배치 업로드하는 전체 프로세스를 제어합니다.

## 2. Core Workflow
1. **자막 다운로드 (Download)**: `yt-dlp`를 사용하여 원본 한국어 자막(또는 자동 생성 자막)을 SRT/VTT 파일로 내려받습니다.
2. **자막 정제 및 번역 (Heal & Translate)**:
   - LLM을 활용해 음성 인식 오탈자를 수정하고 읽기 편한 구어체로 다듬습니다 (자막 시간 코드 엄격 보존).
   - 정제된 한국어 텍스트를 기준으로 영어(en), 일본어(ja), 중국어(zh) 자막을 일괄 생성합니다.
3. **자막 업로드 (Upload)**: 로컬 프로젝트 `projects/yt-subtitle-helper`의 CLI를 호출하여 자막 목록 조회 및 업로드(등록/덮어쓰기)를 수행합니다.

## 3. Reference Links
- [core-instructions.md](./references/core-instructions.md): 단계별 CLI 명령어 및 프로세스 실행 가이드
- [best-practices.md](./references/best-practices.md): 자막 교정 시 프롬프트 원칙 및 쿼터 제한 핸들링 가이드

---
*Created by MS_Dev Skill Forge*
