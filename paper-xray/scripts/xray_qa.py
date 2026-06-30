#!/usr/bin/env python3
"""xray_qa.py — X-Ray 브리핑 산출물 기계 검수 게이트.

`paper-xray`의 최종 산출물(`{논문}_xray.md`)을 파싱해, constitution의
독해 헌법을 **prose 규범에서 기계 게이트로 승격**시킨다. 사실 정확성을
증명하지는 못하지만(그건 인간 검토 몫), 구조 누락·미완성 흔적·유령 페이지
인용·정본 미확인 서지정보 같은 *기계적으로 잡히는 위반*을 차단한다.

핵심 검사:
  - 구조: templates.md의 5대 섹션(메타/Thesis/Skeleton/Battleground/Insight) 존재
  - 미완성: TODO·템플릿 플레이스홀더 잔재·빈 섹션
  - 유령 페이지(★우위): 브리핑이 인용한 p.N ⊆ 정본 `_paged_healed.md`의
    실제 `===== p.N =====` 마커 집합 (paper-cards의 "범위 내" 검사보다 강함)
  - 날조 의심(제1조): 정본에 없는 연도를 `[미확인]` 없이 단정 → WARN
  - 금칙 찬사(제5조): "치밀·유용" 류 영혼 없는 평가 → WARN

사용:
    python3 scripts/xray_qa.py <xray.md> [--source <paged_healed.md>]

FAIL이 하나라도 있으면 exit 1. WARN만 있으면 exit 0(검토 요망).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── 섹션 시그니처 (이모지·번호 표기 변형 허용, 키워드로 매칭) ──
SECTION_SIGNATURES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("0. 논문 메타데이터", re.compile(r"^#{1,4}\s.*(메타데이터|metadata)", re.I | re.M)),
    ("1. 1-Sentence Thesis", re.compile(r"^#{1,4}\s.*(thesis|논지)", re.I | re.M)),
    ("2. 논증의 뼈대", re.compile(r"^#{1,4}\s.*(뼈대|skeleton|flow)", re.I | re.M)),
    ("3. 학술적 전선", re.compile(r"^#{1,4}\s.*(전선|battleground|combat)", re.I | re.M)),
    ("4. 분석자 인사이트", re.compile(r"^#{1,4}\s.*(인사이트|insight)", re.I | re.M)),
)

# ── 템플릿 잔재·미완성 흔적 (안 채운 placeholder) ──
RESIDUE_PATTERN = re.compile(
    r"TODO|1~2줄\)|논리 단계 \d\)|핵심 흐름 1|핵심 요약 1|\[저자명|"
    r"\(어떤 [^)]*\?\)|\(논증의 치밀함|\(실천적, 실존적"
)

# ── 페이지 참조 / 정본 마커 ──
# 본문 PDF 인용 `p.N`만 잡고, 출처 인쇄 페이지(`pp.137-163` 복수형)와
# 인쇄 페이지 주석(`printed p.`/`인쇄 p.`)은 제외한다. (paper-cards qa_check 차용)
PAGE_REF_PATTERN = re.compile(r"(?<![pP])(?<!printed )(?<!인쇄 )p\.?\s*(\d{1,4})(?:\s*[-–~]\s*(\d{1,4}))?")
KOREAN_PAGE_PATTERN = re.compile(r"페이지\s*(\d{1,4})")
MARKER_PATTERN = re.compile(r"=====\s*p\.?\s*(\d{1,4})\s*=====", re.I)

# ── 서지/평가 ──
YEAR_PATTERN = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
UNVERIFIED_FLAGS = ("[미확인]", "[잠정]")
PRAISE_PATTERN = re.compile(r"(치밀|탁월|훌륭|유용|흥미로|인상적|뛰어난|매우 좋)")


@dataclass(frozen=True, slots=True)
class CheckResult:
    hard: list[str] = field(default_factory=list)
    warn: list[str] = field(default_factory=list)


def check_structure(text: str) -> list[str]:
    return [
        f"H1 섹션 누락: {label}"
        for label, pattern in SECTION_SIGNATURES
        if pattern.search(text) is None
    ]


def check_residue(text: str) -> list[str]:
    hits = sorted({match.group(0) for match in RESIDUE_PATTERN.finditer(text)})
    return [f"H2 미완성 흔적/템플릿 잔재: {hit[:40]}" for hit in hits]


def check_empty_sections(text: str) -> list[str]:
    parts = re.split(r"^(#{2,4}\s.+)$", text, flags=re.M)
    failures: list[str] = []
    for index in range(1, len(parts), 2):
        heading = parts[index].strip()
        body = parts[index + 1] if index + 1 < len(parts) else ""
        if not body.strip():
            failures.append(f"H3 빈 섹션(내용 없음): {heading[:40]}")
    return failures


def page_refs(text: str) -> set[int]:
    refs: set[int] = set()
    for match in PAGE_REF_PATTERN.finditer(text):
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else start
        if start <= end <= start + 100:  # 비정상 광역 범위 가드
            refs.update(range(start, end + 1))
    for match in KOREAN_PAGE_PATTERN.finditer(text):
        refs.add(int(match.group(1)))
    return refs


def source_markers(source_text: str) -> set[int]:
    return {int(match.group(1)) for match in MARKER_PATTERN.finditer(source_text)}


def check_pages(text: str, source_text: str | None) -> CheckResult:
    if source_text is None:
        return CheckResult(warn=["W0 정본(--source) 미제공: 유령 페이지 검증 건너뜀"])
    markers = source_markers(source_text)
    if not markers:
        return CheckResult(warn=["W0 정본에 '===== p.N =====' 마커 없음: 페이지 검증 불가"])
    refs = page_refs(text)
    ghosts = sorted(ref for ref in refs if ref not in markers)
    if ghosts:
        return CheckResult(
            hard=[
                f"H4 유령 페이지 인용: {ghosts[:8]} (정본 마커 범위 p.{min(markers)}–{max(markers)} 밖)"
            ]
        )
    return CheckResult()


def check_fabrication(text: str, source_text: str | None) -> list[str]:
    if source_text is None:
        return []
    source_years = set(YEAR_PATTERN.findall(source_text))
    suspect: set[str] = set()
    for line in text.splitlines():
        if any(flag in line for flag in UNVERIFIED_FLAGS):
            continue  # 이미 [미확인]/[잠정]으로 정직하게 표기된 줄은 면제
        for year in YEAR_PATTERN.findall(line):
            if year not in source_years:
                suspect.add(year)
    if not suspect:
        return []
    return [
        f"W1 정본 미확인 연도 {sorted(suspect)}: 정본에 근거 없음 — [미확인] 표기 검토(제1조)"
    ]


def check_praise(text: str) -> list[str]:
    hits = sorted({match.group(0) for match in PRAISE_PATTERN.finditer(text)})
    if not hits:
        return []
    return [f"W2 영혼 없는 찬사 의심 표현 {hits}: 사실/평가 분리 점검(제5조)"]


def check_card(text: str, source_text: str | None) -> CheckResult:
    hard: list[str] = []
    warn: list[str] = []
    hard += check_structure(text)
    hard += check_residue(text)
    hard += check_empty_sections(text)
    page_result = check_pages(text, source_text)
    hard += page_result.hard
    warn += page_result.warn
    warn += check_fabrication(text, source_text)
    warn += check_praise(text)
    return CheckResult(hard=hard, warn=warn)


def fix_markdown_emphasis(text: str) -> tuple[str, int]:
    """
    마크다운 렌더링을 깨뜨리는 각종 요소들을 자동 교정합니다:
    1. 줄 전체가 이탤릭으로 감싸진 경우 앞뒤의 * 기호를 제거하여 이탤릭체 해제.
    2. 이탤릭체 사용 금지 규정에 따라 인라인 이탤릭(*텍스트*)을 볼드(**텍스트**)로 자동 전환.
       (단, 이미지 경로 내 언더바 충돌을 막기 위해 언더바 이탤릭 변환은 제외하며,
        글머리 기호 리스트 * 등은 보존하기 위해 정교한 정규식을 사용함)
    3. 괄호와 닫는 강조 기호의 결합부()**) 충돌 우회 보정 ()\u200b**\u200b 삽입).
    4. 강조 기호(**) 뒤에 한글/영어가 밀착될 때 렌더링 풀림 방지를 위해 U+200B 삽입.
    """
    count = 0
    
    # 1. 줄 전체가 이탤릭으로 감싸진 경우 -> 이탤릭 기호(*) 제거 (줄바꿈 플래그 M 활성화)
    pattern_line_italic = r'^\s*(?<!\*)\*(?!\s)(.+?)\*(?!\*)\s*$'
    text, c0 = re.subn(pattern_line_italic, r'\1', text, flags=re.M)
    count += c0
    
    # 2. 인라인 이탤릭체(*텍스트*) -> 볼드(**텍스트**) 변환 (최대 200자, 공백 시작 불가)
    pattern_italic_star = r'(?<!\*)\*(?!\s)([^*]{1,200}?\S)\*(?!\*)'
    text, c1 = re.subn(pattern_italic_star, r'**\1**', text)
    count += c1

    # 3. 괄호 뒤 볼드 닫기 충돌 보정: )**로 -> )\u200b**\u200b로
    pattern_paren = r'(\))\*\*(?!\u200b)([가-힣a-zA-Z])'
    text, c2 = re.subn(pattern_paren, r'\1' + '\u200b' + r'**' + '\u200b' + r'\2', text)
    count += c2

    # 4. 괄호 뒤 볼드 닫기 기호 바로 앞에도 U+200B가 없는 경우 보정: )** -> )\u200b**
    pattern_paren_direct = r'(\))(?!\u200b)\*\*'
    text, c3 = re.subn(pattern_paren_direct, r'\1' + '\u200b' + r'**', text)
    count += c3

    # 5. 일반적인 볼드 기호 뒤 결합 보정: **단어 -> **\u200b단어 / **조사 -> **\u200b조사
    pattern_general = r'\*\*(?!\u200b)([가-힣a-zA-Z])'
    text, c4 = re.subn(pattern_general, r'**' + '\u200b' + r'\1', text)
    count += c4

    return text, count


def parse_args(argv: list[str]) -> tuple[Path, Path | None]:
    parser = argparse.ArgumentParser(description="X-Ray 브리핑 기계 검수 게이트")
    parser.add_argument("card", help="검수할 {논문}_xray.md 경로")
    parser.add_argument(
        "--source",
        help="페이지 마커 교차검증용 정본 {논문}_paged_healed.md 경로(권장)",
    )
    args = parser.parse_args(argv)
    return Path(args.card), (Path(args.source) if args.source else None)


def main(argv: list[str]) -> int:
    card_path, source_path = parse_args(argv)
    if not card_path.exists():
        print(f"FAIL  H0 브리핑 파일 없음: {card_path}")
        return 1
    text = card_path.read_text(encoding="utf-8")
    
    # 마크다운 강조 렌더링 린트 및 자동 보정 (U+200B 삽입)
    fixed_text, fix_count = fix_markdown_emphasis(text)
    if fix_count > 0:
        card_path.write_text(fixed_text, encoding="utf-8")
        print(f"FIX   마크다운 볼드 강조 렌더링 깨짐 자동 보정 완료 ({fix_count}곳 U+200B 삽입)")
        text = fixed_text

    source_text: str | None = None
    if source_path is not None:
        if not source_path.exists():
            print(f"FAIL  H0 정본 파일 없음: {source_path}")
            return 1
        source_text = source_path.read_text(encoding="utf-8")

    result = check_card(text, source_text)
    for finding in result.hard:
        print(f"FAIL  {finding}")
    for finding in result.warn:
        print(f"WARN  {finding}")
    if result.hard:
        return 1
    print("PASS  warning review required" if result.warn else "PASS  no mechanical findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
