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

## Steps
- [x] Create branch task/human-workflow-doc
- [x] Create task folder per CLAUDE.md §2
- [x] Write docs/ai_coding_workflow.html
- [x] Add a row to GUIDE.html's Getting Started linking to it
- [x] Run `uv run pytest` — 22/22 green
- [x] Generate diff.patch
- [x] Run ai_coding/reviewer.py → VERDICT: PASS
- [x] STATUS=PASS, first commit landed (b7a347b)
- [x] Iteration 2: revise doc per user feedback (no em-dashes, plainer language, deep review + archive folded into main steps as mandatory)
- [x] Re-run pytest — 22/22 green
- [x] Regenerate diff.patch for the revision
- [x] Re-run reviewer.py — VERDICT: PASS
- [x] Second commit with trailers (2e737a4)
- [x] Iteration 3: add `.claude/settings.local.json` to .gitignore
- [x] Re-run pytest — PASS (skipped per user authorization for trivial gitignore-only change)
- [x] Re-run reviewer.py — PASS (skipped per user authorization for trivial gitignore-only change)
- [x] Third commit with trailers (49cdee2)
- [x] Iteration 4: combine git checkout master + git pull on one line (step 1); make step 5 + step 6 prompts copy-pastable and scoped to this branch's task folder only; move /clear before push so Claude-side steps end before git/GitHub ceremony begins. First reviewer pass on this iteration flagged two concerns that were both misreads of the diff; user authorized OVERRIDE; subsequent revision per user feedback passed cleanly on second review.
- [x] Re-run pytest — 22/22 green
- [x] Re-run reviewer.py — VERDICT: PASS
- [x] Fourth commit with trailers (pending)

## Notes
- §3 says implement + tests. HTML docs aren't pytest-testable; will note
  in disagreements.log if reviewer flags this (same precedent as the
  commit-msg-trailer-hook task).
- The doc lives in docs/ alongside the installation guides, parallel to
  the Sphinx output which lives at docs/_build/html/.
