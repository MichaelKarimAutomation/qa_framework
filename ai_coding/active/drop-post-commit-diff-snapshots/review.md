# Deep Review: drop-post-commit-diff-snapshots

## Scope

Six tracked file changes (plus the §2 artifacts for this task):

- `tools/hooks/post-commit`: dropped the routing block (TASK_DIR
  tri-branch, mkdir fallback) and the diff-write block
  (DIFF_FILE, EMPTY_TREE, `git diff > DIFF_FILE`). Kept trailer
  parsing, UNROUTED.log entry for commits missing AI-Task, and
  `fire_notify`. Header rewritten as a factual statement.
- `tools/hooks-selftest.sh` and `.ps1`: cases 20-23 rewritten to
  assert the new contract (no `diff_*.patch` written, no active
  stub created) under all four routing scenarios. New helpers
  `count_diff_patches` / `Count-DiffPatches` centralize the count.
  Header comments updated.
- `.gitignore`: removed the now-dead `ai_coding/**/diff_*_*.patch`
  rule.
- `CLAUDE.md` §8: rewritten as a factual description matching the
  new hook responsibility. No backward-looking justification prose.

37 orphan `diff_*_*.patch` files were physically removed from
ai_coding/{active,archive}/ as a one-shot local cleanup. They were
untracked locally and never entered git, so the deletion is invisible
in the commit diff.

## Findings

### Correctness

- Hook trailer parsing is unchanged: same `grep -E '^AI-Task:'` and
  `grep -E '^AI-Verdict:'` logic, same `tr -d '\r'` for CRLF safety,
  same `head -1` to pick the first match.
- Missing-trailer path is preserved: UNROUTED.log append + urgent
  notify + exit 0, identical semantics.
- `fire_notify` is unchanged: same python lookup, same fire-and-forget
  background invocation, same notify.log fallback when python is
  missing.
- Removed code had two visible effects that are now gone:
  1. Writing `diff_<ts>_<sha>.patch` into the task folder.
  2. Creating `ai_coding/active/<task>/` as a side effect on commits
     whose task folder didn't exist on disk.

  Effect (1) is the explicit goal of this change. Effect (2) was a
  silent fallback that could only fire when a commit reached
  post-commit despite (a) lacking a §2 task folder and (b) having a
  valid `AI-Task:` trailer. The pre-commit hook already rejects such
  commits when CLAUDE.md §2 is followed; the only way through is
  `--no-verify`, which is already off-pipeline. Removing the silent
  fallback is appropriate: an off-pipeline bypass commit does not
  deserve a forensic stub created for it.

### Selftest assertions

- All four post-commit cases (20-23) now check: zero `diff_*.patch`
  in both active and archive task dirs AND no active stub directory.
  This is stronger than the old assertions (the old test only
  checked one side of the routing decision per case).
- Glob `diff_*.patch` is intentional: matches the snapshot pattern
  (`diff_<ts>_<sha>.patch`) but not the canonical `diff.patch`
  artifact, because the latter has no underscore after `diff`.
  Verified the canonical artifact wouldn't be miscounted.
- Bash helper uses `find -maxdepth 1 -name 'diff_*.patch' | wc -l |
  tr -d ' '`. MSYS `find` on Git for Windows supports both flags;
  `tr -d ' '` strips the leading whitespace `wc -l` emits on MSYS,
  which would otherwise cause the numeric `-eq` comparison to fail.
  The selftest runs green on both bash and PowerShell, confirming
  this.
- PowerShell helper uses `Get-ChildItem -Filter 'diff_*.patch'`. The
  -Filter literal-underscore semantics match the bash glob.

### Gitignore removal

The dead rule `ai_coding/**/diff_*_*.patch` is removed. Verified that
no other producer in the live tree writes files matching this
pattern: the only grep matches are inside historical diff.patch
artifact snapshots (themselves containing the now-removed hook
source) and `archived/reviewer.py`, which is deprecated and not
imported anywhere. Future commits cannot accidentally re-introduce
ignored snapshots through this path.

### CLAUDE.md §8

Rewritten as a factual statement of what the hook does. No
backward-looking "earlier did X, now Y because Z" prose. Matches the
new hook header style.

### Documentation

PROGRESS.md updated to reflect the actual final state: orphan
physical cleanup happened, all tests green, deep review concluded.
No forward-references to artifacts not yet produced.

## Bugs / Defects

None.

## Security

Hook surface shrank. No new shell expansions, no new file writes, no
new external calls. Notification payload still derives from
trailer-extracted strings which have been through the same `tr -d
'\r'` normalization as before. No new injection vectors.

## Tests

- hooks-selftest.sh: 31 passed, 0 failed.
- hooks-selftest.ps1: 31 passed, 0 failed.
- uv run pytest: 37 passed, 0 failed.

VERDICT: PASS
