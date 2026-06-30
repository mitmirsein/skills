"""release_guard.py 공개 위생 게이트의 분기별 테스트."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
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


release_guard = _load("scripts/release_guard.py", "release_guard_under_test")

# 원전 추출물(정본) 모사 — 충분히 긴 본문(>200자)
SOURCE = "바르트는 계시의 유비를 존재의 유비에 맞세우며 이를 거듭 강조한다. " * 8


def _make_run(tmp: str, xray_body: str, source_body: str = SOURCE) -> Path:
    run = Path(tmp)
    (run / "foo_xray.md").write_text(xray_body, encoding="utf-8")
    (run / "foo_paged_healed.md").write_text(source_body, encoding="utf-8")
    (run / "foo.json").write_text("{}", encoding="utf-8")
    return run


class WhitelistTests(unittest.TestCase):
    def test_clean_card_passes_and_classifies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = _make_run(tmp, "분석 결과 paraphrase. 저자 고유의 해석을 드라이하게 발라낸다.")
            verdict = release_guard.assess(run, release_guard.DEFAULT_WINDOW)
            self.assertEqual(release_guard.decide(verdict), "PASS")
            public = {path.name for path in verdict.public}
            private = {path.name for path in verdict.private}
            self.assertIn("foo_xray.md", public)
            self.assertIn("foo_paged_healed.md", private)
            self.assertIn("foo.json", private)

    def test_assets_dir_is_public(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = _make_run(tmp, "paraphrase 분석.")
            assets = run / "assets" / "equations"
            assets.mkdir(parents=True)
            (assets / "eq1.svg").write_text("<svg/>", encoding="utf-8")
            verdict = release_guard.assess(run, release_guard.DEFAULT_WINDOW)
            self.assertTrue(any(p.name == "eq1.svg" for p in verdict.public))


class VerbatimTests(unittest.TestCase):
    def test_long_verbatim_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            leaked = "서론에서 인용한다. " + SOURCE[:250] + " 이상 인용."
            run = _make_run(tmp, leaked)
            verdict = release_guard.assess(run, release_guard.DEFAULT_WINDOW)
            self.assertEqual(release_guard.decide(verdict), "BLOCK")
            self.assertTrue(verdict.verbatim_hits)

    def test_short_quote_does_not_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = _make_run(tmp, "저자는 '계시의 유비'를 말한다.")  # 짧은 인용
            verdict = release_guard.assess(run, release_guard.DEFAULT_WINDOW)
            self.assertEqual(verdict.verbatim_hits, [])


class MissingArtifactTests(unittest.TestCase):
    def test_no_xray_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            (run / "foo_paged_healed.md").write_text(SOURCE, encoding="utf-8")
            verdict = release_guard.assess(run, release_guard.DEFAULT_WINDOW)
            self.assertEqual(release_guard.decide(verdict), "WARN")


if __name__ == "__main__":
    unittest.main()
