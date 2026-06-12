# Workflow Reference

## 표준 실행 순서

```bash
cd ~/Desktop/MS_Dev.nosync/projects/lecture_video_generator
uv run python pipeline.py generate input/sample_lecture.md --design modern
uv run python pipeline.py tts input/sample_lecture.md
uv run python pipeline.py assemble output/sample_lecture
```

## 일괄 실행

```bash
uv run python pipeline.py all input/sample_lecture.md --design modern
```

## 단계별 검수

### generate 이후

- `outline.json` 존재
- `slide_*.svg` 존재
- `slide_*.png` 존재
- `tts_*.txt` 존재

### tts 이후

- `audio_*.wav` 존재
- 섹션 번호와 오디오 번호가 대응

### assemble 이후

- `final.mp4` 존재
- `segments/` 임시 산출물이 정리되었는지 확인

## 권장 운영 방식

- 배치 실행에서는 `--design`을 명시한다.
- `generate`의 대화형 테마 선택은 자동화 안정성을 떨어뜨리므로 피한다.
- 실패 시 어느 단계 계약이 깨졌는지 먼저 식별한다.
