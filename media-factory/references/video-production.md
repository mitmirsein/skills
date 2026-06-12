# Media Factory: Video Production & FFmpeg

오디오와 이미지를 결합하여 고품질 MP4 비디오(Audiogram)를 제작하기 위한 지침입니다.

## 🎬 Video Factory Engine
`scripts/video_factory.py` 스크립트를 사용하여 비디오를 렌더링합니다.

```bash
uv run scripts/video_factory.py "[AUDIO_PATH]" "[IMAGE_PATH]" "[OUTPUT_PATH]" --mode cinema
```

### ⚙️ Rendering Modes
- **cinema (default)**: 이미지를 1920x1080으로 확대 및 크롭하여 화면을 꽉 채웁니다.
- **blur**: 이미지를 중앙에 배치하고 배경에는 흐릿한(Blured) 배경을 생성합니다. (1:1 이미지를 16:9 영상으로 만들 때 권장)
- **fit**: 이미지 전체가 보이도록 맞추고 나머지는 검은색 바(Black bars)로 채웁니다.

## 📽️ Output Standards
- **Format**: MP4 (H.264 Video + AAC Audio).
- **Duration**: 오디오 파일의 길이에 맞춰 비디오가 생성됩니다.
- **Verification**: 파일 생성 후 물리적 존재 여부와 용량을 확인하여 보고합니다.
