import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/user/create",
        "httpMethod": "POST",
        "headers": {"Authorization": "fake-access-token"},
        "body": json.dumps(
            {
                "business": "company name",
                "business_id": "12354",
                "full_name": "completed name",
                "email": "fakemail@mail.com",
                "company_position": "admin",
                "role": "business_admin",
            }
        ),
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


def test_create_user_value_error(mocker, event, lambda_context):
    """Test create user value error."""
    from src.adapters.primary.user.create_user.index import handler
    
    mocker.patch(
        "src.adapters.primary.user.create_user.index.role_required",
        return_value=lambda func: func  # Devuelve una función que simplemente devuelve la función original
    )

    event["body"] = json.dumps(
        {
            "roles": "admindeveloper",
            "business_id": "12354",
        }
    )
    response = handler(event, lambda_context)

    assert response["statusCode"] == 400
    assert json.loads(response["body"])["message"] == "Invalid role: None"


def test_create_user_validation_error(event, lambda_context):
    """Test create user validation error."""
    from src.adapters.primary.user.create_user.index import handler

    body = json.loads(event["body"])
    body["full_name"] = "name_with special_characters"
    event["body"] = json.dumps(body)

    response = handler(event, lambda_context)

    assert response["statusCode"] == 422


def test_handler_general_exception(mocker, event, lambda_context):
    """Test handler for general exception."""
    from src.adapters.primary.user.create_user.index import handler

    mock_create_user_use_case = mocker.patch(
        "src.adapters.primary.user.create_user.index.create_user_use_case"
    )
    mock_create_user_use_case.side_effect = Exception("Unexpected error")
    response = handler(event, lambda_context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert body["message"] == "An error occurred: Unexpected error"


def test_create_user(mocker, event, lambda_context):
    """Test create user."""
    from src.adapters.primary.user.create_user.index import handler

    mock_create_user_use_case = mocker.patch(
        "src.adapters.primary.user.create_user.index.create_user_use_case"
    )
    mock_create_user_use_case.return_value = {"message": "User created successfully"}
    response = handler(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "User created successfully"
