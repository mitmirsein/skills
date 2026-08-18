---
name: digital-curator
description: >
  Analyzes a useful website or database URL and registers it in the vault's
  Digital_Library_Inventory.md in the standard format, with duplicate
  detection and category assignment. Use when the user asks to add a site
  to the library or register a resource in the inventory.
  키워드: 사이트 등록, 인벤토리 추가, 디지털 자료 큐레이션
version: 3.1.1
codename: Skill Standard v3.1
author: MS_Dev
sources_of_truth:
  - "~/Desktop/MS_Library.nosync/000 System/Digital_Library_Inventory.md"
triggers:
  - "#curate [URL]"
  - "#등록 [URL]"
  - "library에 추가해줘"
  - "인벤토리에 사이트 등록해줘"
capabilities:
  - web_resource_analysis
  - automated_library_registration
  - scholarly_resource_classification
  - duplicate_entry_detection
references_path: "./references"
status: active
---

# 🌐 Digital Curator 3.1

## 1. Overview
사용자가 제공한 URL을 분석하여 그 가치를 평가하고, 이를 `Digital_Library_Inventory.md`의 표준 양식에 맞게 자동으로 등록하는 관리형 스킬입니다. 파편화된 웹 지식을 사령부의 공식 인벤토리로 통합하는 지식 관문의 역할을 수행합니다.

## 2. Dynamic Workflow (RISE)

### Step 1: Fetch & Verify (RISE-1)
- 입력된 URL의 내용을 `read_url_content` 또는 `search_web`으로 정찰합니다.
- 사이트의 제목, 목적, 핵심 제공 서비스, 그리고 특이사항(Zotero 지원 여부 등)을 추출합니다.
- `Digital_Library_Inventory.md`를 먼저 읽어 **이미 등록된 중복 사이트**인지 반드시 확인합니다.

### Step 2: Analyze & Classify (RISE-2)
- 추출된 정보를 바탕으로 **표준 카테고리**(신학, 성서신학, 인문학, AI 등)를 할당합니다.
- [core-instructions.md](./references/core-instructions.md)의 **등록 양식**에 맞게 데이터를 매핑합니다.

### Step 3: Execute & Link (RISE-3)
- 인벤토리 파일의 가장 적절한 섹션(Research, Tool, Library 등)을 찾아 내용을 삽입합니다.
- 삽입 시 기존 마크다운 구조를 깨뜨리지 않도록 주의합니다.

### Step 4: Reflect & Propose (RISE-4)
- 등록 결과를 대장에게 보고하고, 해당 사이트의 자료를 적극적으로 수집(`knowledge-archivist`)하거나 온톨로지화(`ontology-builder`)할 필요가 있는지 제안합니다.

## 3. Reference Links
- [gotchas.md](./references/gotchas.md): 중복 등록 및 불확실한 정보 입력 방지 가이드.
- [core-instructions.md](./references/core-instructions.md): 표준 등록 양식 및 파일 삽입 규칙.
- [config.json](./config.json): 인벤토리 파일 경로 및 선호 카테고리 설정.

---
*Created by MS_Dev Skill Forge v5.1*
