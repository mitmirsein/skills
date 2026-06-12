# Batch Operator: Parallel Execution & Safety

대규모 파일군에 대한 일괄 작업(Batch)의 병렬 실행 전략과 안전 수칙입니다.

## 🚀 The Batch Pipeline
1. **Scout (색인)**: `grep_search`나 `find_by_name`을 통해 대상 파일 목록과 변경 패턴을 파악합니다.
2. **Batch Plan (계획)**: 총 작업량을 분석하고, 에이전트의 처리 한도에 맞춰 배치 그룹(예: 5개씩 1세트)을 나눕니다.
3. **Blast (일괄 반영)**: 시스템의 병렬 도구 호출(Concurrent Tool Calls) 기능을 활용하여 한 턴에 여러 파일을 동시 수정합니다.
4. **Verify & Report (검증)**: 수정된 파일 샘플을 검증하고, 총 결과물(파일 수, 변경 지점)을 보고합니다.

## 🛡️ Safety & Token Economy
- **Atomic Commits**: 대규모 변경 전 `git commit`을 제안하거나 작업 로그를 남겨 롤백 가능성을 확보합니다.
- **Concurrent Limit**: 에이전트의 안정성을 위해 한 번에 5~10개 이상의 파일을 병렬로 다루지 않는 것이 좋습니다. (필요 시 배치 분할)
- **Targeted Replace**: 파일 전체를 덮어쓰기보다 `multi_replace_file_content`로 핵심 지점만 정확히 타격하여 토큰을 절약합니다.

## 🏗️ Use Cases
- 프레임워크 마이그레이션 (예: Jest → Vitest).
- 전역 주석 번역 및 독스트링 추가.
- 명칭 일괄 변경 및 코드 스타일 수정.
