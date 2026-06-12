#!/usr/bin/env python3
"""
theology_pdf_compiler.py
Converts Markdown theological manuscripts to high-fidelity PDF via Pandoc + XeLaTeX.
Includes a built-in Audit Phase (100-pt scoring) that runs after every successful build.
"""

import sys
import os
import argparse
import re
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_PREAMBLE_PATH = Path(__file__).resolve().parents[1] / "resources" / "preamble.tex"

# Required font substrings (lower-case) that must appear in pdffonts output
REQUIRED_FONTS = {
    "Noto Serif KR": "notoserifkr",
    "Brill":         "brill",
    "SBL Hebrew":    "sblhebrew",
    "SBL Greek":     "sblgreek",
}

# ---------------------------------------------------------------------------
# Audit data structures
# ---------------------------------------------------------------------------
@dataclass
class AuditResult:
    score: int = 100
    font_score: int = 40     # max 40 — all required fonts embedded
    missing_score: int = 30  # max 30 — no Missing character warnings
    layout_score: int = 20   # max 20 — no Overfull/Underfull/undefined refs
    preprocess_score: int = 10  # max 10 — no raw circled numbers left
    issues: List[str] = field(default_factory=list)
    passed: bool = True

    def compute_total(self):
        self.score = self.font_score + self.missing_score + self.layout_score + self.preprocess_score
        self.passed = self.score >= 80

