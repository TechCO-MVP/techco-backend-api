from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.position.configuration import get_assistant_for_phase
from src.domain.position_configuration import STATUS, TYPE, PositionConfigurationDTO
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationEntity,
    PositionConfigurationRepository,
)
from src.repositories.document_db.user_repository import UserRepository


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
    if not role:
        raise ValueError("Role not found for the given business id")

    position_configuration_entity = start_phase(
        next_phase(position_configuration_entity, configuration_type)
    )
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

    if current_phase is None:
        current_phase = position_configuration_entity.props.phases[0]
        current_phase.status = STATUS.IN_PROGRESS
        current_phase.configuration_type = configuration_type
        position_configuration_entity.props.current_phase = current_phase.type
        position_configuration_entity.props.phases[0] = current_phase

        return position_configuration_entity

    index, phase = next(
        (
            (idx, phase)
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


def start_phase(
    position_configuration_entity: PositionConfigurationEntity,
) -> PositionConfigurationDTO:
    """Start phase."""
    current_phase = position_configuration_entity.props.current_phase

    index, phase = next(
        (
            (idx, phase)
            for idx, phase in enumerate(position_configuration_entity.props.phases)
            if phase.type == current_phase
        ),
        (None, None),
    )

    if phase.configuration_type == TYPE.AI_TEMPLATE:
        if phase.thread_id:
            raise ValueError("Thread already exists")

        assistant_id = get_assistant_for_phase[phase.type](
            position_configuration_entity, phase.type
        )
        open_ai_adapter = OpenAIAdapter()
        thread_run = open_ai_adapter.initialize_assistant_thread(assistant_id)

        phase.thread_id = thread_run.thread_id
        position_configuration_entity.props.phases[index] = phase

    return position_configuration_entity
