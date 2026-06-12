#!/usr/bin/env python3
"""grafeo-connector 융합 검색 — 텍스트 축(BM25) + 그래프 축(엔티티 매칭) 병렬 보고.

deps: stdlib only. 실행: python3 scripts/search.py --query "Gotteslehre" [--limit 5]
G3 Provenance: 모든 텍스트 히트에 global_chunk_id·printed_page 원본 좌표 유지.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict

from grafeo_lite import MANIFEST_PATH, iter_chunks, load_graph, tokenize

K1, B = 1.5, 0.75  # BM25 표준 파라미터


def bm25_search(q_terms: list[str], limit: int) -> list[dict]:
    if not MANIFEST_PATH.is_file():
        raise SystemExit("오류: data/manifest.json 없음 — 먼저 `python3 scripts/sync.py` 실행")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    n_docs, avgdl = manifest["n_chunks"], manifest["avgdl"] or 1.0

    qset = set(q_terms)
    docs, df = [], defaultdict(int)
    for fname, chunk in iter_chunks():  # 단일 패스: 질의어 tf + df 동시 수집
        toks = tokenize(chunk.get("content", ""))
        tf = Counter(t for t in toks if t in qset)
        if tf:
            for t in tf:
                df[t] += 1
            docs.append((tf, len(toks), chunk))

    scored = []
    for tf, dl, chunk in docs:
        s = sum(
            math.log(1 + (n_docs - df[t] + 0.5) / (df[t] + 0.5))
            * (tf[t] * (K1 + 1)) / (tf[t] + K1 * (1 - B + B * dl / avgdl))
            for t in tf)
        scored.append((s, chunk))
    scored.sort(key=lambda x: -x[0])
    return [{"score": round(s, 3),
             "global_chunk_id": c.get("global_chunk_id"),
             "printed_page": c.get("printed_page"),
             "section": c.get("section") or "—",
             "snippet": (c.get("content", "")[:200] + "…")}
            for s, c in scored[:limit]]


def graph_search(q_terms: list[str], graph: dict, limit: int) -> list[dict]:
    qset = set(q_terms)
    hits = []
    for node in graph["nodes"].values():
        hay = tokenize(" ".join([node["id"], *node.get("names", []), node.get("description", "")]))
        overlap = len(qset & set(hay))
        if overlap:
            rels = [e for e in graph["edges"]
                    if e["source"] == node["id"] or e["target"] == node["id"]]
            hits.append({"overlap": overlap, "id": node["id"], "type": node.get("type"),
                         "description": node.get("description", "")[:120],
                         "relations": [f"{e['source']} —{e['relation']}→ {e['target']}" for e in rels[:4]],
                         "key_chunks": node.get("key_chunks", [])})
    hits.sort(key=lambda h: -h["overlap"])
    return hits[:limit]


def main():
    ap = argparse.ArgumentParser(description="grafeo 융합 검색")
    ap.add_argument("--query", required=True)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    q_terms = tokenize(args.query)
    graph = load_graph()
    text_hits = bm25_search(q_terms, args.limit)
    graph_hits = graph_search(q_terms, graph, args.limit)

    if args.json:
        print(json.dumps({"query": args.query, "text_axis": text_hits,
                          "graph_axis": graph_hits}, ensure_ascii=False, indent=1))
        return
    print(f"🔍 질의: {args.query}\n\n## 텍스트 축 (BM25 — msn_th_db, {len(text_hits)}건)")
    for h in text_hits:
        print(f"\n[{h['score']}] {h['global_chunk_id']} (p.{h['printed_page']}, §{h['section']})")
        print(f"  {h['snippet'][:160]}")
    print(f"\n## 그래프 축 (TOSK 엔티티, {len(graph_hits)}건)")
    for h in graph_hits:
        print(f"\n• {h['id']} ({h['type']}) — {h['description']}")
        for r in h["relations"]:
            print(f"    {r}")


if __name__ == "__main__":
    main()
