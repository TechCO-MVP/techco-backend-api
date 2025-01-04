from src.domain.business import BusinessEntity
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.user.user_repository import UserRepository
from src.errors.entity_not_found import EntityNotFound


def get_business_by_id_use_case(business_id: str, user_id: str) -> BusinessEntity:
    user_repository = UserRepository()
    user_entity = user_repository.getById(user_id)

    if user_entity is None:
        raise EntityNotFound("User", user_id)

    business_repository = BusinessRepository()
    business_entity = business_repository.getById(business_id)

    if business_entity is None:
        raise EntityNotFound("Business", business_id)

    parent_business_id = business_entity.get_parent_business_id()

    if parent_business_id != user_entity.props.business_id:
        raise ValueError("User does not have access to this business")

    return business_entity
