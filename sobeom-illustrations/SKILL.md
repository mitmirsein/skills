---
name: sobeom-illustrations
version: 1.0.0
status: active
description: Generate Sobeom-style hand-drawn article illustrations. Use when the user wants to create concept graphics, blog illustrations, workflow diagrams, or metaphor sketches in Korean or English — using the 소범(Sobeom) IP, pure white background, minimal hand-drawn line art, sparse red/orange/blue annotations, and a clean absurd product-sketch aesthetic. 키워드: 소범 일러스트, 손그림 삽화, 개념 그래픽, 블로그 삽화, 소범 그림, sobeom illustration, hand-drawn diagram.
---

# Sobeom (소범) Hand-Drawn Illustrations

## 스킬 시작 방법

**Claude Code / Codex / Claude 채팅 모두 동일하게 작동합니다.**

### 기본 시작

슬래시 커맨드로 작동:
```text
/sobeom-illustrations
```
혹은 직접 파일 읽기 명령으로 실행:
```text
~/.gemini/config/skills/sobeom-illustrations/SKILL.md 읽고 실행해줘
```
그 다음 분석할 텍스트, 블로그 포스트, Notion 페이지 본문, 혹은 시각화하고 싶은 주제를 대화방에 붙여넣기 하면 작동을 개시합니다.

---

## 핵심 포지션

글이나 콘텐츠의 핵심 판단, 흐름, 구조, 상태, 은유(Metaphor)를 16:9 가로형 손그림 삽화로 변환합니다. 정형화된 PPT 인포그래픽이나 귀여운 이모티콘 포스터가 아닌, **"절제되고 엉뚱하며 해학적인 손그림 설명도"**를 지향합니다.

* **기본 캐릭터: 소범 (Sobeom)**
  * 외모: 하얗고 둥근 얼굴, 쫑긋 솟은 귀 2개, 얼굴과 이마의 서너 개 줄무늬, 무표정하고 맹하게 동그란 두 눈, 가느다란 스틱 형태의 몸과 팔다리.
  * 소품: 머리에 전통 검은색 갓(Gat)을 비스듬히 쓰고 있습니다.
  * 조건: 소범이는 단순 장식이 아닌 삽화 내부 **핵심 동작의 주체**여야 합니다.
* **기본 언어**: 한국어 또는 영어. 사용자의 작업 컨텍스트에 맞춰 주석과 레이블을 작성합니다.

---

## 필수 참조 가이드

작업 목적에 따라 필요한 레퍼런스를 수시로 읽어 참조하십시오.

- `references/style-dna.md`：여백, 선화 굵기, 3색 주석 사용법 및 금기 사항.
- `references/sobeom-ip.md`：소범이 IP의 정서, 동작 라이브러리 및 디자인 금기.
- `references/composition-patterns.md`：구도 타입 및 상황별 독창적 은유(Metaphor) 설계법.
- `references/prompt-template.md`：나노 바나나 프로(Nano Banana Pro)용 이미지 생성 프롬프트 템플릿.
- `references/qa-checklist.md`：삽화 생성 후 검증 및 반복 수정 규칙.

---

## 에이전트 워크플로우 (Workflow)

### 1. 콘텐츠 이해 및 뉘앙스 파악
제시된 본문을 꼼꼼히 읽고 핵심 개념, 반전이 일어나는 문단, 시각적 설명이 들어갔을 때 효과적인 "인지적 앵커 포인트"를 식별합니다. 평균적으로 고르게 배치하지 않고 중요한 논리적 지점들에 집중 배치합니다.

### 2. 삽화 설계 전략 (Shot List) 수립
사용자가 기획이나 전략 구성을 먼저 물었을 때, 이미지 생성을 멈추고 샷 리스트를 제안합니다. (짧은 글 1~3장, 긴 글 4~8장)
* 어느 문단 뒤에 배치할지
* 삽화의 주제
* 핵심 의미와 구도 타입
* 소범이가 그림 안에서 하고 있는 구체적인 엉뚱한 행동
* 삽화 내에 손글씨로 쓰여질 한국어/영어 레이블 (2~5단어 이내)

### 3. 단장 이미지 생성 (Image Generation)
사용자가 생성을 지시하면, 멈추지 않고 내장된 `generate_image` 툴을 사용해 각 삽화를 1장씩 순차적으로 생성합니다. 프롬프트에 다음 필수 구성 요소를 보장합니다:
* 16:9 가로형 삽화 (16:9 horizontal illustration)
* 순백색 배경 (Pure white background)
* 거친 느낌의 얇은 검정 손그림 선화 (Minimalist wobbly black hand-drawn line art)
* 갓을 쓴 하얀 호랑이 캐릭터 '소범(Sobeom)'이 동작의 주체
* 2~5단어 내외의 극도로 짧은 포인트 컬러 손글씨 주석
* PPT 스타일의 사각 격자, 정형화된 흐름도, 복잡한 시스템 아키텍처 및 좌상단 고정 타이틀 절대 금지

### 4. 품질 검증 및 튜닝 (QA)
생성된 각 이미지가 `references/qa-checklist.md`를 통족하는지 점검합니다. 소범이가 단순 장식으로 서 있거나, 여백이 너무 없거나, 텍스트가 뭉개져 오타가 크게 발생했다면 해당 이미지의 묘사를 다듬어 즉각 재생성(Regenerate)을 제안하거나 수행합니다.

### 5. 결과 전달 및 에셋 저장
생성된 고화질 이미지를 워크스페이스의 아래 경로로 순차적으로 저장하여 전달합니다.
```text
assets/<article-slug>-illustrations/
01-topic-name.png
02-topic-name.png
```
사용자가 원본 파일을 덮어쓰도록 요청하지 않는 한, 기존 생성물을 보존하면서 추가 버전을 넘버링하여 전달합니다.
