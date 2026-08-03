"""PDF를 Markdown으로 추출하는 선택형 엔진 라우터.

의존성: 표준 라이브러리 + 선택 엔진(opendataloader-pdf, pdf-inspector) + Poppler.
실행: python scripts/extract_pdf.py --input <PDF_PATH> [--engine ENGINE]
"""

import os
import time
import argparse
import json
import shutil
import subprocess


PAGE_MARKER = "===== p.{n} ====="
SUPPORTED_ENGINES = ("opendataloader", "pdf-inspector", "poppler")


def _load_pdf_inspector():
    """pdf-inspector를 지연 import하고 미설치 상태를 호출자에게 알립니다."""
    try:
        import pdf_inspector
    except ImportError:
        print(
            "❌ pdf-inspector 엔진이 선택되었지만 `pdf_inspector` 모듈이 없습니다. "
            "`uv pip install -r requirements.txt` 또는 `pip install pdf-inspector`로 설치하십시오."
        )
        return None
    return pdf_inspector


def _as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_page_list(value):
    if value is None:
        return []
    if isinstance(value, (str, bytes)):
        value = [value]
    try:
        values = list(value)
    except TypeError:
        values = [value]
    pages = []
    for item in values:
        try:
            pages.append(int(item))
        except (TypeError, ValueError):
            continue
    return pages


def _pdf_inspector_gate(result):
    """단순 native-text만 fast lane 완료로 허용합니다."""
    pdf_type = str(getattr(result, "pdf_type", "unknown")).strip().lower()
    ocr_pages = _as_page_list(getattr(result, "pages_needing_ocr", []))
    encoding_issues = bool(getattr(result, "has_encoding_issues", False))
    complex_layout = bool(getattr(result, "is_complex_layout", False))
    columns = _as_page_list(getattr(result, "pages_with_columns", []))
    tables = _as_page_list(getattr(result, "pages_with_tables", []))

    if pdf_type != "text_based":
        print(
            f"❌ pdf-inspector 안전 게이트: pdf_type={pdf_type!r}. "
            "스캔·이미지·Mixed PDF는 이 엔진에서 완료 처리하지 않습니다."
        )
        if ocr_pages:
            print(f"   OCR 필요 페이지(1-based): {ocr_pages}")
        return False
    if ocr_pages:
        print(
            "❌ pdf-inspector 안전 게이트: OCR이 필요한 페이지가 있어 "
            f"완전 추출로 처리하지 않습니다 (1-based: {ocr_pages})."
        )
        return False
    if encoding_issues:
        print(
            "❌ pdf-inspector 안전 게이트: 글꼴 인코딩 이상이 감지되었습니다. "
            "Poppler 비교 추출 또는 Vision/OCR을 사용하십시오."
        )
        return False
    if complex_layout or columns or tables:
        signals = []
        if complex_layout:
            signals.append("is_complex_layout=true")
        if columns:
            signals.append(f"pages_with_columns={columns}")
        if tables:
            signals.append(f"pages_with_tables={tables}")
        print(
            "❌ pdf-inspector 안전 게이트: 복잡한 레이아웃은 fast lane에서 "
            f"완료 처리하지 않습니다 ({', '.join(signals)}). "
            "OpenDataLoader Hybrid 또는 Poppler를 검토하십시오."
        )
        return False
    return True


def _write_pdf_inspector_page_marked_markdown(
    output_dir,
    base_name,
    pages_result,
    page_count,
    start_page=1,
):
    """0-based page API를 기존 1-based 인용 마커로 변환합니다."""
    pages = list(getattr(pages_result, "pages", []) or [])
    expected_count = _as_int(page_count)
    if expected_count <= 0 or len(pages) != expected_count:
        print(
            "❌ pdf-inspector 페이지 결과 검증 실패: "
            f"기대 {expected_count}쪽, 실제 {len(pages)}쪽입니다."
        )
        return None

    page_indexes = []
    for page in pages:
        page_index = getattr(page, "page", None)
        try:
            page_indexes.append(int(page_index))
        except (TypeError, ValueError):
            print("❌ pdf-inspector 페이지 결과 검증 실패: page.page가 정수가 아닙니다.")
            return None
    expected_indexes = list(range(expected_count))
    if page_indexes != expected_indexes:
        print(
            "❌ pdf-inspector 페이지 결과 검증 실패: "
            f"0-based 페이지가 {page_indexes}이며 기대값 {expected_indexes}와 다릅니다."
        )
        return None

    page_ocr = _as_page_list(getattr(pages_result, "pages_needing_ocr", []))
    page_columns = _as_page_list(getattr(pages_result, "pages_with_columns", []))
    page_tables = _as_page_list(getattr(pages_result, "pages_with_tables", []))
    if page_ocr or page_columns or page_tables or bool(getattr(pages_result, "is_complex", False)):
        print(
            "❌ pdf-inspector 페이지 결과 검증 실패: 페이지별 OCR/복잡 레이아웃 "
            f"신호가 남아 있습니다 (ocr={page_ocr}, columns={page_columns}, tables={page_tables})."
        )
        return None

    lines = [
        "<!-- page-marked Markdown; cite with preserved page markers. -->",
        "",
    ]
    for page in pages:
        lines.append(PAGE_MARKER.format(n=start_page + int(page.page)))
        lines.append("")
        markdown = str(getattr(page, "markdown", "") or "").strip()
        if markdown:
            lines.append(markdown)
        lines.append("")

    marked_path = os.path.join(output_dir, f"{base_name}_paged.md")
    try:
        with open(marked_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).rstrip() + "\n")
    except OSError as exc:
        print(f"❌ pdf-inspector 페이지 Markdown 저장 실패: {exc}")
        return None
    return marked_path


