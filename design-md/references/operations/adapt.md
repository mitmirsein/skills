# 동사: adapt — 반응형·멀티타깃 출력

같은 디자인 의도를 화면 크기와 **출력 매체**에 맞게 적응시킨다. 출력 타깃은 shape 단계에서 정해진다.

## 반응형 (화면)
- **Mobile-First**: 기본 스타일은 모바일, `min-width` 미디어쿼리로 확장.
- 브레이크포인트는 콘텐츠 기준(레이아웃이 깨지는 지점)으로. 고정 기기명 추종 X. 권장 시드: 640 / 768 / 1024 / 1280.
- 유동 타이포·간격: `clamp()` 활용(`font-size: clamp(1rem, 0.9rem + .5vw, 1.25rem)`).
- 터치 타깃 ≥ 44×44px, 호버 의존 기능에 터치 대체 제공.
- `<meta name="viewport">` 필수. 컨테이너 쿼리(`@container`)는 컴포넌트 단위 반응형에 적극 사용.

## 출력 타깃 규약
- **HTML / React**: 시맨틱 태그, 토큰은 CSS custom properties, 컴포넌트는 시맨틱 색 토큰만 참조.
- **인쇄(PDF)**: [print-grade.md](./print-grade.md)로 위임 — `@page`, 금칙, 각주.
- **Obsidian-native** (창발: 볼트 상시 활용):
  - 인라인 스타일 대신 **callout**(`> [!note]`, `> [!quote]`)과 vault CSS snippet을 우선.
  - 폰트·색은 `.obsidian/snippets/`에 둘 CSS로 제안하고, 노트 본문은 Markdown 의미구조 유지(헌법: 위키링크·임베드·frontmatter 보존).
  - 표·다이어그램은 Mermaid/Dataview 친화적으로. 외부 폰트 임포트는 사용자 승인 후.

## 함정
- `max-width` 미디어쿼리(Desktop-First) 혼용 → 캐스케이드 충돌.
- Obsidian 출력에 무거운 인라인 `<style>` 박기 → 볼트 오염. snippet로 분리.
