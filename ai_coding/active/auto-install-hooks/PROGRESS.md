# PROGRESS — auto-install-hooks

Task: implement automatic git hook installation in install.py so that
running `python install.py` activates the hooks (sets core.hooksPath to
tools/hooks). README's "Repository hooks" section already documents
this; implementation is missing.

Branch: task/auto-install-hooks

## Steps completed
- Branch created from master.
- Task folder + PROGRESS.md created (this file).
- Read install.py, tools/install-hooks.ps1, tools/install-hooks.sh.
- install.py modified: post-setup dispatch to tools/install-hooks.{ps1,sh}
  added; non-zero return propagates as install.py exit.
- Local verification PASS: unset core.hooksPath; ran install.py end-to-end
  (full Windows setup including .venv rebuild); core.hooksPath = tools/hooks.
- §5 full pytest: 22/22 green.
- §6 reviewer: model returned VERDICT: FAIL with two nitpicks (see
  disagreements.log). Both not applicable: same pattern as existing code in
  install.py (ExecutionPolicy ByPass, no pre-validate of script path).
  User reviewed the reasoning and approved as PASS. Final verdict: PASS.

## Steps remaining
- Commit with AI-Verdict: PASS + AI-Task: auto-install-hooks trailers.

## Decisions
- Hooks are part of setup, not optional. Non-zero from the hook installer
  must propagate as the install.py exit code (per task brief).
- Matches the existing platform-dispatch pattern at install.py:21-66.
  No new abstraction.
