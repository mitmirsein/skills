#!/usr/bin/env python3
"""Deep Research 결정론적 스크립트 회귀 테스트. deps: stdlib. 실행: python3 -m unittest evals/test_scripts.py"""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_DIR / "scripts"


def run_script(name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPTS / name), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


class ScriptFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        query_path = self.root / "query.json"
        query_path.write_text(
            json.dumps(
                {
                    "topic": "테스트 연구",
                    "question": "검증 파이프라인이 작동하는가?",
                    "audience": "developer",
                    "depth": "brief",
                    "deliverables": ["executive_summary"],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = run_script(
            "research_session.py",
            "init",
            "--root",
            str(self.root / "RESEARCH"),
            "--query",
            str(query_path),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.session = Path(result.stdout.strip())

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def populate_valid_evidence(self) -> None:
        write_jsonl(
            self.session / "sources/sources.jsonl",
            [
                {
                    "id": "src_001",
                    "url": "https://a.example/report",
                    "title": "A",
                    "quality_rating": "A",
                    "primary": True,
                    "independence_group": "a",
                },
                {
                    "id": "src_002",
                    "url": "https://b.example/report",
                    "title": "B",
                    "quality_rating": "B",
                    "primary": False,
                    "independence_group": "b",
                },
            ],
        )
        write_jsonl(
            self.session / "artifacts/claim_ledger.jsonl",
            [
                {
                    "claim_id": "clm_001",
                    "text": "검증된 핵심 주장",
                    "risk": "high",
                    "claim_type": "numeric",
                    "source_ids": ["src_001", "src_002"],
                    "counter_search": "반증 자료를 검색했으나 발견하지 못함",
                    "counter_refuted": False,
                    "conflicting": False,
                }
            ],
        )

    def test_end_to_end_validation_and_report_audit(self) -> None:
        self.populate_valid_evidence()
        validation = run_script("validate_ledger.py", "--session", str(self.session))
        self.assertEqual(
            validation.returncode, 0, validation.stdout + validation.stderr
        )

        report = self.session / "outputs/report.md"
        report.write_text(
            "# 보고서\n\n검증된 주장이다. [src_001] [src_002] [clm_001]\n\n"
            "## Confidence\n\n높음\n\n## Refuted\n\n없음\n\n"
            "## Unresolved\n\n없음\n",
            encoding="utf-8",
        )
        audit = run_script(
            "evaluate_report.py",
            "--session",
            str(self.session),
            "--report",
            str(report),
            "--strict-coverage",
        )
        self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
        result = json.loads((self.session / "outputs/eval_report.json").read_text())
        self.assertEqual(result["verdict"], "PASS")

    def test_high_risk_claim_requires_counter_search(self) -> None:
        self.populate_valid_evidence()
        ledger_path = self.session / "artifacts/claim_ledger.jsonl"
        claim = json.loads(ledger_path.read_text(encoding="utf-8"))
        claim["counter_search"] = ""
        write_jsonl(ledger_path, [claim])
        result = run_script("validate_ledger.py", "--session", str(self.session))
        self.assertEqual(result.returncode, 1)
        self.assertIn("PROCESS_ERROR", result.stdout)

    def test_malformed_claim_is_hard_error(self) -> None:
        self.populate_valid_evidence()
        write_jsonl(
            self.session / "artifacts/claim_ledger.jsonl",
            [{"claim_id": "clm_001", "text": "source_ids가 없다"}],
        )
        result = run_script("validate_ledger.py", "--session", str(self.session))
        self.assertEqual(result.returncode, 2)
        self.assertIn("HARD_ERROR", result.stdout)

    def test_claim_and_sources_convert_to_deduplicated_footnote(self) -> None:
        self.populate_valid_evidence()
        report = self.session / "outputs/report.md"
        output = self.session / "outputs/report_footnotes.md"
        report.write_text(
            "# 보고서\n\n"
            "첫 주장 [clm_001] [src_001] [src_002]\n\n"
            "같은 근거 [src_002] [clm_001] [src_001]\n\n"
            "## Confidence\n\n원본 태그 유지 [clm_001]\n",
            encoding="utf-8",
        )
        result = run_script(
            "convert_footnotes.py",
            "--session",
            str(self.session),
            "--report",
            str(report),
            "--output",
            str(output),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        converted = output.read_text(encoding="utf-8")
        self.assertEqual(converted.count("[^1]"), 3)
        self.assertEqual(converted.count("[^1]:"), 1)
        self.assertIn("[^1]: **주장 [clm_001]**: 검증된 핵심 주장", converted)
        self.assertIn("https://a.example/report", converted)
        self.assertIn("## Confidence\n\n원본 태그 유지 [clm_001]", converted)
        self.assertIn("[clm_001]", report.read_text(encoding="utf-8"))

    def test_unresolved_claim_is_allowed_only_in_annex(self) -> None:
        self.populate_valid_evidence()
        ledger_path = self.session / "artifacts/claim_ledger.jsonl"
        claim = json.loads(ledger_path.read_text(encoding="utf-8"))
        claim["claim_id"] = "clm_002"
        claim["source_ids"] = ["src_001"]
        write_jsonl(ledger_path, [claim])
        validation = run_script("validate_ledger.py", "--session", str(self.session))
        self.assertEqual(
            validation.returncode, 0, validation.stdout + validation.stderr
        )

        report = self.session / "outputs/report.md"
        report.write_text(
            "# 보고서\n\n확정된 핵심 주장은 없다.\n\n## Confidence\n\n낮음\n\n"
            "## Refuted\n\n없음\n\n## Unresolved\n\n검증 보류 [clm_002]\n",
            encoding="utf-8",
        )
        annex_audit = run_script(
            "evaluate_report.py",
            "--session",
            str(self.session),
            "--report",
            str(report),
        )
        self.assertEqual(
            annex_audit.returncode, 0, annex_audit.stdout + annex_audit.stderr
        )

        report.write_text(
            "# 보고서\n\n검증 보류 [clm_002]\n\n## Confidence\n\n낮음\n\n"
            "## Refuted\n\n없음\n\n## Unresolved\n\n상세 내용\n",
            encoding="utf-8",
        )
        leaked_audit = run_script(
            "evaluate_report.py",
            "--session",
            str(self.session),
            "--report",
            str(report),
        )
        self.assertEqual(leaked_audit.returncode, 1)
        self.assertIn("outside annex", leaked_audit.stdout)

    def test_merge_findings_deduplicates_tracking_urls(self) -> None:
        first = self.root / "first.json"
        second = self.root / "second.jsonl"
        first.write_text(
            json.dumps(
                {
                    "sources": [
                        {
                            "url": "https://example.org/item?utm_source=test",
                            "title": "Item",
                            "claims": ["one"],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        write_jsonl(
            second,
            [
                {
                    "url": "https://example.org/item",
                    "title": "Item",
                    "claims": ["two"],
                }
            ],
        )
        output = self.root / "sources.jsonl"
        result = run_script(
            "merge_findings.py",
            "--output",
            str(output),
            str(first),
            str(second),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        records = [json.loads(line) for line in output.read_text().splitlines()]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["claims"], ["one", "two"])


if __name__ == "__main__":
    unittest.main()
