# 📚 EPUB Bindery: Gotchas & Anti-Patterns

전자책(EPUB) 제작 및 제본 시 에이전트가 주의해야 할 사항입니다.

## 1. Typography Pitfalls (타이포그래피의 함정)
- **폰트 미포함 (Font missing)**: 사용자 정의 폰트를 사용할 때 실제 EPUB 패키지에 폰트 파일이 포함(Embed)되었는지 확인하십시오. 뷰어에 따라 기본 폰트로 깨져 보일 수 있습니다.
- **정렬 붕괴**: 양쪽 정렬(Justify) 시 너무 긴 단어가 있을 경우 가독성이 떨어집니다. 하이픈(-) 처리를 점검하십시오.

## 2. Structural Failures (구조적 실패)
- **내부 링크 파손**: Obsidian 지식 그래프의 `[[Link]]` 형식이 EPUB 내부의 상대 경로로 적절히 변환되지 않으면 '페이지를 찾을 수 없음' 오류가 발생합니다.
- **이미지 경로 오류**: 상대 경로로 지정된 이미지 애셋이 컴파일 과정에서 누락되지 않도록 `assets/` 경로를 절대적으로 관리하십시오.

## 3. Metadata Errors (메타데이터 오류)
- **Manifest 불일치**: `book_manifest.yaml`에 정의된 순서와 실제 파일 목록이 다르면 챕터가 누락되거나 순서가 뒤섞입니다.
- **커버 이미지 규격**: 너무 큰 커버 이미지는 일부 구형 e-reader에서 로딩 오류를 일으킵니다.

---
*Created by MS_Dev Third Gen Standard*
