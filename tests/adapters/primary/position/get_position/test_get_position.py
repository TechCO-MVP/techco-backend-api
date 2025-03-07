import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def event():
    """Fixture for the input event."""
    return {
        "path": "/position/list",
        "httpMethod": "GET",
        "headers": {"Authorization": "fake-access-token"},
        "queryStringParameters": {
            "business_id": "6778c3fa49a61649b054659d",
            "user_id": "6778c3fa49a61649b05465us",
            "id": "6778c3fa49a61649b054659d",
        },
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


def test_get_position_value_error(event, lambda_context):
    """Test get position value error."""
    from src.adapters.primary.position.get_position.index import handler

    event["queryStringParameters"] = {}
    response = handler(event, lambda_context)

    assert response["statusCode"] == 400
    assert "Invalid query parameters" in json.loads(response["body"])["message"]


def test_get_user_validation_error(event, lambda_context):
    """Test get user validation error."""
    from src.adapters.primary.position.get_position.index import handler

    event["queryStringParameters"].pop("id")

    response = handler(event, lambda_context)
    assert response["statusCode"] == 400


def test_handler_general_exception(mocker, event, lambda_context):
    """Test handler for general exception."""
    from src.adapters.primary.position.get_position.index import handler

    mock_create_user_use_case = mocker.patch(
        "src.adapters.primary.position.get_position.index.get_position_use_case"
    )
    mock_create_user_use_case.side_effect = Exception("Unexpected error")
    response = handler(event, lambda_context)
    print("************************", response)
    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert body["message"] == "An error occurred: Unexpected error"


def test_get_position(mocker, event, lambda_context):
    """Test get position."""
    from src.adapters.primary.position.get_position.index import handler
    from src.domain.position import PositionEntity
    from src.domain.base_entity import from_dto_to_entity

    mock_create_position_use_case = mocker.patch(
        "src.adapters.primary.position.get_position.index.get_position_use_case"
    )

    mock_position_case = [{
            "_id":"67cb2b29e1d7f34f0574b051",
            "business_id":"679077da2d6626a2b007f8f9",
            "owner_position_user_id":"6777862efe77308365432a36",
            "recruiter_user_id":"679077da2d6626a2b007f8fa",
            "role":"developer",
            "responsible_users":[{"user_id":"679077da2d6626a2b007f8fa","can_edit":True}],
            "seniority":"senior",
            "country_code":"CO",
            "city":"Bogota",
            "description":"backend senior bogota",
            "responsabilities":["coding","tests"],
            "skills":[{"name":"python","required":True}],
            "languages":[{"name":"ingles","level":"high"}],
            "hiring_priority":"high",
            "work_mode":"Remote",
            "created_at": "2021-10-10T10:10:10",
            "updated_at": "2021-10-10T10:10:10"
        }
    ]

    mock_create_position_use_case.return_value = mock_position_case
    response = handler(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Position found successfully"


def test_get_position_not_found(mocker, event, lambda_context):
    """Test get position."""
    from src.adapters.primary.position.get_position.index import handler
    from src.domain.position import PositionEntity
    from src.domain.base_entity import from_dto_to_entity

    mock_create_position_use_case = mocker.patch(
        "src.adapters.primary.position.get_position.index.get_position_use_case"
    )

    mock_create_position_use_case.return_value = []
    response = handler(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Position not found"
