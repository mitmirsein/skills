---
name: barth-kd-navigator
description: >
  Reads Karl Barth's Kirchliche Dogmatik (KD) from the German text,
  translates it into Korean Protestant terminology with fidelity gates, and
  archives study notes by paragraph (§). Use when the user wants to read,
  translate, or take notes on Barth's Church Dogmatics.
  키워드: 바르트, KD 읽기, 교의학 번역
version: 2.1.1
codename: Fidelity Gate
author: MS_Dev
triggers:
  - "#KD"
  - "KD 읽기"
  - "#바르트"
capabilities:
  - german_theology_translation
  - barthian_exegesis
  - academic_archiving
  - error_mining_and_gotcha_avoidance
references_path: "./references"
status: active
---

# 🎓 Barth KD Navigator 2.0

## 1. Overview
칼 바르트의 『교의학』(Kirchliche Dogmatik, KD) 독일어 원문을 정독하며 한국 개신교 신학 용어 체계에 맞춰 번역하고 지혜를 축적하는 전용 연구 스킬입니다.

## 2. Dynamic Workflow
본 스킬은 연구 전 **번역 함정(Gotchas)**과 **사용자 환경(Config)**을 먼저 점검합니다.

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 현재 연구 중인 §(단락) 번호와 목표 디렉토리 경로를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 개신교 용어 이탈 및 독일어 오타 교정 실수를 방지합니다.

### Phase 1: Text Refining (교정)
PDF 복합 사본의 OCR 오류를 독일어 문법에 맞춰 정밀 교정하고 확정합니다.
**[v2.1 추가]** 교정 완료 후 **Structural Manifest** 생성:
- 총 문장 수, Fremdwörter(외래어) 목록, 핵심 신학 개념어 목록

### Phase 2: Contextual Translation (번역)
정제된 원문을 개신교 용어 체계로 번역하고 바르트 특유의 주요 개념(Akt, Vollzug 등)을 주석으로 해설합니다.
**[v2.1 추가]** 각 문장에 `[S1]`, `[S2]` 넘버링 부여. 독일어 원문 → 번역문 1:1 추적 가능성 확보.

### Phase 2.5: Red-Team Audit (신규)
**[v2.1 신규]** [gotchas.md § 4](./references/gotchas.md)의 **Red-Team Adversary Protocol 실행**.
- KD 특화 체크리스트(변증법 구조, 삽입절, §번호) 대조표 제출.
- F-Score 산출: `uv run python agents/translator_audit.py --source <원문> --target <번역> --strict`
  - `--strict` 옵션: 합격 기준 95%로 상향 (바르트 고위험군 텍스트)

### Phase 3: Dialectic & Archiving (토론 및 저장)
**[v2.1 추가]** Red-Team 대조표를 먼저 대장에게 제시하여 검증 포인트 사전 공유.
이후 신학적 토론을 거쳐 3중 분리 저장 시스템(`Translations`, `Protocols`, `Insights`)에 결과물을 영구 보전합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): **(중요)** 개신교 용어 고수 및 바르트 연구 시 주의해야 할 3개 영역(번역, 교정, 기록).
- [terminology-guide.md](./references/terminology-guide.md): 바르트 연구 전용 개신교 신학 용어 대조표.
- [kd-structure.md](./references/kd-structure.md): KD 73개 Paragraph 전체 인덱스.

---
*Created by MS_Dev Third Gen Standard*
