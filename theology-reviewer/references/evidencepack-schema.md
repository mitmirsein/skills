# EvidencePack Schema

`EvidencePack.json` is the handoff artifact between Phase 0 evidence gathering and Phase 1/2 review work.

## Top-Level Fields

- `schema_version`: currently `1`.
- `session_id`: review session timestamp id.
- `target`: source paper text/Markdown path.
- `query_set_path`: path to `QuerySet.json`.
- `abstracts`: normalized evidence records from Semantic Scholar, Google Scholar Labs, and google-scholar-quick.
- `semantic_scholar`: raw Semantic Scholar records.
- `google_scholar_labs`: raw Google Scholar Labs records.
- `google_scholar_quick`: raw google-scholar-quick records.
- `google_scholar`: combined Google Scholar-family records.
- `provenance`: source-level counts and run notes.
- `validation_warnings`: optional schema warnings.

## Normalized Evidence Record

- `schema_version`: currently `1`.
- `source_tool`: one of `semantic_scholar_api`, `google_scholar_semantic`, `google_scholar_quick`, or `unknown`.
- `source`: source label from the tool.
- `query`: query that produced the record.
- `rank`: result rank when available.
- `title`: paper title.
- `authors`: normalized author list.
- `authors_text`: raw author text if available.
- `year`: publication year or `null`.
- `venue`: journal/book/conference metadata.
- `url`: source URL.
- `doi`: DOI when available.
- `abstract`: abstract/snippet text used by Phase 1/2.
- `snippet`: shorter displayed excerpt.
- `citation`: primary formatted citation.
- `citation_variants`: all formatted citation rows captured from Scholar Labs.
- `citation_links`: citation export links such as BibTeX.
- `citation_status`: `ok`, `empty`, `missing_button`, `error:<ExceptionName>`, or empty for non-Labs sources.
- `citation_count`: integer citation count when available.
- `provenance`: `raw_source_tool`, `source_file`, and `retrieved_at`.
- `raw`: original tool record.

Records with `citation_status` other than `ok` are usable for topical context but incomplete as bibliography evidence.
