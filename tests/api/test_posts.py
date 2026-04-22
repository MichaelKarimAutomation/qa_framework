import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_get_post(api_client):
    response = api_client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.api
@pytest.mark.regression
def test_create_post(api_client):
    payload = {"title": "My Post", "body": "Hello world", "userId": 1}
    response = api_client.post("/posts", payload)
    assert response.status_code == 201
    assert response.json()["title"] == "My Post"
