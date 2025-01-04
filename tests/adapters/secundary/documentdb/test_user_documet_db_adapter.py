from unittest.mock import MagicMock

import pytest

from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter
from src.domain.user import UserDTO, UserEntity


@pytest.fixture
def user_dto():
    return UserDTO(
        full_name="John Doe",
        email="john.doe@example.com",
        company_position="Developer",
        rol="Admin",
        business="TechCo",
        business_id="12345",
    )


@pytest.fixture
def user_entity(user_dto):
    return UserEntity(props=user_dto)


@pytest.fixture
def mock_db_client(mocker):
    mock_client = mocker.patch(
        "src.adapters.secondary.documentdb.user_db_adapter.create_documentdb_client"
    )
    return mock_client


def test_create_user_success(mocker, user_entity, mock_db_client):
    """Test successful creation of a user."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = None
    mock_collection.insert_one.return_value.inserted_id = "mock_id"

    adapter = UserDocumentDBAdapter()
    response = adapter.create(user_entity)

    assert response["message"] == "User created successfully"
    assert response["body"]["user"]["_id"] == "mock_id"
    mock_collection.find_one.assert_called_once_with({"email": user_entity.props.email})
    mock_collection.insert_one.assert_called_once()


def test_create_user_already_exists(mocker, user_entity, mock_db_client):
    """Test creation of a user that already exists."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {"email": user_entity.props.email}

    adapter = UserDocumentDBAdapter()

    with pytest.raises(ValueError, match="A user with this email already exists."):
        adapter.create(user_entity)

    mock_collection.find_one.assert_called_once_with({"email": user_entity.props.email})
    mock_collection.insert_one.assert_not_called()


def test_create_user_database_error(mocker, user_entity, mock_db_client):
    """Test creation of a user with a database error."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.side_effect = Exception("Database error")

    adapter = UserDocumentDBAdapter()

    with pytest.raises(Exception, match="Database error: Database error"):
        adapter.create(user_entity)

    mock_collection.find_one.assert_called_once_with({"email": user_entity.props.email})
    mock_collection.insert_one.assert_not_called()


def test_get_all_users(mocker, mock_db_client):
    """Test getAll function."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find.return_value = [
        {"_id": "1", "full_name": "John Doe", "email": "john.doe@example.com"},
        {"_id": "2", "full_name": "Jane Doe", "email": "jane.doe@example.com"},
    ]

    adapter = UserDocumentDBAdapter()
    users = adapter.getAll()

    assert len(users) == 2
    assert users[0]["full_name"] == "John Doe"
    assert users[1]["full_name"] == "Jane Doe"
    mock_collection.find.assert_called_once()


def test_get_by_id(mocker, mock_db_client):
    """Test getById function."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {
        "_id": "1",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
    }

    adapter = UserDocumentDBAdapter()
    user = adapter.getById("1")

    assert user["_id"] == "1"
    assert user["full_name"] == "John Doe"
    mock_collection.find_one.assert_called_once_with({"_id": "1"})


def test_update_user(mocker, user_entity, mock_db_client):
    """Test update function."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection

    adapter = UserDocumentDBAdapter()
    adapter.update("1", user_entity)

    mock_collection.update_one.assert_called_once_with({"_id": "1"}, {"$set": user_entity.to_dto()})


def test_delete_user(mocker, mock_db_client):
    """Test delete function."""
    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection

    adapter = UserDocumentDBAdapter()
    adapter.delete("1")

    mock_collection.delete_one.assert_called_once_with({"_id": "1"})
