#!/usr/bin/env python3
"""grafeo-connector 공용 모듈 — 경량 내장 LPG/텍스트 백엔드.

deps: stdlib only. GrafeoDB 엔진 미설치 환경에서 동일한 인터페이스 계약
(sync/search/analyze_rel)을 충족하는 파일 기반 구현. 추후 GrafeoDB 도입 시
이 모듈만 교체하면 된다.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = SKILL_DIR / "data"
GRAPH_PATH = DATA_DIR / "graph.json"
MANIFEST_PATH = DATA_DIR / "manifest.json"

# 데이터 원천 (환경변수로 재지정 가능)
CHUNKS_DIR = Path(os.environ.get(
    "MSN_TH_DB_CHUNKS",
    Path.home() / "Desktop/MS_Dev.nosync/projects/msn_th_db/01_Library/archive/chunks"))
TOSK_DIR = Path(os.environ.get(
    "TOSK_DATA",
    Path.home() / "Desktop/MS_Dev.nosync/projects/TOSK-External/data/KSW"))

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+|[가-힣]+|[Α-Ωα-ωἀ-ῼ]+")


def tokenize(text: str) -> list[str]:
    """라틴(움라우트 포함)/한글/그리스어 토큰화. 한글은 2-gram도 추가해 부분 일치 보강."""
    tokens = []
    for tok in TOKEN_RE.findall(text.lower()):
        tokens.append(tok)
        if re.match(r"[가-힣]{3,}", tok):
            tokens.extend(tok[i:i + 2] for i in range(len(tok) - 1))
    return tokens


def iter_chunks():
    """msn_th_db 청크 스트림. (file, dict) yield — G3 provenance 필드 보존."""
    for fp in sorted(CHUNKS_DIR.glob("*.jsonl")):
        with open(fp, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        yield fp.name, json.loads(line)
                    except json.JSONDecodeError:
                        continue


def load_graph() -> dict:
    if not GRAPH_PATH.is_file():
        raise SystemExit("오류: data/graph.json 없음 — 먼저 `python3 scripts/sync.py` 실행")
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def tilde(path: Path | str) -> str:
    """산출물에 기록할 경로는 ~ 표기로 (절대 사용자 경로 금지 — STANDARDS §5)."""
    s = str(path)
    home = str(Path.home())
    return s.replace(home, "~") if s.startswith(home) else s
