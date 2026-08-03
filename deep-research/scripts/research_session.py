#!/usr/bin/env python3
"""재개 가능한 연구 세션을 생성·조회·갱신한다. deps: stdlib. 실행: python3 scripts/research_session.py --help"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PHASES = tuple(range(1, 8))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    compact = re.sub(r"[\s_]+", "-", value.strip().lower())
    compact = "".join(ch for ch in compact if ch.isalnum() or ch == "-")
    compact = re.sub(r"-+", "-", compact).strip("-")
    return compact[:60] or "research"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def init_session(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser()
    query = read_json(Path(args.query).expanduser()) if args.query else {}
    topic = args.topic or str(query.get("topic", "")).strip()
    if not topic:
        raise ValueError("topic is required")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    session = root / f"{slugify(topic)}_{stamp}"
    for relative in (
        "artifacts/agent-results",
        "artifacts/drafts",
        "sources",
        "outputs",
    ):
        (session / relative).mkdir(parents=True, exist_ok=False)

    if query:
        atomic_json(session / "artifacts/query.json", query)

    state = {
        "schema_version": "1.0",
        "session_id": session.name,
        "topic": topic,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "status": "in_progress",
        "current_phase": 1,
        "requirements": query,
        "progress": {f"phase_{phase}": "pending" for phase in PHASES},
        "sources_count": 0,
        "verification": {"passed": False},
        "errors": [],
    }
    state["progress"]["phase_1"] = "in_progress"
    atomic_json(session / "state.json", state)
    print(session)
    return 0


def load_state(session: Path) -> dict[str, Any]:
    state_path = session / "state.json"
    if not state_path.is_file():
        raise FileNotFoundError(f"state.json not found: {session}")
    return read_json(state_path)


def status_session(args: argparse.Namespace) -> int:
    session = Path(args.session).expanduser()
    print(json.dumps(load_state(session), ensure_ascii=False, indent=2))
    return 0


def set_phase(args: argparse.Namespace) -> int:
    session = Path(args.session).expanduser()
    state = load_state(session)
    phase = int(args.phase)
    state["current_phase"] = phase
    state["progress"][f"phase_{phase}"] = args.phase_status
    if args.phase_status == "completed" and phase < 7:
        state["progress"][f"phase_{phase + 1}"] = "in_progress"
        state["current_phase"] = phase + 1
    if args.phase_status == "completed" and phase == 7:
        state["status"] = "completed"
    state["updated_at"] = utc_now()
    atomic_json(session / "state.json", state)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def list_sessions(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser()
    sessions = []
    if root.is_dir():
        for state_path in sorted(root.glob("*/state.json")):
            try:
                state = read_json(state_path)
                sessions.append(
                    {
                        "session": str(state_path.parent),
                        "topic": state.get("topic"),
                        "status": state.get("status"),
                        "current_phase": state.get("current_phase"),
                        "updated_at": state.get("updated_at"),
                    }
                )
            except (OSError, ValueError, json.JSONDecodeError) as error:
                sessions.append(
                    {"session": str(state_path.parent), "error": str(error)}
                )
    print(json.dumps(sessions, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a research session")
    init_parser.add_argument("--root", default="RESEARCH")
    init_parser.add_argument("--topic")
    init_parser.add_argument("--query")
    init_parser.set_defaults(handler=init_session)

    status_parser = subparsers.add_parser("status", help="print session state")
    status_parser.add_argument("--session", required=True)
    status_parser.set_defaults(handler=status_session)

    phase_parser = subparsers.add_parser("set-phase", help="update phase state")
    phase_parser.add_argument("--session", required=True)
    phase_parser.add_argument("--phase", type=int, choices=PHASES, required=True)
    phase_parser.add_argument(
        "--phase-status",
        choices=("pending", "in_progress", "completed", "blocked"),
        required=True,
    )
    phase_parser.set_defaults(handler=set_phase)

    list_parser = subparsers.add_parser("list", help="list sessions")
    list_parser.add_argument("--root", default="RESEARCH")
    list_parser.set_defaults(handler=list_sessions)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.handler(args))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
