import pytest
import httpx
import allure
from pytest_httpserver import HTTPServer


@allure.feature("API Mocking")
@allure.story("Mock GET request")
@pytest.mark.api
@pytest.mark.smoke
def test_mock_get_post(httpserver: HTTPServer):
    httpserver.expect_request("/posts/1").respond_with_json({"id": 1, "title": "Mocked Post", "userId": 1})

    with allure.step("Send GET request to mock server"):
        response = httpx.get(httpserver.url_for("/posts/1"))

    with allure.step("Verify mocked response"):
        assert response.status_code == 200
        assert response.json()["title"] == "Mocked Post"


@allure.feature("API Mocking")
@allure.story("Mock server error")
@pytest.mark.api
@pytest.mark.regression
def test_mock_server_error(httpserver: HTTPServer):
    httpserver.expect_request("/posts/999").respond_with_data("Internal Server Error", status=500)

    with allure.step("Send GET request to mock server"):
        response = httpx.get(httpserver.url_for("/posts/999"))

    with allure.step("Verify error response handled"):
        assert response.status_code == 500
