from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UpdateUserEntity

def put_user_status_use_case(dto) -> UpdateUserEntity:
    """put user status use case."""
    user_repository = UserRepository()
    user_id = dto.id
    entity = UpdateUserEntity(props=dto)

    return user_repository.update(user_id, entity)
