import pytest
from unittest.mock import MagicMock
from src.use_cases.user.update_user_data import put_user_data_use_case
from src.domain.user import UserEntity
from src.domain.base_entity import from_dto_to_entity

@pytest.fixture
def user_dto():
    from src.domain.user import UserDTO
    return UserDTO(
        full_name="John Doe",
        email="john.doe@example.com",
        company_position="Developer",
        role="Admin",
        business_id="6778c3fa49a61649b054659d",
        roles=[{"role": "business_admin", "business_id": "6778c3fa49a61649b054659d"}],
    )


@pytest.fixture
def user_entity(user_dto):
    from src.domain.user import UserEntity
    return UserEntity(props=user_dto)


@pytest.fixture
def mock_user_repository(mocker):
    mock_repository = mocker.patch("src.use_cases.user.update_user_data.UserRepository")
    return mock_repository


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")


def test_put_user_data_use_case_success(mock_user_repository, caplog):
    """Test get user success."""
    from src.use_cases.user.update_user_data import put_user_data_use_case
    from src.domain.user import UserEntity
    from src.domain.base_entity import from_dto_to_entity
    
    response_user_entity = from_dto_to_entity(UserEntity,{
        "full_name":"John Doe",
        "email":"john.doe@example.com",
        "company_position":"Developer",
        "business_id":"6778c3fa49a61649b054659d",
        "roles":[{"role": "super_admin", "business_id": "6778c3fa49a61649b054659d"}],
        "_id": "6778c3fa49a61649b054867834ad",
        "status": "pending",
        "created_at":"2021-10-10T00:00:00",
        "updated_at":"2021-10-10T00:00:00",
        "deleted_at":None,
    }
    )
    mock_user_repository.return_value.getByEmail.return_value = response_user_entity
    user_data = {"user_id":"6778c3fa49a61649b054867834ad", "user_full_name": "pepito perez", "business_id": "6778c3fa49a61649b054659d", "user_role": "recruiter", "user_email": "kake_@mail.com"}
    with caplog.at_level("INFO"):
        put_user_data_use_case(user_data)

    assert any("Updating user data" in message for message in caplog.messages)
    assert any("full_name='pepito perez'" in message for message in caplog.messages)
    assert any("role=<Role.RECRUITER: 'recruiter'" in message for message in caplog.messages)
    
    mock_user_repository.return_value.update.return_value = response_user_entity

    response = put_user_data_use_case(user_data)
    assert response == response_user_entity