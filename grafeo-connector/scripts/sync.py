#!/usr/bin/env python3
"""grafeo-connector 동기화 — TOSK 그래프 + msn_th_db 코퍼스 매니페스트 구축.

deps: stdlib only. 실행: python3 scripts/sync.py
산출: data/graph.json (LPG 노드·에지), data/manifest.json (코퍼스 통계 — G1 무결성 근거)
"""

from __future__ import annotations

import json
from datetime import datetime

from grafeo_lite import (CHUNKS_DIR, GRAPH_PATH, MANIFEST_PATH, TOSK_DIR,
                         iter_chunks, save_json, tilde, tokenize)


def load_jsonl(path):
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    # 1. TOSK 그래프 적재
    entities = load_jsonl(TOSK_DIR / "entities.jsonl")
    relations = load_jsonl(TOSK_DIR / "relations.jsonl")
    graph = {
        "synced_at": datetime.now().isoformat(timespec="seconds"),
        "source": tilde(TOSK_DIR),
        "nodes": {e["id"]: e for e in entities},
        "edges": relations,
    }
    save_json(GRAPH_PATH, graph)

    # 2. 코퍼스 매니페스트 (BM25용 통계 — 인덱스 비대화 방지를 위해 통계만 보존)
    files, n_chunks, total_len = {}, 0, 0
    for fname, chunk in iter_chunks():
        files[fname] = files.get(fname, 0) + 1
        n_chunks += 1
        total_len += len(tokenize(chunk.get("content", "")))
    manifest = {
        "synced_at": graph["synced_at"],
        "chunks_dir": tilde(CHUNKS_DIR),
        "files": files,
        "n_chunks": n_chunks,
        "avgdl": (total_len / n_chunks) if n_chunks else 0.0,
    }
    save_json(MANIFEST_PATH, manifest)

    # G1 무결성 보고: 소스 ↔ 적재 카운트 일치 확인
    print(f"✅ Graph: 노드 {len(graph['nodes'])}/{len(entities)} · 에지 {len(graph['edges'])}/{len(relations)} "
          f"{'(G1 일치)' if len(graph['nodes']) == len(entities) else '(G1 불일치!)'}")
    print(f"✅ Corpus: 파일 {len(files)}개, 청크 {n_chunks}개, 평균 길이 {manifest['avgdl']:.0f} 토큰")
    print(f"   → {GRAPH_PATH}\n   → {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
