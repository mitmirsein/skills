"""xray_qa.py 게이트의 분기별 회귀 테스트."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def _load(relative: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


xray_qa = _load("scripts/xray_qa.py", "xray_qa_under_test")

GOOD_CARD = """### 📄 0. 논문 메타데이터
- **저자 & 출처**: van Wolde, 2005
- **제목**: Does Amos 4:13 Praise or Threaten?

### 🎯 1. 1-Sentence Thesis
> "아모스 4:13은 위협의 절정이다." (p.2)

### 🏗️ 2. 논증의 뼈대
* [도입]: 통설 비판 (p.1)
* [본론]: 통사 분석 (p.3)
* [결론]: 심판 종결 (p.4)

### ⚔️ 3. 학술적 전선
* 비판 타겟: Crusemann 계열
* 무기: 통사론

### 💡 4. 분석자 인사이트
* 기여: 형태론적 논증
* 적용: 경외의 신앙
"""

SOURCE = """<!-- page-marked Markdown -->
===== p.1 =====
서론. van Wolde 2005.
===== p.2 =====
본문 분석.
===== p.3 =====
통사 구조.
===== p.4 =====
결론부.
"""


class GoodCardTests(unittest.TestCase):
    def test_clean_card_has_no_hard_findings(self) -> None:
        result = xray_qa.check_card(GOOD_CARD, SOURCE)
        self.assertEqual(result.hard, [])
        self.assertEqual(result.warn, [])


class StructureTests(unittest.TestCase):
    def test_missing_section_fails(self) -> None:
        broken = GOOD_CARD.replace("### ⚔️ 3. 학술적 전선", "### 잡담")
        result = xray_qa.check_card(broken, SOURCE)
        self.assertTrue(any("H1" in finding and "전선" in finding for finding in result.hard))

    def test_residue_fails(self) -> None:
        dirty = GOOD_CARD.replace("경외의 신앙", "경외의 신앙 TODO 보충")
        result = xray_qa.check_card(dirty, SOURCE)
        self.assertTrue(any("H2" in finding for finding in result.hard))

    def test_empty_section_fails(self) -> None:
        empty = (
            "### 📄 0. 논문 메타데이터\n- a\n\n"
            "### 🎯 1. Thesis\n> t (p.1)\n\n"
            "### 🏗️ 2. 뼈대\n* s (p.1)\n\n"
            "### ⚔️ 3. 전선\n* b\n\n"
            "### 💡 4. 인사이트\n"
        )
        result = xray_qa.check_card(empty, SOURCE)
        self.assertTrue(any("H3" in finding for finding in result.hard))


class PageTests(unittest.TestCase):
    def test_ghost_page_fails(self) -> None:
        ghost = GOOD_CARD.replace("(p.4)", "(p.4, p.99)")
        result = xray_qa.check_card(ghost, SOURCE)
        self.assertTrue(any("H4" in finding and "99" in finding for finding in result.hard))

    def test_in_range_pages_pass(self) -> None:
        result = xray_qa.check_card(GOOD_CARD, SOURCE)
        self.assertFalse(any("H4" in finding for finding in result.hard))

    def test_no_source_warns_not_fails(self) -> None:
        result = xray_qa.check_card(GOOD_CARD, None)
        self.assertEqual(result.hard, [])
        self.assertTrue(any("W0" in finding for finding in result.warn))

    def test_journal_source_pages_not_treated_as_ghost(self) -> None:
        # 출처 인쇄 페이지(pp.137-163)는 본문 PDF 페이지 인용이 아니므로 유령이 아님
        card = GOOD_CARD.replace("van Wolde, 2005", "van Wolde, 2005, pp.137-163")
        result = xray_qa.check_card(card, SOURCE)
        self.assertFalse(any("H4" in finding for finding in result.hard))


class FabricationTests(unittest.TestCase):
    def test_unverified_year_warns(self) -> None:
        suspect = GOOD_CARD.replace("* 적용: 경외의 신앙", "* 적용: 경외의 신앙\n* 참고: Smith 1888 연구")
        result = xray_qa.check_card(suspect, SOURCE)
        self.assertTrue(any("W1" in finding and "1888" in finding for finding in result.warn))

    def test_flag_exempts_unverified_year(self) -> None:
        flagged = GOOD_CARD.replace(
            "* 적용: 경외의 신앙", "* 적용: 경외의 신앙\n* 참고: Smith 1888 [미확인]"
        )
        result = xray_qa.check_card(flagged, SOURCE)
        self.assertFalse(any("W1" in finding for finding in result.warn))


class PraiseTests(unittest.TestCase):
    def test_praise_warns(self) -> None:
        flattering = GOOD_CARD.replace("형태론적 논증", "매우 치밀하고 유용한 논증")
        result = xray_qa.check_card(flattering, SOURCE)
        self.assertTrue(any("W2" in finding for finding in result.warn))


if __name__ == "__main__":
    unittest.main()
