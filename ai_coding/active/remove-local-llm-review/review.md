# Deep review — remove-local-llm-review

## Scope reviewed
- CLAUDE.md full rewrite of §0, §2, §4, §6, §10, §11, §12, §13.
- README.md — two text edits.
- tools/hooks/{pre-commit, commit-msg, post-commit} rewrites for the new
  verdict surface (PASS | OVERRIDE) and artifact rename (review.md).
- tools/install-hooks.{ps1,sh} banner text.
- tools/hooks-selftest.{sh,ps1} — full rewrite of cases for the new
  verdict surface; ran the .sh version, 31/31 pass.
- .github/workflows/tests.yml merge gate now accepts PASS | OVERRIDE,
  drops `quarantine` from the path-pattern regex.
- .github/workflows/auto-archive.yml — new workflow.
- ai_coding/clear_queue.py — stripped quarantine logic, repurposed as
  documented backup utility.
- ai_coding/reviewer.py — deleted, copied to archived/reviewer.py.
- ai_coding/quarantine/ — directory removed (was empty, untracked).
- docs/ai_coding_workflow.html — full rewrite of step list and FAQs.
- .claude/hooks/promptsubmit_status.ps1 — string change to drop the
  reviewer.py invocation pointer.
- archived/README.md — new file describing the graveyard convention.

## Test status
- Inner test loop: tools/hooks-selftest.sh passed 31/31 on first run, no
  iterations needed.
- §5 full suite: `uv run pytest` → 37 passed in 25s. No regressions.

## Findings

### Resolved before this verdict
1. Auto-archive `git mv` was being called with a trailing-slash source
   path from the glob (`"$ACTIVE_DIR"/*/`). Most git versions accept this,
   but it's unportable. Fixed by stripping the trailing slash with bash
   parameter expansion (`d="${raw%/}"`).
2. Auto-archive workflow had no concurrency group. Two simultaneous
   merges to master would both checkout, both attempt their own `git mv`
   + `git push`, and the second would lose with non-fast-forward.
   Fixed by adding `concurrency: { group: auto-archive-master,
   cancel-in-progress: false }`.

### Considered, not flagged
- The auto-archive workflow uses three independent guards against
  self-triggering: (a) GitHub's default behavior of not firing downstream
  workflows for commits made with GITHUB_TOKEN, (b) `[skip ci]` in the
  subject line, (c) the `if: "!contains(...'[auto-archive]')"` job-level
  filter. Triple belt-and-suspenders is acceptable given the cost of a
  workflow loop is high.
- Removing `clear_queue.py`'s `--quarantine` flag is a breaking change to
  the CLI surface. Acceptable: the quarantine concept itself is gone, so
  the flag would have nothing to do. No CI workflow or script invokes
  this with `--quarantine` (verified by grepping the tree).
- The `archived/reviewer.py` copy shows up in git as a rename rather than
  a separate add + delete. That's accurate from a content-similarity
  standpoint and keeps the deprecation history clean.
- `ai_coding/quarantine/` was empty and untracked. Deleted with `rmdir`,
  no git operation needed. Its absence from the merge-gate regex
  (tests.yml line 35) is the only enforcement change.
- Hook `pre-commit` now checks STATUS=PASS when review.md ends with
  `VERDICT: PASS` (previously only the OVERRIDE branch checked STATUS).
  This closes a hole where a PASS review could ship with a non-PASS
  STATUS. New regression-pin tests `10b` and `10c` cover both directions.
- Hook `commit-msg` now rejects `VERDICT: FAIL` in review.md
  unconditionally. Under the old flow FAIL was the local model's verdict
  and was allowed if paired with OVERRIDE/CAP_REACHED escape hatches.
  Under the new flow FAIL is intermediate-only and never ships. Test 09
  covers this; the legacy escape-hatch test (old case 10) is replaced by
  case 10 covering OVERRIDE end-to-end.
- The legacy verdicts CAP_REACHED in STATUS and AI-Verdict are now
  explicitly rejected. New tests `08a` and `16a` are regression pins
  against a future rollback re-introducing them.

## Risk areas

- The auto-archive workflow has not yet been observed running in CI.
  First run will be on merging this PR into master. If the bash logic
  has a subtle bug, the result is a failed CI run with no folder moved
  and the human archives manually that one time. Low blast-radius.
- If a developer pushes directly to master outside of the PR flow with
  a commit message containing `[auto-archive]`, the workflow won't run.
  This is intentional self-guard; the only side-effect is a missed
  sweep, which the next master push will pick up.

## Verdict
VERDICT: PASS
