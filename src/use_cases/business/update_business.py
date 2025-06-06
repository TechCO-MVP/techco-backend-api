from src.domain.business import BusinessDTO, BusinessEntity
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.business_repository import BusinessRepository


def update_business_use_case(id: str, business_dto: BusinessDTO) -> BusinessEntity:
    business_repository = BusinessRepository()
    business_entity = business_repository.getById(id)

    if business_entity is None:
        raise EntityNotFound("Business", id)

    # Update properties except for is_admin and parent_business_id
    updated_props = {
        **business_entity.props.model_dump(
            exclude={"is_admin", "parent_business_id", "assistants"}
        ),
        **business_dto.model_dump(exclude={"is_admin", "parent_business_id", "assistants"}),
    }
    updated_props["is_admin"] = business_entity.props.is_admin
    updated_props["parent_business_id"] = business_entity.props.parent_business_id
    updated_props["assistants"] = business_entity.props.assistants
    updated_props["position_flows"] = business_entity.props.position_flows
    business_entity.props = updated_props

    return business_repository.update(business_entity.id, business_entity)
