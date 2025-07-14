from typing import Dict, List

from src.domain.position_configuration import PositionConfigurationEntity
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)
from src.repositories.document_db.user_repository import UserRepository


def get_position_configuration_by_business_use_case(business_id: str) -> list[dict]:
    """get position configuration by business use case."""
    position_configuration_repository = PositionConfigurationRepository()
    positions_configuration = position_configuration_repository.getAll({"business_id": business_id})
    
    return build_response(positions_configuration)


def build_response(
    positions_configuration: List[PositionConfigurationEntity],
) -> List[Dict]:
    """Build the response data for the positions configuration."""
    user_repository = UserRepository()
    response = []

    for position_configuration in positions_configuration:
        data = position_configuration.to_dto(flat=True)
        user = user_repository.getById(data["user_id"])
        data["creator_user_name"] = user.props.full_name
        response.append(data)

    return response
