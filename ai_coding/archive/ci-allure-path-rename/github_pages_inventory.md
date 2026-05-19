# GitHub Pages Inventory

Tracking every path published to the `gh-pages` branch under
`https://michaelkarimautomation.github.io/qa_framework/` so the user can
clean up stale paths once this task lands.

## Currently deployed (per workflow files on master pre-change)

| Path | Source workflow | Step / setting | Status |
|---|---|---|---|
| `/qa_framework/smoke/` | [.github/workflows/tests.yml](../../../.github/workflows/tests.yml) | `destination_dir: smoke` (now changed to `allure-suite`) | **Stale after next master push.** Full suite was deploying here despite the misleading "smoke" name. README link updated. Delete the `smoke/` directory from `gh-pages` branch manually after first new deploy lands. |
| `/qa_framework/reference/` | [.github/workflows/docs.yml](../../../.github/workflows/docs.yml) | `destination_dir: reference` | Keep. Sphinx API docs. |
| `/qa_framework/` (root) | _historical / unknown_ | n/a | README previously linked here. Likely stale or 404. README link removed in feature 1. |

## After feature 2 lands

| Path | Action required by user |
|---|---|
| `/qa_framework/smoke/` | Delete from `gh-pages` branch after first new deploy lands. Stale once `destination_dir` renames. |
| `/qa_framework/allure-suite/` | New live Allure path. README already links here. Appears on first master push after this branch merges. |
| `/qa_framework/reference/` | No change. |
| `/qa_framework/` (root) | If anything is sitting at the root of `gh-pages`, decide whether to leave / redirect / delete. |

## Reminder for end of task

Before closing this task, surface the cleanup list above to the user
explicitly so they don't forget that the old `/smoke/` directory will
linger on `gh-pages` even after the workflow change.
