from src.domain.position import PositionEntity
from src.domain.position_configuration import PHASE_TYPE
from src.repositories.document_db.user_repository import UserRepository
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)


def create_position_use_case(
    position_configuration_id: str,
    user_email: str,
) -> PositionEntity:
    """
    Use case to create a position based on a position configuration.
    """
    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = position_configuration_repository.getById(
        position_configuration_id
    )

    if not position_configuration_entity:
        raise ValueError("Position configuration not found")

    if position_configuration_entity.props.current_phase not in [
        PHASE_TYPE.FINAL_INTERVIEW,
        PHASE_TYPE.READY_TO_PUBLISH,
    ]:
        raise ValueError("Position configuration is not in a valid phase to create a position")

    user_repository = UserRepository()
    user_entity = user_repository.getByEmail(user_email)
    if not user_entity:
        raise ValueError("User not found")

    business_id = position_configuration_entity.props.business_id
    role = next((r for r in user_entity.props.roles if r.business_id == business_id), None)
    if not role:
        raise ValueError("Role not found for the given business id")

    position_entity = PositionRepository.getAll(
        {position_configuration_id: position_configuration_id}
    )
    if position_entity:
        raise ValueError("Position already exists for this configuration")

    return {
        "position_configuration_id": position_configuration_id,
        "user_email": user_email,
        "status": "created",
    }
