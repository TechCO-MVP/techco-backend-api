from src.repositories.document_db.position_configuration_repository import PositionConfigurationRepository
from src.domain.position_configuration import PositionConfigurationEntity
from src.domain.base_entity import from_dto_to_entity


def put_position_configuration_use_case(position_configuration_dto: dict) -> PositionConfigurationEntity:
    """update position configuration use case."""
    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = from_dto_to_entity(PositionConfigurationEntity, position_configuration_dto)
    
    return position_configuration_repository.update(position_configuration_entity.id, position_configuration_entity)
