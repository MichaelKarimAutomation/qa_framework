# Task: human-workflow-doc

**Branch:** task/human-workflow-doc
**Started:** 2026-05-17

## Goal
Add `docs/ai_coding_workflow.html` — a cut-and-dry, Point-A-to-Point-B
guide for the **human** side of the CLAUDE.md AI coding workflow. Should
explain just the steps the human takes (branch creation, telling Claude
what to do, reviewing progress, opening the PR, deep review, /clear).
Detail belongs in CLAUDE.md — this doc just gets a contributor from
"I want to start a feature" to "it's merged" without forcing them to
read the operating contract first.

## Iterations
1. Wrote docs/ai_coding_workflow.html. Added Getting Started row in GUIDE.html. pytest 22/22 green. reviewer PASS.
2. Revised per user feedback: removed em-dashes, plainer language, deep review + archive folded into main steps as mandatory. pytest 22/22. reviewer PASS.
3. Added `.claude/settings.local.json` to .gitignore. pytest + reviewer skipped per user authorization (trivial gitignore-only change).
4. Step 1: combined `git checkout master` and `git pull` on one chained line. Steps 5 + 6: copy-pastable prompts scoped to this branch's task folder only. Moved /clear before push so Claude-side steps end before git/GitHub ceremony. First reviewer pass flagged two concerns that were both misreads of the diff; user authorized OVERRIDE; subsequent revision per user feedback passed cleanly. pytest 22/22. reviewer PASS.
5. Addressed first deep-review findings: softened step 2 hook language, added [OVERRIDE] to step 4 tag list, added brief quarantine mention in step 6. pytest 22/22. reviewer PASS.
6. Addressed second deep-review findings: renamed step 4 title to cover all four tags (not just halt ones); branched the closing options into halt vs committed tag groups. pytest + reviewer skipped per user authorization.
7. Addressed third deep-review findings: reworded edge case 1 so "rewrite history to PASS" is no longer suggested (loses audit trail); replaced with "redo work for genuine PASS, or admin-override to preserve history." Stopped recording forward-referencing commit SHAs and "(pending)" markers in this file (they kept rotting; git log is the SHA record).
8. Addressed fourth deep-review findings: fixed edge case 2's muddled causal chain. Two separate hooks were being conflated; the new wording distinguishes the PreToolUse hook (blocks Claude's edits, not human ones) from the commit-msg hook (the one `--no-verify` actually bypasses). pytest + reviewer skipped per user authorization.
9. Addressed fifth deep-review findings: step 6 archive prompt only said "move the folder" — never "commit the move." Without a commit, the archive operation would have sat uncommitted, never pushed, and the PR would have shipped with the task folder still in active/. Prompt now tells Claude to commit the move with the standard pipeline trailers. pytest + reviewer skipped per user authorization.
10. Addressed sixth deep-review findings: step 6 prompt body contained the literal trailer strings, which risked Claude echoing them into the archive commit's message body and tripping the commit-msg hook's head-1 parse (a live-demonstrated risk after that exact bug bit the iteration 9 commit message). Prompt now references "standard AI tag lines used on the other commits on this branch" instead of quoting them. pytest + reviewer skipped per user authorization.

## Notes
- §3 says implement + tests. HTML docs aren't pytest-testable; flagged in
  earlier reviews and not contested by the local reviewer.
- The doc lives in docs/ alongside the installation guides, parallel to
  the Sphinx output which lives at docs/_build/html/.
- See git log for commit SHAs.
