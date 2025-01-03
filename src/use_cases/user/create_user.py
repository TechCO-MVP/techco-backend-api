from src.domain.user import UserDTO, UserEntity
from src.repositories.user.user_repository import UserRepository


def create_user_use_case(user_dto: UserDTO) -> dict:
    """Create user use case."""
    user_repository = UserRepository()
    user_data = UserEntity(props=user_dto).to_dto(flat=True)
    
    return user_repository.save_user(user_data)
