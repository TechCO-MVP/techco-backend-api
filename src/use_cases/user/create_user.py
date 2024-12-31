from src.domain.user import UserDTO, UserEntity
from src.repositories.document_db.business_repository import BusinessRepository


def create_user_use_case(user_dto: UserDTO) -> UserEntity:
    business_repository = BusinessRepository()
    user_entity = UserEntity(props=user_dto)

    return business_repository.create(user_entity).to_dto()
