# Journal Collector: Librarian Operations

신학 학술지의 호(Heft) 단위 서지 수집 운용 지침입니다.
**데이터 원천은 Crossref API** — 출판사 사이트 스크레이핑이 아니므로 차단·약관 위험이 없습니다.

## 📖 Supported Journal Codes
- **kud**: Kerygma und Dogma (ISSN 2196-8020)
- **evth**: Evangelische Theologie (ISSN 2198-0470)
- **znw**: Zeitschrift für die Neutestamentliche Wissenschaft (ISSN 1613-009X)
- **zthk**: Zeitschrift für Theologie und Kirche (ISSN 0044-3549)

그 외 저널은 `--issn`으로 직접 지정한다 (ISSN은 `../theology_journals.json` 참조).

## 🚀 Execution Guide

사용자 요청에서 저널 코드, 권(Band), 호(Heft)를 추출하여 실행한다.

### 1. Specific Issue Collection
```bash
python3 scripts/librarian.py --journal zthk --band 120 --heft 1 --output markdown
python3 scripts/librarian.py --journal kud --band 71 --output json     # 권 전체
python3 scripts/librarian.py --issn 0028-6818 --band 65               # 코드 외 저널
```

### 2. URL 기반 수집 (비권장)
`--url`은 안내만 출력한다. 출판사 페이지를 직접 봐야 하면 `.skills/insane-search`
(`python3 -m engine "<URL>"`)로 정찰한다 — Cloudflare 등 보안 솔루션 대응 포함.

## 🛡️ Errors & Fallbacks
- **결과 0건**: Band/Heft 표기가 Crossref 레코드와 다를 수 있음 — 필터 없이 권 전체를
  받아 실제 volume/issue 값을 확인 후 재시도.
- **수집 한도**: cursor 페이징 최대 2,000건(10페이지) — 초과 저널은 Band 필터 필수.
- 수집 결과 검증: 건수와 페이지 연속성(쪽 범위)을 확인하고 표본 DOI 1건을 dx.doi.org로 점검.
