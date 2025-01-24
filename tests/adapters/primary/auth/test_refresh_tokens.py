"""Tests for the refresh_toekns module."""

import json
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/auth/refresh_tokens",
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"refresh_token": "fake_refresh_token"}),
    }


@pytest.fixture
def lambda_context():
    context = MagicMock
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.aws_request_id = "test-request-id"

    return context


def test_refresh_tokens_success(mocker, event, lambda_context):
    """Test refresh_tokens success."""
    from src.adapters.primary.auth.post_refresh_token import lambda_handler

    mocker.patch("src.adapters.primary.auth.post_refresh_token.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.post_refresh_token.CLIENT_ID", "fake-client-id")

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.post_refresh_token.cognito_client")
    mock_cognito_client.initiate_auth.return_value = {
        "id_token": "fake-id-token",
        "access_token": "fake-access-token",
        "expires_in": "36000"
    }

    response = lambda_handler(event, lambda_context)
    mock_cognito_client.initiate_auth.assert_called_once_with(
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": "fake_refresh_token"},
        ClientId="fake-client-id",
    )
    assert response["statusCode"] == 200


def test_lambda_handler_client_error(mocker, event, lambda_context):
    """Test refresh token client error."""
    from src.adapters.primary.auth.post_refresh_token import lambda_handler

    mocker.patch("src.adapters.primary.auth.post_refresh_token.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.post_refresh_token.CLIENT_ID", "fake-client-id")

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.post_refresh_token.cognito_client")
    error_response = {
        "Error": {"Code": "refreshTokenExpired", "Message": "Refresh token expired"},
        "ResponseMetadata": {
            "RequestId": "string",
            "HostId": "string",
            "HTTPStatusCode": 500,
            "HTTPHeaders": {"header-name": "header-value"},
            "RetryAttempts": 0,
        },
    }
    mock_cognito_client.initiate_auth.side_effect = ClientError(error_response, "InitiateAuth")

    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Refresh token expired" in body["message"]
