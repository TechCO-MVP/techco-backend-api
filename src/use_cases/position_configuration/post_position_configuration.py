from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.position.configuration import assistant_phase_mapping, position_configuration
from src.domain.position_configuration import (
    FLOW_TYPE,
    PHASE_TYPE,
    Phase,
    PositionConfigurationDTO,
    PositionConfigurationEntity,
)
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)


def post_position_configuration_use_case(
    business_id: str, flow_type: FLOW_TYPE, user_id: str
) -> PositionConfigurationEntity:
    """create position configuration use case."""
    position_configuration_dto = PositionConfigurationDTO(
        user_id=user_id,
        business_id=business_id,
        flow_type=flow_type,
    )
    position_configuration_dto.phases = create_position_phases(position_configuration_dto)

    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = PositionConfigurationEntity(props=position_configuration_dto)

    return position_configuration_repository.create(position_configuration_entity)


def create_position_phases(
    position_configuration_dto: PositionConfigurationDTO,
) -> list[dict]:
    """create position phases."""
    return position_configuration["flow_type"][position_configuration_dto.flow_type]


def create_ai_phases(
    position_configuration_dto: PositionConfigurationDTO,
) -> list[Phase]:
    """create ai phases."""
    phases = position_configuration["phases"]
    for phase in phases:
        if phase.type == PHASE_TYPE.DESCRIPTION:
            phase.thread_id = initialize_assistant(
                position_configuration_dto=position_configuration_dto,
                phase_type=PHASE_TYPE.DESCRIPTION,
            )

    return phases


def create_custom_phases(
    _: PositionConfigurationDTO,
) -> list[Phase]:
    """create custom phases."""
    phases = position_configuration["phases"]
    return phases


def create_other_position_phases(
    _: PositionConfigurationDTO,
) -> list[Phase]:
    """create other position phases."""
    phases = position_configuration["phases"]
    return phases


def initialize_assistant(
    position_configuration_dto: PositionConfigurationDTO, phase_type: PHASE_TYPE
) -> str:
    """initialize assistant."""
    business_repository = BusinessRepository()
    business = business_repository.getById(position_configuration_dto.business_id)
    if not business:
        raise ValueError("Business does not exist")

    assistant_type = assistant_phase_mapping.get(phase_type)
    if not assistant_type:
        raise ValueError("Assistant type does not exist")

    assistant = business.props.assistants[assistant_type]

    if not assistant:
        raise ValueError("Assistant does not exist")

    open_ai_adapter = OpenAIAdapter()
    thread_run = open_ai_adapter.initialize_assistant_thread(assistant.assistant_id)

    return thread_run.thread_id
