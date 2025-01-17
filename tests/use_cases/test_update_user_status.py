import pytest


@pytest.fixture
def mock_user_repository(mocker):
    mock_repo = mocker.patch("src.use_cases.user.update_user_status.UserRepository")
    return mock_repo

@pytest.fixture
def mock_cognito_client(mocker):
    mock_client = mocker.patch("src.use_cases.user.update_user_status.boto3.client")
    return mock_client

@pytest.fixture
def mock_user_entity():
    from src.domain.user import UserEntity
    return UserEntity(
        props={
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "company_position": "Developer",
            "business_id": "6778c3fa49a61649b054659d",
            "roles": [{"role": "recruiter", "business_id": "6778c3fa49a61649b054659d"}],
            "_id": "6778c3fa49a61649b054867834ad",
            "status": "pending",
            "created_at": "2021-10-10T00:00:00",
            "updated_at": "2021-10-10T00:00:00",
            "deleted_at": None,
        }
    )

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("COGNITO_USER_POOL_ID", "fake-user-pool-id")
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")

def test_put_user_status_use_case_success(mock_user_repository, mock_user_entity):
    """Test put user status use case success."""
    from src.use_cases.user.update_user_status import put_user_status_use_case
    from src.domain.user import UpdateUserStatusDTO

    mock_user_repository.return_value.getByEmail.return_value = mock_user_entity
    mock_user_repository.return_value.update.return_value = mock_user_entity

    user_dto = UpdateUserStatusDTO(
        user_id="6778c3fa49a61649b054867834ad",
        user_email="john.doe@example.com",
        user_status="enabled"
    )

    response = put_user_status_use_case(user_dto)

    assert response == mock_user_entity
    assert mock_user_entity.props.status == "enabled"

def test_user_sign_out_success(mock_cognito_client):
    """Test user sign out success."""
    from src.use_cases.user.update_user_status import user_sign_out

    mock_cognito_client.return_value.list_users.return_value = {
        'Users': [{
            'Attributes': [{'Name': 'sub', 'Value': 'user-sub-value'}]
        }]
    }

    user_sign_out("john.doe@example.com")

    mock_cognito_client.return_value.admin_user_global_sign_out.assert_called_once_with(
        UserPoolId="fake-user-pool-id",
        Username="user-sub-value"
    )

def test_user_sign_out_user_not_found(mock_cognito_client):
    """Test user sign out user not found."""
    from src.use_cases.user.update_user_status import user_sign_out

    mock_cognito_client.return_value.list_users.return_value = {
        'Users': []
    }

    with pytest.raises(ValueError, match="User not found"):
        user_sign_out("john.doe@example.com")