from src.domain.user import UserDTO, UserEntity
from src.repositories.user.user_repository import UserRepository


def create_user_use_case(user_dto: UserDTO) -> UserEntity:
    user_repository = UserRepository()
    user_entity = UserEntity(props=user_dto)

    return user_repository.save_user(user_entity)
