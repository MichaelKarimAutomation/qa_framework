# PROGRESS: drop-post-commit-diff-snapshots

Branch: feat/drop-post-commit-diff-snapshots

## Goal

Stop the post-commit hook from writing per-commit `diff_<ts>_<sha>.patch`
snapshots into `ai_coding/active|archive/<task>/`. The files duplicated
information git already records, were gitignored (so never part of the
repo record), and orphaned in `active/` after the auto-archive workflow
moved the task folder.

## Done

- Branch cut from master.
- Task folder created.
- tools/hooks/post-commit: removed the routing block and the
  git-diff-to-file block. The hook now parses trailers, logs commits
  missing AI-Task to UNROUTED.log, and fires a desktop notification.
- tools/hooks-selftest.{sh,ps1}: cases 20-23 rewritten to assert the
  new contract (no diff_*.patch written, no active stub created) under
  all four routing scenarios. Header comments updated.
- .gitignore: removed the dead `ai_coding/**/diff_*_*.patch` rule.
- 37 orphan `diff_*_*.patch` files physically removed from
  ai_coding/active|archive/ (local cleanup; the files were never tracked).
- CLAUDE.md §8: rewrote as a factual statement of the hook's behavior.
- hooks-selftest: 31/31 green on both bash and PowerShell variants.
- Full pytest: 37/37 green.
- Deep review: PASS.

## Remaining

- Commit.