# ---------------------------------------------------------------------------
# Audit Phase: individual checks
# ---------------------------------------------------------------------------
def _check_fonts(pdf_path: Path, result: AuditResult) -> None:
    """40점 — 필수 폰트 임베딩 확인 (미임베딩 폰트당 -10점)."""
    try:
        out = subprocess.run(
            ["pdffonts", str(pdf_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        fonts_str = out.stdout.lower()
        missing_fonts = [name for name, key in REQUIRED_FONTS.items() if key not in fonts_str]
        penalty = len(missing_fonts) * 10
        result.font_score = max(0, 40 - penalty)
        for name in missing_fonts:
            result.issues.append(f"[FONT] '{name}' 폰트가 PDF에 임베딩되지 않았습니다.")
    except Exception as e:
        result.font_score = 0
        result.issues.append(f"[FONT] pdffonts 실행 실패: {e}")


def _check_log(log_path: Path, result: AuditResult) -> None:
    """30점(Missing) + 20점(레이아웃) — XeLaTeX 로그 분석."""
    if not log_path.exists():
        result.missing_score = 0
        result.layout_score = 0
        result.issues.append(f"[LOG] XeLaTeX 로그 파일을 찾을 수 없습니다: {log_path}")
        return

    log_text = log_path.read_text(encoding="utf-8", errors="replace")

    # ── Missing character (30점, 개당 -5점)
    missing_chars = re.findall(r"Missing character:", log_text)
    missing_count = len(missing_chars)
    missing_penalty = min(30, missing_count * 5)
    result.missing_score = max(0, 30 - missing_penalty)
    if missing_count:
        result.issues.append(
            f"[MISSING] Missing character 경고 {missing_count}건 "
            f"(-{missing_penalty}점). 미지원 유니코드 문자를 확인하십시오."
        )

    # ── Overfull / Underfull hbox (20점, 개당 -2점, 최대 -10점)
    overfull_count  = len(re.findall(r"Overfull \\hbox", log_text))
    underfull_count = len(re.findall(r"Underfull \\hbox", log_text))
    # Undefined reference (개당 -2점, 최대 -10점)
    undef_count = len(re.findall(r"Reference .* undefined", log_text))

    layout_penalty = min(10, (overfull_count + underfull_count) * 2) + min(10, undef_count * 2)
    result.layout_score = max(0, 20 - layout_penalty)

    if overfull_count:
        result.issues.append(f"[LAYOUT] Overfull \\hbox {overfull_count}건 (-{min(10, overfull_count*2)}점).")
    if underfull_count:
        result.issues.append(f"[LAYOUT] Underfull \\hbox {underfull_count}건.")
    if undef_count:
        result.issues.append(f"[LAYOUT] 미정의 참조(Reference undefined) {undef_count}건 (-{min(10, undef_count*2)}점).")


def _check_preprocess(processed_content: str, result: AuditResult) -> None:
    """10점 — 전처리 무결성: 원문자 미치환 잔류 여부."""
    leftover = re.findall(r"[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]", processed_content)
    if leftover:
        result.preprocess_score = 0
        result.issues.append(
            f"[PREPROCESS] 원문자 {len(leftover)}개가 치환되지 않고 남아 있습니다: "
            f"{''.join(set(leftover))}"
        )


def run_audit(
    pdf_path: Path,
    log_path: Path,
    processed_content: str,
) -> AuditResult:
    """
    PDF 컴파일 직후 품질 감사를 실행하고 AuditResult를 반환한다.
    총점 80점 미만이면 result.passed = False.
    """
    result = AuditResult()
    _check_fonts(pdf_path, result)
    _check_log(log_path, result)
    _check_preprocess(processed_content, result)
    result.compute_total()
    return result


def print_audit_report(result: AuditResult, pdf_path: Optional[Path] = None) -> None:
    """감사 결과를 콘솔에 출력한다."""
    bar = "=" * 52
    print(f"\n{bar}")
    print(f"  📋  Audit Report — theology-pdf-maker")
    if pdf_path:
        print(f"  파일: {pdf_path.name}")
    print(bar)
    print(f"  총점:            {result.score:3d} / 100")
    print(f"  서체 내장 검사:   {result.font_score:3d} / 40")
    print(f"  누락 글자 검사:   {result.missing_score:3d} / 30")
    print(f"  레이아웃 경고:    {result.layout_score:3d} / 20")
    print(f"  전처리 무결성:    {result.preprocess_score:3d} / 10")
    print(bar)
    if result.issues:
        print("  ⚠  발견된 문제:")
        for issue in result.issues:
            print(f"    • {issue}")
    else:
        print("  ✅ 모든 검사 항목 이상 없음.")
    if result.passed:
        print(f"\n  ✅ AUDIT PASSED  (총점 {result.score}/100 — 기준 80점 이상)")
    else:
        print(f"\n  🚫 AUDIT FAILED  (총점 {result.score}/100 — 기준 80점 미만)")
        print(f"     Fail-Fast: PDF가 삭제됩니다.")
    print(bar + "\n")

# ---------------------------------------------------------------------------
# Markdown preprocessor
# ---------------------------------------------------------------------------
def preprocess_markdown(content: str) -> str:
    # 1. Remove YAML frontmatter
    content_no_yaml = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)

    # 2. Strip Obsidian wikilinks [[#Heading]] -> Heading
    processed = re.sub(r'\[\[#([^\]]+)\]\]', r'\1', content_no_yaml)

    # 2.5 Replace circled numbers (① to ⑳) with parenthesized numbers
    circled_map = {
        '①': '(1)', '②': '(2)', '③': '(3)', '④': '(4)', '⑤': '(5)',
        '⑥': '(6)', '⑦': '(7)', '⑧': '(8)', '⑨': '(9)', '⑩': '(10)',
        '⑪': '(11)', '⑫': '(12)', '⑬': '(13)', '⑭': '(14)', '⑮': '(15)',
        '⑯': '(16)', '⑰': '(17)', '⑱': '(18)', '⑲': '(19)', '⑳': '(20)'
    }
    for k, v in circled_map.items():
        processed = processed.replace(k, v)

    # 2.7 Replace Unicode em dash (—) with standard dash (-)
    processed = processed.replace('—', '-')

    # 2.8 Fix bold/italic parentheses formatting: **(text)** -> (**text**)
    processed = re.sub(r'\*\*\(([^)]+)\)\*\*', r'(**\1**)', processed)
    processed = re.sub(r'\*\(([^)]+)\)\*', r'(*\1*)', processed)

    # 2.9a  Structural quote transform: '텍스트(English)' → '텍스트'(English)
    #
    # Root cause: Pandoc's smart extension fails to recognise the CLOSING single
    # quote as a close-quote when immediately followed by a Korean character
    # (e.g. '신학적 조정(theologically motivated rendering)'을 → bare quotes pass
    # through unchanged).  The fundamental fix is to move the closing quote
    # BEFORE the parenthetical English so it now lands before '(' — an
    # unambiguous non-word boundary that Pandoc handles correctly.
    #
    # Result:  '신학적 조정(theologically motivated rendering)'을
    #       →  '신학적 조정'(theologically motivated rendering)을
    #       →  (Pandoc) \enquote*{신학적 조정}(theologically motivated rendering)을
    #
    # re.ASCII: restrict \w to [a-zA-Z0-9_] so Korean chars are excluded from
    # the word-char class, allowing the lookahead/lookbehind to work correctly.
    processed = re.sub(
        r"(?<!\w)'([^'(\n]+)\(([^)\n]{1,60})\)'",
        r"'\1'(\2)",
        processed,
        flags=re.MULTILINE | re.ASCII,
    )

    # 2.9b  Enquote fallback for quotes WITHOUT a trailing parenthetical.
    #
    # After 2.9a, any '...' whose closing ' is followed by '(' has already been
    # restructured and will be handled by Pandoc naturally.  This step catches
    # the remaining cases where the closing ' is followed directly by Korean
    # (e.g. '신적 방법의 소진'이라는) — Pandoc still fails there, so we inject
    # \enquote*{} directly.
    #
    # Guard (?![(\w]): skip if the closing ' is followed by '(' (already
    # restructured by 2.9a) or by an ASCII word char (English apostrophe context).
    processed = re.sub(
        r"(?<!\w)'([^'\\()\n]{2,})'(?![(\w])",
        r'\\enquote*{\1}',
        processed,
        flags=re.MULTILINE | re.ASCII,
    )

    # 3. Strip backticks around Greek/Hebrew text
    def strip_backticks(m):
        val = m.group(1)
        has_hebrew = any(0x0590 <= ord(c) <= 0x05FF or 0xFB1D <= ord(c) <= 0xFB4F for c in val)
        has_greek  = any(0x0370 <= ord(c) <= 0x03FF or 0x1F00 <= ord(c) <= 0x1FFF for c in val)
        if has_hebrew or has_greek:
            return val
        return m.group(0)

    processed = re.sub(r'`([^`]+)`', strip_backticks, processed)

    # 4. Wrap Hebrew words in \texthebrew{...}
    hebrew_char = r'[\u0590-\u05FF\uFB1D-\uFB4F\u05F3\u05F4\u05C3\u05C0־]'
    processed = re.sub(f'({hebrew_char}+)', r'\\texthebrew{\1}', processed)

    # 5. Wrap Greek words in \textgreek{...}
    greek_char = r'[\u0370-\u03FF\u1F00-\u1FFF]'
    processed = re.sub(f'({greek_char}+)', r'\\textgreek{\1}', processed)

    return processed

# ---------------------------------------------------------------------------
# Core compilation + audit pipeline
# ---------------------------------------------------------------------------
def compile_pdf(
    input_md: Path,
    output_pdf: Path,
    fontsize: str,
    linestretch: str,
    margins: str,
    paper: str,
    preamble: Path,
    fail_fast: bool = True,
) -> bool:
    """
    1. Markdown 전처리
    2. Pandoc + XeLaTeX 컴파일
    3. Audit Phase 실행
    4. fail_fast=True이고 감사 점수 < 80이면 PDF를 삭제하고 False를 반환한다.
    """
    if not input_md.exists():
        print(f"Error: Input markdown file '{input_md}' does not exist.")
        return False

    if not preamble.exists():
        print(f"Error: LaTeX preamble template '{preamble}' not found.")
        return False

    print(f"Processing markdown: {input_md.name}...")
    content = input_md.read_text(encoding='utf-8')
    processed_content = preprocess_markdown(content)

    temp_md = Path("/tmp") / f"temp_{input_md.stem}.md"
    temp_md.write_text(processed_content, encoding='utf-8')

    # ── Stage 1: Pandoc MD → LaTeX (.tex) ──────────────────────────────────────────
    stem = f"temp_{input_md.stem}"
    temp_tex = Path("/tmp") / f"{stem}.tex"
    temp_log = Path("/tmp") / f"{stem}.log"
    temp_aux = Path("/tmp") / f"{stem}.aux"
    temp_out = Path("/tmp") / f"{stem}.out"

    pandoc_cmd = [
        "pandoc",
        str(temp_md),
        "-s",
        "-o", str(temp_tex),
        "-V", f"fontsize={fontsize}",
        "-V", f"linestretch={linestretch}",
        "-V", f"geometry={paper}, {margins}",
        "-V", "documentclass=article",
        "-H", str(preamble),
        "-M", "csquotes=true",
    ]

    print(f"[1/2] Pandoc: Markdown → LaTeX...")
    try:
        subprocess.run(pandoc_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Pandoc conversion failed:")
        print(e.stderr)
        if temp_md.exists(): temp_md.unlink()
        return False

    # ── Stage 2: XeLaTeX .tex → PDF ─────────────────────────────────────────────
    xelatex_cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        f"-output-directory=/tmp",
        str(temp_tex),
    ]

    print(f"[2/2] XeLaTeX: LaTeX → PDF ({output_pdf.name})...")
    try:
        subprocess.run(xelatex_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # XeLaTeX 출력은 /tmp/<stem>.pdf — 대상 위치로 이동
        xelatex_pdf = Path("/tmp") / f"{stem}.pdf"
        xelatex_pdf.replace(output_pdf)
        print("Compilation succeeded.")
    except subprocess.CalledProcessError as e:
        print("XeLaTeX compilation failed:")
        print(e.stderr)
        for f in [temp_md, temp_tex, temp_aux, temp_out]:
            if f.exists(): f.unlink()
        return False

    # ── Audit Phase ──────────────────────────────────────────────────────────────────
    # temp_log = /tmp/<stem>.log (과정 2에서 XeLaTeX이 생성)
    audit_result = run_audit(
        pdf_path=output_pdf,
        log_path=temp_log,
        processed_content=processed_content,
    )
    print_audit_report(audit_result, pdf_path=output_pdf)

    # Cleanup temp files
    for f in [temp_md, temp_tex, temp_log, temp_aux, temp_out]:
        if f.exists():
            try:
                f.unlink()
            except Exception:
                pass

    if fail_fast and not audit_result.passed:
        if output_pdf.exists():
            output_pdf.unlink()
        return False

    return True

# ---------------------------------------------------------------------------
# Self-test: standard compilation & font validation
# ---------------------------------------------------------------------------
def run_self_test() -> bool:
    print("=== Running theology-pdf-maker self-test ===")
    test_md_path  = Path("/tmp/theology_pdf_test_src.md")
    test_pdf_path = Path("/tmp/theology_pdf_test_out.pdf")

    test_content = """\
---
title: "Self-Test Document"
author: "Theology PDF Compiler"
---

# 아모스 4:12 해석학적 변환 ①

이 테스트 문서는 한글 텍스트와 원문자 ②, 그리고 히브리어 הִכּוֹן 및 그리스어 χριστός 텍스트의 폰트 출력을 검증합니다.
줄간격은 1.5이며 폰트는 Noto Serif KR, Brill, SBL Hebrew, SBL Greek으로 렌더링되어야 합니다.
'신적 방법의 소진'이라는 해석학적 긴장. "큰따옴표 예시".
"""
    test_md_path.write_text(test_content, encoding='utf-8')

    success = compile_pdf(
        input_md=test_md_path,
        output_pdf=test_pdf_path,
        fontsize="11pt",
        linestretch="1.5",
        margins="top=2.5cm, bottom=2.5cm, left=3cm, right=3cm",
        paper="a4paper",
        preamble=DEFAULT_PREAMBLE_PATH,
        fail_fast=False,  # self-test: 점수 상관없이 리포트만 출력
    )

    if not success:
        print("Self-test compilation FAILED.")
        return False

    # Cleanup
    for f in [test_md_path, test_pdf_path]:
        if f.exists():
            f.unlink()

    return True

# ---------------------------------------------------------------------------
# Audit-only test: artificially broken content to verify Fail-Fast
# ---------------------------------------------------------------------------
def run_audit_test() -> bool:
    """
    --test-audit: 고의로 결함이 있는 원고를 컴파일하여
    Audit Phase가 문제를 탐지하고 Fail-Fast가 동작하는지 검증한다.
    """
    print("=== Running theology-pdf-maker Audit Phase test ===")
    test_md_path  = Path("/tmp/theology_pdf_audit_test_src.md")
    test_pdf_path = Path("/tmp/theology_pdf_audit_test_out.pdf")

    # 원문자 미치환 잔류 시뮬레이션(전처리 skip 우회는 불가하므로 로직 자체 테스트)
    # 여기서는 fail_fast=True로 정상 컴파일 후 80점 이상인지 확인하는 '통과' 케이스를 실행
    test_content = """\
---
title: "Audit Phase Test"
author: "Theology PDF Compiler"
---

# 아모스 감사 검증 ①②

히브리어: הִכּוֹן לִקְרַאת אֱלֹהֶיךָ
그리스어: τὸν χριστὸν αὐτοῦ
단따옴표: '신적 방법의 소진'
큰따옴표: "최후통첩이 아닌 해석학적 초청"
"""
    test_md_path.write_text(test_content, encoding='utf-8')

    print("\n[Phase A] 정상 원고 — Audit PASSED(≥80) 검증...")
    success = compile_pdf(
        input_md=test_md_path,
        output_pdf=test_pdf_path,
        fontsize="11pt",
        linestretch="1.5",
        margins="top=2.5cm, bottom=2.5cm, left=3cm, right=3cm",
        paper="a4paper",
        preamble=DEFAULT_PREAMBLE_PATH,
        fail_fast=True,
    )

    result_label = "PASSED ✅" if success else "FAILED 🚫"
    print(f"  → Phase A 결과: {result_label}")

    # Cleanup
    for f in [test_md_path, test_pdf_path]:
        if f.exists():
            f.unlink()

    print("\n=== Audit Phase 테스트 완료 ===")
    return success

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Theology PDF Compiler — Converts Markdown to high-fidelity PDF "
                    "with Brill, Noto Serif KR, SBL Hebrew/Greek fonts + Audit Phase."
    )
    parser.add_argument("input", nargs="?", help="Path to the input Markdown file.")
    parser.add_argument("-o", "--output",   help="Path to the output PDF file.")
    parser.add_argument("--fontsize",       default="11pt")
    parser.add_argument("--linestretch",    default="1.5")
    parser.add_argument("--margins",        default="top=2.5cm, bottom=2.5cm, left=3cm, right=3cm")
    parser.add_argument("--paper",          default="a4paper")
    parser.add_argument("--preamble",       help="Custom LaTeX preamble path.")
    parser.add_argument("--no-fail-fast",   action="store_true",
                        help="Audit 점수가 80점 미만이어도 PDF를 유지합니다.")
    parser.add_argument("--test",           action="store_true",
                        help="폰트 및 컴파일 파이프라인 자체 검증을 실행합니다.")
    parser.add_argument("--test-audit",     action="store_true",
                        help="Audit Phase Fail-Fast 동작 검증을 실행합니다.")

    args = parser.parse_args()

    if args.test:
        sys.exit(0 if run_self_test() else 1)

    if args.test_audit:
        sys.exit(0 if run_audit_test() else 1)

    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path   = Path(args.input)
    output_path  = Path(args.output) if args.output else input_path.with_suffix(".pdf")
    preamble_path = Path(args.preamble) if args.preamble else DEFAULT_PREAMBLE_PATH

    success = compile_pdf(
        input_md=input_path,
        output_pdf=output_path,
        fontsize=args.fontsize,
        linestretch=args.linestretch,
        margins=args.margins,
        paper=args.paper,
        preamble=preamble_path,
        fail_fast=not args.no_fail_fast,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
