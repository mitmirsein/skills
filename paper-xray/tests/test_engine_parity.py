"""엔진 단일출처(SSOT) 강제 게이트.

`paper-xray`가 복제 보유한 추출 엔진(scripts/·tests/의 .py)이 정본
`pdf-extractor`와 1바이트라도 어긋나면 FAIL한다. 정본에서 엔진을 고친 뒤
`pdf-extractor/scripts/sync_engine.py`를 돌리지 않으면 여기서 잡힌다.

정본(pdf-extractor)이 없으면(단독 배포) skip — 그 경우 미러가 곧 정본이다.
"""
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

MIRROR_SKILL = Path(__file__).resolve().parents[1]          # .../.skills/paper-xray
CANON_SKILL = MIRROR_SKILL.parent / "pdf-extractor"         # .../.skills/pdf-extractor
ENGINE_SUBDIRS = ("scripts", "tests")
EXCLUDE = {"sync_engine.py", "test_engine_parity.py"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class EngineParityTests(unittest.TestCase):
    def test_mirror_matches_canonical(self) -> None:
        if not CANON_SKILL.is_dir():
            self.skipTest("정본(pdf-extractor) 미존재 — 단독 배포로 간주")
        checked = 0
        for sub in ENGINE_SUBDIRS:
            canon_dir = CANON_SKILL / sub
            if not canon_dir.is_dir():
                continue
            for src in sorted(canon_dir.glob("*.py")):
                if src.name in EXCLUDE:
                    continue
                with self.subTest(file=f"{sub}/{src.name}"):
                    mirror = MIRROR_SKILL / sub / src.name
                    self.assertTrue(
                        mirror.exists(),
                        f"미러 누락: {sub}/{src.name} — pdf-extractor에서 sync_engine.py 실행 필요",
                    )
                    self.assertEqual(
                        _sha256(src),
                        _sha256(mirror),
                        f"엔진 drift: {sub}/{src.name} — 정본 수정 후 sync_engine.py 미실행",
                    )
                    checked += 1
        self.assertGreater(checked, 0, "검증된 엔진 파일이 없음 — 경로 설정 확인")


if __name__ == "__main__":
    unittest.main()
