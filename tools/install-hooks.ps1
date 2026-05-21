# install-hooks.ps1 -- point git at tools/hooks/ so the CLAUDE.md gates fire
# on every commit in this clone.
#
# Run this once after cloning. Re-run is idempotent.

$ErrorActionPreference = 'Stop'

$repoRoot = (& git rev-parse --show-toplevel).Trim()
$hooksDir = Join-Path $repoRoot 'tools\hooks'

if (-not (Test-Path -LiteralPath $hooksDir -PathType Container)) {
    Write-Error "error: $hooksDir does not exist -- run from the qa_framework clone"
    exit 1
}

$gitVer = (& git --version) -replace '^git version ', ''
$verParts = $gitVer.Split('.')
$major = [int]$verParts[0]
$minor = [int]$verParts[1]
if ($major -lt 2 -or ($major -eq 2 -and $minor -lt 9)) {
    Write-Error "error: git $gitVer is too old; core.hooksPath needs git >= 2.9"
    exit 1
}

foreach ($h in @('pre-commit', 'commit-msg', 'post-commit')) {
    $p = Join-Path $hooksDir $h
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) {
        Write-Error "error: missing $p"
        exit 1
    }
}

& git config core.hooksPath tools/hooks

Write-Host 'installed: core.hooksPath = tools/hooks'
Write-Host '  pre-commit   : enforces CLAUDE.md sections 2-6 artifact presence (PASS | OVERRIDE)'
Write-Host '  commit-msg   : enforces section 7 trailers + section 6-7 trailer consistency'
Write-Host '  post-commit  : routes the just-committed diff into the task folder'
