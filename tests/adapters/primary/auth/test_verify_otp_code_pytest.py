"""Tests for the verify_auth_otp_code module."""

import json
import pytest
from botocore.exceptions import ClientError


@pytest.fixture
def event():
    return {
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {"email": "email@test.co", "otp": "123456", "session": "fake-session"}
        ),
    }

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")

def test_verify_auth_otp_code_success(mocker, event):
    """Test verify_auth_otp_code success."""
    from src.adapters.primary.auth.verify_auth_otp_code import lambda_handler

    mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.CLIENT_ID", "fake-client-id")

    # Mock the Cognito client
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.cognito_client")
    mock_cognito_client.respond_to_auth_challenge.return_value = {
        "AuthenticationResult": {
            "IdToken": "fake-id-token",
            "AccessToken": "fake_access_token",
            "RefreshToken": "fake_refresh_token",
        }
    }

    response = lambda_handler(event, {})

    mock_cognito_client.respond_to_auth_challenge.assert_called_once_with(
        ClientId="fake-client-id",
        ChallengeName="CUSTOM_CHALLENGE",
        ChallengeResponses={"USERNAME": "email@test.co", "ANSWER": "123456"},
        Session="fake-session",
    )
    assert response["statusCode"] == 200
    assert response["body"] == json.dumps(
        {
            "message": "Successfully authenticated.",
            "idToken": "fake-id-token",
            "accessToken": "fake_access_token",
            "refreshToken": "fake_refresh_token",
        }
    )

def test_verify_auth_otp_code_failed(mocker, event):
    """Test verify_auth_otp_code failed."""
    from src.adapters.primary.auth.verify_auth_otp_code import lambda_handler

    mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.REGION_NAME", "fake-region")
    mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.CLIENT_ID", "fake-client-id")

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.cognito_client")
    mock_cognito_client.respond_to_auth_challenge.return_value = {"Error": "error response"}

    response = lambda_handler(event, {})

    mock_cognito_client.respond_to_auth_challenge.assert_called_once_with(
        ClientId="fake-client-id",
        ChallengeName="CUSTOM_CHALLENGE",
        ChallengeResponses={"USERNAME": "email@test.co", "ANSWER": "123456"},
        Session="fake-session",
    )
    assert response["statusCode"] == 400
    assert response["body"] == json.dumps({"message": "Invalid OTP code."})

def test_lambda_handler_client_error(mocker, event):
    """Test verify_auth_otp_code client error."""
    from src.adapters.primary.auth.verify_auth_otp_code import lambda_handler

    mock_cognito_client = mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.cognito_client")
    error_response = {"Error": {"Message": "User does not exist"}}
    mock_cognito_client.respond_to_auth_challenge.side_effect = ClientError(
        error_response, "InitiateAuth"
    )

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "Error validating OTP code:" in body["error"]

def test_lambda_handler_unexpected_error(mocker, event):
    """Test verify_auth_otp_code unexpected error."""
    from src.adapters.primary.auth.verify_auth_otp_code import lambda_handler
    
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.verify_auth_otp_code.cognito_client")
    mock_cognito_client.respond_to_auth_challenge.side_effect = Exception("Unexpected error")

    response = lambda_handler(event, {})

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Unexpected error" in body["error"]