#!/usr/bin/env python3
"""보고서의 출처 ID와 검증 주장 배치를 감사한다. deps: stdlib. 실행: python3 scripts/evaluate_report.py --help"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SOURCE_PATTERN = re.compile(r"\[(src_\d{3,})\]")
CLAIM_PATTERN = re.compile(r"\[(clm_\d{3,})\]")
REQUIRED_SECTIONS = ("Confidence", "Refuted", "Unresolved")


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    temporary.replace(path)


def section_map(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1).strip()] = text[match.end() : end]
    return sections


def claim_ids(records: list[dict[str, Any]]) -> set[str]:
    return {str(record.get("claim_id")) for record in records if record.get("claim_id")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--strict-coverage", action="store_true")
    args = parser.parse_args()

    session = Path(args.session).expanduser()
    report_path = Path(args.report).expanduser()
    try:
        text = report_path.read_text(encoding="utf-8")
        sources = read_jsonl(session / "sources/sources.jsonl")
        verified = read_json(session / "outputs/verified_claims.json")
        unresolved = read_json(session / "outputs/unresolved_claims.json")
        refuted = read_json(session / "outputs/refuted_claims.json")
        state = read_json(session / "state.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f"error: {error}\n")

    known_sources = {str(source.get("id")) for source in sources}
    used_sources = set(SOURCE_PATTERN.findall(text))
    unknown_sources = sorted(used_sources - known_sources)
    sections = section_map(text)
    missing_sections = [name for name in REQUIRED_SECTIONS if name not in sections]

    main_text = re.sub(
        r"^##\s+(?:Refuted|Unresolved)\s*$.*?(?=^##\s+|\Z)",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    leaked_claims = sorted(
        (claim_ids(unresolved) | claim_ids(refuted))
        & set(CLAIM_PATTERN.findall(main_text))
    )
    verified_ids = claim_ids(verified)
    used_claims = set(CLAIM_PATTERN.findall(text))
    verified_coverage = (
        len(verified_ids & used_claims) / len(verified_ids) if verified_ids else 1.0
    )
    citation_resolution = (
        len(used_sources & known_sources) / len(used_sources) if used_sources else 1.0
    )

    failures = []
    if not state.get("verification", {}).get("passed"):
        failures.append("state verification has not passed")
    if unknown_sources:
        failures.append("unknown source ids: " + ", ".join(unknown_sources))
    if missing_sections:
        failures.append("missing sections: " + ", ".join(missing_sections))
    if leaked_claims:
        failures.append(
            "unresolved/refuted claims outside annex: " + ", ".join(leaked_claims)
        )
    if args.strict_coverage and verified_coverage < 1.0:
        failures.append("not every verified claim is represented")

    result = {
        "verdict": "FAIL" if failures else "PASS",
        "report": str(report_path),
        "metrics": {
            "citation_resolution_rate": round(citation_resolution, 4),
            "verified_coverage_rate": round(verified_coverage, 4),
            "known_source_count": len(known_sources),
            "used_source_count": len(used_sources),
            "verified_claim_count": len(verified_ids),
        },
        "failures": failures,
        "limitations": [
            "This audit resolves IDs but does not prove semantic entailment.",
            "Claim leakage detection depends on explicit [clm_NNN] markers.",
        ],
    }
    output_path = session / "outputs/eval_report.json"
    atomic_json(output_path, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
