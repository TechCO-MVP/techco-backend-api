from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)
from src.repositories.document_db.user_repository import UserRepository
from src.domain.position_configuration import PositionConfigurationEntity


def get_position_configuration_use_case(
    params: dict, user_email: str
) -> list[PositionConfigurationEntity]:
    """get position use case."""
    position_configuration_repository = PositionConfigurationRepository()

    if id := params.get("id"):
        return [position_configuration_repository.getById(id)]
    elif params["all"].lower() == "true":
        user_repository = UserRepository()
        user_entity = user_repository.getByEmail(user_email)
        query = {"user_id": user_entity.id, "business_id": params["business_id"]}
        position_configurations = position_configuration_repository.getAll(query)
        return position_configurations.reverse()
    else:
        raise ValueError("Invalid values")
