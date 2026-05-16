import pytest
import os
from utils.api_client import APIClient


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, 'rep_' + rep.when, rep)


@pytest.fixture
def todo_url():
    return os.getenv('TODOMVC_URL')


@pytest.fixture
def grocery_url():
    return os.getenv('SELENIUM_PRACTISE_URL')


@pytest.fixture
def practice_url():
    return os.getenv('SELENIUM_PRACTICE2_URL')


@pytest.fixture(scope='session')  # Ran once per scope
def api_client():
    client = APIClient()
    yield client
    client.close()


def pytest_configure(config):
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
