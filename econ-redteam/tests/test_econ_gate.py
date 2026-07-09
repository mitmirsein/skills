"""econ_gate.py 결정론 게이트 단위 테스트.

deps: Python 3.9+ stdlib only (unittest). `python3 -m unittest discover -s tests` 또는 pytest로 실행.

게이트를 CLI로 호출해 *종료 코드*를 검증한다 — 게이트가 실제로 무는지가 검증 대상이지
내부 함수의 반환값이 아니다. 4종 구획: 정상 / 경계 / 누락 / 변조.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
GATE = SKILL_DIR / "scripts" / "econ_gate.py"
FIX = Path(__file__).resolve().parent / "fixtures"

TARGET_ANTE = str(FIX / "target_exante.md")
TARGET_POST = str(FIX / "target_expost.md")
PARAGRAPHS = str(FIX / "paragraphs_exante.json")
VALID = str(FIX / "critique_valid.json")

EXIT_OK, EXIT_SCRIPT_ERROR, EXIT_GATE = 0, 1, 2


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(GATE), *args],
                          capture_output=True, text=True)


def mutate(tmpdir: str, name: str, fn) -> str:
    """정상 패킷을 고의 변조해 임시 파일로 떨군다 — red 재현용."""
    packet = json.loads(Path(VALID).read_text(encoding="utf-8"))
    fn(packet)
    path = Path(tmpdir) / name
    path.write_text(json.dumps(packet, ensure_ascii=False), encoding="utf-8")
    return str(path)


class ClassifyTests(unittest.TestCase):
    """classify는 자문일 뿐 판정이 아니다 — 항상 exit 0."""

    def test_always_advisory(self):
        for target in (TARGET_ANTE, TARGET_POST):
            with self.subTest(target=target):
                r = run("classify", "--target", target)
                self.assertEqual(r.returncode, EXIT_OK, r.stderr)
                self.assertIn("자문 신호", r.stdout)

    def test_lexicon_leans_correctly(self):
        self.assertIn("ex-ante 쪽", run("classify", "--target", TARGET_ANTE).stdout)
        self.assertIn("ex-post 쪽", run("classify", "--target", TARGET_POST).stdout)


class CheckNormalTests(unittest.TestCase):
    """정상: 완전한 패킷은 모든 차단 플래그를 켜도 통과한다."""

    def test_valid_packet_passes_all_gates(self):
        r = run("check", "--critiques", VALID, "--target", TARGET_ANTE,
                "--fail-on-schema", "--fail-on-ungrounded",
                "--fail-on-missing-axis", "--fail-on-mode-unset")
        self.assertEqual(r.returncode, EXIT_OK, r.stderr)
        self.assertIn("스키마 0 / ungrounded 0 / 누락 축 0 / 경고 0", r.stdout)

    def test_valid_packet_with_paragraph_ids(self):
        r = run("check", "--critiques", VALID, "--target", TARGET_ANTE,
                "--paragraphs", PARAGRAPHS, "--fail-on-ungrounded", "--fail-on-schema")
        self.assertEqual(r.returncode, EXIT_OK, r.stderr)

    def test_report_is_written(self):
        with tempfile.TemporaryDirectory() as td:
            out = str(Path(td) / "report.md")
            run("check", "--critiques", VALID, "--target", TARGET_ANTE, "--report", out)
            report = Path(out).read_text(encoding="utf-8")
            self.assertIn("축 커버리지", report)
            self.assertIn("✅ 전 축 커버", report)


class CheckBoundaryTests(unittest.TestCase):
    """경계: 정규화 후에만 일치하는 인용, 차단 플래그 없는 위반."""

    def test_quote_matches_only_after_nfkc_and_whitespace_norm(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                for c in p["critiques"]:
                    if c["id"] == "C1":
                        c["source_quote"] = "재정승수는\n  1.3으로   가정하였고"
            path = mutate(td, "norm.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE,
                    "--fail-on-ungrounded", "--fail-on-schema")
            self.assertEqual(r.returncode, EXIT_OK, r.stderr)

    def test_violation_without_flag_is_report_only(self):
        """도입 곡선: --fail-on-* 없이는 위반이 있어도 차단하지 않는다."""
        r = run("check", "--critiques", str(FIX / "critique_ungrounded.json"),
                "--target", TARGET_ANTE)
        self.assertEqual(r.returncode, EXIT_OK, r.stderr)
        self.assertIn("ungrounded 2", r.stdout)

    def test_duplicate_anchor_warns_but_does_not_block(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                quote = next(c for c in p["critiques"] if c["id"] == "C1")["source_quote"]
                next(c for c in p["critiques"] if c["id"] == "C2")["source_quote"] = quote
                next(c for c in p["critiques"] if c["id"] == "C2")["paragraph_id"] = "P_0002"
            path = mutate(td, "dup.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE,
                    "--fail-on-schema", "--fail-on-ungrounded")
            self.assertEqual(r.returncode, EXIT_OK, r.stderr)
            self.assertIn("앵커 중복", r.stderr)


class CheckMissingTests(unittest.TestCase):
    """누락: 축·모드·필수 필드가 빠지면 해당 플래그가 차단한다."""

    def test_missing_axes_blocked(self):
        args = ("check", "--critiques", str(FIX / "critique_missing_axis.json"),
                "--target", TARGET_ANTE)
        self.assertEqual(run(*args).returncode, EXIT_OK)                       # 플래그 없으면 통과
        r = run(*args, "--fail-on-missing-axis")
        self.assertEqual(r.returncode, EXIT_GATE, r.stdout)
        self.assertIn("누락 축 3", r.stdout)

    def test_mode_unset_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            path = mutate(td, "nomode.json", lambda p: p.pop("mode"))
            r = run("check", "--critiques", path, "--target", TARGET_ANTE,
                    "--fail-on-mode-unset")
            self.assertEqual(r.returncode, EXIT_GATE, r.stdout)
            self.assertIn("mode 미선언", r.stdout)

    def test_missing_steelman_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                next(c for c in p["critiques"] if c["id"] == "C2")["steelman"] = ""
            path = mutate(td, "nosteel.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE, "--fail-on-schema")
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("steelman 비어 있음", r.stderr)

    def test_directive_without_refs_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                next(c for c in p["critiques"] if c["id"] == "D1").pop("refs")
            path = mutate(td, "noref.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE, "--fail-on-schema")
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("refs 없음", r.stderr)


class CheckTamperTests(unittest.TestCase):
    """변조: 유령 인용·표 셀 인용·범주 오류·허수아비는 반드시 잡힌다."""

    def test_ghost_quote_and_table_cell_are_ungrounded(self):
        r = run("check", "--critiques", str(FIX / "critique_ungrounded.json"),
                "--target", TARGET_ANTE, "--fail-on-ungrounded")
        self.assertEqual(r.returncode, EXIT_GATE, r.stdout)
        self.assertIn("C1 source_quote가 대상 산문에 없음", r.stderr)   # 날조
        self.assertIn("C5 source_quote가 대상 산문에 없음", r.stderr)   # 표 셀은 산문 아님

    def test_category_error_blocked(self):
        r = run("check", "--critiques", str(FIX / "critique_category_error.json"),
                "--target", TARGET_ANTE, "--fail-on-schema")
        self.assertEqual(r.returncode, EXIT_GATE, r.stdout)
        self.assertIn("범주 오류: mode=ex-ante인데 axis=E1", r.stderr)

    def test_steelman_identical_to_critique_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                c = next(c for c in p["critiques"] if c["id"] == "C3")
                c["steelman"] = c["critique"]
            path = mutate(td, "strawman.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE, "--fail-on-schema")
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("최강 버전을 세우지 않았음", r.stderr)

    def test_paragraph_id_not_in_map_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                next(c for c in p["critiques"] if c["id"] == "C1")["paragraph_id"] = "P_9999"
            path = mutate(td, "badpid.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE,
                    "--paragraphs", PARAGRAPHS, "--fail-on-ungrounded")
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("실존하지 않음", r.stderr)

    def test_quote_in_prose_but_wrong_paragraph_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                next(c for c in p["critiques"] if c["id"] == "C1")["paragraph_id"] = "P_0003"
            path = mutate(td, "wrongpid.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE,
                    "--paragraphs", PARAGRAPHS, "--fail-on-ungrounded")
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("문단 안에 없음", r.stderr)

    def test_mixed_mode_requires_matching_part(self):
        with tempfile.TemporaryDirectory() as td:
            def wreck(p):
                p["mode"] = "mixed"          # A축 지적인데 part 미태깅
            path = mutate(td, "mixed.json", wreck)
            r = run("check", "--critiques", path, "--target", TARGET_ANTE, "--fail-on-schema")
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("part='proposal'여야 함", r.stderr)


class InputErrorTests(unittest.TestCase):
    """입력 오류는 게이트 실패와 같은 exit 2 — 조용히 통과시키지 않는다."""

    def test_missing_file(self):
        r = run("check", "--critiques", "no/such.json", "--target", TARGET_ANTE)
        self.assertEqual(r.returncode, EXIT_GATE)
        self.assertIn("[입력 오류]", r.stderr)

    def test_broken_json(self):
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.json"
            bad.write_text("{ not json", encoding="utf-8")
            r = run("check", "--critiques", str(bad), "--target", TARGET_ANTE)
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("파싱 실패", r.stderr)


class PrepareDecideTests(unittest.TestCase):
    """판정 패킷 이디엄: prepare는 비차단, 실질 판정은 코드가 하지 않는다."""

    def test_prepare_emits_unjudged_slots_and_excludes_directives(self):
        with tempfile.TemporaryDirectory() as td:
            out = str(Path(td) / "wl.json")
            r = run("prepare", "--critiques", VALID, "--out", out)
            self.assertEqual(r.returncode, EXIT_OK, r.stderr)
            wl = json.loads(Path(out).read_text(encoding="utf-8"))
            self.assertEqual(len(wl["items"]), 6)                       # D1·D2 제외
            self.assertTrue(all(i["verdict"] == "UNJUDGED" for i in wl["items"]))
            self.assertTrue(all(i["is_strongest"] == "UNJUDGED" for i in wl["items"]))

    def test_decide_on_unjudged_worklist_passes(self):
        with tempfile.TemporaryDirectory() as td:
            out = str(Path(td) / "wl.json")
            run("prepare", "--critiques", VALID, "--out", out)
            r = run("decide", "--worklist", out, "--fail-on-strawman",
                    "--fail-on-unengaged", "--fail-on-flattened")
            self.assertEqual(r.returncode, EXIT_OK, r.stderr)
            self.assertIn("미판정 6", r.stdout)

    def test_decide_blocks_each_gap_independently(self):
        wl = str(FIX / "worklist_strawman.json")
        self.assertEqual(run("decide", "--worklist", wl).returncode, EXIT_OK)   # 리포트-only
        for flag, marker in (("--fail-on-strawman", "허수아비 공격"),
                             ("--fail-on-unengaged", "최강 반론 미대면"),
                             ("--fail-on-flattened", "평탄화")):
            with self.subTest(flag=flag):
                r = run("decide", "--worklist", wl, flag)
                self.assertEqual(r.returncode, EXIT_GATE, r.stdout)
                self.assertIn(marker, r.stderr)

    def test_decide_rejects_nonstandard_verdict(self):
        with tempfile.TemporaryDirectory() as td:
            wl = json.loads((FIX / "worklist_strawman.json").read_text(encoding="utf-8"))
            wl["items"][0]["verdict"] = "아마도"
            path = Path(td) / "bad_wl.json"
            path.write_text(json.dumps(wl, ensure_ascii=False), encoding="utf-8")
            r = run("decide", "--worklist", str(path))
            self.assertEqual(r.returncode, EXIT_GATE)
            self.assertIn("verdict 비표준", r.stderr)


if __name__ == "__main__":
    unittest.main()
