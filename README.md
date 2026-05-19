# QA Automation Framework

A Python-based QA automation framework built from scratch, covering UI, API, performance, and contract testing. Designed with scalability, maintainability, and CI/CD integration in mind.

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

**Test targets:**
- **UI smoke** ([TodoMVC](https://demo.playwright.dev/todomvc)): single add-and-verify check against the TodoMVC demo.
- **UI end-to-end** ([Rahul Shetty practice page](https://rahulshettyacademy.com/AutomationPractice/)): full POM exercise of forms, dropdowns, alerts, windows, tabs, hover, and iframes.
- **UI (mocked)** ([Rahul Shetty grocery site](https://rahulshettyacademy.com/seleniumPractise/#/)): Playwright `page.route()` request interception.
- **API** ([JSONPlaceholder](https://jsonplaceholder.typicode.com)): REST API tests with a shared httpx client.

**Key design decisions:**
- Layered architecture chosen over hexagonal for faster iteration and lower onboarding cost.
- `httpx` instead of `requests`: supports async if we need it later, with the same synchronous API.
- `factory_boy` + `Faker` for test data: generates realistic data on demand instead of hardcoded fixtures.
- `jsonschema` instead of `pact-python`: easier to install (Pact needs native binaries that often fail on Windows and CI). Trade-off: `jsonschema` only checks that an API response has the right shape. It can't verify that both sides of an API stay in agreement the way Pact does.

---

## Stack

Python 3.13 + uv · pytest · Playwright · httpx · Locust · Allure · Ruff · GitHub Actions · Docker

See [pyproject.toml](pyproject.toml) for the full dependency list.

---

## Architecture

```
qa_framework/
├── pom/                    # UI interaction layer (Page Object Model)
├── tests/
│   ├── ui/                 # Playwright UI tests
│   ├── api/                # httpx API tests
│   ├── config/             # Environment / configuration tests
│   └── conftest.py         # Session-scoped fixtures and .env validation
├── utils/
│   └── api_client.py       # Shared API client; attaches request/response to Allure
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
- **Tests**: what to verify
- **POM**: how to interact with the UI
- **API Client**: how to talk to APIs
- **Factories**: how to generate test data
- **Fixtures**: environment, setup, teardown

---

## Repository hooks

Git hooks live under [tools/hooks/](tools/hooks/) and are tracked in git,
so every clone has the same versioned set. `python install.py` activates
them automatically by setting `core.hooksPath` to `tools/hooks`. If you
skipped install.py, you can activate them manually with:

```powershell
# Windows (PowerShell)
.\tools\install-hooks.ps1
```

```bash
# Linux / macOS / Git for Windows bash
bash tools/install-hooks.sh
```

The hooks check the CLAUDE.md §2-§7 rules on each commit: required task
files are present, STATUS is valid, commit trailers match the local
review, and diffs land in the right task folder. To verify the hooks
without running pytest or ollama, run the self-test:

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

A `Makefile` wraps the common workflows. Run `make help` to list every target. Most-used: `make test`, `make report`, `make smoke`, `make parallel`.

**Run by marker:**
```bash
pytest tests/ -m smoke
pytest tests/ -m "api and regression"
```

---

## CI/CD

**GitHub Actions** runs on every push and pull request to `master`. It can also be triggered manually from the GitHub UI.

The pipeline:
- Installs dependencies via `uv`
- Installs Playwright browsers with system dependencies
- Runs the full test suite
- Uploads Allure results as artifacts
- Deploys the Allure report to GitHub Pages

Live Allure report: [michaelkarimautomation.github.io/qa_framework/allure-suite/](https://michaelkarimautomation.github.io/qa_framework/allure-suite/)

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
- Playwright trace zip on UI failure: stored at `test-results/<test-name>/trace.zip` and also attached to the Allure report. Open at [trace.playwright.dev](https://trace.playwright.dev/) to replay every action and network call.
- Retry history for flaky tests
