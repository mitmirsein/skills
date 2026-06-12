# Hybrid Browser Swarm Guide

브라우징 작전의 효율성과 기밀성을 극대화하기 위한 두 가지 엔진의 병행 운용 수칙입니다.

## 🐎 Lightpanda (고속 정찰 엔진)
**용도**: 빠른 정보 수집, 대규모 스크래핑, 브라우저 핑거프린트가 중요하지 않은 공통 데이터 검색.

- **장점**: 엄청난 속도(Zig 기반), 적은 메모리 사용, AI 전용 Semantic Tree 내장.
- **MCP 명령**:
  - `lightpanda.goto(url)`: 정찰 지점 이동.
  - `lightpanda.semantic_tree()`: 고효율 AI 요약 트리 획득.
  - `lightpanda.markdown()`: 페이지 마크다운 추출.

## Stealth Browser (정밀 브라우저 엔진)
**용도**: 사용자 로그인 필요 작업, 복잡한 웹 애플리케이션 조작, 화이트리스트 기반 세션 유지.

- **장점**: 실제 크롬 프로필 및 쿠키 연동, 100% 웹 API 호환성.
- **포팅된 기능**: `scripts/semantic-summary.js`를 통해 브라우저 세션에서도 Lightpanda 스타일의 고화질 요약 트리를 사용할 수 있습니다.

## 🔄 워크플로우 (Swarm Logic)

1. **[Recon Phase]**: 먼저 `lightpanda`를 투입하여 대규모 검색 및 정찰을 수행합니다. (자원 소모 최소화)
2. **[Identification]**: 추가적인 조작이나 사용자 권한이 필요한 페이지를 식별합니다.
3. **[Infiltration Phase]**: 특정 타겟에 대해서만 `stealth-browser`를 기동하여 정밀 조작을 수행합니다.

## 🛠️ Tip: Semantic Tree 사용하기
기존 `read_browser_page` 대신 `lightpanda.semantic_tree()`를 사용하면 토큰 사용량을 70% 이상 절감하면서도 AI의 요소 식별 정확도를 높일 수 있습니다.
