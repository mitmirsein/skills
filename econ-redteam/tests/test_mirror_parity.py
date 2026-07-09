"""정본↔미러 단일출처(SSOT) 강제 게이트.

정본 `.skills/econ-redteam`과 미러 `projects/omni-academic-framework/skills/econ-redteam`이
1바이트라도 어긋나면 FAIL한다. 정본을 고친 뒤 `scripts/econ_gate.py sync`를 돌리지 않으면
여기서 잡힌다.

미러가 없으면(단독 배포·다른 머신) skip — 그 경우 정본만 존재한다.

deps: Python 3.9+ stdlib only.
"""
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import econ_gate  # noqa: E402  (경로 주입 후 import — 대조 대상 목록의 단일 진실)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MirrorParityTests(unittest.TestCase):
    def test_mirror_matches_canonical(self) -> None:
        mirror = econ_gate.resolve_mirror()
        if mirror is None:
            self.skipTest("정본(.skills/econ-redteam)이 아닌 위치 — 미러에서 실행 중")
        if not mirror.is_dir():
            self.skipTest(f"미러 미존재({mirror}) — 단독 배포로 간주")

        canon_rels = econ_gate.sync_items(SKILL_DIR)
        self.assertGreater(len(canon_rels), 0, "대조 대상 파일이 없음 — 경로 설정 확인")

        for rel in canon_rels:
            with self.subTest(file=str(rel)):
                dst = mirror / rel
                self.assertTrue(dst.is_file(),
                                f"미러 누락: {rel} — `econ_gate.py sync` 실행 필요")
                self.assertEqual(_sha256(SKILL_DIR / rel), _sha256(dst),
                                 f"drift: {rel} — 정본 수정 후 sync 미실행")

        stale = set(econ_gate.sync_items(mirror)) - set(canon_rels)
        self.assertEqual(stale, set(), f"미러 전용 잔여 파일: {sorted(map(str, stale))}")


if __name__ == "__main__":
    unittest.main()
