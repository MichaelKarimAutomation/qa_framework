# Task: commit-msg-trailer-hook

**Branch:** ai-coding-infrastructure
**Started:** 2026-05-17

## Goal
Add `.git/hooks/commit-msg` that rejects local commits missing
`AI-Verdict:` / `AI-Task:` trailers on this repo. Local-loop counterpart
to the CI merge gate in [.github/workflows/tests.yml](../../../.github/workflows/tests.yml).
Hook is non-mandatory per CLAUDE.md (the CI gate is the authoritative
enforcement); this just gives faster feedback at `git commit` time.

## Steps
- [x] Create task folder per CLAUDE.md §2
- [x] Initial PROGRESS.md
- [ ] Write `.git/hooks/commit-msg` (POSIX sh, matches existing post-commit style)
- [ ] Manual test: commit msg without trailers rejected; with trailers accepted; with CAP_REACHED accepted but warned
- [ ] Run `uv run pytest` (regression check — no pytest tests cover git hooks; this is just a "did I break anything else" sanity run)
- [ ] Generate `diff.patch`
- [ ] Run `ai_coding/reviewer.py` → `review_local.md`
- [ ] Judge verdict, write STATUS, commit with trailers

## Pending decisions
- Hook distribution: local-only `.git/hooks/` (matches existing post-commit
  pattern) vs tracked location with setup-script install. Defaulting to
  local-only; flag for user follow-up.

## Notes
- CLAUDE.md §3 calls for tests but git hooks don't fit pytest. Will note
  this in disagreements.log if reviewer flags it as a §3 violation.
