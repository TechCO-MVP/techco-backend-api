from src.domain.user import UserDTO, UserEntity, UserStatus
from src.repositories.document_db.user_repository import UserRepository


def create_user_use_case(user_dto: UserDTO) -> dict:
    """Create user use case."""
    user_repository = UserRepository()
    user_dto.status = UserStatus.PENDING
    user_entity = UserEntity(props=user_dto)

    return user_repository.create(user_entity)
