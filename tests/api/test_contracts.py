import pytest
import allure
import jsonschema


POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
    },
    "additionalProperties": False,
}


@allure.feature("Contract Tests")
@allure.story("Get Post Schema")
@pytest.mark.api
@pytest.mark.regression
def test_get_post_schema(api_client):
    with allure.step("GET post 1"):
        response = api_client.get("/posts/1")
    with allure.step("Validate response schema"):
        jsonschema.validate(instance=response.json(), schema=POST_SCHEMA)

@allure.feature("Contract Tests")
@allure.story("Detect Schema Violation")
@pytest.mark.api
@pytest.mark.regression
def test_schema_violation_detected(api_client):
    wrong_schema = {
        "type": "object",
        "required": ["id", "title", "body", "userId", "email"],
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "body": {"type": "string"},
            "userId": {"type": "integer"},
            "email": {"type": "string"},
        },
    }

    with allure.step("GET post 1"):
        response = api_client.get("/posts/1")
    with allure.step("Verify schema violation is detected"):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=response.json(), schema=wrong_schema)
