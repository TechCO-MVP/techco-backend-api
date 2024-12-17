"""Tests for the start_auth module."""

import json
import pytest
from botocore.exceptions import ClientError
from src.adapters.primary.auth.start_auth import lambda_handler


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"email": "email@test.co"}),
    }


def test_start_auth_success(mocker, event):
    """Test start_auth success."""
    # Mock environment variables
    mocker.patch("src.adapters.primary.auth.start_auth.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.start_auth.CLIENT_ID", "fake-client-id")

    # Mock the Cognito client
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.start_auth.cognito_client")
    mock_cognito_client.initiate_auth.return_value = {"Session": "fake-session-token"}

    response = lambda_handler(event, {})

    mock_cognito_client.initiate_auth.assert_called_once_with(
        AuthFlow="CUSTOM_AUTH",
        AuthParameters={"USERNAME": "email@test.co"},
        ClientId="fake-client-id",
    )
    assert response["statusCode"] == 200


def test_lambda_handler_client_error(mocker, event):
    """Test start_auth client error."""
    # Mock environment variables
    mocker.patch("src.adapters.primary.auth.start_auth.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.start_auth.CLIENT_ID", "fake-client-id")

    # Mock the Cognito client
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

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "Failed to start authentication:" in body["error"]


def test_lambda_handler_unexpected_error(mocker, event):
    """Test start_auth unexpected error."""
    # Mock environment variables
    mocker.patch("src.adapters.primary.auth.start_auth.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.start_auth.CLIENT_ID", "fake-client-id")

    # Mock the Cognito client
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.start_auth.cognito_client")
    mock_cognito_client.initiate_auth.side_effect = Exception("Unexpected error")

    response = lambda_handler(event, {})

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Unexpected error" in body["error"]
