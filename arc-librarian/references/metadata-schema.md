# ARC Librarian: YAML Metadata Schema

MS_Brain.nosync 볼트 내 모든 지식 자산에 공통으로 적용되는 표준 YAML Frontmatter 규격입니다.

## 📄 Schema Definition
```yaml
---
tags: [Primary/Sub, Topic, Keyword] # 계층형 태그 활용
created: YYYY-MM-DD
updated: YYYY-MM-DD
related: 
  - "[[Note_Name]]" # 관련 노트 백링크
themes: [Key_Keyword1, Key_Keyword2]
references: [Source_Material, Bible_Verse]
category: 'XXX' # ARC 분류 코드 (예: 110, 210)
arc_score: 5 # 1~10 품질 점수
---
```

## 📜 Field Guide
- **tags**: `Theology/Biblical`, `Ministry/Meditation` 등 대분류/소분류 형식 권장.
- **related**: 최소 1개 이상의 기존 노트와 연결하여 지식 그래프의 밀도를 높입니다.
- **references**: 핵심 출처(성경 구절, 저작명 등)를 명시하여 지식의 계보를 추적 가능하게 합니다.
- **category**: ARC 맵에 따른 소분류 코드를 문자열 형식으로 입력합니다.
