# Deep Research

출처 삼각검증, 재개 가능한 세션, Claim Ledger, 인용 감사, Markdown 각주 변환을 제공하는 도구 독립적 심층 연구 스킬입니다.

Codex, Claude Code, Gemini CLI처럼 `SKILL.md` 기반 지침과 파일·검색 도구를 사용할 수 있는 에이전트를 대상으로 합니다. 특정 제품의 서브에이전트 API나 권한 우회 옵션을 요구하지 않으며, 병렬 실행을 사용할 수 없으면 동일한 조사 역할을 순차 실행합니다.

## 주요 기능

- 질문 정제부터 패키징까지 이어지는 7단계 연구 파이프라인
- `state.json` 기반 세션 저장, 상태 조회, 중단 후 재개
- 웹·학술·기술·1차 자료를 역할별로 조사하는 능력 기반 오케스트레이션
- 추적 URL 정규화와 출처 레지스트리 중복 제거
- 핵심 주장별 독립 출처, 반증 검색, 1차 자료를 검사하는 Claim Ledger
- 검증·미확정·반박 주장을 분리하는 결정론적 게이트
- 보고서의 출처 ID와 주장 배치를 검사하는 품질 감사
- `[clm_001] [src_001]` 태그를 표준 Markdown 각주로 변환
- Python 표준 라이브러리만 사용하는 실행 스크립트

## 설치

Codex의 기본 스킬 디렉터리에 설치하는 예:

```bash
git clone https://github.com/mitmirsein/deep-research.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/deep-research"
```

다른 에이전트에서는 해당 제품이 사용하는 스킬 디렉터리 안에 이 저장소를 복제하거나 복사합니다. 제품 버전에 따라 발견 경로가 달라질 수 있으므로 해당 에이전트의 스킬 문서를 확인하십시오.

## 사용

다음과 같이 자연어 또는 명시적 스킬 호출로 요청합니다.

```text
$deep-research를 사용해서 AI 코딩 도구가 개발자 생산성에 미치는 영향을 조사해줘.

/deep-research 톨스토이의 성서 해석과 산상수훈 이해를 심층 연구해줘.
```

에이전트는 사용 가능한 검색·브라우징·학술검색·서브에이전트 능력을 탐지하고, 없는 기능은 순차 조사로 대체합니다.

## 연구 흐름

```text
질문 정제
  → 검색 계획
  → 적응형 조사
  → 출처 삼각검증과 Claim Ledger
  → 검증된 주장 중심 합성
  → 품질 감사와 각주 변환
  → 결과 패키징
```

기본 연구 세션은 현재 작업 디렉터리의 `RESEARCH/`에 만들어집니다.

```text
RESEARCH/<topic>_<timestamp>/
├── state.json
├── artifacts/
│   ├── query.json
│   ├── research_plan.json
│   ├── agent-results/
│   └── claim_ledger.jsonl
├── sources/
│   ├── sources.jsonl
│   └── bibliography.md
└── outputs/
    ├── verified_claims.json
    ├── unresolved_claims.json
    ├── refuted_claims.json
    ├── eval_report.json
    ├── report.md
    └── report_footnotes.md
```

## 명령줄 도구

세션 생성:

```bash
python3 scripts/research_session.py init \
  --root RESEARCH --topic "Research topic" --query query.json
```

조사 결과 병합:

```bash
python3 scripts/merge_findings.py \
  --output <session>/sources/sources.jsonl <finding-files...>
```

Claim Ledger 검증:

```bash
python3 scripts/validate_ledger.py --session <session>
```

보고서 감사:

```bash
python3 scripts/evaluate_report.py \
  --session <session> --report <session>/outputs/report.md
```

Claim·Source 태그를 각주로 변환:

```bash
python3 scripts/convert_footnotes.py \
  --session <session> \
  --report <session>/outputs/report.md \
  --output <session>/outputs/report_footnotes.md
```

## 검증

요구사항은 Python 3.10 이상입니다. 런타임 외부 패키지는 필요하지 않습니다.

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
```

Ruff가 설치된 개발 환경에서는 다음 검사도 실행할 수 있습니다.

```bash
ruff format --check scripts evals
ruff check scripts evals
```

## 한계와 안전

- 자동 감사는 출처·주장 ID의 정합성을 검사하지만, 인용이 문장을 의미론적으로 지지하는지 완전히 증명하지는 않습니다.
- 검색 스니펫이나 AI 요약을 원문 확인으로 취급하지 마십시오.
- 의료·법률·재무·규제 연구는 최신 1차 자료와 전문가 검토가 추가로 필요합니다.
- 미확정 또는 반박된 주장을 삭제해 품질 점수만 높이지 말고 보고서의 전용 절에 남기십시오.

## 헌정 및 감사 (Acknowledgements)

이 프로젝트는 [fivetaku](https://github.com/fivetaku) 님이 Claude Code용 멀티 에이전트 심층 연구 플러그인으로 최초 개발한 [fivetaku/insane-research](https://github.com/fivetaku/insane-research)를 기반으로, 도구 독립적(Tool-Agnostic)이고 범용적인 딥리서치 스킬로 독자 확장한 개작 버전입니다.

원작 프로젝트는 7단계 연구 워크플로우, 세션 재개 메커니즘, 출처 품질 평가(A–E 등급), 주장 검증 장부(Claim Ledger) 등 본 프로젝트의 훌륭한 영감이 된 핵심 아키텍처를 제시했습니다. 원작자의 저작권 표기와 MIT 라이선스는 [LICENSE](LICENSE) 및 [references/upstream-license.md](references/upstream-license.md)에 보존되어 있습니다.

뛰어난 원작 프로젝트를 공개해 주신 fivetaku 님께 깊이 감사드립니다. 본 저장소는 `mitmirsein`에 의해 독립적으로 유지보수되며, 원작자와의 직접적인 제휴 관계는 없습니다.

## License

MIT License. 자세한 내용은 [LICENSE](LICENSE)을 참조하십시오.
