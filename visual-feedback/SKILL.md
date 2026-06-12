---
name: visual-feedback
description: >
  Closes the loop between a user's visual selection in the browser and the
  source code — reads agent-picker selections (CSS selector, text,
  attributes), hunts down the owning component file, applies the fix, and
  reports status back to the browser UI. Use when the user picks an element
  in the running app and asks to change it.
  키워드: 화면 선택 수정, 비주얼 피드백, 이 버튼 고쳐줘
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "#picker"
  - "지금 선택한 거 수정해줘"
  - "화면에서 찍은 부분 고쳐줘"
references_path: ./references
---

# 🎯 Visual Feedback (시각 선택 → 코드 수정 루프)

사용자가 브라우저에서 찍은 요소를 소스 컴포넌트로 역추적해 수정하는 스킬입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- 사전 조건: `agent-pickerd` 데몬 가동 (벤더 경로 `~/Desktop/MS_Dev.nosync/vendor/agent-picker/`).

## Phase 1 — 선택 정보 획득 (정본: [agent-picker-api.md](./references/agent-picker-api.md))

```bash
npm run agent-pickerd:get-selection   # → JSON: selector, text_content, tag_name, attributes
```

## Phase 2 — 소스 추적 (정본: [localization-hunter.md](./references/localization-hunter.md))

1. **Selector Parsing**: 유일 ID(`#hero`) 최우선, 해시 클래스는 구조 태그+속성 조합으로 검색
2. **Text-Content Search**: 셀렉터가 모호하면 `text_content`로 `grep -rI` (다국어 키 주의)
3. **Hierarchy Traversal**: 부모 노드를 거슬러 컴포넌트 경계 특정

## Phase 3 — 수정·상태 공유

- 수정 전 **Acknowledge**: "AboutUs.tsx의 2번째 항목을 수정하겠습니다" 식으로 위치를 먼저 보고
- `npm run agent-pickerd:set-agent-note`로 처리 상태를 브라우저 UI에 실시간 표시

## 검증·보고

- 수정한 파일:줄, 적용 결과(핫 리로드 확인), 선택 요소와의 일치 근거를 보고합니다.
- 추적 실패(다중 매칭 등) 시 후보 목록을 제시하고 사용자에게 확인을 받습니다.
