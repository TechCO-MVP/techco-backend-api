import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/business/create",
        "httpMethod": "POST",
        "headers": {"Authorization": "fake-access-token"},
        "body": json.dumps({}),
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


def test_create_business_value_error(event, lambda_context):
    from src.adapters.primary.business.create_business.index import handler

    response = handler(event, lambda_context)

    assert response["statusCode"] == 400


def test_create_business_validation_error(event, lambda_context):
    from src.adapters.primary.business.create_business.index import handler

    event["body"] = json.dumps({"name": "test"})

    response = handler(event, lambda_context)

    assert response["statusCode"] == 400
