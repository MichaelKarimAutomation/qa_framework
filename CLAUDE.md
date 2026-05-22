# CLAUDE.md: Standing Rules for Claude Code (qa_framework)

This file is the operating contract for Claude Code in this repository. It
encodes deliberate decisions. Do not deviate without the user explicitly
changing this file.

## 0. Environment (do not assume; these are fixed facts)
- Repo root: C:\Coding\qa_framework
- OS: Windows
- Test command: `uv run pytest`

## 1. Workflow Scope
- One feature at a time, in one Claude Code session.
- Every feature is developed on its own branch split from main. Never work
  directly on main. Never commit to main.
- Concurrency is handled structurally by branch isolation + per-task folders
  + the AI-Task commit trailer (see §7, §8). There is no lockfile by design.
- Every code edit in this repository is feature work regardless of size.
  There is no casual mode. Doc tweaks, folder renames, gitignore changes,
  single-line fixes, and `git mv` archive operations all trigger the
  §2-§7 pipeline (task folder, tests if applicable, §5 full-suite run,
  §6 deep review, commit with trailers). A small request is not an exemption.

## 2. Task Folder (create at start of every task)
For task `<task>`, create:

    ai_coding/active/<task>/
      diff.patch          (final diff for the commit)
      disagreements.log   (see §6)
      PROGRESS.md         (see §9)
      review.md           (deep review output)
      STATUS              (single token: PASS | OVERRIDE)

`<task>` is a short kebab-case name (e.g. `login-retry-fix`). It is the
identity used in the AI-Task trailer and for hook routing. If a folder for a
different task already exists in active/, that is expected and fine. Folders
are isolated; do not move or disturb another task's folder.

Note: `review.md` may end with `VERDICT: FAIL` as an intermediate state
during the §6 loop. FAIL is never a STATUS or AI-Verdict value; it only
lives in `review.md` until the verdict becomes PASS (after a fix) or
OVERRIDE (after human acceptance). See §6.

## 3. Implementation + Test Rule
- Implement the requested change AND write/update tests for it.
- The task is NOT complete until tests pass.

## 4. Inner Test-Fix Loop (cap = 3)
- During the loop, run only affected/relevant tests (not the full suite) to
  conserve tokens.
- Fix failures, re-run. Maximum 3 iterations.
- If still failing after 3 iterations:
  - Tag: `[TEST_CAP_REACHED]`
  - Write it to disagreements.log (§6)
  - STATUS file is NOT written (no commit happens)
  - **HALT. Do NOT commit.** Notify the user (§10). Wait for human action.

## 5. Final Full-Suite Run (once, after inner loop is green)
- After affected tests pass, run the FULL suite exactly once: `uv run pytest`.
- If the full suite passes, proceed to §6 deep review.
- If the full suite FAILS (regression in untouched code):
  - Tag: `[FULL_SUITE_FAILED]`
  - Write it to disagreements.log
  - **HALT. Do NOT commit.** Notify the user. Wait for human action.
  - This is an objective failure, NOT a judgment call. It must never fall
    through to the review step or be overridden.

## 6. Deep Review
- Generate the diff, save to ai_coding/active/<task>/diff.patch.
- Re-read the diff, the touched source files, and the relevant test
  output. The goal: find real bugs, correctness defects, security issues,
  significant logic problems. Ignore pure style and formatting.
- Write the full review to review.md, ending with exactly one line:
  `VERDICT: PASS` or `VERDICT: FAIL`.
  - **PASS** writes STATUS=PASS, proceed to §7 commit.
  - **FAIL** shows findings in chat and asks the human, in one concise
    line: *"Deep review found issues: fix, or accept as OVERRIDE?"*
    - *fix*: address the findings, regenerate the diff, re-run the deep
      review. Repeat until PASS or until the human accepts OVERRIDE. There
      is no cap on this loop; each iteration is human-gated by the chat
      prompt, so the human controls when to stop.
    - *override*: rewrite review.md's last line to `VERDICT: OVERRIDE`,
      append an `[OVERRIDE]` entry to disagreements.log with the accepted
      issues and the human's stated reasoning, write STATUS=OVERRIDE,
      proceed to §7 commit.

### disagreements.log format

    [YYYY-MM-DD HH:MM] [OVERRIDE] commit <sha>
      Findings: "<list of issues Claude flagged>"
      Human reasoning: "<why accepted>"

    [YYYY-MM-DD HH:MM] [TEST_CAP_REACHED]   (no commit, halted)
      Failing tests: [list]
      Attempts: 3

    [YYYY-MM-DD HH:MM] [FULL_SUITE_FAILED]   (no commit, halted)
      Failing tests: [list]

