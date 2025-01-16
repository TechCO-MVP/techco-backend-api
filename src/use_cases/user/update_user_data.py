from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity, UpdateUserDTO

def put_user_data_use_case(user_data: dict) -> UserEntity:
    """put user data use case."""
    user_repository = UserRepository()
    user_data_db = user_repository.getByEmail(user_data["user_email"])

    if user_data.get("user_full_name"):
        user_data_db.props.full_name = user_data["user_full_name"]
    if user_data.get("user_roles")[0].get("role"):
        user_data_db.props.roles[0].role = user_data["user_roles"][0].get("role")

    return user_repository.update(user_data["user_id"], user_data_db)
