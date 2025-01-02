import pytest
from unittest.mock import MagicMock, patch
from src.repositories.user.user_repository import UserRepository


@pytest.fixture
def user_repository():
    """Fixture UserRepository mock DocumentDBAdapter."""
    with patch("src.repositories.user.user_repository.DocumentDBAdapter") as MockAdapter:
        mock_adapter = MockAdapter.return_value
        mock_adapter.get_collection.return_value = MagicMock()
        return UserRepository()


def test_save_user_success(user_repository):
    """Test save successfully."""
    mock_collection = user_repository.collection
    mock_collection.find_one.return_value = None

    mock_result = MagicMock()
    mock_result.inserted_id = "mocked_id"
    mock_collection.insert_one.return_value = mock_result

    user_data = {
        "email": "test@test.com",
        "full_name": "John Doe",
        "company_position": "Manager",
        "rol": "Admin",
        "business": "Test Corp",
        "business_id": "12345",
    }

    response = user_repository.save_user(user_data)
    assert response["message"] == "User created successfully"
    assert response["body"]["user"]["_id"] == "mocked_id"
    assert "uuid" in response["body"]["user"]

    mock_collection.find_one.assert_called_once_with({"email": user_data["email"]})
    mock_collection.insert_one.assert_called_once_with(user_data)


def test_save_user_existing_email(user_repository):
    """Test exists user."""
    mock_collection = user_repository.collection
    mock_collection.find_one.return_value = {"email": "test@test.com"}

    user_data = {
        "email": "test@test.com",
        "full_name": "John Doe",
        "company_position": "Manager",
        "rol": "Admin",
        "business": "Test Corp",
        "business_id": "12345",
    }

    with pytest.raises(ValueError, match="A user with this email already exists."):
        user_repository.save_user(user_data)

    mock_collection.insert_one.assert_not_called()


def test_save_user_general_exception(user_repository):
    """Test general exception."""
    mock_collection = user_repository.collection
    mock_collection.find_one.return_value = None
    mock_collection.insert_one.side_effect = Exception("Mocked database error")

    user_data = {
        "email": "test@test.com",
        "full_name": "John Doe",
        "company_position": "Manager",
        "rol": "Admin",
        "business": "Test Corp",
        "business_id": "12345",
    }

    with pytest.raises(Exception, match="Database error: Mocked database error"):
        user_repository.save_user(user_data)

    mock_collection.find_one.assert_called_once_with({"email": user_data["email"]})
    mock_collection.insert_one.assert_called_once_with(user_data)
