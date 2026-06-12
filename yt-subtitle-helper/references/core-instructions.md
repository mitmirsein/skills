# YouTube Subtitle Helper: Core Instructions

본 문서는 에이전트가 유튜브 자막 다운로드, LLM 교정/번역, 그리고 API 업로드를 실행할 때 따라야 하는 기술 매뉴얼입니다.

---

## Phase 1: 자막 다운로드 (`yt-dlp`)
유튜브 영상 ID를 확인한 뒤, 다음 명령어를 실행하여 원본 자막을 다운로드합니다.

```bash
# 자동 생성 자막(ko)을 다운로드하여 test_sub.ko.vtt로 저장
~/.local/bin/yt-dlp --write-auto-subs --skip-download --sub-lang "ko" --output "test_sub" "https://www.youtube.com/watch?v=[VIDEO_ID]"

# 만약 수동 업로드된 자막을 확인하고 싶다면:
~/.local/bin/yt-dlp --list-subs "https://www.youtube.com/watch?v=[VIDEO_ID]"
```

---

## Phase 2: 자막 힐링 및 다국어 번역 (LLM)
다운로드한 자막 파일(VTT/SRT)은 시간 코드와 번호가 들어 있습니다. LLM 프롬프트에 자막의 구조적 정합성을 엄격히 깨지 않도록 지시한 후 진행합니다.

### 1. 한국어 자막 힐링 프롬프트
> **역할**: 구어체 텍스트 오탈자 교정, 한글 맞춤법 준수, 맥락에 맞지 않는 단어 수정 (특히 고유명사나 전문 용어).
```text
[System Prompt]
너는 전문 유튜버 자막 교정 전문가이다. 
제공하는 SRT/VTT 파일 내용에서:
- 일련번호(예: 1, 2)와 시간 코드(예: 00:01:23,450 --> 00:01:25,120)는 공백 하나 틀리지 말고 그대로 보존해야 한다.
- 오타, 띄어쓰기, 맞춤법을 정확히 정정하라. (특히 '방구석 리뷰룸', 'M5 맥북' 등의 고유명사나 문맥에 맞지 않는 발음 기반 오류 정정)
- 구어체 특유의 어색한 어미나 조사 생략을 어색하지 않게 정리하되, 원래 말소리의 흐름과 싱크를 크게 벗어나지 않게 하라.
- 마크다운 문법이나 부가 설명 없이 오직 완성된 자막 파일 결과만 텍스트로 출력하라.
```

### 2. 다국어 번역 프롬프트
교정된 한국어 자막을 소스로 하여 각각 영어, 일본어, 중국어로 번역합니다.
```text
[System Prompt]
너는 전문 번역가이자 자막 현지화 전문가이다.
제공하는 힐링된 한국어 SRT/VTT 자막 파일을 [영어(en) / 일본어(ja) / 중국어(zh-Hans)]로 번역하라.
- 시간 코드와 일련번호는 한 자도 고쳐서는 안 된다.
- 현지 시청자가 보기에 직관적이고 자연스러운 뉘앙스로 번역하라.
- 마크다운 펜스(```) 등을 사용하지 말고, 결과물 자막 파일 텍스트만 그대로 출력하라.
```

---

## Phase 3: 자막 배치 업로드 (`cli.py`)
번역된 다국어 자막 파일을 `projects/yt-subtitle-helper` 디렉토리 아래에 정해진 언어명으로 저장한 후, 다음 CLI 명령어를 활용해 업로드를 수행합니다.

### 1. 사전 권한 검증 및 세션 확인
```bash
# 최초 1회 또는 세션 만료 시 로그인 창 활성화
uv run --inexact python cli.py login
```

### 2. 비디오 자막 리스트 확인
```bash
uv run --inexact python cli.py list [VIDEO_ID]
```

### 3. 언어별 자막 업로드
동일 언어의 자막이 이미 리스트에 있으면 CLI 내부에서 자동으로 `update` (덮어쓰기)를 수행하고, 없을 시 `insert` (새 트랙 등록)를 수행합니다.
```bash
# 한국어 교정본 업로드
uv run --inexact python cli.py upload [VIDEO_ID] "path/to/ko.srt" ko --name "한국어 (교정본)"

# 영어 번역 자막 업로드
uv run --inexact python cli.py upload [VIDEO_ID] "path/to/en.srt" en --name "English"

# 일본어 번역 자막 업로드
uv run --inexact python cli.py upload [VIDEO_ID] "path/to/ja.srt" ja --name "日本語"

# 중국어 번역 자막 업로드
uv run --inexact python cli.py upload [VIDEO_ID] "path/to/zh-Hans.srt" zh-Hans --name "简体中文"
```
