import pytest
import allure
from data.factories import PostFactory


@allure.feature("API Tests")
@allure.story("Get Post")
@pytest.mark.api
@pytest.mark.smoke
def test_get_post(api_client):
    with allure.step("Send GET request for post 1"):
        response = api_client.get("/posts/1")
    with allure.step("Verify response status and id"):
        assert response.status_code == 200
        assert response.json()["id"] == 1


@allure.feature("API Tests")
@allure.story("Create Post")
@pytest.mark.api
@pytest.mark.regression
def test_create_post(api_client):
    with allure.step("Create POST request for posts"):
        payload = {"title": "My Post", "body": "Hello world", "userId": 1}
        response = api_client.post("/posts", payload)
    with allure.step("Verify response satus and title"):
        assert response.status_code == 201
        assert response.json()["title"] == "My Post"


@allure.feature("API Tests")
@allure.story("Get Post with Factory")
@pytest.mark.api
@pytest.mark.smoke
def test_create_post_with_factory(api_client):
    with allure.step("Create POST using Factory for posts"):
        payload = PostFactory()
        response = api_client.post("/posts", payload)
    with allure.step("Verify response satus and title"):
        assert response.status_code == 201
        assert response.json()["title"] == payload["title"]
