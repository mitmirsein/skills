# Theology Reviewer AgentOps Spec

This file defines the skill-to-skill contracts for `theology-reviewer`. It intentionally excludes `MS_Brain.nosync/500 Parrehsia/parrehsia`; that frontend is not part of the automatic review pipeline.

## Core Roles

- `theology-reviewer`: orchestrates Phase 0 evidence gathering, Phase 1 review handoff, and Phase 2 verification.
- `projects/easy-review-system`: stores prompts, configs, validators, annotation tokens, and theological method checklists.
- `semantic-scholar`: returns fast structured paper metadata and abstracts.
- `google-scholar-semantic`: returns Scholar Labs JSONL with citation fields. It must use at most 4 queries per browser session and `citation_depth=all` by default.
- `google-scholar-quick`: returns lightweight Google Scholar result lists.
- `pdf-extractor`: converts PDFs to Markdown/Text before this skill runs.
- `paper-xray`: optional fast pre-brief before full review.

## Artifact Contracts

- Input to `theology-reviewer`: Markdown/Text paper file. PDF input must be converted first.
- Phase 0 output: `QuerySet.json`, `EvidencePack.json`, `ToolLog.json`.
- Phase 1 output: `handoff_packet.json`.
- Phase 2 output: `verified_claims.json`, `transparency_report.md`, `p2_handoff_packet.json`.
- Final review location: `MS_Brain.nosync/000 System/Inbox/Review_Reports`.
- Evidence location: `MS_Brain.nosync/000 System/Inbox/Evidence`.

## Operating Rules

- Do not publish or rewrite frontend files automatically.
- Do not fabricate bibliography entries. Use `[Evidence_Missing]` when evidence is incomplete.
- Treat `citation_status != "ok"` as incomplete bibliography evidence.
- Preserve both supporting and counter-evidence; unresolved tension is better than forced synthesis.
