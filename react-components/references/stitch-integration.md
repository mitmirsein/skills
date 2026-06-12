# React Components: Stitch Integration & Fetching

Stitch 디자인 데이터를 고신뢰도로 확보하고 리액트 프로젝트로 이식하기 위한 기술 연동 규격입니다.

## 📡 Stitch MCP Discovery
- `list_tools` 실행 후 발견되는 Stitch MCP 접두사(예: `stitch:`)를 확인합니다.
- `[prefix]:get_screen`을 호출하여 디자인의 JSON 메타데이터와 HTML 코드를 획득합니다.

## ⚡ High-Reliability Fetch (fetch-stitch.sh)
내장된 에이전트 도구가 Google Cloud Storage 등의 도메인에서 인증 오류나 리다이렉트 실패 시 수동으로 발동합니다.
- **Location**: `.skills/reactcomponents/scripts/fetch-stitch.sh`
- **Command**: `bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"`
- **Role**: 보안 핸드셰이크와 리다이렉트를 처리하여 원본 HTML 소스를 로컬로 확보합니다.

## 👁️ Visual Audit
- `screenshot.downloadUrl`을 통해 실제 렌더링된 화면의 종횡비, 컴포넌트 간 간격, 폰트 웨이트(Weight) 등을 최종 확인하여 코드로 번역합니다.
