#!/usr/bin/env python3
"""extract_pdf.py page marker helpers."""

import json
import builtins
import contextlib
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import extract_pdf  # noqa: E402


def _safe_result(**overrides):
    values = {
        "pdf_type": "text_based",
        "markdown": "# 제목\n\n본문입니다.\n",
        "page_count": 2,
        "pages_needing_ocr": [],
        "has_encoding_issues": False,
        "is_complex_layout": False,
        "pages_with_columns": [],
        "pages_with_tables": [],
    }
    values.update(overrides)
    return types.SimpleNamespace(**values)


def _pages_result(page_indexes=(0, 1)):
    pages = [
        types.SimpleNamespace(
            page=index,
            markdown=f"페이지 {index + 1}",
            needs_ocr=False,
        )
        for index in page_indexes
    ]
    return types.SimpleNamespace(
        pages=pages,
        pages_needing_ocr=[],
        pages_with_columns=[],
        is_complex=False,
    )


def _write_fake_pdf(directory):
    pdf_path = Path(directory) / "paper.pdf"
    pdf_path.write_bytes(b"%PDF-fake")
    return pdf_path


class TestPageMarkedMarkdown(unittest.TestCase):
    def test_writes_page_markers_from_json_kids(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "paper.json").write_text(
                json.dumps(
                    {
                        "number of pages": 2,
                        "kids": [
                            {"page number": 1, "content": "첫 페이지"},
                            {"page number": 2, "content": "둘째 페이지"},
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            marked = extract_pdf._write_page_marked_markdown(str(out), "paper")
            text = Path(marked).read_text(encoding="utf-8")

        self.assertIn("===== p.1 =====", text)
        self.assertIn("첫 페이지", text)
        self.assertIn("===== p.2 =====", text)
        self.assertIn("둘째 페이지", text)


class TestPdfInspectorEngine(unittest.TestCase):
    def _run(self, directory, result, *, page_markers=False, start_page=1, pages=None):
        pdf_path = _write_fake_pdf(directory)
        fake_module = types.SimpleNamespace(
            process_pdf=lambda path: result,
            extract_pages_markdown=lambda path: pages or _pages_result(),
        )
        with patch.object(extract_pdf, "_load_pdf_inspector", return_value=fake_module):
            return extract_pdf.extract_pdf(
                str(pdf_path),
                output_dir=str(Path(directory) / "output"),
                page_markers=page_markers,
                start_page=start_page,
                engine="pdf-inspector",
            )

    def test_pdf_inspector_simple_text_writes_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._run(directory, _safe_result(page_count=1), pages=_pages_result((0,)))
            self.assertIsNotNone(result)
            self.assertEqual(Path(result).read_text(encoding="utf-8"), "# 제목\n\n본문입니다.\n")

    def test_pdf_inspector_page_markers_preserve_all_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._run(
                directory,
                _safe_result(page_count=2),
                page_markers=True,
                pages=_pages_result((0, 1)),
            )
            text = Path(result).read_text(encoding="utf-8")
            self.assertEqual(text.count("===== p."), 2)
            self.assertIn("===== p.1 =====", text)
            self.assertIn("===== p.2 =====", text)
            self.assertIn("페이지 1", text)
            self.assertIn("페이지 2", text)

    def test_pdf_inspector_respects_start_page(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._run(
                directory,
                _safe_result(page_count=2),
                page_markers=True,
                start_page=7,
                pages=_pages_result((0, 1)),
            )
            text = Path(result).read_text(encoding="utf-8")
            self.assertIn("===== p.7 =====", text)
            self.assertIn("===== p.8 =====", text)
            self.assertNotIn("===== p.1 =====", text)

    def test_pdf_inspector_missing_dependency_is_legible(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = _write_fake_pdf(directory)
            original_import = builtins.__import__

            def missing_pdf_inspector(name, *args, **kwargs):
                if name == "pdf_inspector":
                    raise ImportError("missing in test")
                return original_import(name, *args, **kwargs)

            stdout = io.StringIO()
            with patch("builtins.__import__", side_effect=missing_pdf_inspector):
                with contextlib.redirect_stdout(stdout):
                    result = extract_pdf.extract_pdf(
                        str(pdf_path),
                        output_dir=str(Path(directory) / "output"),
                        engine="pdf-inspector",
                    )
            self.assertIsNone(result)
            self.assertIn("pdf-inspector 엔진이 선택되었지만", stdout.getvalue())

    def test_pdf_inspector_rejects_encoding_issue(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._run(directory, _safe_result(has_encoding_issues=True))
            self.assertIsNone(result)

    def test_pdf_inspector_reports_pages_needing_ocr(self):
        with tempfile.TemporaryDirectory() as directory:
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                result = self._run(
                    directory,
                    _safe_result(pages_needing_ocr=[3]),
                )
            self.assertIsNone(result)
            self.assertIn("1-based: [3]", stdout.getvalue())

    def test_pdf_inspector_rejects_scanned_or_mixed_as_complete(self):
        for pdf_type in ("scanned", "image_based", "mixed"):
            with self.subTest(pdf_type=pdf_type), tempfile.TemporaryDirectory() as directory:
                result = self._run(directory, _safe_result(pdf_type=pdf_type))
                self.assertIsNone(result)

    def test_pdf_inspector_flags_column_or_complex_layout(self):
        cases = (
            {"pages_with_columns": [2]},
            {"is_complex_layout": True},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as directory:
                result = self._run(directory, _safe_result(**overrides))
                self.assertIsNone(result)

    def test_pdf_inspector_rejects_missing_or_duplicate_page(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._run(
                directory,
                _safe_result(page_count=2),
                page_markers=True,
                pages=_pages_result((0, 0)),
            )
            self.assertIsNone(result)


class TestEngineSelection(unittest.TestCase):
    def test_default_engine_remains_opendataloader(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = _write_fake_pdf(directory)
            calls = []

            def convert(*args, **kwargs):
                calls.append(kwargs)
                output_dir = Path(kwargs["output_dir"])
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "paper.md").write_text("core", encoding="utf-8")

            fake_module = types.SimpleNamespace(convert=convert)
            with patch.dict(sys.modules, {"opendataloader_pdf": fake_module}):
                result = extract_pdf.extract_pdf(
                    str(pdf_path), output_dir=str(Path(directory) / "output")
                )
            self.assertTrue(result.endswith("paper.md"))
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["hybrid"], "off")

    def test_explicit_poppler_bypasses_opendataloader_import(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = _write_fake_pdf(directory)
            original_import = builtins.__import__

            def reject_opendataloader(name, *args, **kwargs):
                if name == "opendataloader_pdf":
                    raise AssertionError("opendataloader must not be imported")
                return original_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=reject_opendataloader):
                with patch.object(
                    extract_pdf,
                    "_extract_via_poppler",
                    return_value="poppler.md",
                ) as poppler:
                    result = extract_pdf.extract_pdf(
                        str(pdf_path),
                        output_dir=str(Path(directory) / "output"),
                        engine="poppler",
                    )
            self.assertEqual(result, "poppler.md")
            poppler.assert_called_once()

    def test_hybrid_rejected_for_non_opendataloader_engine(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = _write_fake_pdf(directory)
            with self.assertRaises(ValueError):
                extract_pdf.extract_pdf(str(pdf_path), hybrid=True, engine="poppler")


if __name__ == "__main__":
    unittest.main(verbosity=2)
