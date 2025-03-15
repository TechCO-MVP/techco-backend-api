from src.domain.business import BusinessDTO, BusinessEntity
from src.repositories.document_db.business_repository import BusinessRepository


def create_business_use_case(business_dto: BusinessDTO) -> BusinessEntity:
    business_repository = BusinessRepository()

    if business_dto.is_admin:
        raise ValueError("Businesses cannot be created as admin")

    if not business_dto.parent_business_id:
        raise ValueError("Businesses must have a parent business")

    parent_business_id = business_dto.parent_business_id
    parent_business = business_repository.getById(parent_business_id)

    if not parent_business:
        raise ValueError("Parent business does not exist")

    business_entity = BusinessEntity(props=business_dto)
    return business_repository.create(business_entity)
