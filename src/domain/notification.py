from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.domain.base_entity import BaseEntity


class NotificationStatus(str, Enum):
    NEW = "NEW"
    READ = "READ"
    REVIEWED = "REVIEWED"


class NotificationType(str, Enum):
    PHASE_CHANGE = "PHASE_CHANGE"
    TAGGED_IN_COMMENT = "TAGGED_IN_COMMENT"
    PROFILE_FILTER_PROCESS = "PROFILE_FILTER_PROCESS"


class NotificationDTO(BaseModel):
    user_id: str = Field(default="", alias="user_id")
    business_id: str = Field(default="", alias="business_id")
    message: str
    notification_type: NotificationType
    status: NotificationStatus = NotificationStatus.NEW
    process: Optional[str] = Field(default="", alias="process")
    hiring_process_id: Optional[str] = Field(default="", alias="hiring_process_id")
    read_at: Optional[str] = Field(default=None, alias="read_at")
    phase_id: Optional[str] = Field(default="", alias="phase_id")


class UpdateNotificationStatusDTO(BaseModel):
    notification_id: str
    status: NotificationStatus


class NotificationEntity(BaseEntity[NotificationDTO]):
    pass
