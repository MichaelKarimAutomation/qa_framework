# Deep review: forbid-claude-skip-ci

## Scope reviewed
Single change: CLAUDE.md gets a new §14 "Forbidden Literals in Commit
Messages and PR Bodies". Designed as an extensible list with a
section-wide permission carve-out, seeded with one entry for GitHub
skip-CI markers.

## Test status
- hooks-selftest.sh: 31/31 (no hook code touched).
- Full pytest suite: 37/37 in 19.74s. No regressions.

## Findings

### Considered, not flagged
- The section uses no em-dashes (memory rule honored).
- The auto-archive workflow carve-out is named explicitly so future
  readers don't think the workflow YAML's skip-CI usage violates the
  rule.
- The permission carve-out is stated once at the section level so it
  applies to every future bullet without restating per-entry.
- The phrasing "Claude must NOT include" makes the actor explicit. The
  rule binds Claude, not the repo's other contributors.
- Past-incident reference (PR #14) is concrete and gives a future
  reader the failure they're protecting against.

### Risk areas
- CLAUDE.md is a directive, not a hook. A misbehaving or non-following
  Claude instance can still type the forbidden literal. The
  enforcement is the same as the rest of CLAUDE.md (a contract Claude
  is asked to follow). The user has already accepted that limit
  ("mechanical enforcement is not available" was option D and
  declined).

VERDICT: PASS
