from src.repositories.document_db.user_repository import UserRepository
from src.domain.position_configuration import STATUS
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
    PositionConfigurationEntity,
)


def complete_phase_position_configuration_use_case(
    position_configuration_id: str,
    data: dict,
    user_email: str,
) -> PositionConfigurationEntity:
    """Complete phase use case."""
    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = position_configuration_repository.getById(
        position_configuration_id
    )

    if not position_configuration_entity:
        raise ValueError("Position configuration not found")

    user_repository = UserRepository()
    user_entity = user_repository.getByEmail(user_email)

    if not user_entity:
        raise ValueError("User not found")

    business_id = position_configuration_entity.props.business_id
    role = next((r for r in user_entity.props.roles if r.business_id == business_id), None)
    if not role:
        raise ValueError("Role not found for the given business id")

    position_configuration_entity = complete_current_phase(position_configuration_entity, data)
    position_configuration_repository.update(
        position_configuration_id, position_configuration_entity
    )

    return position_configuration_entity


def complete_current_phase(
    position_configuration_entity: PositionConfigurationEntity,
    data: dict,
) -> PositionConfigurationEntity:
    """Complete current phase."""
    current_phase = position_configuration_entity.props.current_phase

    for phase in position_configuration_entity.props.phases:
        if phase.name == current_phase:
            if phase.status == STATUS.COMPLETED:
                raise ValueError("Phase already completed")

            phase.status = STATUS.COMPLETED
            phase.data = data

    return position_configuration_entity
