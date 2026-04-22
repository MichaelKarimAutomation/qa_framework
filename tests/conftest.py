import pytest
import os
from utils.api_client import APIClient
from playwright.sync_api import Page, BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,    # spread existing defaults, override/add to them
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.fixture
def todo_url():
    return os.getenv("TODOMVC_URL")

@pytest.fixture
def api_client(scope="session"):
    client = APIClient()
    yield client
    client.close()
