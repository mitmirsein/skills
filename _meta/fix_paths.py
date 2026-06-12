#!/usr/bin/env python3
"""절대 사용자 경로(/Users/msn/, /Users/msna-mba/)를 이식 가능한 형태로 일괄 치환.

deps: stdlib only. 실행: python3 _meta/fix_paths.py [--apply]  (기본은 드라이런)
규칙:
  *.py   : 따옴표 안 경로 → os.path.expanduser("~/...") (import os 자동 보장),
           주석/독스트링 등 비리터럴 → ~/ 표기
  그 외  : /Users/<user>/ → ~/ 표기
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".venv", "node_modules", ".playwright-cli", "__pycache__", ".git",
             "output", "results", "gws", "_meta"}
EXTS = {".md", ".py", ".json", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml", ".txt", ".html"}

USER_RE = re.compile(r"/Users/(?:msn|msna-mba)/")
PY_QUOTED_RE = re.compile(r'(["\'])/Users/(?:msn|msna-mba)/(.*?)\1')


def ensure_import_os(text: str) -> str:
    if re.search(r"^\s*(import os\b|from os\b)", text, re.M):
        return text
    m = re.search(r"^(import |from )", text, re.M)
    if m:
        return text[: m.start()] + "import os\n" + text[m.start():]
    return "import os\n" + text


def fix_py(text: str) -> tuple[str, int]:
    n = 0
    out_lines = []
    used_expanduser = False
    for line in text.splitlines(keepends=True):
        if USER_RE.search(line):
            new, k = PY_QUOTED_RE.subn(r'os.path.expanduser(\1~/\2\1)', line)
            if k:
                used_expanduser = True
                n += k
                line = new
            if USER_RE.search(line):
                line, k2 = USER_RE.subn("~/", line)
                n += k2
        out_lines.append(line)
    text = "".join(out_lines)
    if used_expanduser:
        text = ensure_import_os(text)
    return text, n


def main():
    apply = "--apply" in sys.argv
    total_files, total_hits = 0, 0
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if not p.is_file() or p.is_symlink() or p.suffix.lower() not in EXTS:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not USER_RE.search(text):
            continue
        if p.suffix == ".py":
            new_text, n = fix_py(text)
        else:
            new_text, n = USER_RE.subn("~/", text)
        total_files += 1
        total_hits += n
        print(f"{'[적용]' if apply else '[드라이런]'} {rel}: {n}건")
        if apply:
            p.write_text(new_text, encoding="utf-8")
    print(f"\n합계: {total_files}개 파일, {total_hits}건 치환 {'(적용됨)' if apply else '(미적용 — --apply로 실행)'}")


if __name__ == "__main__":
    main()
