# PROGRESS: forbid-claude-skip-ci

Task: add CLAUDE.md §14 forbidding Claude from writing GitHub skip-CI
markers in commit messages or PR bodies in this repo, with an
ask-first carve-out for legitimate exceptions. Designed as an
extensible list so future forbidden literals can be appended as new
bullets without restructuring the section.

Branch: feature/forbid-claude-skip-ci

## Done
- §2 task folder created
- §3 CLAUDE.md §14 added with section-wide permission carve-out and
  the skip-CI marker entry seeded
- §4 affected tests: none (CLAUDE.md is prose; hooks-selftest
  unchanged, 31/31 still green as sanity)
- §5 full pytest suite: 37/37 green
- §6 deep review: VERDICT PASS, no findings
