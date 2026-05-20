# gh-pages-index-trigger-fix

- Task: Fix the `push: branches: [gh-pages]` trigger on
  `.github/workflows/gh-pages-index.yml`. Confirmed inert after the
  PR #12 merge: docs.yml and tests.yml deployed to gh-pages, but the
  index workflow never appeared in the Actions feed because GitHub
  Actions evaluates `push` triggers against workflow files that exist
  on the branch receiving the push, and the file lives on master only
  (peaceiris/actions-gh-pages never copies `.github/workflows/` to
  gh-pages).
- Branch: `feature/gh-pages-root-index` (reused; remote-deleted after
  PR #12 merged, reset locally to origin/master).

## Steps completed
- Replaced `push: branches: [gh-pages]` (+ `paths-ignore`) with
  `workflow_run` on "Build and Deploy Docs" and "QA Framework Tests"
  completing on master. `workflow_run` reads the workflow file from
  the default branch.
- Full pytest suite: 37/37 green in 19.42s.
- reviewer.py: PASS first attempt, no overrides needed.

## Steps remaining
- Commit with `AI-Verdict: PASS` and `AI-Task: gh-pages-index-trigger-fix`
  trailers; post-commit hook routes the diff.
- Push branch, open PR.
- Post-merge: confirm the workflow appears in the Actions feed when
  docs.yml or tests.yml completes on master.

## Pending decisions / open items
- None.
