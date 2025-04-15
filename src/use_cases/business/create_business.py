from src.domain.business import BusinessDTO, BusinessEntity
from src.repositories.document_db.business_repository import BusinessRepository
from src.use_cases.business.create_admin_business import create_assistants_for_business


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

    assistants = create_assistants_for_business()
    business_dto.assistants = assistants

    business_entity = BusinessEntity(props=business_dto)
    return business_repository.create(business_entity)
