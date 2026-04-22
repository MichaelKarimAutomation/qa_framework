import pytest
import os
from utils.api_client import APIClient


@pytest.fixture
def todo_url():
    return os.getenv("TODOMVC_URL")

@pytest.fixture
def api_client(scope="session"):
    client = APIClient()
    yield client
    client.close()
