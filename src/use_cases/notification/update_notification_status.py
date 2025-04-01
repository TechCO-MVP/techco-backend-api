from datetime import datetime

from src.repositories.document_db.notification_repository import NotificationRepository
from src.domain.notification import UpdateNotificationStatusDTO


def put_notificationr_status_use_case(notification_dto: UpdateNotificationStatusDTO) -> bool:
    """put notification status use case."""
    notification_repository = NotificationRepository()

    notification = notification_repository.getById(notification_dto.notification_id)
    
    if not notification:
        raise ValueError("Notification not found")
    
    notification.props.status = notification_dto.status
    notification.props.read_at = datetime.now().isoformat()
    notification_repository.update(notification_dto.notification_id, notification)
    
    return True
