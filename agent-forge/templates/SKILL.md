---
name: [Skill Name]
description: [One-sentence purpose for agent routing - high signal]
version: 1.0.0
author: MS_Dev
sources_of_truth:
  - "[Official Documentation URL 1]"
  - "[Official Documentation URL 2]"
triggers:
  - "#keyword"
  - "natural language intent"
capabilities:
  - main_action_1
  - main_action_2
references_path: "./references"
---

# 🛠️ [Skill Name] (v3.1)

## 1. Overview & DNA
[Skill Name]의 목적과 핵심 가치를 기술합니다. 모델이 자신의 기본 지식(훈련 데이터)과 다른 '이 스킬만의 최신 지침'을 파악하게 하세요.

## 2. Dynamic Knowledge Workflow
1. **Fetch & Verify**: 상단 `sources_of_truth` URL 중 가장 관련성 높은 문서를 `read_url_content` 등으로 읽어 현재 지식과 대조합니다. (Knowledge Gap 해소)
2. **Setup (선택)**: 개인화가 필요한 스킬만 `config.json`을 읽는다. 없으면 이 단계를 건너뛴다.
3. **Review History (선택)**: 장기 맥락 재사용 스킬만 `history.log`를 읽는다.
4. **Analyze & Execute**: 핵심 로직을 수행한다.
   - 상세 지침: [core-instructions.md](./references/core-instructions.md)
5. **Guardrail Check**: [gotchas.md](./references/gotchas.md)를 대조하여 흔한 실수를 방지한다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(필수)** 반드시 피해야 할 함정 및 예외 케이스.
- [core-instructions.md](./references/core-instructions.md): 상세 가이드 및 명령어 예시.
- `config.json` *(선택)*: 사용자 개인화가 필요한 경우에만 생성.

## 4. Sources of Truth (Live Knowledge)
에이전트는 작업 수행 전 다음 공식 소스를 참조하여 최신 사양을 확인해야 합니다:
- [Source Name 1]: [URL 1]
- [Source Name 2]: [URL 2]

---
*MS_Dev Agent Forge 표준 템플릿. 생성 스킬은 version 1.0.0에서 시작한다. 표준 권위: agent-forge/SKILL.md.*
