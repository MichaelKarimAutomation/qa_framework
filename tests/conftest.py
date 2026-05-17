import pytest
import os
from utils.api_client import APIClient


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach each phase's TestReport (setup/call/teardown) onto the test item as `rep_setup`/`rep_call`/`rep_teardown`. This is what lets fixtures like `screenshot_on_failure` ask `request.node.rep_call.failed` after the test body has run."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, 'rep_' + rep.when, rep)


@pytest.fixture
def todo_url():
    """Return the TodoMVC base URL from the TODOMVC_URL env var, so tests don't hardcode the target environment."""
    return os.getenv('TODOMVC_URL')


@pytest.fixture
def grocery_url():
    """Return the grocery practice site URL from the SELENIUM_PRACTISE_URL env var."""
    return os.getenv('SELENIUM_PRACTISE_URL')


@pytest.fixture
def practice_url():
    """Return the rahulshettyacademy practice page URL from the SELENIUM_PRACTICE2_URL env var."""
    return os.getenv('SELENIUM_PRACTICE2_URL')


@pytest.fixture(scope='session')
def api_client():
    """Provide a single APIClient instance for the entire test session and close it during teardown. Session scope avoids the overhead of rebuilding the underlying HTTP connection pool for every API test."""
    client = APIClient()
    yield client
    client.close()


def pytest_configure(config):
    """Run once at pytest startup: load .env into the process environment, then read .env.example and fail-fast with a clear error if any key that has a non-empty value in the template is missing locally. Prevents tests from running against partial config and silently producing misleading failures."""
    from dotenv import load_dotenv
    from pathlib import Path

    load_dotenv('.env', override=True)

    missing = []
    for line in Path('.env.example').read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, _, value = line.partition('=')
        if value and not os.getenv(key):
            missing.append(key)

    if missing:
        raise RuntimeError(f"Missing required env vars (see .env.example): {', '.join(missing)}")
