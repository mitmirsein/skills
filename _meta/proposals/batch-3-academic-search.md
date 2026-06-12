# 배치 3 구현안 — academic-search 카테고리 (2026-06-12)

16개 전부 A등급 달성 (notebooklm은 빈 폴더로 판명되어 제거 — 17→16개).

## insane-search (1.0.0 → 1.1.0) — SPLIT + 재분류
- 346줄 → 105줄. 하네스 규칙 R1~R7은 본문 보존(고삐 기능), Phase 0 API 색인+빠른 명령
  → `references/phase0-api-index.md`, 격자·폴백·MCP 규칙·R7 근거 → `fetch-chain-guide.md`,
  No-Site-Name Rule → `no-site-name-rule.md`, 참조 내비게이션 → `reading-guide.md`.
- 폐기된 kci-searcher 참조 8곳 → kci-api-searcher로 교체. kci.md의 2단계 `--detail` 흐름은
  단일 호출(초록 포함)로 재작성 (kci-api-searcher에 --detail 없음 — 기능 정합성 교정).
- 분류 academic-search → **dev-tools** (실체는 범용 웹 차단 우회 엔진).

## notebooklm-researcher (3.2.0 → 3.2.1) — 소프트캡 분할
- 190줄 → 99줄. 인라인 보고서 템플릿 → 기존 templates/research-report-template.md 포인터로,
  6축 상세 → 기존 plan-mode-guide.md 포인터로. 검증·보고 절 신설([미확인] 표기 규칙).

## description 하이브리드화 11건 (패치 범프)
crossref-journal-searcher, google-scholar-quick/semantic(상호 경계 명문화: 빠른 리스트 ↔
인용 심층), ixtheo-searcher, nlk-biblio/interlinker/subject(파이프라인 순서 명문화),
semantic-scholar(S2 API ↔ 브라우저 GS 경계), paper-xray, riss-searcher, tawp.

## 결함 교정
- semantic-scholar: 실재하지 않는 `triple_researcher.py` 언급 → 실제 파일 `legacy_researcher.py`.
- riss-searcher: 빈 .venv 껍데기 제거(0바이트), JSON 예시 압축으로 150줄 준수.
- notebooklm/: .DS_Store뿐인 빈 폴더 확인 후 제거 (MERGE? 안건 자연 해소).

## journal-collector (신규 1.0.0)
- 자산 명시: theology/economics_journals.json은 crossref-journal-searcher가 소비하는 ISSN 세트.
- 레지스트리 관리 절차(Crossref 검증→스키마 추가→표본 검색) + Librarian 호 수집.
- ⚠️ agents/librarian.py 부재 정직 표기.

## 검증기 개선
- W09 경로 경계 앵커(외부 절대경로 내부 부분매칭 오탐 제거), deprecated 스킬 형식 경고 면제.
