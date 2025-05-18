from src.domain.position import PositionEntity, POSITION_STATUS
from src.domain.position_configuration import PositionConfigurationEntity
from src.domain.role import Role
from src.domain.user import UserEntity
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)
from src.repositories.document_db.position_repository import (
    PositionRepository,
)



def delete_position_configuration_use_case(
    position_id: str, user_entity: UserEntity
) -> None | ValueError:
    """delete position configuration use case."""

    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = position_configuration_repository.getById(position_id)

    if not position_configuration_entity:
        raise ValueError("Position configuration not found")

    if position_configuration_entity.props.user_id != user_entity.id:
        check_user_has_permission_to_delete_position_configuration(user_entity, position_configuration_entity)


    position_repository = PositionRepository()
    position_entity: PositionEntity = position_repository.getByPositionConfigirationId(position_configuration_entity.id)

    if position_entity and position_entity.props.status == POSITION_STATUS.ACTIVE:
        raise ValueError("Position is active, cannot delete position configuration")

    position_configuration_repository.delete(position_configuration_entity.id)

    return

def check_user_has_permission_to_delete_position_configuration(
    user_entity: UserEntity,
    position_configuration_entity: PositionConfigurationEntity
) -> None | ValueError:
    """check if user has permission to delete position configuration."""
    for role in user_entity.props.roles:
        if (
            role.business_id == position_configuration_entity.props.business_id
            and role.role in [Role.SUPER_ADMIN, Role.BUSINESS_ADMIN]
        ):
            return

    raise ValueError("User does not have permission to delete this position configuration")
