# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyhwp",
#     "html2text",
#     "beautifulsoup4",
#     "lxml",
# ]
# ///

"""
HWP/HWPX → Markdown 합체 변환기 (3단계 Fallback)

전략:
  1차: hwp5html (pyhwp) → html2text → Markdown  (HWP 5.0+ 전용)
  2차: LibreOffice headless → Pandoc → Markdown  (HWP 3.0/2.x 구형 포맷 구원)
  3차: 최종 실패 보고
"""

import time
import argparse
import subprocess
import shutil
import tempfile
import re
from pathlib import Path


# ──────────────────────────────────────────────
# 후처리: 마크다운 청소 (Pandoc/hwp5html 잔여물 제거)
# ──────────────────────────────────────────────
def cleanup_markdown(text):
    """HWP→HTML 변환 시 발생하는 잡음을 제거"""
    # 1. 콜론으로 시작하는 줄 제거 (스타일 찌꺼기)
    text = re.sub(r'^:.*$', '', text, flags=re.MULTILINE)
    # 2. {lang="en-US"}, {style="..."} 등 인라인 속성 블록 제거
    text = re.sub(r'\{[^}]*\}', '', text)
    # 3. ::: div 블록 제거 (Pandoc이 생성하는 래퍼)
    text = re.sub(r'^:::.*$', '', text, flags=re.MULTILINE)
    # 4. 빈 대괄호 링크 잔해 제거 (예: []  )
    text = re.sub(r'\[\]\s*', '', text)
    # 5. 이스케이프된 작은따옴표 정리
    text = text.replace("\\'", "'")
    # 6. 연속된 빈 줄 정리 (3줄 이상 → 2줄)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 7. 연속 역슬래시+줄바꿈 (Pandoc 하드 줄바꿈) 정리
    text = re.sub(r'\\\n', '\n', text)

    return text.strip()


