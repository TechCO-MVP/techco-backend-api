from src.domain.business import BusinessEntity
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.user_repository import UserRepository


def get_business_by_id_use_case(business_id: str, email: str) -> BusinessEntity:
    user_repository = UserRepository()
    user_entity = user_repository.getByEmail(email)

    if user_entity is None:
        raise EntityNotFound("User", email)

    business_repository = BusinessRepository()
    business_entity = business_repository.getById(business_id)

    if business_entity is None:
        raise EntityNotFound("Business", business_id)

    parent_business_id = business_entity.get_parent_business_id()

    if parent_business_id not in [business.business_id for business in user_entity.props.roles]:
        raise ValueError("User does not have access to this business")

    return business_entity
