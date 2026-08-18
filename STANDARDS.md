# MS_Dev 스킬 표준 헌장 (Skill Standards Charter)

버전: 1.0.0 / 제정: 2026-06-12

이 문서는 `.skills/` 라이브러리의 모든 스킬이 따라야 할 규범이다.
새 스킬 생성·기존 스킬 개선 시 이 헌장과 `_meta/validate.py` 검증을 통과해야 한다.

---

## 1. 디렉토리 구조

```text
[skill-name]/                # kebab-case, 영문 소문자
├── SKILL.md                 # [필수] 에이전트 행동 지침
├── references/              # [선택] 상세 문서 — gotchas.md, 스키마, 프로토콜 등
├── scripts/                 # [선택] 실행 코드 (Python/JS/shell)
├── templates/               # [선택] 출력 템플릿
├── assets/                  # [선택] 정적 데이터
└── evals/                   # [선택] 평가·테스트
```

- 스킬 폴더 안에 `.venv`, `node_modules`, 대용량 `output/` 산출물을 두지 않는다.
  (작업 산출물은 스킬 밖 작업 폴더로, venv는 §5 참조)

## 2. Frontmatter 스키마

```yaml
---
name: skill-name              # [필수] 디렉토리명과 동일 (kebab-case)
description: >                # [필수] 하이브리드 형식 — §3 참조
  ...
version: 1.0.0                # [필수] SemVer만. 세대명/코드명 금지
status: active                # [필수] active | stub | deprecated
author: MS_Dev                # [선택]
triggers:                     # [선택] 호출 패턴
  - "/skill-name"
capabilities: []              # [선택]
references_path: ./references # [선택] references/ 있으면 명시
---
```

- `version`에 `3.0.0 (Third Gen)` 같은 라벨 금지. 코드명이 필요하면 본문 첫 절이나
  `codename:` 별도 필드에 둔다.

## 3. description 형식 (하이브리드 정책)

**영어 "Use when..." 문장 + 한국어 트리거 키워드 병기.** 에이전트 매칭 안정성(영어)과
사용자 호출 어휘(한국어)를 동시에 충족한다.

```yaml
description: >
  Searches KCI (Korea Citation Index) via official OpenAPI and returns
  verified article metadata. Use when the user asks for Korean academic
  papers, KCI search, or domestic journal lookup.
  키워드: KCI 검색, 한국 학술논문, 국내 저널 조회
```

규칙:
- 1문장째: 무엇을 하는가 (3인칭 현재형)
- 2문장째: `Use when ...` — 언제 쓰는가
- 마지막: `키워드:` 한국어 트리거 단어 3~6개
- 전체 1024자 이내

## 4. SKILL.md 본문 규칙

- **본문 언어: 한국어** (코드·명령 예시는 원어 그대로)
- **분량: 150줄 권장, 200줄 절대 상한.** 초과분은 `references/`로 분리하고
  본문에는 "어떤 파일을 언제 읽어라"만 남긴다 (progressive disclosure).
- 권장 골격:
  1. `# 스킬명` + 한 줄 요약
  2. `## Phase 0 — 가드레일`: 시작 전 반드시 읽을 references (특히 `gotchas.md`)
  3. `## Phase 1..N — 실행 절차`
  4. `## 검증·보고`: 무엇을 확인하고 어떻게 보고하는가
- 다른 스킬을 참조할 때는 `.skills/<skill-name>` 상대 경로 표기.

## 5. 경로 이식성 (듀얼 맥 + Syncthing — 위반 시 즉시 고장)

이 라이브러리는 사용자명이 다른 두 Mac(M1 Air / Intel iMac) 사이를 Syncthing으로
오간다. **절대 경로 `/Users/<이름>/...` 하드코딩은 전면 금지.**

| 위치 | 올바른 형태 |
|---|---|
| Markdown 산문·예시 | `~/Desktop/MS_Dev.nosync/...` (`~` 표기) |
| Python | `Path(__file__).resolve().parents[N]` 앵커링, 또는 `Path.home() / "Desktop/..."` |
| Shell | `"$HOME/Desktop/..."` |
| JSON 설정 | `~/...` 표기 후 읽는 쪽에서 `expanduser` |
| 심링크 | **상대 경로만** (예: `../../MS_Thoughts.nosync/.skills/wiki`) |

- venv: 스킬/저장소 트리 안에 두지 않는다. 필요 시 머신별 분리(`.venv-m1`,
  `.venv-intel`)와 `.stignore` 등록 후 사용 (워크스페이스 헌법 준수).

## 6. 스크립트 표준

- 파일 머리에 모듈 docstring으로 **용도 / 의존성 / 실행법** 1~3줄 명시.
  ```python
  """KCI OpenAPI 검색. deps: requests. 실행: uv run scripts/search.py <질의어>"""
  ```
- API 키·자격증명은 **환경변수로만** 받는다. 키 값 하드코딩 금지.
  `.env` 파일을 언급할 때도 `~/` 표기.
- 패키지 설치 가드레일(릴리스 7일 지연 등 워크스페이스 헌법)을 따른다.

## 7. 중복·수명 관리

- 같은 대상을 다루는 스킬이 둘 이상이면 `_meta/TRIAGE.md`에 MERGE 후보로 기록하고
  **사용자 승인 후** 통합·폐기한다. 임의 삭제 금지.
- 폐기 결정된 스킬은 즉시 삭제하지 않고 `status: deprecated` + 본문에 대체 스킬
  안내를 남긴 뒤, 한 배치 주기 후 제거한다.
- 골격만 있는 스킬은 `status: stub`으로 정직하게 표기한다.

## 8. 최고 수준 스킬 체크리스트

스킬을 "완성(A등급)"으로 선언하려면 전부 충족:

- [ ] frontmatter: name(=디렉토리명)/description(§3 형식)/version(SemVer)/status 존재
- [ ] SKILL.md ≤ 150줄, 본문 한국어, Phase 골격
- [ ] `references/gotchas.md` 존재 (함정·실패 사례 1개 이상 기록)
- [ ] 본문이 참조하는 모든 파일이 실제로 존재
- [ ] 절대 사용자 경로 0건 (스킬 전체 파일 기준)
- [ ] 스크립트마다 의존성·실행법 docstring
- [ ] API 키 환경변수화, 자격증명 하드코딩 0건
- [ ] 실존하지 않는 모델명·API·도구 언급 0건
- [ ] 검증·보고 절차가 본문에 명시됨
- [ ] `_meta/validate.py` 오류 0건

## 9. 검증 도구

```bash
python3 .skills/_meta/validate.py            # 전체 감사 → _meta/AUDIT.md 갱신
python3 .skills/_meta/validate.py <skill>    # 단일 스킬 검사
```

- `gws/`(외부 유래 묶음)와 `_meta/`, `_template/`은 등급 산정에서 제외된다.
- 심링크 스킬(wiki 등)은 링크 무결성만 검사하고 본체는 원본 위치에서 관리한다.
