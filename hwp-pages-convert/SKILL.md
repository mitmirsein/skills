---
name: hwp-pages-convert
description: >
  Converts HWP/HWPX and Apple Pages (.pages) files to clean Markdown (.md) documents,
  sanitizing emphasis formatting to follow the vault constitution (converting italics
  to bold, and injecting zero-width spaces after bold markers when followed
  by Korean particles). 키워드: 한글 변환, HWP 변환, HWPX 변환, hwp to md, pages 변환, pages to md
version: 1.1.0
author: Antigravity
triggers:
  - "hwp 변환"
  - "hwpx 변환"
  - "hwp to md"
  - "한글 파일 변환"
  - "hwp 마크다운"
  - "pages 변환"
  - "pages to md"
  - "페이지 변환"
capabilities:
  - hwp_hwpx_to_markdown
  - pages_to_markdown
  - markdown_emphasis_healing
scripts_path: "."
status: active
---

# 📝 hwp-pages-convert: HWP/HWPX/Pages to Markdown 변환 스킬

이 스킬은 한글 파일(`.hwp`, `.hwpx`) 및 애플의 Pages 파일(`.pages`)을 마크다운(`.md`) 파일로 일괄 변환합니다.
동시에 **Obsidian 볼트 헌법(Constitution)**에 부합하도록 마크다운 서식을 정제 및 보정합니다.

---

## 🛠️ 핵심 기능 (Capabilities)

1. **HWP/HWPX 고정밀 파싱**: 표(Table), 굵기 강조 등을 보존하여 마크다운 본문을 추출합니다 (`dochan` 라이브러리 사용).
2. **Apple Pages 자동 변환**: macOS AppleScript 환경을 사용하여 Pages 앱을 백그라운드로 실행하고 docx로 export한 뒤, `pandoc`을 통과시켜 마크다운으로 깔끔히 변환합니다.
3. **이탤릭체 변환**: 볼트의 헌법(이탤릭체 전면 사용 금지)에 따라 모든 이탤릭체(`*텍스트*`, `_텍스트_`)를 볼드체(`**텍스트**`)로 대체합니다.
4. **볼드체조사 버그 방지 (Zero-Width Space 삽입)**: 볼드 닫는 기호(`**`) 바로 뒤에 가독성을 저해하고 렌더링을 깨뜨릴 수 있는 한글 조사 및 영숫자가 연이어 출현하는 경우, 보이지 않는 무폭 공백(`U+200B`)을 기호 사이에 자동으로 주입합니다. (예: `**텍스트**로` ➔ `**텍스트**[ZWSP]로`)
5. **RTL 태그 및 구두점 노이즈 정규화**: Pages 변환 시 pandoc으로 인해 유입되는 `["]{dir="rtl"}` 등 포맷팅 잔재를 제거하고 올바른 본래의 기호로 환원합니다.

---

## 🚀 사용법 (Usage)

터미널에서 가상환경의 파이썬 인터프리터를 사용하여 실행합니다.

```bash
# 단일 파일 변환 (출력 경로 생략 시 원본 폴더에 .md 저장)
uv run --inexact python ~/Desktop/MS_Dev.nosync/.skills/hwp-pages-convert/convert.py <입력_파일_경로.hwp/.pages>

# 디렉토리 내 전체 파일 일괄 변환 (HWP/HWPX/Pages 혼합 디렉토리 지원)
uv run --inexact python ~/Desktop/MS_Dev.nosync/.skills/hwp-pages-convert/convert.py <대상_디렉토리_경로>
```
