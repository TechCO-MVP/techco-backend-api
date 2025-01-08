from unittest.mock import MagicMock

import pytest
from bson.objectid import ObjectId

from src.domain.user import UserDTO, UserEntity


@pytest.fixture
def user_dto():
    return UserDTO(
        full_name="John Doe",
        email="john.doe@example.com",
        company_position="Developer",
        role="Admin",
        business="TechCo",
        business_id="6778c3fa49a61649b054659d",
    )


@pytest.fixture
def user_entity(user_dto):
    return UserEntity(props=user_dto)


@pytest.fixture
def mock_db_client(mocker):
    mock_client = mocker.patch(
        "src.repositories.document_db.client.DocumentDBClient.create_documentdb_database_client",
    )
    return mock_client


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("REGION_NAME", "fake-region")
    monkeypatch.setenv("CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("ENV", "tests")


def test_create_user_success(mocker, user_entity, mock_db_client):
    """Test successful creation of a user."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.side_effect = [
        None,
        {"_id": "6778c3fa49a61649b054659d", "name": "John Doe company"},
    ]
    mock_collection.insert_one.return_value.inserted_id = "mock_id"

    adapter = UserDocumentDBAdapter()
    response = adapter.create(user_entity)

    assert response["message"] == "User created successfully"
    assert response["body"]["user"]["_id"] == "mock_id"
    calls = [
        mocker.call({"email": user_entity.props.email}),
        mocker.call({"_id": ObjectId(user_entity.props.business_id)}),
    ]
    mock_collection.find_one.assert_has_calls(calls)


def test_create_user_already_exists(mocker, user_entity, mock_db_client):
    """Test creation of a user that already exists."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

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
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

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
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find.return_value = [
        {
            "_id": "1",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "business_id": "6778c3fa49a61649b054659d",
            "company_position": "recluter",
            "rol": "recluter",
            "status": "Active",
        },
        {
            "_id": "2",
            "full_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "business_id": "6778c3fa49a61649b054659d",
            "company_position": "recluter",
            "rol": "recñluter",
            "status": "Active",
        },
    ]

    adapter = UserDocumentDBAdapter()
    users = adapter.getAll({"business_id": "6778c3fa49a61649b054659d"})
    data = users["body"]["data"]

    assert users["message"] == "Users found successfully"
    assert len(data) == 2
    assert data[0]["full_name"] == "John Doe"
    assert data[1]["full_name"] == "Jane Doe"
    mock_collection.find.assert_called_once()


def test_get_all_users_not_users(mocker, mock_db_client):
    """Test getAll function -> not user."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find.return_value = []

    adapter = UserDocumentDBAdapter()
    users = adapter.getAll({"business_id": "6778c3fa49a61649b054659d"})
    data = users["body"]["data"]

    assert users["message"] == "Users not found"
    assert len(data) == 0
    mock_collection.find.assert_called_once()


def test_get_by_id(mocker, mock_db_client):
    """Test getById function."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {
        "_id": "6778c3fa49a61649b054659d",
        "business_id": "6778c3fa49a61649b054659d",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
    }

    adapter = UserDocumentDBAdapter()
    user = adapter.getById("6778c3fa49a61649b054659d")
    data = user["body"]["data"]

    assert user["message"] == "User found successfully"
    assert data[0]["email"] == "john.doe@example.com"
    assert data[0]["full_name"] == "John Doe"
    mock_collection.find_one.assert_called_once_with({"_id": ObjectId("6778c3fa49a61649b054659d")})


def test_get_by_id_not_found_user(mocker, mock_db_client):
    """Test getById function not users."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection
    mock_collection.find_one.return_value = {}

    adapter = UserDocumentDBAdapter()
    with pytest.raises(ValueError, match="User not found"):
        adapter.getById("6778c3fa49a61649b054659d")

    mock_collection.find_one.assert_called_once_with({"_id": ObjectId("6778c3fa49a61649b054659d")})


def test_update_user(mocker, user_entity, mock_db_client):
    """Test update function."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection

    adapter = UserDocumentDBAdapter()
    adapter.update("1", user_entity)

    mock_collection.update_one.assert_called_once_with({"_id": "1"}, {"$set": user_entity.to_dto()})


def test_delete_user(mocker, mock_db_client):
    """Test delete function."""
    from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter

    mock_collection = MagicMock()
    mock_db_client.return_value.__getitem__.return_value = mock_collection

    adapter = UserDocumentDBAdapter()
    adapter.delete("1")

    mock_collection.delete_one.assert_called_once_with({"_id": "1"})
