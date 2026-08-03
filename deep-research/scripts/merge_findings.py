#!/usr/bin/env python3
"""조사 반환 JSON/JSONL을 중복 제거해 출처 레지스트리로 병합한다. deps: stdlib. 실행: python3 scripts/merge_findings.py --help"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def normalized_url(value: str) -> str:
    parts = urlsplit(value.strip())
    query = [
        (key, item)
        for key, item in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), "")
    )


def load_records(path: Path) -> Iterable[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: object required")
            yield value
        return

    value = json.loads(text)
    if isinstance(value, list):
        candidates = value
    elif isinstance(value, dict) and isinstance(value.get("sources"), list):
        candidates = value["sources"]
    elif isinstance(value, dict):
        candidates = [value]
    else:
        raise ValueError(f"{path}: object or array required")
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError(f"{path}: source object required")
        yield candidate


def merge_claims(current: list[Any], incoming: list[Any]) -> list[Any]:
    result = list(current)
    for value in incoming:
        if value not in result:
            result.append(value)
    return result


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("findings", nargs="+")
    args = parser.parse_args()

    output = Path(args.output).expanduser()
    inputs = [Path(value).expanduser() for value in args.findings]
    existing = list(load_records(output)) if output.is_file() else []
    combined = existing[:]
    for path in inputs:
        combined.extend(load_records(path))

    by_url: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    rejected = 0
    for record in combined:
        url = str(record.get("url", "")).strip()
        title = str(record.get("title", "")).strip()
        if not url or not title:
            rejected += 1
            continue
        key = normalized_url(url)
        if key not in by_url:
            clean = dict(record)
            clean["url"] = key
            clean.pop("id", None)
            clean["claims"] = list(clean.get("claims") or [])
            by_url[key] = clean
            order.append(key)
        else:
            target = by_url[key]
            target["claims"] = merge_claims(
                list(target.get("claims") or []), list(record.get("claims") or [])
            )
            for field, value in record.items():
                if (
                    field not in {"id", "url", "claims"}
                    and not target.get(field)
                    and value
                ):
                    target[field] = value

    records = []
    for index, key in enumerate(order, start=1):
        record = by_url[key]
        record["id"] = f"src_{index:03d}"
        parts = urlsplit(record["url"])
        record.setdefault("domain", parts.netloc.lower())
        record.setdefault("independence_group", record["domain"])
        record.setdefault("primary", False)
        records.append(record)

    write_jsonl(output, records)
    print(
        json.dumps(
            {
                "output": str(output),
                "sources": len(records),
                "deduplicated": len(combined) - rejected - len(records),
                "rejected": rejected,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
