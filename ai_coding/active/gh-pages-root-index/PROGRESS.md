# gh-pages-root-index

- Task: Add a CI workflow that regenerates a root index.html on the gh-pages
  branch, listing the existing subsite directories (`allure-suite`,
  `reference`) and any future top-level directories.
- Branch: `feature/gh-pages-root-index`

## Steps completed
- Generator script `scripts/generate_gh_pages_index.py` written.
- Workflow `.github/workflows/gh-pages-index.yml` written
  (push gh-pages with `paths-ignore: ['index.html']`, plus workflow_dispatch).
- Unit tests added: `tests/scripts/test_generate_gh_pages_index.py`,
  15/15 green.
- Full pytest suite: 37/37 green in 26.37s.
- Reviewer.py: model emitted no `VERDICT:` line; both substantive comments
  (defensive empty-timestamp guard, recursive `tmp_path` fixture
  redefinition) were not actionable. User reclassified to PASS pending a
  permanent fix to the local-reviewer reliability problem.

## Steps remaining
- Commit landed with `AI-Verdict: PASS` and `AI-Task: gh-pages-root-index`
  trailers; post-commit hook routes the diff.
- Manual workflow_dispatch run on gh-pages after merge to validate the
  rendered landing page.

## Pending decisions / open items
- None.
