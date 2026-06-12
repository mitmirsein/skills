---
name: theology-terminology-linter
description: >
  Lints a document for inconsistent Korean renderings of the same
  theological term (equivocation) against the tre_terms.csv vocabulary and
  reports warnings without forcing replacements. Use when the user asks to
  check terminology consistency before publishing — per workspace policy,
  a final reference filter, not an early-stage constraint.
  키워드: 용어 린터, 번역어 혼용 검사, 용어 일관성
version: 1.0.1
author: MS_Dev
triggers:
  - "#theology-terminology-linter"
  - "#용어린터"
  - "신학 용어 일관성 검사해줘"
  - "용어 혼용 검사해줘"
capabilities:
  - terminology_consistency_audit
  - equivocation_detection
  - tre_vocabulary_alignment
references_path: "./references"
status: active
---

# 🔍 Theology Terminology Linter

## 1. 개요
신학 학술 서술에서 가장 빈번하게 발생하는 문제 중 하나는 동일한 원어 개념에 대해 서로 다른 한국어 번역어를 혼용함으로써 발생하는 **개념적 혼동(Equivocation)**이다. 본 스킬은 `tre_terms.csv`에 명시된 신학 용어 데이터베이스를 기반으로 문서 내부의 번역 일관성을 검사하여 리포트를 생성한다.

## 2. 작동 원리
1. **단어 파싱**: `tre_terms.csv`에 정의된 대체 역어(슬래시 `/` 분리 단어들) 및 문서 내 고유한 신학적 대립 쌍을 식별한다.
2. **문서 스캔**: 대상 문서를 라인 단위로 스캔하여 각 용어가 출현하는 정확한 라인을 기록한다.
3. **혼용 진단**: 동일 개념의 대체 역어가 하나의 문서 안에서 동시에 검출되는 경우(예: '면죄부'와 '면벌부'), 이를 일관성 붕괴(Equivocation) 경고로 분류한다.
4. **리포트 작성**: 강제적인 치환을 행하지 않고, 경고 대상 단어와 출현 위치를 명시한 보고서(`*_terminology_audit.md`)를 한국어 평서문으로 작성한다.
