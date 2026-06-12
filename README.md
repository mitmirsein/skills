# 🧩 MS_Dev Agent Skills Library

이 디렉토리는 **Agent Skills** 프로토콜에 따라 정의된 에이전트 스킬들을 모아두는 곳입니다.
에이전트에게 "OOO 스킬을 사용해줘"라고 요청하면, 에이전트가 해당 폴더의 `SKILL.md`를 읽고 수행합니다.

## 📂 구조

```text
.skills/
├── STANDARDS.md      # 스킬 표준 헌장 (규범 — 모든 스킬이 따라야 함)
├── INDEX.md          # 전체 스킬 인덱스 (validate.py --index로 자동 생성)
├── _template/        # 새 스킬 템플릿 (복사해서 시작)
├── _meta/            # 거버넌스: validate.py(검증기), AUDIT.md, TRIAGE.md, PROGRESS.md
└── [스킬명]/
    ├── SKILL.md      # [필수] 에이전트 행동 지침
    ├── references/   # [옵션] 상세 문서 (gotchas.md 권장)
    ├── scripts/      # [옵션] 실행 코드
    └── assets/       # [옵션] 정적 데이터
```

## 🚀 새 스킬 만들기

1. `_template/`를 복사해 kebab-case 이름으로 변경
2. `SKILL.md` frontmatter와 본문을 `STANDARDS.md` 규범에 맞게 작성
3. `python3 _meta/validate.py <스킬명>` 으로 검증 통과 확인
4. `python3 _meta/validate.py --index` 로 INDEX.md 갱신

## ⚠️ 핵심 규칙 (위반 시 다른 머신에서 고장)

- 절대경로 `/Users/<이름>/...` 하드코딩 금지 — md/json은 `~/`, Python은 `os.path.expanduser`
- 심링크는 상대경로만
- 스킬 폴더 안에 `.venv`, `node_modules`, 대용량 산출물 금지
- 자세한 규범: `STANDARDS.md`
