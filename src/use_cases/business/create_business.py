from src.domain.business import BusinessDTO, BusinessEntity
from src.repositories.document_db.business_repository import BusinessRepository


def create_business_use_case(business_dto: BusinessDTO) -> BusinessEntity:
    business_repository = BusinessRepository()
    business_entity = BusinessEntity(props=business_dto)

    return business_repository.create(business_entity)
