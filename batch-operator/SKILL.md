---
name: batch-operator
description: >
  Runs large-scale parallel file processing and bulk code migrations (a
  /batch-style operator). Use when the user asks to apply the same change
  across many files or automate a repository-wide migration.
  키워드: 일괄 처리, 대량 마이그레이션, 배치 작업
version: 2.0.1
codename: Second Gen
author: MS_Dev
triggers:
  - "#batch"
  - "일괄 처리해줘"
  - "파일 전체 마이그레이션 시작"
  - "bulk update [files]"
capabilities:
  - concurrent_file_editing
  - batch_migration_pipeline
  - targeted_content_replacement
  - massive_refactoring_automation
references_path: "./references"
status: active
---

# 🚀 Batch Operator 2.0

## 1. Overview
수십 개의 파일을 동시에 수정하거나 시스템 전반의 대규모 마이그레이션을 자동화하는 고성능 일괄 처리 도구입니다. 병렬 실행(Concurrency)을 통해 작업 시간을 극적으로 단축합니다.

## 2. Core Workflow
1. **Scout & Planning**: 대상 파일을 식별하고 배치 처리 계획(Chunking)을 수립합니다.
2. **Execution (Blast)**: 병렬 도구 호출 기능을 동원하여 다수의 파일을 한 번에 업데이트합니다.
   - 상세 병렬 실행 전략 및 안전 규정은 [parallel-execution.md](./references/parallel-execution.md)를 참조하십시오.
3. **Verification**: 샘플링 검증을 통해 일괄 수정의 정확도를 보고합니다.

## 3. Reference Links
- [parallel-execution.md](./references/parallel-execution.md): 배치 파이프라인(Scout-Plan-Blast-Report), 병렬 호출 한도, 안전망 및 토큰 최적화 지침.

---
*Created by MS_Dev Second Gen Skill Forge*
