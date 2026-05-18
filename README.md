# QA Automation Framework

A production-quality Python-based QA automation framework built from scratch, covering UI, API, performance, and contract testing. Designed with scalability, maintainability, and CI/CD integration in mind.

---

## Table of Contents

- [Overview](#overview)
- [Stack](#stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [CI/CD](#cicd)
- [Reporting](#reporting)

---

## Overview

This framework was built to demonstrate SDET-level engineering — not just writing tests, but making deliberate architectural decisions, building reusable infrastructure, and integrating the full delivery pipeline.

**Test targets:**
- **UI:** [TodoMVC](https://demo.playwright.dev/todomvc) — Playwright-driven end-to-end tests with Page Object Model
- **API:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — REST API tests with a centralized httpx client
- **Browser Mocking:** [Rahul Shetty's Grocery Site](https://rahulshettyacademy.com/seleniumPractise/#/) — Playwright `page.route()` interception

**Key design decisions:**
- Layered architecture chosen over hexagonal for faster iteration and lower onboarding cost
- `httpx` over `requests` for async-readiness and modern API design
- `factory_boy` integrated from the start rather than bolted on later
- `jsonschema` over `pact-python` — eliminates native binary compilation issues while covering the core contract validation use case
- Separate `.env` files per environment with CLI flag (`--env`) for environment switching

---

## Stack

| Category | Tool |
|---|---|
| Language & Package Management | Python 3.13, uv |
| Test Framework | pytest, pytest-xdist, pytest-rerunfailures |
| UI Automation | Playwright, pytest-playwright |
| API Client | httpx |
| Test Data | Faker, Factory Boy |
| Mocking | pytest-httpserver, Playwright page.route() |
| Contract Testing | jsonschema |
| Performance | Locust |
| Reporting | Allure |
| Code Quality | Ruff |
| Environment Config | pytest-dotenv |
| Containerization | Docker |
| CI/CD | GitHub Actions, GitLab CI |

---

## Architecture

```
qa_framework/
├── pom/                    # Page Object Model — UI interaction layer
├── tests/
│   ├── ui/                 # Playwright UI tests
│   ├── api/                # httpx API tests
│   └── conftest.py         # Shared fixtures
├── utils/
│   └── api_client.py       # Centralized API client with Allure attachments
├── data/
│   └── factories.py        # Factory Boy factories with Faker
├── performance/
│   └── locustfile.py       # Locust load test definitions
├── scripts/
│   ├── setup-windows.ps1   # Windows setup automation
│   ├── setup-linux.sh      # Linux/Docker setup automation
│   └── delete_reports.py   # Cross-platform report cleanup
├── docs/                   # Installation guides
├── .github/workflows/      # GitHub Actions CI pipeline
├── .gitlab-ci.yml          # GitLab CI pipeline
├── Dockerfile              # Container definition
├── Makefile                # Developer shortcuts
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
| `docs/install-windows.html` | Full Windows setup from scratch |
| `docs/install-docker.html` | Docker-based setup |

**Quick start (Windows):**
```bash
python install.py
```

**Quick start (Docker):**
```bash
docker build -t qa-framework .
make docker-run
```

---

## Running Tests

| Command | Description |
|---|---|
| `make test` | Run all tests against UAT |
| `make smoke` | Run smoke tests only |
| `make parallel` | Run all tests in parallel |
| `make docker-build` | Build the Docker image |
| `make docker-run` | Run tests in Docker |
| `make report` | Open Allure report locally |
| `make lint` | Run Ruff linter |
| `make format` | Run Ruff formatter |

**Environment selection:**
```bash
pytest tests/ --env=dev_env
pytest tests/ --env=uat_env
```

**Run by marker:**
```bash
pytest tests/ -m smoke
pytest tests/ -m "api and regression"
```

---

## CI/CD

**GitHub Actions** — triggers on push and pull request to `master`. Supports manual environment selection (dev/uat) via workflow dispatch.

**GitLab CI** — equivalent pipeline for GitLab environments. Environment selection via CI/CD variables.

Both pipelines:
- Install dependencies via `uv`
- Install Playwright browsers with system dependencies
- Run the full test suite
- Upload Allure results as artifacts
- Deploy the Allure report to GitHub Pages (GitHub Actions)

Live report: [GitHub Pages](https://michaelkarimautomation.github.io/qa_framework/)

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
