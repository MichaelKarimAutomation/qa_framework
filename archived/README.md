# archived/

Graveyard for features removed from the active codebase. The original file
is copied here before being deleted from its source location, so the
implementation history is preserved without bloating the tree git ships.

Each file carries a deprecation header at the top noting the date and the
replacement (if any).

Files here are not imported, executed, or referenced anywhere in the
running project. If you find one being referenced, that's a bug: either
the file should come back, or the reference should go.

## Distinct from `ai_coding/archive/`

`ai_coding/archive/` holds completed task folders from the AI coding
pipeline (see [CLAUDE.md](../CLAUDE.md)). This folder holds deprecated
**source files**, not task records.
