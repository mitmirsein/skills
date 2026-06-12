import os
import time
import argparse
import json


PAGE_MARKER = "===== p.{n} ====="


def _write_page_marked_markdown(output_dir, base_name):
    """Build a citation-safe Markdown file from opendataloader JSON page metadata."""
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
        "<!-- pdf-extractor page-marked Markdown; cite with preserved page markers. -->",
        "",
    ]
    for i, parts in enumerate(pages, 1):
        lines.append(PAGE_MARKER.format(n=i))
        lines.append("")
        if parts:
            lines.append("\n\n".join(parts).strip())
        lines.append("")

    with open(marked_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    return marked_path


def extract_pdf(pdf_path, hybrid=False, output_dir="output", page_markers=False):
    """
    opendataloader-pdf 엔진으로 PDF를 마크다운으로 변환합니다.

    Args:
        pdf_path (str): 입력 PDF 경로
        hybrid (bool): False(기본) = 일반 모드, True = Hybrid(Java+Docling) 모드.
            기본값을 False로 둔 이유: Hybrid 모드는 별도 서버
            (`uv run opendataloader-pdf-hybrid`) 기동이 선행되어야 하며,
            텍스트 PDF에는 불필요하다. CLI `--hybrid` 플래그와 기본값 일치.
        output_dir (str): 출력 디렉토리 경로
        page_markers (bool): True이면 JSON의 page number를 사용해
            `===== p.N =====` 마커가 박힌 Markdown을 별도 생성.
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF not found at {pdf_path}")
        return None

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(pdf_path)
    base_name = os.path.splitext(filename)[0]

    # 모드 선택
    mode_str = "docling-fast" if hybrid else "off"
    print(f"🚀 opendataloader: Processing {filename} (Mode: {mode_str})...")

    start_time = time.time()
    try:
        import opendataloader_pdf

        # JSON + Markdown 동시 생성
        formats = ["json", "markdown"]

        opendataloader_pdf.convert(
            pdf_path,
            output_dir=output_dir,
            hybrid=mode_str,
            hybrid_mode="full" if hybrid else None,
            format=formats
        )

        # 생성된 .md 파일 경로 반환
        expected_md = os.path.join(output_dir, f"{base_name}.md")

        if page_markers:
            marked_md = _write_page_marked_markdown(output_dir, base_name)
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
            files_in_output = os.listdir(output_dir)
            print(f"⚠️ 기대 경로({expected_md}) 없음. 출력 디렉토리 내용: {files_in_output}")
            # .md 파일이 하나라면 그것을 반환
            md_files = [f for f in files_in_output if f.endswith(".md")]
            if len(md_files) == 1:
                fallback = os.path.join(output_dir, md_files[0])
                print(f"💡 대체 경로 사용: {fallback}")
                return fallback
            return None

    except Exception as e:
        print(f"❌ 추출 실패: {e}")
        if "Hybrid server" in str(e):
            print("💡 Tip: 별도 터미널에서 'uv run opendataloader-pdf-hybrid' 를 먼저 실행하세요.")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="opendataloader PDF → Markdown 추출기 (신학 논문 특화)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  일반 모드:  uv run python extract_pdf.py --input paper.pdf
  페이지 마커: uv run python extract_pdf.py --input paper.pdf --page-markers
  Hybrid 모드: uv run python extract_pdf.py --input paper.pdf --hybrid
  출력 지정:   uv run python extract_pdf.py --input paper.pdf --output /path/to/output
        """
    )
    parser.add_argument("--input", "-i", required=True, help="입력 PDF 파일 경로")
    parser.add_argument(
        "--hybrid", action="store_true",
        help="Hybrid 변환 모드 활성화 (Java+Docling, 스캔본/복잡한 레이아웃 권장)"
    )
    parser.add_argument(
        "--page-markers", action="store_true",
        help="JSON page number 기반 `===== p.N =====` 마커 포함 Markdown 생성"
    )
    parser.add_argument("--output", "-o", default="output", help="출력 디렉토리 (기본: output/)")

    args = parser.parse_args()
    result = extract_pdf(
        args.input,
        hybrid=args.hybrid,
        output_dir=args.output,
        page_markers=args.page_markers,
    )

    if result:
        print(f"\n📎 다음 단계: post_cleaner → healer 로 정제")
        print(f"   uv run python scripts/post_cleaner.py \"{result}\"")


if __name__ == "__main__":
    main()
