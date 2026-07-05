---
name: theology-handoff
description: >
  Use when a research or writing session is ending, context is about to be
  compacted, or a long theology project is being handed to a fresh session —
  to carry over gathered evidence, established claims, and unresolved aporia
  without loss.
  키워드: 연구 세션 인계, scholar handoff, 세션 핸드오프, 연구 인계, 컨텍스트 압축, 아포리아 이월
version: 1.1.0
author: MS_Dev
triggers:
  - "연구 세션 인계"
  - "scholar handoff"
  - "세션 핸드오프"
  - "연구 인계"
capabilities:
  - context_compaction
  - unresolved_aporia_listing
  - bibliography_state_transfer
status: active
---

# 🤝 theology-handoff: 학술 컨텍스트 세션 인계

긴 텍스트 주해·대규모 연구에서 세션 리셋이나 컨텍스트 한계로 인한 연구 맥락 단절을 막는 정보 컴팩션 도구. 대화의 장황함을 걷어내고 학술적 팩트·가설·미결 쟁점만 남긴다.

> ⚖️ 아포리아 우선: 봉합되지 않은 신학적 긴장은 요약에서 지우지 말고 §3에 명시적으로 이월한다.

---

## 📋 인계 요약문 표준 템플릿

본 스킬이 트리거되면, 현재 작업 중인 노트·논문 파일을 분석해 다음 항목을 채운 간결하고 강력한 인계 문서를 출력한다.

```markdown
# 🤝 [연구 프로젝트명] 세션 인계서 (Scholar Handoff)

## 📌 1. 현재 연구 현황
- **진행 단계**: (예: 요 1:1a 프롤로그 주해 분석 완료)
- **주요 대상 텍스트**: (예: 요한복음 1:1)

## ⚖️ 2. 확립된 논지 및 증거 (Established Claims)
theology-evidence-writing(EDD) 증거 테이블 `EV-*` 또는 TAWP `claim-ledger` 의 claim ID 로 확증된 내용.
- **[요지 A]** (근거: `EV-01`)
- **[요지 B]** (근거: `EV-02`)

## 🔍 3. 미결 해석학적 아포리아 (Unresolved Aporia)
다음 세션에서 긴장을 보존하며 풀어야 할 갈등·난제. (평탄화 금지)
1. **[아포리아 1]**: (예: 창조 로고스와 성육신 로고스의 존재론적 연속성)
2. **[아포리아 2]**: (예: 사본 간 단어 혼용에서 오는 해석학적 편향 가능성)

## 🎯 4. 다음 단계 태스크
- [ ] (예: 요 1:1b "말씀이 하나님과 함께 계셨으니" 문맥 주해)
- [ ] (예: 2차 문헌 Bultmann 주석 대조)

## 📂 5. 주요 파일 및 서지
- **정본 소스 파일**: [파일명](볼트 루트 기준 상대경로)
- **참고 문헌**: (주요 서적·DB 링크)
```

> ⚠️ 경로 이식성: 인계서에 `file:///Users/...` 절대경로를 쓰지 않는다. 사용자명이 다른 두 Mac(Syncthing 동기화) 사이에서 깨진다. 볼트/프로젝트 루트 기준 상대경로를 쓴다.
> ⚠️ 서지 표기: 책 제목에 이탤릭(`*…*`)을 쓰지 않는다(볼트 전면 금지). 『제목』 또는 따옴표로 표기한다.

---

## 🚀 실행 프로세스

1. **컨텍스트 축소** — 장황한 진행 과정을 걷어내고 팩트·가설·미결 쟁점 중심으로 단순화한다.
2. **아포리아 명시** — 대화에서 조율됐으나 본문에 아직 서술되지 않은 신학적 텐션을 §3에 누락 없이 기록한다.
3. **다음 에이전트 가이드** — 이 인계서가 다음 세션의 최우선 정렬 기준(SSOT)이 된다. 출력 후 세션을 안전하게 종료한다.

## When NOT to use

- 사용자 **선호·버릇** 영속 학습(연구 상태가 아님) → `continuous-learner`
- TAWP 논문의 **버전·Phase·아티팩트 상태** 추적 → `tawp` 의 run_manifest
