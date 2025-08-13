from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)
from src.repositories.document_db.user_repository import UserRepository
from src.domain.position_configuration import PositionConfigurationEntity
from src.domain.role import Role

from src.utils.index import get_role_business


def get_position_configuration_use_case(
    params: dict, user_email: str
) -> list[PositionConfigurationEntity]:
    """get position use case."""
    position_configuration_repository = PositionConfigurationRepository()

    if id := params.get("id"):
        return [position_configuration_repository.getById(id)]
    elif params["all"].lower() == "true":
        user_repository = UserRepository()
        user_entity = user_repository.getByEmail(user_email)

        business_id = params["business_id"]
        if not business_id:
            raise ValueError("Business ID is required")

        role = get_role_business(user_entity, business_id)

        if not role:
            raise ValueError("Role not found for the given business id")

        if role.role in [Role.SUPER_ADMIN.value, Role.BUSINESS_ADMIN.value]:
            return get_position_configuration_for_admin_use_case(
                params, position_configuration_repository
            )

        query = {"user_id": user_entity.id, "business_id": params["business_id"]}
        position_configurations = position_configuration_repository.getAll(query)
        return position_configurations
    else:
        raise ValueError("Invalid values")


def get_position_configuration_for_admin_use_case(
    params: dict, position_configuration_repository: PositionConfigurationRepository
) -> list[PositionConfigurationEntity]:
    """Get position configuration for admin use case."""

    query = {"business_id": params["business_id"]}
    return position_configuration_repository.getAll(query)
