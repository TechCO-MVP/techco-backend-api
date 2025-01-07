import pytest

from src.domain.user import UserDTO, UserEntity


@pytest.fixture
def user_dto():
    return UserDTO(
        full_name="John Doe",
        email="john.doe@example.com",
        company_position="Developer",
        rol="Admin",
        business_id="12345",
    )


@pytest.fixture
def user_entity(user_dto):
    return UserEntity(props=user_dto)


@pytest.fixture
def mock_adapter(mocker):
    mock_adapter = mocker.patch(
        "src.repositories.document_db.user_repository.UserDocumentDBAdapter"
    )
    return mock_adapter

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")


def test_get_all_users(mock_adapter):
    """Test getAll function."""
    from src.repositories.document_db.user_repository import UserRepository

    mock_adapter.return_value.getAll.return_value = [
        {"_id": "1", "full_name": "John Doe", "email": "john.doe@example.com"},
        {"_id": "2", "full_name": "Jane Doe", "email": "jane.doe@example.com"},
    ]

    repository = UserRepository()
    users = repository.getAll({})

    assert len(users) == 2
    assert users[0]["full_name"] == "John Doe"
    assert users[1]["full_name"] == "Jane Doe"
    mock_adapter.return_value.getAll.assert_called_once()


def test_get_by_id(mock_adapter):
    """Test getById function."""
    from src.repositories.document_db.user_repository import UserRepository

    mock_adapter.return_value.getById.return_value = {
        "_id": "1",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
    }

    repository = UserRepository()
    user = repository.getById("1")

    assert user["_id"] == "1"
    assert user["full_name"] == "John Doe"
    mock_adapter.return_value.getById.assert_called_once_with("1")


def test_create_user(mock_adapter, user_entity):
    """Test create function."""
    from src.repositories.document_db.user_repository import UserRepository

    mock_adapter.return_value.create.return_value = {
        "message": "User created successfully",
        "body": {"user": {"_id": "mock_id"}},
    }

    repository = UserRepository()
    response = repository.create(user_entity)

    assert response["message"] == "User created successfully"
    assert response["body"]["user"]["_id"] == "mock_id"
    mock_adapter.return_value.create.assert_called_once_with(user_entity)


def test_update_user(mock_adapter, user_entity):
    """Test update function."""
    from src.repositories.document_db.user_repository import UserRepository

    repository = UserRepository()
    repository.update("1", user_entity)

    mock_adapter.return_value.update.assert_called_once_with("1", user_entity)


def test_delete_user(mock_adapter):
    """Test delete function."""
    from src.repositories.document_db.user_repository import UserRepository
    
    repository = UserRepository()
    repository.delete("1")

    mock_adapter.return_value.delete.assert_called_once_with("1")
