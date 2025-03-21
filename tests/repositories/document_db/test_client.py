from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def pre_config(monkeypatch):
    monkeypatch.setenv("DOCUMENTDB_USERNAME", "fake-username")
    monkeypatch.setenv("DOCUMENTDB_SECRET_NAME", "fake-secret-name")
    monkeypatch.setenv("DOCUMENTDB_ENDPOINT", "fake-endpoint")
    monkeypatch.setenv("DOCUMENTDB_PORT", "27017")
    monkeypatch.setenv("DOCUMENTDB_DATABASE", "fake-database")


@patch("boto3.client")
def test_documentdb_config(mock_boto_client):
    from src.repositories.document_db.utils import get_documentdb_config

    mock_secrets_client = mock_boto_client.return_value
    mock_secrets_client.get_secret_value.return_value = {
        "SecretString": '{"username": "fake-username", "password": "test"}',
    }

    config = get_documentdb_config()

    assert config["username"] == "fake-username"
    assert config["password"] == "test"
    assert config["cluster_endpoint"] == "fake-endpoint"
    assert config["cluster_port"] == "27017"
    assert config["database_name"] == "fake-database"
    mock_secrets_client.get_secret_value.assert_called_once()


@patch("boto3.client")
def test_get_password_secret(mock_boto_client):
    from src.repositories.document_db.utils import get_user_password_secret

    mock_secrets_client = mock_boto_client.return_value
    mock_secrets_client.get_secret_value.return_value = {
        "SecretString": '{"username": "fake-username", "password": "test"}',
    }

    secret_value = get_user_password_secret("test-secret-key")
    assert secret_value["username"] == "fake-username"
    assert secret_value["password"] == "test"
    mock_secrets_client.get_secret_value.assert_called_once()
