#!/usr/bin/env python3
"""release_guard.py — 공개 전 위생 게이트 (저작권/원전 보호).

paper-xray의 작업 폴더 `output/{논문명}/`에는 저작권 있는 원전의 추출
전문(`_paged_healed.md` 등)이 평문으로 쌓인다. 공개해도 되는 산출물은
분석 결과 `{논문}_xray.md`(paraphrase)와 자작 도식뿐이다. 이 게이트는:

  1. 화이트리스트 강제 — run_dir에서 공개 가능 파일(`*_xray.md`, `assets/`)만
     공개 영역으로 분류하고, 원전 파생물 전부를 '비공개'로 명시한다.
  2. verbatim 게이트(★신학 특화) — `_xray.md`가 정본 추출물의 장문(기본 200자)을
     연속 복제하면 BLOCK. 원전 verbatim 누출과 인용 최소화 위반을 차단한다.

paper-cards의 release_hygiene(privacy report 대조)와 같은 계열이되,
원전 verbatim 누출이라는 신학 작업 고유 위험에 초점을 맞춘다.

사용:
    python3 scripts/release_guard.py <run_dir> [--window N]

exit: BLOCK=2, WARN=1, PASS=0
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PUBLIC_SUFFIX = "_xray.md"
PUBLIC_DIR = "assets"
MARKER_PATTERN = re.compile(r"=====\s*p\.?\s*\d{1,4}\s*=====", re.I)
DEFAULT_WINDOW = 200  # 연속 일치 문자 수 임계(한글 기준 장문 — 위양성 최소화)
# verbatim 비교 대상 정본 후보(원본에 가까운 순)
SOURCE_PRIORITY = ("_paged_healed.md", "_paged_cleaned.md", "_paged.md")


@dataclass(frozen=True, slots=True)
class Verdict:
    public: list[Path]
    private: list[Path]
    verbatim_hits: list[tuple[Path, str]]
    notes: list[str]


def is_public(path: Path, run_dir: Path) -> bool:
    if path.name.endswith(PUBLIC_SUFFIX):
        return True
    return PUBLIC_DIR in path.relative_to(run_dir).parts


def normalize(text: str) -> str:
    text = MARKER_PATTERN.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_source(run_dir: Path) -> Path | None:
    for suffix in SOURCE_PRIORITY:
        matches = sorted(run_dir.glob(f"*{suffix}"))
        if matches:
            return matches[0]
    # 폴백: _xray가 아닌 임의 추출 .md
    for path in sorted(run_dir.glob("*.md")):
        if not path.name.endswith(PUBLIC_SUFFIX):
            return path
    return None


def verbatim_run(xray_text: str, source_text: str, window: int) -> str | None:
    """xray가 정본에서 연속 window자 이상 복제한 첫 블록(없으면 None)."""
    xray_norm = normalize(xray_text)
    source_norm = normalize(source_text)
    if len(xray_norm) < window or len(source_norm) < window:
        return None
    source_windows = {
        source_norm[index : index + window]
        for index in range(len(source_norm) - window + 1)
    }
    for index in range(len(xray_norm) - window + 1):
        candidate = xray_norm[index : index + window]
        if candidate in source_windows:
            return candidate
    return None


def assess(run_dir: Path, window: int) -> Verdict:
    public: list[Path] = []
    private: list[Path] = []
    for path in sorted(run_dir.rglob("*")):
        if path.is_file():
            (public if is_public(path, run_dir) else private).append(path)

    notes: list[str] = []
    xray_files = [path for path in public if path.name.endswith(PUBLIC_SUFFIX)]
    if not xray_files:
        notes.append("공개 가능한 _xray.md 산출물이 없음")

    verbatim_hits: list[tuple[Path, str]] = []
    source = find_source(run_dir)
    if source is None:
        if xray_files:
            notes.append("정본 추출물을 못 찾음 — verbatim 검사 건너뜀")
    else:
        source_text = source.read_text(encoding="utf-8", errors="replace")
        for xray in xray_files:
            hit = verbatim_run(xray.read_text(encoding="utf-8", errors="replace"), source_text, window)
            if hit is not None:
                verbatim_hits.append((xray, hit))

    return Verdict(public=public, private=private, verbatim_hits=verbatim_hits, notes=notes)


def decide(verdict: Verdict) -> str:
    if verdict.verbatim_hits:
        return "BLOCK"
    if verdict.notes:
        return "WARN"
    return "PASS"


def report(run_dir: Path, verdict: Verdict, decision: str) -> None:
    print(f"릴리스 점검 대상: {run_dir}")
    print(f"결정: {decision}")
    print()
    print(f"공개 가능 (화이트리스트, {len(verdict.public)}개):")
    for path in verdict.public:
        print(f"  + {path.relative_to(run_dir)}")
    print(f"비공개 (원전 파생 — 공개 금지, {len(verdict.private)}개):")
    for path in verdict.private:
        print(f"  - {path.relative_to(run_dir)}")
    if verdict.verbatim_hits:
        print()
        print("❌ 원전 verbatim 장문 복제 (BLOCK):")
        for path, snippet in verdict.verbatim_hits:
            print(f"  {path.relative_to(run_dir)}: …{snippet[:60]}…")
    for note in verdict.notes:
        print(f"WARN  {note}")


def parse_args(argv: list[str]) -> tuple[Path, int]:
    parser = argparse.ArgumentParser(description="공개 전 위생 게이트(원전 보호)")
    parser.add_argument("run_dir", help="점검할 output/{논문명}/ 작업 폴더")
    parser.add_argument("--window", type=int, default=DEFAULT_WINDOW, help=f"verbatim 임계 문자 수(기본 {DEFAULT_WINDOW})")
    args = parser.parse_args(argv)
    return Path(args.run_dir), args.window


def main(argv: list[str]) -> int:
    run_dir, window = parse_args(argv)
    if not run_dir.is_dir():
        print(f"BLOCK  점검 대상 디렉토리 없음: {run_dir}")
        return 2
    verdict = assess(run_dir, window)
    decision = decide(verdict)
    report(run_dir, verdict, decision)
    return {"BLOCK": 2, "WARN": 1, "PASS": 0}[decision]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
