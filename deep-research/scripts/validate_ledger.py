#!/usr/bin/env python3
"""출처와 Claim Ledger를 검증하고 합성 허용 목록을 만든다. deps: stdlib. 실행: python3 scripts/validate_ledger.py --session PATH"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


RATINGS = set("ABCDE")
HIGH_RISK_TYPES = {"numeric", "legal", "causal", "medical", "financial", "regulatory"}


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: {error.msg}") from error
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: object required")
            records.append(value)
    return records


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    temporary.replace(path)


def signature_for(*paths: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_sources(
    records: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    sources: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for index, source in enumerate(records, start=1):
        source_id = str(source.get("id", ""))
        if not source_id:
            errors.append(f"source line {index}: missing id")
            continue
        if source_id in sources:
            errors.append(f"duplicate source id: {source_id}")
            continue
        if not source.get("url") or not source.get("title"):
            errors.append(f"{source_id}: url and title are required")
        rating = str(source.get("quality_rating", ""))
        if rating not in RATINGS:
            errors.append(f"{source_id}: quality_rating must be A-E")
        source.setdefault("domain", urlsplit(str(source.get("url", ""))).netloc.lower())
        source.setdefault("independence_group", source.get("domain") or source_id)
        source.setdefault("primary", False)
        sources[source_id] = source
    return sources, errors


def classify_claim(
    claim: dict[str, Any], sources: dict[str, dict[str, Any]]
) -> tuple[dict[str, Any], str | None]:
    claim_id = str(claim.get("claim_id", ""))
    source_ids = claim.get("source_ids")
    if not claim_id or not claim.get("text") or not isinstance(source_ids, list):
        return claim, "claim_id, text, and source_ids[] are required"

    missing = [source_id for source_id in source_ids if source_id not in sources]
    if missing:
        return claim, f"{claim_id}: unknown source ids: {', '.join(missing)}"

    usable = [
        sources[source_id]
        for source_id in source_ids
        if sources[source_id]["quality_rating"] != "E"
    ]
    groups = sorted({str(source["independence_group"]) for source in usable})
    high_risk = (
        claim.get("risk") == "high" or claim.get("claim_type") in HIGH_RISK_TYPES
    )
    process_error = None

    if claim.get("counter_refuted"):
        status = "refuted"
        confidence = "high"
    elif claim.get("conflicting"):
        status = "unresolved"
        confidence = "low"
    elif high_risk and not str(claim.get("counter_search", "")).strip():
        status = "unresolved"
        confidence = "low"
        process_error = f"{claim_id}: high-risk claim lacks counter_search"
    elif len(groups) < 2:
        status = "unresolved"
        confidence = "low"
    elif high_risk and not any(bool(source.get("primary")) for source in usable):
        status = "unresolved"
        confidence = "medium"
    else:
        status = "verified"
        confidence = (
            "high"
            if any(source["quality_rating"] == "A" for source in usable)
            else "medium"
        )

    result = dict(claim)
    result.update(
        {
            "status": status,
            "confidence": confidence,
            "high_risk": high_risk,
            "source_count": len(usable),
            "independent_groups": groups,
        }
    )
    return result, process_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True)
    args = parser.parse_args()

    session = Path(args.session).expanduser()
    source_path = session / "sources/sources.jsonl"
    ledger_path = session / "artifacts/claim_ledger.jsonl"
    state_path = session / "state.json"
    required = (source_path, ledger_path, state_path)
    missing_files = [str(path) for path in required if not path.is_file()]
    if missing_files:
        parser.exit(2, "error: missing files: " + ", ".join(missing_files) + "\n")

    try:
        source_records = read_jsonl(source_path)
        claim_records = read_jsonl(ledger_path)
        state = read_json(state_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f"error: {error}\n")

    sources, errors = validate_sources(source_records)
    seen_claims: set[str] = set()
    classified: list[dict[str, Any]] = []
    process_errors: list[str] = []
    for claim in claim_records:
        claim_id = str(claim.get("claim_id", ""))
        if claim_id and claim_id in seen_claims:
            errors.append(f"duplicate claim id: {claim_id}")
            continue
        seen_claims.add(claim_id)
        result, error = classify_claim(claim, sources)
        if error and "lacks counter_search" in error:
            process_errors.append(error)
        elif error:
            errors.append(error)
        classified.append(result)

    if errors:
        for error in errors:
            print(f"HARD_ERROR: {error}")
        return 2
    if process_errors:
        for error in process_errors:
            print(f"PROCESS_ERROR: {error}")
        return 1

    buckets = {
        "verified": [item for item in classified if item.get("status") == "verified"],
        "unresolved": [
            item for item in classified if item.get("status") == "unresolved"
        ],
        "refuted": [item for item in classified if item.get("status") == "refuted"],
    }
    for name, records in buckets.items():
        atomic_json(session / f"outputs/{name}_claims.json", records)

    state["sources_count"] = len(sources)
    state["verification"] = {
        "passed": True,
        "signature": signature_for(source_path, ledger_path),
        "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "counts": {name: len(records) for name, records in buckets.items()},
    }
    atomic_json(state_path, state)
    print(json.dumps(state["verification"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
