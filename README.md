# QA Automation Framework

A production-quality Python-based QA automation framework built from scratch, covering UI, API, performance, and contract testing. Designed with scalability, maintainability, and CI/CD integration in mind.

---

## Table of Contents

- [Overview](#overview)
- [Stack](#stack)
- [Architecture](#architecture)
- [Repository hooks](#repository-hooks)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [Reporting](#reporting)

---

## Overview

A reference QA automation framework covering UI, API, performance, and contract testing, with reusable infrastructure and CI/CD wired in.

**Test targets:**
- **UI:** [TodoMVC](https://demo.playwright.dev/todomvc) — Playwright-driven end-to-end tests with Page Object Model
- **API:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — REST API tests with a centralized httpx client
- **UI (mocked):** [Rahul Shetty's Grocery Site](https://rahulshettyacademy.com/seleniumPractise/#/) — Playwright `page.route()` request interception

**Key design decisions:**
- Layered architecture chosen over hexagonal for faster iteration and lower onboarding cost
- `httpx` over `requests` for async-readiness and modern API design
- `factory_boy` integrated from the start rather than bolted on later
- `jsonschema` over `pact-python` — covers schema-shape validation without the native-binary deployment friction. The trade-off: this does not replace Pact's consumer-driven / provider-state contract testing, which is the stronger guarantee Pact offers.

---

## Stack

Python 3.13 + uv · pytest · Playwright · httpx · Locust · Allure · Ruff · GitHub Actions · Docker

See [pyproject.toml](pyproject.toml) for the full dependency list.

---

## Architecture

```
qa_framework/
├── pom/                    # Page Object Model — UI interaction layer
├── tests/
│   ├── ui/                 # Playwright UI tests
│   ├── api/                # httpx API tests
│   ├── config/             # Environment / configuration tests
│   └── conftest.py         # Session-scoped fixtures and .env validation
├── utils/
│   └── api_client.py       # Centralized API client with Allure attachments
├── data/
│   └── factories.py        # Factory Boy factories with Faker
├── performance/
│   └── *.py                # Locust load test definitions
├── scripts/                # Setup, docs build, report cleanup, make-help helpers
├── tools/                  # Git hook installers + versioned hooks under tools/hooks/
├── docs/                   # Sphinx source + bundled HTML install guides
├── .github/workflows/      # GitHub Actions CI pipelines (tests + docs deploy)
├── ai_coding/              # CLAUDE.md task pipeline (active/, archive/, reviewer.py)
├── .env.example            # Required env-var template; conftest validates against it
├── Dockerfile              # Container definition
├── Makefile                # Developer shortcuts (run `make help`)
├── install.py              # Cross-platform setup entry point
└── pyproject.toml          # Dependencies, markers, pytest config
```

**Layers:**
- **Tests** — what to verify
- **POM** — how to interact with the UI
- **API Client** — how to talk to APIs
- **Factories** — how to generate test data
- **Fixtures** — environment, setup, teardown

---

## Repository hooks

Git hooks are version-controlled under [tools/hooks/](tools/hooks/) and
activated via `core.hooksPath`. They enforce the CLAUDE.md §2-§7 pipeline
locally (artifact presence, STATUS validity, trailer consistency, diff
routing). After every fresh clone, run one of:

```powershell
# Windows (PowerShell)
.\tools\install-hooks.ps1
```

```bash
# Linux / macOS / Git for Windows bash
bash tools/install-hooks.sh
```

This sets `git config core.hooksPath tools/hooks`. The hooks then fire on
every commit in that clone, with no per-machine drift. To verify the hooks,
run the self-test (no pytest / ollama needed):

```bash
bash tools/hooks-selftest.sh
# or:  powershell -File tools/hooks-selftest.ps1
```

---

## Installation

Two installation paths are available. Full step-by-step guides are in the `docs/` folder:

| Guide | Description |
|---|---|
| `docs/installation_guide_windows.html` | Full Windows setup from scratch |
| `docs/installation_guide_docker.html` | Docker-based setup |

API documentation (Sphinx-generated, deployed on every push to `master`): [michaelkarimautomation.github.io/qa_framework/reference/](https://michaelkarimautomation.github.io/qa_framework/reference/)

**Quick start (host install, any OS):**
```bash
python install.py
```

**Quick start (Docker):**
```bash
make docker-build
make docker-run
```

---

## Running Tests

A `Makefile` wraps the common workflows — run `make help` to list every target. Most-used: `make test`, `make report`, `make smoke`, `make parallel`.

**Run by marker:**
```bash
pytest tests/ -m smoke
pytest tests/ -m "api and regression"
```

---

## CI/CD

**GitHub Actions** — triggers on push and pull request to `master`, with manual runs available via workflow dispatch.

The pipeline:
- Installs dependencies via `uv`
- Installs Playwright browsers with system dependencies
- Runs the full test suite
- Uploads Allure results as artifacts
- Deploys the Allure report to GitHub Pages

Live Allure report: [michaelkarimautomation.github.io/qa_framework/smoke/](https://michaelkarimautomation.github.io/qa_framework/smoke/)

---

## Reporting

Allure reports are generated automatically on every test run.

**View locally:**
```bash
make test
make report
```

**View in CI:**
The latest report is published to GitHub Pages after every push to `master`.

Reports include:
- Pass/fail status per test
- Step-by-step execution log
- Request/response attachments for API tests
- Screenshots on UI test failure
- Retry history for flaky tests
