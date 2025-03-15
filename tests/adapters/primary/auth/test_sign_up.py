import json
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/auth/signup",
        "httpMethod": "POST",
        "body": json.dumps({"email": "email@test.com", "name": "test"}),
    }


@pytest.fixture
def lambda_context():
    context = MagicMock
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.aws_request_id = "test-request-id"

    return context


@patch("boto3.client")
def test_sign_up_user_sign_up_failed(mock_boto_client, event, lambda_context):
    from src.adapters.primary.auth.sign_up import handler

    mock_cognito_client = mock_boto_client.return_value
    mock_cognito_client.sign_up.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}

    response = handler(event, lambda_context)
    print(json.loads(response["body"]))
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["message"] == "User sign up failed"


def test_create_random_password():
    from src.adapters.primary.auth.sign_up import create_random_password

    password = create_random_password()
    assert len(password) == 8
