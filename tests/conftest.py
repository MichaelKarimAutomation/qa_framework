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


@pytest.fixture
def grocery_url():
    return os.getenv("SELENIUM_PRACTISE_URL")


@pytest.fixture(scope="session")  # Ran once per scope
def api_client():
    client = APIClient()
    yield client
    client.close()


def pytest_addoption(parser):
    parser.addoption("--env", default="uat", help="Environment to run tests against")


def pytest_configure(config):
    env = config.getoption("--env", default="uat")
    env_file = f".env.{env}"
    from dotenv import load_dotenv

    load_dotenv(env_file, override=True)
