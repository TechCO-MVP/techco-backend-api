import pytest
from unittest.mock import patch


@pytest.fixture()
def pre_config(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "us-east-1")
    monkeypatch.setenv("COGNITO_USER_POOL_CLIENT_ID", "fake-client-id")


@patch("src.adapters.primary.auth.create_auth_challenge.generate_secret_code")
@patch("boto3.client")
def test_handler(mock_boto_cient, generate_secret_code_mock, pre_config):
    from src.adapters.primary.auth.create_auth_challenge import handler

    generate_secret_code_mock.return_value = "123456"
    mock_ses_client = mock_boto_cient.return_value

    event = {
        "request": {"userAttributes": {"username": "username", "email": "email"}},
        "response": {},
    }

    response = handler(event, {})

    assert "publicChallengeParameters" in response["response"]
    assert "privateChallengeParameters" in response["response"]
    assert "challengeMetadata" in response["response"]
    assert response["response"]["challengeMetadata"] == "CODE-123456"
    mock_ses_client.send_email.assert_called_once()


def test_generate_secret_code(pre_config):
    from src.adapters.primary.auth.create_auth_challenge import generate_secret_code

    secret_code = generate_secret_code()

    assert len(secret_code) == 6
    assert secret_code.isdigit()


@patch("boto3.client")
def test_send_otp_email(mock_boto_client, pre_config):
    from src.adapters.primary.auth.create_auth_challenge import send_otp_email

    email = "test@gmail.com"
    secret_code = "123456"
    mock_ses_client = mock_boto_client.return_value

    send_otp_email(email, secret_code)

    mock_boto_client.assert_called_once()
    mock_ses_client.send_email.assert_called_once()
