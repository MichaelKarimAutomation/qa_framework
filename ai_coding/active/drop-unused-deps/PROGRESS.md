# PROGRESS — drop-unused-deps

- Branch: task/readme-refactor (shared with [readme-content-refactor] and [ci-allure-path-rename])
- Scope: Drop dependencies in `pyproject.toml` with zero imports anywhere in the repo.
- Confirmed unused (grep `import X` / `from X` → zero matches outside pyproject/uv.lock):
  - `psycopg2-binary`
  - `sqlalchemy`
  - `testcontainers`
- Confirmed still used (kept):
  - `plyer` — used by `ai_coding/reviewer.py` and `ai_coding/notify.py` (CLAUDE.md §10 notifications)
  - `sphinx`, `sphinx-rtd-theme` — used by `scripts/generate_docs.py` and `docs/conf.py`
- Steps completed: investigation
- Steps remaining:
  - Remove the three unused entries from `pyproject.toml`
  - Refresh `uv.lock` via `uv sync` (or `uv lock`)
- Pending decisions: none
- Test impact: none expected — these deps had no callers. Full-suite run will confirm.
