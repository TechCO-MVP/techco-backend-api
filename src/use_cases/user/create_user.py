from src.domain.user import UserDTO, UserEntity, UserStatus
from src.repositories.document_db.user_repository import UserRepository
from src.repositories.document_db.business_repository import BusinessRepository


def create_user_use_case(user_dto: UserDTO, business_id: str) -> dict:
    """Create user use case."""
    business_repository = BusinessRepository()
    business_entity = business_repository.getById(business_id)

    if business_entity is None:
        raise ValueError("Business not found")

    if not business_entity.props.is_admin:
        business_id = business_entity.props.parent_business_id

    user_dto.business_id = business_id

    user_repository = UserRepository()
    user_dto.status = UserStatus.PENDING
    user_entity = UserEntity(props=user_dto)

    return user_repository.create(user_entity)
