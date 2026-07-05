# No-Site-Name Rule (전문)

`engine/**`, `waf_profiles.yaml`, `engine/templates/**` 파일에는 **특정 사이트의 도메인/URL/셀렉터/브랜드명을 하드코딩하지 않는다**. (R3 편향 금지의 상세 규칙. `python3 engine/bias_check.py`가 CI 게이트로 강제.)

## 금지

- `"coupang.com": {...}` 같은 사이트별 레지스트리 엔트리
- `if "coupang" in url: ...` 같은 도메인 분기
- WAF 프로파일 `notes`에 특정 사이트 이름이나 경험적 byte 크기 박제

## 허용

- `SKILL.md` / `references/*.md`의 **설명 텍스트**에 사이트 이름 예시 (독자 이해용)
- `Phase 0` 공식 API 인덱스 (플랫폼이 공식 공개한 엔드포인트)
- `observations/*.jsonl` 로그 (append-only 관측 데이터 — 코드 경로에 영향 없음)
- 호출자가 제공하는 `success_selectors`, `user_hint` (현재 호출에만 유효)

## 경계 사례 판단 기준

> "이 엔트리가 다른 사이트에서도 같은 WAF를 쓰면 일반적으로 유효한가?" → YES면 `waf_profiles.yaml`, NO면 runtime hint.

## 새 사이트가 안 뚫릴 때

1. 먼저 `result.trace`에서 어느 phase가 실패했는지 확인
2. 사용자의 `user_hint`로 1회 재시도
3. 반복 성공 패턴이 관측되면 `observations/`에 로그 (아직 자동 기록 없음 — 수동)
4. 3회+ 반복 확인되고 **동일 WAF를 쓰는 다른 사이트에도 유효**하면 `waf_profiles.yaml` 해당 프로파일의 `tls_impersonate_candidates` / `url_transform_order`를 튜닝 (사이트명 절대 넣지 않음)
5. 여전히 안 되면 새 WAF 프로파일 후보 검토 (예: DataDome 세부화, Kasada 등)
