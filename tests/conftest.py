import pytest
import os


@pytest.fixture
def todo_url():
    return os.getenv("TODOMVC_URL")