## 7. Commit
Only reached when §4 passed, §5 passed, and §6 resolved (PASS or OVERRIDE).
- Commit to the working branch only. NEVER main.
- Write STATUS file with the final verdict token: PASS | OVERRIDE
- The commit message MUST include both trailers, on their own lines, at the
  end of the message:

      AI-Verdict: PASS | OVERRIDE
      AI-Task: <task>

  These are load-bearing. The merge gate and the post-commit hook depend on
  them. Omitting them is a defect, not a shortcut.

## 8. Post-Commit (automatic, do not invoke manually)
The post-commit hook parses the AI-Task / AI-Verdict trailers on the
just-made commit, logs any commit missing the AI-Task trailer to
ai_coding/UNROUTED.log, and fires a desktop notification. It writes
nothing into the task folder. You do not call this; it fires on commit.
Just ensure the trailer is correct.

## 9. PROGRESS.md Checkpointing
- Update ai_coding/active/<task>/PROGRESS.md at MEANINGFUL BOUNDARIES only:
  (a) inner loop green, (b) post deep-review judgment, (c) post-commit.
  NOT every step. Per-step writes spend the very budget they protect.
- Record: current task, branch, steps completed, steps remaining, pending
  decisions/issues.
- Record verdicts and iteration descriptions only (e.g. `pytest 22/22 green`,
  `deep review PASS`, `iteration 3: <what changed>`). Do NOT write commit SHAs
  or `(pending)` / `(TBD)` markers that forward-reference artifacts which
  do not yet exist. The git log is the authoritative SHA record; duplicating
  SHAs in PROGRESS.md just creates staleness.
- Honest limitation (do not overstate to the user): nothing COMMITTED is
  lost on session death; in-loop progress since the last boundary may repeat.
  The test-fix loop is the least-protected phase. Do not claim "nothing is
  lost."
- Claude Pro usage is NOT programmatically readable. Do not attempt to query
  remaining usage or build a usage meter; it is impossible. PROGRESS.md is
  the recovery substitute, nothing more.

## 10. Notifications
Routine completion and urgent halts are surfaced via desktop notification
(plyer), triggered by the post-commit hook. Urgent =
[TEST_CAP_REACHED], [FULL_SUITE_FAILED]. Routine = clean commit.

## 11. Auto-Archive on Merge
A GitHub Actions workflow (`.github/workflows/auto-archive.yml`) runs on
every push to `master`. It scans `ai_coding/active/` for task folders whose
STATUS is `PASS` or `OVERRIDE` and moves them to `ai_coding/archive/`.
The workflow's own commit uses `[skip ci]` so it does not loop. You never
move a finished task folder by hand.

OVERRIDE folders are archived alongside PASS. The chat-only OVERRIDE
acceptance in §6 is the gate, and once it's committed and merged, the
folder no longer belongs in `active/`.

## 12. /clear Timing
After the §7 commit and before starting the next feature, prompt the user:
"Commit done. Run /clear before starting the next feature."

You cannot clear your own context, so this is a reminder, not an action.
Running /clear yourself wipes the build reasoning that the post-commit
context relies on, so don't prompt for it earlier in the flow.

## 13. Archiving Deprecated Source Files
When a feature is removed (not just refactored), copy the original file(s)
to `archived/` BEFORE deleting from the source location. Add a one-line
header noting the deprecation date and what replaced it. This preserves
implementation history without bloating the running tree.

`archived/` is for source files. `ai_coding/archive/` is for completed
task-pipeline folders. Do not confuse the two.

## 14. Forbidden Literals in Commit Messages and PR Bodies
Claude must NOT include any of the literals listed below in a commit
message, PR title, or PR body it authors in this repo. The list is
expected to grow over time; new entries follow the same shape (the
literal, its variants, why it's forbidden).

**Permission carve-out** (applies to every entry below): if Claude
believes a specific commit or PR genuinely needs to include a
forbidden literal, Claude MUST ask the user first, in plain language,
naming the literal and the reason. Claude proceeds only on explicit
yes. No silent inclusion, no after-the-fact disclosure.

This rule binds Claude only. It is not enforced by a git hook and
does not constrain human contributors or CI-generated commits (the
auto-archive workflow in particular is allowed to keep using these
markers in its own commit message template, since its commits are
made by CI and never pass through this directive).

### Entries

1. **GitHub skip-CI markers.** All variants:
   - `[skip ci]`, `[ci skip]`, `[no ci]`
   - `[skip actions]`, `[actions skip]`
   - `[skip-ci]`, `[ci-skip]`
   - `***NO_CI***`
   - `skip-checks: true` (trailer form)

   *Why:* a squash-merge inherits the PR body verbatim into a master
   commit. If the body mentions the marker (even in prose describing
   what it does), GitHub Actions skips ALL push-triggered workflows
   for that commit. Past incident: PR #14 merged with `[skip ci]`
   in the body describing the auto-archive workflow, and the merge
   silently ran no workflows. To refer to the marker in prose,
   indirection like *"the GitHub skip-CI marker"* or *"the
   CI-bypass phrase"* works.
