from src.repositories.document_db.position_repository import PositionRepository
from src.domain.position import PositionEntity, UpdatePositionStatusDTO


def put_position_status_use_case(position_status_dto: UpdatePositionStatusDTO) -> list[dict]:
    """get position use case."""
    position_repository = PositionRepository()
    
    position = position_repository.getById(position_status_dto.position_id)
    user_can_edit = validate_user_can_edit(position, position_status_dto.user_id)

    if not user_can_edit:
        raise ValueError("User is not allowed to edit this position")
    
    position.props.status = position_status_dto.position_status
    return position_repository.update(position.id, position)

def validate_user_can_edit(position: PositionEntity, user_id: str) -> bool:
    """Validate if the user can edit the position."""
    user_can_edit = False
    list_users = [position.props.owner_position_user_id]

    if position.props.recruiter_user_id:
        list_users.append(position.props.recruiter_user_id)
    
    for stakeholder in position.props.responsible_users:
        if stakeholder.user_id == user_id and stakeholder.can_edit:
            list_users.append(stakeholder.user_id)

    if user_id in list_users:
        user_can_edit = True
    
    return user_can_edit