def _extract_via_pdf_inspector(
    pdf_path,
    target_output_dir,
    base_name,
    page_markers,
    start_time,
    start_page=1,
):
    """pdf-inspector의 보수적 native-text fast lane을 실행합니다."""
    pdf_inspector = _load_pdf_inspector()
    if pdf_inspector is None:
        return None

    try:
        result = pdf_inspector.process_pdf(pdf_path)
    except Exception as exc:
        print(f"❌ pdf-inspector 추출 실패: {exc}")
        return None

    if not _pdf_inspector_gate(result):
        return None

    os.makedirs(target_output_dir, exist_ok=True)
    if page_markers:
        try:
            pages_result = pdf_inspector.extract_pages_markdown(pdf_path)
        except Exception as exc:
            print(f"❌ pdf-inspector 페이지별 Markdown 추출 실패: {exc}")
            return None
        marked_path = _write_pdf_inspector_page_marked_markdown(
            target_output_dir,
            base_name,
            pages_result,
            getattr(result, "page_count", 0),
            start_page,
        )
        if marked_path is None:
            return None
        duration = time.time() - start_time
        print(f"✅ pdf-inspector 페이지 마커 파일: {marked_path} ({duration:.2f}s)")
        return marked_path

    markdown = getattr(result, "markdown", None)
    if not isinstance(markdown, str) or not markdown.strip():
        print("❌ pdf-inspector가 완료 가능한 Markdown을 반환하지 않았습니다.")
        return None
    md_path = os.path.join(target_output_dir, f"{base_name}.md")
    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)
    except OSError as exc:
        print(f"❌ pdf-inspector Markdown 저장 실패: {exc}")
        return None
    duration = time.time() - start_time
    print(f"✅ pdf-inspector 생성된 파일: {md_path} ({duration:.2f}s)")
    return md_path


