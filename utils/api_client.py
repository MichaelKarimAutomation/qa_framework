import httpx
import os
import allure


class APIClient:
    
    def __init__(self) -> None:
        self.base_url = os.getenv("JSONPLACEHOLDER_URL")
        self.client = httpx.Client()

    def get(self, endpoint: str) -> httpx.Response:
        response = self.client.get(f"{self.base_url}{endpoint}")
        allure.attach(str(response.json()), name=f"GET {endpoint}", attachment_type=allure.attachment_type.TEXT)
        return response

    def post(self, endpoint:str, payload: dict) -> httpx.Response:
        response = self.client.post(f"{self.base_url}{endpoint}", json=payload)
        allure.attach(str(payload), name=f"POST {endpoint} - Request", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(response.json()), name=f"POST {endpoint} - Response", attachment_type=allure.attachment_type.TEXT)
        return response
    
    def close(self) -> None:
        self.client.close()
        