# PROGRESS — readme-plain-language

- Branch: task/readme-refactor (continued; fourth feature on this branch)
- Scope: Strip AI-styled writing from README.md (em-dashes, marketing-ish phrases, niche jargon) and rewrite in plain language. Bound by the rule: keep terms a typical QA Engineer knows; drop those they wouldn't.
- Decisions made up front (per user feedback this turn):
  - Remove em-dashes everywhere in prose; replace with colon, period, parentheses, or comma. Recorded as standing feedback in user memory.
  - Subtitle: drop "production-quality" only; keep the rest.
  - Layered-architecture bullet: keep as-is, user preference.
  - factory_boy bullet: reframe as design point ("generates realistic data on demand instead of hardcoded fixtures").
  - Pact bullet: keep the plain rewrite the user already approved.
- Steps remaining:
  - User signal to commit.
  - §5 full pytest run.
  - §6 reviewer.
  - Commit with AI-Verdict / AI-Task trailers.
- Notes:
  - Hooks section was rewritten as if `python install.py` already activates hooks automatically. This is a short-term lie by explicit user direction; the implementation lands in a separate future task (`auto-install-hooks`). README claim becomes true once that ships.
- Test impact: none expected (README only).
