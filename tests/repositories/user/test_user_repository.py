import pytest
from unittest.mock import MagicMock, patch
from src.repositories.user.user_repository import UserRepository


@pytest.fixture
def user_repository():
    """Fixture para inicializar el UserRepository con un mock de DocumentDBAdapter."""
    with patch("src.repositories.user.user_repository.DocumentDBAdapter") as MockAdapter:
        mock_adapter = MockAdapter.return_value
        mock_adapter.get_collection.return_value = MagicMock()
        return UserRepository()


def test_save_user_success(user_repository):
    """Test para guardar un usuario correctamente."""
    mock_collection = user_repository.collection

    # Simular que no existe un usuario con el mismo email
    mock_collection.find_one.return_value = None

    # Simular que la inserción es exitosa
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

    # Validar resultados
    assert response["message"] == "User created successfully"
    assert response["body"]["user"]["_id"] == "mocked_id"
    assert "uuid" in response["body"]["user"]

    # Verificar llamadas a los métodos mockeados
    mock_collection.find_one.assert_called_once_with({"email": user_data["email"]})
    mock_collection.insert_one.assert_called_once_with(user_data)


def test_save_user_existing_email(user_repository):
    """Test para manejar el caso en el que ya existe un usuario con el mismo email."""
    mock_collection = user_repository.collection

    # Simular que ya existe un usuario con el email proporcionado
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

    # Verificar que no se intentó insertar un nuevo documento
    mock_collection.insert_one.assert_not_called()


def test_save_user_general_exception(user_repository):
    """Test para manejar excepciones generales durante la operación."""
    mock_collection = user_repository.collection

    # Simular que ocurre una excepción durante la inserción
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

    # Verificar que se intentó insertar el documento
    mock_collection.find_one.assert_called_once_with({"email": user_data["email"]})
    mock_collection.insert_one.assert_called_once_with(user_data)
