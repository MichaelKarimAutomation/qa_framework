# QA Framework - Windows Setup Script
# Run via: python scripts/setup.py

$ErrorActionPreference = "Stop"
$PathsToAdd = @()

Write-Host "=== QA Framework Windows Setup ===" -ForegroundColor Cyan

# ─── Install Scoop ───────────────────────────────────────────────────────────
Write-Host "`nInstalling Scoop..." -ForegroundColor Yellow
if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    $PathsToAdd += "$env:USERPROFILE\scoop\shims"
    Write-Host "Scoop installed." -ForegroundColor Green
} else {
    Write-Host "Scoop already installed, skipping." -ForegroundColor Gray
}

# ─── Install Java, Make, Allure via Scoop ────────────────────────────────────
Write-Host "`nInstalling Java, Make, and Allure via Scoop..." -ForegroundColor Yellow
scoop bucket add java | Out-Null
$scoopPackages = @()
    if (-not (Get-Command allure -ErrorAction SilentlyContinue)) { $scoopPackages += "allure" }
    if (-not (Get-Command make -ErrorAction SilentlyContinue)) { $scoopPackages += "make" }
    if (-not (scoop list | Select-String "temurin-lts-jdk")) { $scoopPackages += "temurin-lts-jdk" }
    if ($scoopPackages.Count -gt 0) {
        scoop install @scoopPackages
    } else {
        Write-Host "Java, Make, and Allure already installed, skipping." -ForegroundColor Gray
    }
Write-Host "Java, Make, and Allure installed." -ForegroundColor Green

# ─── Install uv ──────────────────────────────────────────────────────────────
Write-Host "`nInstalling uv..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Invoke-RestMethod -Uri https://astral.sh/uv/install.ps1 | Invoke-Expression
    $PathsToAdd += "$env:USERPROFILE\.local\bin"
    Write-Host "uv installed." -ForegroundColor Green
} else {
    Write-Host "uv already installed, skipping." -ForegroundColor Gray
}

# ─── Update PATH ─────────────────────────────────────────────────────────────
if ($PathsToAdd.Count -gt 0) {
    Write-Host "`nUpdating PATH..." -ForegroundColor Yellow
    $CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    foreach ($Path in $PathsToAdd) {
        if ($CurrentPath -notlike "*$Path*") {
            $CurrentPath += ";$Path"
            Write-Host "Added to PATH: $Path" -ForegroundColor Green
        }
    }
    [Environment]::SetEnvironmentVariable("PATH", $CurrentPath, "User")
    $env:PATH += ";" + ($PathsToAdd -join ";")
    Write-Host "PATH updated." -ForegroundColor Green
}

# ─── Virtual Environment ─────────────────────────────────────────────────────
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
uv venv
Write-Host "Virtual environment created." -ForegroundColor Green

# ─── Install Python Dependencies ─────────────────────────────────────────────
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
uv add pytest pytest-xdist pytest-rerunfailures playwright pytest-playwright httpx allure-pytest faker factory-boy sqlalchemy psycopg2-binary testcontainers pytest-dotenv ruff pytest-httpserver locust jsonschema
Write-Host "Python dependencies installed." -ForegroundColor Green

# ─── Install Playwright Browsers ─────────────────────────────────────────────
Write-Host "`nInstalling Playwright browsers..." -ForegroundColor Yellow
uv run playwright install
Write-Host "Playwright browsers installed." -ForegroundColor Green

# ─── Done ─────────────────────────────────────────────────────────────────────
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Copy .env.example to .env and fill in values" -ForegroundColor White
Write-Host "  2. Select Python interpreter in VS Code (Ctrl+Shift+P -> Python: Select Interpreter)" -ForegroundColor White
Write-Host "  3. Run: make test" -ForegroundColor White
