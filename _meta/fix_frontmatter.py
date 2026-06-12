#!/usr/bin/env python3
"""SKILL.md frontmatter 정규화: version SemVer화(+codename 보존), status 기본값 추가.

deps: stdlib only. 실행: python3 _meta/fix_frontmatter.py [--apply]  (기본 드라이런)
규칙 (STANDARDS.md §2):
  version: "3.0.0 (Third Gen)" → version: 3.0.0 + codename: Third Gen
  version 없음               → version: 1.0.0 추가
  status 없음                → status: active 추가 (stub 분류는 TRIAGE에서 수동)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"_meta", "_template", "gws"}
VERSION_RE = re.compile(r'^version:[ \t]*["\']?(\d+\.\d+\.\d+)[ \t-]*\(?([^)"\'\n]*?)\)?["\']?[ \t]*$', re.M)


def normalize(text: str) -> tuple[str, list[str]]:
    changes = []
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text, changes
    # 닫는 --- 위치
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return text, changes

    fm = "".join(lines[1:end])
    m = VERSION_RE.search(fm)
    if m:
        ver, label = m.group(1), m.group(2).strip()
        if m.group(0).strip() != f"version: {ver}":
            repl = f"version: {ver}"
            if label:
                repl += f"\ncodename: {label}"
            fm = fm[: m.start()] + repl + fm[m.end():]
            changes.append(f"version '{m.group(0).strip()}' → SemVer" + (f" + codename '{label}'" if label else ""))
    else:
        fm += "version: 1.0.0\n"
        changes.append("version: 1.0.0 추가")
    if not re.search(r"^status:", fm, re.M):
        fm += "status: active\n"
        changes.append("status: active 추가")
    if not changes:
        return text, changes
    return lines[0] + fm + "".join(lines[end:]), changes


def main():
    apply = "--apply" in sys.argv
    count = 0
    for entry in sorted(ROOT.iterdir()):
        if entry.name.startswith(".") or entry.name in EXCLUDE or not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8")
        new_text, changes = normalize(text)
        if changes:
            count += 1
            print(f"{'[적용]' if apply else '[드라이런]'} {entry.name}: " + "; ".join(changes))
            if apply:
                skill_md.write_text(new_text, encoding="utf-8")
    print(f"\n합계 {count}개 파일 {'(적용됨)' if apply else '(미적용 — --apply로 실행)'}")


if __name__ == "__main__":
    main()