def _write_page_marked_markdown(output_dir, base_name, start_page=1):
    """Build citation-safe Markdown from opendataloader JSON page metadata."""
    json_path = os.path.join(output_dir, f"{base_name}.json")
    if not os.path.exists(json_path):
        json_files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
        if len(json_files) != 1:
            return None
        json_path = os.path.join(output_dir, json_files[0])

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    page_count = int(data.get("number of pages") or 0) if isinstance(data, dict) else 0
    pages = [[] for _ in range(max(1, page_count))]

    for kid in data.get("kids", []) if isinstance(data, dict) else []:
        if not isinstance(kid, dict):
            continue
        content = str(kid.get("content") or "").strip()
        if not content:
            continue
        try:
            idx = max(0, int(kid.get("page number") or 1) - 1)
        except (TypeError, ValueError):
            idx = 0
        while idx >= len(pages):
            pages.append([])
        pages[idx].append(content)

    marked_path = os.path.join(output_dir, f"{base_name}_paged.md")
    lines = [
        "<!-- page-marked Markdown; cite with preserved page markers. -->",
        "",
    ]
    for i, parts in enumerate(pages, start_page):
        lines.append(PAGE_MARKER.format(n=i))
        lines.append("")
        if parts:
            lines.append("\n\n".join(parts).strip())
        lines.append("")

    with open(marked_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    return marked_path


def _extract_via_poppler(pdf_path, target_output_dir, base_name, page_markers, start_time, start_page=1):
    """opendataloader 부재/실패 시 poppler(pdftotext -layout)로 폴백 추출.

    한글 논문에서 pypdf의 자간 분해 문제를 피하고 띄어쓰기를 보존한다.
    page_markers=True이면 폼피드(form feed) 페이지 경계마다 `===== p.N =====`를 박는다.
    """
    pdftotext = shutil.which("pdftotext")
    if pdftotext is None:
        print("❌ poppler(pdftotext)도 PATH에 없습니다 — 추출 불가. "
              "(macOS: brew install poppler 또는 MacPorts)")
        return None

    if page_markers:
        completed = subprocess.run(
            [pdftotext, "-layout", pdf_path, "-"],
            capture_output=True, text=True,
        )
        if completed.returncode != 0:
            print(f"❌ pdftotext 실패: {completed.stderr.strip()}")
            return None
        pages = completed.stdout.split("\f")
        while pages and not pages[-1].strip():
            pages.pop()
        lines = ["<!-- page-marked Markdown; cite with preserved page markers. -->", ""]
        for i, page_text in enumerate(pages, start_page):
            lines.append(PAGE_MARKER.format(n=i))
            lines.append("")
            lines.append(page_text.strip())
            lines.append("")
        marked_path = os.path.join(target_output_dir, f"{base_name}_paged.md")
        with open(marked_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).rstrip() + "\n")
        duration = time.time() - start_time
        print(f"✅ (poppler 폴백) 페이지 마커 파일: {marked_path} ({duration:.2f}s, {len(pages)}쪽)")
        return marked_path

    md_path = os.path.join(target_output_dir, f"{base_name}.md")
    completed = subprocess.run(
        [pdftotext, "-layout", pdf_path, md_path],
        capture_output=True, text=True,
    )
    if completed.returncode != 0:
        print(f"❌ pdftotext 실패: {completed.stderr.strip()}")
        return None
    duration = time.time() - start_time
    print(f"✅ (poppler 폴백) 생성된 파일: {md_path} ({duration:.2f}s)")
    return md_path


