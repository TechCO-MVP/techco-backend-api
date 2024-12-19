"""Tests for the finish session module."""

import json
import pytest
from src.adapters.primary.auth.sign_out import lambda_handler


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "httpMethod": "POST",
        "headers": {"Authorization": "Bearer fake-access-token"},
    }


def test_finish_session_success(mocker, event):
    """Test successful user signout."""
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.sign_out.cognito_client")
    mock_cognito_client.global_sign_out.return_value = {}

    response = lambda_handler(event, {})

    mock_cognito_client.global_sign_out.assert_called_once_with(
        AccessToken="fake-access-token"
    )
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["message"] == "User successfully signed out."


def test_finish_session_unauthorized_missing_header(mocker):
    """Test missing Authorization header."""
    event = {"httpMethod": "POST", "headers": {}}
    response = lambda_handler(event, {})

    assert response["statusCode"] == 401
    assert json.loads(response["body"])["message"] == "Unauthorized: Missing or invalid Authorization header"


def test_finish_session_unauthorized_invalid_header(mocker):
    """Test invalid Authorization header."""
    event = {"httpMethod": "POST", "headers": {"Authorization": "InvalidHeader"}}
    response = lambda_handler(event, {})

    assert response["statusCode"] == 401
    assert json.loads(response["body"])["message"] == "Unauthorized: Missing or invalid Authorization header"


def test_finish_session_not_authorized_exception(mocker, event):
    """Test Cognito NotAuthorizedException."""
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.sign_out.cognito_client")

    class NotAuthorizedException(Exception):
        pass

    mock_cognito_client.exceptions = mocker.Mock(NotAuthorizedException=NotAuthorizedException)
    mock_cognito_client.global_sign_out.side_effect = NotAuthorizedException

    response = lambda_handler(event, {})

    assert response["statusCode"] == 401
    assert json.loads(response["body"])["message"] == "Unauthorized: Invalid or expired token."
