from aws_lambda_powertools import Logger

from src.domain.profile import PROCESS_TYPE
from src.domain.notification import NotificationDTO, NotificationType, NotificationStatus
from src.domain.business import PHASE_CLASSIFICATION
from src.repositories.document_db.position_repository import PositionRepository
from src.utils.send_notification_by_websocket import send_notification_by_websocket

logger = Logger()


def lambda_handler(event: dict, _):
    """
    Notify the completion of the profile filter process.
    """
    try:
        logger.info("Notifying completion of profile filter process")
        logger.info(event)

        process_id: str = event.get("_id", None)
        if not process_id:
            raise Exception("The id is required")
        
        send_message_to_websocket_by_position_id(event)

        return event
    except Exception as e:
        logger.error(f"Error notifying completion of profile filter process: {e}")
        return {
            "status": "ERROR",
            "errorInfo": "Error notifying completion of profile filter process",
            "errorDetails": f"{e}",
        }

def send_message_to_websocket_by_position_id(event):
    """ Build message to send to WebSocket connection by prosition_id
    """
    position_repository = PositionRepository()
    position = position_repository.getById(event["position_id"])    
    user_to_notify = [position.props.owner_position_user_id]
    recruiter_user_id = position.props.recruiter_user_id

    if recruiter_user_id:
        user_to_notify.append(recruiter_user_id)
    
    responsible_users = [user.user_id for user in position.props.responsible_users]
    user_to_notify.extend(responsible_users)

    if event["type"] == PROCESS_TYPE.PROFILES_SEARCH.value:
        notification_message = f"¡Listo tu tablero de seguimiento! Ya puedes hacer seguimiento a la vacante {event['process_filters']['role']} desde tu nuevo tablero."
        phase_type = PHASE_CLASSIFICATION.CALL_TO_ACTION.value
    else:
        notification_message = f"Tu vacante {event['process_filters']['role']} está llamando la atención. ¡Se ha postulado un nuevo candidato."
        phase_type = PHASE_CLASSIFICATION.INFORMATIVE.value
    
    for user in set(user_to_notify):
        notification = NotificationDTO(
            user_id=user,
            business_id=event["business_id"],
            message=notification_message,
            notification_type=NotificationType.PROFILE_FILTER_PROCESS,
            status=NotificationStatus.NEW,
            position_id=position.id,
            phase_type=phase_type,
        )
        
        send_notification_by_websocket(notification)
