# Google Scholar Semantic Output Schema

`scholar_runner.py` writes one JSON object per line. Fields may be empty when Scholar Labs omits metadata or citation extraction fails.

## Required Fields

- `id`: stable 16-character SHA-1 prefix from query, title, and URL.
- `record_type`: always `scholar_result`.
- `source`: always `google_scholar_labs`.
- `query`: normalized query that produced the result.
- `rank`: result rank within parsed records.
- `title`: result title.
- `url`: result URL, if available.
- `authors_text`: raw author string from Scholar metadata.
- `authors`: parsed author list when available.
- `year`: publication year as integer or `null`.
- `venue`: venue/journal/book metadata when parseable.
- `publisher`: publisher metadata when parseable.
- `raw_meta`: raw Scholar metadata line.
- `snippet`: Scholar snippet or parsed text excerpt.
- `citation_count`: integer count parsed from `Cited by` / `인용`.
- `document_type`: Scholar document type label without brackets.
- `source_file`: HTML/text capture file that produced the record.
- `retrieved_at`: parser timestamp in ISO format.
- `parser`: parser path used for the record.

## Dual-Summary Fields (Scholar Labs 자료당 2요약)

Scholar Labs는 `.gs_rs` 컨테이너에 자료당 **두 종류의 설명**을 담는다. 파서는 이를 분리한다.

- `summary_synthesis`: AI가 질문에 맞춰 생성한 **종합 산문**(보통 "Explains that…"). 이전 버전이
  `snippet`에 핵심 포인트와 뒤섞어 담던 텍스트를 정제한 것.
- `key_points`: `<ul class="gs_asl">`에서 분해한 **라벨형 핵심 포인트** 목록.
  각 항목은 `{"label": "측면명", "text": "설명"}`. (예: `Internal Transformation`)
- `summary_provenance`: 위 두 필드가 채워졌으면 `google_ai_labs`, 아니면 빈 문자열.
  **⚠️ AI 생성물이므로 저자 원문 인용으로 사용 금지** — 직접 인용 근거는 원문에서 확인한다.
- `snippet`: 역호환 필드. Labs 결과면 `summary_synthesis`와 동일, 텍스트/폴백 결과면 원래 발췌.

집계 산출물(리포트 내): **Aspect Index** — `key_points`의 라벨을 쿼리별로 빈도 집계하여
질문에 대한 문헌의 논점 지형(어느 측면에 몰리는지, 각 측면을 어느 rank가 다루는지)을 제공한다.
`build_aspect_index(records)`로 프로그램에서도 직접 호출 가능.

## Citation Fields

- `citation`: primary formatted citation, usually APA when Scholar provides the standard row order.
- `citation_variants`: all formatted citation rows captured from the citation modal.
- `citation_links`: citation export links such as BibTeX, EndNote, RefMan, or RefWorks.
- `citation_status`: `ok`, `empty`, `missing_button`, or `error:<ExceptionName>`.

Treat records with `citation_status != "ok"` as incomplete bibliography evidence and retry or flag them in the final report.
