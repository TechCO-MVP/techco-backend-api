from typing import List

from src.domain.business import BusinessEntity
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.user_repository import UserRepository


def list_businesses_use_case(email: str) -> List[BusinessEntity]:
    """
    List businesses by user
    """
    user_repository = UserRepository()
    user_entity = user_repository.getByEmail(email)

    if user_entity is None:
        raise EntityNotFound("User", email)

    parent_business_id = user_entity.props.business_id
    business_repository = BusinessRepository()

    parent_business = business_repository.getById(parent_business_id)
    if parent_business is None:
        raise EntityNotFound("Business", parent_business_id)

    businesses = business_repository.getAll({"parent_business_id": parent_business_id})

    return [parent_business] + businesses
