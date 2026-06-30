# KCI (한국학술지인용색인) API 접근

> KCI 포털은 dynamic content가 많고 접근 제어가 있을 수 있으므로, API 키가 설정된 전용 `kci-api-searcher` 스킬 CLI를 우선 활용한다.

## 0. API 키

개발 워크스페이스 `.env`에 KCI 키가 설정되어 있다.

- `KCI_OPEN_API_KEY`: KCI 포털 직접 OpenAPI 키. `open.kci.go.kr` articleSearch 권위검색용.
- `KCI_API_KEY`: data.go.kr 계열 KCI/NLK OpenAPI service key.

키 값은 출력하거나 응답에 노출하지 않는다. CLI 실행 시 `.skills/kci-api-searcher`가 필요한 키를 환경에서 읽도록 한다.

## 1. 전용 스킬 CLI 접근

KCI 논문 검색 및 초록 조회는 `.skills/kci-api-searcher/scripts/search.py`를 호출한다.

### 제공되는 명령

```bash
uv run python .skills/kci-api-searcher/scripts/search.py "<keyword>" --limit 10 --output markdown
uv run python .skills/kci-api-searcher/scripts/search.py "<keyword>" --limit 5 --output json
```

- 검색 1회 호출이 저자·소속·학술지·DOI·**초록**까지 통합 반환한다
  (구 kci-searcher의 2단계 `--detail` 조회는 폐기 — 더 이상 필요 없음).

## 2. 접근 전략

1. **Phase 0 (직접 검색)**: 사용자의 검색어 및 의도(저자, 학술지, 주제어)에 따라 `kci-api-searcher` CLI를 호출 — 초록 포함 전체 메타데이터를 1회에 수집.
2. **Phase 1 (Fallback)**: KCI 포털 구조 변경이나 서버 문제로 검색 결과가 없는 경우, 브라우저 렌더링 방식의 별도 확인을 검토한다.

## 3. 주요 유의사항
- **Rate Limit**: 단일 세션에서 과도한 호출은 지양하고 필요한 핵심 논문에 집중한다.
- **Fallback**: API/CLI가 실패할 때만 일반 웹 접근 또는 브라우저 렌더링을 검토한다. KCI 검색은 Phase 0에서 공개 API 경로가 우선이다.
