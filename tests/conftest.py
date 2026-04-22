import pytest
import os
import allure
from utils.api_client import APIClient
from playwright.sync_api import Page, BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,    # spread existing defaults, override/add to them
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    if request.node.rep_call.failed:
        allure.attach(
            page.screenshot(),
            name="Screenshot on failure",
            attachment_type=allure.attachment_type.PNG
        )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture
def todo_url():
    return os.getenv("TODOMVC_URL")

@pytest.fixture
def api_client(scope="session"):
    client = APIClient()
    yield client
    client.close()
