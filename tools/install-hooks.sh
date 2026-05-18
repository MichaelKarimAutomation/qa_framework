#!/usr/bin/env sh
# install-hooks.sh — point git at tools/hooks/ so the CLAUDE.md gates fire
# on every commit in this clone.
#
# Uses `git config core.hooksPath` (git >= 2.9). The hooks live in version
# control, so once installed they cannot drift per-clone.
#
# Run this once after cloning. Re-run is idempotent.

set -eu

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/tools/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  printf 'error: %s does not exist — run from the qa_framework clone\n' \
    "$HOOKS_DIR" >&2
  exit 1
fi

# Refuse to silently downgrade if the user is on a git too old for hooksPath.
GIT_VER="$(git --version | awk '{print $3}')"
GIT_MAJOR="$(printf '%s' "$GIT_VER" | awk -F. '{print $1+0}')"
GIT_MINOR="$(printf '%s' "$GIT_VER" | awk -F. '{print $2+0}')"
if [ "$GIT_MAJOR" -lt 2 ] || { [ "$GIT_MAJOR" -eq 2 ] && [ "$GIT_MINOR" -lt 9 ]; }; then
  printf 'error: git %s is too old; core.hooksPath needs git >= 2.9\n' \
    "$GIT_VER" >&2
  exit 1
fi

# Make sure each hook is executable in the working tree. (Git on Windows
# ignores the FS bit but POSIX systems need it; this is what blocks the
# "hook silently doesn't run" failure mode.)
for h in pre-commit commit-msg post-commit; do
  if [ ! -f "$HOOKS_DIR/$h" ]; then
    printf 'error: missing %s\n' "$HOOKS_DIR/$h" >&2
    exit 1
  fi
  chmod +x "$HOOKS_DIR/$h" 2>/dev/null || true
done

git config core.hooksPath tools/hooks

printf 'installed: core.hooksPath = tools/hooks\n'
printf '  pre-commit   : enforces CLAUDE.md §2-§6 artifact presence\n'
printf '  commit-msg   : enforces §7 trailers + §6-§7 trailer consistency\n'
printf '  post-commit  : routes the just-committed diff into the task folder\n'
