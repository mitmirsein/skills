---
name: theology-pdf-maker
description: >
  Compiles theological Markdown into publication-grade PDF (Brill, Noto
  Serif KR, SBL Hebrew/Greek fonts, SBL layout) with a built-in audit phase
  that scores typesetting and fail-fasts below 80. Use when the user asks to
  turn a theological manuscript or lecture note into a PDF.
  키워드: PDF 변환, 조판, 신학 논문 PDF
version: 1.0.1
status: active
---

# 📚 Theology PDF Compiler Skill (`theology-pdf-maker`)

이 스킬은 한글 신학 논문, 강의안 및 신학 서적 마크다운 원고를 SBL 학술 규격에 맞춰 고품질 PDF 문서로 원클릭 컴파일하는 에이전트 전용 기술입니다. 컴파일 완료 후 **내장 감사 단계(Audit Phase)**가 자동 실행되어 조판 품질을 100점 만점으로 수치화하고, 80점 미만 시 Fail-Fast로 빌드를 기각합니다.

---

## 1. 사용 시점 (When to Use)

- 사용자가 특정 마크다운 노트(신학 텍스트)를 PDF로 변환해 달라고 요청할 때.
- 히브리어, 그리스어 등 고전어 텍스트가 포함된 학술 논문을 조판할 때.
- 한글 폰트 **Noto Serif KR**, 라틴계열 **Brill**, 고전어 **SBL Hebrew / SBL Greek** 폰트를 적용해야 할 때.
- 줄간격 **1.5배**, A4 규격 및 학술 여백 규칙이 일괄 적용된 전문 레이아웃이 필요할 때.

---

## 2. 사용 방법 (How to Use)

```bash
python3 ~/Desktop/MS_Dev.nosync/.skills/theology-pdf-maker/scripts/theology_pdf_compiler.py [마크다운_경로]
```

### 주요 옵션 매개변수
| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `-o, --output` | 입력명.pdf | 출력 PDF 경로 |
| `--fontsize` | `11pt` | 기본 폰트 크기 |
| `--linestretch` | `1.5` | 줄간격 |
| `--margins` | `top=2.5cm, bottom=2.5cm, left=3cm, right=3cm` | 여백 |
| `--paper` | `a4paper` | 종이 규격 |
| `--no-fail-fast` | (미설정) | Audit 점수 < 80이어도 PDF 보존 |
| `--test` | (미설정) | 폰트 정합성 자가진단 |
| `--test-audit` | (미설정) | Audit Phase Fail-Fast 동작 검증 |

---

## 3. 핵심 동작 파이프라인 (Core Pipeline)

```
마크다운 원고
    │
    ▼
[전처리 엔진]
    ├─ YAML 프론트매터 제거
    ├─ Obsidian 위키링크 평탄화([[#H]] → H)
    ├─ 원문자 치환(①~⑳ → (1)~(20))
    ├─ em dash 치환(— → -)
    ├─ 괄호 강조 보정(**〔text〕** → (**text**))
    ├─ 백틱 고전어 추출(Hebrew/Greek 자동 감지)
    ├─ \texthebrew{...} / \textgreek{...} 매크로 래핑
    │
    ▼
[Stage 1] Pandoc MD → LaTeX (.tex)
    └─ csquotes 활성화: 따옴표 → \enquote{}/\enquote*{}
    │
    ▼
[Stage 2] XeLaTeX → PDF
    └─ Brill + Noto Serif KR + SBL Hebrew/Greek 임베딩
    │
    ▼
[Audit Phase] — 자동 실행 (100점 만점)
    ├─ 서체 내장 검사 (40점): pdffonts 기반 4종 폰트 임베딩 확인
    ├─ 누락 글자 검사 (30점): XeLaTeX 로그 Missing character 탐지
    ├─ 레이아웃 경고 검사 (20점): Overfull/Underfull hbox, 미정의 참조
    └─ 전처리 무결성 검사 (10점): 원문자 미치환 잔류 탐지
    │
    ├─ ≥80점: ✅ AUDIT PASSED → PDF 출력 완료
    └─ <80점:  🚫 AUDIT FAILED → Fail-Fast, PDF 삭제
```

---

## 4. 감사 단계(Audit Phase) 상세

### 평가 기준

| 항목 | 만점 | 감점 단위 |
|------|------|-----------|
| 서체 내장 검사 | 40점 | 미임베딩 폰트 1종당 -10점 |
| 누락 글자 검사 | 30점 | Missing character 경고 1건당 -5점 |
| 레이아웃 경고 | 20점 | Overfull/Underfull 2건당 -2점, 미정의 참조 1건당 -2점 |
| 전처리 무결성 | 10점 | 미치환 원문자 잔류 시 -10점 |

### Fail-Fast 동작
- **점수 ≥ 80**: PDF 정상 출력. Audit Report는 콘솔에 항상 표시.
- **점수 < 80**: 생성된 PDF를 삭제하고 에러 코드 반환. `--no-fail-fast` 옵션으로 우회 가능.

### Fail 발생 시 대처 전략
| 문제 | 원인 | 해결 |
|------|------|------|
| 서체 내장 FAILED | 폰트 미설치 | `brew install --cask font-noto-serif-cjk-kr` 등 |
| Missing character 다수 | 폰트 미지원 유니코드 | 해당 문자를 LaTeX 명령으로 대체 |
| Overfull hbox 다수 | 긴 URL/단어 | `\url{}` 사용 또는 개행 추가 |
| 원문자 미치환 | 신규 원문자 범위 | `preprocess_markdown()` circled_map에 추가 |

---

## 5. 폰트 자간 설정 (Typography)

| 서체 | 적용 자간 | 이유 |
|------|-----------|------|
| Brill (라틴/고전어) | `0` (기본값 유지) | 고전어 음소 부호 충돌 방지 |
| Noto Serif KR (한글) | `InterHangul=-0.04em` | 한글 바탕체 지면 밀도 최적화 |

---

## 6. 검증 명령 (Verification)

```bash
# 표준 자가진단 (폰트 임베딩 + 컴파일 파이프라인)
python3 ~/Desktop/MS_Dev.nosync/.skills/theology-pdf-maker/scripts/theology_pdf_compiler.py --test

# Audit Phase Fail-Fast 동작 검증
python3 ~/Desktop/MS_Dev.nosync/.skills/theology-pdf-maker/scripts/theology_pdf_compiler.py --test-audit
```

