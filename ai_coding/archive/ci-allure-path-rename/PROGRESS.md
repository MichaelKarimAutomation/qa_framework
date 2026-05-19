# PROGRESS — ci-allure-path-rename

- Branch: task/readme-refactor (shared with [readme-content-refactor] and [drop-unused-deps])
- Scope: Rename `.github/workflows/tests.yml` `destination_dir: smoke` → `allure-suite` so the deployed Allure path matches what's actually deployed (the full pytest suite, not just the smoke subset). Update the README link to match the new path.
- Steps completed:
  - `tests.yml`: `destination_dir: smoke` → `destination_dir: allure-suite`
  - README live Allure link updated to `/qa_framework/allure-suite/`
  - GitHub Pages inventory captured (see [github_pages_inventory.md](github_pages_inventory.md))
- Steps remaining: none (work itself complete; pending pipeline steps shared across the branch's commits)
- Pending decisions: none
- Test impact: none (CI workflow + README only)
- Post-task: user must manually delete the stale `smoke/` directory from the `gh-pages` branch after the first new deploy lands.
