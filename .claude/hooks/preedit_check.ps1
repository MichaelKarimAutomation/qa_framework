# PreToolUse hook (Edit|Write|MultiEdit): enforces CLAUDE.md §2.
# Blocks edits outside ai_coding/active/<task>/ when no active task folder
# exists. Always allows edits inside .claude/ and ai_coding/ so the task
# folder itself can be created and these hooks themselves can be edited.

$ErrorActionPreference = 'Stop'
$repoRoot = 'c:\Coding\qa_framework'
$activeDir = Join-Path $repoRoot 'ai_coding\active'

$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
$filePath = $payload.tool_input.file_path
if (-not $filePath) { exit 0 }

try { $full = [System.IO.Path]::GetFullPath($filePath) } catch { exit 0 }
$norm = $full.ToLower().Replace('/', '\')

$alwaysAllowPrefixes = @(
    (Join-Path $repoRoot 'ai_coding\').ToLower().Replace('/', '\'),
    (Join-Path $repoRoot '.claude\').ToLower().Replace('/', '\')
)
foreach ($prefix in $alwaysAllowPrefixes) {
    if ($norm.StartsWith($prefix)) { exit 0 }
}

$hasActive = $false
if (Test-Path $activeDir) {
    $folders = @(Get-ChildItem -Path $activeDir -Directory -ErrorAction SilentlyContinue)
    if ($folders.Count -gt 0) { $hasActive = $true }
}

if (-not $hasActive) {
    $reason = "CLAUDE.md section 2: no active task folder under ai_coding/active/. Target: $filePath. Required first step: create ai_coding/active/<task>/ with PROGRESS.md, disagreements.log, STATUS (pending). Then editing source files is permitted."
    $out = @{
        hookSpecificOutput = @{
            hookEventName = 'PreToolUse'
            permissionDecision = 'deny'
            permissionDecisionReason = $reason
        }
    } | ConvertTo-Json -Depth 5 -Compress
    Write-Output $out
}
exit 0
