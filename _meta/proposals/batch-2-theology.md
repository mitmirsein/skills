# 배치 2 구현안 — theology 카테고리 (2026-06-12)

18개 전부 A등급 달성. 핵심 변경 요지:

## faith-compass (3.6.0 → 3.6.1) — SPLIT
- 356줄 → 112줄. 내용 불변 분할: RISE 7규칙·첫 응답 규칙 전문 → `references/rise-engine.md`,
  출력 템플릿 5종 → `references/output-templates.md`, v3.6 변경 내역 → `references/changelog.md`.
- 본문에는 RISE 요약(1줄/규칙)·상태 기계 골격·명령어 표만 유지. Safety Layer 본질은
  본문에 보존(요약 #7 + 원칙 #6).

## 기존 13개 — description 하이브리드화 (패치 버전 범프)
theology-research, -exegesis, -scholar, -reviewer, -redteam, -reader, -citation-linker,
-discourse-mapper, -pdf-maker, -terminology-linter, -local-searcher, barth-kd-navigator,
sermon-insight. 추가로 경계 명문화: scholar(심층) ↔ research(서베이 래퍼),
terminology-linter에 "최종 필터" 헌법 정책 반영.

## 신규 SKILL.md 4건 (references 기반 복원, 각 1.0.0/6.0.0)
- **theology-translator (6.0.0)**: Orchestrator + Drafter/Red-Team Auditor/Stylist 역할
  격리 루프, Token Ratio Guard 70%, Author Mode(Exegetical Analyst), YT 강연 프로토콜.
  TRE "최종 필터" 정책 내장. ⚠️ translator_audit.py 부재 정직 표기(수동 검문으로 대체).
- **theology-chunker (1.0.0)**: msn_th_db JSONL 인입 — 사전 점검 3종(메타데이터/페이지
  오프셋/OCR), paragraph·token 전략, uv run 실행. theology-local-searcher와 동반 관계 명시.
- **bible-meditation (1.0.0)**: 돈 까밀로 대화 → Lewis×Peterson 종합 → TTS·번역 3단계.
  **210 Meditation 읽기 전용 + 산출물은 220 Sermons/600 Kerygma** 헌법 조항 내장.
  ⚠️ generate_tts.py 부재 정직 표기(대본 텍스트까지만).
- **rise-battleground-map (1.0.0)**: 7축 긴장 지형도(객관/주관/초월) 0–10 점수화(근거
  필수), HTML Chart.js → Mermaid radar → ASCII 시각화 우선순위. 아포리아 보존 명시.