# ──────────────────────────────────────────────
# 1차 엔진: hwp5html (pyhwp) → html2text
# ──────────────────────────────────────────────
def convert_via_hwp5html(hwp_path):
    """HWP 5.0+ 파일용. hwp5html로 HTML 생성 후 html2text로 변환."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_html_dir = Path(temp_dir) / "html_out"

        subprocess.run(
            ["hwp5html", "--output", str(output_html_dir), str(hwp_path)],
            check=True,
            capture_output=True,
            text=True,
        )

        html_file = next(output_html_dir.glob("index.*"), None)
        if not html_file:
            raise FileNotFoundError("hwp5html 출력에서 index 파일을 찾을 수 없음")

        import html2text
        h2t = html2text.HTML2Text()
        h2t.ignore_links = False
        h2t.ignore_images = True
        h2t.body_width = 0
        
        html_content = html_file.read_text(encoding="utf-8", errors="ignore")
        return cleanup_markdown(h2t.handle(html_content))


# ──────────────────────────────────────────────
# 2차 엔진: LibreOffice headless → Pandoc
# ──────────────────────────────────────────────
SOFFICE_PATHS = [
    "/usr/local/bin/soffice",
    "/opt/homebrew/bin/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
    "C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe",
    "soffice",  # PATH fallback
]

PANDOC_PATHS = [
    "/usr/local/bin/pandoc",
    "/opt/homebrew/bin/pandoc",
    "C:\\Program Files\\Pandoc\\pandoc.exe",
    "pandoc",  # PATH fallback
]


def find_executable(candidates):
    """주어진 후보 경로 중 실제로 존재하는 첫 번째 실행 파일 반환"""
    for path in candidates:
        if shutil.which(path):
            return path
    return None


def convert_via_libreoffice(hwp_path):
    """HWP 3.0/2.x 구형 파일용. LibreOffice → HTML → Pandoc → Markdown."""
    soffice = find_executable(SOFFICE_PATHS)
    if not soffice:
        raise FileNotFoundError("LibreOffice(soffice)를 찾을 수 없습니다.")

    pandoc = find_executable(PANDOC_PATHS)
    if not pandoc:
        raise FileNotFoundError("Pandoc을 찾을 수 없습니다.")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        # 한글 파일명 문제 방지를 위해 임시 ASCII 파일명으로 복사
        temp_hwp = temp_dir_path / f"input{hwp_path.suffix}"
        shutil.copy2(hwp_path, temp_hwp)

        # LibreOffice headless → HTML 변환
        result = subprocess.run(
            [soffice, "--headless", "--convert-to", "html", "--outdir", str(temp_dir_path), str(temp_hwp)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        html_file = temp_dir_path / "input.html"
        if not html_file.exists():
            raise Exception(f"LibreOffice 변환 실패: {result.stderr or result.stdout}")

        # Pandoc → Markdown 변환
        pandoc_result = subprocess.run(
            [pandoc, "-f", "html", "-t", "markdown", "--wrap=none", str(html_file)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if pandoc_result.returncode != 0:
            raise Exception(f"Pandoc 변환 실패: {pandoc_result.stderr}")

        return cleanup_markdown(pandoc_result.stdout)


# ──────────────────────────────────────────────
# 통합 변환 함수 (3단계 Fallback)
# ──────────────────────────────────────────────
def convert_hwp_to_md(hwp_path):
    """
    3단계 Fallback 전략:
      1차: hwp5html (HWP 5.0+)
      2차: LibreOffice headless (HWP 3.0/2.x)
      3차: 최종 실패
    """
    hwp_path = Path(hwp_path)
    errors = []

    # ── 1차: hwp5html ──
    try:
        content = convert_via_hwp5html(hwp_path)
        if content and content.strip():
            return content, "hwp5html"
    except Exception as e:
        errors.append(f"[1차 hwp5html] {str(e)[:80]}")

    # ── 2차: LibreOffice + Pandoc ──
    try:
        content = convert_via_libreoffice(hwp_path)
        if content and content.strip():
            return content, "libreoffice"
    except Exception as e:
        errors.append(f"[2차 LibreOffice] {str(e)[:80]}")

    # ── 3차: 최종 실패 ──
    raise Exception(" | ".join(errors))


# ──────────────────────────────────────────────
# 메인 실행부
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="HWP/HWPX → Markdown 합체 변환기 (3단계 Fallback)"
    )
    parser.add_argument("target_dir", type=str, nargs="?", default=".", help="변환할 타겟 폴더 경로")
    parser.add_argument("-o", "--output-dir", type=str, help="결과물을 저장할 출력 폴더 경로")
    args = parser.parse_args()

    target_dir = Path(args.target_dir)
    output_dir = Path(args.output_dir) if args.output_dir else None

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    # 파일 탐색 (대소문자 모두)
    files = []
    if target_dir.is_file():
        files.append(target_dir)
    else:
        for ext in ("*.hwp", "*.HWP", "*.hwpx", "*.HWPX", "*.h30", "*.H30"):
            files.extend(target_dir.rglob(ext))

    files = sorted(set(files))  # 중복 제거

    print(f"🚀 발견: {len(files)}개 파일 (3단계 Fallback 전략 가동)")
    if not files:
        print("대상 파일이 없습니다.")
        return

    ok = fail = skip = 0
    engine_stats = {"hwp5html": 0, "libreoffice": 0}
    failures = []
    start = time.time()

    for i, f in enumerate(files, 1):
        if output_dir:
            # 배치 변환 시 상대 경로 구조를 유지하여 파일명 충돌 방지
            rel = f.relative_to(target_dir) if not target_dir.is_file() else Path(f.name)
            md_path = (output_dir / rel).with_suffix(".md")
            md_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            # 기본 정책: 원본 파일과 동일한 경로에 저장
            md_path = f.with_suffix(".md")

        if md_path.exists():
            skip += 1
            continue

        try:
            content, engine = convert_hwp_to_md(f)

            if not content:
                fail += 1
                failures.append((f, "변환 결과 비어있음"))
                continue

            md_path.write_text(content, encoding="utf-8")
            ok += 1
            engine_stats[engine] += 1
            print(f"[{i}/{len(files)}] ✅ {f.name} ({engine})")

        except Exception as e:
            fail += 1
            failures.append((f, str(e)[:200]))
            print(f"[{i}/{len(files)}] ❌ {f.name}")

    elapsed = time.time() - start
    print(f"\n✨ 작업 완료! (소요시간: {elapsed:.1f}초)")
    print(f"성공: {ok} (hwp5html: {engine_stats['hwp5html']}, LibreOffice: {engine_stats['libreoffice']}) | 건너뜀: {skip} | 실패: {fail}")

    if failures:
        print("\n[상세 실패 목록]")
        for path, msg in failures:
            print(f"  - {path.name}: {msg}")


if __name__ == "__main__":
    main()
