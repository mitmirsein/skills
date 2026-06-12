#!/usr/bin/env python3
"""journal-collector Librarian — 독일어권 신학 저널의 호(Heft) 단위 서지 수집.

deps: stdlib only (urllib). 데이터 원천: Crossref API (스크레이핑 아님 — WAF/약관 안전).
실행: python3 librarian.py --journal kud --band 71 [--heft 2] [--output markdown|json]
      python3 librarian.py --issn 0044-3549 --band 120
      python3 librarian.py --url "..."   # 안내만 출력 (브라우저 수집은 insane-search 경유)

저널 코드 (ISSN은 ../theology_journals.json과 일치):
  kud  = Kerygma und Dogma          (2196-8020)
  evth = Evangelische Theologie     (2198-0470)
  znw  = Z. f. d. neutestamentliche Wissenschaft (1613-009X)
  zthk = Z. f. Theologie und Kirche (0044-3549)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

JOURNALS = {
    "kud": ("2196-8020", "Kerygma und Dogma"),
    "evth": ("2198-0470", "Evangelische Theologie"),
    "znw": ("1613-009X", "Zeitschrift für die neutestamentliche Wissenschaft"),
    "zthk": ("0044-3549", "Zeitschrift für Theologie und Kirche"),
}
API = "https://api.crossref.org/journals/{issn}/works"
HEADERS = {"User-Agent": "MS_Dev-journal-collector/1.0 (mailto:mitmirsein@gmail.com)"}
MAX_PAGES = 10  # cursor 페이징 안전 상한 (10 × 200 = 2000건)


def fetch_works(issn: str, band: str | None, heft: str | None) -> list[dict]:
    items, cursor = [], "*"
    for _ in range(MAX_PAGES):
        params = {"rows": "200", "cursor": cursor,
                  "select": "title,author,volume,issue,page,DOI,issued,type"}
        url = API.format(issn=issn) + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        msg = data["message"]
        batch = msg.get("items", [])
        if not batch:
            break
        items.extend(batch)
        cursor = msg.get("next-cursor", "")
        if len(items) >= msg.get("total-results", 0) or not cursor:
            break
    if band:
        items = [w for w in items if w.get("volume") == str(band)]
    if heft:
        items = [w for w in items if w.get("issue") == str(heft)]
    return items


def fmt_author(w: dict) -> str:
    return "; ".join(f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
                     for a in w.get("author", [])) or "—"


def fmt_year(w: dict) -> str:
    parts = (w.get("issued") or {}).get("date-parts", [[None]])
    return str(parts[0][0] or "—")


def main():
    ap = argparse.ArgumentParser(description="저널 호 단위 서지 수집 (Crossref)")
    ap.add_argument("--journal", choices=sorted(JOURNALS), help="저널 코드")
    ap.add_argument("--issn", help="저널 코드 대신 ISSN 직접 지정")
    ap.add_argument("--band", help="권(Volume)")
    ap.add_argument("--heft", help="호(Issue)")
    ap.add_argument("--url", help="(비권장) URL 스크레이핑 — 안내만 출력")
    ap.add_argument("--output", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args()

    if args.url:
        sys.exit("URL 직접 스크레이핑은 차단 위험이 큽니다. `.skills/insane-search`로 "
                 f"먼저 정찰하십시오: python3 -m engine \"{args.url}\"")
    if not (args.journal or args.issn):
        ap.error("--journal 또는 --issn 필요")

    issn, name = JOURNALS[args.journal] if args.journal else (args.issn, args.issn)
    print(f"📚 {name} (ISSN {issn}) — Band {args.band or '전체'} / Heft {args.heft or '전체'} 수집 중...",
          file=sys.stderr)
    works = fetch_works(issn, args.band, args.heft)
    works.sort(key=lambda w: (w.get("volume", ""), w.get("issue", ""), w.get("page", "")))

    if args.output == "json":
        out = [{"title": " ".join(w.get("title", ["—"])), "authors": fmt_author(w),
                "year": fmt_year(w), "volume": w.get("volume"), "issue": w.get("issue"),
                "pages": w.get("page"), "doi": w.get("DOI"), "type": w.get("type")} for w in works]
        print(json.dumps({"journal": name, "issn": issn, "count": len(out), "results": out},
                         ensure_ascii=False, indent=1))
    else:
        print(f"# {name} — Band {args.band or '전체'}{f' Heft {args.heft}' if args.heft else ''} ({len(works)}건)\n")
        print("| 저자 | 제목 | 권/호 | 쪽 | 연도 | DOI |\n|---|---|---|---|---|---|")
        for w in works:
            title = " ".join(w.get("title", ["—"])).replace("|", "/")
            print(f"| {fmt_author(w)} | {title} | {w.get('volume', '—')}/{w.get('issue', '—')} "
                  f"| {w.get('page', '—')} | {fmt_year(w)} | {w.get('DOI', '—')} |")
    if not works:
        print("⚠️ 결과 0건 — Band/Heft 표기가 Crossref와 다를 수 있음 (필터 없이 재시도 권장)",
              file=sys.stderr)


if __name__ == "__main__":
    main()
