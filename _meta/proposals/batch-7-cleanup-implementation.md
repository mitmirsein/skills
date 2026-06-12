# 배치 7 구현안 — 승인 안건 처리 + 부재 스크립트 구현 (2026-06-12)

사용자 결정(①②승인 / ③삭제 / ④구현)에 따라 전부 실행. **최종: 84/84 A등급, 오류 0, 경고 0.**

## ① kci-searcher 최종 삭제
- 삭제 전 잔존 참조 9개 파일을 kci-api-searcher로 일괄 재지정 — 특히 **런타임 통합**
  (theology-reviewer config.json `script_path` + review_engine.py 폴백 경로). 호출 시그니처
  (`search.py <query> --limit N --output json`) 호환 확인 후 교체, py_compile 통과.
- insane-search USAGE.md의 구 `--detail` 2단계 예시는 폐기 주석으로 교체.

## ② knowledge-gardener 뒷정리
- MS_Brain 본체 폴더 삭제(폐기 공지문만 있었음). 헌법 5문서(MS_Dev CLAUDE/AGENTS +
  MS_Brain CLAUDE/AGENTS/GEMINI) 47행의 언급을 wiki·vault-query만 남기고 흡수 이력 주석으로 교체.

## ③ pdf-extractor/output 360MB 삭제 (사용자 지시: 이동 아닌 삭제)

## ④ 부재 스크립트 4종 구현 (전부 stdlib 전용 + 실데이터 테스트 통과)
- **translator_audit.py**: ¶ 마커 정합 / 정보량 비율(교차 문자체계 인지형 — 라틴→한글은
  단어수×2.0 기준) / 용어집 / 신명 일관성. PASS·FAIL 케이스 테스트 통과.
- **generate_tts.py**: `%%TTS-SCRIPT%%` 블록 추출 → macOS `say`(기본)/edge-tts → m4a.
  실합성 테스트: 79자 대본 → 10.1초 AAC 생성 확인.
- **librarian.py**: 출판사 스크레이핑 대신 **Crossref API** (차단·약관 안전). 코드 4종
  (kud/evth/znw/zthk) + `--issn`. 실호출 테스트: ZThK 120/1 → 논문 6건 수집.
  librarian-ops.md를 새 경로·방식으로 갱신.
- **grafeo 3종** (sync/search/analyze_rel + grafeo_lite 공용 모듈): GrafeoDB 미설치
  환경 대응 **경량 내장 백엔드**(파일 기반 LPG + 단일 패스 BM25, 한글 2-gram 보강).
  실데이터 테스트: G1 일치(노드 9·에지 4·청크 5,061), 독일어 BM25 히트(provenance 포함),
  그래프 축 엔티티 매칭, 최단 경로(배려→차별). TOSK 데이터가 노드 미등록 개념을 관계에
  쓰는 현실에 맞춰 에지 끝점 암묵 노드 해석 지원. 산출물 data/는 gitignore + `~` 경로 표기.
  벡터/RRF는 GrafeoDB 도입 시 grafeo_lite.py 교체로 활성화 (SKILL.md에 명시).

## SKILL.md 갱신 4건
theology-translator·bible-meditation·journal-collector의 "부재" 표기 → 실행 명령으로 교체.
grafeo-connector stub → active (백엔드 주석 포함, 1.1.0).
