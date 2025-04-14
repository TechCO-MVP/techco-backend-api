from src.repositories.document_db.position_configuration_repository import PositionConfigurationRepository
from src.domain.position_configuration import PositionConfigurationEntity, PositionConfigurationDTO


def post_position_configuration_use_case(position_configuration_dto: PositionConfigurationDTO) -> list[dict]:
    """create position configuration use case."""
    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = PositionConfigurationEntity(props=position_configuration_dto)
    
    return position_configuration_repository.create(position_configuration_entity)
