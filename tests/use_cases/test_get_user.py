import pytest



@pytest.fixture
def user_dto():
    from src.domain.user import UserDTO, UserEntity
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
    from src.domain.user import UserDTO, UserEntity
    return UserEntity(props=user_dto)


@pytest.fixture
def mock_user_repository(mocker):
    mock_repository = mocker.patch("src.use_cases.user.get_user.UserRepository")
    return mock_repository


# @pytest.fixture
# def mock_business_repository(mocker):
#     mock_repository = mocker.patch("src.use_cases.user.create_user.BusinessRepository")
#     return mock_repository


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")


def test_get_user_use_case_success(mock_user_repository):
    """Test get user success."""
    from src.use_cases.user.get_user import get_user_use_case
    from src.domain.user import UserEntity
    from src.domain.base_entity import from_dto_to_entity
    
    response_user_entity = from_dto_to_entity(UserEntity,{
        "full_name":"John Doe",
        "email":"john.doe@example.com",
        "company_position":"Developer",
        "business_id":"6778c3fa49a61649b054659d",
        "roles":[{"role": "recruiter", "business_id": "6778c3fa49a61649b054659d"}],
        "_id": "6778c3fa49a61649b054867834ad",
        "status": "pending",
        "created_at":"2021-10-10T00:00:00",
        "updated_at":"2021-10-10T00:00:00",
        "deleted_at":None,
    }
    )
    mock_user_repository.return_value.getById.return_value = response_user_entity

    response = get_user_use_case({"id": "6778c3fa49a61649b054659d"})

    assert response == response_user_entity


def test_get_all_user_use_case_success(mock_user_repository):
    """Test get all user success."""
    from src.use_cases.user.get_user import get_user_use_case
    from src.domain.user import UserEntity
    from src.domain.base_entity import from_dto_to_entity
    
    response_user_entity = [from_dto_to_entity(UserEntity,{
        "full_name":"John Doe",
        "email":"john.doe@example.com",
        "company_position":"Developer",
        "business_id":"6778c3fa49a61649b054659d",
        "roles":[{"role": "recruiter", "business_id": "6778c3fa49a61649b054659d"}],
        "_id": "6778c3fa49a61649b054867834ad",
        "status": "pending",
        "created_at":"2021-10-10T00:00:00",
        "updated_at":"2021-10-10T00:00:00",
        "deleted_at":None,
    }
    )]
    mock_user_repository.return_value.getAll.return_value = response_user_entity

    response = get_user_use_case({"all": "true"})

    assert response == response_user_entity

def test_get_user_use_case_value_error(mock_user_repository):
    """Test get user use case raises ValueError."""
    from src.use_cases.user.get_user import get_user_use_case

    with pytest.raises(ValueError, match="Invalid values"):
        get_user_use_case({"all": "false"})