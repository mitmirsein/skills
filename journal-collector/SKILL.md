---
name: journal-collector
description: >
  Maintains curated journal registries (theology_journals.json,
  economics_journals.json — ISSN sets consumed by crossref-journal-searcher)
  and guides issue-level collection of German theology journals (KuD, EvTh,
  ZNW, ZThK) via the Librarian workflow. Use when the user asks to add or
  update a journal in the curated list, or collect a specific journal
  issue's metadata. 키워드: 저널 목록 관리, 학술지 수집, ISSN 등록
version: 1.0.0
status: active
author: MS_Dev
triggers:
  - "저널 목록에 추가해줘"
  - "이 학술지 수집해줘"
  - "journal collector"
references_path: ./references
---

# 📚 Journal Collector (저널 레지스트리·수집)

엄선된 저널 레지스트리(JSON)를 관리하고, 독일어권 신학 학술지의 호(Heft) 단위 수집을
안내하는 스킬입니다.

### 이 스킬의 자산 (다른 스킬이 소비)

- `theology_journals.json` — 신학 프리미엄 저널 ISSN 세트 → `.skills/crossref-journal-searcher`가 필터로 사용
- `economics_journals.json` — 경제학 저널 세트

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 함정을 확인합니다.
- 레지스트리 JSON 수정 전 **반드시 기존 항목 중복(ISSN 기준)을 확인**하고,
  수정 후 JSON 유효성(`python3 -m json.tool`)을 검증합니다.

## Phase 1 — 레지스트리 관리

1. 추가할 저널의 정식 명칭·ISSN(print/electronic)을 Crossref(`api.crossref.org/journals/{ISSN}`)로 검증
2. 해당 JSON에 기존 스키마와 동일한 형태로 추가
3. `.skills/crossref-journal-searcher`로 표본 검색을 1회 실행해 필터가 동작하는지 확인

## Phase 2 — 호 단위 수집 (Librarian 워크플로우)

[librarian-ops.md](./references/librarian-ops.md)가 정본입니다.
- 지원 코드: `kud`(Kerygma und Dogma), `evth`(Evangelische Theologie),
  `znw`(ZNW), `zthk`(ZThK) — 그 외 저널은 `--issn` 직접 지정
- 실행 (데이터 원천: **Crossref API** — 스크레이핑 아님, 차단 위험 없음):
  ```bash
  python3 scripts/librarian.py --journal zthk --band 120 --heft 1 --output markdown
  ```
- 출판사 페이지 직접 열람이 필요하면 `.skills/insane-search` 경유.

## 검증·보고

- 레지스트리 변경: 변경 전후 항목 수, 추가된 ISSN, JSON 유효성 결과를 보고합니다.
- 수집: 확보한 호의 논문 수와 메타데이터 표본을 보고하고, 차단 등으로 실패한 부분은
  사유와 함께 명시합니다.
