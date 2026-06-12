# EPUB Bindery: Compilation & CLI Usage

Pandoc 엔진을 활용하여 고품질 EPUB 전자책을 조립하기 위한 기술적 지침입니다.

## 🛠️ Pandoc Compilation Command
고해상도 타이포그래피와 폰트 임베딩이 적용된 표준 컴파일 명령어 예시입니다.

```bash
# 컴파일 예시 (폰트 임베딩 및 메타데이터 적용)
pandoc [목록_파일.md] \
  -o "[출력파일명].epub" \
  --metadata-file=book_manifest.yaml \
  --css=epub_style.css \
  --epub-cover-image=cover.jpg \
  --epub-embed-font="assets/fonts/KoPubBatang.ttf" \
  --epub-embed-font="assets/fonts/Pretendard.ttf" \
  --toc --toc-depth=2 \
  --split-chapters --epub-chapter-level=1
```

## 🏗️ Essential Components
- **`book_manifest.yaml`**: 제목, 저자, 권리 표기 등 책의 메타데이터 및 제본 순서 정의.
- **`epub_style.css`**: 신학/연구 가독성에 특화된 CSS (인용구, 각주 팝업, 드롭캡 서식 등).
- **Fonts**: 고전적 가치를 위한 명조체(KoPub Batang)와 명료한 가독성을 위한 고딕체(Pretendard) 파일.

## ⚠️ Operation Rules
- **Order Confirmation**: 파일 병합 순서를 에이전트 임의로 결정하지 말고, 반드시 Manifest를 제안하여 사용자의 최종 승인을 받으십시오.
- **Cover Check**: 표지 파일(`cover.jpg`)이 없는 경우 `media-factory`를 호출하여 표지 생성을 제안하십시오.
- **Path Cleanup**: 마크다운 내부의 로컬 이미지 경로를 EPUB 패키징이 가능한 상대 경로로 자동 변조(Smilzo 역할)합니다.
