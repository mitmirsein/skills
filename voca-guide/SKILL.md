---
name: voca-guide
description: >
  Builds a high-quality vocabulary textbook PDF (13-step storyline
  card-news format, light mode) from a word list or source text. Use when
  the user asks to create vocabulary teaching material or a voca card-news
  PDF. 키워드: 어휘 교재, 단어 카드뉴스, 보카 PDF
version: 1.0.1
status: active
---

# Voca Guide Skill

## When to use this skill
* 사용자가 영어 어휘 목록, 교과서 텍스트(예: YBM Lesson 1 등), 혹은 기출 단어 PDF를 주고 "카드뉴스 교재로 만들어줘", "어원 분석 자료집 PDF 뽑아줘"라고 요청할 때 사용합니다.
* 어휘 분석 시, 라틴어/그리스어 어근 원형과 뜻을 명확히 대조하고, 다의어의 물리적 뜻과 추상적 뜻을 연결해주는 인과적 논리 서사(13단계)를 빌드하여 학습용 PDF로 자동 컴파일해야 할 때 유용합니다.

## How to use it

### Phase 1: 단어 데이터베이스 구축
1. 사용자의 타겟 단어(예: 40개 단어 등)를 수집하거나, 본문 텍스트에서 주요 어휘를 추출합니다.
2. 각 단어마다 다음 13단계 정보를 포함한 상세 데이터셋(`vocab_data.json`)을 구축합니다. (필요 시 `cts/generate_vocab_data_complete.py` 패턴 참조)
   * `word`: 표제어
   * `pronunciation`: 발음기호 (예: `KAHM-pruh-myz`)
   * `meaning1`: 물리적/일반적인 뜻
   * `meaning2`: 추상적/비유적인 전이 뜻
   * `intro`: 흥미를 끄는 질문형 인사말
   * `etymology`: 어근 분해 및 흐름 정보
   * `examples1`: 첫 번째 뜻에 대응하는 영어 예문 2개 및 한국어 대역
   * `transition_question`: 의미가 어떻게 2번째 뜻으로 확장되는지에 대한 징검다리 질문
   * `logic_flow`: 단계별 변화 흐름 (배열)
   * `logic_desc`: 변화에 대한 인과 설명 핵심 요약
   * `examples2`: 두 번째 뜻에 대응하는 영어 예문 2개 및 한국어 대역
   * `feeling`: 단어 고유의 핵심 뉘앙스/이미지 (Core Image)
   * `real_tip`: 수능/내신 시험/뉴스 등에서의 실전 꿀팁
   * `summary_flow`: 어원에서 최종 의미까지 꼬리에 꼬리를 무는 빌드업 시퀀스
   * `quiz`: 본문에 맞춤 적용된 2문항 빈칸 채우기 퀴즈 및 정답

### Phase 2: 라틴어 어근 맵핑 및 템플릿 처리
1. 어원 카드(4번 카드) 렌더링 시, 라틴어(`L.`), 그리스어 (`Gk.`), 고대영어(`OE.`) 원어와 의미를 반드시 명기합니다.
   * 예시: `e- (L. ex- : out of / 벗어남)` + `norm (L. norma : rule, standard / 규격, 기준)`
2. `cts/build_vocab_html.py` 내의 `latin_etymologies` 맵핑 테이블을 참조하여, 새 단어 추가 시에 해당하는 라틴어 원어 정보를 매칭 사전에 업데이트합니다.

### Phase 3: 라이트 모드 HTML 및 PDF 렌더링
1. `build_vocab_html.py`에 구현된 **Premium Lightmode (Luxury Cream & Pastel Shadow)** CSS 테마를 기반으로 HTML을 동적 뿜어냅니다.
   * `body` 배경: `#f7f6f3` (고급 진주/크림 웜 화이트 미색)
   * 카드 배경: `rgba(255, 255, 255, 0.85)` (글래스모피즘)
   * 포인트 보더: 질문(`Amber`), 어휘(`Sky/Indigo`), 퀴즈(`Pink/Purple`)
2. Playwright의 chromium 인쇄 엔진을 기동하여 A4 1페이지당 1단어(13개 카드뉴스 타일 배치) 규격으로 PDF 출력을 컴파일합니다.
   * 폰트 및 리소스 렌더링을 완전히 보장하기 위해 `wait_for_load_state("networkidle")` 및 최소 `3000ms`의 명시적 `sleep` 대기를 거친 뒤 PDF를 저장합니다.

## Verification & Audit

1. **품질 검사기(Audit Harness) 구동**:
   * 빌드 전에 `scripts/audit_harness.py`를 실행하여 데이터 무결성을 검증합니다.
   * 명령어: `python3 audit_harness.py <vocab_data_lessonX.json>`
   * 에러(Error)가 발생하면 빌드가 자동으로 중단되며, 경고(Warning)는 가급적 0개로 수렴되도록 데이터 분량과 어투를 조율하는 것이 권장됩니다.
2. **문체 및 어투 보증**:
   * 한글 설명부(`intro`, `logic_desc`, `feeling`, `real_tip`)가 딱딱한 격식체(`~입니다`, `~했습니다`)가 아닌 친근한 과외식 구어체 반말(`~이지`, `~했어` 등)인지 검사합니다.
3. **오버플로우 방지 및 규격 검수**:
   * 각 설명부의 글자 수 임계치(`logic_desc` 150자, `real_tip` 200자, 예문 100자 등)를 준수하여 오버플로우가 나지 않는지 확인합니다.
   * `pdfinfo` 도구를 통해 최종 생성된 PDF의 페이지 수가 단어 개수(40페이지)와 정확히 일치하며 A4 용지 규격인지 물리적으로 확인합니다.
