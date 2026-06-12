#!/usr/bin/env python3
"""
NLK Subject Searcher (lod.nl.go.kr SPARQL 기반)
==============================================
국립중앙도서관 LOD(lod.nl.go.kr) SPARQL 엔드포인트를 직접 조회하여
주제어를 SKOS 관계(상위어/하위어/관련어/비우선어/정의)로 확장한다.

기존 data.go.kr SubjectInformationService 게이트웨이는 기관 백엔드 장애로
무응답이라 폐기하고, 동일 SKOS 데이터의 권위 원천인 LOD SPARQL로 전환했다(무키).

참고: lod.nl.go.kr 주제 데이터의 주축은 KDC(한국십진분류)를 SKOS로 표현한 것이다.
broader(상위 분류)·narrower(하위 분류)·definition(범위주기/참조)을 제공하며,
related(연관어, RT)는 분류체계 특성상 대개 비어 있다.

사용법:
    python search.py "종말론" --output markdown
    python search.py "구원론" --limit 5 --output json
"""

import argparse
import asyncio
import json
import os
import re
import sys
from typing import Any

import httpx

SPARQL_ENDPOINT = "https://lod.nl.go.kr/sparql"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
ENV_PATH = os.path.expanduser("~/Desktop/MS_Dev.nosync/.env")


def load_env_file(env_path: str = ENV_PATH) -> None:
    """선택적: .env 로드(SPARQL은 키 불필요, 호환성 위해 유지)."""
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")


def clean_label(s: str) -> str:
    """lod.nl.go.kr 라벨 아티팩트 정리: 꼬리 '~', 정렬접두 'N-', 이중공백 이후 외국어 제거."""
    if not s:
        return ""
    s = s.strip()
    if s.endswith("~"):
        s = s[:-1]
    s = re.sub(r"^\d+-", "", s)            # prefLabel 정렬 접두 (예: '2-')
    s = re.split(r"\s{2,}", s, 1)[0]       # '교리  Religious doctrines...' → 국문만
    return s.strip()


def concept_key(uri: str) -> str:
    """판본 접미(_e5/_e6) 제거한 개념 키. 예: .../kdc/231.62_e6 → 231.62"""
    tail = uri.rstrip("/").split("/")[-1]
    return re.sub(r"_e\d+$", "", tail)


def edition_rank(uri: str) -> int:
    """최신 판본 우선용 정렬키 (_e6 > _e5)."""
    m = re.search(r"_e(\d+)$", uri)
    return int(m.group(1)) if m else 0


def cleaner_of(labels: list[str]) -> str:
    """후보 라벨 중 가장 깔끔한 것(공백 적고 짧은 것). 'e6'의 '교 리' 같은 quirk 회피."""
    cands = [c for c in (clean_label(x) for x in labels) if c]
    if not cands:
        return ""
    return sorted(cands, key=lambda x: (x.count(" "), len(x)))[0]


SKOS = "http://www.w3.org/2004/02/skos/core#"
SUBJECT_SCHEME = "http://lod.nl.go.kr/resource/subjectTermScheme"

# 1단계: 검색어로 개념 URI 후보 찾기
#  - KSH(주제명표목표): 스킴 한정 CONTAINS (라벨이 '삼위일체[三位一體]' 식이라 정확매칭 불가)
#  - KDC(십진분류): prefLabel 정확매칭 (분류 표목명, 예: 종말론)
FIND_KSH = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?s WHERE {{
  ?s skos:inScheme <%s> ; rdfs:label ?l .
  FILTER(CONTAINS(STR(?l), "{term}"))
}} LIMIT {n}""" % SUBJECT_SCHEME

FIND_KDC = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?s WHERE {{ ?s skos:prefLabel "{term}"@ko . FILTER(CONTAINS(STR(?s), "/kdc/")) }} LIMIT {n}"""

