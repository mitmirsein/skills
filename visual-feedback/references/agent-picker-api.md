# Visual Feedback: Agent Picker API & Commands

사용자의 실시간 시각적 선택(Selection) 정보를 획득하고, 에이전트의 처리 상태를 공유하기 위한 API 명세입니다.

## 📡 Agent Picker Daemon (agent-pickerd)
- **Vendored Path**: `~/Desktop/MS_Dev.nosync/vendor/agent-picker/`
- **Execution Context**: 프로젝트 루트 또는 벤더 디렉토리에서 `npm run`을 지원합니다.

## 🛠️ Key Commands

### 1. 픽커 선택 정보 획득 (Get Selection)
사용자가 앱에서 특정 요소를 선택했을 때 그 메타데이터를 가져옵니다.
```bash
npm run agent-pickerd:get-selection
```
- **Output**: JSON (selector, text_content, tag_name, attributes 등 포함).

### 2. 에이전트 노트/상태 업데이트 (Set Note)
현재 작업 상태를 사용자의 브라우저 UI에 표시합니다.
```bash
npm run agent-pickerd:set-agent-note -- --author pepone --status [status] --message "[msg]"
```
- **Statuses**: `acknowledged`, `in_progress`, `fixed`, `error`.

## 📦 Data Format (Selection JSON)
```json
{
  "selector": "body > div.container > nav > ul > li:nth-child(2)",
  "text_content": "About Us",
  "comment": "폰트를 Inter Bold로 변경해줘."
}
```
