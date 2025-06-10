from src.domain.business import BusinessEntity
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.business_repository import BusinessRepository


def get_business_only_with_id_use_case(business_id: str) -> BusinessEntity:
    business_repository = BusinessRepository()
    business_entity = business_repository.getById(business_id)

    if business_entity is None:
        raise EntityNotFound("Business", business_id)

    return business_entity