import pytest
import allure
import jsonschema


POST_SCHEMA = {
    'type': 'object',
    'required': ['id', 'title', 'body', 'userId'],
    'properties': {
        'id': {'type': 'integer'},
        'title': {'type': 'string'},
        'body': {'type': 'string'},
        'userId': {'type': 'integer'},
    },
    'additionalProperties': False,
}


@allure.feature('Contract Tests')
@allure.story('Get Post Schema')
@pytest.mark.api
@pytest.mark.regression
def test_get_post_schema(api_client):
    """Contract test: GET /posts/1 must match POST_SCHEMA exactly (required keys present, types correct, no extra properties). Detects upstream API changes that would silently break clients."""
    with allure.step('GET post 1'):
        response = api_client.get('/posts/1')
    with allure.step('Validate response schema'):
        jsonschema.validate(instance=response.json(), schema=POST_SCHEMA)


@allure.feature('Contract Tests')
@allure.story('Detect Schema Violation')
@pytest.mark.api
@pytest.mark.regression
def test_schema_violation_detected(api_client):
    """Negative meta-test: validate the real GET /posts/1 response against a deliberately wrong schema (extra required `email` field) and confirm jsonschema raises ValidationError. Proves the schema validator is actually catching mismatches, not silently passing everything."""
    wrong_schema = {
        'type': 'object',
        'required': ['id', 'title', 'body', 'userId', 'email'],
        'properties': {
            'id': {'type': 'integer'},
            'title': {'type': 'string'},
            'body': {'type': 'string'},
            'userId': {'type': 'integer'},
            'email': {'type': 'string'},
        },
    }

    with allure.step('GET post 1'):
        response = api_client.get('/posts/1')
    with allure.step('Verify schema violation is detected'):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=response.json(), schema=wrong_schema)


USER_SCHEMA = {
    'type': 'object',
    'required': ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company'],
    'properties': {
        'id': {'type': 'integer'},
        'name': {'type': 'string'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'address': {'type': 'object'},
        'phone': {'type': 'string'},
        'website': {'type': 'string'},
        'company': {'type': 'object'},
    },
    'additionalProperties': False,
}

COMMENT_SCHEMA = {
    'type': 'object',
    'required': ['id', 'postId', 'name', 'email', 'body'],
    'properties': {
        'id': {'type': 'integer'},
        'postId': {'type': 'integer'},
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'body': {'type': 'string'},
    },
    'additionalProperties': False,
}

TODO_SCHEMA = {
    'type': 'object',
    'required': ['id', 'userId', 'title', 'completed'],
    'properties': {
        'id': {'type': 'integer'},
        'userId': {'type': 'integer'},
        'title': {'type': 'string'},
        'completed': {'type': 'boolean'},
    },
    'additionalProperties': False,
}

CONTRACTS = [
    ('/posts/1', POST_SCHEMA),
    ('/users/1', USER_SCHEMA),
    ('/comments/1', COMMENT_SCHEMA),
    ('/todos/1', TODO_SCHEMA),
]


@allure.feature('Contract Tests')
@allure.story('Response schema matches contract')
@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize('endpoint,schema', CONTRACTS, ids=[c[0] for c in CONTRACTS])
def test_response_matches_schema(api_client, endpoint, schema):
    """Parametrized contract sweep across /posts/1, /users/1, /comments/1, and /todos/1. Each endpoint's live response is validated against its declared schema so any drift in any of the four resources fails its own test case (rather than hiding behind a single combined check)."""
    with allure.step(f'GET {endpoint}'):
        response = api_client.get(endpoint)
    with allure.step('Validate response matches schema'):
        jsonschema.validate(instance=response.json(), schema=schema)
