# PROGRESS: auto-archive-pat-auth

Task: switch the auto-archive workflow from the default GITHUB_TOKEN
(identity = github-actions[bot], not in bypass list) to a Personal
Access Token stored as repo secret AUTO_ARCHIVE_TOKEN, which carries
the user's Repository-admin identity through the push and bypasses
the master ruleset.

Background: the previous auto-archive run on master (after PR #15
merged) ran the sweep correctly but the final `git push origin master`
was rejected by the ruleset because GITHUB_TOKEN does not match any
bypass entry. The CI local commit evaporated, leaving both
remove-local-llm-review and forbid-claude-skip-ci stuck in
ai_coding/active/.

Branch: feature/auto-archive-pat-auth

## Done
- §2 task folder created
- §3 .github/workflows/auto-archive.yml updated: actions/checkout's
  token: param now references secrets.AUTO_ARCHIVE_TOKEN, with an
  inline comment explaining why GITHUB_TOKEN won't work
- §4 hooks-selftest sanity: 31/31 (no hook logic touched)
- §5 full pytest suite: 37/37 green
- §6 deep review: VERDICT PASS, no findings

## User-side prerequisites
Must be done before the next master push for the workflow to succeed:
- Generate classic PAT with `repo` scope
- Add as repo secret AUTO_ARCHIVE_TOKEN
- Tick Repository admin in master ruleset bypass list