def extract_pdf(
    pdf_path,
    hybrid=False,
    output_dir="output",
    page_markers=False,
    start_page=1,
    engine="opendataloader",
):
    """
    선택한 엔진으로 PDF를 마크다운으로 변환합니다.

    Args:
        pdf_path (str): 입력 PDF 경로
        hybrid (bool): False(기본) = 일반 모드, True = Hybrid(Java+Docling) 모드.
            기본값을 False로 둔 이유: Hybrid 모드는 별도 서버
            (`uv run opendataloader-pdf-hybrid`) 기동이 선행되어야 하며,
            텍스트 PDF에는 불필요하다. CLI `--hybrid` 플래그와 기본값 일치.
        output_dir (str): 출력 디렉토리 경로
        page_markers (bool): True이면 JSON의 page number를 사용해
            `===== p.N =====` 마커가 박힌 Markdown을 별도 생성.
        start_page (int): 실제 논문 인쇄 시작 페이지 번호.
        engine (str): `opendataloader`(기본), `pdf-inspector`, `poppler` 중 하나.
            기존 호출 호환성을 위해 기본값은 opendataloader로 유지합니다.
    """
    engine = str(engine).strip().lower()
    if engine not in SUPPORTED_ENGINES:
        raise ValueError(
            f"지원하지 않는 엔진입니다: {engine!r}. "
            f"가능한 값: {', '.join(SUPPORTED_ENGINES)}"
        )
    if hybrid and engine != "opendataloader":
        raise ValueError("--hybrid는 engine=opendataloader에서만 사용할 수 있습니다.")
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF not found at {pdf_path}")
        return None

    filename = os.path.basename(pdf_path)
    base_name = os.path.splitext(filename)[0]

    # 논문별 전용 하위 폴더 생성 (예: output/논문명)
    target_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(target_output_dir, exist_ok=True)

    start_time = time.time()

    if engine == "poppler":
        print(
            f"🚀 poppler: Processing {filename} (Start Page: {start_page}) "
            f"→ Folder: {target_output_dir}..."
        )
        return _extract_via_poppler(
            pdf_path,
            target_output_dir,
            base_name,
            page_markers,
            start_time,
            start_page,
        )

    if engine == "pdf-inspector":
        print(
            f"🚀 pdf-inspector: Processing {filename} (Start Page: {start_page}) "
            f"→ Folder: {target_output_dir}..."
        )
        return _extract_via_pdf_inspector(
            pdf_path,
            target_output_dir,
            base_name,
            page_markers,
            start_time,
            start_page,
        )

    # 모드 선택
    mode_str = "docling-fast" if hybrid else "off"
    print(f"🚀 opendataloader: Processing {filename} (Mode: {mode_str}, Start Page: {start_page}) → Folder: {target_output_dir}...")

    # opendataloader 부재 시 poppler 폴백 (Intel Mac·미설치 환경 대응)
    try:
        import opendataloader_pdf
    except ImportError:
        print("⚠️ opendataloader-pdf 미설치 → poppler(pdftotext -layout) 폴백으로 전환합니다.")
        return _extract_via_poppler(pdf_path, target_output_dir, base_name, page_markers, start_time, start_page)

    try:
        # JSON + Markdown 동시 생성
        formats = ["json", "markdown"]

        opendataloader_pdf.convert(
            pdf_path,
            output_dir=target_output_dir,
            hybrid=mode_str,
            hybrid_mode="full" if hybrid else None,
            format=formats
        )

        # 생성된 .md 파일 경로 반환
        expected_md = os.path.join(target_output_dir, f"{base_name}.md")

        if page_markers:
            marked_md = _write_page_marked_markdown(target_output_dir, base_name, start_page)
            if marked_md:
                duration = time.time() - start_time
                print(f"✅ 성공! 페이지 마커 파일: {marked_md} ({duration:.2f}s)")
                return marked_md

        if os.path.exists(expected_md):
            duration = time.time() - start_time
            print(f"✅ 성공! 생성된 파일: {expected_md} ({duration:.2f}s)")
            return expected_md
        else:
            # 디렉토리 내 파일 목록으로 진단
            files_in_output = os.listdir(target_output_dir)
            print(f"⚠️ 기대 경로({expected_md}) 없음. 출력 디렉토리 내용: {files_in_output}")
            # .md 파일이 하나라면 그것을 반환
            md_files = [f for f in files_in_output if f.endswith(".md")]
            if len(md_files) == 1:
                fallback = os.path.join(target_output_dir, md_files[0])
                print(f"💡 대체 경로 사용: {fallback}")
                return fallback
            return None

    except Exception as e:
        print(f"❌ opendataloader 추출 실패: {e}")
        if "Hybrid server" in str(e):
            print("💡 Tip: 별도 터미널에서 'uv run opendataloader-pdf-hybrid' 를 먼저 실행하세요.")
        print("⚠️ poppler(pdftotext -layout) 폴백을 시도합니다.")
        return _extract_via_poppler(pdf_path, target_output_dir, base_name, page_markers, start_time, start_page)


def main():
    parser = argparse.ArgumentParser(
        description="PDF → Markdown 선택형 추출기 (신학 논문 특화)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  일반 모드:  uv run python extract_pdf.py --input paper.pdf
  pdf-inspector: uv run python extract_pdf.py --input paper.pdf --engine pdf-inspector
  Poppler:      uv run python extract_pdf.py --input paper.pdf --engine poppler
  페이지 마커: uv run python extract_pdf.py --input paper.pdf --page-markers
  Hybrid 모드: uv run python extract_pdf.py --input paper.pdf --hybrid
  출력 지정:   uv run python extract_pdf.py --input paper.pdf --output /path/to/output
        """
    )
    parser.add_argument("--input", "-i", required=True, help="입력 PDF 파일 경로")
    parser.add_argument(
        "--hybrid", action="store_true",
        help="opendataloader Hybrid 변환 모드 활성화 (별도 서버 필요)"
    )
    parser.add_argument(
        "--engine",
        choices=SUPPORTED_ENGINES,
        default="opendataloader",
        help="추출 엔진 (기본: opendataloader; pdf-inspector/poppler는 opt-in)",
    )
    parser.add_argument(
        "--page-markers", action="store_true",
        help="JSON page number 기반 `===== p.N =====` 마커 포함 Markdown 생성"
    )
    parser.add_argument(
        "--start-page", type=int, default=1,
        help="실제 논문 인쇄 시작 페이지 번호 (기본값: 1)"
    )
    parser.add_argument("--output", "-o", default="output", help="출력 디렉토리 (기본: output/)")

    args = parser.parse_args()
    try:
        result = extract_pdf(
            args.input,
            hybrid=args.hybrid,
            output_dir=args.output,
            page_markers=args.page_markers,
            start_page=args.start_page,
            engine=args.engine,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if result:
        print(f"\n📎 다음 단계: post_cleaner → healer 로 정제")
        print(f"   uv run python scripts/post_cleaner.py \"{result}\"")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
