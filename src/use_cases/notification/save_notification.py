
from src.domain.notification import NotificationDTO, NotificationEntity
from src.repositories.document_db.notification_repository import NotificationRepository


def post_notification_use_case(notification_dto: NotificationDTO) -> None:
    """Post notification use case."""
    notification_repository = NotificationRepository()
    notification_entity = NotificationEntity(props=notification_dto)
    response = notification_repository.create(notification_entity)
    
    return response

