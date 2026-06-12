# 🩻 paper-xray: 고정밀 논문 추출 및 투시 분석 파이프라인

[![Python Unit Tests](https://img.shields.io/badge/tests-33%20passed-success)](https://github.com/mitmirsein/th_battleground)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

`paper-xray`는 학술 PDF나 스캔본 문서로부터 텍스트를 고정밀로 추출하고, 불필요한 파싱 노이즈를 교정한 후, 논문의 뼈대(Skeleton)와 핵심 논지를 신속하게 추출하는 **AI 에이전트 전용 통합 분석 스킬 프로젝트**입니다. 

기존의 단순 요약기들과 다르게 저자의 핵심 논리 위상(Topology)과 학술 대립 전선(Battleground)을 발라내는 고유한 인지적 헌법을 내장하고 있습니다.

---

## 📂 프로젝트 구조 (Architecture)

관심사의 명확한 분리를 위해 **설계도(SKILL.md), 헌법(constitution.md), 템플릿(templates.md), 실행 스크립트(scripts/)**로 구조화되어 있습니다.

```text
paper-xray/
├── README.md            # 본 소개 문서
├── SKILL.md             # [설계도] 에이전트 인터페이스 및 파일 계약서 (상대경로 링킹)
├── constitution.md      # [독해 헌법] SSOT (매의 눈 독해 휴리스틱, 스캔 정직성)
├── GEMINI.md            # 🔗 constitution.md 심볼릭 링크
├── CLAUDE.md            # 🔗 constitution.md 심볼릭 링크
├── AGENTS.md            # 🔗 constitution.md 심볼릭 링크
├── Agents.md            # 🔗 constitution.md 심볼릭 링크
├── requirements.txt     # opendataloader-pdf, pypdf 의존 패키지
├── scripts/             # 물리 파이프라인 파이썬 코드군
│   ├── preflight.py      # 1단계: 사전 진단 (Triage)
│   ├── extract_pdf.py    # 2단계: 하이브리드/일반 추출 (Core)
│   ├── post_cleaner.py   # 3단계: 1차 Spalte/단어 하이픈 복원
│   ├── healer.py         # 3단계: 괄호/각주 격리 지능형 교정
│   ├── vision_extractor.py # 2단계: 이미지-to-마크다운 비전 OCR
│   └── vision_to_json.py # 2단계: 시맨틱 레이아웃 JSON 골격 생성
├── tests/               # 교정기 무결성 단위 테스트
│   ├── test_extract_pdf.py
│   ├── test_healer.py
│   └── test_post_cleaner.py
└── references/
    ├── gotchas.md       # 실행 예외 및 하드웨어 충돌(Intel Mac) 함정 가이드
    └── templates.md     # X-Ray 브리핑 최종 마크다운 양식 및 Worked Example
```

---

## ⚙️ 의존성 및 요구사항 (Prerequisites)

* **Python 3.10+** 및 **`uv` 패키지 매니저** 권장
* **외부 라이브러리:** `pip install -r requirements.txt` 로 설정
  - `opendataloader-pdf>=2.0.2` (추출 엔진)
  - `pypdf>=6.10.0` (사전 진단용)

> [!WARNING]
> **Intel Mac(2017 iMac 등) 주의사항:** 
> opendataloader-pdf의 PyTorch 의존성이 Intel Mac CPU 아키텍처 환경에서 충돌할 수 있습니다. 충돌이 발생할 경우 일반 모드(`--hybrid` 미사용)로 가볍게 우회하여 수행하십시오. ([gotchas.md](./references/gotchas.md) 참조)

---

## 🚀 설치 및 사용법 (Quick Start)

### 1. 에이전트 스킬 장착
원격 깃허브 저장소에서 자신의 에이전트 글로벌 스킬 디렉토리에 복제합니다.
```bash
git clone https://github.com/사용자/paper-xray.git .skills/paper-xray
```
*(Git은 심볼릭 링크 구조를 완벽하게 보존하여 다운로드하므로 파일 깨짐 걱정이 없습니다.)*

### 2. 포맷별 라우팅 가이드
에이전트는 입력 문서 확장자에 맞춰 최적의 리소스를 사용하도록 파이프라인을 자동 분기합니다.

| 입력 포맷 | 단계별 처리 경로 | 설명 |
| :--- | :--- | :--- |
| **PDF** | `[1단계 Triage]` ➡️ `[2단계 Extraction]` ➡️ `[3단계 Healing]` ➡️ `[4단계 X-Ray]` | 표준 4단계 전체 프로세스를 따르며, 최종 브리핑 파일도 생성합니다. |
| **DOCX** | `[Pandoc/CLI 변환]` ➡️ `[4단계 X-Ray]` | `.md` 확보 후 곧바로 4단계로 진입하며, **최종 브리핑 결과물을 `{논문명}_xray.md`로 물리 저장**합니다. |
| **MD / TXT** | `[4단계 X-Ray]` (즉시 분석 ➡️ 파일 저장) | 1~3단계를 생략하고 즉시 4단계 분석을 가동하며, **최종 브리핑 결과물을 `{논문명}_xray.md`로 물리 저장**합니다. |

---

## 🏆 핵심 파이프라인 및 명령어

### [1단계] 사전 진단 (Triage)
추출 전 첫 3페이지의 노이즈 밀도를 스캔하여 Core(텍스트) 또는 Vision(시각 지능) 경로를 판정합니다.
```bash
uv run python scripts/preflight.py <PDF_PATH> --json
```

### [2단계] 추출 (Core Mode)
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --page-markers
```
*결과물은 `output/{논문명}/` 서브디렉토리에 깔끔하게 고립되어 생성됩니다. `--page-markers`는 `===== p.N =====` 마커가 박힌 `{논문명}_paged.md`를 생성하므로 연구 인용과 TKG 전달에 적합합니다.*

### [3단계] 지능형 구조 교정 (Healing & Audit)
```bash
# 1. 분철된 단어 결합 및 Spalte 1차 정제
uv run python scripts/post_cleaner.py output/{논문명}/{논문명}_paged.md

# 2. 괄호 스택 매칭 및 고아 각주 분리, Deletion Audit Report 발행
uv run python scripts/healer.py output/{논문명}/{논문명}_paged_cleaned.md --report
```
최종 X-Ray와 TKG `input/<source>/`에는 `{논문명}_paged_healed.md`를 넘기는 것을 권장합니다.

### [4단계] X-Ray 분석 및 물리적 파일 자동 보존
위 과정에서 확보된 `_paged_healed.md` 문서를 바탕으로 에이전트 독해 헌법([constitution.md](./constitution.md))에 의거한 예리한 X-Ray 브리핑을 채팅창에 출력하고, 동시에 **`output/{논문명}/{논문명}_xray.md` 파일로 디스크에 강제 저장**합니다.

---

## ⚖️ 최상위 헌법 규약 (Single Source of Truth)

에이전트는 최종 요약을 출력하기 전 [constitution.md](./constitution.md)의 5대 규칙을 성실히 자문합니다.
1. **스캔 정직성:** 확인되지 않은 서지 정보와 년도는 절대 추측하여 날조하지 않고 `[미확인]`으로 비워둔다.
2. **현학성 박리:** 저자의 수식어를 걷어내고 드라이한 핵심 주장(Claim) 한 줄만 도출한다.
3. **위상 변화 추적:** 단순 목차 요약을 금지하고, 논리가 단계별로 고도화되는 위상 변화를 적는다.
4. **학술 전선도:** 누구를 무너뜨리기 위해(Antagonist), 누구의 학설(Allies)을 무기로 차용했는지 전쟁 구도로 파악한다.
5. **이중 교량:** 이 논문의 미시적 기여(1인치)와 현대인의 삶/실존으로의 다리를 각각 건설한다.

---

## 🛡️ License
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자유롭게 포크하고 기여해 주십시오!
