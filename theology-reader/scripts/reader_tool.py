import sys
import argparse
from pathlib import Path
import fitz  # PyMuPDF

def read_docs(target: str, limit: int = 20) -> str:
    """
    Reads documents from the directory OR a specific file and prints them to stdout.
    Support formats: PDF, MD, TXT, HTML.
    """
    path = Path(target)
    if not path.exists():
        return f"Error: Path {target} does not exist."

    files = []
    if path.is_file():
        files = [path]
    elif path.is_dir():
        # Added HTML support
        files = sorted(list(path.glob("*.pdf")) + list(path.glob("*.md")) + list(path.glob("*.txt")) + list(path.glob("*.html")))
        files = files[:limit]
    else:
        return f"Error: {target} is not a file or directory."

    output = []
    output.append(f"--- START OF DOCUMENT DUMP ({len(files)} files) ---")
    
    for f in files:
        output.append(f"\n### FILE: {f.name}")
        content = ""
        try:
            if f.suffix.lower() == ".pdf":
                with fitz.open(f) as doc:
                    for page in doc:
                        content += page.get_text() + "\n"
            else:
                # Text-based files (md, txt, html)
                content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = f"[Error reading file: {e}]"
            
        # Increased limit for thorough single-file analysis
        if len(content) > 100000:
            content = content[:100000] + "\n...[Truncated]"
            
        output.append(content)
        output.append(f"--- END OF FILE: {f.name} ---")
        
    return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to file or directory")
    args = parser.parse_args()
    print(read_docs(args.path))
