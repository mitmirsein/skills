#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAWP pre-PDF quality gate.

This gate catches manuscript issues that are easy to miss in semantic review but
visible in PDF output: unintended Unicode script contamination and Markdown
code spans that force romanized terms into monospace fonts.
"""

import argparse
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import List


CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
ASCII_TRANSLITERATION_RE = re.compile(r"^[A-Za-z][A-Za-z' -]{2,}$")

SUSPICIOUS_SCRIPT_RANGES = [
    ("Thai", 0x0E00, 0x0E7F),
    ("Lao", 0x0E80, 0x0EFF),
    ("Cyrillic", 0x0400, 0x04FF),
    ("Myanmar", 0x1000, 0x109F),
    ("Khmer", 0x1780, 0x17FF),
]


@dataclass
class Issue:
    code: str
    line: int
    message: str
    excerpt: str


def script_name(ch: str) -> str:
    for name, start, end in SUSPICIOUS_SCRIPT_RANGES:
        if start <= ord(ch) <= end:
            return name
    return ""


def compact_excerpt(line: str, width: int = 180) -> str:
    line = line.strip()
    if len(line) <= width:
        return line
    return line[: width - 1] + "…"


def audit_suspicious_scripts(lines: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    for line_no, line in enumerate(lines, 1):
        hits = []
        for ch in line:
            name = script_name(ch)
            if name:
                hits.append((ch, name, unicodedata.name(ch, "UNKNOWN")))
        if not hits:
            continue
        details = ", ".join(
            f"U+{ord(ch):04X} {ch} ({script}; {unicode_name})"
            for ch, script, unicode_name in hits[:8]
        )
        issues.append(
            Issue(
                code="SUSPICIOUS_SCRIPT",
                line=line_no,
                message=(
                    "비허용 문자권 문자가 발견되었다. 한국어 신학 원고에서는 Thai/Cyrillic "
                    "등이 원어 표기 안에 섞인 OCR/입력 오류일 가능성이 높다: "
                    f"{details}"
                ),
                excerpt=compact_excerpt(line),
            )
        )
    return issues


def audit_latin_code_spans(lines: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    for line_no, line in enumerate(lines, 1):
        for match in CODE_SPAN_RE.finditer(line):
            value = match.group(1).strip()
            if not ASCII_TRANSLITERATION_RE.fullmatch(value):
                continue
            if value.upper() == value:
                continue
            issues.append(
                Issue(
                    code="LATIN_CODE_SPAN",
                    line=line_no,
                    message=(
                        f"라틴 문자 음역어 `{value}`가 백틱 코드로 감싸져 있다. "
                        "theology-pdf/Pandoc에서는 모노스페이스로 렌더링되어 각주와 본문 "
                        "타이포그래피가 깨진다. 원어가 아니라 음역어라면 백틱을 제거하거나 "
                        f"*{value}*처럼 이탤릭으로 표기하라."
                    ),
                    excerpt=compact_excerpt(line),
                )
            )
    return issues


def run_quality_gate(content: str) -> List[Issue]:
    lines = content.splitlines()
    issues: List[Issue] = []
    issues.extend(audit_suspicious_scripts(lines))
    issues.extend(audit_latin_code_spans(lines))
    return issues


def render_report(target: Path, issues: List[Issue]) -> str:
    report = [
        "# TAWP Pre-PDF Quality Gate Report",
        "",
        f"- Target: `{target}`",
        f"- Status: {'PASS' if not issues else 'FAIL'}",
        f"- Issues: {len(issues)}",
        "",
    ]
    if not issues:
        report.append("No suspicious script contamination or typography-risk code spans were found.")
        return "\n".join(report) + "\n"

    report.append("## Issues")
    report.append("")
    for issue in issues:
        report.append(f"### {issue.code} at line {issue.line}")
        report.append("")
        report.append(issue.message)
        report.append("")
        report.append("```text")
        report.append(issue.excerpt)
        report.append("```")
        report.append("")
    return "\n".join(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="TAWP pre-PDF quality gate")
    parser.add_argument("-f", "--file", required=True, help="Target Markdown file")
    parser.add_argument("-o", "--output", help="Optional report path")
    parser.add_argument("--halt-on-fail", action="store_true", help="Exit non-zero when issues are found")
    args = parser.parse_args()

    target = Path(args.file)
    if not target.exists():
        print(f"[ERROR] Target file not found: {target}", file=sys.stderr)
        return 1

    content = target.read_text(encoding="utf-8")
    issues = run_quality_gate(content)
    report = render_report(target, issues)

    output_path = Path(args.output) if args.output else None
    if output_path:
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written: {output_path}")
    else:
        print(report)

    if issues and args.halt_on_fail:
        print(f"[HALT] TAWP quality gate found {len(issues)} issue(s).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
