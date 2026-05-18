# Task: claudemd-clarifications

**Branch:** task/claudemd-clarifications
**Started:** 2026-05-18

## Goal
Two clarifying additions to CLAUDE.md, derived from prior feedback that has
already bitten this repo:

1. §1 (Workflow Scope) — codify that every code edit is feature work
   regardless of size. No casual mode bypasses the §2-§7 pipeline.
2. §9 (PROGRESS.md Checkpointing) — codify that PROGRESS.md records verdicts
   and iteration descriptions only. Never write commit SHAs or "(pending)"
   markers; the git log is the authoritative SHA record.

Both rules are already practiced; this task only writes them down so the
contract matches the behaviour.

## Iterations
1. §1: added bullet "every code edit is feature work regardless of size — no
   casual mode bypasses §2-§7." §9: added bullet "record verdicts and
   iteration descriptions only — no SHAs, no (pending) markers; git log is
   authoritative." pytest 22/22 green. reviewer PASS (first pass, no fixes).

## Notes
- §3 says implement + tests. CLAUDE.md is a prose contract, not testable
  with pytest; §5 full-suite run is still required as a regression check.
- See git log for commit SHAs.
