#!/usr/bin/env python3
"""grafeo-connector 관계 분석 — 두 개념 간 최단 경로·연결성(BFS, 무방향).

deps: stdlib only. 실행: python3 scripts/analyze_rel.py --nodes "장애인,교회"
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque

from grafeo_lite import load_graph


def resolve(graph: dict, name: str) -> str | None:
    """엔티티 + 에지 끝점(암묵 노드 — TOSK 데이터가 노드 미등록 개념을 관계에 쓸 수 있음)에서 해석."""
    name_l = name.strip().lower()
    edge_ids = {e["source"] for e in graph["edges"]} | {e["target"] for e in graph["edges"]}
    # 1순위: 정확 일치 (노드 id/별칭 → 에지 암묵 노드)
    for nid, node in graph["nodes"].items():
        if name_l == nid.lower() or any(name_l == n.lower() for n in node.get("names", [])):
            return nid
    for eid in edge_ids:
        if name_l == eid.lower():
            return eid
    # 2순위: 부분 일치
    for nid, node in graph["nodes"].items():
        if name_l in nid.lower() or any(name_l in n.lower() for n in node.get("names", [])):
            return nid
    for eid in edge_ids:
        if name_l in eid.lower():
            return eid
    return None


def main():
    ap = argparse.ArgumentParser(description="두 개념 간 관계 분석")
    ap.add_argument("--nodes", required=True, help='"개념A,개념B"')
    args = ap.parse_args()

    graph = load_graph()
    names = [n.strip() for n in args.nodes.split(",")]
    if len(names) != 2:
        raise SystemExit('오류: --nodes "A,B" 형식 필요')

    ids = []
    for n in names:
        nid = resolve(graph, n)
        if not nid:
            edge_ids = {e["source"] for e in graph["edges"]} | {e["target"] for e in graph["edges"]}
            cand = ", ".join(sorted(set(graph["nodes"]) | edge_ids)[:12])
            raise SystemExit(f"오류: '{n}' 엔티티 없음. 보유 노드 예: {cand}")
        ids.append(nid)

    adj = defaultdict(list)
    for e in graph["edges"]:
        adj[e["source"]].append((e["target"], e))
        adj[e["target"]].append((e["source"], e))

    # BFS 최단 경로
    start, goal = ids
    prev: dict = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            break
        for nxt, edge in adj[cur]:
            if nxt not in prev:
                prev[nxt] = (cur, edge)
                queue.append(nxt)

    print(f"🕸️ 관계 분석: {start} ↔ {goal}")
    print(f"   연결도(degree): {start}={len(adj[start])}, {goal}={len(adj[goal])}")
    if goal not in prev:
        print("   ⚠️ 두 개념을 잇는 경로 없음 — 그래프상 독립 (잠재 연구 간극일 수 있음)")
        return
    path = []
    cur = goal
    while prev[cur] is not None:
        parent, edge = prev[cur]
        arrow = f"—{edge['relation']}→" if edge["source"] == parent else f"←{edge['relation']}—"
        path.append((parent, arrow, cur, edge.get("evidence_chunk", "?")))
        cur = parent
    print(f"   최단 경로 ({len(path)}단계):")
    for parent, arrow, child, ev in reversed(path):
        print(f"     {parent} {arrow} {child}   [증거: {ev}]")


if __name__ == "__main__":
    main()
