# .skills 스킬 인덱스 (INDEX)

갱신: 2026-06-18 / `python3 _meta/validate.py --index`로 재생성

gws/(Google Workspace 하위 스킬 98개)는 외부 유래 묶음으로 본 인덱스에서 제외.

## academic-search (14)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| crossref-journal-searcher | active | A | Searches the Crossref /works API filtered to a curated list of premium theology journals (… |
| google-scholar-quick | active | A | Fast Google Scholar scrape via Playwright CLI (CDP) — grabs paper lists and URLs with near… |
| google-scholar-semantic | active | A | Deep Google Scholar Labs recon via Playwright (CDP) — question-first semantic querying, ci… |
| ixtheo-searcher | active | A | Searches Tübingen's Index Theologicus (IxTheo) via OpenSearch/SRU and parses MARCXML for p… |
| journal-collector | active | A | Maintains curated journal registries (theology_journals.json, economics_journals.json — IS… |
| kci-api-searcher | active | A | Searches KCI (Korea Citation Index) via the official OpenAPI (open.kci.go.kr) and returns … |
| nlk-biblio-searcher | active | A | Searches the National Library of Korea OpenAPI (www.nl.go.kr) by title, author, or ISBN an… |
| nlk-interlinker | active | A | Queries the National Library of Korea LOD SPARQL endpoint for a control number's owl:sameA… |
| nlk-subject-searcher | active | A | Expands a subject term through the National Library of Korea LOD SPARQL — preferred/non-pr… |
| notebooklm-researcher | active | A | Operates NotebookLM as a consolidated research library — multi-source acquisition over 5 c… |
| paper-xray | active | A | Extracts a PDF to high-fidelity Markdown, heals parsing noise, and reverse-engineers the c… |
| riss-searcher | active | A | Searches RISS (Korean academic research service) for journal articles, theses, and books —… |
| semantic-scholar | active | A | Searches papers and citation networks via the Semantic Scholar Graph API (s2_runner.py) an… |
| tawp | active | A | Runs the Theological Academic Writing Pipeline (TAWP) — from a one-line natural-language i… |

## dev-tools (15)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| agent-forge | active | A | Designs, generates, validates, and optimizes agent skills with a Meta-Harness outer loop —… |
| code-simplifier | active | A | Simplifies code — token diet, complexity reduction, and abstraction flattening while prese… |
| git-workflow | active | A | Standardized Git workflow — Conventional Commits, branch strategy, and pull-request flow. … |
| github-ops | active | A | Automates GitHub operations via the gh CLI — repo creation, remote wiring, issues, and PRs… |
| insane-search | active | A | Auto-bypass for blocked websites — tries every method until one works. Use when WebFetch r… |
| langgraph-supervisor | active | A | Orchestrates large multi-step jobs as a Supervisor-Worker state machine — plan, delegate t… |
| lightpanda-recon | active | A | Headless browser recon via the Lightpanda binary — faster and lighter than Playwright for … |
| log-miner | active | A | Mines unstructured conversation logs (.logs/) for reusable knowledge — flash ideas, code s… |
| prompt-engineer | active | A | Designs model-optimized prompts using per-model strategy references (Claude XML/adaptive t… |
| react-components | active | A | Converts Stitch design screens into modular Vite/React components — logic isolated into ho… |
| stealth-browser | active | A | Playwright browser automation with isolated local profiles and optional CDP providers — ta… |
| tech-architect | active | A | Keeps a project's structure clean and its code maintainable — directory reorganization wit… |
| tech-reviewer | active | A | Reviews code for logic and safety — shadow-path tracing (empty/error/ latency paths beyond… |
| tech-strategist | active | A | Reframes a request to find the "10-star product" hidden inside it, scouts repos/landscape,… |
| tech-tdd | active | A | Drives development through the Red-Green-Refactor cycle — acceptance criteria first, faili… |

## media (12)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| academic-illustrator | active | A | Transforms theological/humanities text into publication-quality academic diagrams via a vi… |
| create-slide-from-markdown | active | A | Generates an open-slide deck from a Markdown or Obsidian note — handles frontmatter, headi… |
| create-slide-image-prompts | active | A | Builds image-generation prompts for Master Of Slide decks from a distilled GPT Image 2 che… |
| epub-bindery | active | A | Compiles Markdown files into a publication-grade EPUB ebook via pandoc — chapters, metadat… |
| hwp-converter | active | A | Converts HWP/HWPX (Korean word processor) documents to Markdown on both macOS and Windows,… |
| lecture-video-generator | active | A | Orchestrates the existing lecture_video_generator project pipeline to turn a theology lect… |
| media-factory | active | A | Creative studio — generates high-quality AI images ("holy aesthetic" presets) and converts… |
| pdf-extractor | active | A | Extracts PDFs to high-fidelity Markdown using structural hybrid engines, elite Vision-base… |
| remotion-studio | active | A | Generates videos programmatically with Remotion (code-as-video), edge-tts narration, and J… |
| slide | active | A | Turns a Markdown/Obsidian document into a Master Of Slide deck and edits existing decks — … |
| yt-digest | active | A | Extracts transcripts from YouTube URLs via yt-dlp, cleans them up, and produces structured… |
| yt-subtitle-helper | active | A | Coordinates the YouTube subtitle workflow — download via yt-dlp, LLM spelling correction a… |

## theology (18)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| barth-kd-navigator | active | A | Reads Karl Barth's Kirchliche Dogmatik (KD) from the German text, translates it into Korea… |
| bible-meditation | active | A | Accompanies the user's daily Bible meditation in three phases — Don Camillo-persona theolo… |
| faith-compass | active | A | Interactive theological exploration companion — guides a user through a topic in four card… |
| rise-battleground-map | active | A | Maps the contested terrain of a theological topic across 7 axes of tension (objective/subj… |
| sermon-insight | active | A | Converts a theological paper's argument into a sermon insight package — decompiling the ex… |
| theology-chunker | active | A | Ingests theological PDFs and texts into the msn_th_db JSONL archive — pre-ingestion metada… |
| theology-citation-linker | active | A | Parses temporary citation anchors ([Ref: ...]) in a Markdown draft, maps them to EvidenceP… |
| theology-discourse-mapper | active | A | Extracts scholars (Actors), claims, and concepts from a theological text using the omni-ac… |
| theology-exegesis | active | A | Performs scholarly exegesis of a biblical or theological text through four academic lenses… |
| theology-local-searcher | active | A | Searches the local Theology AI Lab JSONL archive (msn_th_db) with 3-way multilingual lexic… |
| theology-pdf-maker | active | A | Compiles theological Markdown into publication-grade PDF (Brill, Noto Serif KR, SBL Hebrew… |
| theology-reader | active | A | Fast document loader — bulk-reads PDF/MD/TXT/HTML files in a folder into the agent's conte… |
| theology-redteam | active | A | Adversarially attacks a theological outline (TOC) and minimal ontology before writing begi… |
| theology-research | active | A | Orchestrates the full theological research survey pipeline — multilingual query expansion,… |
| theology-reviewer | active | A | Reviews a specific theological paper across eight dimensions (structure, argument, compari… |
| theology-scholar | active | A | Top-tier theological research engine ('Cathedral') — primary-text analysis (PAF), hypothes… |
| theology-terminology-linter | active | A | Lints a document for inconsistent Korean renderings of the same theological term (equivoca… |
| theology-translator | active | A | Translates theological texts (DE/EN → KO) through an orchestrator-led, role-isolated team … |

## utilities (11)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| batch-operator | active | A | Runs large-scale parallel file processing and bulk code migrations (a /batch-style operato… |
| btw | active | A | Handles quick side questions without polluting the main task context — answers briefly, th… |
| continuous-learner | active | A | Learns durable user preferences from session behavior — scaffolding questions, discovery o… |
| design-md | active | A | Designs and renders UI/UX from a single source of truth (design.md SSOT) by composing focu… |
| dictionary-editor | active | A | Writes encyclopedic theological dictionary articles — multilingual lemma standards (EN/DE/… |
| grafeo-connector | active | A | Connects the msn_th_db corpus and TOSK ontology for fused search — BM25 text axis with chu… |
| mole-manager | active | A | Automates macOS diagnostics, cleanup, optimization, and monitoring with the Mole CLI (tw93… |
| ontology-builder | active | A | Extracts knowledge-graph elements from text — entities, evidence-backed relations, and apo… |
| research-mentor | active | A | Socratic theological research mentor — develops a vague interest into a defensible academi… |
| thoughtbox-lite | active | A | Cookbook of thinking strategies for the Sequential Thinking MCP — efficient reasoning patt… |
| visual-feedback | active | A | Closes the loop between a user's visual selection in the browser and the source code — rea… |

## vault (9)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| arc-librarian | active | A | Standardizes vault notes into the ARC architecture — assigns category codes (100 Theology … |
| digital-curator | active | A | Analyzes a useful website or database URL and registers it in the vault's Digital_Library_… |
| knowledge-archivist | active | A | Collects web articles and documents into the vault with /collect (defuddle-first extractio… |
| note-share | active | A | Publishes an Obsidian note to the web via Advanced URI and the Share Note plugin (Just Sha… |
| obsidian-cli | active | A | Operates the Obsidian vault through the official Obsidian CLI (v1.12.x+) — note CRUD, sear… |
| obsidian-web-clipper | active | A | Clips a single web page into clean Markdown with official Obsidian Web Clipper-compatible … |
| vault-query | active | A | Searches the MS_Brain vault with strict separation between I-Library (others' scholarship)… |
| wiki | active | A | Runs the MS_Brain vault operations engine: inbox intake, classification, wiki composing/me… |
| zettel-capture | active | A | Captures a sentence, insight, or source into an atomic Zettelkasten card (Fleeting/Literat… |

## writing (5)

| 스킬 | 상태 | 등급 | 설명 |
|---|---|---|---|
| clear-english-writer | active | A | Translates and refines Korean theological, homiletic, and academic texts into publication-… |
| clear-korean-writer | active | A | Opt-in Korean prose polishing and AI-tell removal — reduces AI-generated patterns (transla… |
| eng-student-consultant | active | A | Manages the English academy workflow — generates student counseling reports in the Obsidia… |
| slash-criticalthink | active | A | Self red-teams the AI's own just-produced answer (code, architecture, paper outline) — dis… |
| voca-guide | active | A | Builds a high-quality vocabulary textbook PDF (13-step storyline card-news format, light m… |