# 2단계: 확정된 개념 URI들의 관계/라벨/정의를 한 번에 확장
EXPAND = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?s ?slabel ?def ?notation ?rel ?t ?tlabel WHERE {{
  VALUES ?s {{ {values} }}
  OPTIONAL {{ ?s rdfs:label ?slabel }}
  OPTIONAL {{ ?s skos:definition ?def }}
  OPTIONAL {{ ?s skos:notation ?notation }}
  OPTIONAL {{
    VALUES ?rel {{ skos:broader skos:narrower skos:related skos:altLabel }}
    ?s ?rel ?t .
    OPTIONAL {{ ?t rdfs:label ?tlabel }}
  }}
}} LIMIT 800"""


def source_of(uri: str) -> str:
    if "/kdc/" in uri:
        return "KDC"
    if "/resource/KSH" in uri:
        return "KSH"
    return "기타"


class NLKSubjectClient:
    def __init__(self, endpoint: str = SPARQL_ENDPOINT):
        self.endpoint = endpoint

    async def _query(self, client: httpx.AsyncClient, sparql: str) -> list[dict]:
        headers = {"User-Agent": UA, "Accept": "application/sparql-results+json"}
        resp = await client.get(self.endpoint, params={"query": sparql}, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}")
        return json.loads(resp.text).get("results", {}).get("bindings", [])

    async def search(self, term: str, limit: int = 10) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        safe = term.replace('"', '\\"')
        try:
            async with httpx.AsyncClient(timeout=40.0, follow_redirects=True) as client:
                # 1단계: KSH + KDC 후보 URI 수집
                ksh = await self._query(client, FIND_KSH.format(term=safe, n=limit))
                kdc = await self._query(client, FIND_KDC.format(term=safe, n=max(2, limit)))
                uris = []
                for b in ksh + kdc:
                    u = b.get("s", {}).get("value", "")
                    if u and u not in uris:
                        uris.append(u)
                if not uris:
                    return [], {"endpoint": self.endpoint, "total_fetched": 0, "error": "결과 없음"}
                # 2단계: 확장
                values = " ".join(f"<{u}>" for u in uris[: limit + 4])
                rows = await self._query(client, EXPAND.format(values=values))
        except httpx.TimeoutException:
            return [], {"error": "SPARQL 요청 타임아웃 (lod.nl.go.kr 응답 지연)"}
        except Exception as exc:
            return [], {"error": str(exc)}

        results = self._group(rows)[:limit]
        return results, {"endpoint": self.endpoint, "total_fetched": len(results)}

    def _group(self, bindings: list[dict]) -> list[dict[str, Any]]:
        # 1) 개념키(판본 무시)별로 행을 모은다
        groups: dict[str, dict[str, Any]] = {}
        for b in bindings:
            s_uri = b.get("s", {}).get("value", "")
            if not s_uri:
                continue
            key = concept_key(s_uri)
            g = groups.setdefault(key, {
                "uris": set(), "slabels": [], "defs": [], "notations": [],
                "broader": {}, "narrower": {}, "related": {},
                "alt": set(), "same_as": set(),
            })
            g["uris"].add(s_uri)
            if b.get("slabel", {}).get("value"):
                g["slabels"].append(b["slabel"]["value"])
            if b.get("def", {}).get("value"):
                g["defs"].append(b["def"]["value"])
            if b.get("notation", {}).get("value"):
                g["notations"].append(b["notation"]["value"])

            rel = b.get("rel", {}).get("value", "")
            t = b.get("t", {})
            tval = t.get("value", "")
            tlabel = b.get("tlabel", {}).get("value", "")
            if not rel or not tval:
                continue
            relname = rel.replace(SKOS, "")
            if relname == "altLabel":
                cl = clean_label(tval)
                if cl:
                    g["alt"].add(cl)
            elif relname in ("closeMatch", "exactMatch"):
                g["same_as"].add(tval)
            elif relname in ("broader", "narrower", "related"):
                tk = concept_key(tval) if tval.startswith("http") else tval
                # 같은 대상 개념의 라벨 후보를 모은다
                bucket = g[relname].setdefault(tk, [])
                if tlabel:
                    bucket.append(tlabel)
                elif tval and not tval.startswith("http"):
                    bucket.append(tval)

        # 2) 그룹을 정규화 아이템으로 변환
        items = []
        for key, g in groups.items():
            canonical_uri = sorted(g["uris"], key=lambda u: -edition_rank(u))[0] if g["uris"] else ""
            pref = cleaner_of(g["slabels"]) or key
            scope = ""
            if g["defs"]:
                scope = clean_label(sorted(g["defs"], key=len)[-1])  # 가장 풍부한 정의
            notation = ""
            if g["notations"]:
                notation = clean_label(g["notations"][0])

            def rel_labels(d: dict[str, list[str]]) -> list[str]:
                out = []
                for _tk, labs in d.items():
                    lab = cleaner_of(labs) or clean_label(_tk)
                    if lab and lab not in out:
                        out.append(lab)
                return out

            items.append({
                "id": notation or key,
                "uri": canonical_uri,
                "source": source_of(canonical_uri),
                "preferred_label": pref,
                # 영문 비우선어 'eschatologyen'(=eschatology+lang) 중복 제거
                "alt_labels": sorted(a for a in g["alt"] if not (a.endswith(("en", "ko")) and a[:-2] in g["alt"])),
                "broader": rel_labels(g["broader"]),
                "narrower": rel_labels(g["narrower"]),
                "related": rel_labels(g["related"]),
                "scope_note": scope,
                "same_as": sorted(g["same_as"]),
                "notation": notation,
            })
        # 표기(notation) 기준 정렬로 안정적 순서
        items.sort(key=lambda x: x.get("notation") or x.get("id") or "")
        return items


def format_json(query: str, results: list[dict[str, Any]], stats: dict[str, Any]) -> str:
    return json.dumps({"query": query, "total": len(results), "results": results, "stats": stats}, ensure_ascii=False, indent=2)


def format_markdown(query: str, results: list[dict[str, Any]], stats: dict[str, Any]) -> str:
    lines = [
        f"## 국립중앙도서관 주제어 검색(LOD: KSH 주제명표목표 + KDC): `{query}`",
        "",
        f"- 엔드포인트: `{stats.get('endpoint', '')}` (SPARQL, 무키)",
        f"- 매칭 개념: **{len(results)}건**",
        "",
    ]
    if not results:
        lines.append(f"> {stats.get('error', '결과 없음 (정확한 주제어/표목인지 확인)')}")
        return "\n".join(lines)

    lines.append("| # | 출처 | 우선어 | 비우선어 | 상위어 | 하위어 |")
    lines.append("|---|------|--------|----------|--------|--------|")
    for i, it in enumerate(results, 1):
        lines.append(
            f"| {i} | {it.get('source') or '-'} | {it.get('preferred_label') or '-'} | "
            f"{', '.join(it.get('alt_labels') or []) or '-'} | "
            f"{', '.join(it.get('broader') or []) or '-'} | "
            f"{', '.join(it.get('narrower') or []) or '-'} |"
        )
    lines.append("")
    for i, it in enumerate(results, 1):
        if it.get("scope_note"):
            tag = it.get("notation") or it.get("id") or ""
            lines.append(f"### {i}. {it.get('preferred_label')} ({tag})")
            lines.append(f"> {it['scope_note']}")
            lines.append("")
    return "\n".join(lines)


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="국립중앙도서관 LOD(SPARQL) 주제어 검색 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python scripts/search.py "종말론" --output markdown
  python scripts/search.py "구원론" --limit 5 --output json
        """,
    )
    parser.add_argument("query", nargs="?", help="주제어 검색어 (정확 표제어 권장)")
    parser.add_argument("--limit", type=int, default=10, help="반환 개념 수 (기본: 10)")
    parser.add_argument("--output", default="json", choices=["json", "markdown"], help="출력 형식")
    # 하위호환(무시): 과거 data.go.kr 시절 인자
    parser.add_argument("--endpoint", help=argparse.SUPPRESS)
    parser.add_argument("--base-url", help=argparse.SUPPRESS)
    parser.add_argument("--query-param", help=argparse.SUPPRESS)
    parser.add_argument("--subject-id", help=argparse.SUPPRESS)
    parser.add_argument("--page", type=int, default=1, help=argparse.SUPPRESS)
    parser.add_argument("--type", default="json", help=argparse.SUPPRESS)
    parser.add_argument("--param", action="append", default=[], help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not args.query:
        parser.error("주제어가 필요합니다. 예: search.py \"종말론\"")

    load_env_file()
    client = NLKSubjectClient()
    results, stats = await client.search(args.query, limit=args.limit)

    if "error" in stats and not results:
        print(json.dumps({"error": stats["error"], "stats": stats}, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.output == "json":
        print(format_json(args.query, results, stats))
    else:
        print(format_markdown(args.query, results, stats))


if __name__ == "__main__":
    asyncio.run(main())
