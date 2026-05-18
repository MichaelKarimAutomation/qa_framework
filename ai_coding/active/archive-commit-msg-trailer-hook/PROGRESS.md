# Task: archive-commit-msg-trailer-hook

**Branch:** chore/archive-commit-msg-trailer-hook
**Started:** 2026-05-17

## Goal
The `commit-msg-trailer-hook` task was merged in upstream commit 5c8ab65
but its task folder remained in `ai_coding/active/`. Move it to
`ai_coding/archive/` per CLAUDE.md §11 (consumption-based clearing of
reviewed clean-pass folders).

## Iterations
1. `git mv ai_coding/active/commit-msg-trailer-hook
   ai_coding/archive/commit-msg-trailer-hook` (five tracked files: PROGRESS.md,
   STATUS, diff.patch, disagreements.log, review_local.md). Gitignored
   hook artifact `diff_20260517T223907Z_3522ebf.patch` followed via the
   on-disk rename. Commit cbacfc2 with trailers `AI-Verdict: PASS`,
   `AI-Task: archive-commit-msg-trailer-hook`.

## Notes
- §2-§6 of CLAUDE.md were NOT performed at the time of cbacfc2 — this
  folder + its STATUS, diff.patch, review_local.md are being backfilled
  in a follow-up commit (task `backfill-cbacfc2-artifacts`). This file
  is the retrospective record, not real-time progress.
- §3 (implement + tests): N/A — pure file rename, no behavioral code,
  no tests to add.
- §5 (full suite): not run at the time of cbacfc2 (skipped in lapse).
  The backfill commit re-runs the full suite to satisfy §5 against the
  combined working tree.
- §6 (local review): not run at the time of cbacfc2 (skipped in lapse).
  Backfilled now by running reviewer.py against the cbacfc2 diff.
