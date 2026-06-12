# 🔧 AgentOps Specification: zettel-capture

## 1. 상태 관리 (State Management)
- **Stateless 설계**: 각 카드 생성은 독립적 트랜잭션. 이전 카드의 상태에 의존하지 않음.
- **ID 채번 상태**: `config.json`의 `zettel_dir`에서 기존 파일을 스캔하여 다음 ID를 동적으로 결정.
- **성숙 상태**: 각 카드의 YAML `maturity` 필드에 저장. 중앙 DB 불필요.

## 2. 권한 경계 (Permission Boundaries)
- **읽기 허용**: `zettel_dir` 내 기존 카드 (ID 채번, 태그 스캔, Connection 제안용)
- **쓰기 허용**: `zettel_dir` 내 신규 카드 생성, 기존 카드 maturity/connections 업데이트
- **쓰기 금지**: `zettel_dir` 외부 경로, 다른 스킬의 관할 영역(ARC 폴더 등)
- **삭제 권한**: `/zettel review`에서 대장의 명시적 "폐기" 지시가 있을 때만

## 3. 관측 가능성 (Observability)
- **작업 로그**: 카드 생성/승격/폐기 시 `history.log`에 한 줄 기록.
  - 형식: `[YYYY-MM-DD HH:MM] ACTION zettel_id type maturity`
  - 예시: `[2026-03-25 10:05] CREATED 20260325-001 literature 🌱`
- **통계 캐시**: `/zettel stats` 호출 시 실시간 스캔 (캐시 불필요, 카드 수가 수천 단위를 넘지 않을 전망)

## 4. 실패 복구 (Failure Recovery)
- **파일 쓰기 실패**: 임시 파일로 먼저 기록 후 이동(atomic write). 실패 시 원본 보존.
- **ID 충돌**: 기존 파일과 ID가 겹칠 경우 NNN을 +1 재시도 (최대 10회).
- **Source 메타데이터 누락**: 누락 시 카드 생성을 거부하지 않고, `title: "Unknown"` 으로 대체 후 🌱로 표시.

## 5. 승인 워크플로 (Approval Workflow)
- **카드 생성**: 대장의 입력을 구조화한 후 **미리보기**를 제시하고 승인을 받은 후 저장.
- **카드 승격**: `/zettel review`에서 승격 후보를 제시하고 대장의 "승격/유지/폐기" 지시를 기다림.
- **카드 삭제**: 대장의 명시적 "폐기" 지시 후에만 실행. 자동 삭제 금지.

---
*Created by MS_Dev Third Gen Standard*
