import pytest
import os
from utils.api_client import APIClient


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture
def todo_url():
    return os.getenv("TODOMVC_URL")

@pytest.fixture(scope="session")    # Ran once per scope
def api_client():
    client = APIClient()
    yield client
    client.close()
