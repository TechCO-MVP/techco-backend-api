from src.domain.position import PositionEntity
from src.repositories.document_db.position_repository import PositionRepository


def get_position_entity_use_case(params: dict) -> PositionEntity:
    """get position use case."""
    position_repository = PositionRepository()
    return position_repository.getById(params["id"])
