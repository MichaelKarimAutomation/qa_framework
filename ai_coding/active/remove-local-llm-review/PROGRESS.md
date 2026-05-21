# PROGRESS: remove-local-llm-review

Task: remove the Ollama / qwen3-coder review step. Claude performs
the deep review itself in §6. Add `archived/` graveyard. Add auto-archive
workflow on master push. Remove CAP_REACHED verdict and the quarantine bucket.

Branch: feature/remove-local-llm-review

## Done
- §2 task folder + initial artifacts
- §3 implementation across CLAUDE.md, README.md, hooks, workflows, docs,
  promptsubmit_status, clear_queue.py
- §3 archived/ graveyard created with reviewer.py copy and README
- §3 reviewer.py deleted from ai_coding/, quarantine/ removed
- §3 new workflow .github/workflows/auto-archive.yml
- §4 affected tests (hooks-selftest.sh) 31/31 green on first attempt
- §5 full suite: 37/37 pytest green
- §6 self deep review: VERDICT PASS (after two pre-verdict fixes to the
  auto-archive workflow: trailing-slash + concurrency)
- §7 commit ea14066

## Follow-up (commit 2)
- CLAUDE.md / promptsubmit_status.ps1: stripped historical phrasing
  ("Claude's own", "no local LLM") from §2 task-folder description,
  §6 header, §6 body, and the PreToolUse-injected message
- Em-dash scrub across this-session-touched files (CLAUDE.md, hooks,
  selftests, auto-archive workflow, clear_queue.py, archived/README.md,
  docs/ai_coding_workflow.html, this PROGRESS.md, review.md)
- hooks-selftest.sh: 31/31 (no hook logic changes)
- Full pytest suite: 37/37
- §6 deep review: VERDICT PASS, no findings
