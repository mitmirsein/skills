# Note Share: Execution Workflow

백그라운드 에이전트 환경에서 충돌 없이 노트 공유 명령을 처리하기 위한 4단계 워크플로우입니다.

## 🚀 4-Step Pipeline
1. **URI Encoding**: 파일 경로에 빈 칸이나 특수문자가 포함되므로 반드시 URL 인코딩을 수행합니다.
   - `ENCODED_PATH=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$FILEPATH")`
2. **Advanced URI Call**: `open` 명령을 사용하여 Obsidian 앱에 플러그인 실행 신호를 보냅니다.
   - `open "obsidian://advanced-uri?vault=MS_Brain.nosync&filepath=${ENCODED_PATH}&commandid=[명령ID]"`
3. **Wait & Capture**: 네트워크 업로드 및 클립보드 복사 시간을 위해 대기(`sleep 5`) 후 `pbpaste`로 URL을 확보합니다.
4. **Metadata Update**: 획득한 URL을 노트의 `share_url` 속성(Properties)에 공식 CLI를 사용하여 기록합니다.
   - `obsidian property:set file="파일명" name="share_url" value="$URL" ...`

## ⚠️ Key Rules
- **No `obsidian command`**: 이 스킬에서는 공식 CLI의 `command` 명령을 사용하지 않습니다. (Electron Trace/BPT trap 오류 방지)
- **Plugin Priority (Share Note -> JSP)**: 사용자의 특별한 개별 지정이 없는 한, 항상 **Share Note (`share-note:share-note`)**를 1순위로 실행하여 업로드를 시도합니다. 만약 Share Note 플러그인이 설치되어 있지 않거나 업로드 에러가 발생하는 경우, 차선책인 2순위 **Just Share Please (JSP) (`just-share-please:share`)**를 기동하여 폴백 처리를 보장합니다.
- **Sleep Duration**: 대용량 노트나 네트워크 지연을 고려하여 `3~5초` 정도의 충분한 대기 시간을 가져야 합니다.
