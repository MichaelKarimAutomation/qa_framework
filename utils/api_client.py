import httpx
import os
import allure


class APIClient:
    """Thin httpx wrapper that prepends a configurable base URL to every request and auto-attaches request/response bodies to the Allure report for debugging."""

    def __init__(self) -> None:
        """Resolve the API base URL from the JSONPLACEHOLDER_URL env var and open a single httpx Client whose connection pool will be reused across all calls."""
        self.base_url = os.getenv('JSONPLACEHOLDER_URL')
        self.client = httpx.Client()

    def get(self, endpoint: str) -> httpx.Response:
        """Send a GET to base_url + endpoint, attach the JSON body to the active Allure step, and return the raw response."""
        response = self.client.get(f'{self.base_url}{endpoint}')
        allure.attach(
            str(response.json()),
            name=f'GET {endpoint}',
            attachment_type=allure.attachment_type.TEXT,
        )
        return response

    def post(self, endpoint: str, payload: dict) -> httpx.Response:
        """Send a JSON POST to base_url + endpoint, attach both the outgoing payload and the response body to Allure (as separate attachments), and return the raw response."""
        response = self.client.post(f'{self.base_url}{endpoint}', json=payload)
        allure.attach(
            str(payload),
            name=f'POST {endpoint} - Request',
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            str(response.json()),
            name=f'POST {endpoint} - Response',
            attachment_type=allure.attachment_type.TEXT,
        )
        return response

    def close(self) -> None:
        """Release the underlying httpx Client's connection pool. Call this once at the end of the test session (the `api_client` fixture handles this automatically)."""
        self.client.close()
