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
- Steps completed:
  - Removed psycopg2-binary, sqlalchemy, testcontainers from `pyproject.toml` and refreshed `uv.lock`.
  - Committed (AI-Verdict: OVERRIDE).
- Follow-up landing in a second commit on this task:
  - `scripts/setup-windows.ps1` and `scripts/setup-linux.sh` both hardcoded `uv add ... psycopg2-binary sqlalchemy testcontainers ...`. Running `install.py` fresh would have re-added the dropped deps to pyproject. Now removed.
- Pending decisions: none
- Test impact: still none. Setup scripts only run at install time; full pytest already passed against the new deps list.
