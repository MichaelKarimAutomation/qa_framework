import httpx
import os


class APIClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("JSONPLACEHOLDER_URL")
        self.client = httpx.Client()

    def get(self, endpoint: str) -> httpx.Response:
        return self.client.get(f"{self.base_url}{endpoint}")

    def post(self, endpoint:str, payload: dict) -> httpx.Response:
        return self.client.post(f"{self.base_url}{endpoint}", json=payload)
    
    def close(self) -> None:
        self.client.close()
        