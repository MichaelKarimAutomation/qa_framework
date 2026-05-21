# PROGRESS — remove-local-llm-review

Task: remove the local LLM (Ollama / qwen3-coder) review step. Claude performs
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
  auto-archive workflow — trailing-slash + concurrency)
