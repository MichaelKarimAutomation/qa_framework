# UserPromptSubmit hook: injects CLAUDE.md pipeline state into Claude's
# context every turn. If no task folder exists under ai_coding/active/,
# warns that any code edit needs one first.

$repoRoot = 'c:\Coding\qa_framework'
$activeDir = Join-Path $repoRoot 'ai_coding\active'

$folders = @()
if (Test-Path $activeDir) {
    $folders = @(Get-ChildItem -Path $activeDir -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Name })
}

if ($folders.Count -eq 0) {
    $msg = 'CLAUDE.md PIPELINE STATE: no active task folder under ai_coding/active/. Per CLAUDE.md section 2, the FIRST step before any code edit (Edit/Write/MultiEdit on source files) is to create ai_coding/active/<task>/ with PROGRESS.md, disagreements.log, and STATUS. Read-only ops (Read/Grep/Glob/Bash for git status etc) are unrestricted. The PreToolUse hook will deny edits outside ai_coding/ and .claude/ until a task folder exists.'
} else {
    $names = $folders -join ', '
    $msg = "CLAUDE.md PIPELINE STATE: active task folder(s): $names. Continue following CLAUDE.md sections 3-9 (write/update tests, run pytest within cap, invoke ai_coding/reviewer.py, update PROGRESS.md at boundaries, commit with AI-Verdict + AI-Task trailers)."
}

$out = @{
    hookSpecificOutput = @{
        hookEventName = 'UserPromptSubmit'
        additionalContext = $msg
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $out
exit 0
