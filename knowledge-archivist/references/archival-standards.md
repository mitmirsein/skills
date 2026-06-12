# Knowledge Archivist: Collection & Archival Standards

웹 자료와 문서를 MS_Brain.nosync Vault의 ARC 구조로 수집하고 정리하기 위한 표준 지침입니다.

## 🌟 Collection Process (`/collect`)
1. **Defuddle Optimization**: 웹 수집 시 `defuddle parse <url> --md` 명령을 최우선으로 사용하여 노이즈를 제거한 본문을 추출합니다.
2. **Metadata Enrichment**: 모든 파일 상단에 반드시 YAML Frontmatter를 생성합니다. (Created, Source, Tags, Summary, Author 필수)
3. **Naming Convention**: `YYYYMMDD-Title` 또는 학술 자료의 경우 `Author-Year-Title` 형식을 사용합니다.

## 📂 Organizational Logic (`/organize`)
인박스(`000 System/Inbox`)의 문장과 맥락을 분석하여 ARC 구조로 분류합니다.
- **100 Theology**: 신학적 원전 및 연구 자료.
- **200 Ministry**: 목회, 설교, 묵상 자료.
- **300 Tech**: AI, 코딩, 방법론 자료.
- **900 Archive**: 그 외 분류가 불분명하거나 보관용 자료.

## 📋 Tagging & Linking
- ARC 구조에 부합하는 계층형 태그를 사용합니다. (예: `#theology/historical`, `#tech/ai`)
- 원본 소스(`source`)를 반드시 명시하여 지식의 계보를 보존합니다.
- 수집된 내용의 AI 요약을 통해 빠른 탐색이 가능하게 합니다.
