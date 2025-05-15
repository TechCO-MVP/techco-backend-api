from src.constants.position.configuration import position_configuration
from src.domain.position_configuration import (
    FLOW_TYPE,
    STATUS,
    PositionConfigurationDTO,
    PositionConfigurationEntity,
)

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
        current_phase=None,
        status=STATUS.IN_PROGRESS,
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
