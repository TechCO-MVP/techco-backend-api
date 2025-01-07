from src.repositories.document_db.user_repository import UserRepository


def get_user_use_case(params: dict) -> dict:
    """get user use case."""
    business_id = params["business_id"]
    user_repository = UserRepository()

    if id := params.get("id"):
        return user_repository.getById(id, business_id)
    elif params["all"].lower() == "true":
        return user_repository.getAll(business_id)
    else:
        raise ValueError("Invalid values")
