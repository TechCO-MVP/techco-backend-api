import datetime
import os
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock
from src.use_cases.profile.add_unique_link_vacancy_form import add_unique_link_vacancy_form, add_links_form, encript_data
from src.domain.profile_brightdata import ProfileBrightDataDTO
from src.domain.profile import ProfileFilterProcessEntity, ProfileFilterProcessQueryDTO
from src.domain.base_entity import from_dto_to_entity

@pytest.fixture
def mock_profile():
    return ProfileBrightDataDTO(
        timestamp="10-10-2024",
        linkedin_num_id="12345",
        name="John Doe",
        title="Software Engineer",
        location="New York",
        # skills=["Python", "Django"],
        # experience=["Company A", "Company B"],
        # education=["University X"],
        link_vacancy_form="form_link"
    )

@pytest.fixture
def mock_event():
    DTO = {
        "_id": "67aa9fe5e45a8924426e2ffa",
        "created_at": "2025-02-11T00:55:01.488274",
        "updated_at": "2025-02-11T00:55:01.488284",
        "deleted_at": None,
        "status": "pending",
        "execution_arn": None,
        "user_id": "6791f6f8886eb975df789f6a",
        "position_id": "yyy",
        "business_id": "xxx",
        "process_filters": {
            "role": "Software Engineer",
            "seniority": "Senior",
            "country_code": "USA",
            "city": "San Francisco",
            "description": "Experienced software engineer with expertise in Python and cloud technologies.",
            "responsabilities": [
            "Design and develop scalable and maintainable software solutions.",
            "Collaborate with cross-functional teams to deliver high-quality products.",
            "Participate in code reviews and provide constructive feedback."
            ],
            "skills": [
            {
                "name": "Python",
                "required": True
            },
            {
                "name": "AWS",
                "required": True
            },
            {
                "name": "Docker",
                "required": True
            },
            {
                "name": "Kubernetes",
                "required": False
            },
            {
                "name": "Agile Methodologies",
                "required": False
            }
            ],
            "business_id": "xxx",
            "position_id": "yyy",
            "snapshot_id": ""
        },
        "profiles": [{
            "timestamp": "10-10-2024",
            "linkedin_num_id": "linkedin_num_id",
        }]
    }

    return from_dto_to_entity(ProfileFilterProcessEntity, DTO)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("PROFILE_FILTER_PROCESS_ARN", "fake-arn")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")


@patch("src.use_cases.profile.add_unique_link_vacancy_form.ProfileFilterProcessDocumentDBAdapter")
@patch("src.use_cases.profile.add_unique_link_vacancy_form.encript_data")
def test_add_unique_link_vacancy_form(mock_encript_data, MockProfileFilterProcessDocumentDBAdapter, mock_event):
    mock_encript_data.return_value = "mock_token"
    mock_repo_instance = MockProfileFilterProcessDocumentDBAdapter.return_value
    mock_repo_instance.update.return_value = mock_event

    response = add_unique_link_vacancy_form(mock_event)
    
    assert response["profiles"][0]["link_vacancy_form"] == "https://www.evoly.ofertas/Software_Engineer?token=mock_token"
    mock_repo_instance.update.assert_called_once_with(mock_event.id, mock_event)
    mock_encript_data.assert_called_once()


@patch("src.use_cases.profile.add_unique_link_vacancy_form.jwt.encode")
def test_encript_data(mock_jwt_encode, mock_profile, mock_event):
    mock_jwt_encode.return_value = "mock_token"
    token = encript_data(mock_profile, mock_event)
    assert token == "mock_token"
    mock_jwt_encode.assert_called_once_with(
        {
            "id": mock_event.id,
            "business_id": mock_event.props.business_id,
            "linkedin_id": mock_profile.linkedin_num_id,
            "created_at": mock.ANY,
            "exp": mock.ANY
        },
        os.getenv("PROFILE_FILTER_PROCESS_ARN"),
        algorithm="HS256"
    )