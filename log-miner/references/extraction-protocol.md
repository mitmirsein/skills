# Log Miner: Insight Extraction Protocol

비정형화된 대화 로그 파일에서 핵심 지식과 인사이트를 발굴(Mining)하기 위한 공정 지침입니다.

## 📂 The Mine Structure (`.logs/`)
로그는 다음 카테고리로 분류되어 저장됩니다.
- `.logs/tech/`: 코드 스니펫, 개발 논의, 아키텍처 발상.
- `.logs/theology/`: 석의 노트, 신학적 통찰, 아포리아 질문.
- `.logs/misc/`: 기타 잡무 및 일상 대화.

## ⛏️ Mining Process (Sifting)
1. **Flash Ideas (💡)**: "만약 X를 한다면?"과 같은 창의적 발상을 추출하여 `ideas.md`에 기록합니다.
2. **Code Snippets (💾)**: 재사용 가능한 함수나 설정을 추출하여 `snippets.md`에 기록합니다.
3. **Tactical Instincts (🦁)**: 사용자의 취향, 교정 사항 등을 추출하여 `continuous-learner`에 전달, `instincts.md`를 업데이트합니다.
4. **Todos (✅)**: 대본이나 대화 중 언급된 미완성 작업을 추출하여 `todo.md`에 추가합니다.

## 🏗️ Refinement & Retention
- 추출된 지식은 `data/` 또는 관련 프로젝트 폴더의 지식 베이스에 통합됩니다.
- **Retention Policy**: 작업 완료 후 사용자에게 로그 파일의 아카이브 또는 삭제 여부를 반드시 확인합니다.
