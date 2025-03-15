from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity


def get_user_use_case(params: dict) -> UserEntity:
    """get user use case."""
    user_repository = UserRepository()

    if id := params.get("id"):
        return user_repository.getById(id)
    elif params["all"].lower() == "true":
        return user_repository.getAll(params)
    else:
        raise ValueError("Invalid values")
