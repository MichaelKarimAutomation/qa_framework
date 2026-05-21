# hooks-selftest.ps1 -- exercise tools/hooks/{pre-commit,commit-msg,post-commit}
# against synthetic staged sets in a temp git repo. Asserts each rejection
# branch of pre-commit and pins the post-commit tri-branch routing fix.
#
# The hooks themselves are POSIX-sh scripts (Git for Windows MSYS bash runs
# them). This script invokes them via git's own commit machinery (hooksPath)
# or directly via `bash`, depending on what's available -- same outcome.
#
# Run via:  pwsh -File tools\hooks-selftest.ps1   (or Windows PowerShell)
# Exit 0 iff every case passes; exit 1 with a summary of failed cases.

# Native-command stderr (e.g. git warnings, intentional hook rejection
# messages) should NOT terminate this script; we check $LASTEXITCODE
# explicitly per case.
$ErrorActionPreference = 'Continue'

$SelfDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $SelfDir
$HooksDir  = Join-Path $RepoRoot 'tools\hooks'
$Tmp       = Join-Path ([System.IO.Path]::GetTempPath()) ("hooks-selftest-" + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $Tmp | Out-Null

# Cleanup on exit. Use a script-scope flag so the finally block can find $Tmp.
$Script:CleanupPath = $Tmp

# bash from Git for Windows runs the POSIX hooks. Find it.
$Bash = $null
foreach ($cand in @(
  'C:\Program Files\Git\bin\bash.exe',
  'C:\Program Files\Git\usr\bin\bash.exe',
  'C:\Program Files (x86)\Git\bin\bash.exe'
)) {
  if (Test-Path -LiteralPath $cand) { $Bash = $cand; break }
}
if (-not $Bash) {
  $cmd = Get-Command bash -ErrorAction SilentlyContinue
  if ($cmd) { $Bash = $cmd.Source }
}
if (-not $Bash) {
  Write-Error "bash not found -- Git for Windows must be installed to exercise POSIX hooks"
  exit 1
}

$Pass = 0
$Fail = 0
$Failed = New-Object System.Collections.Generic.List[string]

function OK([string]$name)  { Write-Host "  [ok]   $name"; $Script:Pass++ }
function BAD([string]$name) { Write-Host "  [FAIL] $name"; $Script:Fail++; $Script:Failed.Add($name) }

function Init-Repo {
  $scratch = Join-Path $Script:CleanupPath 'scratch'
  # cd out before deletion. Windows locks the directory if any process has
  # its CWD inside it.
  Set-Location -LiteralPath $Script:RepoRoot
  if (Test-Path -LiteralPath $scratch) { Remove-Item -LiteralPath $scratch -Recurse -Force }
  New-Item -ItemType Directory -Path $scratch | Out-Null
  Set-Location -LiteralPath $scratch
  & git init -q
  & git config user.email 'selftest@example.com'
  & git config user.name  'selftest'
  & git config commit.gpgsign false
  # Use forward-slash form because git wants POSIX paths in hooksPath under MSYS.
  $hooksPosix = ($Script:HooksDir -replace '\\', '/')
  & git config core.hooksPath $hooksPosix
  'seed' | Out-File -Encoding ascii seed.txt
  & git add seed.txt
  & git commit -q --no-verify -m 'seed'
}
$Script:HooksDir = $HooksDir
$Script:RepoRoot = $RepoRoot

function Write-Task {
  param([string]$Task, [string]$Status, [string]$Review, [string]$DLog = '')
  $dir = "ai_coding/active/$Task"
  New-Item -ItemType Directory -Path $dir -Force | Out-Null
  'progress' | Out-File -Encoding ascii (Join-Path $dir 'PROGRESS.md')
  $Status    | Out-File -Encoding ascii (Join-Path $dir 'STATUS')
  $DLog      | Out-File -Encoding ascii -NoNewline (Join-Path $dir 'disagreements.log')
  'diff body' | Out-File -Encoding ascii (Join-Path $dir 'diff.patch')
  ("review body`n`nVERDICT: $Review`n") | Out-File -Encoding ascii (Join-Path $dir 'review.md')
  & git add $dir | Out-Null
}

function Closeout-Rename {
  # Git for Windows `git mv` is broken on directories. Mirror what `git mv`
  # does on Linux/Mac: OS rename + rmdir + git add -A (rename detection via
  # -M in pre-commit/commit-msg collapses staged delete+add back to a rename).
  param([string]$Task)
  $src = "ai_coding/active/$Task"
  $dst = "ai_coding/archive/$Task"
  New-Item -ItemType Directory -Path $dst -Force | Out-Null
  Get-ChildItem -LiteralPath $src -Force | ForEach-Object {
    Move-Item -LiteralPath $_.FullName -Destination (Join-Path $dst $_.Name) -Force
  }
  Remove-Item -LiteralPath $src -Recurse -Force
  & git add -A $src $dst | Out-Null
}

function Run-PreCommit {
  # Merge bash stdout+stderr and discard. We only care about exit code.
  $null = & $Bash -c "'$($HooksDir -replace '\\','/')/pre-commit'" 2>&1
  return $LASTEXITCODE
}

function Expect-PrePass([string]$name) {
  if ((Run-PreCommit) -eq 0) { OK $name } else { BAD "$name (pre-commit unexpectedly rejected)" }
}
function Expect-PreFail([string]$name) {
  if ((Run-PreCommit) -ne 0) { OK $name } else { BAD "$name (pre-commit unexpectedly accepted)" }
}

function Write-Msg {
  param([string]$Path, [string]$Task, [string]$Verdict)
  "feat: scratch`n`nAI-Verdict: $Verdict`nAI-Task: $Task`n" | Out-File -Encoding ascii -NoNewline $Path
}

function Run-CommitMsg([string]$MsgPath) {
  $posix = ($MsgPath -replace '\\','/')
  $null = & $Bash -c "'$($HooksDir -replace '\\','/')/commit-msg' '$posix'" 2>&1
  return $LASTEXITCODE
}

function Expect-MsgPass([string]$MsgPath, [string]$name) {
  if ((Run-CommitMsg $MsgPath) -eq 0) { OK $name } else { BAD "$name (commit-msg unexpectedly rejected)" }
}
function Expect-MsgFail([string]$MsgPath, [string]$name) {
  if ((Run-CommitMsg $MsgPath) -ne 0) { OK $name } else { BAD "$name (commit-msg unexpectedly accepted)" }
}

Write-Host "pre-commit cases:"

  Init-Repo
  Write-Task 'ok-task' 'PASS' 'PASS'
  Expect-PrePass '01 golden path accepts'

  Init-Repo
  Write-Task 'no-progress' 'PASS' 'PASS'
  Remove-Item ai_coding/active/no-progress/PROGRESS.md
  & git rm -q --cached ai_coding/active/no-progress/PROGRESS.md | Out-Null
  Expect-PreFail '02 missing PROGRESS.md rejects'

  Init-Repo
  Write-Task 'no-status' 'PASS' 'PASS'
  Remove-Item ai_coding/active/no-status/STATUS
  & git rm -q --cached ai_coding/active/no-status/STATUS | Out-Null
  Expect-PreFail '03 missing STATUS rejects'

  Init-Repo
  Write-Task 'no-dlog' 'PASS' 'PASS'
  Remove-Item ai_coding/active/no-dlog/disagreements.log
  & git rm -q --cached ai_coding/active/no-dlog/disagreements.log | Out-Null
  Expect-PreFail '04 missing disagreements.log rejects'

  Init-Repo
  Write-Task 'no-diff' 'PASS' 'PASS'
  Remove-Item ai_coding/active/no-diff/diff.patch
  & git rm -q --cached ai_coding/active/no-diff/diff.patch | Out-Null
  Expect-PreFail '05 missing diff.patch rejects'

  Init-Repo
  Write-Task 'no-review' 'PASS' 'PASS'
  Remove-Item ai_coding/active/no-review/review.md
  & git rm -q --cached ai_coding/active/no-review/review.md | Out-Null
  Expect-PreFail '06 missing review.md rejects'

  Init-Repo
  Write-Task 'status-unstaged' 'PASS' 'PASS'
  & git rm -q --cached ai_coding/active/status-unstaged/STATUS | Out-Null
  Expect-PreFail '07 STATUS on disk but unstaged rejects'

  Init-Repo
  Write-Task 'bad-status' 'PASS' 'PASS'
  'FOOBAR' | Out-File -Encoding ascii ai_coding/active/bad-status/STATUS
  & git add ai_coding/active/bad-status/STATUS | Out-Null
  Expect-PreFail "08 STATUS contents 'FOOBAR' rejects"

  # 8a. STATUS=CAP_REACHED (legacy verdict) rejects -- pin against resurfacing.
  Init-Repo
  Write-Task 'legacy-cap' 'PASS' 'PASS'
  'CAP_REACHED' | Out-File -Encoding ascii ai_coding/active/legacy-cap/STATUS
  & git add ai_coding/active/legacy-cap/STATUS | Out-Null
  Expect-PreFail '08a STATUS=CAP_REACHED (legacy) rejects'

  # 9. review.md VERDICT: FAIL is an intermediate state -- always rejects.
  Init-Repo
  Write-Task 'review-fail' 'OVERRIDE' 'FAIL' '[OVERRIDE] reason'
  Expect-PreFail '09 review.md VERDICT: FAIL rejects (intermediate state)'

  # 10. review.md VERDICT: OVERRIDE + STATUS=OVERRIDE + [OVERRIDE] accepts.
  Init-Repo
  Write-Task 'override-clean' 'OVERRIDE' 'OVERRIDE' '[OVERRIDE] reason'
  Expect-PrePass '10 review OVERRIDE + STATUS=OVERRIDE + [OVERRIDE] accepts'

  # 10a. review.md VERDICT: OVERRIDE without [OVERRIDE] in disagreements rejects.
  Init-Repo
  Write-Task 'override-no-marker' 'OVERRIDE' 'OVERRIDE' ''
  Expect-PreFail '10a review OVERRIDE without [OVERRIDE] marker rejects'

  # 10b. review.md VERDICT: OVERRIDE but STATUS=PASS rejects.
  Init-Repo
  Write-Task 'override-status-mismatch' 'PASS' 'OVERRIDE' '[OVERRIDE] reason'
  Expect-PreFail '10b review OVERRIDE but STATUS=PASS rejects'

  # 10c. review.md VERDICT: PASS but STATUS=OVERRIDE rejects.
  Init-Repo
  Write-Task 'pass-status-mismatch' 'OVERRIDE' 'PASS' '[OVERRIDE] reason'
  Expect-PreFail '10c review PASS but STATUS=OVERRIDE rejects'

  # 11. Close-out pure rename.
  Init-Repo
  New-Item -ItemType Directory -Path ai_coding/active/oldtask -Force | Out-Null
  'progress' | Out-File -Encoding ascii ai_coding/active/oldtask/PROGRESS.md
  & git add ai_coding/active/oldtask | Out-Null
  & git commit -q --no-verify -m 'set up oldtask' | Out-Null
  Closeout-Rename 'oldtask'
  Expect-PrePass '11 pure close-out rename accepts (exempt)'

  # 12. Close-out rename + unrelated non-task file.
  Init-Repo
  New-Item -ItemType Directory -Path ai_coding/active/oldtask2 -Force | Out-Null
  'progress' | Out-File -Encoding ascii ai_coding/active/oldtask2/PROGRESS.md
  & git add ai_coding/active/oldtask2 | Out-Null
  & git commit -q --no-verify -m 'set up oldtask2' | Out-Null
  Closeout-Rename 'oldtask2'
  'hi' | Out-File -Encoding ascii unrelated.txt
  & git add unrelated.txt | Out-Null
  Expect-PrePass '12 close-out rename + unrelated non-task file accepts'

  # 13. No ai_coding paths staged at all.
  Init-Repo
  'x' | Out-File -Encoding ascii unrelated.txt
  & git add unrelated.txt | Out-Null
  Expect-PrePass '13 no ai_coding paths staged accepts'

  # 13a. Missing VERDICT line + STATUS=PASS -> reject.
  Init-Repo
  Write-Task 'no-verdict-pass' 'PASS' 'PASS'
  $rfile = 'ai_coding/active/no-verdict-pass/review.md'
  (Get-Content $rfile) | Where-Object { $_ -notmatch '^VERDICT:' } | Set-Content $rfile -Encoding ascii
  & git add $rfile | Out-Null
  Expect-PreFail '13a missing VERDICT + STATUS=PASS rejects'

  # 13b. Missing VERDICT line + STATUS=OVERRIDE + [OVERRIDE] -> accept.
  Init-Repo
  Write-Task 'no-verdict-override' 'OVERRIDE' 'PASS' '[OVERRIDE] reason'
  $rfile = 'ai_coding/active/no-verdict-override/review.md'
  (Get-Content $rfile) | Where-Object { $_ -notmatch '^VERDICT:' } | Set-Content $rfile -Encoding ascii
  & git add $rfile | Out-Null
  Expect-PrePass '13b missing VERDICT + STATUS=OVERRIDE + [OVERRIDE] accepts'

  Write-Host "commit-msg cases:"

  Init-Repo
  Write-Task 'good' 'PASS' 'PASS'
  Write-Msg msg.txt 'good' 'PASS'
  Expect-MsgPass 'msg.txt' '14 trailers + STATUS=PASS match accepts'

  Init-Repo
  'feat: no trailers' | Out-File -Encoding ascii msg.txt
  Expect-MsgFail 'msg.txt' '15 missing trailers rejects'

  Init-Repo
  Write-Task 'good2' 'PASS' 'PASS'
  Write-Msg msg.txt 'good2' 'SOMETHING'
  Expect-MsgFail 'msg.txt' '16 malformed AI-Verdict rejects'

  # 16a. CAP_REACHED in AI-Verdict (legacy) rejects -- regression pin.
  Init-Repo
  Write-Task 'legacy-cap-trailer' 'PASS' 'PASS'
  Write-Msg msg.txt 'legacy-cap-trailer' 'CAP_REACHED'
  Expect-MsgFail 'msg.txt' '16a AI-Verdict: CAP_REACHED (legacy) rejects'

  Init-Repo
  Write-Task 'mismatch' 'PASS' 'PASS'
  Write-Msg msg.txt 'mismatch' 'OVERRIDE'
  Expect-MsgFail 'msg.txt' '17 STATUS=PASS but AI-Verdict=OVERRIDE rejects'

  Init-Repo
  Write-Task 'review-fail-but-pass-trailer' 'OVERRIDE' 'FAIL' '[OVERRIDE] x'
  'PASS' | Out-File -Encoding ascii ai_coding/active/review-fail-but-pass-trailer/STATUS
  & git add ai_coding/active/review-fail-but-pass-trailer/STATUS | Out-Null
  Write-Msg msg.txt 'review-fail-but-pass-trailer' 'PASS'
  Expect-MsgFail 'msg.txt' '18 review FAIL but AI-Verdict=PASS rejects'

  # 18a. review.md VERDICT: OVERRIDE + AI-Verdict=OVERRIDE + STATUS=OVERRIDE accepts.
  Init-Repo
  Write-Task 'msg-override-clean' 'OVERRIDE' 'OVERRIDE' '[OVERRIDE] x'
  Write-Msg msg.txt 'msg-override-clean' 'OVERRIDE'
  Expect-MsgPass 'msg.txt' '18a OVERRIDE end-to-end accepts'

  Init-Repo
  New-Item -ItemType Directory -Path ai_coding/active/oldtask3 -Force | Out-Null
  'progress' | Out-File -Encoding ascii ai_coding/active/oldtask3/PROGRESS.md
  & git add ai_coding/active/oldtask3 | Out-Null
  & git commit -q --no-verify -m 'set up oldtask3' | Out-Null
  Closeout-Rename 'oldtask3'
  Write-Msg msg.txt 'archive-oldtask3' 'PASS'
  Expect-MsgPass 'msg.txt' '19 close-out commit-msg accepts with bare trailers'

  Write-Host "post-commit cases:"

  # 20. Archive-only routing.
  Init-Repo
  New-Item -ItemType Directory -Path ai_coding/archive/already-archived -Force | Out-Null
  'old' | Out-File -Encoding ascii ai_coding/archive/already-archived/PROGRESS.md
  & git add ai_coding/archive/already-archived | Out-Null
  & git commit -q --no-verify -m 'prep already-archived' | Out-Null
  'change' | Out-File -Encoding ascii scratch.txt
  & git add scratch.txt | Out-Null
  & git commit -q --no-verify -m "scratch`n`nAI-Verdict: PASS`nAI-Task: already-archived" | Out-Null
  $diffInArchive   = @(Get-ChildItem -Path ai_coding/archive/already-archived -Filter 'diff_*.patch' -ErrorAction SilentlyContinue).Count
  $activeDirExists = Test-Path -LiteralPath ai_coding/active/already-archived
  if ($diffInArchive -ge 1 -and -not $activeDirExists) {
    OK '20 routing: archive-only -> diff in archive, no active stub'
  } else {
    BAD "20 routing: archive-only (diffInArchive=$diffInArchive activeDirExists=$activeDirExists)"
  }

  # 21. CRITICAL: close-out rename -- fix B regression pin.
  Init-Repo
  New-Item -ItemType Directory -Path ai_coding/active/closing-task -Force | Out-Null
  'progress' | Out-File -Encoding ascii ai_coding/active/closing-task/PROGRESS.md
  & git add ai_coding/active/closing-task | Out-Null
  & git commit -q --no-verify -m 'set up closing-task' | Out-Null
  Closeout-Rename 'closing-task'
  & git commit -q --no-verify -m "close out`n`nAI-Verdict: PASS`nAI-Task: closing-task" | Out-Null
  $diffInArchive   = @(Get-ChildItem -Path ai_coding/archive/closing-task -Filter 'diff_*.patch' -ErrorAction SilentlyContinue).Count
  $activeDirExists = Test-Path -LiteralPath ai_coding/active/closing-task
  if ($diffInArchive -ge 1 -and -not $activeDirExists) {
    OK '21 close-out rename -> diff in archive, no active stub (fix B)'
  } else {
    BAD "21 close-out rename (diffInArchive=$diffInArchive activeDirExists=$activeDirExists)"
  }

  # 22. Active-exists routing.
  Init-Repo
  New-Item -ItemType Directory -Path ai_coding/active/normal-task -Force | Out-Null
  'progress' | Out-File -Encoding ascii ai_coding/active/normal-task/PROGRESS.md
  & git add ai_coding/active/normal-task | Out-Null
  & git commit -q --no-verify -m 'set up normal-task' | Out-Null
  'edit' | Out-File -Encoding ascii note.txt
  & git add note.txt | Out-Null
  & git commit -q --no-verify -m "scratch`n`nAI-Verdict: PASS`nAI-Task: normal-task" | Out-Null
  $diffInActive = @(Get-ChildItem -Path ai_coding/active/normal-task -Filter 'diff_*.patch' -ErrorAction SilentlyContinue).Count
  if ($diffInActive -ge 1) {
    OK '22 routing: active exists -> diff in active'
  } else {
    BAD "22 routing: active exists (diffInActive=$diffInActive)"
  }

  # 23. Fallback: neither.
  Init-Repo
  'edit' | Out-File -Encoding ascii note.txt
  & git add note.txt | Out-Null
  & git commit -q --no-verify -m "scratch`n`nAI-Verdict: PASS`nAI-Task: brand-new-task" | Out-Null
  $diffInActive = @(Get-ChildItem -Path ai_coding/active/brand-new-task -Filter 'diff_*.patch' -ErrorAction SilentlyContinue).Count
  if ($diffInActive -ge 1) {
    OK '23 routing: neither exists -> fallback to active'
  } else {
    BAD "23 routing: neither (diffInActive=$diffInActive)"
  }

Write-Host ""
Write-Host ("hooks-selftest: {0} passed, {1} failed" -f $Pass, $Fail)

# Cleanup -- best-effort, never blocks the result.
Set-Location -LiteralPath $RepoRoot
if (Test-Path -LiteralPath $Script:CleanupPath) {
  Remove-Item -LiteralPath $Script:CleanupPath -Recurse -Force -ErrorAction SilentlyContinue
}

if ($Fail -ne 0) {
  Write-Host 'failed cases:'
  foreach ($n in $Failed) { Write-Host "    - $n" }
  exit 1
}
exit 0
