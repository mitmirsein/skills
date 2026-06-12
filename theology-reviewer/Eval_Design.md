# Theology Reviewer Eval Design

Use these checks after changing `theology-reviewer`, `easy-review-system`, or the linked evidence skills.

## Offline Checks

Run:

```bash
uv run python .skills/theology-reviewer/scripts/review_engine.py --self-test
PYTHONPYCACHEPREFIX=/tmp/theology_reviewer_pycache uv run python -m py_compile .skills/theology-reviewer/scripts/review_engine.py
```

Expected:

- Config paths resolve.
- Google Scholar Semantic contract enforces `max_queries_per_session <= 4`.
- `citation_depth` is valid.
- EvidencePack validation accepts a minimal normalized pack.
- Contradiction heuristic can identify explicit counter-evidence.

## Fixture Plan

- Fixture A: short Markdown paper with clear author/year citations.
- Fixture B: review draft with `[Critique]`, `[Defense]`, `[Conclusion]`, and one intentionally unsupported claim.
- Fixture C: EvidencePack with one supporting item and one counter-evidence item.

## Pass Criteria

- Phase 0 writes `QuerySet.json`, `EvidencePack.json`, and `ToolLog.json`.
- Phase 1 writes `handoff_packet.json` and includes annotation tokens.
- Phase 2 writes `verified_claims.json`, `transparency_report.md`, and `p2_handoff_packet.json`.
- Claims are never marked `Anchored` solely because a title exists; source and evidence text must be preserved.
- Records with missing citations remain usable for context but are flagged as incomplete bibliography evidence.
