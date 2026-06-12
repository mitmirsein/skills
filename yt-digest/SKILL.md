---
name: yt-digest
description: >
  Extracts transcripts from YouTube URLs via yt-dlp, cleans them up, and
  produces structured summaries with optional theological analysis. Use
  when the user shares a YouTube link asking for a digest, summary, or
  transcript. 키워드: 유튜브 요약, 자막 추출, 영상 다이제스트
version: 3.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#yt"
  - "#유튜브"
  - "#digest"
  - "summarize this video"
  - "extract transcript"
  - "YouTube URL: [URL]"
capabilities:
  - transcript_extraction
  - intelligent_cleanup
  - theological_synthesis
  - video_error_mining_gotcha_avoidance
references_path: "./references"
status: active
---

# 📺 YouTube Digest (Yuboto) 3.0

## 1. Overview
유튜브 URL에서 자막을 추출하고 지능형 정제 및 신학적 분석을 수행하는 요약 스킬입니다.

## 2. Dynamic Workflow
본 추출 전 **영상 함정(Gotchas)**과 **추출 옵션(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 자막 추출 언어 우선순위 및 요약 결과물 저장 경로를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 자동 생성 자막의 노이즈 및 맥락 오판을 주의합니다.

### Phase 1: Context Detection
유튜브 URL을 감지하고 영상의 주제를 파악합니다.

### Phase 2: Extraction & Cleanup
`yt-dlp` 및 `refiner`를 사용하여 자막을 확보하고 정제합니다. CLI 옵션은 [cli-usage.md](./references/cli-usage.md)를 참조하십시오.

### Phase 3: Synthesis & Reports (Output)
지능형 요약 및 신학적 통찰을 제공하며 `010 Inbox`에 저장합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 제목 낚시 방지 및 화사 의도(반어법 등) 맥락 파악 가이드.
- [cli-usage.md](./references/cli-usage.md): `yt-dlp` 플래그 및 자막 언어 우선순위 로직.
- [best-practices.md](./references/best-practices.md): 시너 가이드 및 리포트 작성 표준.

---
*Powered by MS_Dev Third Gen Standard*
