from src.repositories.document_db.notification_repository import NotificationRepository
from src.domain.user import UserEntity
from src.use_cases.notification.build_notification_response import (
    build_notification_response_use_case,
)


def get_notification_use_case(user: UserEntity) -> dict:
    """get notification use case."""

    notification_repository = NotificationRepository()
    notifications = notification_repository.getAll({"user_id": user.id})
    build_response = [build_notification_response_use_case(notification) for notification in notifications]
    return build_response.reverse()
