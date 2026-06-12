# Remotion Studio: Asset Rendering & Production

스토리보드를 실제 비디오 파일로 변환하기 위한 프로그래밍 방식의 렌더링 파이프라인입니다.

## 🚀 3-Step Production Pipeline

### 1. Asset Generation (Voiceover)
`edge-tts`를 활용하여 씬별 음성(MP3)과 자막 데이터(`metadata.json`)를 생성합니다.
```bash
uv run python agents/generate_voiceover.py projects/remotion_studio/video-config.json
```
- **Inputs**: `video-config.json`.
- **Outputs**: `public/audio/*.mp3`, `public/metadata.json`.

### 2. Video Rendering
Remotion 엔진을 가동하여 React 컴포넌트를 비디오 프레임으로 렌더링합니다.
```bash
cd projects/remotion_studio && npm run render
```
- **Location**: `projects/remotion_studio/`.
- **Internal**: `remotion render src/index.ts MyComp public/video.mp4`.

### 3. Verification & Export
- **Output Location**: `projects/remotion_studio/public/video.mp4`.
- **Final Report**: 사용자에게 완성된 비디오의 재생 시간, 형식, 그리고 저장 경로를 통지합니다.

## ⚠️ Common Failure Points
- **Duration Mismatch**: 음성 길이보다 씬 기간이 짧을 경우 렌더링 오류가 발생합니다. (`generate_voiceover`에서 자동 계산된 결과 확인 필수).
- **Node Modules**: 렌더링 전 프로젝트 루트의 `node_modules` 존재 여부를 확인합니다.
