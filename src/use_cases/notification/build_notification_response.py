from src.repositories.document_db.hiring_process_repository import HiringProcessDBAdapter
from src.domain.hiring_process import HiringProcessEntity
from src.repositories.document_db.position_repository import PositionDBAdapter
from src.domain.position import PositionEntity
from src.domain.notification import NotificationEntity



def build_notification_response_use_case(notifications: NotificationEntity) -> dict:
    """build notification response use case."""
    hiring_process_repository = HiringProcessDBAdapter()
    notification_response = notifications.to_dto(flat=True)

    if notifications.props.hiring_process_id:
        hiring_process: HiringProcessEntity = hiring_process_repository.getById(notifications.props.hiring_process_id)
        notification_response["card_id"] = hiring_process.props.card_id
        notification_response["profile_name"] = hiring_process.props.profile.name
    
        position: PositionEntity = PositionDBAdapter().getById(hiring_process.props.position_id)
        notification_response["pipe_id"] = position.props.pipe_id
        notification_response["position_name"] = position.props.role

    return notification_response
