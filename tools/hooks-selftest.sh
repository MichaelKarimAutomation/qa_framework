#!/usr/bin/env bash
# hooks-selftest.sh — exercise tools/hooks/{pre-commit,commit-msg,post-commit}
# against synthetic staged sets in a temp git repo. Asserts each rejection
# branch of pre-commit and pins the post-commit tri-branch routing fix.
#
# Standalone: does not require pytest or any project dependency.
# Run via:  bash tools/hooks-selftest.sh
#
# Exit 0 iff every case passes. Exit 1 with a summary of failed cases.

set -u

SELF_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(cd -- "$SELF_DIR/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/tools/hooks"

if [ ! -x "$HOOKS_DIR/pre-commit" ]; then
  chmod +x "$HOOKS_DIR/pre-commit" "$HOOKS_DIR/commit-msg" "$HOOKS_DIR/post-commit" 2>/dev/null || true
fi

TMP="$(mktemp -d 2>/dev/null || mktemp -d -t hooks-selftest)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0
FAILED=""

ok()  { printf '  [ok]   %s\n' "$1"; PASS=$((PASS+1)); }
bad() { printf '  [FAIL] %s\n' "$1"; FAIL=$((FAIL+1)); FAILED="${FAILED}    - $1
"; }

init_repo() {
  rm -rf "$TMP/scratch"
  mkdir -p "$TMP/scratch"
  cd "$TMP/scratch" || exit 1
  git init -q
  git config user.email "selftest@example.com"
  git config user.name  "selftest"
  git config commit.gpgsign false
  git config core.hooksPath "$HOOKS_DIR"
  echo seed > seed.txt
  git add seed.txt
  # --no-verify to skip our hooks for the seed commit (no AI-Task trailer).
  git commit -q --no-verify -m "seed"
}

write_task() {
  # write_task <task> <status> <review_verdict> [dlog_marker]
  local task="$1" status="$2" review="$3" dlog="${4:-}"
  local dir="ai_coding/active/$task"
  mkdir -p "$dir"
  printf 'progress\n' > "$dir/PROGRESS.md"
  printf '%s\n' "$status" > "$dir/STATUS"
  printf '%s' "$dlog" > "$dir/disagreements.log"
  printf 'diff body\n' > "$dir/diff.patch"
  printf 'review body\n\nVERDICT: %s\n' "$review" > "$dir/review.md"
  git add "$dir"
}

run_pre()  { "$HOOKS_DIR/pre-commit"; }
expect_pre_pass() {
  if run_pre >/dev/null 2>&1; then ok "$1"; else bad "$1 (pre-commit unexpectedly rejected)"; fi
}
expect_pre_fail() {
  if run_pre >/dev/null 2>&1; then bad "$1 (pre-commit unexpectedly accepted)"; else ok "$1"; fi
}

run_commit_msg() {
  # $1 = message file (must already exist), $2 = optional source
  "$HOOKS_DIR/commit-msg" "$1" "${2:-}"
}
write_msg() {
  # write_msg <path> <task> <verdict>
  local f="$1" t="$2" v="$3"
  printf 'feat: scratch\n\nAI-Verdict: %s\nAI-Task: %s\n' "$v" "$t" > "$f"
}
expect_msg_pass() {
  if run_commit_msg "$1" >/dev/null 2>&1; then ok "$2"; else bad "$2 (commit-msg unexpectedly rejected)"; fi
}
expect_msg_fail() {
  if run_commit_msg "$1" >/dev/null 2>&1; then bad "$2 (commit-msg unexpectedly accepted)"; else ok "$2"; fi
}

# =============================================================================
# PRE-COMMIT TEST CASES
# =============================================================================
printf 'pre-commit cases:\n'

# 1. Golden path — all artifacts present, staged, internally consistent.
init_repo
write_task "ok-task" PASS PASS ""
expect_pre_pass "01 golden path accepts"

# 2. Missing PROGRESS.md.
init_repo
write_task "no-progress" PASS PASS ""
rm  ai_coding/active/no-progress/PROGRESS.md
git rm -q --cached ai_coding/active/no-progress/PROGRESS.md
expect_pre_fail "02 missing PROGRESS.md rejects"

# 3. Missing STATUS.
init_repo
write_task "no-status" PASS PASS ""
rm  ai_coding/active/no-status/STATUS
git rm -q --cached ai_coding/active/no-status/STATUS
expect_pre_fail "03 missing STATUS rejects"

# 4. Missing disagreements.log.
init_repo
write_task "no-dlog" PASS PASS ""
rm  ai_coding/active/no-dlog/disagreements.log
git rm -q --cached ai_coding/active/no-dlog/disagreements.log
expect_pre_fail "04 missing disagreements.log rejects"

# 5. Missing diff.patch.
init_repo
write_task "no-diff" PASS PASS ""
rm  ai_coding/active/no-diff/diff.patch
git rm -q --cached ai_coding/active/no-diff/diff.patch
expect_pre_fail "05 missing diff.patch rejects"

# 6. Missing review.md.
init_repo
write_task "no-review" PASS PASS ""
rm  ai_coding/active/no-review/review.md
git rm -q --cached ai_coding/active/no-review/review.md
expect_pre_fail "06 missing review.md rejects"

# 7. STATUS present on disk, not staged.
init_repo
write_task "status-unstaged" PASS PASS ""
git rm -q --cached ai_coding/active/status-unstaged/STATUS
expect_pre_fail "07 STATUS present on disk but unstaged rejects"

# 8. STATUS contents malformed.
init_repo
write_task "bad-status" PASS PASS ""
printf 'FOOBAR\n' > ai_coding/active/bad-status/STATUS
git add ai_coding/active/bad-status/STATUS
expect_pre_fail "08 STATUS contents 'FOOBAR' rejects"

# 8a. STATUS=CAP_REACHED (legacy verdict) rejects — pin against resurfacing.
init_repo
write_task "legacy-cap" PASS PASS ""
printf 'CAP_REACHED\n' > ai_coding/active/legacy-cap/STATUS
git add ai_coding/active/legacy-cap/STATUS
expect_pre_fail "08a STATUS=CAP_REACHED (legacy) rejects"

# 9. review.md VERDICT: FAIL is an intermediate state — always rejects.
init_repo
write_task "review-fail" OVERRIDE FAIL "[OVERRIDE] reason"
expect_pre_fail "09 review.md VERDICT: FAIL rejects (intermediate state)"

# 10. review.md VERDICT: OVERRIDE + STATUS=OVERRIDE + [OVERRIDE] accepts.
init_repo
write_task "override-clean" OVERRIDE OVERRIDE "[OVERRIDE] reason"
expect_pre_pass "10 review OVERRIDE + STATUS=OVERRIDE + [OVERRIDE] accepts"

# 10a. review.md VERDICT: OVERRIDE without [OVERRIDE] in disagreements rejects.
init_repo
write_task "override-no-marker" OVERRIDE OVERRIDE ""
expect_pre_fail "10a review OVERRIDE without [OVERRIDE] marker rejects"

# 10b. review.md VERDICT: OVERRIDE but STATUS=PASS rejects.
init_repo
write_task "override-status-mismatch" PASS OVERRIDE "[OVERRIDE] reason"
expect_pre_fail "10b review OVERRIDE but STATUS=PASS rejects"

# 10c. review.md VERDICT: PASS but STATUS=OVERRIDE rejects.
init_repo
write_task "pass-status-mismatch" OVERRIDE PASS "[OVERRIDE] reason"
expect_pre_fail "10c review PASS but STATUS=OVERRIDE rejects"

# Helper: rename ai_coding/active/<task> → ai_coding/archive/<task> using
# OS mv + git add -A (Git for Windows' `git mv` is broken on directories;
# rename detection via -M collapses the staged delete+add back to a rename).
closeout_rename() {
  local task="$1"
  mkdir -p "ai_coding/archive/$task"
  mv "ai_coding/active/$task"/* "ai_coding/archive/$task"/
  rmdir "ai_coding/active/$task"
  git add -A "ai_coding/active/$task" "ai_coding/archive/$task"
}

# 11. Close-out pure rename ai_coding/active/x → ai_coding/archive/x.
init_repo
mkdir -p ai_coding/active/oldtask
printf 'progress\n' > ai_coding/active/oldtask/PROGRESS.md
git add ai_coding/active/oldtask
git commit -q --no-verify -m "set up oldtask"
closeout_rename oldtask
expect_pre_pass "11 pure close-out rename accepts (exempt)"

# 12. Close-out rename + an unrelated non-ai_coding edit (NOT pure close-out,
#     and no active/<task>/ paths touched) → still accepts since no task touched.
init_repo
mkdir -p ai_coding/active/oldtask2
printf 'progress\n' > ai_coding/active/oldtask2/PROGRESS.md
git add ai_coding/active/oldtask2
git commit -q --no-verify -m "set up oldtask2"
closeout_rename oldtask2
printf 'hi\n' > unrelated.txt
git add unrelated.txt
expect_pre_pass "12 close-out rename + unrelated non-task file accepts"

# 13. No ai_coding paths staged at all.
init_repo
printf 'x\n' > unrelated.txt
git add unrelated.txt
expect_pre_pass "13 no ai_coding paths staged accepts"

# 13a. Missing VERDICT line + STATUS=PASS → reject. The PASS path must not
#      silently accept reviews that lack a parseable verdict.
init_repo
write_task "no-verdict-pass" PASS PASS ""
# Strip the VERDICT line out of review.md.
sed -i '/^VERDICT:/d' ai_coding/active/no-verdict-pass/review.md
git add ai_coding/active/no-verdict-pass/review.md
expect_pre_fail "13a missing VERDICT line + STATUS=PASS rejects"

# 13b. Missing VERDICT line + STATUS=OVERRIDE + [OVERRIDE] in disagreements.log
#      → accept. §6 escape hatch must survive a review.md write that misfires.
#      Regression pin that protects the OVERRIDE path against hook tightening.
init_repo
write_task "no-verdict-override" OVERRIDE PASS "[OVERRIDE] reason"
sed -i '/^VERDICT:/d' ai_coding/active/no-verdict-override/review.md
git add ai_coding/active/no-verdict-override/review.md
expect_pre_pass "13b missing VERDICT line + STATUS=OVERRIDE + [OVERRIDE] accepts"

# =============================================================================
# COMMIT-MSG TEST CASES
# =============================================================================
printf 'commit-msg cases:\n'

# 14. Trailers + STATUS match (golden).
init_repo
write_task "good" PASS PASS ""
write_msg msg.txt good PASS
expect_msg_pass msg.txt "14 trailers + STATUS=PASS match accepts"

# 15. Missing trailers.
init_repo
printf 'feat: no trailers\n' > msg.txt
expect_msg_fail msg.txt "15 missing trailers rejects"

# 16. Malformed verdict.
init_repo
write_task "good2" PASS PASS ""
write_msg msg.txt good2 SOMETHING
expect_msg_fail msg.txt "16 malformed AI-Verdict rejects"

# 16a. CAP_REACHED in AI-Verdict trailer (legacy) rejects — regression pin.
init_repo
write_task "legacy-cap-trailer" PASS PASS ""
write_msg msg.txt legacy-cap-trailer CAP_REACHED
expect_msg_fail msg.txt "16a AI-Verdict: CAP_REACHED (legacy) rejects"

# 17. STATUS vs AI-Verdict mismatch (STATUS=PASS, AI-Verdict=OVERRIDE).
init_repo
write_task "mismatch" PASS PASS ""
write_msg msg.txt mismatch OVERRIDE
expect_msg_fail msg.txt "17 STATUS=PASS but AI-Verdict=OVERRIDE rejects"

# 18. review.md VERDICT: FAIL but AI-Verdict=PASS (should reject).
init_repo
write_task "review-fail-but-pass-trailer" OVERRIDE FAIL "[OVERRIDE] x"
# Doctor STATUS to PASS so the STATUS↔trailer check doesn't fire first.
printf 'PASS\n' > ai_coding/active/review-fail-but-pass-trailer/STATUS
git add ai_coding/active/review-fail-but-pass-trailer/STATUS
write_msg msg.txt review-fail-but-pass-trailer PASS
expect_msg_fail msg.txt "18 review FAIL but AI-Verdict=PASS rejects"

# 18a. review.md VERDICT: OVERRIDE + AI-Verdict=OVERRIDE + STATUS=OVERRIDE accepts.
init_repo
write_task "msg-override-clean" OVERRIDE OVERRIDE "[OVERRIDE] x"
write_msg msg.txt msg-override-clean OVERRIDE
expect_msg_pass msg.txt "18a OVERRIDE end-to-end accepts"

# 19. Close-out commit-msg shape — pure rename → exempt from consistency checks
#     (but still requires trailers, which we provide).
init_repo
mkdir -p ai_coding/active/oldtask3
printf 'progress\n' > ai_coding/active/oldtask3/PROGRESS.md
git add ai_coding/active/oldtask3
git commit -q --no-verify -m "set up oldtask3"
closeout_rename oldtask3
# Close-out task name in trailer differs from the archived task — fine, since
# the consistency checks against ai_coding/active/oldtask3/STATUS are skipped.
write_msg msg.txt archive-oldtask3 PASS
expect_msg_pass msg.txt "19 close-out commit-msg accepts with bare trailers"

# =============================================================================
# POST-COMMIT TEST CASES — the heart of fix B.
# =============================================================================
printf 'post-commit cases:\n'

# 20. Archive-only routing: archive/<task>/ exists, active/<task>/ does not.
#     A subsequent commit with AI-Task: <task> must NOT recreate an active
#     stub — diff must land in archive/<task>/.
init_repo
mkdir -p ai_coding/archive/already-archived
printf 'old\n' > ai_coding/archive/already-archived/PROGRESS.md
git add ai_coding/archive/already-archived
git commit -q --no-verify -m "prep already-archived"
printf 'change\n' > scratch.txt
git add scratch.txt
git commit -q --no-verify -m "scratch

AI-Verdict: PASS
AI-Task: already-archived"
diff_in_archive=$(ls ai_coding/archive/already-archived/diff_*.patch 2>/dev/null | wc -l)
active_dir_exists=0
[ -d ai_coding/active/already-archived ] && active_dir_exists=1
if [ "$diff_in_archive" -ge 1 ] && [ "$active_dir_exists" -eq 0 ]; then
  ok "20 routing: archive-only → diff in archive, no active stub"
else
  bad "20 routing: archive-only (diff_in_archive=$diff_in_archive active_dir_exists=$active_dir_exists)"
fi

# 21. CRITICAL: close-out commit (rename active/x → archive/x) → routes to
#     archive/x, NOT active/x. Pins fix B against regression.
init_repo
mkdir -p ai_coding/active/closing-task
printf 'progress\n' > ai_coding/active/closing-task/PROGRESS.md
git add ai_coding/active/closing-task
git commit -q --no-verify -m "set up closing-task"
closeout_rename closing-task
git commit -q --no-verify -m "close out closing-task

AI-Verdict: PASS
AI-Task: closing-task"
diff_in_archive=$(ls ai_coding/archive/closing-task/diff_*.patch 2>/dev/null | wc -l)
active_dir_exists=0
[ -d ai_coding/active/closing-task ] && active_dir_exists=1
if [ "$diff_in_archive" -ge 1 ] && [ "$active_dir_exists" -eq 0 ]; then
  ok "21 close-out rename → diff in archive, no active stub (fix B)"
else
  bad "21 close-out rename (diff_in_archive=$diff_in_archive active_dir_exists=$active_dir_exists)"
fi

# 22. Active-exists routing: standard case.
init_repo
mkdir -p ai_coding/active/normal-task
printf 'progress\n' > ai_coding/active/normal-task/PROGRESS.md
git add ai_coding/active/normal-task
git commit -q --no-verify -m "set up normal-task"
printf 'edit\n' > note.txt
git add note.txt
git commit -q --no-verify -m "scratch

AI-Verdict: PASS
AI-Task: normal-task"
diff_in_active=$(ls ai_coding/active/normal-task/diff_*.patch 2>/dev/null | wc -l)
if [ "$diff_in_active" -ge 1 ]; then
  ok "22 routing: active exists → diff in active"
else
  bad "22 routing: active exists (diff_in_active=$diff_in_active)"
fi

# 23. Fallback routing: neither active/<task>/ nor archive/<task>/ exists.
init_repo
printf 'edit\n' > note.txt
git add note.txt
git commit -q --no-verify -m "scratch

AI-Verdict: PASS
AI-Task: brand-new-task"
diff_in_active=$(ls ai_coding/active/brand-new-task/diff_*.patch 2>/dev/null | wc -l)
if [ "$diff_in_active" -ge 1 ]; then
  ok "23 routing: neither exists → fallback to active"
else
  bad "23 routing: neither exists (diff_in_active=$diff_in_active)"
fi

# =============================================================================
# SUMMARY
# =============================================================================
printf '\n'
printf 'hooks-selftest: %d passed, %d failed\n' "$PASS" "$FAIL"
if [ "$FAIL" -ne 0 ]; then
  printf 'failed cases:\n%s' "$FAILED"
  exit 1
fi
exit 0
