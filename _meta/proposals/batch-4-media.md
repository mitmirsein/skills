# 배치 4 구현안 — media 카테고리 (2026-06-12)

12개 전부 A등급 달성. 남은 C등급 0개.

## slide (4.0.0 → 4.0.1) — SPLIT
- 263줄 → 115줄. 1080px 수직 예산 규율 → `references/canvas-and-budget.md`,
  DesignSystem·React 스타터 템플릿·에셋 규칙 → `references/design-and-template.md`.
- 본문에는 호출·사전 질문·테마 가이드·하드 룰·파일 계약·자가검수 체크리스트·안티패턴 유지.
- 검증·보고 절 신설(프리뷰 URL 포함). W09(assets/hero.jpg)는 코드 예시 오탐 — 검증기
  경계 수정으로 해소됨.

## create-slide-from-markdown (1.0.0 → 1.0.1) — 중복 제거
- 165줄 → 146줄. 테마 라벨 목록이 본문에 두 번 존재하던 중복 제거, 테마 설명은 slide
  스킬 가이드로 위임하고 고유 정보(데모 참조 경로 5종)만 압축 유지.

## create-slide-image-prompts (1.0.0 → 1.0.1) — SPLIT
- 161줄 → 101줄. 카테고리 레시피 7종(프롬프트 원형) → `references/category-recipes.md`,
  본문에는 카테고리·용도 표만 유지.

## description 하이브리드화 9건 (패치 범프)
lecture-video-generator(프로젝트 파이프라인 오케스트레이션 명시), remotion-studio,
yt-digest ↔ yt-subtitle-helper(요약 ↔ 자막 교정·업로드 경계), epub-bindery,
pdf-extractor(paper-xray와의 경계: 추출 ↔ 추출+논증 브리핑), hwp-converter,
media-factory, academic-illustrator.
