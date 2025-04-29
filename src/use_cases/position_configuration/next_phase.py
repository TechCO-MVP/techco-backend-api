from src.repositories.document_db.user_repository import UserRepository
from src.domain.position_configuration import STATUS
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
    PositionConfigurationEntity,
)


def next_phase_position_configuration_use_case(
    position_configuration_id: str,
    configuration_type: str,
    user_email: str,
) -> PositionConfigurationEntity:
    """Next phase use case."""
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
    if role:
        raise ValueError("Role not found for the given business id")

    position_configuration_entity = next_phase(position_configuration_entity, configuration_type)
    position_configuration_repository.update(
        position_configuration_id, position_configuration_entity
    )

    return position_configuration_entity


def next_phase(
    position_configuration_entity: PositionConfigurationEntity,
    configuration_type: str,
) -> PositionConfigurationEntity:
    """Next phase."""
    current_phase = position_configuration_entity.props.current_phase
    phase, index = next(
        (
            (phase, idx)
            for idx, phase in enumerate(position_configuration_entity.props.phases)
            if phase.type == current_phase
        ),
        (None, None),
    )

    if not phase:
        raise ValueError("Current phase not found")

    if phase.status != STATUS.COMPLETED:
        raise ValueError("Current phase is not completed")

    if index + 1 >= len(position_configuration_entity.props.phases):
        raise ValueError("No more phases available")

    next_phase = position_configuration_entity.props.phases[index + 1]
    next_phase.status = STATUS.IN_PROGRESS
    next_phase.configuration_type = configuration_type
    position_configuration_entity.props.current_phase = next_phase.type
    position_configuration_entity.props.phases[index + 1] = next_phase

    return position_configuration_entity
