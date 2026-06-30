#!/usr/bin/env python3
"""추출 엔진 정본 → 형제 스킬 미러 동기화기 (단일출처 강제).

이 디렉토리(`pdf-extractor`)가 추출 엔진(preflight·extract_pdf·post_cleaner·
healer·vision_*)의 **정본(SSOT)**이다. `paper-xray` 등 형제 스킬은 동일
엔진을 복제 보유하므로, 엔진을 수정할 때는 **반드시 이 정본에서 고친 뒤**
본 스크립트로 미러에 전파한다.

미러 무결성은 각 미러 스킬의 `tests/test_engine_parity.py`가 검증한다
(정본과 1바이트라도 어긋나면 FAIL).

사용:
    python3 scripts/sync_engine.py            # 미러 갱신
    python3 scripts/sync_engine.py --check    # 복사 없이 drift만 보고(불일치 시 exit 1)
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]   # .../.skills/pdf-extractor
SKILLS_ROOT = SKILL_DIR.parent                    # .../.skills
MIRROR_SKILLS = ("paper-xray",)                   # 엔진을 복제 보유하는 형제 스킬
ENGINE_SUBDIRS = ("scripts", "tests")             # 미러 대상 하위 폴더
SELF_NAME = Path(__file__).name                   # sync_engine.py 자신은 미러 제외


def engine_files() -> list[tuple[str, str]]:
    """(subdir, filename) — 정본에서 미러로 전파할 .py 전부."""
    items: list[tuple[str, str]] = []
    for sub in ENGINE_SUBDIRS:
        directory = SKILL_DIR / sub
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.py")):
            if path.name == SELF_NAME:
                continue
            items.append((sub, path.name))
    return items


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(check_only: bool) -> int:
    drift: list[str] = []
    copied = 0
    for mirror in MIRROR_SKILLS:
        mirror_dir = SKILLS_ROOT / mirror
        if not mirror_dir.is_dir():
            print(f"⏭️  미러 없음(건너뜀): {mirror}")
            continue
        for sub, name in engine_files():
            src = SKILL_DIR / sub / name
            dst = mirror_dir / sub / name
            if dst.exists() and sha256(src) == sha256(dst):
                continue
            if check_only:
                drift.append(f"{mirror}/{sub}/{name}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
                print(f"↪️  동기화: {mirror}/{sub}/{name}")
    if check_only:
        if drift:
            print("❌ drift 발견 (정본과 불일치):")
            for entry in drift:
                print(f"   - {entry}")
            print("→ python3 scripts/sync_engine.py 로 전파하십시오.")
            return 1
        print("✅ 모든 미러가 정본과 일치")
        return 0
    print(f"✅ 동기화 완료 (갱신 {copied}개)" if copied else "✅ 이미 최신 (변경 없음)")
    return 0


def main() -> int:
    return run(check_only="--check" in sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
