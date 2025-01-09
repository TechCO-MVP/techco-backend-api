import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/user/list",
        "httpMethod": "GET",
        "headers": {"Authorization": "fake-access-token"},
        "queryStringParameters": {
            "business_id": "6778c3fa49a61649b054659d",
            "id": "6778c3fa49a61649b054659d",
        },
        "body": json.dumps({}),
    }


@pytest.fixture
def lambda_context():

    context = MagicMock
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.aws_request_id = "test-request-id"

    return context


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")


def test_get_user_value_error(event, lambda_context):
    """Test get user value error."""
    from src.adapters.primary.user.get_user.index import handler

    event["queryStringParameters"] = {}
    response = handler(event, lambda_context)

    assert response["statusCode"] == 400
    assert "Invalid query parameters" in json.loads(response["body"])["message"]


def test_get_user_validation_error(event, lambda_context):
    """Test get user validation error."""
    from src.adapters.primary.user.get_user.index import handler

    event["queryStringParameters"].pop("id")

    response = handler(event, lambda_context)
    assert response["statusCode"] == 400


def test_handler_general_exception(mocker, event, lambda_context):
    """Test handler for general exception."""
    from src.adapters.primary.user.get_user.index import handler

    mock_create_user_use_case = mocker.patch(
        "src.adapters.primary.user.get_user.index.get_user_use_case"
    )
    mock_create_user_use_case.side_effect = Exception("Unexpected error")
    response = handler(event, lambda_context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert body["message"] == "An error occurred: Unexpected error"


def test_get_user(mocker, event, lambda_context):
    """Test get user."""
    from src.adapters.primary.user.get_user.index import handler

    mock_create_user_use_case = mocker.patch(
        "src.adapters.primary.user.get_user.index.get_user_use_case"
    )
    mock_create_user_use_case.return_value = {"message": "User found successfully"}
    response = handler(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "User found successfully"
