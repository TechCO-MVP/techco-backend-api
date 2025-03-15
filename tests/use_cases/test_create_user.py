import pytest

from src.domain.user import UserDTO, UserEntity


@pytest.fixture
def user_dto():
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
    return UserEntity(props=user_dto)


@pytest.fixture
def mock_user_repository(mocker):
    mock_repository = mocker.patch("src.use_cases.user.create_user.UserRepository")
    return mock_repository


@pytest.fixture
def mock_business_repository(mocker):
    mock_repository = mocker.patch("src.use_cases.user.create_user.BusinessRepository")
    return mock_repository


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")


def test_create_user_use_case_success(mock_user_repository, mock_business_repository, user_dto):
    """Test successful creation of a user."""
    from src.use_cases.user.create_user import create_user_use_case

    mock_business_repository.return_value.create.return_value = {
        "message": "Business created successfully",
        "body": {"business": {"_id": "6778c3fa49a61649b054659d"}},
    }

    mock_user_repository.return_value.create.return_value = {
        "message": "User created successfully",
        "body": {"user": {"_id": "6778c3fa49a61649b054659d"}},
    }

    response = create_user_use_case(user_dto, "6778c3fa49a61649b054659d")

    assert response["message"] == "User created successfully"
    assert response["body"]["user"]["_id"] == "6778c3fa49a61649b054659d"
