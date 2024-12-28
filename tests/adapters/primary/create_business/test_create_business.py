import json
import pytest
from unittest.mock import MagicMock

from src.adapters.primary.create_business.index import handler


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


def test_create_business_validation_error(event, lambda_context):
    response = handler(event, lambda_context)

    assert response["statusCode"] == 400
