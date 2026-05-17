# CLAUDE.md — Standing Rules for Claude Code (qa_framework)

This file is the operating contract for Claude Code in this repository. It
encodes deliberate decisions. Do not deviate without the user explicitly
changing this file.

## 0. Environment (do not assume — these are fixed facts)
- Repo root: C:\Coding\qa_framework
- OS: Windows
- Test command: `uv run pytest`
- Local review model: `qwen3-coder:30b` via Ollama HTTP API at
  http://localhost:11434 — NEVER the ollama CLI (VS Code PATH staleness).
- Fallback models if 30b underperforms: `deepseek-coder-v2:16b`,
  `qwen2.5-coder` (documented only; do not switch without user instruction).

## 1. Workflow Scope
- One feature at a time, in one Claude Code session.
- Every feature is developed on its own branch split from main. Never work
  directly on main. Never commit to main.
- Concurrency is handled structurally by branch isolation + per-task folders
  + the AI-Task commit trailer (see §7, §8). There is no lockfile by design.

## 2. Task Folder (create at start of every task)
For task `<task>`, create:

    ai_coding/active/<task>/
      diff.patch          (final diff for the commit)
      disagreements.log   (see §6)
      PROGRESS.md         (see §9)
      review_local.md     (local AI review output)
      STATUS              (single token: PASS | CAP_REACHED | OVERRIDE)

`<task>` is a short kebab-case name (e.g. `login-retry-fix`). It is the
identity used in the AI-Task trailer and for hook routing. If a folder for a
different task already exists in active/, that is expected and fine — folders
are isolated; do not move or disturb another task's folder.

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
  - Set STATUS file is NOT written (no commit happens)
  - **HALT. Do NOT commit.** Notify the user (§10). Wait for human action.

## 5. Final Full-Suite Run (once, after inner loop is green)
- After affected tests pass, run the FULL suite exactly once: `uv run pytest`.
- If the full suite passes → proceed to §6 local review.
- If the full suite FAILS (regression in untouched code):
  - Tag: `[FULL_SUITE_FAILED]`
  - Write it to disagreements.log
  - **HALT. Do NOT commit.** Notify the user. Wait for human action.
  - This is an objective failure, NOT a judgment call. It must never fall
    through to the review step or be overridden.

## 6. Local AI Review + Judgment
- Generate the diff, save to ai_coding/active/<task>/diff.patch.
- Send the diff to the local model via reviewer.py (HTTP API).
- The local model returns prose ending with `VERDICT: PASS` or
  `VERDICT: FAIL` on the last line. Save full output to review_local.md.
- You (Claude Code) are the JUDGE, not a blind executor:
  - Legitimate issue → fix it, regenerate diff, re-run local review.
    This counts toward the OUTER cap (= 2 iterations).
  - Disagreement (model is wrong / nitpicking / not applicable) → record an
    `[OVERRIDE]` entry in disagreements.log with your reasoning, then proceed.
    The verdict is advisory, not binding.
  - If the outer cap (2) is exhausted with unresolved issues:
    - Tag: `[CAP_REACHED]`
    - Record unresolved issues + last attempt summary in disagreements.log
    - Proceed to commit on the working branch (this is allowed by design),
      then notify the user with urgency.

### disagreements.log format
    [YYYY-MM-DD HH:MM] [OVERRIDE] commit <sha>
      Local model flagged: "<issue>"
      Claude Code reasoning: "<why overridden>"

    [YYYY-MM-DD HH:MM] [CAP_REACHED] commit <sha>
      Iterations: 2
      Unresolved issues: [list]
      Last attempt: [summary]

    [YYYY-MM-DD HH:MM] [TEST_CAP_REACHED]   (no commit — halted)
      Failing tests: [list]
      Attempts: 3

    [YYYY-MM-DD HH:MM] [FULL_SUITE_FAILED]   (no commit — halted)
      Failing tests: [list]

## 7. Commit
Only reached when §4 passed, §5 passed, and §6 resolved (PASS) or
[CAP_REACHED]/[OVERRIDE].
- Commit to the working branch only. NEVER main.
- Write STATUS file with the final verdict token: PASS | CAP_REACHED | OVERRIDE
- The commit message MUST include both trailers, on their own lines, at the
  end of the message:

      AI-Verdict: PASS | CAP_REACHED | OVERRIDE
      AI-Task: <task>

  These are load-bearing. The merge gate and the post-commit hook depend on
  them. Omitting them is a defect, not a shortcut.

## 8. Post-Commit (automatic, do not invoke manually)
The .git/hooks/post-commit hook reads the AI-Task trailer and routes the
committed diff into ai_coding/active/<task>/. You do not call this; it fires
on commit. Just ensure the trailer is correct.

## 9. PROGRESS.md Checkpointing
- Update ai_coding/active/<task>/PROGRESS.md at MEANINGFUL BOUNDARIES only:
  (a) inner loop green, (b) post local-review judgment, (c) post-commit.
  NOT every step — per-step writes spend the very budget they protect.
- Record: current task, branch, steps completed, steps remaining, pending
  decisions/issues.
- Honest limitation (do not overstate to the user): nothing COMMITTED is
  lost on session death; in-loop progress since the last boundary may repeat.
  The test-fix loop is the least-protected phase. Do not claim "nothing is
  lost."
- Claude Pro usage is NOT programmatically readable. Do not attempt to query
  remaining usage or build a usage meter — it is impossible. PROGRESS.md is
  the recovery substitute, nothing more.

## 10. Notifications
Routine completion and urgent halts are surfaced via desktop notification
(plyer), triggered by reviewer.py or the post-commit hook. Urgent =
[TEST_CAP_REACHED], [FULL_SUITE_FAILED], [CAP_REACHED]. Routine = clean commit.

## 11. Deep Review (manual, user-initiated, SAME session)
When the user asks for a deep review:
- Read all diffs/logs in ai_coding/active/ and the actual source files
  (filesystem access is why review happens here, not in web UI).
- Pay special attention to commits tagged [CAP_REACHED] / [OVERRIDE] and any
  halted tasks.
- After the review, archive reviewed CLEAN-PASS task folders to
  ai_coding/archive/ (consumption-based clearing). Leave [CAP_REACHED] /
  [OVERRIDE] folders in place — they go to quarantine, cleared manually only.

## 12. /clear Timing — DECIDED: Point B
You cannot clear your own context. Therefore:
- Do NOT prompt for /clear before the deep review.
- AFTER the deep review is complete and clean-pass folders archived, and
  BEFORE the next feature begins, explicitly prompt the user:
  "Deep review complete. Run /clear before starting the next feature."
Rationale (do not re-litigate): clearing before review would destroy the
build reasoning the review depends on. Point B preserves context-aware
review. This is settled unless the user changes this file.

## 13. Cap Tuning Tradeoff (read before changing §4/§6 caps)
Inner cap 3 / outer cap 2 are tuned for token economy. Raising them shifts
cost from "Claude Code tokens now" to "human merge-review load later" — more
[CAP_REACHED] commits reach the merge gate, the one manual safeguard. This
cost is invisible at the point of change. Tune deliberately.
