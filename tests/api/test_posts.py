import pytest
import allure
from data.factories import PostFactory, UserFactory


@allure.feature('API Tests')
@allure.story('Get Post')
@pytest.mark.api
@pytest.mark.smoke
def test_get_post(api_client):
    """Smoke check the JSONPlaceholder API: GET /posts/1 returns 200 and the body's `id` matches the requested id. Acts as the canary that the API base URL and api_client fixture are wired up correctly."""
    with allure.step('Send GET request for post 1'):
        response = api_client.get('/posts/1')
    with allure.step('Verify response status and id'):
        assert response.status_code == 200
        assert response.json()['id'] == 1


@allure.feature('API Tests')
@allure.story('Create Post')
@pytest.mark.api
@pytest.mark.regression
def test_create_post(api_client):
    """POST a hardcoded post payload to /posts and assert the API echoes back 201 plus the same title. Confirms the create-post happy path with a literal payload (no factory)."""
    with allure.step('Create POST request for posts'):
        payload = {'title': 'My Post', 'body': 'Hello world', 'userId': 1}
        response = api_client.post('/posts', payload)
    with allure.step('Verify response satus and title'):
        assert response.status_code == 201
        assert response.json()['title'] == 'My Post'


@allure.feature('API Tests')
@allure.story('Get Post with Factory')
@pytest.mark.api
@pytest.mark.regression
def test_create_post_with_factory(api_client):
    """Same create-post path as test_create_post, but the payload comes from PostFactory so the test runs against randomized realistic data. Catches schema or validation rules that only fail on certain inputs."""
    with allure.step('Create POST using Factory for posts'):
        payload = PostFactory()
        response = api_client.post('/posts', payload)
    with allure.step('Verify response satus and title'):
        assert response.status_code == 201
        assert response.json()['title'] == payload['title']


@allure.feature('API Tests')
@allure.story('Create User with Factory')
@pytest.mark.api
@pytest.mark.regression
def test_create_user_with_factory(api_client):
    """Generate a user payload from UserFactory, POST it to /users, and assert the email round-trips back unchanged. Exercises the user-create endpoint with factory-generated input."""
    with allure.step('Generate user data'):
        user = UserFactory()
    with allure.step('Send POST request'):
        response = api_client.post('/users', user)
    with allure.step('Verify response'):
        assert response.status_code == 201
        assert response.json()['email'] == user['email']


@allure.feature('API Tests')
@allure.story('Get Post')
@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize('post_id', [1, 2, 3])
def test_get_multiple_posts(api_client, post_id):
    """Parametrized smoke across posts 1, 2, and 3: each GET /posts/<id> returns 200 with a matching id in the body. Confirms GET-by-id works for more than just the canary post used in test_get_post."""
    with allure.step(f'Send GET request for post {post_id}'):
        response = api_client.get(f'/posts/{post_id}')
    with allure.step('Verify response'):
        assert response.status_code == 200
        assert response.json()['id'] == post_id
