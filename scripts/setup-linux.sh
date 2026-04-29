#!/bin/bash
# QA Framework - Linux/Docker Setup Script
# Run via: install.py

set -e

echo "=== QA Framework Linux/Docker Setup ==="

PATHS_TO_ADD=()

# ─── Detect if running in Docker ─────────────────────────────────────────────
IN_DOCKER=false
if [ -f /.dockerenv ]; then
    IN_DOCKER=true
    echo "Docker environment detected."
fi

# ─── System Dependencies ─────────────────────────────────────────────────────
echo ""
echo "Installing system dependencies..."
apt-get update -qq
apt-get install -y -qq wget curl make default-jre-headless

# ─── Install Allure ───────────────────────────────────────────────────────────
echo ""
echo "Installing Allure..."
if ! command -v allure &> /dev/null; then
    wget -q -O allure.tgz https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz
    tar -zxf allure.tgz
    mv allure-2.32.0 /opt/allure
    rm allure.tgz
    PATHS_TO_ADD+=("/opt/allure/bin")
    echo "Allure installed."
else
    echo "Allure already installed, skipping."
fi

# ─── Install uv ──────────────────────────────────────────────────────────────
echo ""
echo "Installing uv..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    PATHS_TO_ADD+=("$HOME/.local/bin")
    echo "uv installed."
else
    echo "uv already installed, skipping."
fi

# ─── Update PATH ─────────────────────────────────────────────────────────────
if [ ${#PATHS_TO_ADD[@]} -gt 0 ]; then
    echo ""
    echo "Updating PATH..."
    SHELL_RC="$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    for PATH_ENTRY in "${PATHS_TO_ADD[@]}"; do
        if ! grep -q "$PATH_ENTRY" "$SHELL_RC" 2>/dev/null; then
            echo "export PATH=\"$PATH_ENTRY:\$PATH\"" >> "$SHELL_RC"
        fi
        export PATH="$PATH_ENTRY:$PATH"
    done
    echo "PATH updated."
fi

# ─── Virtual Environment ─────────────────────────────────────────────────────
echo ""
echo "Creating virtual environment..."
uv venv --clear
echo "Virtual environment created."

# ─── Install Python Dependencies ─────────────────────────────────────────────
echo ""
echo "Installing Python dependencies..."
uv add pytest pytest-xdist pytest-rerunfailures playwright pytest-playwright httpx allure-pytest faker factory-boy sqlalchemy psycopg2-binary testcontainers pytest-dotenv ruff pytest-httpserver locust jsonschema
echo "Python dependencies installed."

# ─── Install Playwright Browsers ─────────────────────────────────────────────
echo ""
echo "Installing Playwright browsers..."
uv run playwright install --with-deps chromium
echo "Playwright browsers installed."

# ─── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup Complete ==="
echo "Next steps:"
echo "  1. Copy .env.example to .env and fill in values"
if [ "$IN_DOCKER" = false ]; then
    echo "  2. Restart your terminal to apply PATH changes"
    echo "  3. Run: make test"
else
    echo "  2. Run: make test"
fi
