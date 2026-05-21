# Deep review: auto-archive-pat-auth

## Scope reviewed
Single edit to `.github/workflows/auto-archive.yml`: the
`actions/checkout` step's `token:` parameter changes from
`secrets.GITHUB_TOKEN` to `secrets.AUTO_ARCHIVE_TOKEN`. A short
comment block above the line explains why.

## Test status
- hooks-selftest.sh: 31/31 (no hook logic touched).
- Full pytest suite: 37/37. No regressions.

## Findings

### Considered, not flagged

- The previous `token: ${{ secrets.GITHUB_TOKEN }}` line was actually
  redundant (that's the default for actions/checkout). Explicitly
  named it before just for symmetry with the new line; the meaningful
  change is the secret name. No need to drop the explicit `token:`
  param now that the value differs from the default.
- The IDE GitHub Actions extension warns "Context access might be
  invalid: AUTO_ARCHIVE_TOKEN" because it can't see secrets that
  haven't been created in the repo yet. False positive; GitHub will
  resolve the value at runtime once the user creates the secret per
  the documented manual steps.
- The PAT identity (admin user) flows through actions/checkout's
  remote configuration. The subsequent `git config user.name` /
  `user.email` set the COMMITTER identity to github-actions[bot],
  which is cosmetic; the AUTHENTICATING identity for `git push` is
  determined by the credential helper that checkout installed,
  which uses the PAT. So the push succeeds even though the commit
  appears to be authored by the bot.
- No exposure risk: PATs in workflows are masked in logs by GitHub
  Actions' secret-redaction. The token never appears in stdout.
- This change has no effect until the user does the three manual
  steps (generate PAT, add secret, tick Repository admin in bypass
  list). If any of those is missed, the workflow will fail on
  checkout (token unresolvable) or on push (bypass not granted).
  Failure mode is the same as today: workflow run shows red, the
  active folders stay stuck, no permanent state change. Recoverable.

### Risk areas
- PAT expiration: if the user picks an expiration date, the workflow
  will silently start failing after that date. "No expiration" classic
  PATs avoid this but GitHub has been pushing users toward
  fine-grained PATs with mandatory expiration. The PROGRESS.md text
  notes this; long-term, migrating to a GitHub App token would be
  more robust.
- PAT scope: `repo` is broad (read/write to all of the user's repos).
  Acceptable for a personal-account repo; an org would want a
  fine-grained PAT scoped to this repo only.

## Verdict
VERDICT: PASS
