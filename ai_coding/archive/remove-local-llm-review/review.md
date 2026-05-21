# Deep review: remove-local-llm-review (commit 2)

## Scope reviewed
Follow-up to the prior commit (ea14066). Text edits to strip historical
phrasing ("Claude's own", "no local LLM") that described what changed
rather than the current state, plus a session-wide em-dash scrub per
user feedback.

### Phrasing cleanup
- CLAUDE.md:31: `(Claude's own deep review output)` becomes `(deep review output)`.
- CLAUDE.md:68: `## 6. Deep Review (Claude's own, no local LLM)` becomes
  `## 6. Deep Review`.
- CLAUDE.md:69-74: body of §6 rephrased from "Claude re-reads... Claude
  writes..." to imperative voice ("Re-read... Write..."), matching the
  style of §4 and §5.
- .claude/hooks/promptsubmit_status.ps1:17: drop "Claude's own" from the
  §6 pointer in the injected pipeline-state message.

### Em-dash scrub (session-touched files only)
- CLAUDE.md: 10+ em-dashes replaced with `:`, `.`, `,`, or `()` per
  context.
- tools/hooks/pre-commit: 4 em-dashes in comments/error messages replaced.
- tools/hooks/commit-msg: 3 em-dashes in comments replaced.
- tools/hooks-selftest.sh: 9 em-dashes in case-comment headers replaced.
- tools/hooks-selftest.ps1: 2 em-dashes in inline comments replaced.
- .github/workflows/auto-archive.yml: 1 em-dash in the header comment.
- ai_coding/clear_queue.py: 1 em-dash in the docstring.
- archived/README.md: 1 em-dash in the prose.
- docs/ai_coding_workflow.html: 2 em-dashes in prose (already fixed
  before this scrub by user request).
- This file and PROGRESS.md: rewritten without em-dashes.

Em-dashes in files I did not author or substantially rewrite this
session (GUIDE.html, install-hooks.{sh,ps1}, post-commit, notify.py,
docs/index.rst, scripts/generate_docs.py, gh-pages-index.yml,
tests.yml lines I did not touch, archived/reviewer.py's preserved
historical content) are out of scope for this scrub.

## Test status
- hooks-selftest.sh: 31/31 (verified after the scrub).
- Full pytest suite: 37/37.

## Findings
None. Text-only edits across the touched files. No behavioral change,
no test signal change.

VERDICT: PASS
