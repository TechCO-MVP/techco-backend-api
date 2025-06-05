from aws_lambda_powertools import Logger

from src.domain.business import BusinessDTO, BusinessEntity
from src.domain.role import BusinessRole, Role
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.user_repository import UserRepository
from src.use_cases.business.create_admin_business import create_assistants_for_business
from src.constants.business.configuration import base_position_flows

logger = Logger("CreateBusinessUseCase")


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

    business_dto.position_flows = base_position_flows.copy()

    business_entity = BusinessEntity(props=business_dto)
    business_created = business_repository.create(business_entity)
    add_role_to_admin_user(business_entity)

    return business_created


def add_role_to_admin_user(business_entity: BusinessEntity):
    """Add role to admin user."""
    user_repository = UserRepository()
    user_admin = user_repository.get_admin_user_by_business_id(
        business_entity.props.parent_business_id
    )

    if user_admin:
        logger.info(
            f"Adding role to super_admin user {user_admin.id} for business {business_entity.id}"
        )
        user_admin.props.roles.append(
            BusinessRole(business_id=business_entity.id, role=Role.BUSINESS_ADMIN.value)
        )
        user_repository.update(user_admin.id, user_admin)
