# YT-Digest CLI & Priority Guide

## 1. Transcript Extraction Priority
`yt-dlp`를 사용하여 다음 우선순위에 따라 자막을 추출합니다.

- **우선순위 1**: 사용자 직접 업로드 자막(Manually uploaded) 중 **원어(Source Language)** 자막 최우선.
- **우선순위 2**: 사용자 업로드 자막이 없을 경우, **자동 생성 자막(Auto-generated)** 중 **원어** 자막 우선.

## 2. Command Examples

### Subtitle List Check
```bash
uv run yt-dlp --list-subs [URL]
```

### Manual Subtitle Extraction
독일어 영상의 경우 `de` 등 원어 코드를 사용합니다.
```bash
uv run yt-dlp --write-subs --skip-download --sub-lang [lang] --output "/tmp/yt_subs" [URL]
```

### Auto-generated Subtitle Extraction
업로드된 자막이 없을 때 사용합니다.
```bash
uv run yt-dlp --write-auto-subs --skip-download --sub-lang [lang] --output "/tmp/yt_subs" [URL]
```

## 3. Failure Handling
- **429 Too Many Requests**: 유튜브 IP 차단 시 `stealth-browser`를 통해 브라우저 상에서 자막을 취득합니다.
- **No Subs Found**: 영상 자체에 자막 데이터가 없는 경우 OCR 실행을 검토합니다.
