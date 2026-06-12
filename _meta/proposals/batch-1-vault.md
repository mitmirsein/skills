# 배치 1 구현안 — vault 카테고리 (2026-06-12)

각 스킬의 변경 요지. 적용 완료 후 검증 결과는 `_meta/PROGRESS.md` 참조.

## vault-query (1.0.0 → 1.1.0) 🔗 MS_Brain
- description 하이브리드화. references/gotchas.md 신설(기둥 오판·격리 위반·검색 노이즈 3종)
  + 본문 가드레일 참조 연결. 본문 구조는 우수해 유지.

## wiki (4.1.0 → 4.1.1) 🔗 MS_Brain
- description 하이브리드화만. ARC v4.0 프로토콜·6단계 파이프라인·references 4종 모두
  건전 — 본문 불변. (config.json·tre_lookup.py 경로는 배치 0에서 이식성 수정 완료)

## knowledge-gardener — 제거(MS_Dev 심링크)
- 2026-04-13 wiki v4.0에 흡수되어 deprecated 선언, "1주 유예" 2개월 경과 → MS_Dev
  심링크 제거. **MS_Brain 본체 폴더와 CLAUDE.md/AGENTS.md/GEMINI.md의 언급 제거는
  사용자 승인 대기.**

## obsidian-cli (3.0.0 → 3.0.1)
- description 하이브리드화. Phase 0이 실재하지 않는 config.json을 참조 → `which obsidian`
  + `vault=` 파라미터 점검으로 교정.

## obsidian-web-clipper (1.0.0 → 1.0.1)
- description 하이브리드화 + knowledge-archivist와의 경계(단일 클립 vs 수집·배치) 명문화.

## zettel-capture (1.0.0 → 1.0.1)
- description 하이브리드화만. 본문·references 4종 건전.

## digital-curator (3.1.0 → 3.1.1)
- description 하이브리드화. sources_of_truth의 `file://~` 표기 → 일반 `~/` 경로.
  config.json 참조 링크 `../../digital-curator/` → `./` 교정.

## arc-librarian (신규 1.0.0)
- references 3종(arc-categorization, metadata-schema, gotchas)에 충실한 SKILL.md 복원.
  역할: ARC 분류·표준 frontmatter·arc_score·실존 링크. Negative scope로 archivist/wiki/
  zettel과 경계 설정. 210 Meditation 제외 명시.

## knowledge-archivist (신규 1.0.0)
- /collect(defuddle 우선, frontmatter 5필수, 명명 규칙) + /organize(dry-run→승인→
  obsidian move) 구조로 SKILL.md 복원. 볼트 헌법의 일괄 이동 승인 절차 내장.

## note-share (신규 1.0.0)
- 4-Step 파이프라인(인코딩→Advanced URI→대기·캡처→속성 기록), Share Note→JSP 폴백,
  `command` 서브커맨드 금지(BPT trap), 공개 가능 여부 사전 확인을 SKILL.md로 복원.
