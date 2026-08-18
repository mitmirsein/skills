#!/usr/bin/env python3
"""
Dual Slide & Presenter HTML Builder
Generates a synchronized pair of HTML files:
1. [name]_slides.html   - Main fullscreen presentation deck with canvas drawing tools.
2. [name]_presenter.html - Presenter view with timer, clock, speaker notes, and jump buttons.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def sanitize_channel_name(title: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", title.strip().lower())
    return f"slide_sync_{cleaned[:30]}"


def build_dual_slides(deck_data: dict, output_dir: Path, base_name: str = "presentation") -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    
    title = deck_data.get("title", "Presentation")
    description = deck_data.get("description", "")
    slides_data = deck_data.get("slides", [])
    
    if not slides_data:
        raise ValueError("deck_data must contain at least one slide in 'slides'")
    
    channel_name = sanitize_channel_name(base_name)
    slides_filename = f"{base_name}_slides.html"
    presenter_filename = f"{base_name}_presenter.html"
    
    slides_path = output_dir / slides_filename
    presenter_path = output_dir / presenter_filename
    
    # 1. Build slide titles and speeches
    titles = []
    speeches = []
    slides_html_parts = []
    total_slides = len(slides_data)
    
    for idx, slide in enumerate(slides_data, start=1):
        s_title = slide.get("title", f"Slide {idx}")
        s_speech = slide.get("speaker_notes", slide.get("speech", ""))
        titles.append(f"{idx}. {s_title}")
        speeches.append(s_speech)
        
        # Build individual slide HTML if raw HTML is not provided
        if "html" in slide:
            slides_html_parts.append(slide["html"])
        else:
            tag = slide.get("tag", "TOPIC")
            heading = slide.get("heading", s_title)
            body_content = slide.get("content_html", f"<p>{html.escape(slide.get('text', ''))}</p>")
            page_str = f"{idx:02d} / {total_slides:02d}"
            
            slide_block = f"""    <!-- SLIDE {idx}: {html.escape(s_title)} -->
    <section class="slide{' active' if idx == 1 else ''}" data-slide="{idx}">
      <div class="slide-header">
        <div class="header-left">
          <span class="eyebrow-tag">{html.escape(tag)}</span>
          <span class="header-divider">|</span>
          <span class="header-title">{html.escape(s_title)}</span>
        </div>
        <span class="header-page">{page_str}</span>
      </div>
      <div class="slide-body">
        <h2 class="slide-heading">{html.escape(heading)}</h2>
        {body_content}
      </div>
    </section>"""
            slides_html_parts.append(slide_block)
            
    combined_slides_html = "\n\n".join(slides_html_parts)
    
    # Read templates
    main_template = (TEMPLATES_DIR / "main_slides_template.html").read_text(encoding="utf-8")
    presenter_template = (TEMPLATES_DIR / "presenter_view_template.html").read_text(encoding="utf-8")
    
    # Replace variables in main template
    main_html = main_template
    main_html = main_html.replace("{{TITLE}}", html.escape(title))
    main_html = main_html.replace("{{DESCRIPTION}}", html.escape(description))
    main_html = main_html.replace("{{SLIDES_HTML}}", combined_slides_html)
    main_html = main_html.replace("{{SPEECHES_JSON}}", json.dumps(speeches, ensure_ascii=False))
    main_html = main_html.replace("{{TITLES_JSON}}", json.dumps(titles, ensure_ascii=False))
    main_html = main_html.replace("{{CHANNEL_NAME}}", channel_name)
    main_html = main_html.replace("{{PRESENTER_HTML_FILENAME}}", presenter_filename)
    
    # Replace variables in presenter template
    pres_html = presenter_template
    pres_html = pres_html.replace("{{TITLE}}", html.escape(title))
    pres_html = pres_html.replace("{{TOTAL_SLIDES}}", str(total_slides))
    pres_html = pres_html.replace("{{SPEECHES_JSON}}", json.dumps(speeches, ensure_ascii=False))
    pres_html = pres_html.replace("{{TITLES_JSON}}", json.dumps(titles, ensure_ascii=False))
    pres_html = pres_html.replace("{{CHANNEL_NAME}}", channel_name)
    
    slides_path.write_text(main_html, encoding="utf-8")
    presenter_path.write_text(pres_html, encoding="utf-8")
    
    return slides_path, presenter_path


def main():
    parser = argparse.ArgumentParser(description="Build synchronized dual slides (Presentation & Presenter View)")
    parser.add_argument("deck_json", type=Path, help="Path to deck.json data file")
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("."), help="Output directory")
    parser.add_argument("-n", "--name", type=str, default="deck", help="Base name for generated files")
    
    args = parser.parse_args()
    
    if not args.deck_json.exists():
        print(f"Error: {args.deck_json} not found.", file=sys.stderr)
        sys.exit(1)
        
    deck_data = json.loads(args.deck_json.read_text(encoding="utf-8"))
    s_path, p_path = build_dual_slides(deck_data, args.output_dir, args.name)
    
    print(f"Successfully generated dual slides:")
    print(f"  1. Main Slides:     {s_path}")
    print(f"  2. Presenter View:  {p_path}")


if __name__ == "__main__":
    main()
