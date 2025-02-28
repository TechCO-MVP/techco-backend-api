import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def event():
    """Fixture for the input event."""
    return json.dumps(
        {
            "_id": "67aa9fe5e45a8924426e2ffa",
            "created_at": "2025-02-11T00:55:01.488274",
            "updated_at": "2025-02-11T00:55:01.488284",
            "deleted_at": None,
            "status": "in_progress",
            "execution_arn": None,
            "user_id": "6791f6f8886eb975df789f6a",
            "position_id": "yyy",
            "business_id": "679077da2d6626a2b007f8f9",
            "process_filters": {
                "role": "Software Engineer",
                "seniority": "Senior",
                "country_code": "USA",
                "city": "San Francisco",
                "description": "Experienced software engineer with expertise in Python and cloud technologies.",
                "responsabilities": [
                    "Design and develop scalable and maintainable software solutions.",
                    "Collaborate with cross-functional teams to deliver high-quality products.",
                    "Participate in code reviews and provide constructive feedback.",
                ],
                "skills": [
                    {"name": "Python", "required": True},
                    {"name": "AWS", "required": True},
                    {"name": "Docker", "required": True},
                    {"name": "Kubernetes", "required": False},
                    {"name": "Agile Methodologies", "required": False},
                ],
                "business_id": "xxx",
                "position_id": "yyy",
                # "snapshot_id": "snap_m715tx5812bbjy69ar" # 100 registros
                "snapshot_id": "snap_m7cl5a21218si2ws8o",  # 2 registrops
            },
            "profiles": [
                {
                    "timestamp": "10-10-2024",
                    "linkedin_num_id": "linkedin_num_id",
                    "email": "",
                },
                {
                    "timestamp": "10-10-2024",
                    "linkedin_num_id": "linkedin_num_id",
                    "email": "",
                },
            ],
        }
    )


@pytest.fixture
def lambda_context():

    context = MagicMock
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = (
        "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    )
    context.aws_request_id = "test-request-id"

    return context


# @pytest.fixture(autouse=True)
# def set_env(monkeypatch):
#     monkeypatch.setenv("REGION_NAME", "fake-region")
#     monkeypatch.setenv("CLIENT_ID", "fake-client-id")


# @pytest.fixture
# def mock_role_required(mocker):
#     """Mock del decorador role_required."""
#     return mocker.patch(
#         "src.utils.authorization.role_required",
#         side_effect=lambda app, roles: lambda func: func,
#     )


def test_error(event, lambda_context):
    """Test error."""
    from src.adapters.primary.profile.filter.add_link_vacancy_form import lambda_handler

    event = {}
    response = lambda_handler(event, lambda_context)
    assert response["status"] == "Error"


def test_add_link(mocker, event, lambda_context):
    """Test get user."""
    from src.adapters.primary.profile.filter.add_link_vacancy_form import lambda_handler
    from src.domain.base_entity import from_dto_to_entity
    from src.domain.profile import ProfileFilterProcessEntity
    from src.use_cases.profile.add_unique_link_vacancy_form import (
        add_unique_link_vacancy_form,
    )

    mock_add_unique_link_vacancy_form = mocker.patch(
        "src.adapters.primary.profile.filter.add_link_vacancy_form.add_unique_link_vacancy_form"
    )

    mock_entity = from_dto_to_entity(
        ProfileFilterProcessEntity,
        {
            "_id": "67aa9fe5e45a8924426e2ffa",
            "created_at": "2025-02-11T00:55:01.488274",
            "updated_at": "2025-02-11T00:55:01.488284",
            "deleted_at": None,
            "status": "in_progress",
            "execution_arn": None,
            "user_id": "6791f6f8886eb975df789f6a",
            "position_id": "yyy",
            "business_id": "679077da2d6626a2b007f8f9",
            "process_filters": {
                "role": "Software Engineer",
                "seniority": "Senior",
                "country_code": "USA",
                "city": "San Francisco",
                "description": "Experienced software engineer with expertise in Python and cloud technologies.",
                "responsabilities": [
                    "Design and develop scalable and maintainable software solutions.",
                    "Collaborate with cross-functional teams to deliver high-quality products.",
                    "Participate in code reviews and provide constructive feedback.",
                ],
                "skills": [
                    {"name": "Python", "required": True},
                    {"name": "AWS", "required": True},
                    {"name": "Docker", "required": True},
                    {"name": "Kubernetes", "required": False},
                    {"name": "Agile Methodologies", "required": False},
                ],
                "business_id": "xxx",
                "position_id": "yyy",
                # "snapshot_id": "snap_m715tx5812bbjy69ar" # 100 registros
                "snapshot_id": "snap_m7cl5a21218si2ws8o",  # 2 registrops
            },
            "profiles": [
                {
                    "timestamp": "10-10-2024",
                    "linkedin_num_id": "linkedin_num_id",
                    "email": "",
                },
                {
                    "timestamp": "10-10-2024",
                    "linkedin_num_id": "linkedin_num_id",
                    "email": "",
                },
            ],
        },
    )
    mock_add_unique_link_vacancy_form.return_value = mock_entity
    response = lambda_handler(event, lambda_context).to_dto()

    assert response["props"]["profiles"][0]["link_vacancy_form"] is None
