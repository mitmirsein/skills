---
name: zettel-capture
description: >
  Captures a sentence, insight, or source into an atomic Zettelkasten card
  (Fleeting/Literature/Permanent) with auto-assigned IDs and a maturation
  queue. Use when the user wants to memo an inspiration, turn a quote into
  a card, or review and promote immature cards.
  키워드: 제텔, 메모 카드, 영감 기록, 카드 승격
version: 1.0.1
codename: Third Gen
author: MS_Dev
triggers:
  - "#zettel"
  - "#제텔"
  - "#메모"
  - "#카드"
  - "/zettel"
  - "/z"
  - "이 문장 메모해줘"
  - "이거 카드로 만들어줘"
  - "인사이트 기록해줘"
capabilities:
  - zettelkasten_atomic_note_capture
  - three_tier_note_classification
  - maturation_queue_management
  - source_metadata_structuring
  - connection_suggestion
references_path: "./references"
status: active
---

# 🗃️ Zettel Capture 1.0

## 1. Overview
독서, 논문, 영상, 팟캐스트, 일상적 사유 등에서 얻은 **영감의 순간**을 구조화된 원자적 메모(Zettel Card)로 즉시 포착하는 경량 전문 스킬입니다.

**이 스킬의 정체성**: "포착(Capture)만 한다. 분류(Filing)와 온톨로지 추출은 다른 스킬의 영역이다."

### Negative Scope (이 스킬이 하지 않는 것)
- ❌ ARC 폴더 분류 → `arc-librarian`
- ❌ 온톨로지/엔티티 추출 → `ontology-builder`
- ❌ 웹 스크래핑/PDF 수집 → `knowledge-archivist`
- ❌ 유튜브 트랜스크립트 추출 → `yt-digest`

## 2. Dynamic Workflow

### Phase 0: Setup & Guardrail
- **Verify Config**: `config.json`에서 기본 저장 경로, 태그 프리셋, 사유 촉발(Prompting) ON/OFF를 확인합니다.
- **Gotcha Check**: [gotchas.md](./references/gotchas.md)를 읽고 과잉 카드 생성, fleeting 방치 등을 방지합니다.

### Phase 1: INTAKE (입력물 수용)
대장의 입력물(문장, URL, 파일 경로, 자유 텍스트)을 수용합니다. 상세 지침은 [capture-instructions.md](./references/capture-instructions.md)를 참조하십시오.

### Phase 2: CLASSIFY (노트 유형 판별)
3단계 노트 유형(💭 Fleeting / 📖 Literature / 💎 Permanent) 중 적합한 유형을 판별하여 제안합니다. 유형별 규격은 [card-schema.md](./references/card-schema.md)를 참조하십시오.

### Phase 3: CRAFT (카드 구조화)
해당 유형의 템플릿에 맞춰 카드를 구조화합니다. 사유 촉발은 **Default OFF** — 대장이 Zettel 섹션을 비워놓았을 때에만 한 번 물어봅니다.

### Phase 4: SAVE (저장)
`config.json`에 정의된 경로에 마크다운 파일로 저장합니다. Zettel ID는 `YYYYMMDD-NNN` 형식으로 자동 부여됩니다.

## 3. Additional Commands
- `/zettel review`: 미성숙(🌱) 카드 리뷰 및 승격 프로세스. 상세 지침은 [maturation-guide.md](./references/maturation-guide.md)를 참조하십시오.
- `/zettel stats`: 유형별·성숙도별 카드 현황 통계.

## 4. Reference Links
- [gotchas.md](./references/gotchas.md): **(필수)** 과잉 생성 방지 및 품질 유지 가이드.
- [capture-instructions.md](./references/capture-instructions.md): 입력 유형별 처리 로직 및 소스 구조화 규칙.
- [card-schema.md](./references/card-schema.md): 3단계 노트 유형별 카드 템플릿 규격.
- [maturation-guide.md](./references/maturation-guide.md): 성숙 큐 운영 및 승격 기준 가이드.

---
*Created by MS_Dev Third Gen Skill Forge*
