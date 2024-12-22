"""Tests for the finish session module."""

import json
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/auth/signout",
        "httpMethod": "POST",
        "headers": {"Authorization": "fake-access-token"},
    }


@pytest.fixture
def lambda_context():
    context = MagicMock
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.aws_request_id = "test-request-id"

    return context


def test_finish_session_success(mocker, event, lambda_context):
    """Test successful user signout."""
    from src.adapters.primary.auth.sign_out import lambda_handler

    mocker.patch("src.adapters.primary.auth.sign_out.REGION_NAME", "fake-region")
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.sign_out.cognito_client")
    mock_cognito_client.global_sign_out.return_value = {}

    response = lambda_handler(event, lambda_context)

    mock_cognito_client.global_sign_out.assert_called_once_with(AccessToken="fake-access-token")
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["message"] == "User successfully signed out."


def test_finish_session_unauthorized_missing_header(mocker, lambda_context):
    """Test missing Authorization header."""
    from src.adapters.primary.auth.sign_out import lambda_handler

    mocker.patch("src.adapters.primary.auth.sign_out.REGION_NAME", "fake-region")
    event = {"path": "/auth/signout", "httpMethod": "POST", "headers": {}}
    response = lambda_handler(event, lambda_context)
    print("----------------------", response)

    assert response["statusCode"] == 500
    assert json.loads(response["body"])["message"] == "An error occurred"


def test_finish_session_unauthorized_invalid_header(mocker, lambda_context):
    """Test invalid Authorization header."""
    from src.adapters.primary.auth.sign_out import lambda_handler

    mocker.patch("src.adapters.primary.auth.sign_out.REGION_NAME", "fake-region")
    event = {
        "path": "/auth/signout",
        "httpMethod": "POST",
        "headers": {"Authorization": "InvalidHeader"},
    }
    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 401
    assert json.loads(response["body"])["message"] == "Unauthorized: Invalid or expired token."


def test_finish_session_not_authorized_exception(mocker, event, lambda_context):
    """Test Cognito NotAuthorizedException."""
    from src.adapters.primary.auth.sign_out import lambda_handler

    mocker.patch("src.adapters.primary.auth.sign_out.REGION_NAME", "fake-region")
    mock_cognito_client = mocker.patch("src.adapters.primary.auth.sign_out.cognito_client")

    class NotAuthorizedException(Exception):
        pass

    mock_cognito_client.exceptions = mocker.Mock(NotAuthorizedException=NotAuthorizedException)
    mock_cognito_client.global_sign_out.side_effect = NotAuthorizedException

    response = lambda_handler(event, lambda_context)

    assert response["statusCode"] == 401
    assert json.loads(response["body"])["message"] == "Unauthorized: Invalid or expired token."
