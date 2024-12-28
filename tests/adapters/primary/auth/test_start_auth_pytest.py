"""Tests for the start_auth module."""

import json
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/auth/start_auth",
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"email": "email@test.co"}),
    }


@pytest.fixture
def lambda_context():
    context = MagicMock
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.aws_request_id = "test-request-id"

    return context


def test_start_auth_success(mocker, event, lambda_context):
    """Test start_auth success."""
    from src.adapters.primary.auth.start_auth import lambda_handler

    mocker.patch("src.adapters.primary.auth.start_auth.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.start_auth.CLIENT_ID", "fake-client-id")

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.start_auth.cognito_client")
    mock_cognito_client.initiate_auth.return_value = {"Session": "fake-session-token"}

    response = lambda_handler(event, lambda_context)
    mock_cognito_client.initiate_auth.assert_called_once_with(
        AuthFlow="CUSTOM_AUTH",
        AuthParameters={"USERNAME": "email@test.co"},
        ClientId="fake-client-id",
    )
    assert response["statusCode"] == 200


def test_lambda_handler_client_error(mocker, event, lambda_context):
    """Test start_auth client error."""
    from src.adapters.primary.auth.start_auth import lambda_handler

    mocker.patch("src.adapters.primary.auth.start_auth.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.start_auth.CLIENT_ID", "fake-client-id")

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.start_auth.cognito_client")
    error_response = {
        "Error": {"Code": "UserNotFoundException", "Message": "User does not exist"},
        "ResponseMetadata": {
            "RequestId": "string",
            "HostId": "string",
            "HTTPStatusCode": 400,
            "HTTPHeaders": {"header-name": "header-value"},
            "RetryAttempts": 0,
        },
    }
    mock_cognito_client.initiate_auth.side_effect = ClientError(error_response, "InitiateAuth")

    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "Failed to start authentication:" in body["error"]


def test_lambda_handler_unexpected_error(mocker, event, lambda_context):
    """Test start_auth unexpected error."""
    from src.adapters.primary.auth.start_auth import lambda_handler

    mocker.patch("src.adapters.primary.auth.start_auth.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.start_auth.CLIENT_ID", "fake-client-id")

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.start_auth.cognito_client")
    mock_cognito_client.initiate_auth.side_effect = Exception("Unexpected error")

    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Unexpected error" in body["error"]
