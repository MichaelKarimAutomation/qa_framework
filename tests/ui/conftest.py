import pytest
import allure


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    """Override pytest-playwright's browser context for the UI test session: force a 1920x1080 viewport and ignore HTTPS certificate errors."""
    return {
        **browser_context_args,  # spread existing defaults, override/add to them
        'viewport': {'width': 1920, 'height': 1080},
        'ignore_https_errors': True,
    }


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    """Auto-attach a screenshot of the page to the Allure report whenever a UI test fails, so failures can be debugged visually."""
    yield
    if request.node.rep_call.failed:
        allure.attach(
            page.screenshot(),
            name='Screenshot on failure',
            attachment_type=allure.attachment_type.PNG,
        )
