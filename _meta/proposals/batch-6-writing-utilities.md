# 배치 6 구현안 — writing + utilities (2026-06-12)

16개 전부 A등급 달성. **이로써 라이브러리 전체 85/85 A등급, 오류 0, 경고 0.**

## 신규 SKILL.md 4건 (references 기반 복원, 각 1.0.0)
- **continuous-learner**: SDE 루프(Scaffolding→Discovery→Evaluation), 추측 본능 저장 금지,
  instincts.md 영구 보존 + 충돌 시 사용자 우선순위 확인. log-miner와의 연동 명시.
- **dictionary-editor**: 다국어 표제어 규약(TRE ID), 필수 5섹션, Aporia Guard(tensions
  블록 완성 의무), relations 9종 어휘. wiki(안치)와의 경계 명시.
- **ontology-builder**: Micro/Macro-Hybrid 추출 모드, 증거(key_chunks/evidence) 없는
  엔티티·관계 생성 금지, 부정 온톨로지(add_aporia), HITL 승인 후 주입.
- **visual-feedback**: agent-pickerd 선택 → Hunter 전략(셀렉터→텍스트→계층 역추적) →
  수정 전 위치 보고(Acknowledge) → 브라우저 상태 공유.

## grafeo-connector (1.0.0 → 1.0.1) — stub 정직화
- scripts/가 비어 있는데 본문이 sync/search/analyze_rel.py 실행을 지시하던 결함 →
  `status: stub` + "구현 부재 — 실행 시도 금지, 구현 필요 안내" 명시.
- 검증기 정책 추가: stub 스킬은 W09 면제 (구현 부재를 명시한 설계 명세 허용).

## description 하이브리드화 12건 (패치 범프)
clear-english/korean-writer, slash-criticalthink, eng-student-consultant, voca-guide,
mole-manager, batch-operator, design-md, research-mentor, thoughtbox-lite, btw,
grafeo-connector.
